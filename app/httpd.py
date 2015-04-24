#!/usr/bin/env python3

import sys
import subprocess
import http.server
import socketserver

PORT = 8000
ETCD_TOKEN_FILE = "etcd_discovery_token"

work_dir = sys.argv[1]
server_ip = sys.argv[2]
port = int(sys.argv[3])

try:
    with open(work_dir + "/" + ETCD_TOKEN_FILE, "r") as f:
        etcd_discovery_token = f.read()
except FileNotFoundError:
    with open(work_dir + "/" + ETCD_TOKEN_FILE, "w") as f:
        print("Creating new etcd discovery token")

        etcd_discovery_token = subprocess.check_output(["wget", "-qO-", "https://discovery.etcd.io/new?size=3"]).decode("utf-8")
        f.write(etcd_discovery_token)

print("etcd discovery token: %s" % etcd_discovery_token)

class PxeHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        print("Access from %s" % self.client_address[0])

        try:
            template = open(work_dir + self.path).read()
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.end_headers()

        options = {
                "server_ip": server_ip,
                "client_ip": self.client_address[0],
                "client_ip_dash": self.client_address[0].replace(".", "-"),
                "etcd_discovery_token": etcd_discovery_token,
        }
        self.wfile.write(bytes(template % options, "utf-8"))

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer((server_ip, port), PxeHandler)

print("serving at %s:%s" % (server_ip, port))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
