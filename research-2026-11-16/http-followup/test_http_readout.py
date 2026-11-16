"""Loopback-only HTTP readout checks. No device or firmware binary execution."""
import contextlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import io
import json
from pathlib import Path
import struct
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import h13_http_readout as reader

HEADER = bytearray(52)
HEADER[:6] = b'\x7fELF\x01\x01'
struct.pack_into('<H', HEADER, 18, 40)
APP_FIXTURE = bytes(HEADER) + b'ARTIFICIAL NONEXECUTED TEST DATA' * 8


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.requests.append(self.path)
        if self.server.behavior == 'redirect':
            self.send_response(302)
            self.send_header('Location', f'http://127.0.0.1:{self.server.server_port}/never-follow')
            self.end_headers()
            return
        status = 200
        if self.path == '/api/getdeviceinfo?cmd=2001':
            body = b'{"product":"R8-V2.0","sp":"qckj"}'
        elif self.path == '/api/getdeviceinfo?cmd=8567':
            body = b''
        elif self.path == '/':
            body = b'<html><a href="/never-follow">example</a></html>'
        elif self.path == '/usr/bin/cvr_app':
            body = APP_FIXTURE if self.server.behavior != 'html' else b'<html>not an app</html>'
        else:
            status, body = 404, b'not found'
        self.send_response(status)
        self.send_header('Content-Type', 'application/octet-stream')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class ReadoutChecks(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.server.requests = []
        self.server.behavior = 'normal'
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def fetch(self, address, path, limit):
        return self.original_fetch(address, path, limit, http_port=self.server.server_port, timeout=2)

    def run_main(self, out):
        self.original_fetch = reader.fetch_path
        original_info = reader.get_info
        with patch.object(sys, 'argv', ['h13_http_readout.py', '--host', '127.0.0.1', '--out', str(out)]), \
             patch.object(reader, 'fetch_path', side_effect=self.fetch), \
             patch.object(reader, 'get_info', side_effect=lambda addr, cmd: original_info(addr, cmd, http_port=self.server.server_port, timeout=2)), \
             contextlib.redirect_stdout(io.StringIO()):
            reader.main()
        return json.loads((out / 'http-report.json').read_text())

    def test_fixed_paths_and_candidate_capture(self):
        with tempfile.TemporaryDirectory(prefix='h13-http-test-') as temp:
            out = Path(temp) / 'readout'
            report = self.run_main(out)
            self.assertEqual((out / 'cvr_app.system-path.original').read_bytes(), APP_FIXTURE)
            self.assertEqual(report['requests']['update_identity']['received_bytes'], 0)
            self.assertEqual(report['requests']['update_identity']['status'], 200)
            self.assertEqual(self.server.requests, ['/api/getdeviceinfo?cmd=2001'] + [p for _, p, _ in reader.REQUESTS])
            self.assertNotIn('/never-follow', self.server.requests)

    def test_html_at_app_path_not_saved_as_application(self):
        self.server.behavior = 'html'
        with tempfile.TemporaryDirectory(prefix='h13-http-test-') as temp:
            out = Path(temp) / 'readout'
            report = self.run_main(out)
            self.assertFalse((out / 'cvr_app.system-path.original').exists())
            self.assertIn('not an app', report['requests']['app_system_path']['text'])

    def test_truncated_arm_file_not_saved(self):
        with tempfile.TemporaryDirectory(prefix='h13-http-test-') as temp, patch.object(reader, 'APP_LIMIT', 100):
            out = Path(temp) / 'readout'
            report = self.run_main(out)
            self.assertFalse((out / 'cvr_app.system-path.original').exists())
            self.assertTrue(report['requests']['app_system_path']['truncated'])

    def test_redirect_not_followed_and_unknown_path_rejected(self):
        self.server.behavior = 'redirect'
        result, _ = reader.fetch_path('127.0.0.1', '/', 1000, http_port=self.server.server_port)
        self.assertEqual(result['status'], 302)
        self.assertEqual(self.server.requests, ['/'])
        with self.assertRaises(ValueError):
            reader.fetch_path('127.0.0.1', '/api/setdeviceinfo?cmd=3003', 100)


if __name__ == '__main__':
    unittest.main(verbosity=2)
