---
title: "Maximizing Visibility: Collecting and Analyzing Logs from Oracle Databases using OCI Logging Analytics"
date: 2024-06-20
last_modified_at: 2024-06-20T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - Oracle Database
  - OCI Log Analytics
---

In this blog, we will unravel the significance of database logs and how Oracle Logging Analytics emerges as an ally in extracting valuable insights from the database logs. We will explore the intricacies of collecting logs from various Oracle databases, spanning across Linux and Windows environments and delving into the area of the Exadata Database system. These logs hold the key to unlocking powerful insights revealing the inner workings of your database's activities.  
  
Oracle Logging Analytics, a versatile and robust offering capable of channeling logs from a variety of log sources, with databases being a prominent among them. We leverage Logging Analytics’ ability to transform scattered log entries into a unified, coherent narrative, offering a comprehensive overview of your database operations.  
  
In this series, we will walk you through the pre-work required to prepare your environment, followed by a step-by-step guide on dowloading and installing the Management agent, a key tool for fetching database logs. Additionally, we cover the process of creating corresponding entities and log sources in OCI Logging Analytics, which enables the parsing of incoming log data. Finally, we show you how to leverage the Database Audit Dashboard to unlock valuable insights from your log data. By end of this series, you'll be equipped with the knowledge to successfully set up and utlize these powerful tools to enhance your database monitoring and auditing capabilities.

## Blog Content Guide

