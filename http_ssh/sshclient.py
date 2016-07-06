#!/usr/bin/python
"""This is the client which simulates a simplified kind of SSH."""

import argparse
import sys
import paramiko
import socket
import time

def request(server):
    """Connect and send commands to server.
	Closes the Connection, If server violates the predefined packet exchange"""
	
    hostname = server
    password = 'Karthik'
    username = "Karthik.Mathi"
    port = 10022

    try:
     client = paramiko.SSHClient()
     client.load_system_host_keys()
     client.set_missing_host_key_policy(paramiko.WarningPolicy())
    
     client.connect(hostname, port=port, username=username, password=password,pkey=None,key_filename=None,allow_agent=False, 		         look_for_keys=False)     
     
     chan = client.invoke_shell()
     
     print('Successfully Logged In\n')
     print(str(chan.recv(1024)))  
     chan.settimeout(10)
     
     try:
	i = 1
	while(i<=10):
		chan.send('Command' + str(i))     
     		data = chan.recv(1024)
		if((len(data.split(',')[1]) > 300) | (len(data.split(',')[1]) < 10)):
			print('>>> ' + data.split(',')[0])
     			print('Received {0} ' .format(len(data.split(',')[1])) + ' bytes from server')
			print('Server violated the predefined packet exchange. closing connection')
			chan.close()
			client.close()
			sys.exit(1)
		else:
			print('>>> ' + data.split(',')[0])
     			print('Received {0} ' .format(len(data.split(',')[1])) + ' bytes from server')			
			print(data.split(',')[1])
			i = i + 1
     	
	chan.send('logout')
     	chan.close()
     except socket.timeout as timeout:
  	print('*** Caught exception: ' + str(timeout.__class__) + ': ' + str(timeout))
        chan.send('logout')     	
     	chan.close()
     	
    finally:
     client.close()


def main():
    """Check user input and start client."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="IP address of the SSH Server",
               required=True)
    args = parser.parse_args()
    start_Time = int(round(time.time() * 1000))
    request(args.server)
    end_Time = int(round(time.time() * 1000))
    print("Client Protocol Run Duration in milliseconds {0} " .format(int(end_Time - start_Time))) 


if __name__ == "__main__":
    main()
