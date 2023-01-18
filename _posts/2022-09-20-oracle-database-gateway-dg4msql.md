---
title: "Oracle Database Gateway DG4MSQL Configuration"
date: 2019-04-18T15:34:30-04:00
categories:
  - Cloud Integration
tags:
  - Database Gateway
  - Oracle DG4MSQL
---

# Oracle Gateway for MSSQL DG4MSQL configuration

### Environment
* MSSQL database on Docker 2022-latest
* Oracle database 12.2
* Oracle Database Gateway 19.3
* VirtualBox

### References
- How to Configure DG4MSQL (Database Gateway for MS SQL Server) on a 64bit Windows post install (Doc ID 1086365.1)
- https://rkkoranteng.com/2021/09/20/oracle-database-gateway-19c-deployment-for-sql-server/
- http://oracle-help.com/oracle-database/oracle-database-gateway-microsoft-sql-server/
- https://oracle-base.com/articles/misc/heterogeneous-services-generic-connectivity

### Synaposis
The Oracle Database Gateway for MSSQL comes on a separate CD. It can be installed into an existing ORACLE_HOME(attention: if the ORACLE_HOME contains an already patched release of the database, you MUST apply the patchset agian.) Recommended installation is to install into a separate home under the same ORACLE_BASE

## Overview installation and configuration steps:
* MSSQL installation
* Oracle database setup
* Software installation
* Software configuration
* Listener configuration
* tnsnames.ora file configuration
* initdg4msql.ora file configuration
* Database Link creation
* Testing the connection

