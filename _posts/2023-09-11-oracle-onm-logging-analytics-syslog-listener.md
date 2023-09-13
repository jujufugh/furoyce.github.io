---
title: "Use Oracle Management Agent to forward logs to Logging Analytics via syslog listener"
date: 2023-09-11
last_modified_at: 2023-09-11T16:20:02-05:00
categories:
  - Blog
tags:
  - Observerability and Monitoring
  - Management Agent
---

### Introduction
Oracle Cloud Logging Analytics is a cloud solution in Oracle Cloud Infrastructure that lets you index, enrich, aggregate, explore, search, analyze, correlate, visualize and monitor all log data from your applications and system infrastructure. 

As the OCI central log repository for log analysis, we can ingest logs from OCI service logs and audit logs, custom and application logs generated from cloud and on-prem systems. 

![OCI Logging Analytics Ingestion](/images/posts/2023-09/royce_blog_syslog_listener1.png){: .align-center}

### Logging Analytics Syslog Listener Configuration
Syslog is a commonly used standard for logging the system event messages. The destination of these messages can include the system console, files, remote syslog servers, or relays. In this blog, we will configure a central syslog server for log-consolidation and log-forwarding scenario. The syslog server is meant to gather log data from all the clients and then forward the log data to Logging Analytics using Oracle Management Agent.

