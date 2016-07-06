from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
import argparse
import sys
log = core.getLogger()

bandwidthport = 0
latencyport = 0
known_ports = dict()

def install_rule_destport (conn, tcpport, port):
	""" Installs the rule to forward the packet to 'port' if TCP destination port is 'tcpport' """
	msg = of.ofp_flow_mod()
	msg.match.nw_proto = 6
	msg.match.dl_type = 0x0800
	msg.match.tp_dst = tcpport
	msg.actions.append(of.ofp_action_output(port = port))
	conn.send(msg)

def install_rule_srcport (conn, tcpport, port):
	""" Installs the rule to forward the packet to 'port' if TCP source port is 'tcpport' """
	msg = of.ofp_flow_mod()
	msg.match.nw_proto = 6
	msg.match.dl_type = 0x0800
	msg.match.tp_src = tcpport
	msg.actions.append(of.ofp_action_output(port = port))
	conn.send(msg)

def handle_latencyrule (conn, switch, tcpport):
	""" Installs the Latency Rule for every switch present in the Topology """
	if(str(switch) == "1"):
		install_rule_destport (conn, tcpport, 3)
                install_rule_srcport (conn, tcpport, 1)
	#For Switch 2 , the rule is not needed, because switch 2 does not
	#come in the path for lowest possible latency
        if(str(switch) == "2"):
                install_rule_destport (conn, tcpport, 3)
                install_rule_srcport (conn, tcpport, 1)

        if(str(switch) == "3"):
                install_rule_destport(conn, tcpport, 3)
                install_rule_srcport(conn, tcpport, 1)

        if(str(switch) == "4"):
                install_rule_destport(conn, tcpport, 1)
                install_rule_srcport(conn, tcpport, 3)

def handle_bandwidthrule (conn, switch, tcpport):
	""" Installs the Bandwidth rule for every switch present in the Topology """
	if(str(switch) == "1"):
		install_rule_destport (conn, tcpport, 2)
		install_rule_srcport (conn, tcpport, 1)

	if(str(switch) == "2"):
		install_rule_destport (conn, tcpport, 2)
		install_rule_srcport (conn, tcpport, 1)

	if(str(switch) == "3"):
		install_rule_destport(conn, tcpport, 3)
		install_rule_srcport(conn, tcpport, 2)

	if(str(switch) == "4"):
		install_rule_destport(conn, tcpport, 1)
		install_rule_srcport(conn, tcpport, 3)

def _handle_ConnectionUp (event):
  """ Handles switch connection up event """
  print "installing custom flowtable entries on %s" % dpidToStr(event.dpid)
  
  handle_bandwidthrule (event.connection, event.dpid, bandwidthport)
  handle_latencyrule (event.connection, event.dpid, latencyport)

def _handle_PacketIn(event):
  """ Handles switch packetIn event"""
  dpid = event.dpid
  packet = event.parsed
  
  if(packet.type == 0x0806):
	print("Received ARP PACKET")
  	action = of.ofp_action_output(port = of.OFPP_FLOOD)
  	msg = of.ofp_packet_out()
  	msg.data = event.ofp
  	msg.actions.append(action)
  	event.connection.send(msg)

def launch(highbandwidth="http",lowlatency="ssh"):
  global bandwidthport
  global latencyport

  if(highbandwidth == lowlatency):
	print("Invalid arguments")
	sys.exit()
  if(highbandwidth=="http"):
        bandwidthport = 10080
  else:
	bandwidthport = 10022
  if(lowlatency == "ssh"):
	latencyport = 10022
  else:
	latencyport = 10080
  print("Packets with target Port "+str(bandwidthport)+" will be routed in HighBandwidth Path")
  print("Packets with target port "+str(latencyport)+ " will be routed in minimum latency path")
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