## Prerequisite
### MSSQL server configuration
```
root@LAPTOP-HUPVGV43:~# docker images
REPOSITORY                                                TAG                                                                          IMAGE ID       CREATED         SIZE
mochoa/sqlcl-docker-extension                             22.2.1                                                                       85688c8ad40c   6 days ago      271MB
hubproxy.docker.internal:5000/docker/desktop-kubernetes   kubernetes-v1.24.2-cni-v1.1.1-critools-v1.24.2-cri-dockerd-v0.2.1-1-debian   5dcc4b79ec39   2 months ago    364MB
k8s.gcr.io/kube-apiserver                                 v1.24.2                                                                      d3377ffb7177   2 months ago    130MB
k8s.gcr.io/kube-proxy                                     v1.24.2                                                                      a634548d10b0   2 months ago    110MB
k8s.gcr.io/kube-scheduler                                 v1.24.2                                                                      5d725196c1f4   2 months ago    51MB
k8s.gcr.io/kube-controller-manager                        v1.24.2                                                                      34cdf99b1bb3   2 months ago    119MB
k8s.gcr.io/etcd                                           3.5.3-0                                                                      aebe758cef4c   4 months ago    299MB
k8s.gcr.io/pause                                          3.7                                                                          221177c6082a   6 months ago    711kB
0.0.0.0:5000/flask-restapi                                1.0                                                                          27249a61c7e2   7 months ago    1.05GB
127.0.0.1:5000/flask-restapi                              1.0                                                                          27249a61c7e2   7 months ago    1.05GB
flask-restapi                                             latest                                                                       27249a61c7e2   7 months ago    1.05GB
localhost:5000/flask-restapi                              1.0                                                                          27249a61c7e2   7 months ago    1.05GB
<none>                                                    <none>                                                                       ed696e912e26   8 months ago    1.05GB
flask-restapi                                             1.0                                                                          75a948a9e78b   8 months ago    1.05GB
kindest/node                                              v1.23.1                                                                      49b8c1a84228   8 months ago    1.46GB
docker/desktop-kubernetes                                 kubernetes-v1.22.4-cni-v0.8.5-critools-v1.17.0-debian                        493a106d3678   9 months ago    294MB
k8s.gcr.io/kube-apiserver                                 v1.22.4                                                                      8a5cc299272d   9 months ago    128MB
k8s.gcr.io/kube-controller-manager                        v1.22.4                                                                      0ce02f92d3e4   9 months ago    122MB
k8s.gcr.io/kube-scheduler                                 v1.22.4                                                                      721ba97f54a6   9 months ago    52.7MB
k8s.gcr.io/kube-proxy                                     v1.22.4                                                                      edeff87e4802   9 months ago    104MB
registry                                                  2                                                                            b8604a3fe854   9 months ago    26.2MB
k8s.gcr.io/coredns/coredns                                v1.8.6                                                                       a4ca41631cc7   11 months ago   46.8MB
k8s.gcr.io/etcd                                           3.5.0-0                                                                      004811815584   14 months ago   295MB
k8s.gcr.io/coredns/coredns                                v1.8.4                                                                       8d147537fb7d   15 months ago   47.6MB
kindest/node                                              <none>                                                                       32b8b755dee8   15 months ago   1.12GB
docker/desktop-vpnkit-controller                          v2.0                                                                         8c2c38aa676e   16 months ago   21MB
docker/desktop-storage-provisioner                        v2.0                                                                         99f89471f470   16 months ago   41.9MB
k8s.gcr.io/pause                                          3.5                                                                          ed210e3e4a5b   18 months ago   683kB
root@LAPTOP-HUPVGV43:~# sudo docker pull mcr.microsoft.com/mssql/server:2022-latest
2022-latest: Pulling from mssql/server
9e92253e66cd: Pull complete
03f9a33f72ef: Pull complete
889f53a1308c: Pull complete
Digest: sha256:ea5e3a6dd0535fadeccfc2919a33d81bf9f48f1581681a1454399bce0dd88ba5
Status: Downloaded newer image for mcr.microsoft.com/mssql/server:2022-latest
mcr.microsoft.com/mssql/server:2022-latest
root@LAPTOP-HUPVGV43:~# sudo docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Keroro20220606$" \
  -p 143>    -p 1433:1433 --name mssql1 --hostname mssql1 \
>    -d \
>    mcr.microsoft.com/mssql/server:2022-latest
978dfb61e2439049e7edb7609b25168db5fac2db16452825667b916e1e7d0b73
root@LAPTOP-HUPVGV43:~#
root@LAPTOP-HUPVGV43:~#
root@LAPTOP-HUPVGV43:~#
root@LAPTOP-HUPVGV43:~# docker ps -a
CONTAINER ID   IMAGE                                        COMMAND                  CREATED         STATUS         PORTS                                                                 NAMES
978dfb61e243   mcr.microsoft.com/mssql/server:2022-latest   "/opt/mssql/bin/perm…"   4 seconds ago   Up 3 seconds   0.0.0.0:1433->1433/tcp                                                mssql1
3284168ac7b0   99f89471f470                                 "/storage-provisione…"   2 weeks ago     Up 2 weeks                                                                           k8s_storage-provisioner_storage-provisioner_kube-system_9097e1b1-f511-4dae-ab5a-a71f627c9f6a_5
b52fdbcb1e52   a4ca41631cc7                                 "/coredns -conf /etc…"   2 weeks ago     Up 2 weeks                                                                           k8s_coredns_coredns-6d4b75cb6d-6czg7_kube-system_7e282468-d710-4b7c-b601-104357800aa6_3
41b0c4aee9e1   k8s.gcr.io/pause:3.7                         "/pause"                 2 weeks ago     Up 2 weeks                                                                           k8s_POD_vpnkit-controller_kube-system_d2705682-3032-4a30-95bd-5ac08039f86c_3
0bb177fa73ae   a4ca41631cc7                                 "/coredns -conf /etc…"   2 weeks ago     Up 2 weeks                                                                           k8s_coredns_coredns-6d4b75cb6d-q8fxc_kube-system_bd679124-b77f-4126-9409-33dab4e8c830_3
76e70daabc75   a634548d10b0                                 "/usr/local/bin/kube…"   2 weeks ago     Up 2 weeks                                                                           k8s_kube-proxy_kube-proxy-jvwdr_kube-system_b4344daa-3731-4017-aec4-ff99c2460c0f_3
41bed96f1861   k8s.gcr.io/pause:3.7                         "/pause"                 2 weeks ago     Up 2 weeks                                                                           k8s_POD_coredns-6d4b75cb6d-6czg7_kube-system_7e282468-d710-4b7c-b601-104357800aa6_3
6e7bc6e69f2c   k8s.gcr.io/pause:3.7                         "/pause"                 2 weeks ago     Up 2 weeks                                                                           k8s_POD_storage-provisioner_kube-system_9097e1b1-f511-4dae-ab5a-a71f627c9f6a_3
937d3dc512e7   k8s.gcr.io/pause:3.7                         "/pause"                 2 weeks ago     Up 2 weeks                                                                           k8s_POD_kube-proxy-jvwdr_kube-system_b4344daa-3731-4017-aec4-ff99c2460c0f_3
1d087775abb7   k8s.gcr.io/pause:3.7                         "/pause"                 2 weeks ago     Up 2 weeks                                                                           k8s_POD_coredns-6d4b75cb6d-q8fxc_kube-system_bd679124-b77f-4126-9409-33dab4e8c830_3
59c63f88ef15   d3377ffb7177                                 "kube-apiserver --ad…"   2 weeks ago     Up 2 weeks                                                                           k8s_kube-apiserver_kube-apiserver-docker-desktop_kube-system_f59181e45aa4f2d140b33c1ad42bf0f0_3
bfe7976901bc   aebe758cef4c                                 "etcd --advertise-cl…"   2 weeks ago     Up 2 weeks                                                                           k8s_etcd_etcd-docker-desktop_kube-system_2449ddc0985e3be8dd23ffc4d12cb53b_3
9013a89d8483   5d725196c1f4                                 "kube-scheduler --au…"   2 weeks ago     Up 2 weeks                                                                           k8s_kube-scheduler_kube-scheduler-docker-desktop_kube-system_a31c4b29a6bb804ea33360ba0a65dc67_3
dbfe58b6bbf9   34cdf99b1bb3                                 "kube-controller-man…"   2 weeks ago     Up 2 weeks                                                                           k8s_kube-controller-manager_kube-controller-manager-docker-desktop_kube-system_738606756aab710f2003c9939fe352c3_3
411fdf72bf22   k8s.gcr.io/pause:3.7                         "/pause"                 2 weeks ago     Up 2 weeks                                                                           k8s_POD_kube-apiserver-docker-desktop_kube-system_f59181e45aa4f2d140b33c1ad42bf0f0_3
8bd828e24e1c   k8s.gcr.io/pause:3.7                         "/pause"                 2 weeks ago     Up 2 weeks                                                                           k8s_POD_etcd-docker-desktop_kube-system_2449ddc0985e3be8dd23ffc4d12cb53b_3
dfcea006dce6   k8s.gcr.io/pause:3.7                         "/pause"                 2 weeks ago     Up 2 weeks                                                                           k8s_POD_kube-controller-manager-docker-desktop_kube-system_738606756aab710f2003c9939fe352c3_3
adcd6d91c4ce   k8s.gcr.io/pause:3.7                         "/pause"                 2 weeks ago     Up 2 weeks                                                                           k8s_POD_kube-scheduler-docker-desktop_kube-system_a31c4b29a6bb804ea33360ba0a65dc67_3
35a38495a63e   kindest/node:v1.23.1                         "/usr/local/bin/entr…"   7 months ago    Up 2 weeks     0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp, 127.0.0.1:39831->6443/tcp   flask-api-control-plane
e0a8891f05f8   registry:2                                   "/entrypoint.sh /etc…"   8 months ago    Up 2 weeks     0.0.0.0:5000->5000/tcp, :::5000->5000/tcp                             local-registry
root@LAPTOP-HUPVGV43:~# docker exec -t mssql1 cat /var/opt/mssql/log/errorlog | grep connection
2022-09-08 12:15:48.38 Server      The maximum number of dedicated administrator connections for this instance is '1'
2022-09-08 12:15:49.90 Server      Dedicated admin connection support was established for listening locally on port 1434.
2022-09-08 12:15:49.91 spid54s     SQL Server is now ready for client connections. This is an informational message; no user action is required.
2022-09-08 12:15:52.22 spid62s     Always On: The availability replica manager is waiting for the instance of SQL Server to allow client connections. This is an informational message only. No user action is required.
root@LAPTOP-HUPVGV43:~# sudo docker exec -it mssql1 "bash"
mssql@mssql1:/$ bash
mssql@mssql1:/$ /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "Keroro20220606$"
1> CREATE DATABASE TestDB;
2>
3>
4>
5> SELECT Name from sys.databases;
6>
7>
8>
9> go
Name
--------------------------------------------------------------------------------------------------------------------------------
master
tempdb
model
msdb
TestDB

(5 rows affected)
1> USE TestDB;
2> CREATE TABLE Inventory (id INT, name NVARCHAR(50), quantity INT);
3> INSERT INTO Inventory VALUES (1, 'banana', 150); INSERT INTO Inventory VALUES (2, 'orange', 154);
4> go
Changed database context to 'TestDB'.

(1 rows affected)

(1 rows affected)
1>
2>
3>
4>
5> SELECT * FROM Inventory WHERE quantity > 152;
6> GO
id          name                                               quantity
----------- -------------------------------------------------- -----------
          2 orange                                                     154

(1 rows affected)
1> SELECT * FROM Inventory WHERE quantity > 152;
2>
3> go
id          name                                               quantity
----------- -------------------------------------------------- -----------
          2 orange                                                     154

(1 rows affected)
1> go
1> SELECT * FROM Inventory WHERE quantity > 152;
2> go
id          name                                               quantity
----------- -------------------------------------------------- -----------
          2 orange                                                     154

(1 rows affected)
1> exit;
2> quit;
3>
```
### Oracle Databaes configuration
Oracle VirtualBox Developer Day existing image

