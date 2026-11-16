"""Host-only regression checks with artificial source files and temporary cards.

This runs our shell script, never a firmware binary. It does not contact H13.
Only the source-app/version paths are substituted in a temporary script copy.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / 'card-root/rk_pcba_test_res/memtester_smd'
text = ORIGINAL.read_text()
subprocess.run(['sh', '-n', str(ORIGINAL)], check=True)
assert b'\r' not in ORIGINAL.read_bytes()
results = []

for label, arguments, invocation in [
    ('no arguments', [], 'absolute'),
    ('reference arguments', ['128m', '1'], 'absolute'),
    ('different arguments', ['512M', '3', 'extra value'], 'absolute'),
    ('relative script path', ['256m'], 'relative'),
    ('bare filename from script directory', [], 'bare'),
]:
    with tempfile.TemporaryDirectory(prefix='h13-v2-test-') as temp:
        root = Path(temp)
        sd = root / 'card with spaces'
        base = sd / 'rk_pcba_test_res'
        base.mkdir(parents=True)
        app = root / 'fake-app'
        app.write_bytes(b'ARTIFICIAL APP\0\x7fELF')
        version = root / 'fake-version'
        version.write_text('ARTIFICIAL VERSION\n')
        expected_hash = hashlib.sha256(app.read_bytes()).hexdigest()
        script = base / 'memtester_smd'
        script.write_text(text.replace('/usr/bin/cvr_app', str(app)).replace('/oem/etc/version', str(version)))
        if invocation == 'relative':
            cwd, name = root, str(script.relative_to(root))
        elif invocation == 'bare':
            cwd, name = base, 'memtester_smd'
        else:
            cwd, name = root, str(script)
        proc = subprocess.run(['sh', name, *arguments], cwd=cwd, capture_output=True, timeout=30)
        assert proc.returncode == 0, (label, proc.stderr)
        marker = base / 'H13-PROBE-STARTED.txt'
        out = sd / 'H13-READOUT'
        assert marker.is_file() and (out / 'STARTED.txt').is_file()
        assert f'argument count: {len(arguments)}' in marker.read_text()
        for argument in arguments:
            assert f'argument: <{argument}>' in marker.read_text()
        assert (out / 'COMPLETE.txt').is_file()
        assert (out / 'cvr_app').read_bytes() == app.read_bytes()
        assert (out / 'oem-version.txt').read_text() == version.read_text()
        assert hashlib.sha256(app.read_bytes()).hexdigest() == expected_hash
        (out / 'cvr_app').write_bytes(b'PRESERVE THIS EARLIER CAPTURE')
        subprocess.run(['sh', name, *arguments], cwd=cwd, check=True, capture_output=True, timeout=30)
        assert (out / 'cvr_app').read_bytes() == b'PRESERVE THIS EARLIER CAPTURE'
        assert 'Existing H13-READOUT preserved' in marker.read_text()
        results.append({'case': label, 'result': 'passed; marker, arguments, capture, unchanged source, earlier capture preservation'})

print(json.dumps({'scope': 'Host shell with artificial source files and temporary card paths; not a real H13 run. Host /proc/sys metadata outputs discarded.', 'results': results}, indent=2))
