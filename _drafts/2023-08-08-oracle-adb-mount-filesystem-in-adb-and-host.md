---
title: "Mount Oracle Filesytem service mount target in Autonomous Database and OCI compute instance"
date: 2023-08-08
last_modified_at: 2023-08-18T16:20:02-05:00
categories:
  - Blog
tags:
  - Oracle Filesystem service
  - Cloud Database
  - Oracle Cloud Infrastructure
  - Autonumous Database
---

### Introduction
In the ever-evolving landscape of cloud computing, the ability to efficiently log, monitor and manage resources has become a cornerstone of operational success. At the heart of this intricate ecosystem are OCI agents such as Oracle Cloud Agent, Oracle Management Agent, and Unified Monitoring Agent emerge as crucial players in ensuring observability and management is seamless and tightly integrated with OCI cloud resources.

#### OCI Filesystem service cross mount reference architecture

![Oracle Cloud Infrastrcuture Observability & Management Architecture](/images/posts/2023-08/royce-blog-onm_reference_architecture_review.color.png){: .align-center}

### OCI Filesystem overview
Oracle Cloud Infrastructure agents come in various forms, each designed with a specific set of capabilities to address different use cases. However, while these agents offer powerful functionalities, navigating the landscape and choosing the right agent for your unique requirements can sometimes be a daunting task. This overview aims to shed light on the types of OCI agents available, their key features, and how to approach selecting the most suitable agent for your use cases.

*Note: All the configuration details will be Linux OS version based.*

#### Oracle Management Agent Use Cases
1. Collect application custom logs into Logging Analytics
2. Collect Oracle Base Database Systems logs or Exadata Database Service Dedicated alert log and trace files into Logging Analytics
3. Collect Oracle Autonomous Database Serverless audit logs and data in tables/views into Logging Analytics
4. Onboard on-prem Oracle Databases to Database Management Service or Operations Insights
5. Onboard Oracle RAC databases to Database Management Service
6. Collect Oracle Kubernetes Clusters metrics by deploying Management Agent Statefulset of replica one and Metric Server for collecting and pushing the metrics to OCI Monitoring.

#### Oracle Unified Monitoring Agent Use Cases
1. Collect syslog and security logs into Logging Service to stream to third party SIEM
2. Collect Oracle Base Database Systems alert logs and trace files into Logging Service to send logs to external systems
3. Collect Oracle Kubernetes Clusters pod logs, object logs, syslogs into Logging Analytics using OCI Logging Analytics Fluentd output plugin `fluent-plugin-oci-logging-analytics` when it buffers into local file system, periodically creates payload and uploads it to OCI Logging Analytics.

### Conclusion
Oracle Cloud Infrastructure agents are the unsung heroes of cloud management and monitoring. While they empower you with unprecedented control and visibility, selecting the right agent for your specific needs requires careful consideration. By understanding the types of agents available, assessing your environment, and evaluating features against your use cases, you can confidently navigate the agent landscape and make informed decisions that drive operational excellence within your Oracle Cloud environment.

### Reference
* [Oracle Management Agent Technical Details](https://docs.oracle.com/en-us/iaas/management-agents/index.html)
* [Unified Monitoring Agent Technical Details](https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/agent_management.htm)
* [Set Up Continuous Log Collection From Your Hosts](https://docs.oracle.com/en/cloud/paas/logging-analytics/laagt/#before_you_begin)
* [Install Oracle Unified Monitoring Agent](https://docs.oracle.com/en-us/iaas/Content/Logging/Task/installing_the_agent.htm)
* [Unified Monitoring Agent Configuration](https://docs.oracle.com/en-us/iaas/Content/Logging/Task/agent-configuration-management.htm)
* [OCI Management Agent Helm Chart](https://github.com/oracle-quickstart/oci-management-agent/tree/main/kubernetes-monitoring/mgmtagent_helm)
* OCI: How to Collect Management Agent Diagnostic Bundle? (Doc ID 2890347.1)
* How to solve Oracle Cloud Agent metrics not populated issue (Doc ID 2795938.1)
* OCI -Oracle Cloud Agent status showing invalid (Doc ID 2908911.1)

