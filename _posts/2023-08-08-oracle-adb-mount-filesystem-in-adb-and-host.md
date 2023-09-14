---
title: "Mount Oracle Filesytem service mount target in Autonomous Database and OCI compute instance"
date: 2023-08-30
last_modified_at: 2023-09-01T16:20:02-05:00
categories:
  - Blog
tags:
  - Oracle Filesystem service
  - Cloud Database
  - Oracle Cloud Infrastructure
  - Autonumous Database
---

### Introduction
Recently I was asked about a use case to run a set of homebrew SQL/PLSQL based monitoring scripts in Autonomous Database and collect logs for analysis and correlation in OCI Logging Analytics. It poses a challenge because Autonomous Database is a managed service which doesn't allow host level access even with the service offering Autonomous Database on Dedicated Exadata Infrastructure. However, Autonomous Database offers various options for interacting with external data sources, for instance, calling API endpoint, interacting with the OCI Object Storage, and OCI File Storage service.

![OCI O&M File Storage Server Reference Architecture](/images/posts/2023-09/fss_adb_reference_architecture.png){: .align-center}

#### Autonomous Database (OCI ADB) Overview
Oracle Autonomous Database is a fully automated service that makes it easy for all organizations to develop and deploy application workloads, regardless of complexity, scale, or criticality. The service’s converged engine supports diverse data types, simplifying application development and deployment from modeling and coding to ETL, database optimization, and data analysis. With machine learning–driven automated tuning, scaling, and patching, Autonomous Database delivers the highest performance, availability, and security for OLTP, analytics, batch, and Internet of Things (IoT) workloads. Built on Oracle Database and Oracle Exadata, Autonomous Database is available on Oracle Cloud Infrastructure (OCI) for serverless or dedicated deployments as well as on-premises with Oracle Exadata Cloud@Customer and OCI Dedicated Region.

#### File Storage Service (OCI FSS) Overview
Oracle Cloud Infrastructure File Storage Service is a fully managed elastic file system built for the cloud that enables customers to migrate their enterprise workloads to the cloud. Every file system scales automatically to accommodate the growth of up to 8 exabytes. File Storage eliminates the need to provision capacity in advance, so customers pay only for the capacity they need. File Storage also offers asynchronous replication, snapshot, and clone capabilities to simplify business continuity for enterprise applications.

The File Storage service supports the Network File System version 3.0 (NFSv3) protocol. The service supports the Network Lock Manager (NLM) protocol for file locking functionality.

### Technical Configuration

#### Configure Oracle File Storage Service 
* Prerequisite: Network Security Rules are properly configured for OCI File Storage Service
  * Stateful ingress from ALL ports in source CIDR block to TCP ports 111, 2048, 2049, and 2050.
  * Stateful ingress from ALL ports in source CIDR block to UDP ports 111 and 2048.
  * Stateful egress from TCP  ALL ports to ports 111, 2048, 2049, and 2050 in destination CIDR block.
  * Stateful egress from UDP  ALL ports to port 111 in destination CIDR block.
* Create a file system in OCI FSS
  * OCI Console: Home -> Storage -> File Storage -> File Systems -> Create File System
  * ![Create File System in OCI File Storage Service](/images/posts/2023-09/royce_blog_fss_adb_1.png){: .align-center}
* Configure the Mount Target so that it can be cross mounted between Autonomous Database and Compute instance

![OCI File Storage Service Mount Target](/images/posts/2023-09/royce_blog_fss_adb2.png){: .align-center}

* Get the FQDN for attaching the file system in ADB

#### Attach File System in Autonomous Database via DBMS_CLOUD_ADMIN package
* Create Oracle Database Directories
```
SQL> CREATE DIRECTORY PPFSS_DIR AS 'fss'; 

Directory created.

SQL> create directory FSS_TEST_DIR as 'fss/test/logs/PPADB1'; 

Directory created.

```

* Attach the File System
```
SQL> BEGIN
DBMS_CLOUD_ADMIN.ATTACH_FILE_SYSTEM (
    file_system_name      => 'PPFSS',
    file_system_location  => 'ppfsstest.testsubnet.test.oraclevcn.com:/ppfss',
    directory_name        => 'PPFSS_DIR',  
    description           => 'Source FSS data'                                   
);END;                                                                          
/
```

* Verify the File System is attached
```
SQL> SELECT file_system_name, file_system_location, directory_path FROM dba_cloud_file_systems;

FILE_SYSTEM_NAME
--------------------------------------------------------------------------------
FILE_SYSTEM_LOCATION
--------------------------------------------------------------------------------
DIRECTORY_PATH
--------------------------------------------------------------------------------
PPFSS
ppfsstest.testsubnet.test.oraclevcn.com:/ppfss
/u02/data/dbfs/hca7zs94/039E4EF45F9D9F8BE063526A000A3781/fss/
```

