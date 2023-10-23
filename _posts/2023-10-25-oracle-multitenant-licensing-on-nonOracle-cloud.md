---
title: "Oracle Multitenant licensing change on Non-Oracle Cloud"
date: 2023-10-25
last_modified_at: 2023-10-25T16:20:02-05:00
categories:
  - Blog
tags:
  - Oracle 19c
  - Oracle License
  - Oracle Multitenant
---

### Synopsis
I came across an issue a while back when creating pluggable databases in Azure. When you create the forth PDB in your Oracle database server(Azure VM), you will find the following interesting error. 

```
SQL> create pluggable database PDB4;

create pluggable database PDB4
                          *
ERROR at line 1:
ORA-65010: maximum number of pluggable databases created

```

My first instinct would be we don't have multitenant license because if you are not licensed for Oracle Multitnant, you can still use Multitenant up to 3 user-created PDBs in a given CDB. 

With Multitenant license, you can use the full Multitenant options. 
* Enterprise Edition: create up to 252 PDBs
* Enterprise Edition with Engineering Systems(Exadata): create up to 4096 PDBs
* OCI Database Cloud Service with license included option(EE High Performance and EE Extreme Performance): create up to 4096 PDBs
* OCI Exadata Database Service: create up to 4096 PDBs

In this case, we have the Multitenant license for the Oracle database, unfortunately we still see the error. Even when we tried to have the max_pdbs parameter set to a much higher value.

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
 
FEATURE_NAME               VERSION           DETECTED_USAGES  AUX_COUNT             
-------------------------- ----------------- --------------- ----------
Oracle Multitenant         19.15             3                10

```

After additional cross reference in Oracle License documentation, we found a limitation in the Notes section about using Oracle Multitenant feature in Non-Oracle Cloud Environment.
**Non-Oracle Cloud Environments: Use is limited to three pluggable databases per container database.**

<img src='/images/posts/2023-01-29/snap-2023-01-29-at-12.59.56-AM.png'>

So with the Multitenant feature, you can't create the fourth user PDB on Non-Oracle Cloud Environment. You probably tried to use following [workaround](https://www.dbi-services.com/blog/oracle-disables-your-multitenant-option-when-you-run-on-ec2/) to bypass this limitation. 

```
SQL> alter system set "_cdb_disable_pdb_limit"=true scope=spfile;
System altered.
```

When you run the strace on the Oracle process, you can see that it checks for the non_oracle_cloud_provider

```
> /u01/app/oracle/product/19/db_home1/bin/oracle(kgcs_clouddb_provider_detect+0xf9) [0x49ffce9]
 > /u01/app/oracle/product/19/db_home1/bin/oracle(kscs_is_non_oracle_cloud+0x244) [0x13f1104]
```

### Conclusion
As you can see above, with the latest update in the licensing document, the Oracle Multitenant license usage is limted to three pluggable databases per container for Non-Oracle Cloud Environments. It's the time to make sure that you are compliant with this limitation.

### Reference
Creating More Than 3 PDBs Raises ORA-65011 Error In Enterprise Edition When On Public Cloud (Doc ID 2815338.1)
[Oracle Multitenant License Information](https://docs.oracle.com/en/database/oracle/oracle-database/19/dblic/Licensing-Information.html#GUID-0F9EB85D-4610-4EDF-89C2-4916A0E7AC87)
[Oracle disables your multitenant option when you run on EC2](https://www.dbi-services.com/blog/oracle-disables-your-multitenant-option-when-you-run-on-ec2/)
[Oracle DB on Azure with Multitenant Option](https://www.dbi-services.com/blog/oracle-db-on-azure-with-multitenant-option/)