### Step 1 Oracle Database Gateway installation
```
[oracle@localhost ~]$ cd Downloads/
[oracle@localhost Downloads]$ ls -ltr
total 983864
drwxr-xr-x. 5 oracle oinstall         85 Apr 17  2019 gateways
-rwxrwx---. 1 oracle oinstall 1007154302 Sep  8 12:27 LINUX.X64_193000_gateways.zip
-rwxrwx---. 1 oracle oinstall     317816 Sep  8 14:10 jtds-1.3.1.jar
[oracle@localhost Downloads]$ cd gateways
[oracle@localhost gateways]$ ls -ltr
total 24
-rwxrwxr-x.  1 oracle oinstall  500 Feb  6  2013 welcome.html
-rwxr-xr-x.  1 oracle oinstall 8850 Apr 17  2019 runInstaller
drwxr-xr-x.  4 oracle oinstall 4096 Apr 17  2019 install
drwxrwxr-x.  2 oracle oinstall   35 Apr 17  2019 response
drwxr-xr-x. 16 oracle oinstall 4096 Apr 17  2019 stage
[oracle@localhost gateways]$ ./runInstaller
Starting Oracle Universal Installer...

Checking Temp space: must be greater than 415 MB.   Actual 14481 MB    Passed
Checking swap space: must be greater than 150 MB.   Actual 4095 MB    Passed
Checking monitor: must be configured to display at least 256 colors.    Actual 16777216    Passed
Preparing to launch Oracle Universal Installer from /tmp/OraInstall2022-09-08_02-14-08PM. Please wait ...[oracle@localhost gateways]$ The response file for this session can be found at:
 /u01/app/oracle/product/12.2/gw_mssql/install/response/tg_2022-09-08_02-14-08PM.rsp

You can find the log of this install session at:
 /u01/installervb/logs/installActions2022-09-08_02-14-08PM.log

[oracle@localhost gateways]$
[oracle@localhost gateways]$
```

