---
title: "OCI Logging Analytics Best Practices Series - Cost Optimization"
date: 2024-01-08
last_modified_at: 2024-01-08T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - OCI Log Analytics
  - Best Practices
---

Oracle Cloud Infrastructure (OCI) Logging Analytics offers powerful tools for the collection, analysis, and management of log data, providing insights that drive informed decision-making. The efficient management of cloud cost is a pivotal aspect of operational success. In this blog, we will look into the keys to optimizing expenses in OCI Logging Analytics in understanding and implementing best practices for data retention and comprehending the nuances of Logging Analytics storage pricing. By the end of this guide, you'll be equipped with best practices that not only streamline your operations but also ensure that your use of OCI Logging Analytics is as cost-effective as possible. Let's embark on this journey to maximize efficiency and optimize costs in the realm of cloud log management.

## Data Retention and Storage

Data retention and storage strategies directly impact both the cost and effectiveness of your OCI Logging Analytics setup. By understanding your data's lifecycle, setting precise retention policies, leveraging cost-effective storage options, and continually monitoring and adjusting your approach, you can strike a balance between cost, performance, and compliance. As with all cloud services, staying proactive and informed ensures optimal utilization and value extraction.

**Logging Analytics Storage Fun Facts:**

- Price model is based on the size of the storage usage of ingested and processed log data size.
- 1 Active Storage Unit or 1 Archive Storage Unit is 300GB of log data
- Archive storage can be used when 1 TB of log data in Active Storage Unit
- Active Storage Unit log data can be archived beyond 30 days
- Log data can be purged based on log query and timestamp
- Logging Analytics log data is stored in Oracle managed buckets, each bucket is approximately 400MB of log entries.
- Logging Analytics uses newest log timestamp to determine whether the logs that can be moved to Archive storage. The newest log timestamp older than 30days can be archived.
- Archive process runs very 24 hours, not depending on the time when the archive was enabled.
- Archive storage can be purged based on the duration(days).
- Archive log entries cannot be purged based on query filter.
- Active log entries cannot be archived based on the query filter.
- Archive data can be recalled into Active storage using timestamp and query to filter data.
- Recall the archived data makes a copy of log data in Active storage.
- After the analysis is completed on recalled data, you can release the log data to clean up the active archival recall.
- Purge on the recalled log data before release to reduce the cost on Active storage.

**We have multiple different log sources from OCI, on-prem or third-party cloud:**

- Audit logs: Logs related to events emitted by the Audit service.
- Service logs: Logs emitted by individual services such as API Gateway, Events, Functions, Load Balancing, Object Storage, and VCN flow logs.
- Custom logs: Logs that contain diagnostic information from custom applications, other cloud providers, or an on-premises environment.
- Ad-hoc log data: for one-time analysis or testing

**Among those log data, we can categorize them into different types:**

- Transient Data: Might only be retained for days or weeks.
- Operational Data: Could be retained for weeks to months.
- Archival Data: Often retained for years.

**Best Practices for Managing Data Retention and Storage of Logging Analytics:**

- Set appropriate purge retention policy for Logging Analytics Active Storage Unit. Not all logs need to be retained in Active Storage Unit. Define a retention policy based on compliance needs and business requirements. The shorter the retention, the less storage costs will be incurred.
    - Example Scenario, Logging Analytics purging and archival strategy for multiple application and infrastructure stacks
    - Log Ingest Rate: 150GB/day
    - Total Retention: 60 months
    - Operations Root Cause Analysis Time Range: 3 months
    - Active Units after month 4: 45

