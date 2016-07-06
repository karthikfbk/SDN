
Problem 4: Controlling the Traffic.

FILES:
	Topology.py --> Same file as Topology.py submitted for Problem 3 except that this one uses Remote Controller(ip=127.0.0.1, port=6633) instead of Local controller.

	TopoDiscover.py --> This is the generic Controller used to discover the network topology. This will output the topology in DOT representation.

	Topology.png --> Topology image after discovery. This is obtained from DOT representation of the Topology.

	CustomController.py --> This is the Custom written Controller especially for the given problem topology used to route packet in high bandwidth and low latency path. Since this is the Custom controller written specific for the given problem topology, the port numbers and switch id's are hard coded for routing.

	BoxPlotHTTP.jpg --> Box and whiskers plot obtained after running HTTP in High bandwidth and low latency path.

	BoxPlotSSH.jpg --> Box and whiskers plot obtained after running SSH in High bandwidth and low latency path.

EXTERNAL LIBRARY DEPENDENCY:
	- TopoDiscovery.py needs python's pydot library.
	- For linux (ubuntu) you can install pydot library by typing "pip install pydot" in terminal.

Problem 4. a:
	1. Run Topology.py to create the topology,
		USAGE: sudo -E python Topology.py

	2. Run TopoDiscover.py as Remote Controller inside mininet's pox directory.
		USAGE: ./pox.py py TopoDiscover
		This will run the Controller in pox interactive mode

	3. Start the Discovery by,
		POX> core.sendlldp()

	4. Export the Topology as Dot file by,
		POX> core.draw()

	5. Step 4 will output 'topo.dot' file. To convert the dot representation to .png using graphviz,
		dot -Tpng topo.dot -o Topology.png
		
Problem 4. b&c:
	1. Running CustomController.py
		- To run the Controller that routes HTTP in highbandwidth path and SSH in low latency path,
		USAGE: ./pox.py CustomController -highbandwidth="http" -lowlatency="ssh"

		- To run the Controller that routes HTTP in lowlatency path and SSH in highbandwidth path
		USAGE: ./pox.py CustomController -highbandwidth="ssh" -lowlatency="http"

	2. Run the Topology.py by supplying the Protocol, Number Of measurements and Result file as arguments.
	3. Obtain the Box plot. Step 2 and 3 are same as in Problem 3. Please refer to README submitted for problem 3 for more info.

	

		