### Step 2 Oracle Database Gateway software configuration
TO-DO

### Step 3 Listener Configuration
```
[oracle@localhost gateways]$ lsnrctl status

LSNRCTL for Linux: Version 12.2.0.1.0 - Production on 08-SEP-2022 14:34:01

Copyright (c) 1991, 2016, Oracle.  All rights reserved.

Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=IPC)(KEY=EXTPROC1)))
STATUS of the LISTENER
------------------------
Alias                     LISTENER
Version                   TNSLSNR for Linux: Version 12.2.0.1.0 - Production
Start Date                08-SEP-2022 13:59:26
Uptime                    0 days 0 hr. 34 min. 35 sec
Trace Level               off
Security                  ON: Local OS Authentication
SNMP                      OFF
Default Service           orcl12c
Listener Parameter File   /u01/app/oracle/product/12.2/db_1/network/admin/listener.ora
Listener Log File         /u01/app/oracle/diag/tnslsnr/localhost/listener/alert/log.xml
Listening Endpoints Summary...
  (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1)))
  (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=0.0.0.0)(PORT=1521)))
  (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=localhost)(PORT=8081))(Presentation=HTTP)(Session=RAW))
Services Summary...
Service "51c99766d7e2568de0530100007f4fae" has 1 instance(s).
  Instance "orcl12c", status READY, has 1 handler(s) for this service...
Service "orcl" has 1 instance(s).
  Instance "orcl12c", status READY, has 1 handler(s) for this service...
Service "orcl12c" has 2 instance(s).
  Instance "orcl12c", status UNKNOWN, has 1 handler(s) for this service...
  Instance "orcl12c", status READY, has 1 handler(s) for this service...
Service "orcl12cXDB" has 1 instance(s).
  Instance "orcl12c", status READY, has 1 handler(s) for this service...
The command completed successfully
```
-- Update listener.ora file
```
[oracle@localhost admin]$ pwd
/u01/app/oracle/product/12.2/db_1/network/admin
[oracle@localhost admin]$ ls -ltr
total 16
-rw-r--r--. 1 oracle oinstall 1441 Aug 28  2015 shrept.lst
drwxr-xr-x. 2 oracle oinstall   61 Jun 12  2017 samples
-rw-r--r--. 1 oracle oinstall   53 Jun 12  2017 sqlnet.ora
-rw-r--r--. 1 oracle oinstall  734 Sep  8 15:42 tnsnames.ora
-rw-r--r--. 1 oracle oinstall  820 Sep  8 15:43 listener.ora
[oracle@localhost admin]$ cat listener.ora
SID_LIST_LISTENER =
  (SID_LIST =
    (SID_DESC =
      (GLOBAL_DBNAME = orcl12c)
      (SID_NAME = orcl12c)
      (ORACLE_HOME = /u01/app/oracle/product/12.2/db_1)
    )
  )

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1))
      (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521))
    )
  )

#HOSTNAME by pluggable not working rstriction or configuration error.
DEFAULT_SERVICE_LISTENER = (orcl12c)

SID_LIST_LISTENER_GW =
  (SID_LIST =
    (SID_DESC =
      (PROGRAM = dg4msql)
      (SID_NAME = dg4msql)
      (ORACLE_HOME = /u01/app/oracle/product/12.2/gw_mssql)
    )
  )

LISTENER_GW =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1))
      (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1531))
    )
  )

[oracle@localhost admin]$
```

