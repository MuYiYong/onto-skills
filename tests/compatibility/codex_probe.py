"""Native discovery probe only; no model calls or persistent skill installation."""
import json
import hashlib
import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[2]


class LocalServer:
    def __init__(self, codex_home, cwd):
        Path(codex_home).mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, CODEX_HOME=str(codex_home))
        self.stderr = tempfile.TemporaryFile(mode='w+t', encoding='utf-8')
        self.proc = subprocess.Popen(
            ['codex', 'app-server', '--listen', 'stdio://'], cwd=cwd, env=env,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.stderr,
            text=True, encoding='utf-8')
        self.messages = queue.Queue()
        self.serial = 0
        threading.Thread(target=self._read, daemon=True).start()
        try:
            self.call('initialize', {'clientInfo': {'name': 'onto-compatibility', 'version': '0.1.0'}})
            self.send({'method': 'initialized'})
        except Exception:
            self.close()
            raise

    def _read(self):
        for line in self.proc.stdout:
            try:
                self.messages.put(json.loads(line))
            except json.JSONDecodeError:
                pass
        self.messages.put({'process_exited': True})

    def send(self, msg):
        self.proc.stdin.write(json.dumps(msg) + '\n')
        self.proc.stdin.flush()

    def call(self, method, params):
        self.serial += 1
        ident = self.serial
        self.send({'id': ident, 'method': method, 'params': params})
        deadline = time.monotonic() + 25
        while time.monotonic() < deadline:
            try:
                item = self.messages.get(timeout=max(0.01, deadline-time.monotonic()))
            except queue.Empty:
                break
            if item.get('process_exited'):
                self.stderr.seek(0)
                raise RuntimeError(f'Codex exited during {method}: {self.stderr.read()}')
            if item.get('id') == ident:
                if 'error' in item:
                    raise RuntimeError(item['error'])
                return item['result']
        raise TimeoutError(f'No terminal response for {method}; process={self.proc.poll()}')

    def close(self):
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()
        self.proc.stdin.close()
        self.proc.stdout.close()
        self.stderr.close()


def probe():
    version = subprocess.check_output(['codex', '--version'], text=True).strip()
    entries = sorted((ROOT / 'skills').glob('*/*/SKILL.md'))
    names = {e.parent.name for e in entries}
    results = []
    # Project .agents/skills is the documented location; CODEX_HOME/skills is
    # the compatibility location currently synchronized by CC-Switch.
    for scope in ('project', 'legacy-codex-home'):
        with tempfile.TemporaryDirectory(prefix='onto-skills-native-') as temp:
            base = Path(temp)
            project = base / 'project'
            project.mkdir()
            codex_home = base / 'codex-home'
            destination = project / '.agents/skills' if scope == 'project' else codex_home / 'skills'
            destination.mkdir(parents=True)
            for phase in ('single', 'multiple'):
                selected = entries[:1] if phase == 'single' else entries
                for entry in selected:
                    target = destination / entry.parent.name
                    if not target.exists():
                        shutil.copytree(entry.parent, target)
                server = LocalServer(codex_home, project)
                try:
                    response = server.call('skills/list', {'cwds': [str(project)], 'forceReload': True})
                finally:
                    server.close()
                data = response['data'][0]
                discovered = {s['name']: s for s in data['skills'] if s['name'] in names}
                expected = {e.parent.name for e in selected}
                if set(discovered) != expected:
                    raise AssertionError(f'{scope}/{phase}: expected {expected}, got {set(discovered)}')
                if data.get('errors'):
                    raise AssertionError(data['errors'])
                resources = 0
                package_hashes = {}
                for name, skill in discovered.items():
                    path = Path(skill['path'])
                    if not path.is_relative_to(destination) or not skill['enabled']:
                        raise AssertionError(f'Not loaded from isolated installation: {name}')
                    # Resource reads use paths returned by the actual native discovery API.
                    digest = hashlib.sha256()
                    for resource in sorted(path.parent.rglob('*')):
                        if resource.is_file():
                            digest.update(str(resource.relative_to(path.parent)).encode('utf-8'))
                            digest.update(b'\0')
                            digest.update(resource.read_bytes())
                            resources += 1
                    package_hashes[name] = digest.hexdigest()
                results.append({'scope': scope, 'phase': phase, 'skill_names': sorted(discovered),
                                'resource_files_read': resources, 'native_metadata_discovery': 'passed',
                                'package_sha256': package_hashes,
                                'model_invocation': 'not-run'})
    return {'codex_version': version, 'platform': os.uname().sysname,
            'results': results, 'limits': ['No model inference or implicit-trigger evaluation',
                'No CC-Switch GUI install/update/uninstall', 'No macOS runtime']}


if __name__ == '__main__':
    print(json.dumps(probe(), ensure_ascii=False, indent=2))
