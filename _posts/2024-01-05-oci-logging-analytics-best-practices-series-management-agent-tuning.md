---
title: "OCI Logging Analytics Best Practices Series - Management Agent Tuning"
date: 2024-01-05
last_modified_at: 2024-01-05T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - OCI Log Analytics
  - Best Practices
---

Oracle Cloud Infrastructure (OCI) Logging Analytics provides a comprehensive solution for managing and analyzing logs, facilitating easier troubleshooting, auditing, and monitoring of applications and infrastructure. In the cloud environment, it's crucial to use it effectively to optimize both performance and cost.

As a log analysis and log correlation cloud service, we always face requirements to ingest log data into Logging Analytics for log processing and indexing. There are many approaches to ingest your logs into Oracle Logging Analytics using the Oracle Management Agent, uploading logs on-demand, collecting them from the OCI Object Store, or using Service Connector. Based on the log sources and destination, we need to select the proper agent for various log ingestion use cases which ensures efficient collection is configured to filter, parse, and forward logs in a structured manner.

## Right Agent for the Right Job

In my blog [Demystifying Logging and Monitoring Agent Types in OCI Observability and Management](https://www.ateam-oracle.com/post/demystifying-logging-and-monitoring-agent-types-in-oci-observability-and-management), I have discussed different agent types and their use cases in OCI. It's very important to understand their feature parity and their pros and cons when choosing the agent for the job. As a common strategy, we make our agent decisions based on the destination service we are going to ingest logs into. 

![OCI Logging Analytics Smart Analytics and Machine Learning for Technology Stacks](/images/posts/2025-blogs/oci_loganalytics_metrics_api_ref_architecture_oci.drawio.png)

Figure 1. OCI Logging Analytics Smart Analytics and Machine Learning for Technology Stacks

**Ingesting logs via Unified Monitoring Agent(FluentD)** 

- Destination: OCI Logging Service
- Option to send log data to different target systems (eg. external SIEM system)
- Limited supported list of parsers: it doesn't allow you to create a custom parser for your logs 
    - None
    - Auditd ([https://github.com/linux-audit/audit-documentation/wiki](https://github.com/linux-audit/audit-documentation/wiki))
    - CRI ([https://github.com/fluent/fluent-plugin-parser-cri](https://github.com/fluent/fluent-plugin-parser-cri))
    - JSON ([https://docs.fluentd.org/parser/json](https://docs.fluentd.org/parser/json))
    - CSV ([https://docs.fluentd.org/parser/csv](https://docs.fluentd.org/parser/csv))
    - TSV ([https://docs.fluentd.org/parser/tsv](https://docs.fluentd.org/parser/tsv))
    - Syslog ([https://docs.fluentd.org/parser/syslog](https://docs.fluentd.org/parser/syslog))
    - Apache2 ([https://docs.fluentd.org/parser/apache2](https://docs.fluentd.org/parser/apache2))
    - Apache_Error ([https://docs.fluentd.org/parser/apache_error](https://docs.fluentd.org/parser/apache_error))
    - Msgpack ([https://docs.fluentd.org/parser/msgpack](https://docs.fluentd.org/parser/msgpack))
    - Regexp ([https://docs.fluentd.org/parser/regexp](https://docs.fluentd.org/parser/regexp))
    - Multiline ([https://docs.fluentd.org/parser/multiline](https://docs.fluentd.org/parser/multiline))
- Limited log retention: 12 months for Audit Logs, and 6 months for service logs and custom logs
- Archive option into Object Storage Bucket

**Ingesting logs via Management Agent**

- Destination: OCI Logging Analytics
- Custom Parsers and Log Sources: besides supported out-of-the-box Parsers and Log Sources, you can use the following parser types to create parsers for your log content
    - Regex Type
    - JSON Type
    - XML Type
    - Delimited Type
- Archive option is integrated into Logging Analytics
- No export option for the indexed and processed data in Logging Analytics
- Supported collection types
    - File
    - Syslog listener
    - Database SQL connection
    - Retrieve logs via REST API calls
    - Windows Event Messages via custom event channels
    - Oracle Diagnostic Logs for Middleware and Oracle Applications 

## Efficient Log Collection and Ingestion

Once you have successfully picked the right agent for the right job and configured the parser and log source for the agent to ingest and process logs in OCI, you might face a challenge when the cloud resources generate a large amount of log data which may exceed the OCI Management Agent upload limit. In those cases, additional Management Agent performance tuning is required to make sure the Management Agent can push through as much log data as possible in real-time. 

**Fun facts about Management Agent configuration and Performance Tuning**

- You can update Agent configuration via the property file ${MGMT_AGENT_HOME}/agent_inst/config/emd.properties
    - [Configure Logging Analytics database SQL collection schedule](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/advanced-configuration-options-management-agent.html#GUID-019DF38E-822A-4E5B-B900-B21A45BCFD09) 
    - [Enable Log Collection from Large Folders(more than 10000 files)](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/advanced-configuration-options-management-agent.html#GUID-02D8CC08-69D6-4043-AA3E-737BB7068308)
- Agent upload file size limit is 1.5MB for each log bundle
    - MOS note: OCI: File Size Limit To Uploaded To Logging Analytics (Doc ID 2946101.1)
    - Enable parallel threads to increase the upload throughput
- Agent Parallel Threads parameter: "_senderManagerPoolSize"
    - Default is 3.
    - Number of threads to work on parallel uploading log bundles
    - Eg. 10MB log data will split into 7 log bundles, if we have 3 parallel upload threads, it takes 3 rounds to upload all log bundles, whereas log bundles will upload all at the same if we have more than 7 upload threads
- Agent Send Time Frequency: "_senderManagerSendTimerFrequency"
    - Default is 30 seconds. 
    - Minimum tiem frequence is 1 second.
- Agent force upload without latency: "_forceSendImmediate"
    - Default value is false. 
    - We can set it to true so that sender manager will upload files as soon as they are generated with no delay.

**In order to improve the Logging Analytics ingestion performance from the OCI Logging Service and Service Connector Hub, we can reduce Log Volume for logs**

- Filter out unnecessary logs or verbose debug logs in Service Connector Hub that don't add value to the analysis
- Controls costs and reduces the clutter in the Logging Analytics workspace

**Another log collection theme in OCI O&M is to forward your logs to the central syslog server**

- Management Agent running on the syslog server is responsible forward logs to Logging Analytics
- Rsyslogd or a built-in remote logging in network appliance can forward the logs to syslog server
- Management Agent can listen to syslog server port to collect and forward logs
- I have two blogs discussing the topic in detail: 
    - [Use Oracle Management Agent to forward logs to Logging Analytics via syslog listener](https://roycefu.com/blog/oracle-onm-logging-analytics-syslog-listener/)
    - [Use Oracle Management Agent to consolidate F5 logs in OCI Logging and Logging Analytics](https://roycefu.com/blog/oracle-onm-F5-log-consolidation-via-management-agent/)

## Conclusion

Optimizing the Management Agent for peak performance in log ingestion is crucial for your infrastructure and operational teams. This enhancement is key to ensuring timely log analysis and detection. By adopting these best practices, you're not just adjusting a system; you're unlocking the full potential of your log data. This enables more informed decision-making, streamlines operational workflows, and boosts security measures. Embrace the power of Management Tuning in your log data analysis to elevate your organization's efficiency and performance, paving the way for operational superiority.

Please check out our [Oracle Cloud Customer Connect Observability and Management Community](https://community.oracle.com/customerconnect/categories/oci-management). You can pose questions, connect with experts, and share your successes, thoughts and ideas about Oracle Cloud Observability and Management solutions (including OCI Application Performance Monitoring, Stack Monitoring, Logging Analytics, Database Management and Operations Insights).

## Further Reading 

- [OCI Logging Analytics Best Practices Series - Custom Log Sources and Parsers Tips](https://www.ateam-oracle.com/post/oci-logging-analytics-best-practices-log-parsing-and-enrichment)
- [OCI Logging Analytics Best Practices Series - Cost Optimization](https://www.ateam-oracle.com/post/oci-logging-analytics-best-practices-series-cost-optimization)
- [Use Macro for Case-Insensitive Match of Log File Path](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/advanced-configuration-options-management-agent.html#GUID-4082092C-C551-4E71-8065-38E90369BAC9)
- [Demystifying Logging and Monitoring Agent Types in OCI Observability and Management](https://blogs.oracle.com/observability/post/la-demystifying-agent-om-oci)

## Acknowledgements

- **Contributor:** Waymon Whiting

​