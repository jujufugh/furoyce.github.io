---
title: "Leveraging Logging Analytics for Oracle Integration Cloud Logging and Monitoring - Part 1"
date: 2024-02-14
last_modified_at: 2024-02-14T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - Oracle Integration Cloud
  - OCI Log Analytics
---

As more customers are onboarded to Oracle Cloud Infrastructure (OCI) and run their critical integrations between OCI cloud services. Having a robust observability and monitoring solution for Oracle Integration Cloud (OIC) is pivotal for ensuring the efficiency, reliability and security of Oracle Integration solutions. It enables the organizations to maintain oversight over their integrations, diagnose issues promptly, and optimize performance. 


Oracle Integration Cloud is a fully managed, preconfigured environment that gives you the power to integrate your Oracle Cloud Infrastructure applications and services and on-premises applications.  
With Oracle Integration Cloud, you can:

- Develop integrations to design, monitor, and manage connections between your applications.
- Create process applications to automate and manage your business work flows.
- Build custom web and mobile applications.
- Store and retrieve files in Oracle Integration using the embedded SFTP-compliant file server.
- Create integrations that use B2B e-commerce to extend business processes to reach trading partners.

As more customers are onboarded to Oracle Cloud Infrastructure (OCI) and run their critical integrations between OCI cloud services. Having a robust observability and monitoring solution for Oracle Integration Cloud (OIC) is pivotal for ensuring the efficiency, reliability and security of Oracle Integration solutions. It enables the organizations to maintain oversight over their integrations, diagnose issues promptly, and optimize performance. 

## Out-of-the-box Oracle Integration Cloud monitoring dashboards

Oracle Integration Cloud offers out-of-the-box monitoring capabilities such as using the Oracle Integration dashboard to monitor and manage your integrations in the runtime environment. 

- Runtime Health
- System Health
- Agent Health
- Integrations Stats
- OIC Scheduling
- Design Time Metrics

You can also view information about how your integrations are performing. You can find more details of OIC native monitoring dashboard in OIC documentation.  
 

![Figure 1. Oracle Integration Cloud Monitoring Dashboard](/images/posts/2025-blogs/logan-ll-fusion-oic-process-monitoring-dashboard.png)

Figure 1. Oracle Integration Cloud Monitoring Dashboard

In the meantime, OCI Logging Analytics service takes the OIC logging and monitoring challenges further by delivering out-of-the-box OIC dashboards for all OCI customers. Oracle Logging Analytics is a cloud solution in Oracle Cloud Infrastructure that lets you index, enrich, aggregate, explore, search, analyze, correlate, visualize, and monitor all log data from your applications and system infrastructure.

OCI Logging Analytics takes the following OIC metrics and OIC activitiy stream logs as the telemetry sources for the out-of-the-box dashboards:

- OIC Service Metrics – Monitoring namespace: Integration
- OIC Activity Stream Logs – Logging Service Logs

![Figure 2. Oracle Integration: Health Overview](/images/posts/2025-blogs/logan-ll-fusion-oic-process-monitoring-dashboard.png)

Figure 2. Oracle Integration: Health Overview

![Figure 3. Oracle Integration: Key Metrics](/images/posts/2025-blogs/blog-oci_db_backup_metrics_explorer.png)

Figure 3. Oracle Integration: Key Metrics

![Figure 4. Oracle Integration: Time Taken Analysis](/images/posts/2025-blogs/blog-oci_db_backup_duration_query_results.png)

Figure 4. Oracle Integration: Time Taken Analysis

## Oracle Integration Cloud Design Time Audit Logs Use Cases

Oracle Integration Cloud also provides comprehensive record of changes and actions taken within the design-time environment of OIC. The Design Time Audit log data is instrumental for security, compliance, troubleshooting, and governance reasons. It provides a critical layer of visibility and control that is essential for managing the Oracle Integration Cloud instances.

- Infrastructure operation teams can view and track the changes across the OIC integrations and configurations
- Security and governance teams can monitor the accesses and changes in OIC to detect unauthorized or suspicious activities for operational transparency and collaboration
- Design Time Audit Log can be a valuable resource for integration developers to identify and troubleshoot issues for faster problem resolution

![Figure 5. Oracle Integration Cloud Design Time Audit Log Records](/images/posts/2025-blogs/blog-oci_database_info_log_explorer.png)

Figure 5. Oracle Integration Cloud Design Time Audit Log Records

There are two ways of accessing Design Time Audit Log records, and Design Time Audit Log records are excluded from the OIC activity stream logs, therefore there is no out-of-the-box integration between OIC Audit Log records and OCI Logging service logs.

- Using OIC console
- Via OIC REST API endpoints

Next, we will walk you through the strategies to enable the OIC Design Time Audit Logs in OCI Logging Analytics, so that you can:

- Enable short term reporting on the OIC Audit logs
- Retain OIC Audit logs in long term archive respository

