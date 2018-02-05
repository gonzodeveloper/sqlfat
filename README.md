# sqlfat
## Python + ANTLR + SQLite = Fully Parallel DBMS 

SQLFat a fully parallel database built on top of SQLite using the socket and multithreading modules within Python 3. For now SQLFat is built with a single-master multi-worker architecture. While the master handles client connections, parses SQL, builds a Query Execution Plan (QEP) and maintains ACID transaction properties, the workers (data nodes) maintain the database in SQLite db files according to the partitioning and repication scheme determined by the master.

### Installation

For a full install, copy this directory to each of the nodes for the database, ensure both sqlite3 and the proper python packages are installed. In the config_test file ensure that you enter in the correct IP addresses and port numbers for your nodes (by convention the master node will listen on port 50000 and the data nodes will listen on port 50001). Then you can start up the data nodes and the master node (IN THAT ORDER!)

On the data nodes:
	
    python3 sqlfat/py/datanode.py localhost 50001

On the master node:
	
    python3 sqlfat/py/master.py localhost 50000 sqlfat/etc/config

You can then use the client module to connect to the database via python (see below for documentation) or you can connect as a client to the database via a shell interface.

	
    chmod a+x sqlfat
    ./sqlfat [masternode ip address] [port]

**_Docker Simulation_**

In the case that you do not have your own cluster of machines you can try out sqlfat with a Dockerized cluster provided in this package. The cluster is built on top of the centos official docker image. To stand up the cluster enter the following commands.

	cd simulation
	chmod a+x cluster
	./cluster build
	./cluster start

To stop the cluster (and remove the containers)

	./cluster stop

This docker cluster has 1 master and 3 datanodes. The master accepts connections at 200.0.0.10:50000, the data nodes have IP 200.0.0.11 - 13, listening for master connection at 50001.


### Use

Once installation is complete we can connect to our cluster with the client.

	chmod a+x sqlfat
	./sqlfat 200.0.0.10

Similar to SQLite we can enter commands prefixed by an underscore. For instance **_use** will specify which database to use. **_quit** will quit the client. 

Otherwise SQL statements can be entered directly. For now the statements must be entered in one line, and do not need to be terminated with a semicolon. In the next version this should be fixed ad the interface should work in a more traditional fashion. 


### Technical Details

As noted before, this is a single-master multi-worker architecture, where the master functions as a controller for the entire cluster. Though the machine running the master node could also run a data node it is not necessary.

![](https://raw.githubusercontent.com/gonzodeveloper/sqlfat/master/img/struct.png)

Because the datanodes are multi-threaded to handle several connections, one could actually run a master on each giving us a multi-master cluster, however the catalog db (see below) would have to be manually
copied to each machine, as there is currently no function for automatic replication across masters.

**Catalog** 

The master node also maintains a catalog database which holds metadata on all tables across the cluster. It contains information on which nodes are storing the specific partitions of each table. For now the catalog cannot be directly queried by the client, rather it is simply used by the master in order to organize queries and establish execution plans.

**Config**

The configuration file for the cluster resides in the "etc" directory and it contains information on all the addresses and port numbers of all data nodes. For backward compatability, each entry for the config file must also contain the database drivers used for each node, though this information is not touched by the sqlfat system. In future configurations we can will also store the address information on each master node so we can run remote catalog updates.

**Transactions

As a fully parallel RDBMS sqlfat ensures ACID property compliance for each transaction. This is accomplished through a two-phase transactional protocol. 

![](https://raw.githubusercontent.com/gonzodeveloper/sqlfat/master/img/commit.png)

Once the master recieves a transaction from the client, it preforms the necessary processing (i.e.indexing/partitioning) then forwards the transaction to the data nodes. The datanodes begin their work by aquiring a lock, performing an intial execution and reporting success or failure back to the master. Once the master has recieved status reports from all the nodes it sends back a commit or abort message accordingly (only commit if all node succeeded in their first transaction). Once this is complete, the lock is released.  