---
title: "A Technical Comparison among OCI Logging and Monitoring Agent Types - Oracle Cloud Agent, Management Agent and Unified Monitoring Agent"
date: 2023-08-17
last_modified_at: 2023-08-17T16:20:02-05:00
categories:
  - Blog
tags:
  - Observerability and Monitoring
  - Management Agent
  - Oracle Cloud Agent
  - Unified Monitoring Agent
---

### Introduction
In the ever-evolving landscape of cloud computing, the ability to efficiently log, monitor and manage resources has become a cornerstone of operational success. At the heart of this intricate ecosystem are OCI agents such as Oracle Cloud Agent, Oracle Management Agent, and Unified Monitoring Agent emerge as crucial players in ensuring observability and management is seamless and tightly integrated with OCI cloud resources.

#### OCI Observability & Management Reference Architecture
<img src='/images/posts/2023-08/royce-blog-onm_reference_architecture_review.color.png'/>

### OCI Agents Overview
Oracle Cloud Infrastructure agents come in various forms, each designed with a specific set of capabilities to address different use cases. However, while these agents offer powerful functionalities, navigating the landscape and choosing the right agent for your unique requirements can sometimes be a daunting task. This overview aims to shed light on the types of OCI agents available, their key features, and how to approach selecting the most suitable agent for your use cases.

*Note: All the configuration details will be Linux OS version based.*

#### OCI Agents Comparison

| Categories	| Oracle Cloud Agent	| Oracle Management Agent	| Oracle Unified Monitoring Agent | 
|-------------|---------------------|-------------------------|---------------------------------|
| Monitoring	| via Compute Instance Monitoring Plugin	| N/A	| N/A |
| Logging	| via Unified Monitoring Agent Plugin	| N/A	| Integration with Loggin Service via User Principal |
| Logging Analytics	| via Management Agent Plugin	| via Logging Analytics Plugin	| N/A |
| Stack Monitoring	| via Management Agent Plugin	| via Stack Monitoring Plugin	| N/A |
| Database Management	| via Management Agent Plugin	| via Database Management Plugin	| N/A |
| Operations Insights	| via Management Agent Plugin	| via Operations Insights Plugin	| N/A |
| Java Usage Tracking	| via Management Agent Plugin	| via Java Usage Tracking Plugin	| N/A |
| Java Management Service	| via Java Management Service Plugin |	via Java Management Service Plugin	| N/A |
| OS Management Hub	| via OS Management Service Plugin |	via OS Management Hub Plugin	| N/A |
| Agent Installation	| Preinstalled for OCI compute, manual installation(zip, rpm) |	Manual installation(zip, rpm)	| Manual installation(zip, rpm) |
| Authentication/Authorization	| Resource Principal, Instance Principal | Resource Principal, Instance Principal	| User Principal |
| Agent Management	| Fully Integrated	| Fully Integrated	| Partially Integrated, no UI |
| Compute Instance Support	| Yes	| Yes	| Yes |
| Oracle Base Database Service Support	| No	| Yes	| Yes* |
| Oracle Exadata Database Service Dedicated Support	| No	| Yes	| Yes* |

