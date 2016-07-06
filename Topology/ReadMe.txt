//Topology.py

---> run as "sudo -E python Topology -P "The protocol" -N "number of measurements" -R "filename to store the result". The help text for these arguments can be accessed with -h or --help.

--> The suite for running the measurements should be present in the same directory as Topology.py

//BoxPlot.py

---> run as "python BoxPlot.py -H "result file for http measurement" - S "result file for ssh measurement"

--> To run this program via SSH , do a "SSH -X" into the mininet-vm. Otherwise you may result in "tclerror no display name and no $display environment variable" error.

//BoxandWhiskers.jpg

--> Since i have implemented the initial key exchange and client authentication via RSA while implementing SSH measurement suite, the delay for running ssh is relatively high compared to http.

--> To get a clear BoxPlot for both of the Protocol suite, i have zoomed in individual protocol for certain millisecond range for better view. 


