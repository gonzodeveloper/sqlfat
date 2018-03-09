#!/usr/bin/python3

from bin.master import Master
from bin.datanode import DataNode
import sys
from threading import Thread

usage = "sqlfat-server [master|datanode]"
if len(sys.argv) < 1 or sys.argv not in ["master", "datanode"]:
    print(usage)
    exit(1)

if sys.argv[1] == "master":
    master = Master()
    print("Master Up...")
    Thread(target=master.master_listen, args=()).start()
    Thread(target=master.client_listen, args=()).start()


elif sys.argv[1] == "datanode":
    node = DataNode()
    print("Datanode Up...")
    node.listen()
