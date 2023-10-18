---
title: "Use Oracle Management Agent to consolidate F5 logs in OCI Logging and Logging Analytics"
date: 2023-10-06
last_modified_at: 2023-10-06T16:20:02-05:00
categories:
  - Blog
tags:
  - Observerability and Monitoring
  - F5
  - Logging Analytics
  - Integration
---

### Introduction
F5 Big-IP is a multifaceted networking device that plays a crucial role in ensuring the availability, performance, security, and scalability of applications and services in modern IT environments. It serves as a critical component for organizations looking to deliver reliable and high-performing applications to their users while protecting them from security threats.

Oracle Cloud Infrastructure Logging and Logging Analytics is a cloud solution in Oracle Cloud Infrastructure that lets you index, enrich, aggregate, explore, search, analyze, correlate, visualize, and monitor all log data from your applications and system infrastructure. As the OCI central log repository for log analysis, we can ingest logs from OCI service logs and audit logs, custom and application logs generated from cloud and on-prem systems. 

In the sections that follow, we'll walk you through the process of configuring F5 Big-IP devices to send syslog data to OCI Logging, setting up log sources, ingesting load balancer logs, and leveraging Logging Analytics for advanced log analysis. Whether you're an IT administrator responsible for network operations or a security professional tasked with threat detection, this guide will equip you with the knowledge to harness the full potential of your F5 Big-IP logs within Oracle Cloud Infrastructure.

### Reference Architecture

![OCI F5 LA Integration Reference Architecture](/images/posts/2023-10/F5_LA_integration_reference_architecture.png){: .align-center}

### Overview of configuring Logging Analytics and OCI Logging for F5 appliance logs

#### Prerequisites

**Logging Analytics should be set up in your tenancy**