* Create a file using UTL_FILE package
Create file in root directory of the mount target
```
DECLARE
  l_file         UTL_FILE.FILE_TYPE;
  l_location     VARCHAR2(100) := 'PPFSS_DIR';
  l_filename     VARCHAR2(100) := 'test_root.csv';
BEGIN
  -- Open the file.
  l_file := UTL_FILE.FOPEN(l_location, l_filename, 'w');
   
  UTL_FILE.PUT(l_file, 'Scott, male, 1000');
 
  -- Close the file.
  UTL_FILE.FCLOSE(l_file);
END;
/ 
```

You can also create create file in subdirectories of the mount target
```
DECLARE
  l_file         UTL_FILE.FILE_TYPE;
  l_location     VARCHAR2(100) := 'FSS_TEST_DIR';
  l_filename     VARCHAR2(100) := 'test_sub.csv';
BEGIN
  -- Open the file.
  l_file := UTL_FILE.FOPEN(l_location, l_filename, 'w');
   
  UTL_FILE.PUT(l_file, 'Scott, male, 1000');
 
  -- Close the file.
  UTL_FILE.FCLOSE(l_file);
END;
/ 
```

* Verify the file is created
```
SELECT object_name FROM DBMS_CLOUD.LIST_FILES('PPFSS_DIR');

OBJECT_NAME 
______________ 
test_root.csv
```

* If you need to detach the file system from the ADB
```
BEGIN
  DBMS_CLOUD_ADMIN.DETACH_FILE_SYSTEM (
    file_system_name      => 'PPFSS'                                       
  );END;                                                                          
/    
```

#### Mount File System in Compute instance
* Get the oracle user and dba group uid and gid from the Autonomous Database
  * oracle uid is 1001
  * dba group gid 1006
* Create oracle user with the uid and dba group with the same gid in the compute instance
```
$ sudo groupadd -g 1006 dba
$ sudo useradd -u 1001 -g 1006 -m -s /bin/bash oracle
$ id oracle
uid=1001(oracle) gid=1006(dba) groups=1006(dba)
```

* Make sure the Squash ID setup properly in OCI File System
We can use Squash UID and Squash GID to map to particular uid and gid for the target mount, however the limitation is at the ADB side where we can only attach the file system to ADB under oracle database server process's uid and gid. 

**More reading regarding Squash Identity: **[Exploring Identity Squash with OCI File Storage Service](https://blogs.oracle.com/cloud-infrastructure/post/exploring-identity-squash-with-oci-file-storage-service)

* Mount the File System in the compute instance (Oracle Linux)
```
sudo yum install nfs-utils
sudo mkdir -p /mnt/ppfss
sudo mount ppfsstest.testsubnet.test.oraclevcn.com:/ppfss /mnt/ppfss
```

* Verify that you can see the file from the File Storage Service mount target in compute instance
```
$ cd /mnt/ppfss/test/logs/PPADB1/
$ ls -ltr
total 8
-rw-r--r--. 1 oracle dba 18 Aug 29 17:17 test_sub.csv
```

### Conclusion
Oracle Cloud Infrastructure File Storage Service provides the solution to attach the file system to the Autonomous Database and cross mount it to one or many compute instances so that we can have real time access to the log files or scripts across many cloud resources. The solution compliments the use cases and requirements that cannot be accomplished by an Object Storage integration with Autonomous Database. Please check out more use cases in the Oracle File Storage Service [documentation](https://docs.oracle.com/en-us/iaas/Content/File/home.htm).

### Reference
* [DBMS_CLOUD_ADMIN package Doc Reference](https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/dbms-cloud-admin.html#GUID-1C562DE9-066C-4D8B-B058-53F30E9061C3)
* [How to Attach a File System to your Autonomous Database](https://blogs.oracle.com/datawarehousing/post/attach-file-system-autonomous-database)
* [Exploring identity squash with OCI File Storage service](https://blogs.oracle.com/cloud-infrastructure/post/exploring-identity-squash-with-oci-file-storage-service)
* [Overview of File Storage](https://docs.oracle.com/en-us/iaas/Content/File/Concepts/filestorageoverview.htm#Overview_of_File_Storage)
* [Attach External File Storage to Autonomous Database on Dedicated Exadata Infrastructure](https://docs.oracle.com/en/cloud/paas/autonomous-database/dedicated/defsd/index.html#articletitle)

