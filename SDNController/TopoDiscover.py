
from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pktt
import pydot
from pox.lib.util import dpidToStr
from pox.lib.util import dpid_to_str

#DATA STRUCTURES FOR STORING THE TOPOLOGY

# List to store the events related to each switch during ConnectionUp
switches = []

#TTL Value for LLDP packet used to discover the topology
lldp_ttl = 1

#Dictionary to store each switch discovered in the topology.
#nodes = {switch : [ {port1:mac1}, {port2:mac2} ,... ]}
nodes = {}

#List to store the links discovered in the topology.
#edges = [((src switch,src port_no,src_mac),(dst switch,dst port_no,dst_mac)),((),()),....]
edges = []

def _handle_ConnectionUp(event):
	"""Handles Switch Connection Up event"""
	global switches
	e = event
	msg = of.ofp_flow_mod()
	msg.match.dl_type = 0x88cc
	msg.match.dl_dst = pktt.ETHERNET.NDP_MULTICAST
	msg.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER))
	event.connection.send(msg)
	if not e.dpid in switches:
		switches.append(e)
	
def _add_Topology():
    """ Populates the Switch ID , Ports and MAC address into the Data Structure"""
    global switches
    global nodes
    for event in switches:
	#Add the Nodes
	if not event.dpid in nodes:
		nodes[event.dpid] = []

		print("Switch " + str(event.dpid) + " added to list of nodes")
		for p in event.ofp.ports:
		  if p.port_no != 65534:
			portno = p.port_no
			hw_addr = str(p.hw_addr)
			if not {portno:hw_addr} in nodes[event.dpid]:
				nodes[event.dpid].append({portno:hw_addr})
				print("Added port no "+ str(portno) + " hw_addr " + hw_addr)

def _send_lldp():
	""" Method the get the initial Topology data structure populated and sends LLDP packets to discover the links"""
	global switches
	_add_Topology()
	for event in switches:
		send_discovery_packet(event)

def _handle_PacketIn(event):
	""" Handles switch packet in event"""
	packet = event.parsed
	if(packet.type == 0x88cc):
		updateedges(packet, event.dpid, event.port)

def updateedges(packet, rec_dpid, rec_port):
	""" Updates the links present in the topology in respective data structure"""
	global topo
	global nodes
	global edges
        if packet.type == 0x88cc:
                lldph = packet.find(pktt.lldp)
                send_dpid = int(lldph.tlvs[0].id)
                send_port = int(lldph.tlvs[1].id)
		send_hw_addr = None
		rec_hw_addr = None
		for li in nodes[send_dpid]:
			if send_port in li.keys():
				send_hw_addr = li[send_port]

		for li in nodes[rec_dpid]:
			if rec_port in li.keys():
				rec_hw_addr = li[rec_port]

		if not ((send_hw_addr is None) or (rec_hw_addr is None)):
			#Add the Edge
			if not ((((send_dpid,send_port,send_hw_addr),(rec_dpid,rec_port,rec_hw_addr)) in edges) or (((rec_dpid,rec_port,rec_hw_addr),(send_dpid,send_port,send_hw_addr))in edges)):
				edges.append(((send_dpid,send_port,send_hw_addr),(rec_dpid,rec_port,rec_hw_addr)))
				print("Added link src switch src port " + str(send_dpid) +" " + str(send_port) +" " +str(send_hw_addr) + " dst swtich dst port " + str(rec_dpid) + " " + str(rec_port)+ " " + str(rec_hw_addr))
				


def send_discovery_packet(event):
	""" Sends the discovery packet used to identity the links present between the switches"""
	for p in event.ofp.ports:
		chass_id = event.dpid
		src = str(p.hw_addr)

		portno = p.port_no
		chassis_id = pktt.chassis_id(subtype=pktt.chassis_id.SUB_LOCAL, id = str(chass_id))
		
		port_id = pktt.port_id(subtype = pktt.port_id.SUB_PORT, id = str(portno))
		ttl = pktt.ttl(ttl = lldp_ttl)


		discovery_packet = pktt.lldp()
		discovery_packet.tlvs.append(chassis_id)
		discovery_packet.tlvs.append(port_id)
		discovery_packet.tlvs.append(ttl)
		discovery_packet.tlvs.append(pktt.end_tlv())

		eth = pktt.ethernet(type = pktt.ethernet.LLDP_TYPE)
		eth.src = src
		eth.dst = pktt.ETHERNET.NDP_MULTICAST
		eth.payload = discovery_packet

		pkt = of.ofp_packet_out(action = of.ofp_action_output(port = portno))
                pkt.data = eth.pack()
                event.connection.send(pkt.pack())

def showgraph():
	""" Outputs Dot representation of the Topology based on information currently present in the data structures"""
	global nodes
	global edges
	graph = pydot.Dot(graph_type='graph', fontname = "Verdana")
	
	for switch in nodes.keys():
		cluster = pydot.Cluster(str(switch), label='Switch \n'+dpidToStr(switch),width = '35')
		for dic in nodes[switch]:
		  key = dic.keys()[0]
		  val = dic[key]
		  value = str(switch) + str(key)
		  cluster.add_node(pydot.Node(value,label = "Port "+str(key) +"\n" + str(val),shape="rectangle",pos=str(switch)+','+str(key)))
        	graph.add_subgraph(cluster)
	
	#create edges
	for edge in edges:
		edge1 = str(str(edge[0][0]) + str(edge[0][1]))
		edge2 = str(str(edge[1][0]) + str(edge[1][1]))
		graph.add_edge(pydot.Edge(edge1,edge2))
	
	graph.write_raw('topo.dot')
	
def launch():
	core.register('draw',showgraph)
	core.register('sendlldp', _send_lldp)
	core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
	core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
