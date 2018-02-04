# sqlfat
## Python + ANTLR + SQLite = Fully Parallel DBMS 

SQLFat a fully parallel database built on top of SQLite using the socket and multithreading modules within Python 3. For now SQLFat is built with a single-master multi-worker architecture. While the master handles client connections, parses SQL, builds a Query Execution Plan (QEP) and maintains ACID transaction properties, the workers (data nodes) maintain the database in SQLite db files according to the partitioning and repication scheme determined by the master.

**Installation **

For a full install, copy this directory to each of the nodes for the database, ensure both sqlite3 and the proper python packages are installed. In the config_test file ensure that you enter in the correct IP addresses and port numbers for your nodes (by convention the master node will listen on port 50000 and the data nodes will listen on port 50001). Then you can start up the data nodes and the master node (IN THAT ORDER!)

On the data nodes:
> python3 sqlfat/py/datanode.py localhost 50001

On the master node:
> python3 sqlfat/py/master.py localhost 50000 sqlfat/etc/config

You can then use the client module to connect to the database via python (see below for documentation) or you can connect as a client to the database via a shell interface.

First
> chmod a+x sqlfat

Then 
> ./sqlfat [masternode ip address] [port]

**_Docker Simulation_**

In the case that you do not have your own cluster of machines you can try out sqlfat with a Dockerized cluster provided in this package. 
