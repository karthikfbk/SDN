from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from time import sleep
import argparse

""" To run this topology,
	sudo -E python Topology.py """

class CustomSwitchTopology(Topo):
    """Simple Custom topology with 4 switches and 2 hosts"""
    hostbandwidth = dict(bw=1,delay='1ms')
    highbandwidth = dict(bw=0.512, delay='20ms')
    lowbandwidth = dict(bw=0.032, delay='1ms')
    def __init__(self, **opts):
        """Create custom topo."""

        # Initialize topology
        # It uses the constructor for the Topo cloass
        super(CustomSwitchTopology, self).__init__(**opts)

        # Add hosts and switches
        h1 = self.addHost('h1')
	h2 = self.addHost('h2')
	
	# Adding switches
        s1 = self.addSwitch('s1', dpid="0000000000000001")
        s2 = self.addSwitch('s2', dpid="0000000000000002")
        s3 = self.addSwitch('s3', dpid="0000000000000003")
        s4 = self.addSwitch('s4', dpid="0000000000000004") 

        # Add links with bandwidth limitations
        self.addLink(h1, s1, **self.hostbandwidth)
        self.addLink(h2, s4, **self.hostbandwidth)
        self.addLink(s1, s2, **self.highbandwidth)
        self.addLink(s1, s3, **self.lowbandwidth)
        self.addLink(s2, s3, **self.highbandwidth)
        self.addLink(s2, s4, **self.lowbandwidth)
        self.addLink(s3, s4, **self.highbandwidth)
       
def dpctl_execute(net,node,port):
	"""Function to disable Flooding for the given port on the node"""
	switch = net.getNodeByName(node)
	switch.dpctl("mod-port",port,"no-flood")	

def run():
    parser = argparse.ArgumentParser(description="""Create the Topology for Measurements. The measurement suite HTTP/SSH Server/Client.py should be in the same directory as this file.""",  
                                       usage='%(prog)s [OPTIONS]')
    parser.add_argument("-P", "--Protocol", help="Protocol to Start the Measurement. Either HTTP or SSH")
    parser.add_argument("-N","--Measurements", help="Number of Measurements to be done. Default will be 100",default=100,type=int)
    parser.add_argument("-R","--fileName", help="Name of the file to store the results. Default file will be Results.txt",default='Results.txt')

    args = parser.parse_args()
   
    net = Mininet(topo=CustomSwitchTopology(), link=TCLink)
   
    HostA, HostB = net.get('h1','h2')
    HostA.setIP('192.168.212.2')
    HostB.setIP('192.168.212.1')

    net.start()
    dumpNodeConnections(net.hosts)
    dumpNodeConnections(net.switches)
    
    #Disable flooding
    dpctl_execute(net,'s1','3')
    dpctl_execute(net,'s3','1')
    dpctl_execute(net,'s2','3')
    dpctl_execute(net,'s4','2')
   
    h1, h2 = net.hosts[0], net.hosts[1]
    i = 1
    if(args.Protocol == 'HTTP'):
        print("Starting HTTP Server\n")
 	print h2.cmd('python httpserver.py -s '+h2.IP()+' &')
    	sleep(1)
    	print("Starting HTTP Client for "+ str(args.Measurements)+" times and storing results in "+args.fileName)
    	while (i <= args.Measurements):
            print("Running HTTP Client Measurement Number " +str(i))
	    h1.cmd('python httpclient.py -s '+h2.IP()+' >> '+(args.fileName))
            i = i + 1
    elif(args.Protocol == 'SSH'):
	print h2.cmd('python sshserver.py -s '+h2.IP()+' &')
        sleep(1)
        print("Starting SSH Client for "+ str(args.Measurements)+" times and storing results in "+args.fileName)
        while (i <= args.Measurements):
            print("Running SSH Client Measurement Number " +str(i))
            h1.cmd('python sshclient.py -s '+h2.IP()+' >> '+(args.fileName))
            i = i + 1  
    else:
	CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
