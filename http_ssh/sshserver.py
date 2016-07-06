#!/usr/bin/python
"""This is the server which simulates a simplified SSH."""

import argparse
import paramiko
import traceback
import sys
import socket
import string, random
host_key = paramiko.RSAKey.generate(1024,progress_func=None)

class MyServer (paramiko.ServerInterface):
  """ Implementation of SSH server.
	Overriding the Methods of paramiko.ServerInterface for which client needs shell access.
	Overriding password authentication method with hardcoded username and password values.
	Server supports only password authentication of clients."""

  def check_auth_password(self, username, password):
        if (username == 'Karthik.Mathi') and (password == 'Karthik'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

  def check_channel_request(self, kind, chanid):
        if kind == 'session':
           return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
 
  def get_allowed_auths(self, username):
        return 'password'

  def check_channel_shell_request(self, channel):
        return True

  def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True


def getRandomStrofLen10_300():
	return ''.join(random.choice(string.letters + string.hexdigits) for _ in range(random.randint(10,300)))

def serve(server):
	"""Wait for client and accept their commands.
	Closes the connection if Client violates the predefined packet exchange."""
	
	try:
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    sock.bind((server, 10022))
	except Exception as e:
		print('*** Bind failed: ' + str(e))
    		traceback.print_exc()
    		sys.exit(1)
        while(True):
		try:
    			sock.listen(1)
    			print('Listening for new connection ...')
    			client, addr = sock.accept()
		except Exception as e:
    			print('Listen/accept failed: ' + str(e))
    			traceback.print_exc()
    			sys.exit(1)

		print('Got a connection!')

		try:
    			t = paramiko.Transport(client)    
    			t.add_server_key(host_key)
    			mserver = MyServer()    	
			try:        	
				t.start_server(server=mserver)
    			except paramiko.SSHException:
        			print('*** SSH negotiation failed.')
        			sys.exit(1)

    			# wait for auth
    			chan = t.accept(20)
    			if chan is None:
        			print('*** No channel.')
        			sys.exit(1)
    			print('Authenticated!')    
    
   	 		chan.setblocking(1)
			chan.send("SSH-0.0-Insecure")
   	 		while(True):
   	 			data = chan.recv(1024)
				if((len(data) < 4) | (len(data) > 20)):
					print('Client violated the predefined packet exchange.')
					break
   	 			if(data == 'logout'):
					print('logging out')
					break
				else:
					dataToSend = getRandomStrofLen10_300()
					chan.send(str(data) + ',' + dataToSend)				
					print("Sent Response {0} bytes \n" .format(len(dataToSend)))			
				
			print("Closing Channel")
   	 
   	 		t.close()
   	 		chan.close()

		except Exception as e:
    			print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
    			traceback.print_exc()
    	try:
        	t.close()
    	except:
        	pass
    		sys.exit(1)


def main():
    """Start simplified SSH server."""
    parser = argparse.ArgumentParser(description="Server simulating SSH.")
    parser.add_argument("-s", "--server", help="IP address of the network interface on which SSH Server should run",
               required=True)
    args = parser.parse_args()    
    serve(args.server)

if __name__ == "__main__":
    main()
