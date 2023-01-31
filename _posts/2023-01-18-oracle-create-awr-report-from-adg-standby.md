---
title: "Create AWR report from Active Data Guard Standby database"
date: 2023-01-18
last_modified_at: 2023-01-18T16:20:02-05:00
categories:
  - Blog
tags:
  - Oracle 19c
  - MAA
---

### Synopsis
The Active Data Guard option is an important part of Oracle MAA reference architecture, the Oracle Active Data Guard 19c gives us a lot of great features beyond the regular Data Guard. 

- Read Only Standby Database to run ad-hoc queries, reports
- Active Standby DML redirection
- Automatic Block Repair
- Far sync for zero data loss protection at any distance
- Rolling Upgrade
- Application Continuity

When you configure your Active Data Guard in long distance replication or cross region replication, you might face performance issue of the Active Data Guard or database performance issue when you have the read only standby database with the long running queries/reports/backups. 

As DBA, our first course of actions is to get the AWR report from the standby database, and soon you will find out that it keeps gerenrating AWR report based on the AWR data of the primary database. Starting from Oracle Database 12.2, AWR data can be captured for Active Data Guard standby database. This great feature opens the door to analyze performance-related issues for ADG standby databases. 

### Use Case
- Check the open mode and database role for the primary and standby databases

```
-- primary
SQL> select db_unique_name,open_mode, database_role from v$database;

DB_UNIQUE_NAME		       OPEN_MODE	    DATABASE_ROLE
------------------------------ -------------------- ----------------
ORCL			       READ WRITE	    PRIMARY

-- standby
SQL> select db_unique_name,open_mode, database_role from v$database;

DB_UNIQUE_NAME		       OPEN_MODE	    DATABASE_ROLE
------------------------------ -------------------- ----------------
ORCLSTBY		       READ ONLY WITH APPLY PHYSICAL STANDBY
```

- The SYS\$UMF user is the default database user that has all the privileges to access the system-level Remote Management Framework (RMF) views and tables. All the AWR related operations in RMF can be performed only by the SYS\$UMF user.

- The SYS\$UMF user is locked by default and it must be unlocked before deploying the RMF topology:

```
SQL> alter user "SYS$UMF" identified by oracle account unlock; 

User altered.

-- primary and standby
SQL> select username,common,account_status from dba_users where username ='SYS$UMF';

USERNAME
--------------------------------------------------------------------------------
COM ACCOUNT_STATUS
--- --------------------------------
SYS$UMF
YES OPEN

```

- Enable hidden parameter _umf_remote_enabled to set to TRUE

```
-- primary and standby
SQL> alter system set "_umf_remote_enabled"=TRUE scope=BOTH;

System altered.

```

- Create database link between the primary database and the standby database and vice versa

```
-- primary
SQL> CREATE DATABASE LINK "PRIMARY_TO_STANDBY_DBLINK" CONNECT TO "SYS$UMF" IDENTIFIED BY oracle using 'ORCLSTBY';

Database link created.

SQL> CREATE DATABASE LINK "STANDBY_TO_PRIMARY_DBLINK" CONNECT TO "SYS$UMF" IDENTIFIED BY oracle using 'ORCL';

Database link created.

SQL> select db_link, username, host from dba_db_links; 

DB_LINK
--------------------------------------------------------------------------------
USERNAME
--------------------------------------------------------------------------------
HOST
--------------------------------------------------------------------------------

PRIMARY_TO_STANDBY_DBLINK
SYS$UMF
ORCLSTBY

STANDBY_TO_PRIMARY_DBLINK
SYS$UMF
ORCL

```

- Validate the database links

```
SQL> select db_unique_name from v$database@STANDBY_TO_PRIMARY_DBLINK;

DB_UNIQUE_NAME
------------------------------
ORCL

SQL> select db_unique_name from v$database@PRIMARY_TO_STANDBY_DBLINK;

DB_UNIQUE_NAME
------------------------------
ORCLSTBY
```

- Configure database nodes to add to the topology, each database node in a topology must be assigned a unique name

```
-- primary
SQL> exec dbms_umf.configure_node ('primary_site');

PL/SQL procedure successfully completed.

-- standby
SQL> exec dbms_umf.configure_node('standby_site','STANDBY_TO_PRIMARY_DBLINK');

PL/SQL procedure successfully completed.

```

- Create the UMF topology, 

