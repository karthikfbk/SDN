#!/usr/bin/python
"""This is the server serving simplified http GET requests."""

import argparse
import socket
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

HOST_PORT = 10080

Kib_1 = bytearray(1024)
Kib_4 = bytearray(4096)
Kib_8 = bytearray(8192)

class CatHTTPRequestHandler(BaseHTTPRequestHandler):
  """ Class that extends BaseHTTPRequestHandler to handle HTTP requests from Clients.
	Overrides do_GET method of BaseHTTPRequestHandler.
	Closes the Connection if client violates pre defined packet exchange. """

  #handle GET command
  def do_GET(self):      
      if self.path == '/':
	self.send_response(200)
	self.send_header("Content-type", "text/plain")
	self.end_headers()
	self.wfile.write(Kib_1)

      elif self.path == 'happy_cat.png':
	self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()	 
	self.wfile.write(Kib_4)

      elif self.path == 'grumpy_cat.png':
	self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
	self.wfile.write(Kib_8)

      else:        
	self.send_error(404, 'Wrong GET Command')
	print("Client violated pre defined packet exchange. Closing server connection")
	self.close_connection = False
	os._exit(1)	

def serve(server):
    	"""Wait for GET and deliver cat pictures."""
        print(server)
	server_address = (server, HOST_PORT)
	httpserver = HTTPServer(server_address, CatHTTPRequestHandler)
	print('HTTP CAT Server is Running for ever')
	httpserver.serve_forever()
	

def main():
    """Check user input and start server."""
    parser = argparse.ArgumentParser(description=
                          "CATTP server serving cat pictures since 2015.")
    parser.add_argument("-s", "--server", help="IP address of the network interface on which this server should run",
               required=True)
    args = parser.parse_args()
    serve(args.server)

if __name__ == "__main__":
    main()
