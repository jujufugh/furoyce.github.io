---
title: "Exploring the log consolidation technical architectures in OCI"
date: 2023-09-14
last_modified_at: 2023-09141T16:20:02-05:00
categories:
  - Blog
tags:
  - Observerability and Monitoring
  - Logging Analytics
  - Logging
  - Log Consolidation
---

### Introduction
Log consolidation is essential for improving security, simplifying log management, enhancing troubleshooting and debugging, meeting compliance requirements, optimizing resource usage, and supporting historical analysis in modern IT and cloud environments. It streamlines the process of collecting, storing, and analyzing log data, making it an indispensable practice for organizations of all sizes.

![OCI O&M Reference Architecture](/images/posts/2023-08/royce-blog-onm_reference_architecture_review.color.png){: .align-center}

### OCI Logs
* Service Logs and Audit Logs
  * Cross Region Consolidation
  * External 
* Custom Logs
  * Application Logs
  * Syslogs
  * Database Audit Logs 
  * Same Region Consolidation
  * Cross Region Consolidation
  * External

### Use Cases
* Centralized Visibility: 
  Log consolidation involves gathering log data from various sources and systems into a central repository or service. This centralization provides a single point of access to all logs, enabling IT teams to have a holistic view of their entire infrastructure's activities and events. It simplifies log management and analysis by eliminating the need to access logs from multiple sources.
  * Cross-region log data consolidation for central log repository within OCI
  * Forward logs to log server before sending to Logging Analytics for analysis
* Security Monitoring: 
  Security is a top concern in IT, and logs play a critical role in detecting and responding to security threats. Centralized logs make it easier to monitor for suspicious or unauthorized activities, identify patterns of behavior indicative of cyberattacks, and respond quickly to security incidents. Without log consolidation, security teams may miss critical information hidden in disparate log sources.
  * Consolidate log data and send the logs to external SIEM system
* Compliance and Auditing:
  Many industries and organizations are subject to regulatory compliance requirements that mandate the retention and secure storage of log data for a specified period. Log consolidation simplifies compliance efforts by centralizing logs, ensuring they are accessible when needed for audits and reporting.
  * Archive Logs in Object Storage for long term retention, compliance and auditing purpose
* 


### Top-Level Use Cases

* IT Ops and DevOps Management
* Application Management
* Audit, Security and Compliance Management
* Kubernets and Cloud Native Management


### Log Ingestion Method



### Conclusion
Oracle Cloud Infrastructure File Storage Service provides the solution to attach the file system to the Autonomous Database and cross mount it to one or many compute instances so that we can have real time access to the log files or scripts across many cloud resources. The solution compliments the use cases and requirements that cannot be accomplished by an Object Storage integration with Autonomous Database. Please check out more use cases in the Oracle File Storage Service [documentation](https://docs.oracle.com/en-us/iaas/Content/File/home.htm).

### Reference
* [DBMS_CLOUD_ADMIN package Doc Reference](https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/dbms-cloud-admin.html#GUID-1C562DE9-066C-4D8B-B058-53F30E9061C3)
* [How to Attach a File System to your Autonomous Database](https://blogs.oracle.com/datawarehousing/post/attach-file-system-autonomous-database)
* [Exploring identity squash with OCI File Storage service](https://blogs.oracle.com/cloud-infrastructure/post/exploring-identity-squash-with-oci-file-storage-service)
* [Overview of File Storage](https://docs.oracle.com/en-us/iaas/Content/File/Concepts/filestorageoverview.htm#Overview_of_File_Storage)
* [Attach External File Storage to Autonomous Database on Dedicated Exadata Infrastructure](https://docs.oracle.com/en/cloud/paas/autonomous-database/dedicated/defsd/index.html#articletitle)