```

SQL> exec DBMS_UMF.create_topology ('Topology_1');

PL/SQL procedure successfully completed.

SQL> select * from dba_umf_topology;

TOPOLOGY_NAME
--------------------------------------------------------------------------------
 TARGET_ID TOPOLOGY_VERSION TOPOLOGY
---------- ---------------- --------
Topology_1
3588577726		  1 ACTIVE


SQL> select * from dba_umf_registration;

TOPOLOGY_NAME
--------------------------------------------------------------------------------
NODE_NAME
--------------------------------------------------------------------------------
   NODE_ID  NODE_TYPE AS_SO AS_CA STATE
---------- ---------- ----- ----- --------------------
Topology_1
primary_site
3588577726	    0 FALSE FALSE OK

-- You can drop the topology by using exec DBMS_UMP.drop_topology function
```

- Add standby node to the topology, you need to include both DBLinks that we created earlier

```
-- primary
SQL> exec DBMS_UMF.register_node ('Topology_1', 'standby_site', 'PRIMARY_TO_STANDBY_DBLINK', 'STANDBY_TO_PRIMARY_DBLINK', 'FALSE', 'FALSE');

PL/SQL procedure successfully completed.

SQL> select * from dba_umf_registration;
TOPOLOGY_NAME															 NODE_NAME									     NODE_ID  NODE_TYPE AS_SO AS_CA STATE
-------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------- ---------- ---------- ----- ----- --------------------
Topology_1															 primary_site									  3588577726	      0 FALSE FALSE OK
Topology_1															 standby_site									    18526484	      0 FALSE FALSE OK
```

- Register standby node for the AWR service

```
-- primary
SQL> exec DBMS_WORKLOAD_REPOSITORY.register_remote_database(node_name=>'standby_site');

PL/SQL procedure successfully completed.

SQL> select * from dba_umf_service;

TOPOLOGY_NAME															    NODE_ID SERVICE
-------------------------------------------------------------------------------------------------------------------------------- ---------- -------
Topology_1															   18526484 AWR

SQL> select * from dba_umf_link;

TOPOLOGY_NAME															 FROM_NODE_ID TO_NODE_ID LINK_NAME
-------------------------------------------------------------------------------------------------------------------------------- ------------ ---------- --------------------------------------------------------------------------------------------------------------------------------
Topology_1															   3588577726	18526484 PRIMARY_TO_STANDBY_DBLINK
Topology_1															     18526484 3588577726 STANDBY_TO_PRIMARY_DBLINK

```

- Once we have everything configured, we can generate some remote snapshots

```
SQL> alter system archive log current;

System altered.

SQL> exec dbms_workload_repository.create_remote_snapshot('standby_site');

PL/SQL procedure successfully completed.

SQL> exec dbms_workload_repository.create_remote_snapshot('standby_site');

PL/SQL procedure successfully completed.

SQL> exec dbms_workload_repository.create_remote_snapshot('standby_site');

PL/SQL procedure successfully completed.

```

- We can run AWR report for the standby database now, you can run awrrpti.sql script from either primary database or standby database. 

```
-- primary
SQL> @?/rdbms/admin/awrrpti.sql

Specify the Report Type
~~~~~~~~~~~~~~~~~~~~~~~
AWR reports can be generated in the following formats.	Please enter the
name of the format at the prompt. Default value is 'html'.

   'html'	   HTML format (default)
   'text'	   Text format
   'active-html'   Includes Performance Hub active report

Enter value for report_type: html

Type Specified: html


Instances in this Workload Repository schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  DB Id      Inst Num	DB Name      Instance	  Host
------------ ---------- ---------    ----------   ------
  18526484	 1	ORCL	     ORCL	  instance-202
* 1638846667	 1	ORCL	     ORCL	  instance-202

Enter value for dbid: 18526484
Using 18526484 for database Id
Enter value for inst_num: 1
Using 1 for instance number


Specify the number of days of snapshots to choose from
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Entering the number of days (n) will result in the most recent
(n) days of snapshots being listed.  Pressing <return> without
specifying a number lists all completed snapshots.


Enter value for num_days: 2

Listing the last 2 days of Completed Snapshots
Instance     DB Name	  Snap Id	Snap Started	Snap Level
------------ ------------ ---------- ------------------ ----------

ORCL	     ORCL		  1  07 Oct 2022 22:04	  1
				  2  07 Oct 2022 22:04	  1
				  3  07 Oct 2022 22:05	  1

```

### References
- How to Generate AWRs in Active Data Guard Standby Databases (Doc ID 2409808.1)