#### **Oracle Cloud Agent** 
* **Oracle Cloud Agent** is a lightweight process that manages plugins running on compute instances. Oracle Cloud Agent plugins collect host logs, performance metrics, install OS updates, and perform other instance management tasks. Oracle Cloud Agent is installed by default for OCI compute instances.
* **Oracle Cloud Agent supports the [Platform Images](https://docs.oracle.com/en-us/iaas/Content/Compute/References/images.htm#OracleProvided_Images)**
For unsupported OS version, **Oracle Management Agent** and **Unified Monitoring Agent** can be used for collecting log and cloud resource data for OCI Observability and Management services. 
* Oracle Cloud Agent manages the following plugins for the OCI Observability and Management, it is considered as the best practice to use Oracle Cloud Agent whenever it is possible.

<img src='/images/posts/2023-08/royce-blog-oracle-agents-oracle_cloud_agent_architecture.png'/>


  | Plugin Name | Description | Reference  |
  |-------------|-------------|------------|
  | Bastion | Allows secure shell (SSH) connections to an instance without public IP addresses using the Bastion service | [Bastion](https://docs.oracle.com/iaas/Content/Bastion/Concepts/bastionoverview.htm) |
  | Block Volume Management | Configures Block Volume sessions for the instance | [Enable the Block Volume Management Plugin](https://docs.oracle.com/en-us/iaas/Content/Block/Tasks/enablingblockvolumemanagementplugin.htm#enablingblockvolumemanagementplugin) |
  | Compute Instance Monitoring | Emits metrics about the instance's health, capacity, and performance. These metrics are consumed by the Monitoring service | [Enable Monitoring for Compute Instance](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/enablingmonitoring.htm#Enabling_Monitoring_for_Compute_Instances) |
  | Compute Instance Run Command | Runs scripts within the instance to remotely configure, manage, and troubleshoot the instance | [Run commands on compute instance](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/runningcommands.htm#runningcommands) |
  | Custom Logs Monitoring | Fluend-based open source Unified Monitoring Agent, Ingests custom logs into the Logging service | [Unified Monitoring Agent](https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/agent_management.htm) |
  | Management Agent | Oracle Management Agent is a service that provides low latency interactive communication and data collection between Oracle Cloud Infrastructure and any other targets | [Oracle Management Agent Plugin](https://docs.oracle.com/en-us/iaas/management-agents/doc/management-agents-oracle-cloud-agent.html) |
  | Oracle Autonomous Linux | Manages autonomous updates and collects data associated with events, including logs and stack traces, for instances managed by the Autonomous Linux service | [Oracle Autonomous Linux](https://docs.oracle.com/iaas/os-management/osms/alx-index.htm) |
  | Oracle Java Management Service | Monitors and performs Java Development Kit (JDK) lifecycle management for Java deployments on instances managed by the Java Management service | [Java Management](https://docs.oracle.com/iaas/jms/index.html) |
  | OS Management Service Agent | Manages updates and patches for the operating system environment on the instance | [OS Management](https://docs.oracle.com/iaas/os-management/osms/index.htm) |
  | Vulnerability Scanning | 	Scans the instance for potential security vulnerabilities like OS packages that require updates | [Scanning Overview](https://docs.oracle.com/iaas/scanning/using/overview.htm) |

##### Oracle Cloud Agent Installation and Configuration

*Note: When we can't install Oracle Cloud Agent in the VM, the workaround is to use Oracle Management Agent or Oracle Unified Monitoring Agent to collect and ingest logs for Logging Analytics Service or Logging Service. *
* Policy to read instance agent plugins
```
Allow group PluginUsers to read instance-agent-plugins in compartment ABC
```
* Check if Oracle Cloud Agent software is installed
```
sudo yum info oracle-cloud-agent
```
* Install Oracle Cloud Agent
```
sudo yum install -y oracle-cloud-agent
```
* Restart Oracle Cloud Agent
```
sudo systemctl restart oracle-cloud-agent
```
* Validate the Oracle Cloud Agent installation
```
rpm -q oracle-cloud-agent && echo "OCA Installed" || echo "OCA not Installed"
```
* Verify the Oracle Cloud Agent is running
```
systemctl is-enabled oracle-cloud-agent &>/dev/null && echo "OCA is enabled" || echo "OCA is disabled" && systemctl is-active oracle-cloud-agent &> /dev/null && echo "OCA is running" || echo "OCA is not running"
```
* Verify that the instance can access the instance metadata service endpoint
```
curl -v -H 'Authorization: Bearer Oracle' http://169.254.169.254/opc/v2/instance/
```
* Check Clock Skew errors which can potentially cause TLS negotiations to fail and prevent instance connecting to Oracle services
```
sudo tail -15 /var/log/oracle-cloud-agent/plugins/gomon/monitoring.log
```
* When you work with support engineer to troubleshoot issues with the Oracle Cloud Agent, you can generate diagnostic data for your agent, the tool will generate a TAR file with a name in the format `oca-diag-<date>.<identifier>.tar.gz`
```
cd /usr/bin/ocatools
sudo ./diagnostic
```
* In any senario, you need to configure proxy for your Oracle Cloud Agent
```
sudo EDITOR=vi systemctl edit oracle-cloud-agent
## Add following entries into the editor window
[Service]
Environment="http_proxy=<proxy_url>:<proxy_port>"
Environment="https_proxy=<proxy_url>:<proxy_port>"
Environment="no_proxy=localhost,127.0.0.1,169.254.169.254"

sudo EDITOR=vi systemctl edit oracle-cloud-agent-updater
## Add following entries into the editor window
[Service]
Environment="http_proxy=<proxy_url>:<proxy_port>"
Environment="https_proxy=<proxy_url>:<proxy_port>"
Environment="no_proxy=localhost,127.0.0.1,169.254.169.254"

# Restart the agent
sudo systemctl daemon-reload
sudo systemctl restart oracle-cloud-agent oracle-cloud-agent-updater
```

#### **Oracle Management Agent**
* **Oracle Management Agent** is a service that provides low latency interactive communication and data collection between Oracle Cloud Infrastructure and IT targets. Oracle Management Agent has plugins integrated with O&M advanced services such as Logging Analytics, Database Management, Operations Insights, Java Management Service, Stack Monitoring, etc. Plugins can collect and ingest data from various cloud resources. Management Agent can be enabled as a plugin of the Oracle Cloud Agent or can install independently. 

<img src='/images/posts/2023-08/royce-blog-oracle-agents-oracle-management-agent-plugins.png'/>

* Supported OS versions
  * Windows-x86_64, Windows-x86
  * Solaris-Sparc64
  * Linux-x86_64, Linux-Aarch64

##### Oracle Management Agent Installation and Configuration

* Prerequisites, [doc reference](https://docs.oracle.com/en-us/iaas/management-agents/doc/perform-prerequisites-deploying-management-agents.html)
  * Ceate or designate compartments for Oracle Management Agent
  * Create a user group to manage Oracle Management Agent
  * Create policies for user group
* Oracle Management Agent download can be done via Management Agent Cloud Service UI or via CLI
* Obtain the object-url value using cli command
```
oci management-agent agent-image list --compartment-id <tenancyId>
```
* The return object-url value is similar to the following
```
https://objectstorage.<region_identifier>.oraclecloud.com/n/<namespace>/b/<bucketName>/o/Linux-x86_64/latest/oracle.mgmt_agent.rpm
```
* Download the Management Agent software with OCI authenticated pricing using 
```
oci os object get --namespace <namespace> --bucket-name <bucketName> --name Linux-x86_64/latest/oracle.mgmt_agent.rpm --file oracle.mgmt_agent.rpm
```
* Run rpm installation
```
$ sudo rpm -ivh oracle.mgmt_agent.rpm
```
* Fix the permission issue
```
chmod a+x /home; sudo chmod a+x /home/opc
```
* Modify the install key for the response file
  * Fill AgentDisplayName field
  * Enable APM and Stack Monitoring : Service.plugin.appmgmt.download=true
  * Enable Logging Analytics : Service.plugin.logan.download=true
  * Enable Database Management : Service.plugin.dbaas.download=true
  * Example:
```
########################################################################
    ########################################################################
    ManagementAgentInstallKey = <install_key_place_holder>
    AgentDisplayName = emdbhost1-mgmt-agent
    #Please uncomment the below tags properties and provide values as needed
    #FreeFormTags = [{"<key1>":"<value1>"}, {"<key2>":"<value2>"}]
    #DefinedTags = [{"namespace1":{"<key1>":"<value1>"}}, {"namespace2":{"<key2>":"<value2>"}}]
    #CredentialWalletPassword = 
    Service.plugin.appmgmt.download=true
    #Service.plugin.jms.download=true
    Service.plugin.dbaas.download=true
    Service.plugin.logan.download=true
    Service.plugin.opsiHost.download=true
    #Service.plugin.jm.download=true
```
* Run the Agent configuration
```
$ sudo /opt/oracle/mgmt_agent/agent_inst/bin/setup.sh opts=/home/opc/input.rsp
```
* Enable additional Plugins, you might see different plugin views when you enable/deploy Oracle Management Agent differently
  * Install Oracle Management Agent independently 
    <img src='/images/posts/2023-08/royce-blog-oracle-agents-plugins_view01.png'/>
  * Enable Management Agent as a Plugin of Oracle Cloud Agent
    <img src='/images/posts/2023-08/royce-blog-oracle-agents-plugins_view02.png'/>
* Generate Management Agent diagnostic support bundle
* If Management Agent is enabled on compute instance via Oracle Cloud Agent
```
sudo -u oracle-cloud-agent /var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/agent_inst/bin/generateDiagnosticBundle.sh
```
* If Management Agent is deployed as standalone installation
```
# sudo -u mgmt_agent /opt/oracle/mgmt_agent/agent_inst/bin/generateDiagnosticBundle.sh
``` 
  
#### **Unified Monitoring Agent** 
* **Unified Monitoring Agent** is [fluentd-based](https://www.fluentd.org/) open-source agent to ingest custom logs such as syslogs, application logs, security logs to Oracle Logging Service. With proper agent configuration, it allows you to control exactly which logs you want to collect, how to parse them, and more.
* Note: The Unified Monitoring Agent is a fully managed agent, and custom client configuration is not officially supported. For example, gathering logs from remote sources is not recommended, since doing so can have serious security implications (because the log source cannot be verified).
* Unified Monitoring Agent supports following OS versions:
  * Oracle Linux 7, Oracle Linux 8
  * CentOS 7, CentOS Stream 8
  * Windows Server 2012 R2, Windows Server 2016, Windows Server 2019
  * Ubuntu 16.04, Ubuntu 18.04, Ubuntu 20.04
#### Oracle Unified Monitoring Agent Installation and Configuration
* Login server
* Download the downloadAgent.sh script [here](https://objectstorage.us-phoenix-1.oraclecloud.com/n/axmjwnk4dzjv/b/upload-agent-script/o/downloadAgent.sh)
* Run the script, use Oracle Linux as an example: 
```
./downloadAgent.sh oel8
```
* Configure User Principals to communiate with OCI native services ([Further reading about User Principals](https://database-heartbeat.com/2021/10/05/auth-cli/))
* Validate the agent - Linux 
```
systemctl status unified-monitoring-agent
```
* Create an Agent Configuration via CLI 
```
oci logging agent-configuration create compartment-id compartment_ocid --is-enabled [true|false] --service-configuration service_configuration [OPTIONS]
```
* List Agents Configurations via CLI 
```
oci logging agent-configuration list --compartment-id compartment_ocid [OPTIONS]
```
* Get Agent Configuration's Details via CLI 
```
oci logging agent-configuration get --config-id config_ocid [OPTIONS]
```
* Edit Agent Configuration 
```
oci logging agent-configuration update --config-id config_ocid --display-name display_name --is-enabled is-enabled [true|false] --service-configuration service_configuration [OPTIONS]
```
* Delete Agent Configuration 
```
oci logging agent-configuration delete --config-id config_ocid [OPTIONS]
```
* Create a Log Configuration for an Agent Configuration 
```
oci logging agent-configuration create-log-configuration --compartment-id compartment_ocid --is-enabled [true|false] [OPTIONS]
```
* Edit a Log Configuration for an Agent Configuration 
```
oci logging agent-configuration update-log-configuration --config-id config_ocid --display-name display_name --is-enabled [true|false] [OPTIONS]
```
* Permissions to read logs from the host
* Determine the agent OS user validate from the /etc/passwd on the server
  *Note: On Unix-based hosts, the user that installs management agent is mgmt_agent for the manually installed management agent, and oracle-cloud-agent when the management agent is a plugin enabled with Oracle Cloud Agent.*
* Check the log files permission with the agent user
```
sudo -u <agentuser> /bin/bash -c "cat <log file with complete path>"
```
* Setup ACL if the tool doesn't exist
```
rpm -q acl
```
* Grant the agent user READ access to the required log file
```
setfacl -m u:<agentuser>:r <path to the log file/log file name>
```
* Grant READ and EXECUTE with recursive options on parent folder in the log file path
```
setfacl -R -m u:<agentuser>:rx <path to the folder>
```
* Grant READ and EXECUTE with default option to allow all future log files created
```
setfacl -d -m u:<agentuser>:rx <path to the folder>
```
* Permissions to upload to Logging Service
  Dynamic group: 
```
ANY {instance.id = 'ocid1.instance.<region>.<location>.<unique_ID>', instance.compartment.id = 'ocid1.compartment.<region>..<unique_ID>'}
allow dynamic-group <dynamic_group_name> to use log-content in tenancy
```
* Supported parsers in Logging Service
  * Auditd (https://github.com/linux-audit/audit-documentation/wiki)
  * CRI (https://github.com/fluent/fluent-plugin-parser-cri)
  * JSON (https://docs.fluentd.org/parser/json)
  * CSV (https://docs.fluentd.org/parser/csv)
  * TSV (https://docs.fluentd.org/parser/tsv)
  * Syslog (https://docs.fluentd.org/parser/syslog)
  * Apache2 (https://docs.fluentd.org/parser/apache2)
  * Apache_Error (https://docs.fluentd.org/parser/apache_error)
  * Msgpack (https://docs.fluentd.org/parser/msgpack)
  * Regexp (https://docs.fluentd.org/parser/regexp)
  * Multiline (https://docs.fluentd.org/parser/multiline)

#### Oracle Management Agent Use Cases
1. Collect application custom logs into Logging Analytics
2. Collect Oracle Base Database Systems logs or Exadata Database Service Dedicated alert log and trace files into Logging Analytics
3. Collect Oracle Autonomous Database Serverless audit logs and data in tables/views into Logging Analytics
4. Onboard on-prem Oracle Databases to Database Management Service or Operations Insights
5. Onboard Oracle RAC databases to Database Management Service 

#### Oracle Unified Monitoring Agent Use Cases
1. Collect syslog and security logs into Logging Service to stream to third party SIEM
2. Collect Oracle Base Database Systems alert logs and trace files into Logging Service to send logs to external systems

### Conclusion
Oracle Cloud Infrastructure agents are the unsung heroes of cloud management and monitoring. While they empower you with unprecedented control and visibility, selecting the right agent for your specific needs requires careful consideration. By understanding the types of agents available, assessing your environment, and evaluating features against your use cases, you can confidently navigate the agent landscape and make informed decisions that drive operational excellence within your Oracle Cloud environment.

### Reference
* [Oracle Management Agent Technical Details](https://docs.oracle.com/en-us/iaas/management-agents/index.html)
* [Unified Monitoring Agent Technical Details](https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/agent_management.htm)
* [Set Up Continuous Log Collection From Your Hosts](https://docs.oracle.com/en/cloud/paas/logging-analytics/laagt/#before_you_begin)
* [Install Oracle Unified Monitoring Agent](https://docs.oracle.com/en-us/iaas/Content/Logging/Task/installing_the_agent.htm)
* [Unified Monitoring Agent Configuration](https://docs.oracle.com/en-us/iaas/Content/Logging/Task/agent-configuration-management.htm)
* OCI: How to Collect Management Agent Diagnostic Bundle? (Doc ID 2890347.1)
* How to solve Oracle Cloud Agent metrics not populated issue (Doc ID 2795938.1)
* OCI -Oracle Cloud Agent status showing invalid (Doc ID 2908911.1)

