---
title: "Demystifying Logging and Monitoring Agent Types in OCI Observability and Management"
date: 2024-01-01
last_modified_at: 2024-01-01T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - Management Agent
  - OCI Agents
---

# Introduction

In the ever-evolving landscape of cloud computing, the ability to efficiently log, monitor and manage resources has become a cornerstone of operational success. At the heart of this intricate ecosystem are OCI agents such as Oracle Cloud Agent, Oracle Management Agent, and Unified Monitoring Agent emerge as crucial players in ensuring observability and management is seamless and tightly integrated with OCI cloud resources.

# OCI Observability & Management Reference Architecture

![Figure 1. OCI Observability and Management Reference Architecture](/images/posts/2025-blogs/oci_loganalytics_metrics_api_ref_architecture_oci.drawio.png)

Figure 1. Oracle Cloud Infrastructure Observability & Management Reference Architecture

# OCI Agents Overview

Oracle Cloud Infrastructure agents come in various forms, each designed with a specific set of capabilities to address different use cases. However, while these agents offer powerful functionalities, navigating the landscape and choosing the right agent for your unique requirements can sometimes be a daunting task. This overview aims to shed light on the types of OCI agents available, their key features, and how to approach selecting the most suitable agent for your use cases.

## OCI Agents Comparison

   
|Categories|Oracle Cloud Agent|Oracle Management Agent|Oracle Unified Monitoring Agent|
|---|---|---|---|
|Monitoring|via Compute Instance Monitoring Plugin|N/A|N/A|
|Logging|via Unified Monitoring Agent Plugin|N/A|Integration with Loggin Service via User Principal|
|Logging Analytics|via Management Agent Plugin|via Logging Analytics Plugin|N/A|
|Stack Monitoring|via Management Agent Plugin|via Stack Monitoring Plugin|N/A|
|Database Management|via Management Agent Plugin|via Database Management Plugin|N/A|
|Operations Insights|via Management Agent Plugin|via Operations Insights Plugin|N/A|
|Java Usage Tracking|via Management Agent Plugin|via Java Usage Tracking Plugin|N/A|
|Java Management Service|via Java Management Service Plugin|via Java Management Service Plugin|N/A|
|OS Management Hub|via OS Management Service Plugin|via OS Management Hub Plugin|N/A|
|Agent Installation|Preinstalled for OCI compute, manual installation(zip, rpm)|Manual installation(zip, rpm)|Manual installation(zip, rpm)|
|Authentication/Authorization|Resource Principal, Instance Principal|Resource Principal, Instance Principal|User Principal|
|Agent Management|Fully Integrated|Fully Integrated|Partially Integrated, no UI|
|Compute Instance Support|Yes|Yes|Yes|
|Oracle Base Database Service Support|No|Yes|Yes*|
|Oracle Exadata Database Service Dedicated Support|No|Yes|Yes*|

_* NOTE: The Unified Monitoring Agent can be installed in Oracle Base Database system or ExaDB-D VMs. Unified Monitoring Agent can send custom logs to OCI Loggign Service. However, open-source fluentd agent doesn't support parsing Oracle databases logs(for instance alert logs, trace files, listener logs, Grid Infrastructure logs etc). Raw database logs will be presented in OCI Logging Service._ 

## Oracle Cloud Agent

