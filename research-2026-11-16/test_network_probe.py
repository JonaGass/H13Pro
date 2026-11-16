"""Loopback-only checks of allowed GETs, redirects, bounds and TCP results."""
import importlib.util
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import socket
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('h13_network_probe', ROOT / 'h13_network_probe.py')
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.requests.append(self.path)
        if self.server.behavior == 'redirect':
            self.send_response(302)
            self.send_header('Location', f'http://127.0.0.1:{self.server.server_port}/unexpected')
            self.end_headers()
            return
        body = b'x' * 70000 if self.server.behavior == 'large' else b'{"mac":"00:11:22:33:44:55","device_id":"TEST-CHIP"}'
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class NetworkChecks(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.server.behavior = 'normal'
        self.server.requests = []
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def query(self, command):
        return probe.get_info('127.0.0.1', command, http_port=self.server.server_port, timeout=2)

    def test_known_gets_bypass_proxy_and_redact_mac(self):
        with patch.dict('os.environ', {'http_proxy': 'http://127.0.0.1:9', 'HTTP_PROXY': 'http://127.0.0.1:9', 'no_proxy': '', 'NO_PROXY': ''}):
            for command in (2001, 2002):
                result = self.query(command)
                self.assertEqual(result['status'], 200)
                self.assertIn('TEST-CHIP', result['body'])
                self.assertNotIn('00:11:22:33:44:55', result['body'])
                self.assertIn('[MAC REDACTED]', result['body'])
        self.assertEqual(self.server.requests, ['/api/getdeviceinfo?cmd=2001', '/api/getdeviceinfo?cmd=2002'])

    def test_unknown_command_sends_no_request(self):
        with self.assertRaises(ValueError):
            self.query(3001)
        self.assertEqual(self.server.requests, [])

    def test_redirect_not_followed(self):
        self.server.behavior = 'redirect'
        self.assertEqual(self.query(2001)['status'], 302)
        self.assertEqual(len(self.server.requests), 1)

    def test_body_size_bounded(self):
        self.server.behavior = 'large'
        result = self.query(2002)
        self.assertTrue(result['truncated'])
        self.assertEqual(len(result['body']), probe.MAX_BODY)

    def test_tcp_connect_sends_no_http_request(self):
        self.assertEqual(probe.probe_port('127.0.0.1', self.server.server_port)['state'], 'open')
        self.assertEqual(self.server.requests, [])
        with socket.socket() as reserved:
            reserved.bind(('127.0.0.1', 0))
            self.assertEqual(probe.probe_port('127.0.0.1', reserved.getsockname()[1])['state'], 'refused')

    def test_address_validation(self):
        self.assertEqual(probe.device_address('192.168.10.1'), '192.168.10.1')
        for address in ('example.com', '8.8.8.8', '127.0.0.1/path', '192.168.10.999'):
            with self.assertRaises(ValueError):
                probe.device_address(address)


if __name__ == '__main__':
    unittest.main(verbosity=2)