* [Logging Analytics](https://docs.oracle.com/en-us/iaas/logging-analytics/index.html)
* [Configure Your Logging Analytics Service](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/configure-your-service.html)
* [Prerequisite IAM Policies](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/prerequisite-iam-policies.html)
* [Enable Access to Logging Analytics and Its Resource](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/enable-access-logging-analytics-and-its-resources.html)

**Compute Instance for Syslog Server**

* [Create Oracle Linux compute instance in OCI](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/launchinginstance.htm)

**Network security configuration**

Note: We need to make sure we have egress traffic from F5 to syslog server port 514 and the Management Agent needs to be communicated with Oracle Service Network.

* [Security Lists](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/securitylists.htm)
* [Network Security Groups](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/networksecuritygroups.htm)
* [Service Gateway](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/servicegateway.htm)
* [Internet Gateway](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/managingIGs.htm#Internet_Gateway)

* [NAT Gateway](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/NATgateway.htm)

**F5 appliance and remote syslog server integration**

* Your system is running BIG-IP 11.x and later.
* The remote syslog server is accessible from your BIG-IP system on the default route domain (Domain 0) or management network, and conversely, your BIG-IP system is accessible from the remote syslog server.
* If you want to use a fully qualified domain name (FQDN) for the syslog servers, configuration of DNS servers is required.

Note: The remote servers to which syslog sends messages must reside on either the management network or route domain 0 of the BIG-IP system. If log messages must be sent to remote servers that reside outside of the management network or route domain 0, consider using remote high-speed logging. Refer to the Configuring Remote High-Speed Logging chapter of the BIG-IP LTM External Monitoring of BIG-IP Systems: Implementations manual.

#### Setup OCI Management Agent on the Syslog server

* Enable the Management plugin in Oracle Cloud Agent tag
  * OCI Navigation Menu -\> Compute -\> Instances -\> Select syslog_server instance
  * Click Oracle Cloud Agent tab
  * Click Enable plugin for Management Agent

* Verify the Management Agent is up and running from OCI and on the VM
  * See the Status of Management Agent plugin shows **Running**
  ![OCI syslog server Oracle Cloud Agent](/images/posts/2023-10/royce-blog-syslog-server-oracle-cloud-agent.png){: .align-center}
  * Log in syslog server host, verify the Management Agent logs
  * Management Agent plugin log location: /var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/agent_inst/log
  * Check log file mgmt_agent.log to see if any error related to Management Agent

* Enable Logging Analytics Plugin in Management Agent Cloud Service
  * OCI Navigation Menu -\> Observability & Management -\> Management Agent -\> Agents
  * Select a specific agent related to your syslog server
  * Verify the Agent availability and the corresponding metrics
  ![OCI syslog server management agent](/images/posts/2023-10/royce-blog-syslog-server-mgmt-agent-1.png){: .align-center}
  * Click **Deploy plug-ins**
  * ![OCI syslog server management agent plugins](/images/posts/2023-10/royce-blog-syslog-server-mgmt-agent-plugin.png){: .align-center}

Reference:
* [Enable Management Agent Plugin for Oracle Cloud Agent](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/manage-plugins.htm)
* [Management Agents deploy Logging Analytics plugins](https://docs.oracle.com/en-us/iaas/management-agents/doc/management-agents-administration-tasks.html)

#### Configure F5 log forwarding in F5 console

The Configuration utility provides a basic means of configuring the syslog configurations, such as defining the log levels. To configure extensive syslog-ng customizations, you must use the command line.

* Log in to the Configuration utility.
![OCI F5 Configuration Utility](/images/posts/2023-10/royce-blog-f5-configuration-utility.png){: .align-center}
* Go to System \> Logs \> Configuration \> Remote Logging.
![OCI F5 Configuration Utility System Logs](/images/posts/2023-10/royce-blog-f5-ui-system-logs.png){: .align-center}
* For Remote IP, enter the destination syslog server IP address, or FQDN. (DNS server configuration required)
* For Remote Port, enter the remote syslog server UDP port (default is 514).
* (Optional) For Local IP, enter the local IP address of the BIG-IP system.
* Note: For BIG-IP systems in a high availability (HA) configuration, the non-floating self IP address is recommended if using a Traffic Management Microkernel (TMM) based IP address.
![OCI F5 Remote Logging](/images/posts/2023-10/royce-blog-f5-remote-logging.png){: .align-center}
Note: 10.0.027 is syslog server IP whereas 10.0.0.33 is the F5 appliance IP
* Select Add.
* Select Update.
* For BIG-IP systems in a high availability (HA) configuration, perform a ConfigSync to synchronize the changes to the other devices in the device group.

#### Configure the F5 BIG-IP system to log to remote syslog server using TCP protocol

* Log in to F5 BIG-IP using tmsh using the following command
  ```
  # tmsh
  ```

* List current remote server configurations
  ```
  # list /sys syslog remote-servers
  sys syslog {
      remote-servers {
          remotesyslog2 {
              host 10.0.0.27
              local-ip 10.0.0.33
          }
      }
  }
  ```

* To forward the syslogs to remote syslog server using the TCP protocol
  ```
  # modify /sys syslog include "destination remote_server {tcp(\"10.0.0.27\" port (514));};filter f_alllogs {level (debug...emerg);};log {source(s_syslog_pipe);filter(f_alllogs);destination(remote_server);};"
  ```

* To save the configuration
  ```
  # save /sys config
  ```

Reference:
* [Configure the BIG-IP system to log to a remote syslog server](https://my.f5.com/manage/s/article/K13080)

#### Configure rsyslogd for syslog server to collect F5 logs

rsyslog is the log processor module available on Linux and Windows releases. While it started as a regular syslogd, rsyslog has evolved into a kind of swiss army knife of logging, being able to accept inputs from a wide variety of sources, transform them, and output to the results to diverse destinations.
* Log in syslog server host
* Edit /etc/rsyslog.conf to enable the TCP syslog reception
  ```
  # vi /etc/rsyslog.conf
  *********Uncomment following lines*********
  # Provides TCP syslog reception
  # for parameters see http://www.rsyslog.com/doc/imtcp.html
  module(load="imtcp") # needs to be done just once
  input(type="imtcp" port="514")
  *********Update the remote incoming logs location*********
  $template remote-incoming-logs, "/var/log/remote/%HOSTNAME%"
  *.* ?remote-incoming-logs
  ```
* Save the /etc/rsyslog.conf
* Restart rsyslogd and check the status
  ```
  # systemctl restart rsyslog
  # sudo systemctl status rsyslog
  ● rsyslog.service - System Logging Service
  Loaded: loaded (/usr/lib/systemd/system/rsyslog.service; enabled; vendor preset: enabled)
  Active: active (running) since Wed 2023-10-04 22:36:32 GMT; 1s ago
  Docs: man:rsyslogd(8)
  https://www.rsyslog.com/doc/
  Main PID: 11078 (rsyslogd)
  Tasks: 8 (limit: 99832)
  Memory: 1.4M
  CGroup: /system.slice/rsyslog.service
  └─11078 /usr/sbin/rsyslogd -n

  Oct 04 22:36:32 syslog-server systemd[1]: Starting System Logging Service...
  Oct 04 22:36:32 syslog-server rsyslogd[11078]: [origin software="rsyslogd" swVersion="8.2102.0-13.el8" x-pid="11078" x-info="https://www.rsyslog.com"] start
  Oct 04 22:36:32 syslog-server systemd[1]: Started System Logging Service.
  Oct 04 22:36:32 syslog-server rsyslogd[11078]: imjournal: journal files changed, reloading...  [v8.2102.0-13.el8 try https://www.rsyslog.com/e/0 ]
  ```

* Add port 514 to the firewall
  ```
  # firewall-cmd --permanent --add-port=514/tcp
  # firewall-cmd –reload
  # sudo firewall-cmd --list-all
  public (active)
    target: default
    icmp-block-inversion: no
    interfaces: ens3
    sources: 
    services: dhcpv6-client ssh
    ports: 514/tcp
    protocols: 
    forward: no
    masquerade: no
    forward-ports: 
    source-ports: 
    icmp-blocks: 
    rich rules:
  ```

#### Configure Logging Analytics Entity and Log Sources for F5 Syslog
* Create an Entity for F5 syslog
  * OCI Navigation Menu -\> Observability & Management -\> Logging Analytics -\> Administration
  * Click **Entities** from the Resources menu and select **Create Entity**
  * Use Host(Linux) as Entity Type
  * Pick the Management Agent Compartment and corresponding Management Agent
  ![OCI Logging Analytics Create Entity](/images/posts/2023-10/royce-blog-la-entity-creation.png){: .align-center}
* Create Log Source for F5 syslog
  * Click **Sources** from the Resource menu
  * Search F5 from the search box
  * Locate the F5 Big IP logs Log Source, click **Duplicate** in the action menu
  ![OCI Logging Analytics Duplicate Log Source](/images/posts/2023-10/royce-blog-la-log-source-duplicate.png){: .align-center}
* A new name for the new Log Source, for example, F5test Big IP Logs
  * Add Entity Types
  * Add Included Patterns for the file names and locations to be ingested
  ![OCI Logging Analytics F5 Log Source](/images/posts/2023-10/royce-blog-la-create-log-source.png){: .align-center}
* F5 Entity and Log Source association
  * In Logging Analytics Sources page, select **Unassociated Entities** from the Resources page
  * Select the Entity to be associated with the Log Source F5test Big IP Logs
  ![OCI Logging Analytics F5 Log Source](/images/posts/2023-10/royce-blog-la-f5test-big-ip-log-source.png){: .align-center}
* Click **Add association**
  * Select Logging Analytics Log Group or Create a new Log Group
  ![OCI Logging Analytics Log Source - Entity association](/images/posts/2023-10/royce-blog-la-f5-log-entity-association.png){: .align-center}
  * Click Submit
  * Monitor the Agent Collection Warning for any error messages
  * Monitor the syslog server Management Agent Logging Analytics plugin logs
  * Log file: /var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/agent_inst/log/ mgmt_agent_logan.log

#### (Optional) Configure OCI Unified Monitoring Agent on the syslog server to forward logs to the OCI Logging Service

Unified Monitoring Agent is fluentd-based open-source agent to ingest custom logs such as syslogs, application logs, security logs to Oracle Logging Service. With proper agent configuration, it allows you to control exactly which logs you want to collect, how to parse them, and more.

Note: The Unified Monitoring Agent is a fully managed agent, and custom client configuration is not officially supported. For example, gathering logs from remote sources is not recommended, since doing so can have serious security implications (because the log source cannot be verified).
* Create API key for the service account user
  * OCI user profile -\> My profile
  * In Resources menu, select **API keys**
  ![OCI user API Key](/images/posts/2023-10/royce-blog-la-user-api-key-1.png){: .align-center}
  * Add **API keys**
  * Select **Generate API key pair**
  * Click **Add**
  ![OCI create API Key](/images/posts/2023-10/royce-blog-la-user-api-key-2.png){: .align-center}
* Create OCI user principal on syslog server
  ```
  [root@syslog-server log]# cd /etc/unified-monitoring-agent/.oci
  [root@syslog-server .oci]# ls -l
  total 8
  -rw-------. 1 root root  351 Oct  5 03:40 config
  -rw-------. 1 root root 1730 Oct  5 00:41 oci_api_key.pem
  [root@syslog-server .oci]# cat config
  [DEFAULT]
  
  [UNIFIED_MONITORING_AGENT]
  user=ocid1.user.oc1..aaaaaaaae5pzkfjhqnpgim6int3psohxo6cjww4yj2cdgc46qne7oxg5fg6a
  fingerprint=18:fb:86:c9:04:51:3d:c3:08:93:09:c8:85:a8:10:bc
  tenancy=ocid1.tenancy.oc1..aaaaaaaaa3qmjxr43tjexx75r6gwk6vjw22ermohbw2vbxyhczksgjir7xdq
  region=eu-frankfurt-1
  key_file=/etc/unified-monitoring-agent/.oci/oci_api_key.pem
  [root@syslog-server .oci]# 
  ```
* Configure Unified Monitoring Agent
* Add configuration into /etc/unified-monitoring-agent/conf.d/fluentd_config/fluentd.conf
```
[root@syslog-server .oci]# cat /etc/unified-monitoring-agent/conf.d/fluentd_config/fluentd.conf
  <source>
    @type tail
    path /var/log/remote/f5test.oci-cloud.lab
    pos_file /var/log/td-agent/f5test.oci-cloud.lab.pos
    tag f5test_message
    <parse>
      @type none
    </parse>
  </source>
  <match f5test_message>
      @type oci_logging
      principal_override user
      log_object_id ocid1.log.oc1.eu-frankfurt-1.amaaaaaac3adhhqahafowmpmlzwfdfavnazgxhtzfg3iicnxsvx5i7cur6aa 
  </match>
```
* Restart the Unified Monitoring Agent
  ```
  # systemctl restart unified-monitoring-agent.service
  # systemctl status unified-monitoring-agent.service
  ● unified-monitoring-agent.service - unified-monitoring-agent: Fluentd based data collector for Oracle Cloud Infrastructure
    Loaded: loaded (/usr/lib/systemd/system/unified-monitoring-agent.service; enabled; vendor preset: disabled)
    Active: active (running) since Thu 2023-10-05 04:05:41 GMT; 11s ago
      Docs: https://docs.cloud.oracle.com/
    Process: 8450 ExecStop=/bin/kill -TERM ${MAINPID} (code=exited, status=0/SUCCESS)
  Main PID: 8459 (fluentd)
      Tasks: 1 (limit: 99832)
    Memory: 220.2M (limit: 5.0G)
    CGroup: /system.slice/unified-monitoring-agent.service
            └─8459 /opt/unified-monitoring-agent/embedded/bin/ruby /opt/unified-monitoring-agent/embedded/bin/fluentd --log /var/log/unified-monitoring-agent/unified-monitoring-agent.log --log-rotate-size 1048576 --log-rotate-age 10

  Oct 05 04:05:41 syslog-server systemd[1]: unified-monitoring-agent.service: Succeeded.
  Oct 05 04:05:41 syslog-server systemd[1]: Stopped unified-monitoring-agent: Fluentd based data collector for Oracle Cloud Infrastructure.
  Oct 05 04:05:41 syslog-server systemd[1]: Started unified-monitoring-agent: Fluentd based data collector for Oracle Cloud Infrastructure.
  ```
* Monitor the Unified Monitoring Agent log
  ```
  # tail -50f /var/log/unified-monitoring-agent/unified-monitoring-agent.log
  2023-10-05 04:15:33 +0000 [info]: gem 'fluent-plugin-oracle-telemetry-out-objectstorage' version '1.0.20230720045849'
  2023-10-05 04:15:33 +0000 [info]: gem 'fluent-plugin-oracle-telemetry-out-telemetry' version '1.0.20230720045849'
  2023-10-05 04:15:33 +0000 [info]: gem 'fluent-plugin-rewrite-tag-filter' version '2.4.0'
  2023-10-05 04:15:33 +0000 [info]: gem 'fluent-plugin-rewrite-tag-filter' version '2.3.0'
  2023-10-05 04:15:44 +0000 [info]: using user signer type with config dir /etc/unified-monitoring-agent/.oci/config
  2023-10-05 04:15:44 +0000 [warn]: If user principal is used, try getting domain from environment variable Or local map first
  2023-10-05 04:15:44 +0000 [info]: in non oci instance, region is eu-frankfurt-1,  hostname is syslog-server, realm is oraclecloud.com
  2023-10-05 04:15:44 +0000 [info]: using cert_bundle_path /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
  2023-10-05 04:15:44 +0000 [info]: using authentication principal user
  2023-10-05 04:15:44 +0000 [info]: Loading proxy settings
  2023-10-05 04:15:44 +0000 [info]: Proxy is not set in the config file. Run without proxy.
  2023-10-05 04:15:44 +0000 [info]: file DEFAULT_CONFIG_FILE, /etc/unified-monitoring-agent/.oci/config
  2023-10-05 04:15:44 +0000 [info]: Uma Source is not present in the config.
  2023-10-05 04:15:44 +0000 [info]: endpoint is https://ingestion.logging.eu-frankfurt-1.oci.oraclecloud.com in region eu-frankfurt-1
  2023-10-05 04:15:44 +0000 [info]: using configuration file: <ROOT>
    <source>
      @type tail
      path "/var/log/remote/f5test.oci-cloud.lab"
      pos_file "/var/log/td-agent/f5test.oci-cloud.lab.pos"
      tag "f5test_message"
      <parse>
        @type "none"
        unmatched_lines 
      </parse>
    </source>
    <match f5test_message>
      @type oci_logging
      principal_override "user"
      log_object_id "ocid1.log.oc1.eu-frankfurt-1.amaaaaaac3adhhqahafowmpmlzwfdfavnazgxhtzfg3iicnxsvx5i7cur6aa"
    </match>
  </ROOT>
  2023-10-05 04:15:44 +0000 [info]: starting fluentd-1.13.3 pid=8643 ruby="3.1.2"
  2023-10-05 04:15:44 +0000 [info]: spawn command to main:  cmdline=["/opt/unified-monitoring-agent/embedded/bin/ruby", "-Eascii-8bit:ascii-8bit", "/opt/unified-monitoring-agent/embedded/bin/fluentd", "--log", "/var/log/unified-monitoring-agent/unified-monitoring-agent.log", "--log-rotate-size", "1048576", "--log-rotate-age", "10", "--under-supervisor"]
  2023-10-05 04:15:45 +0000 [info]: adding match pattern="f5test_message" type="oci_logging"
  2023-10-05 04:15:57 +0000 [info]: #0 using user signer type with config dir /etc/unified-monitoring-agent/.oci/config
  2023-10-05 04:15:57 +0000 [warn]: #0 If user principal is used, try getting domain from environment variable Or local map first
  2023-10-05 04:15:57 +0000 [info]: #0 in non oci instance, region is eu-frankfurt-1,  hostname is syslog-server, realm is oraclecloud.com
  2023-10-05 04:15:57 +0000 [info]: #0 using cert_bundle_path /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
  2023-10-05 04:15:57 +0000 [info]: #0 using authentication principal user
  2023-10-05 04:15:57 +0000 [info]: #0 Loading proxy settings
  2023-10-05 04:15:57 +0000 [info]: #0 Proxy is not set in the config file. Run without proxy.
  2023-10-05 04:15:57 +0000 [info]: #0 file DEFAULT_CONFIG_FILE, /etc/unified-monitoring-agent/.oci/config
  2023-10-05 04:15:57 +0000 [info]: #0 Uma Source is not present in the config.
  2023-10-05 04:15:57 +0000 [info]: #0 endpoint is https://ingestion.logging.eu-frankfurt-1.oci.oraclecloud.com in region eu-frankfurt-1
  2023-10-05 04:15:57 +0000 [info]: adding source type="tail"
  2023-10-05 04:15:57 +0000 [info]: #0 starting fluentd worker pid=8653 ppid=8643 worker=0
  2023-10-05 04:15:57 +0000 [info]: #0 following tail of /var/log/remote/f5test.oci-cloud.lab
  2023-10-05 04:15:57 +0000 [info]: #0 fluentd worker is now running worker=0
  2023-10-05 04:16:57 +0000 [info]: #0 Payload size : 2434
  2023-10-05 04:16:57 +0000 [info]: #0 put_logs request with log_object_id ocid1.log.oc1.eu-frankfurt-1.amaaaaaac3adhhqahafowmpmlzwfdfavnazgxhtzfg3iicnxsvx5i7cur6aa
  2023-10-05 04:16:57 +0000 [info]: #0 log_batch_subject , hostname syslog-server, default_log_entry_time 2023-10-05T04:15:57.365Z, batch_size 17, batch_type com.oraclecloud.logging.custom.empty
  2023-10-05 04:16:57 +0000 [info]: #0 response 200 id: 885DD4322D044A9D86CB5DBCEFC82565/A88D1954F562BFACB21AFA052A197B4F/23B0EFCFBDCAECBDA8DFC4B7D3CEB223
  2023-10-05 04:18:03 +0000 [info]: #0 Payload size : 3099
  2023-10-05 04:18:03 +0000 [info]: #0 put_logs request with log_object_id ocid1.log.oc1.eu-frankfurt-1.amaaaaaac3adhhqahafowmpmlzwfdfavnazgxhtzfg3iicnxsvx5i7cur6aa
  2023-10-05 04:18:03 +0000 [info]: #0 log_batch_subject , hostname syslog-server, default_log_entry_time 2023-10-05T04:16:59.306Z, batch_size 19, batch_type com.oraclecloud.logging.custom.empty
  2023-10-05 04:18:03 +0000 [info]: #0 response 200 id: A6DEA3A81DF84FD7AACF5A7392F8EC7B/3769994277F0764905CBBC698EF3ECF6/68F8B1CCC7D3D57982544FB70B050309
  2023-10-05 04:19:52 +0000 [info]: #0 Payload size : 1186
  2023-10-05 04:19:52 +0000 [info]: #0 put_logs request with log_object_id ocid1.log.oc1.eu-frankfurt-1.amaaaaaac3adhhqahafowmpmlzwfdfavnazgxhtzfg3iicnxsvx5i7cur6aa
  2023-10-05 04:19:52 +0000 [info]: #0 log_batch_subject , hostname syslog-server, default_log_entry_time 2023-10-05T04:18:48.781Z, batch_size 6, batch_type com.oraclecloud.logging.custom.empty
  2023-10-05 04:19:52 +0000 [info]: #0 response 200 id: 2AF034DAE4694788B10E6228A2F62529/B3E52D234AC0D6BC6528C698E88703C2/431DAA69B1E8B6A4C547D997942B6788
  2023-10-05 04:21:03 +0000 [info]: #0 Payload size : 5493
  2023-10-05 04:21:03 +0000 [info]: #0 put_logs request with log_object_id ocid1.log.oc1.eu-frankfurt-1.amaaaaaac3adhhqahafowmpmlzwfdfavnazgxhtzfg3iicnxsvx5i7cur6aa
  2023-10-05 04:21:03 +0000 [info]: #0 log_batch_subject , hostname syslog-server, default_log_entry_time 2023-10-05T04:19:59.303Z, batch_size 40, batch_type com.oraclecloud.logging.custom.empty
  2023-10-05 04:21:03 +0000 [info]: #0 response 200 id: B127A25E6C904169A3D7E9F6101609A7/C0E54BC6C81419FDB1AF5E7826A44129/3CB03031927051A5F7947CE4D8CFD458
  2023-10-05 04:22:08 +0000 [info]: #0 Payload size : 1902
  2023-10-05 04:22:08 +0000 [info]: #0 put_logs request with log_object_id ocid1.log.oc1.eu-frankfurt-1.amaaaaaac3adhhqahafowmpmlzwfdfavnazgxhtzfg3iicnxsvx5i7cur6aa
  ```

### Conclusion

Oracle Logging Analytics allows you to collect and analyze syslog data from various sources. Like example above, F5 Big-IP devices can send syslog data to the syslog server and forward log data to Logging Analytics by setting up log sources, ingesting load balancer logs, and leveraging Logging Analytics for advanced log analysis. Whether you're an IT administrator responsible for network operations or a security professional tasked with threat detection, this blog will equip you with the knowledge to harness the full potential of your F5 Big-IP logs within Oracle Cloud Infrastructure.

### Reference
* [K13080: Configuring the BIG-IP system to log to a remote syslog server (11.x - 17.x)](https://my.f5.com/manage/s/article/K13080#tcpsyslog)
* [K46122561: Restrict access to the BIG-IP management interface using network firewall rules](https://my.f5.com/manage/s/article/K46122561)