-- Start LISTENER_GW
```
[oracle@localhost admin]$ ps -ef | grep tns
root        23     2  0 13:58 ?        00:00:00 [netns]
oracle   21907     1  0 17:55 ?        00:00:00 /u01/app/oracle/product/12.2/db_1/bin/tnslsnr LISTENER -inherit
oracle   22033 13994  0 17:58 pts/1    00:00:00 grep --color=auto tns
[oracle@localhost admin]$ env | grep ORA
ORACLE_UNQNAME=orcl12c
ORACLE_SID=orcl12c
ORACLE_BASE=/u01/app/oracle
ORACLE_HOME=/u01/app/oracle/product/12.2/gw_mssql
[oracle@localhost admin]$ env | grep TNS
[oracle@localhost admin]$ export TNS_ADMIN=/u01/app/oracle/product/12.2/gw_mssql/dg4msql/admin
[oracle@localhost admin]$ lsnrctl start LISTENER_GW

LSNRCTL for Linux: Version 19.0.0.0.0 - Production on 08-SEP-2022 18:00:32

Copyright (c) 1991, 2019, Oracle.  All rights reserved.

TNS-01106: Listener using listener name LISTENER has already been started
```

-- Reload listener
```
[oracle@localhost admin]$ lsnrctl reload LISTENER_GW

LSNRCTL for Linux: Version 19.0.0.0.0 - Production on 08-SEP-2022 18:29:50

Copyright (c) 1991, 2019, Oracle.  All rights reserved.

Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=IPC)(KEY=EXTPROC2)))
The command completed successfully
[oracle@localhost admin]$ ps -ef | grep tns
root        23     2  0 13:58 ?        00:00:00 [netns]
oracle   21907     1  0 17:55 ?        00:00:00 /u01/app/oracle/product/12.2/db_1/bin/tnslsnr LISTENER -inherit
oracle   22385     1  0 18:08 ?        00:00:00 /u01/app/oracle/product/12.2/gw_mssql/bin/tnslsnr LISTENER_GW -inherit
oracle   22957 13994  0 18:29 pts/1    00:00:00 grep --color=auto tns

```

### Step 4 tnsnames.ora file configuration
```
[oracle@localhost admin]$ pwd
/u01/app/oracle/product/12.2/db_1/network/admin
[oracle@localhost admin]$ ls -ltr
total 16
-rw-r--r--. 1 oracle oinstall 1441 Aug 28  2015 shrept.lst
drwxr-xr-x. 2 oracle oinstall   61 Jun 12  2017 samples
-rw-r--r--. 1 oracle oinstall   53 Jun 12  2017 sqlnet.ora
-rw-r--r--. 1 oracle oinstall  734 Sep  8 15:42 tnsnames.ora
-rw-r--r--. 1 oracle oinstall  820 Sep  8 15:43 listener.ora
[oracle@localhost admin]$ cat tnsnames.ora
# tnsnames.ora Network Configuration File: /u01/app/oracle/product/12.2/db_1/network/admin/tnsnames.ora
# Generated by Oracle configuration tools.

ORCL12C =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orcl12c)
    )
  )

LISTENER_ORCL12C =
  (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521))


ORCL =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orcl)
    )
  )

dg4msql =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1531))
    (CONNECT_DATA =
      (SID = dg4msql)
    )
    (HS = OK)
  )
[oracle@localhost admin]$
```

