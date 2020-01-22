# coinstac-search
This is a simulated distributed search plugin for COINSTAC. 

After you have installed the [coinstac-simulator](https://www.npmjs.com/package/coinstac-simulator) and [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) installed you can run the test as follows:

* cd coinstac-search/plugin-sim
* docker build -t coinstac/coinstac-repro-search .
* coinstac-simulator -c 4 

Each simulated local node will read the NIDM data from a file named local**X**.nidm.ttl where the **X** is the node number. You can replace or add to these files with other .ttl files. The simulation will fail if specify more simultated local nodes using the -c option than you have localX.nidm.ttl files.

The simulation will run a distributed PyNIDM REST API call on each of the files. For testing purposes, you can change the REST URI by modifying the file plugin-sim/test/inputspec.json.
