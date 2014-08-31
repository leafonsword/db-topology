#!/usr/bin/env python3
import mysql.connector
from mysql.connector import errorcode
import sys
import networkx as nx
import json
from networkx.readwrite import json_graph

user = 'dbauser'
password = 'dbauser'

g = nx.DiGraph()


def find_top(host, port):
    g.add_node(host + ':' + port)
    try:
        cnx = mysql.connector.connect(
            host=host, port=port, user=user, password=password)
        cursor = cnx.cursor()
        query = (
            "show slave status;select host from INFORMATION_SCHEMA.PROCESSLIST where command = 'Binlog Dump';show slave hosts;")
        l = []
        for result in cursor.execute(query, multi=True):
            l.append(result.fetchall())
        # print(l[0])

        if l[1] != []:
            for k in range(0, len(l[1])):
                slave_host = str(l[1][k][0].split(':')[0])
                slave_port = str(l[2][k][2])
                g.add_node(slave_host + ':' + slave_port)
                g.add_edge(slave_host + ':' + slave_port, host + ':' + port)
                find_top(slave_host, slave_port)
        if l[0] != []:
            master_host = str(l[0][0][1])
            master_port = str(l[0][0][3])
            if master_host+':'+master_port not in g:
                find_top(master_host, master_port)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(
                "Something is wrong with your user name or password for host", host, 'in port', port)
        else:
            print(err)
    else:
        cnx.close()

def main():
    for i in sys.argv[1:]:
        (host, port) = i.split(':')
        find_top(host, port)

    d = json_graph.node_link_data(g)
    json.dump(d, open('./force.json', 'w'))

main()