## Oracle Cloud Integration Audit Logs Ingestion Strategies

We have three log ingestion strategies for OIC Audit logs (applicable to both OIC Gen2 and OIC Gen3), each strategy maps to specific monitoring use cases with the pros and cons. Based on our researches and testing, we recommend the push method via OIC Custom Integration for our customers to simplify the configuration complexity and reduce the overall operation overhead.

**Recommended Option:**

- Push Method via OIC Custom Integration
    - GET OIC Audit Logs via OIC REST API Endpoint into a stage file
    - Push OIC stage file to Logging Analytics via LA Log Upload REST API
    - (Optional) Use Logging Analytics Archival Storage Tier for long term OIC Audit Logs retention with lower cost
    - (Optional) Push OIC Audit Logs into Object Storage bucket and upload to Logging Analytics via Object Collection Rule
    - (Optional) Store the OIC Audit Logs in Object Storage for long term compliance and regulartory requirement
    - Pros:
        - Highly customizable custom integration to orchestrate the OIC Audit Logs ingestion
        - Flexible long term OIC Audit Logs retention options
    - Cons:
        - Additional workload impact on the OIC instances

![Figure 6. OIC Design Time Audit Logs Ingestion Push Method](/images/posts/2025-blogs/oci_loganalytics_metrics_api_ref_architecture_oci.drawio.png)

Figure 6. OIC Design Time Audit Logs Ingestion Push Method

**Other Options:**

- Merge Method via OIC custom integration
    - GET OIC Audit Logs via OIC REST API Endpoint
    - Merge OIC Audit logs into OIC Activity Stream Logs via Logger Action
    - (Optional) Use Logging Analytics Archival Storage Tier for long term OIC Audit Logs retention with lower cost
    - (Optional) Push OIC Audit Logs into Object Storage bucket via Service Connector Hub for long term retention
    - Pros:
        - OIC Audit Logs will be part of the OIC Activity Stream service logs, no need to stage additional files
        - Single REST API call within the custom integration
    - Cons:
        - OIC Audit Log records are XML format in the Activity Stream service elogs, additional parsing is required for the embedded XML format
        - Additional workload impact on the OIC instnaces
- Pull Method via Logging Analytics REST API Log Ingestion
    - GET OIC Audit Logs via OIC REST API Endpoint
    - Via Management Agent Logging Analytics Plugin
    - Pull OIC Audit logs via API endpoint in Management Agent and forward OIC Audit Logs to Logging Analytics
    - Pros:
        - No custom integration required for OIC instance
        - Native Logging Analytics REST API Log Ingestion via Management Agent
    - Cons:
        - Need to maintain an additional VM
        - Logging Analytics Entity will be associated with the Management Agent VM, not with the OIC instance

## Visualization and Dashboard

After successful ingestion of OIC Audit logs into Logging Analytics, we can query and visualize the OIC Audit logs and create widgets for Oracle Integration Cloud Audit Analysis dashboard.

![Figure 6. Oracle Integration: Audit Analysis Sample Dashboard](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 7. Oracle Integration: Audit Analysis Sample Dashboard

## Conclusion

Incorporating OIC Design Time Audit Logs into OCI Logging Analytics represents a strategic approach to maximizing the operational intelligence and security posture of cloud integration environments. By ingesting these detailed change records into OCI Logging Analytics, organizations unlock the potential to transform raw data into actionable insights to foster a more secure, efficient, and compliant integration ecosystem. Furthermore, the aggregation of OIC Audit Logs in Logging Analytics facilitates a more robust compliance framework, offering an aggregated view of activities across the integration landscape that is invaluable for audit trails and regulatory adherence. 

## Further Reading

- [Monitor Integrations OIC GEN2](https://docs.oracle.com/en/cloud/paas/integration-cloud/integrations-user/monitor-integrations.html#GUID-45976C83-37F1-4A6D-B79E-C749121B4E9E) 
- [Monitor Integrations OIC GEN3](https://docs.oracle.com/en/cloud/paas/application-integration/integrations-user/view-dashboard.html#GUID-A18B7212-6246-40A1-A7BB-E495EE29A92A) 
- [Review the OIC RESTful API for monitoring integration](https://docs.oracle.com/en/cloud/paas/integration-cloud/rest-api/op-ic-api-integration-v1-monitoring-auditrecords-get.html)
- [Surfacing OIC Design Time Audit blog](http://•	http://niallcblogs.blogspot.com/2021/10/885-surfacing-oic-design-time-audit.html)
- [OIC and OCI Logging Analytics](http://•	http://niallcblogs.blogspot.com/2023/02/954-oic-and-oci-logging-analytics.html)
- [Collect Logs from OCI Object Storage bucket](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/collect-logs-your-oci-object-storage-bucket.html)
- [Logging Analytics REST API Log Ingestion](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/set-rest-api-log-collection.html)

## Acknowledgements

- **Contributor:** Nolan Trouvé

​