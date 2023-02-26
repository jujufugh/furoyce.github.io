---
title: "Oracle Multitenant licensing change on Non-Oracle Cloud"
date: 2023-01-29
last_modified_at: 2023-01-29T16:20:02-05:00
categories:
  - Blog
tags:
  - Oracle 19c
  - Oracle License
---

You might come across the following issue when creating PDBs on Non-Oracle Cloud vendors such as AWS, Google GCP, Microsoft Azure etc in Oracle 12c, 18c or 19c. 

```
SQL> create pluggable database PDB4;

create pluggable database PDB4
                          *
ERROR at line 1:
ORA-65010: maximum number of pluggable databases created

```

Even you have the max_pdbs parameter set to a much higher value

```
SQL> show parameter max_pdbs
NAME     TYPE    VALUE
-------- ------- -----
max_pdbs integer 10
```

You can check your multitenant feature usage using following SQL: 

```
SQL> select name feature_name,version,detected_usages,aux_count 
     from dba_feature_usage_statistics 
     where name like '%Pluggable%' or name like '%Multitenant%';
 
FEATURE_NAME
--------------------------------------------------------------------------------
VERSION           DETECTED_USAGES  AUX_COUNT
----------------- --------------- ----------
Oracle Multitenant
19.12                    3       10
```

So with the Multitenant feature, you can't create the fourth user PDB on Non-Oracle Cloud Environment. You probably tried to use following workaround to bypass this limitation due to the bug. 

```
SQL> alter system set "_cdb_disable_pdb_limit"=true scope=spfile;
System altered.
```

When you run the strace on the Oracle process, you can see that it checks for the non_oracle_cloud_provider

```
> /u01/app/oracle/product/18/db_home1/bin/oracle(kgcs_clouddb_provider_detect+0xf9) [0x49ffce9]
 > /u01/app/oracle/product/18/db_home1/bin/oracle(kscs_is_non_oracle_cloud+0x244) [0x13f1104]
```

With the latest update in the licensing document by **Jan-29-2023**, you can see that the Multitenant use is limted to three pluggable databases per container for Non-Oracle Cloud Environments. I guess it's the time to make sure that you are compliant with this limitation. 

<img src='/images/posts/2023-01-29/snap-2023-01-29-at-12.59.56-AM.png'>

