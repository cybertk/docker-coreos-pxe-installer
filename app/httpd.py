#!/usr/bin/env python3

import sys
import subprocess
import http.server
import socketserver

PORT = 8000

cc_sh_template = open(sys.argv[1]).read()
cc_yml_template = open(sys.argv[2]).read()
server_ip = sys.argv[3]
port = int(sys.argv[4])
etcd_discovery_token = subprocess.check_output(["wget", "-qO-", "https://discovery.etcd.io/new?size=3"]).decode("utf-8")
print("etcd discovery token: %s" % etcd_discovery_token)

class PxeHandler(http.server.SimpleHTTPRequestHandler):

    def __get_cloud_config_sh(self):
        self.send_response(200)
        self.end_headers()

        self.wfile.write(bytes(cc_sh_template % self.options, "utf-8"))

    def __get_cloud_config_yml(self):
        self.send_response(200)
        self.send_header("Content-type", "application/x-yaml")
        self.end_headers()

        self.wfile.write(bytes(cc_yml_template % self.options, "utf-8"))

    def do_GET(self):

        print("Access from %s" % self.client_address[0])

        self.options = {
                "server_ip": server_ip,
                "client_ip": self.client_address[0],
                "etcd_discovery_token": etcd_discovery_token,
        }
        if (self.path == "/cloud-config.sh"):
            return self.__get_cloud_config_sh()
        if (self.path == "/cloud-config.yml"):
            return self.__get_cloud_config_yml()

        self.send_response(404)
        self.end_headers()
        

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer((server_ip, port), PxeHandler)

print("serving at %s:%s" % (server_ip, port))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