![Logging Analytics Sizing and Pricing Example](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 1. Logging Analytics Sizing and Pricing Example

- Archive Storage Unit doesn’t have option to selective archive log data. If you want to only archive specific log data for example application or audit log, you can use combination of the purging retention policy and archival policy to meet your compliance and regulatory requirement while cut down the storage cost.  
      
    For example: you set your Active Storage Duration for 30 days, log data beyond 30 days will be archived in the Archive Storage Unit. However, you don’t want to archive VCN Flow logs since they occupy huge amount of space and don’t provide much value to troubleshoot your application issues. You can purge your VCN Flow Logs on the 29th of the month, 1 day before the archive job kicks off to purge these log data from Active Storage Unit in advance, therefore you will not archive and store unnecessary data in Logging Analytics.
- Use Object Storage Archive tier to facilitate long term retention for additional cost saving due to the price advantage of the Object Storage Archive tier. This option is suitable for very infrequent access of the archive log data because this approach takes additional time to restore archive log data to standard tier in Object Storage bucket and you will need to upload data back into Logging Analytics via Object Collection Rule or manual upload. 

![Logging Analytics Data Archival Options](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 2. Logging Analytics Data Archival Options

## Understand Pricing Tiers

- OCI Logging Analytics has different pricing tiers based on log storage size. It charges you the full storage unit once the log data stores into the next unit. Estimate your log size generated from your application, infrastructure and cloud resources and optimize your storage unit usage with the cost. For example, if you're close to crossing into another storage unit, consider if some data could be archived or cleaned up.
- Active Storage list price below is based on monthly charge even it is metered hourly per unit, on the other side Archive Storage list price is based on the hourly charge.

![Logging Analytics Storage Tiered Pricing](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 3. Logging Analytics Tiered Pricing

## Logging Analytics Cost Monitoring and Alerts

- **Monitor Storage and Ingestion:** Regularly monitor the amount of data ingested and stored in Logging Analytics. If there’s an unusual spike, investigate to ensure there’s no unnecessary data flooding the system.
    - Monitor the Logging Analytics used Storage size via Monitoring service metric namespace oci_logging_analytics, the following metrics only populates at Root Compartment level because Logging Analytics is a tenancy level service.  
        - Active Storage Used
        - Archival Storage Used
        - Processing Errors

![Logging Analytics Active Storage Size Monitoring](/images/posts/2025-blogs/blog-oci_db_backup_metrics_explorer.png)

Figure 4. Logging Analytics Active Storage Size Monitoring

- Monitor the Logging Analytics upload data size via Monitoring service metric namespace oci_logging_analytics, metric name LogCollectionUploadDataSize with 12-hour interval or 1 day interval over past 7 days, choose Sum as your statistics for the monitoring query.

![Logging Analytics Logs Upload Size Monitoring](/images/posts/2025-blogs/blog-oci_db_backup_metrics_explorer.png)

Figure 5. Logging Analytics Log Upload Size Monitoring

- In Logging Analytics Administration Storage page, you can view your Active Storage Unit and Archive Storage Unit usage. You can estimate used storage size in Purge Logs feature, which you can specify a timestamp and a query to estimate the storage usage for the log type.
- Create dashboard using the metrics above or you can import the prebuilt dashboard from Oracle quickstart community repo for Logging Analytics [Security Operations Dashboard](https://github.com/oracle-quickstart/oci-o11y-solutions/blob/main/knowlege-content/MAP/security-fundamentals-dashboards/Security%20Operations.json)

![Logging Analytics Security Operations Dashboard](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 6. Logging Analytics Security Operations Dashboard

- **Set Alarm to detect the over usage of the Logging Analytics Storage:** like you setup the alarms for other metrics, you can setup alarm for the Logging Analytics storage usage in Monitoring service as well

![Logging Analytics Active Storage Monitoring Alarm](/images/posts/2025-blogs/blog-oci_db_backup_metrics_explorer.png)

Figure 7. Logging Analytics Active Storage Monitoring Alarm

- **Set Budget Alerts:** OCI Cost Management provides budget monitoring and alerting tools. Set up alerts to notify you when your Observability and Management compartment or Logging Analytics compartment spending approaches or exceeds a specific threshold.

![OCI Budget Management for Logging Analytics](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 8. OCI Budget Management for Logging Analytics

## Further Reading

- [OCI Logging Analytics Best Practices Series - Management Agent Tuning](https://www.ateam-oracle.com/post/oci-logging-analytics-best-practices-management-agent-tuning)
- [OCI Logging Analytics Best Practices Series - Custom Log Sources and Parsers Tips](https://www.ateam-oracle.com/post/oci-logging-analytics-best-practices-log-parsing-and-enrichment)
- [Manage Logging Analytics Storage](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/manage-storage.html)
- [Manage Alarms in OCI](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/managingalarms.htm)
- [Observability and Management Platform Pricing](https://www.oracle.com/manageability/pricing/)
- [Create Budgets for Logging Analytics Cost Management](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm#Budgets_Overview)

Please check out our [Oracle Cloud Customer Connect Observability and Management Community](https://community.oracle.com/customerconnect/categories/oci-management). You can pose questions, connect with experts, and share your successes, thoughts and ideas about Oracle Cloud Observability and Management solutions (including OCI Application Performance Monitoring, Stack Monitoring, Logging Analytics, Database Management and Operations Insights).

## Acknowledgements

- **Contributor:** Waymon Whiting

​