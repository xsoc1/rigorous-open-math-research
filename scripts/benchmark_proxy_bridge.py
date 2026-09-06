#!/usr/bin/env python3
"""Forward only the specified WSL client's TCP connections to a local proxy."""

import argparse
import selectors
import socket
import socketserver


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument("--listen-host", required=True)
	Parser.add_argument("--client-host", required=True)
	Parser.add_argument("--port", type=int, default=7898)
	Args = Parser.parse_args()

	class Handler(socketserver.BaseRequestHandler):
		def handle(self):
			if(self.client_address[0] != Args.client_host):
				return
			with socket.create_connection(("127.0.0.1", 7897), timeout=10) as Upstream:
				with selectors.DefaultSelector() as Selector:
					Selector.register(self.request, selectors.EVENT_READ, Upstream)
					Selector.register(Upstream, selectors.EVENT_READ, self.request)
					while(True):
						Events = Selector.select(timeout=1800)
						if(not Events):
							return
						for Key, _ in Events:
							Data = Key.fileobj.recv(65536)
							if(not Data):
								return
							Key.data.sendall(Data)

	class Server(socketserver.ThreadingTCPServer):
		allow_reuse_address = True
		daemon_threads = True

	with Server((Args.listen_host, Args.port), Handler) as Proxy:
		print("Restricted WSL proxy bridge ready", flush=True)
		Proxy.serve_forever()


if(__name__ == "__main__"):
	main()
