db-topology
===========

A small python tool that shows graph topology of MySQL/MariaDB replication

尽管pt-slave-find是个很好的主从拓扑发现工具,但命令行看起来毕竟不太直观,[db-topology](https://github.com/leafonsword/db-topology)是我写的一个python小工具,可以以图方式直观显示MySQL/MariaDB的拓扑结构.如下图:  
*一主两从*  
![](/content/images/2014/Aug/2014-08-31-19-36-01-----fs8.png)  
*级联复制*  
{<3>}![](/content/images/2014/Aug/2014-08-31-17-26-12-----fs8.png)

**基本思路:**  
脚本里指定user和password,这个user能连上所有节点,且至少具有`replication slave`、`replication client`和`process`权限,然后递归找出它的所有master和slave.  

**依赖:**  
Python3
[Connector/Python](http://dev.mysql.com/downloads/connector/python/)  
[NetworkX](http://networkx.github.io/)

**使用方法**  
```shell
$ git clone https://github.com/leafonsword/db-topology.git
$ cd db-topology
$ chmod +x db-topology.py
修改db-topology.py里：
	user = 'yourname'
	password = 'yourpassword'
$ ./db-topology.py IP1:PORT [IP2:PORT ........]
```
然后当前目录下会生成一个`force.json`文件,这是绘图的数据素材,接下来用浏览器打开topology.html就能看到动态图了.