1.  [IAM Policies for the Management Agent](#IAM%20policies%20for%20the%20management%20agent)
2. [Download Management Agent on the Database Host](#Download%20Management%20Agent%20on%20the%20Database%20Host)
3. [Install Management on the Database Host](#Install%20Management%20Agent%20on%20the%20Database%20Host)
    1. [Install Management Agent on Linux Database Host](#Install%20Management%20Agent%20on%20Linux%20Database%20Host)
    2. [Install Management Agent on Windows Database Host](#Install%20Management%20Agent%20on%20Windows%20Database%20Host)
    3. [Install Management Agent on Exadata Database Service Dedicated Infrastructure or Exadata Database Service Cloud@Customer](#Install%20Management%20Agent%20on%20Exadata%20Database%20Service%20Dedicated%20Infrastructure%20or%20Exadata%20Database%20Service%20Cloud@Customer)
4. [Ingest Database Logs](#Ingest%20Database%20Logs)
    1. [For Linux Based Oracle Database: Ingesting File Based Logs](#For%20Linux%20Based%20Oracle%20Database:%20Ingesting%20File%20Based%20Logs)
    2. [For Linux Based Oracle Database: Ingesting Table Based Logs](#For%20Linux%20Based%20Oracle%20Database:%20Ingesting%20Table Based%20Logs)
    3. [For Windows Based Oracle Database](#For%20Windows%20Based%20Oracle%20Database)
5. [Unlocking Hidden Insights from Ingested Database Logs](#Unlocking%20Hidden%20Insights%20from%20Ingested%20Database%20Logs)
6. [References](#References)

## IAM Policies for the Management Agent

The Management Agent is a powerful tool that facilitates seamless log retrieval from database sources for analysis within Logging Analytics. To ensure smooth operations, the appropriate IAM policies must be in place, granting the necessary permissions to the IAM group intended for working with the Management Agent. These policies encompass permissions for managing agents, install keys, and dynamic groups. Additionally, the creation of dynamic groups specifically for management agents is crucial, along with the implementation of corresponding policies to enable log collection and metric ingestion for agents within these groups. This section discusses these IAM Policies and Dynamic Groups.

- Add policies to allow a group to work with management agents and install keys in the given compartment.  
      
    ​​​​​​ _ALLOW GROUP <group_name> TO MANAGE management-agents IN COMPARTMENT <compartment_name>_  
     _ALLOW GROUP <group_name> TO MANAGE management-agent-install-keys IN COMPARTMENT <compartment_name>_  
     _ALLOW GROUP <group_name> TO READ METRICS IN COMPARTMENT <compartment_name>  
     ALLOW GROUP <group_name> TO READ ALARMS IN COMPARTMENT <compartment_name>  
     ALLOW GROUP <group-name> TO READ USERS IN TENANCY_  
      
    **Note:** For more details on Management Agent Pre-requisites refer to_:_ [https://docs.oracle.com/en-us/iaas/management-agents/doc/perform-prerequisites-deploying-management-agents.htm](https://docs.oracle.com/en-us/iaas/management-agents/doc/perform-prerequisites-deploying-management-agents.html)l
- Ensure that the following policies are created for your Logging Analytics user group.

        _ALLOW GROUP Logging-Analytics-User-Group TO MANAGE management-agents IN COMPARTMENT <compartment_name>_  
        _ALLOW GROUP Logging-Analytics-User-Group to MANAGE management-agent-install- keys IN TENANCY_  
        _ALLOW GROUP Logging-Analytics-User-Group TO READ METRICS IN COMPARTMENT <compartment_name>_  
        _ALLOW GROUP Logging-Analytics-User-Group TO READ USERS IN TENANCY_  
  
         **Note**: _Logging-Analytics-User-Group_ is an example user group

- Creating a Management Agent Dynamic Group if it already doesn't exist

        _ALL {resource.type='managementagent', resource.compartment.id='<management_agent_compartment_OCID>'}_

- Create IAM policies for Management-Agent-Dynamic-Group to enable log collection and metrics generation.

        _ALLOW DYNAMIC-GROUP Management-Agent-Dynamic-Group TO USE METRICS IN TENANCY_  
         _ALLOW DYNAMIC-GROUP Management-Agent-Dynamic-Group TO {LOG_ANALYTICS_LOG_GROUP_UPLOAD_LOGS} IN TENANCY_     
     If the dynamic group is under a domain, then include the domain in the policy statement. For example,

     _ALLOW DYNAMIC-GROUP <identity_domain_name>/Management-Agent-Dynamic-Group TO USE METRICS IN TENANCY_  
     _ALLOW DYNAMIC-GROUP <identity_domain_name>/Management-Agent-Dynamic-Group TO {LOG_ANALYTICS_LOG_GROUP_UPLOAD_LOGS} IN TENANCY_  
  
    **Note**: If you use the Set Up Ingestion wizard to configure the Management Agent for log collection, then some of the above policy statements are added automatically.  

## Download Management Agent on the Database Host

In this section, we'll dive into the crucial step of acquiring the right Management Agent for your database environment. With multiple versions available, it is essential to download the correct one to ensure seamless integration and optimal performance. By the end of this section, you'll have the correct version of Management Agent in hand along with the corresponding response file which is essential for agent installation.  
Log in to the OCI console and navigate to **Observability & Management** -> **Management Agents** -> **Downloads & Keys**. For a **Linux** based Oracle Database, Download **Agents for LINUX (X86_64)**. For a **Windows** based Oracle Database, download **Agent for Windows (X86_64)**.

![MA_version](/images/posts/2025-blogs/blog-oci_database_info_listdbhomes_edit.png)

Figure 1. Management Agent Software Download for Linux based Database

![Win_agent_v](/images/posts/2025-blogs/blog-oci_database_info_listdbhomes_edit.png)

Figure 2. Management Agent Software Download for Windows based Database

For Exadata Database Service in OCI, Cloud@Customer or on-premises deployments, Download Agent for LINUX (X86_64) ZIP type from Software download section.  
Exadata Database Service only supports ZIP package type because Exadata Cloud lifecycle activities look for unknown rpms and will remove before patching. To avoid losing the agent and having to reinstall, the Management Agent needs to be installed using the ZIP method. Do not use the rpm method. 

![Figure. Management Agent for Exadata Database Service](/images/posts/2025-blogs/blog-oci_database_info_listdbhomes_edit.png)

Figure 3. Management Agent ZIP for Exadata Database Service

Before we start the management agent installation process, a crucial pre-install step is to download the Install Key to a file. This is useful to download the response file which will be used for the Management Agent installation on the database host.  
On the Management Agents home page, click on **Downloads and Keys** -> **Create Key**. Provide **Key name**, choice of **Compartment**, **Maximum installations** allowed for this key. Once they Install Key is created, navigate to the Install Key pane, click on the three dots on the right side and select **Download Key to File**.

![Install_Key](/images/posts/2025-blogs/blog-oci_database_info_listdbhomes_edit.png)

Figure 4: Create Install Key for Management Agent Installation

**Note:** Oracle recommends to keep the life time of an Install Key to a minimum required time and limited number of agents.

![Download Install key as rsp](/images/posts/2025-blogs/blog-oci_database_info_listdbhomes_edit.png)

Figure 5: Download Install Key as a file to create Response File

## Install Management Agent on the Database Host

With the necessary files in, we are ready to proceed with the installation of Management Agent.In this section, we will delve into the installation process, walking you through each key step and highlighting important considerations.

### Install Management Agent on Linux Database Host

As a best practice, move the management agent installation rpm file and downloaded response file to a **tmp** directory on the database host so that it can be deleted once the install is complete. Edit the response file to provide the required information such as Agent Display Name, uncomment any tag properties and uncomment the agent parameters that you require for your specific agent configuration and update the agent parameter value if needed.For example, in current implementation, uncomment and set **_Service.plugin.logan.download=true_** in the response file. This will enable Logging Analytics plugin for management agent.  
  
Plugins can also be enabled **via the OCI console** after the agent has been installed. To do that, navigate to **Observability & Management** -> **Management Agent** -> **Agents** and click on the name of the agent installed on the database host. Click on Deploy Plug-ins and select **Logging Analytics**.

![plug-in](/images/posts/2025-blogs/blog-oci_database_info_listdbhomes_edit.png)

Figure 6: Enable Logging Analytics Plug-in for the installed Management Agent​​​

To complete the installation of Management Agent software, login with a user with sudo privilege on the host and run the following command:

- _sudo rpm -ivh <rpm_file_name.rpm>_ 

This is the expected output:

![Install_output](/images/posts/2025-blogs/blog-oci_database_info_listdbhomes_edit.png)

Figure 7: Management Agent Install Output on Linux Database​​​​​

 **Note** : A new user called mgmt_agent is created. This will be the management agent user. All agent files are copied and installed by mgmt_agent user. The agent install base directory is the directory where the agent is installed. The directory is created as part of the agent installation process under /opt/oracle/mgmt_agent directory.

### **Ensure READ Access of the Logs for Management Agent User**

With the Management Agent installed, it is essential to configure agent user with the correct access rights to read logs without compromising security and compliance.In this section we will look at necessary steps to ensure management agent user has the necessary permissions and privileges.

- First you can check the current granted file permissions for the management agent user, _mgmt_agent_ by running the following command as an opc user:
    - _sudo -u <agentuser> /bin/bash -c "cat <log file with complete path">_

     If the management agent user cannot read the log files, then use one of the following methods (in the order of best practice) to make the log files readable to the management agent. Use Access Control Lists (ACLs) to      enable the cloud agent user to read the log file path and log files. Ensure that the full path to the log files is readable through the ACL.

- Grant the management agent user READ access to the required log file:
    - _sudo setfacl -m u:<agentuser>:r <path to the log file/log file name>_
- Grant the READ and EXECUTE permissions to each folder in the log file path:

                      _/__/set read, execute permissions on folders other than parent folder_ 

                   _sudo setfacl -m u:<agentuser>:rx <path to the folder>_

                  _//set read, execute permissions with recursive options on parent folder_

                      _sudo setfacl -R m y:<agentuser>:rx <path to the folder>_

                     _/__/set read, execute permissions with default option to allow all future log files created under this folder to be readable_

                     _sudo setfacl -d -m u:<agentuser>:rx <path to the folder>_

-    ​​​ ​​​​​​For nfs mount, it may not be possible to give READ and EXECUTE permission to the agent user to read the log files or folders. In such cases, add the agent user to the log file group:
    - _usermod -a -G <group of log file> <agentuser>_ 
-      Grant Restart the management agent after running the above command.

Place the management agent and the product that generates the logs in the same user group, and make the files readable to the entire group. Restart the agent. Make the log files readable to all users. For example, _chmod o+r <file>._ You may have to give executable permission to the parent folders. For example, _chmod o+rx <parent folder>_.

### Install Management Agent on Windows Database Host

In order to install management agent on a windows base database host, navigate to the directory where you have downloaded the management agent software and unzip it to any preferred location. To install and configure the management agent, login as an Administrator user, open a Command Prompt window and run the following command:

- _installer.bat <full_path_of_response_file>_

The output will look similar to the following:

1. ![agt_install](/images/posts/2025-blogs/blog-oci_database_info_listdbhomes_edit.png)
    
    Figure 8: Management Agent Install Output on Windows Database​​​​​
    
    

### Install Management Agent on Exadata Database Service Dedicated Infrastructure or Exadata Database Service Cloud@Customer

Oracle Exadata Database Service delivers proven Oracle Database capabilities on purpose-built, optimized Oracle Exadata infrastructure in the public cloud and on Cloud@Customer. Built-in cloud automation, elastic resource scaling, security, and fast performance for all Oracle Database workloads helps you simplify management and reduce costs. It is a crucial component for enterprises seeking to optimize their database performance and efficiency.

Given the complexity of managing an Exadata system, observability and monitoring are essential to achieving operational readiness. Comprehensive observability enables administrators to gain deep insights into system performance, detect anomalies, and address potential issues before they escalate into significant problems. To achieve comprehensive observability and management of Exadata systems, we recommend utilizing OCI Observability and Management (O&M) services such as Management Agent Cloud Service, Database Management Service, Ops Insights, and Logging Analytics. These services enable the collection and ingestion of Exadata system metrics and log data across various environments, including OCI, Cloud@Customer, and on-premises deployments.

- Download the Management Agent in ZIP format and transfer ZIP file to all Exadata cluster nodes (Do not use the RPM installation for Exadata deployments including on-premises, Cloud@Customer, and Oracle Cloud Infrastructure) 
- Due to the limited space on /opt, always create a symlink and install on /u02 (i.e. /u02/app/oracle/mgmt_agent)
- Create the Management Agent install directory on an external volume
    - $ sudo mkdir -p /u02/app/oracle/mgmt_agent
- Create a symbolic link in the /opt/oracle directory to point to the external volume
    - $ sudo ln -s /u02/app/oracle/mgmt_agent /opt/oracle/mgmt_agent
- Unzip the Management Agent software Linux ZIP file to the install_dir
    - $ sudo mkdir -p  /u02/app/oracle/mgmt_agent/install_dir
    - $ unzip /home/opc/<mgmt_agent_zip_file> -d /u02/app/oracle/mgmt_agent/install_dir
- Switch to a root shell, set the environment variable OPT_ORACLE_SYMLINK = true, and install the Management Agent software as root user. 
- Set JAVA_HOME if it’s not set properly
    - $ sudo /bin/bash
    - $ export OPT_ORACLE_SYMLINK=true
    - $ ./installer.sh <full_path_of_response_file>
- Validate you have installed the agent with the certified ZIP method and correct install location
    - Use systemctl status to view agent status and binary location
        - # systemctl status mgmt_agent
    - cat agent configuration and look for ZIP
        - # cat /opt/oracle/mgmt_agent/agent_inst/config/security/resource/agent.package | grep packageType=ZIP
    - Use rpm -qa to ensure the rpm version was not installed
- Enable Service Plug-ins available for Exadata Database Service
    - Database Management and Ops Insights Service
    - Logging Analytics
- Configure the Management Agent in accordance with appropriate resource requirements in the table below for the size of your environment
- Edit the properties file opt/oracle/mgmt_agent/agent_inst/config/emd.properties and add the required parameters into the additional properties section

|**Sample Environment**|Disk|CPU|Additional Configuration Parameters||Large log directories  <br>with > 10k files|
|---|---|---|---|---|---|
|Idle (no plugins)|1 GB|64MB|< 1%||#for large log volume on any size environment<br><br>loganalytics.enable_large_dir=true|
|Small (1-2 CDB with 1 PDB each)  <br>4 CPU|1 GB|256 MB|< 4%||
|Medium (12 CDBs, 40 PDBs)  <br>96 CPU|2 GB|1 GB|< 1%|#Sender properties<br><br>senderManagerMaxDiskUsedTotal=1000  <br>_senderManagerPoolSize=10<br><br># Connection pooling properties<br><br>clientConnectionPool.SERVICE_INVOKING.defaultMaxConnectionsPerRoute=50  <br>clientConnectionPool.SERVICE_INVOKING.maxTotalConnections=100|
|Large (22+ CDBs, 145+ PDBs)  <br>96 CPU|3 GB|2 GB|< 1.5%|#Sender properties<br><br>senderManagerMaxDiskUsedTotal=2000  <br>_senderManagerPoolSize=20<br><br># Connection pooling properties<br><br>clientConnectionPool.SERVICE_INVOKING.defaultMaxConnectionsPerRoute=50  <br>clientConnectionPool.SERVICE_INVOKING.maxTotalConnections=100|

For more details and important considerations when installing Management Agent on Exadata Cloud, see **OCI : Observability & Management Support For Exadata Cloud Doc ID 3015115.1** on My Oracle Support.

## Ingest Database Logs

In this section, we will look at the process of ingesting database logs as collected by the management agent into OCI Logging Analytics where we can analyze and visualize log data to gain deeper insights. For a Linux Database, we will look at the process of ingesting both file and table based logs and then move on to the Windows database to ingest the table based logs into Logging Analytics.

### For Linux Based Oracle Database: Ingesting File Based Logs

Create Database Entity in Logging Analytics:

In logging analytics, entities play a crucial role as the represt the sources of log data such as hosts, applications and services. Entities provide a way to categorize and correlate log events. By defining entities, we can create a logical model of our infrastructure, making it easier to identify trends, patters and anomalies in our log data.  
In order to create an Entity for your Linux database, navigate to **Observability & Management**. Under **Logging Analytics**, click **Administration**. Click **Entities** and Click **Create Entity**. Enter **Entity Type** as **Oracle Database Instance**. Enter desired name. Select **Compartment** where Management Agent resides and choose the corresponding management agent associated with the database.

![CE](/images/posts/2025-blogs/blog-oci_database_info_entity_association.png)

Figure 9: Entity Creation for Linux Database Instance

The next section while creating Database Entity is to provide details related to the destination of log files we intend to bring to Logging Analytics.

![Entity](/images/posts/2025-blogs/blog-oci_database_info_entity_association.png)

Figure 10: Property Value for File based Logs Ingestion

**Note:** To determine value such as _adr_home, oracle_home_ in the above step, login to the database and use the following command:

              _SQL> set line 200 pages 2000_

_SQL> select * from v$diag_info;_  
  
To determine values such as _audit_file_dest_ run the following command after logging in to the database:  
  
_SQL>show parameter audit_

Entity-Source Association:

In logging analytics, entity-source association is a critical step in unlocking the full potential of log data. By linking log sources to specific entities we can establish a clear connection between the log data and the systems or components that generated it. While on the Entity page, Click on the **Associated Sources**, **Add Association** and select the Entity Name. In the next page, select the Log Source to associate with the Entity. In this case, for file-based logs, **Database Audit Logs** of type **File** is the Log Source.

![entityselect](/images/posts/2025-blogs/blog-oci_database_info_entity_association.png)

Figure 11: Entity Selection while associating with Source

![LS](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 12: Log Source selection for file based Log Ingestion

Click on **Validate and configure log collection**. Click on **View in Log Explorer** to navigate to the log explorer and take a look at the logs.

### Enable reading large files

Additional configuration might be required for Management Agent to read and upload large files to Logging Analytics. To enable that, follow the steps below:

1.                  1. ssh into the database host and switch to root user by using the following command.  
                           _sudo -su root_
2.                     2. Switch to the config directory to locate the emd.properties file.  
                           _cd /opt/oracle/mgmt_agent/agent_inst/config/_
3.                    3. Edit emd.properties to add the following statement to all large files upload.  
                             _loganalytics.enable_large_dir=true_
4.                    4. Stop and start the management agent by running the following commands.  
                           _systemctl stop mgmt_agent_  
                          _systemctl start mgmt_agent_
5. ### For Linux Based Oracle Database: Ingesting Table Based Logs
    
6. Create Database Entity in Logging Analytics:
    
7. Creating an entity while ingesting table based logs is a similar process as an entity creation for ingesting file based logs. It differs in terms of property values. This database entity requires providing details such as oracle_home, port, service_name and sid.
    
8. ![CE](/images/posts/2025-blogs/blog-oci_database_info_entity_association.png)
    
    Figure 13: Entity Creation for Linux Database Instance
    
    
      
     
9. ![Entity details](/images/posts/2025-blogs/blog-oci_database_info_entity_association.png)
    
    Figure 14: Property Value for Table based Logs Ingestion
    
    
    **Note:** To determine value such as _adr_home, oracle_home_ in the above step, login to the database and use the following command:
    
10.            _SQL> set line 200 pages 2000_
    
11.           _SQL> select * from v$diag_info;_
    
12.           _SQL> select * from v$diag_info;_
    
13. Entity-Source Association:
    
    In this case, for table-based logs, **Oracle Unified DB Audit Log Source Stored in Database 12.2** of type **Database** is the Log Source.
    
14. ![EN_select](/images/posts/2025-blogs/blog-oci_database_info_entity_association.png)
    
    Figure 15: Entity Selection while associating with Source
    
    

![LG_T](/images/posts/2025-blogs/blog-oci_database_info_log_group_association.png)

Figure 16: Log Source selection for table based Log Ingestion

## For Windows Based Oracle Database

Create Database Entity in Logging Analytics:

In order to create an Entity for your Windows database, navigate to **Observability & Management**. Under **Logging Analytics**, click **Administration**. Click **Entities** and Click **Create Entity**. Enter **Entity Type** as **Host(Windows)**. Enter desired name. Select **Compartment** where Management Agent resides and choose the corresponding management agent associated with the database. The only property value required by this entity is the Event ID which is set to 34 specifying audit trail events for database.

![WE](/images/posts/2025-blogs/blog-oci_database_info_entity_association.png)

Figure 17: Entity Creation for Windows Database Instance

Note: Oracle Database for Windows problems and other significant occurences are recorded as events in an application log. Event number 34 specifies an audit trail event. These events are recorded if the parameter AUDIT_TRAIL is set to db(true) or os in the initialization parameter file.

Entity-Source Association:

In this case, for a windows database instance, **Windows Application Events** is the Log Source.

![Add_association](/images/posts/2025-blogs/blog-oci_db_backup_duration_logs_source_association.png)

Figure 18: Entity Selection while associating with Source

![Windows Log Source](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 19: Log Source selection for Windows Table based Log Ingestion

Click on **Validate and configure log collection**. Click on **View in Log Explorer** to navigate to the log explorer and take a look at the logs.

## Unlocking Hidden Insights from Ingested Database Logs

By collecting and analyzing database logs, organizations can gain a deeper understanding of their database activity, identify potential security threats, optimize performance, and make data-driven decisions. But, with the sheer volume and complexity of log data, it can be overwhelming to extract meaningful insights.  
That's where the Database Audit Analysis dashboard in Logging Analytics comes in.

### Database Audit at a Glance

In the first image below, you can see that the database audit dashboard showcases the following:

- **Monitored Databases**: Get a bird's-eye view of your database landscape, with a clear count of monitored databases and their respective status.
- **Audited Object Trends**: Dive into the heart of your database activity, with a detailed count and trend analysis of Oracle Database Audited Objects found in your database audit logs. This includes insights into which objects are being accessed, modified, or queried, helping you identify potential security risks and performance bottlenecks.
- **Most Active Users**: Identify the most active users across your databases, along with their access patterns and behavior. This critical information enables you to detect and respond to potential security threats, optimize user access, and improve overall database performance.

![AD1](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 20: Overview of Database Audit Activity

### Uncovering Hiddern Patterns

In the second image, Database Audit dashboard help you uncover hidden patterns and trends in your Oracle database auditable events such as

- **Identify Unique Clients**: Discover the unique clients and applications interacting with your database, providing valuable insights into database usage and access patterns.
- **DML Action Analysis**: Drill down into the specifics of DML (Data Manipulation Language) actions, such as INSERT, UPDATE, and DELETE operations, to identify potential data breaches, unauthorized changes, or performance bottlenecks.
- **Top 10 Administrative Actions**: Get a clear view of the top 10 administrative actions performed on your database, including GRANT, REVOKE, and ALTER operations, helping you identify potential security risks and areas for improvement.
- **DDL Actions by Database**: Get a detailed view of DDL (Data Definition Language) actions performed on your databases, including CREATE, ALTER, and DROP operations. This enables you to track changes to database schema, identify potential security risks, and optimize database performance.
- **Audit Events by Security Category**: Visualize audit events grouped by security categories, such as Authentication, Authorization, and Data Access. This provides a clear understanding of potential security threats, enabling you to identify and respond to anomalies, unauthorized access, and data breaches.

![Audit Dashboard 2](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 21: Distribution of Audit Actions, Monitored Objects and Clients

### Conclusion

In this blog series, we've covered various aspects of preparing your environment and setting up tools to monitor and audit your databases in Oracle Cloud Infrastructure (OCI). From pre-work and requirements gathering to downloading, installing, and configuring the Management Agent, followed by creating entities and log sources in OCI Logging Analytics, you've learned step-by-step how to set up the necessary components. By following these guides, you should now have the skills to successfully collect and analyze critical database logs, enabling you to monitor and audit your database with greater efficiency and accuracy.The ability to collect and analyze database logs is an essential aspect of database management and maintenance. With the proper setup and utilization of tools like the Management Agent and Logging Analytics in OCI, you can ensure that your database operations are well-monitored and audited, helping you identify and address potential issues, mitigate security risks, and ensure compliance with various regulations. 

### References

1. [Perform pre-requisites for deplying management agent](https://docs.oracle.com/en-us/iaas/management-agents/doc/perform-prerequisites-deploying-management-agents.html#GUID-C5C0C9E2-719D-4BB2-97E7-D7A402AAB5FF)
2. [Install Management Agents](https://docs.oracle.com/en-us/iaas/management-agents/doc/install-management-agent-chapter.html#OCIAG-GUID-92777625-6549-4D8E-A27D-C1C5583071CA)
3. [Allow Continuous Log Collection Using Management Agents](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/allow-continuous-log-collection-using-management-agents.html#LOGAN-GUID-AA23C2F5-6046-443C-A01B-A507E3B5BFB2)
4. [Set Up Continuous Log Collection From Your Hosts](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/set-continuous-log-collection-form-your-hosts.html#LOGAN-GUID-310D58A5-9F27-48C9-AE62-009BD094AB69)
5. [Set Up Database Instance Monitoring](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/set-database-instance-monitoring.html#LOGAN-GUID-8C3BB4F1-1930-4106-BA0C-79C92E5DD2C3)

## Acknowledgements

Amine Tarhini

​