- **Oracle Cloud Agent** is a lightweight process that manages plugins running on compute instances. Oracle Cloud Agent plugins collect host logs, performance metrics, install OS updates, and perform other instance management tasks. Oracle Cloud Agent is installed by default for OCI compute instances.
- **Oracle Cloud Agent** supports the [Platform Images](https://docs.oracle.com/en-us/iaas/Content/Compute/References/images.htm#OracleProvided_Images) For unsupported OS version, **Oracle Management Agent** and **Unified Monitoring Agent** can be used for collecting log and cloud resource data for OCI Observability and Management services.
- **Oracle Cloud Agent** manages the following plugins for the OCI Observability and Management, it is considered as the best practice to use Oracle Cloud Agent whenever it is possible.

![Figure 2. Oracle Cloud Agent Plugins Overview](/images/posts/2025-blogs/oci_loganalytics_metrics_api_ref_architecture_oci.drawio.png)

Figure 2. Oracle Cloud Agent Plugins Overview

|Name|Description|
|---|---|
|Bastion|Allows secure shell (SSH) connections to an instance without public IP addresses using the [Bastion service](https://docs.oracle.com/iaas/Content/Bastion/Concepts/bastionoverview.htm).|
|---|---|
|Block Volume Management|[Configures Block Volume sessions](https://docs.oracle.com/en-us/iaas/Content/Block/Tasks/enablingblockvolumemanagementplugin.htm#enablingblockvolumemanagementplugin) for the instance.|
|---|---|
|Compute Instance Monitoring|Emits metrics about the instance's health, capacity, and performance. These metrics are consumed by the Monitoring service. [Enable Monitoring for Compute instances](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/enablingmonitoring.htm#Enabling_Monitoring_for_Compute_Instances).|
|---|---|
|Compute Instance Run Command|[Running commands](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/runningcommands.htm#runningcommands) and scripts within the instance to remotely configure, manage, and troubleshoot the instance.|
|---|---|
|Custom Logs Monitoring|Ingests [custom logs](https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/custom_logs.htm#custom_logs) into the Logging service.|
|---|---|
|Management Agent|Collects data from resources such as OSs, applications, and infrastructure resources for Oracle Cloud Infrastructure services that are integrated with [Management Agent](https://docs.oracle.com/iaas/management-agents/doc/management-agents-oracle-cloud-agent.html). Data can include observability, log, configuration, capacity, and health data.|
|---|---|
|Oracle Autonomous Linux|Manages autonomous updates and collects data associated with events, including logs and stack traces, for instances managed by the [Autonomous Linux service](https://docs.oracle.com/iaas/os-management/osms/alx-index.htm).|
|---|---|
|Oracle Java Management Service|Monitors and performs Java Development Kit (JDK) lifecycle management for Java deployments on instances managed by the [Java Management service.](https://docs.oracle.com/iaas/jms/index.html)|
|---|---|
|OS Management Service Agent|Manages updates and patches for the operating system environment on the instance. [OS Management](https://docs.oracle.com/iaas/os-management/osms/index.htm)|
|---|---|
|Vulnerability Scanning|[Scans the instance for potential security vulnerabilities](https://docs.oracle.com/iaas/scanning/using/overview.htm) like OS packages that require updates.|
|---|---|

- Supported OS versions
    - Windows-x86_64, Windows-x86
    - Oracle Linux
    - CentOS
    - Ubuntu
- **Oracle Cloud Agent** Troubleshooting, When you work with support engineer to troubleshoot issues with the Oracle Cloud Agent, you can generate diagnostic data for your agent, the tool will generate a TAR file with a name in the format oca-diag-<date>.<identifier>.tar.gz
    - cd /usr/bin/ocatools
    - sudo ./diagnostic

Further Reading about [Oracle Cloud Agent](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/manage-plugins.htm)

## Oracle Management Agent

- **Oracle Management Agent** is a service that provides low latency interactive communication and data collection between Oracle Cloud Infrastructure and IT targets. Oracle Management Agent has plugins integrated with O&M advanced services such as Logging Analytics, Database Management, Operations Insights, Java Management Service, Stack Monitoring, etc. Plugins can collect and ingest data from various cloud resources. Management Agent can be enabled as a plugin of the Oracle Cloud Agent or can install independently.

![Oracle Management Agent Plugins](/images/posts/2025-blogs/oci_loganalytics_metrics_api_ref_architecture_oci.drawio.png)

Figure 3. Oracle Management Agent Plugins

- Supported OS versions
    - Windows-x86_64, Windows-x86
    - Solaris-Sparc64
    - Linux-x86_64, Linux-Aarch64
- Oracle Management Agent Troubleshooting, generate Management Agent diagnostic support bundle
    - If Management Agent is enabled on compute instance via Oracle Cloud Agent
        - sudo -u oracle-cloud-agent /var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/agent_inst/bin/generateDiagnosticBundle.sh
    - If Management Agent is deployed as standalone installation
        - sudo -u mgmt_agent /opt/oracle/mgmt_agent/agent_inst/bin/generateDiagnosticBundle.sh

Further Reading about [Oracle Management Agent](https://docs.oracle.com/en-us/iaas/management-agents/index.html)

## Unified Monitoring Agent

- **Unified Monitoring Agent** is [fluentd-based](https://www.fluentd.org/) open-source agent to ingest custom logs such as syslogs, application logs, security logs to Oracle Logging Service. With proper agent configuration, it allows you to control exactly which logs you want to collect, how to parse them, and more.
- Note: The Unified Monitoring Agent is a fully managed agent, and custom client configuration is not officially supported. For example, gathering logs from remote sources is not recommended, since doing so can have serious security implications (because the log source cannot be verified).
- Unified Monitoring Agent supports following OS versions:
    - Oracle Linux 7, Oracle Linux 8
    - CentOS 7, CentOS Stream 8
    - Windows Server 2012 R2, Windows Server 2016, Windows Server 2019
    - Ubuntu 16.04, Ubuntu 18.04, Ubuntu 20.04
- Unified Monitoring Agent Troubleshooting
    - Log location: /var/log/unified-monitoring-agent/unified-monitoring-agent.log
    - You can also use journalctl to view system logs specific to Unified Monitoring Agent unit
        - unified-monitoring-agent.service
        - unified-monitoring-agent_config_downloader.service
        - unified-monitoring-agent_config_downloader.timer
        - unified-monitoring-agent_restarter.path
        - journalctl -u unified-monitoring-agent_config_downloader.service --since "2023-2-30 00:00:01" --until "2023-08-31 23:59:59"

Further Reading about [Oracle Unified Monitoring Agent](https://docs.oracle.com/en-us/iaas/Content/Logging/Task/installing_the_agent.htm)

## Oracle Management Agent Use Cases

1. Collect application custom logs into Logging Analytics
2. Collect Oracle Base Database Systems logs or Exadata Database Service Dedicated alert log and trace files into Logging Analytics
3. Collect Oracle Autonomous Database Serverless audit logs and data in tables/views into Logging Analytics
4. Onboard on-prem Oracle Databases to Database Management Service or Operations Insights
5. Onboard Oracle RAC databases to Database Management Service
6. Collect Oracle Kubernetes Clusters metrics by deploying Management Agent Statefulset of replica one and Metric Server for collecting and pushing the metrics to OCI Monitoring.

## Oracle Unified Monitoring Agent Use Cases

1. Collect syslog and security logs into Logging Service to stream to third party SIEM
2. Collect Oracle Base Database Systems alert logs and trace files into Logging Service to send logs to external systems
3. Collect Oracle Kubernetes Clusters pod logs, object logs, syslogs into Logging Analytics using OCI Logging Analytics Fluentd output plugin fluent-plugin-oci-logging-analytics when it buffers into local file system, periodically creates payload and uploads it to OCI Logging Analytics.

# Conclusion

Oracle Cloud Infrastructure agents are the unsung heroes of cloud management and monitoring. While they empower you with unprecedented control and visibility, selecting the right agent for your specific needs requires careful consideration. By understanding the types of agents available, assessing your environment, and evaluating features against your use cases, you can confidently navigate the agent landscape and make informed decisions that drive operational excellence within your Oracle Cloud environment.

Sign up for an [Oracle Cloud Infrastructure free trial account](https://www.oracle.com/cloud/free/) today to try out new Oracle Cloud Infrastructure features!

# Further Reading

- [Oracle Cloud Agent Technical Details](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/manage-plugins.htm)
- [Oracle Cloud Agent Troubleshooting](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/manage-plugins-troubleshooting.htm#troubleshoot)
- [Oracle Management Agent Technical Details](https://docs.oracle.com/en-us/iaas/management-agents/index.html)
- [Unified Monitoring Agent Technical Details](https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/agent_management.htm)
- [Unified Monitoring Agent Troubleshooting](https://docs.oracle.com/en-us/iaas/Content/Logging/Reference/agent_troubleshooting.htm)
- [Set Up Continuous Log Collection From Your Hosts](https://docs.oracle.com/en/cloud/paas/logging-analytics/laagt/#before_you_begin)
- [OCI Management Agent Helm Chart](https://github.com/oracle-quickstart/oci-management-agent/tree/main/kubernetes-monitoring/mgmtagent_helm)
- OCI: How to Collect Management Agent Diagnostic Bundle? (Doc ID 2890347.1)
- How to solve Oracle Cloud Agent metrics not populated issue (Doc ID 2795938.1)
- OCI -Oracle Cloud Agent status showing invalid (Doc ID 2908911.1)

​