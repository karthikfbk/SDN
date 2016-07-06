#!/usr/bin/python
"""This is the client which simulates http GET requests."""

import argparse
import httplib
import time
import sys

def request(server, debug):
        """Connect and send requests to server.
	Closes the connection if server violates the pre defined packet exchange.
	Valid responses from server for client commands,
		GET '/' 		Server: data of length 1024 bytes .
		GET 'happy_cat.png'	Server: data of length 4096 bytes .
		GET 'grumpy_cat.png'	Server: data of length 8192 bytes ."""

	conn = httplib.HTTPConnection(server,'10080')
	if debug:
		conn.debuglevel = 1
	conn.request('GET', '/')
	rsp = conn.getresponse()

	if rsp.status == 200:	  	
	  	data_received = rsp.read()
		if len(data_received) == 1024:
	  		print('Received {0} ' .format(len(data_received)) + ' bytes from server')
		else:
			print("Server violated predefined packet exchange. Closing client connection")
			conn.close()
			sys.exit(1)
	else:
		conn.close()

	conn.request('GET', 'happy_cat.png')
	rsp = conn.getresponse()
  
  	if rsp.status == 200:	  	
	  	data_received = rsp.read()
	  	if len(data_received) == 4096:
	  		print('Received {0} ' .format(len(data_received)) + ' bytes from server')
		else:
			print("Server violated predefined packet exchange. Closing client connection")
			conn.close()
			sys.exit(1)
	else:
		conn.close()

	conn.request('GET', 'grumpy_cat.png')
	rsp = conn.getresponse()
  
  	if rsp.status == 200:	  	
	  	data_received = rsp.read()
	  	if len(data_received) == 8192:
	  		print('Received {0} ' .format(len(data_received)) + ' bytes from server')
		else:
			print("Server violated predefined packet exchange. Closing client connection")
			conn.close()
			sys.exit(1)
	else:
		conn.close()

    

def main():
    """Check user input and start client."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="IP address of the server to connect",
               required=True)
    parser.add_argument("-d", "--debug", help="Show debug logs to console",
		action="store_true")
    args = parser.parse_args()
    start_Time = int(round(time.time() * 1000))
    
    request(args.server, args.debug)
    end_Time = int(round(time.time() * 1000))
    print("Client Protocol Run Duration in milliseconds {0} " .format(int(end_Time - start_Time))) 

if __name__ == "__main__":
    main()