### Step 5 initdg4msql.ora file configuration
```
[oracle@localhost admin]$ pwd
/u01/app/oracle/product/12.2/gw_mssql/dg4msql/admin
[oracle@localhost admin]$ ls -ltr
total 28
-rw-rw-r--. 1 oracle oinstall   746 Jun  8  2007 dg4msql_tx.sql
-rw-rw-r--. 1 oracle oinstall 11120 Dec 17  2013 dg4msql_cvw.sql
-rw-rw-r--. 1 oracle oinstall   244 Sep  8 14:18 tnsnames.ora.sample
-rw-rw-r--. 1 oracle oinstall   409 Sep  8 14:18 listener.ora.sample
-rw-rw-r--. 1 oracle oinstall   362 Sep  8 18:29 initdg4msql.ora
[oracle@localhost admin]$ pwd
/u01/app/oracle/product/12.2/gw_mssql/dg4msql/admin
[oracle@localhost admin]$ cat initdg4msql.ora
# This is a customized agent init file that contains the HS parameters
# that are needed for the Database Gateway for Microsoft SQL Server

#
# HS init parameters
#
HS_FDS_CONNECT_INFO=192.168.54.1:1433//TestDB
# alternate connect format is hostname/serverinstance/databasename
HS_FDS_TRACE_LEVEL=OFF
HS_FDS_RECOVERY_ACCOUNT=RECOVER
HS_FDS_RECOVERY_PWD=RECOVER

[oracle@localhost admin]$

```

### Step 6 Database Link creation
```
[oracle@localhost admin]$ env | grep ORA
ORACLE_UNQNAME=orcl12c
ORACLE_SID=orcl12c
ORACLE_BASE=/u01/app/oracle
ORACLE_HOME=/u01/app/oracle/product/12.2/db_1
[oracle@localhost admin]$ sqlplus / as sysdba

SQL*Plus: Release 12.2.0.1.0 Production on Thu Sep 8 15:03:10 2022

Copyright (c) 1982, 2016, Oracle.  All rights reserved.


Connected to:
Oracle Database 12c Enterprise Edition Release 12.2.0.1.0 - 64bit Production

SQL> show con_id

CON_ID
------------------------------
1
SQL> create database link GW_LINK connect to "SA" identified by "Keroro20220606$" using 'dg4msql';

Database link created.

```

### Testing the connection

```
[oracle@localhost oracle]$ . orane
bash: orane: No such file or directory
[oracle@localhost oracle]$ . oraenv
ORACLE_SID = [orcl12c] ?
ORACLE_BASE environment variable is not being set since this
information is not available for the current user ID oracle.
You can set ORACLE_BASE manually if it is required.
Resetting ORACLE_BASE to its previous value or ORACLE_HOME
The Oracle base remains unchanged with value /u01/app/oracle
[oracle@localhost oracle]$
[oracle@localhost oracle]$
[oracle@localhost oracle]$
[oracle@localhost oracle]$ sqlplus / as sysdba

SQL*Plus: Release 12.2.0.1.0 Production on Thu Sep 8 18:31:15 2022

Copyright (c) 1982, 2016, Oracle.  All rights reserved.


Connected to:
Oracle Database 12c Enterprise Edition Release 12.2.0.1.0 - 64bit Production

SQL> select * from "inventory"@GW_LINK;

	id name 						quantity
---------- -------------------------------------------------- ----------
	 1 banana						     150
	 2 orange						     154

SQL> select * from "inventory"@GW_LINK;

	id name 						quantity
---------- -------------------------------------------------- ----------
	 1 banana						     150
	 2 orange						     154

SQL>
```


### Troubleshooting

Error message

```
SQL> select * from "inventory"@GW_LINK
  2  ;
select * from "inventory"@GW_LINK
                          *
ERROR at line 1:
ORA-28500: connection from ORACLE to a non-Oracle system returned this message:
[Oracle][ODBC SQL Server Wire Protocol driver]Connection refused. Verify Host
Name and Port Number. {08001}
ORA-02063: preceding 2 lines from GW_LINK
```

```
SQL> select * from dual@GW_LINK;
select * from dual@GW_LINK
                   *
ERROR at line 1:
ORA-28545: error diagnosed by Net8 when connecting to an agent
Unable to retrieve text of NETWORK/NCR message 65535
ORA-02063: preceding 2 lines from GW_LINK
```