#### Create a compute instance for syslog server and install Oracle Management Agent
Please refer to Oracle Management Agent [blog post](https://roycefu.com/blog/oracle-onm-deep-dive-mgmt-agent-cloud-agent/) for more details.

#### Create user-defined syslog listener log source in Logging Analytics
* OCI console navigation menu and click **Observability & Management**. Under **Logging Analytics**, click **Administration**. The **Administration** Overview page opens
* Click **Sources** on the left hand navigation menu. Click **Create Source**
* Provide details of the Log Source and select **Syslog Listener** as **Source Type**
* Select corresponding **Entity Type** for your use case, we will use **Host (Linux)** as our entity type because we use Oracle Linux as our syslog server OS
* Select proper **Parser** for your logs, for example **Syslog Standard Format** or **Syslog RFC5424 Format**
* Add **Listener Port** and **Listener Protocol(TCP/UDP)** so the Management Agent can listen the port and forward log data to Logging Analytics

![OCI Logging Analytics syslog listener log source](/images/posts/2023-09/royce_blog_syslog_listener2.png){: .align-center}

#### Create the syslog server entity in Logging Analytics
* OCI console navigation menu and click **Observability & Management**. Under **Logging Analytics**, click **Administration**. The **Administration** Overview page opens
* Click **Entities** on the left hand navigation menu. Click **Create Entity** or **Discover New Resource**
* Provide details of the Entity
* Select corresponding **Entity Type** for your use case, we will use **Host (Linux)** as our entity type because we use Oracle Linux as our syslog server OS
* Select corresponding **Management Agent** that we installed on the syslog server
* (Optional) Add Properties if any subsitution variable is required

![OCI Logging Analytics syslog server entity](/images/posts/2023-09/royce_blog_syslog_listener3.png){: .align-center}

#### Associate the syslog server entity with the syslog server log source
* Click **Sources** on the left hand navigation menu.
* Click **Unassociated Entities**, select the syslog-server from the list and click **Add association**
* Review the **Associated Entities** status, it will show **Success** once it's successfully associated
* Once association is completed, you should see the new configuration from `/opt/oracle/mgmt_agent/agent_inst/log/mgmt_agent_logan.log`
```
2023-09-11 16:13:34,342 [Work.P1.0 (PrioritizedWorkBundle-upsertSources) (PrioritizedWork-upsertSources)-281] INFO  - new logcollector instance
2023-09-11 16:13:34,344 [Work.P1.0 (PrioritizedWorkBundle-upsertSources) (PrioritizedWork-upsertSources)-281] INFO  - init logcollector
2023-09-11 16:13:34,344 [Work.P1.0 (PrioritizedWorkBundle-upsertSources) (PrioritizedWork-upsertSources)-281] INFO  - handle log item, sourceId = lacollector.la_syslog, name = la_syslog
2023-09-11 16:13:34,344 [Work.P1.0 (PrioritizedWorkBundle-upsertSources) (PrioritizedWork-upsertSources)-281] INFO  - create sub dir for each source type.
2023-09-11 16:13:34,362 [Work.P1.0 (PrioritizedWorkBundle-upsertSources) (PrioritizedWork-upsertSources)-281] INFO  - [vn=V7] [cv=-2373539744938722878] [agentID=ocid1.managementagent.oc1.iad.amaxxxxxxxxxxxxxxxxxxxxxxxxxx7l2wa] [agentNameSpace=orasenatdpltsecitom02]
2023-09-11 16:13:34,375 [Work.P1.0 (PrioritizedWorkBundle-upsertSources) (PrioritizedWork-upsertSources)-281] INFO  - Add TCP Listen successfully: 8008
2023-09-11 16:13:34,375 [Work.P1.0 (PrioritizedWorkBundle-upsertSources) (PrioritizedWork-upsertSources)-281] INFO  - logcollector is ready to run
2023-09-11 16:13:34,380 [Work.P1.0 (PrioritizedWorkBundle-upsertSources) (PrioritizedWork-upsertSources)-281] INFO  - save config file for source type: syslog
```

### rsyslog configuration
rsyslog is the log processor module available on Linux and Windows releases. While it started as a regular syslogd, rsyslog has evolved into a kind of swiss army knife of logging, being able to accept inputs from a wide variety of sources, transform them, and output to the results to diverse destinations.

#### Verify the rsyslog installed on the host
```
# rpm -qa | grep rsyslog
rsyslog-gnutls-8.2102.0-10.el8.x86_64
rsyslog-8.2102.0-10.el8.x86_64
rsyslog-relp-8.2102.0-10.el8.x86_64
rsyslog-gssapi-8.2102.0-10.el8.x86_64

# rsyslogd -version
rsyslogd  8.2102.0-10.el8 (aka 2021.02) compiled with:
	PLATFORM:				x86_64-redhat-linux-gnu
	PLATFORM (lsb_release -d):		
	FEATURE_REGEXP:				Yes
	GSSAPI Kerberos 5 support:		Yes
	FEATURE_DEBUG (debug build, slow code):	No
	32bit Atomic operations supported:	Yes
	64bit Atomic operations supported:	Yes
	memory allocator:			system default
	Runtime Instrumentation (slow code):	No
	uuid support:				Yes
	systemd support:			Yes
	Config file:				/etc/rsyslog.conf
	PID file:				/var/run/rsyslogd.pid
	Number of Bits in RainerScript integers: 64

See https://www.rsyslog.com for more information.
```

#### Check the rsyslog process is running
```
# systemctl status rsyslog.service
 rsyslog.service - System Logging Service
   Loaded: loaded (/usr/lib/systemd/system/rsyslog.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2023-09-11 18:24:57 GMT; 1 day 1h ago
     Docs: man:rsyslogd(8)
           https://www.rsyslog.com/doc/
 Main PID: 3516314 (rsyslogd)
    Tasks: 3 (limit: 99983)
   Memory: 5.0M
   CGroup: /system.slice/rsyslog.service
           └─3516314 /usr/sbin/rsyslogd -n

Sep 11 18:24:57 webinst01 systemd[1]: rsyslog.service: Succeeded.
Sep 11 18:24:57 webinst01 systemd[1]: Stopped System Logging Service.
Sep 11 18:24:57 webinst01 systemd[1]: Starting System Logging Service...
Sep 11 18:24:57 webinst01 systemd[1]: Started System Logging Service.
Sep 11 18:24:57 webinst01 rsyslogd[3516314]: [origin software="rsyslogd" swVersion="8.2102.0-10.el8" x-pid="3516314" x-info="https://www.rsyslog.com"] start
Sep 11 18:24:57 webinst01 rsyslogd[3516314]: imjournal: journal files changed, reloading...  [v8.2102.0-10.el8 try https://www.rsyslog.com/e/0 ]
```

#### Update the rsyslog.conf configuration file 
Edit file `/etc/rsyslog.conf` and add the following lines to the end of the config file
```
# ### sample forwarding rule ###
#action(type="omfwd"  
# An on-disk queue is created for this action. If the remote host is
# down, messages are spooled to disk and sent when it is up again.
#queue.filename="fwdRule1"       # unique name prefix for spool files
#queue.maxdiskspace="1g"         # 1gb space limit (use as much as possible)
#queue.saveonshutdown="on"       # save messages to disk on shutdown
#queue.type="LinkedList"         # run asynchronously
#action.resumeRetryCount="-1"    # infinite retries if host is down
# Remote Logging (we use TCP for reliable delivery)
# remote_host is: name/ip, e.g. 192.168.0.1, port optional e.g. 10514
#Target="remote_host" Port="XXX" Protocol="tcp")

*.* action(type="omfwd" target="192.168.0.18" port="8008" protocol="tcp")

```

#### Restart the rsyslog process to reload the new configuration file
```
# systemctl restart rsyslog.service
```

#### Check the log about the rsyslog process
```
# grep rsyslog /var/log/messages
Sep 10 03:38:02 webinst01 rsyslogd[2190]: [origin software="rsyslogd" swVersion="8.2102.0-10.el8" x-pid="2190" x-info="https://www.rsyslog.com"] rsyslogd was HUPed
Sep 11 00:06:30 webinst01 rsyslogd[2190]: imjournal: journal files changed, reloading...  [v8.2102.0-10.el8 try https://www.rsyslog.com/e/0 ]
Sep 11 18:24:57 webinst01 rsyslogd[2190]: [origin software="rsyslogd" swVersion="8.2102.0-10.el8" x-pid="2190" x-info="https://www.rsyslog.com"] exiting on signal 15.
Sep 11 18:24:57 webinst01 systemd[1]: rsyslog.service: Succeeded.
Sep 11 18:24:57 webinst01 rsyslogd[3516314]: [origin software="rsyslogd" swVersion="8.2102.0-10.el8" x-pid="3516314" x-info="https://www.rsyslog.com"] start
Sep 11 18:24:57 webinst01 rsyslogd[3516314]: imjournal: journal files changed, reloading...  [v8.2102.0-10.el8 try https://www.rsyslog.com/e/0 ]
```

#### Syslog Listener Testing on syslog server: send message to syslog server listener port via ncat
```
# ncat -c "echo 'RSYSLOG Test Message'" localhost 8008
```

#### rsyslog testing on client server: Create a log entry in client server and check the syslog server
```
# logger -t "Royce Log Message 1" "This is my test log message"
# logger -t "Royce Log Message 2" "This is my test log message"
# logger -t "Royce Log Message 3" "This is my test log message"
```

You should see the log entries are forwarded by Syslog Listener to Logging Analytics
```
2023-09-13 03:12:28,434 [LOG.Executor.6330 (LA_TASK_os_file)-30058] INFO  - LogCollector run started.
2023-09-13 03:12:28,438 [LOG.Executor.6330 (LA_TASK_os_file)-30058] INFO  - LS collection_guid: a7bd2886-5fc5-4ff0-a064-eb3ef0f0aae3, log_set: null, log group: ocid1.loganalyticsloggroup.oc1.iad.amaaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx2oda, entity_name: /var/log/messages, tz: GMT, data_size: 199, burstyStart: 1694574721000, burstyEnd: 1694574736000, entry_count: 3
2023-09-13 03:12:28,438 [LOG.Executor.6330 (LA_TASK_os_file)-30058] INFO  - send data bundle, sourceId = lacollector.la_os_file
2023-09-13 03:12:28,948 [LOG.Executor.6330 (LA_TASK_os_file)-30058] INFO  - LogCollector run ended.
2023-09-13 03:12:39,723 [LOG.Executor.34 (LA_TASK_syslog)-282] INFO  - The channel is closed on port 8008 from 0:0:0:0:0:0:0:1:48438
```

*Note: If the Management Agent is down on Syslog server, the log data streaming to the Syslog listener port might be lost*

#### Visualize Syslog Data using Logging Analytics Log Explorer
Logging Analytics displays the syslog data from all the configured listener ports. You can analyze syslog data from different hosts or devices. For example, you can search RSYSLOG keyword in the command line prompt. 

![Visualize syslog data in OCI Logging Analytics](/images/posts/2023-09/royce_blog_syslog_listener4.png){: .align-center}

#### Other Custom Logs Collection based on Source Types
Based on your log source type, we can collect logs and ingest logs using the following types:
* **File**
  * For collecting most types of logs, such as Application, and Infrastructure logs.
  * [Ingest Application, Infrastructure, Database and other Generic Logs](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/ingest-application-infrastructure-database-and-other-generic-logs.html#GUID-A7635D4D-830A-43A2-A687-120A2C8D3BBD)
* **Database**
  * Collect logs stored in tables and views of a database like Oracle Database Instance, Oracle Pluggable Database, Oracle Autonomous Database, Microsoft SQL Server Database Instance, and MySQL Database Instance.
  * [Set Up Database Instance Monitoring](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/set-database-instance-monitoring.html#GUID-8C3BB4F1-1930-4106-BA0C-79C92E5DD2C3)
* **REST API**
  * Collect logs periodically through REST API calls.
  * [Set Up REST API Log Collection](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/set-rest-api-log-collection.html#GUID-D0FFEA92-A264-4F2C-AEAB-324B85FC64A0)
* **Windows Event Messages**
  * All historic Windows Event Log entries as well as custom event channels.
  * [Set Up Windows Event Monitoring](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/set-windows-event-monitoring.html#GUID-10129DF6-C54E-4F09-B7AE-56990C465F3F)
* **Oracle Diagnostic Logs (ODL)**
  * These are typically the diagnostic logs for Oracle Fusion Middleware and Oracle Applications.
  * [Ingest Logs of Oracle Diagnostic Logging(ODL) format](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/ingest-logs-oracle-diagnostic-logging-odl-format.html#GUID-E668E3F3-8031-4C49-9390-87B63E2DBEC8)

### Conclusion
Oracle Logging Analytics allows you to collect and analyze syslog data from various sources. You just need to configure the syslog output ports in the syslog servers. Oracle Logging Analytics monitors those output ports, accesses the remote syslog contents, and performs the analysis. Syslog monitoring in Oracle Logging Analytics lets you listen to multiple hosts and ports. The protocols supported are TCP and UDP.

### Reference
* [rsyslog: Sending Messages to a Remote Syslog Server](https://www.rsyslog.com/sending-messages-to-a-remote-syslog-server/)
* [rsyslog: Receiving Messages to a Remote Syslog Server](https://www.rsyslog.com/receiving-messages-from-a-remote-system/)
* [Logging Analytics Ingest Logs](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/ingest-logs.html)
* [Ingest Logs to OCI Logging Analytics Using FluentD](https://docs.oracle.com/en/learn/oci_logging_analytics_fluentd/)
* [Harvest Entity Model Data from Enterprise Manager Cloud Control and Collect Logs](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/harvest-entity-model-data-enterprise-manager-cloud-control-and-collect-logs.html#GUID-ED8AFD29-FDDB-427A-B6F0-7AD55B282635)
* [Ingest Custom Logs from OCI Streaming Service Using Service Connector](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/ingest-custom-logs-oci-streaming-service-using-service-connector.html#GUID-494F9C06-AE2B-4841-A56F-E356BA67311E)
* [Ingest Custom Logs from OCI Logging Service Using Service Connector](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/ingest-custom-logs-oci-logging-service-using-service-connector.html#GUID-F6E9F2F7-D8DE-4874-A981-27AC1B312512)
* [Ingest Custom Logs from OCI Logging Service Using Service Connector](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/ingest-custom-logs-oci-logging-service-using-service-connector.html#GUID-F6E9F2F7-D8DE-4874-A981-27AC1B312512)
* [Ingest Logs from Other OCI Services Using Service Connector](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/ingest-logs-other-oci-services-using-service-connector.html#GUID-09B91C93-30C2-454E-87AF-FA8C39207FB4)
* [Collect Logs from Your OCI Object Storage Bucket](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/collect-logs-your-oci-object-storage-bucket.html#GUID-FE409E6D-BBEA-47CB-8744-F82B7687C23B)
* [Upload Logs on Demand](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/upload-logs-demand.html#GUID-B1B33F86-B3B6-4933-939D-E85F090F4648)
* OCI: File Size Limit To Uploaded To Logging Analytics (Doc ID 2946101.1)

