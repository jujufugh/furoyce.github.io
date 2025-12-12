---
title: "ZFS Storage Appliance Observability and Monitoring"
date: 2024-11-04
last_modified_at: 2024-11-04T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - ZFS Storage
  - OCI Log Analytics
---

The Oracle ZFS Storage Appliance stands out as a powerful tool, offering exceptional performance and reliability. This blog post delves into how the integration of OCI services—specifically, OCI Logging Analytics, Stack Monitoring, and Monitoring Service—can bridge this gap. By enhancing the observability and monitoring of the ZFS Storage Appliance, users can gain deeper insights, streamline operations, and ensure optimal performance of their storage infrastructure.


In today's data-driven technology landscape, enterprise applications demand storage solutions that are not only scalable and reliable but also deliver high performance. Many organizations depend on the Oracle ZFS Storage Appliance to fulfill these critical requirements. Recognized for its exceptional capabilities, the ZFS Storage Appliance serves as the backbone for numerous enterprise solutions. This blog post explores how integrating Oracle Cloud Infrastructure (OCI) services—specifically OCI Logging Analytics, Stack Monitoring, and Monitoring Service—can further enhance the observability and monitoring of the ZFS Storage Appliance. By leveraging these OCI services, enterprises can gain deeper insights, streamline operations, and ensure optimal performance of their storage infrastructure.

# Key Monitoring Requirements

Multi-stack monitoring enables comprehensive operational monitoring from the ZFS client to the ZFS Storage Appliance, encompassing all components of the underlying Oracle Cloud Infrastructure (OCI) and associated resources.

- Performance Metrics Dashboard: Consolidate performance-related metrics such as CPU usage, Disk I/O operations, NFS operations, and network throughput into a comprehensive dashboard for real-time performance monitoring.
- Cluster Availability and Failover: Track the availability of the ZFS storage appliance cluster and its failover operations to maintain uninterrupted service.
- Error and Failure Alerts: Monitor for errors or critical failures within the ZFS system, analyze alert and fault logs, and receive real-time alerts via the IT Service Management (ITSM) platform.
- Monitoring NFS Mount Points: Ensure the availability and accessibility of NFS mount points on the ZFS storage appliance.
- OCI Audit API Calls Analysis: Identity is a crucial yet often overlooked component for a effective and smooth cloud operation, implement comprehensive monitoring of OCI API calls helps to identity any failures and potential issues related to API interactions.

![Figure 1. ZFS Storage Appliance Monitoring](/images/posts/2025-blogs/blog-oci_db_backup_metrics_explorer.png)

Figure 1. ZFS Storage Appliance Monitoring Dashboard

![Figure 2. ZFS Storage Appliance Monitoring Dashboard](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 2. ZFS Storage Appliance Monitoring Dashboard

# Reference Architecture

By implementing this architecture, users can effectively manage and optimize their ZFS Storage Appliance, ensuring robust performance and reliability.

![Figure 1. ZFS Storage Appliance Observability and Monitoring Reference Architecture](/images/posts/2025-blogs/oci_loganalytics_metrics_api_ref_architecture_oci.drawio.png)

Figure 3. ZFS Storage Appliance Observability and Monitoring Reference Architecture

# Proposed O&M Services

## Logging Analytics

- **Ingest OCI Audit Logs:** Utilize OCI Logging Analytics to ingest OCI Audit logs for comprehensive analysis. This captures OCI inter-service API call failures, particularly those related to authentication and authorization issues indicated by HTTP status codes 401 (Unauthorized) and 404 (Not Found). By monitoring these failures, organizations can quickly identify security breaches or misconfigurations affecting service interactions.
    
- **Integrate ZFS Logs via REST API:** Ingest logs from the ZFS Storage Appliance into Logging Analytics using REST API ingestion methods. This integration allows for the correlation of OCI authentication failure events with ZFS system and fault logs. By having a unified view of logs from both OCI and ZFS, administrators can perform more effective root cause analysis, enhancing system reliability and reducing downtime.
    

## Stack Monitoring

- **Onboard Application VMs:** Incorporate application virtual machines (VMs) into OCI Stack Monitoring to gain visibility into their performance metrics. This onboarding process ensures that critical metrics—such as CPU utilization, memory usage, and network latency—are accessible via Stack Monitoring dashboards, facilitating proactive performance management.
    
- **Implement Metrics Extensions for NFS Mount Points:** Use Metrics Extensions within Stack Monitoring to test the availability and responsiveness of ZFS mount points. By setting a timeout value of 30 seconds, the system periodically verifies that the NFS mount points are accessible and functioning correctly. This helps in promptly detecting and addressing any connectivity issues that could impact application performance.
    

## Application Performance Monitoring

- **Monitor your ZFS management console:** Use Synthetic Monitoring, a feature of Application Perfromance Monitoring, to proactively monitor the ZFS console to prevent issues before users are impacted.

## Monitoring Service

- **Visualize Metrics and Logs in Dashboards:** Leverage the OCI Monitoring Service to create customizable dashboards that visualize key performance metrics and log analysis results. These dashboards provide real-time insights into system health, enabling IT teams to monitor trends, identify anomalies, and respond swiftly to any performance issues. By consolidating this information into a single pane of glass, organizations can improve operational efficiency and decision-making.

# Enable ZFS Storage Appliance Monitoring in O&M

The Oracle ZFS Storage Appliance provides a robust set of analytical datasets accessible via its analytics services and various log data types. These datasets offer in-depth visibility into various performance and operational aspects of the storage appliance, making them invaluable for comprehensive monitoring and analysis. Including system logs, alert logs, audit logs, and fault logs enriches the monitoring ecosystem, providing deeper insights into the appliance's operational state and aiding in proactive issue resolution. 

- **CPU Usage Metrics:** Monitor processor utilization to identify performance bottlenecks and optimize computational resources.
- **Disk I/O Operations:** Track read/write operations to analyze storage performance and detect potential throughput issues.
- **Network Throughput:** Measure inbound and outbound network traffic to ensure network resources are adequately provisioned and identify any anomalies in data transfer rates.
- **NFS Operations:** Analyze Network File System (NFS) protocol operations to assess the performance and reliability of file-sharing services.
- **System Logs:** Monitoring system logs helps identify underlying issues that could affect the appliance's overall functionality.
- **Alert Logs:** Contain warnings and critical alerts generated by the system. These logs are crucial for detecting anomalies, potential failures that require immediate attention.
- **Audit Logs:** Audit logs are vital for compliance purposes, security audits, and tracking unauthorized access.
- **Fault Logs:** Monitoring fault logs enables prompt identification and rectification of hardware issues, firmware problems, or software glitches.

We can access ZFS Storage Appliance analytical datasets via REST API by utilizing the ZFS Storage Appliance's RESTful API to programmatically access and retrieve the desired analytical datasets and convert the metrics data into log records in Logging Analytics. This method allows for automated data collection at defined intervals and we can ingest the data into Logging Analytics for analysis and correlation such as system fault errors, authentication failures, and CPU, Disk, Network performance metrics. This holistic view aids in identifying patterns and root causes of issues that span multiple system components.

## Prerequisites

- Set up service policies for Oracle Cloud Logging Analytics. See [Enable Access to Logging Analytics and Its Resources](https://docs.oracle.com/iaas/logging-analytics/doc/enable-access-logging-analytics-and-its-resources.html) and [Prerequisite IAM Policies](https://docs.oracle.com/iaas/logging-analytics/doc/prerequisite-iam-policies.html) in Oracle Cloud Infrastructure Documentation.
- Install the Management Agent on a client host VM which has http or https access to your endpoint server, we will use this host for Log Source entity association. See [Set Up Continuous Log Collection From Your Hosts](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/set-continuous-log-collection-form-your-hosts.html#GUID-310D58A5-9F27-48C9-AE62-009BD094AB69).
- On Unix-based hosts, the user that installs management agent is mgmt_agent for the manually installed management agent, and oracle-cloud-agent when the management agent is a plugin enabled with Oracle Cloud Agent.
- Set up Application Performance Monitoring in your tenancy following the steps [here](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/get-started-application-performance-monitoring.html). If your ZFS console URL is available only within your company's network, create a [Dedicated Vantage Point](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/use-dedicated-vantage-points.html) to run your synthetic monitors.

## Configure SSL certificate keystore and truststore to access ZFS REST API endpoint

- Check if the existing truststore file is presented on the management agent VM host

ls -ltr /var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/agent_inst/config/security/plugins/certificates/AgentTrust.jks

- Download the SSL certificate
- Go to the ZFS UI console -> Configuration -> Settings
- Download the SSL certificate whose Issuer common name is the same as your ZFS storage appliance host name  
     

![Figure 4. Download ZFS Storage Appliance SSL certificates](/images/posts/2025-blogs/blog-oci_database_info_listdbhomes_edit.png)

Figure 4. Download ZFS Storage Appliance SSL certificates

- Convert the SSL certificate format from crt to pem

openssl x509 -in 11bb3996-2cbd-4085-8f56-a8afa57d38b3.crt -out instance-zfs.pem -outform PEM

- Create a new JKS keystore by importing SSL certificate

sudo -u oracle-cloud-agent /var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/jdk1.8.0_411-b09/bin/keytool -importcert -alias <FQDN_HOSTNAME>.oraclevcn.com.pem -file /tmp/instance-zfs.pem  -keystore /var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/agent_inst/config/security/plugins/certificates/AgentTrust.jks

- Specify the password for the keystore

/var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/jdk1.8.0_411-b09/bin/keytool -list -keystore /var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/agent_inst/config/security/plugins/certificates/AgentTrust.jks

## Create the credential file to authorize the management agent API access to the ZFS Storage Appliance REST API endpoint

- Management Agent REST API credential file example

cat /tmp/agent_apicreds.json 

{
  "source":"lacollector.la_rest_api",
  "name":"ZFSRESTAPICRED",
  "type":"HTTPSCreds",
  "description":"These are HTTPS (BasicAuth) credentials.",
  "properties":
  [
    { "name":"HTTPSUserName", "value":"CLEAR[opc]" },
    { "name":"HTTPSPassword", "value":"CLEAR[xxxxx]" },
    { "name":"ssl_trustStoreType", "value":"JKS" },
    { "name":"ssl_trustStoreLocation", "value":"/var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/agent_inst/config/security/plugins/certificates/AgentTrust.jks" },
    { "name":"ssl_trustStorePassword", "value":"xxxxxxx" }
  ]
}

- Change file permission of /tmp/agent_apicreds.json to 777 

As opc user, run the following command to register the credential file
cat /tmp/agent_apicreds.json | sudo -u oracle-cloud-agent /var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/agent_inst/bin/credential_mgmt.sh -o upsertCredentials -s logan

- List the credential after register the credentials

sudo -u oracle-cloud-agent /var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/agent_inst/bin/credential_mgmt.sh -o listCredentials -s logan

## Deploy Log Sources and Parsers for the ZFS Storage Appliance metrics and log data

- Download the ZFS related Log Sources and Parsers from the Oracle GitHub knowledge content [here](https://github.com/oracle-quickstart/oci-o11y-solutions/tree/main/knowledge-content/zfs/log-sources).
- Navigation Menu, and go to **Observability and Management**
- Navigate to **Logging Analytics** -> **Administration**
- In **Administration Overview** page, select **Import Configuration Content**

![ZFS Storage Appliance Log Source Import into Logging Analytics](/images/posts/2025-blogs/blog-oci_database_info_listdatabases_review_and_add.png)

Figure 5. ZFS Storage Appliance Log Source Import into Logging Analytics

- Drop the log source zip files downloaded to import configuration content
- Click **Import** to import the Log Sources
    
- Verify the newly imported log sources by going to sources menu
    
- Select the **Log Source**(eg. ZFS_audit_log_source), click **Edit** within the log source to update the **REST API log endpoint**
    
- Replace the **Log URL** with the actual ZFS Storage Appliance console URL
    

![Update the ZFS Monitoring Log Source endpoint URL](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 6. Update the ZFS Monitoring Log Source endpoint URL

- **Validate** and **Save changes**
- **Save Changes** for the Log Source
    

## Add Log Source Association for the Entity

The Entity will be Host(Linux) entity type, the client host entity type needs to match the Log Source Entity Type. The Host Linux entity can be a standalone VM which has the Oracle Management Agent installed or it can be a host VM where you have the ZFS NFS shares mounted. 

- In **Log Source** page, select **Unassociated Entities** from the Resources menu
- Click the check box of the host VM
- Click **Add association**
- Verify the associated entity
- ![Logging Analytics Log Source association for the Host Linux Entity](/images/posts/2025-blogs/blog-oci_database_info_entity_association.png)
    
    Figure 7. Logging Analytics Log Source association for the Host Linux Entity
    
    

## Deploy ZFS Storage Appliance Monitoring Dashboard

- Download the **ZFS Storage Appliance Monitoring Dashboard** from the Oracle GitHub knowledge content [here](https://github.com/oracle-quickstart/oci-o11y-solutions/tree/main/knowledge-content/zfs/dashboards).
- Navigation Menu, and go to **Observability and Management**
- Select **Logging Analytics Dashbobard Overview** sub menu
- Click **Import dashboards**
- Select the downloaded dashboard json file to be imported
- Dashboard should be listed in the dashboard overview page

## Application Performance Monitoring - Synthetic Monitoring

The ZFS UI console is an essential tool for managing your ZFS appliance. with the synthetic moniotring feature of Application Performance Monitoring, you can run scheduled monitors to ensure the console availability and gauge its responsiveness. You can create different types of monitors, but for the purpose of this blog, we created 2 monitors:

1. A "Browser" type monitor for monitoring the availability and response time of the console home page. No login is needed for this monitor.
2. A REST type monitor for monitoring for monitoring the availability and response time of the ZFS Cluster Configuration page of the console. We configured this monitor to login to the console in order to navigate to the desired page.

Once the monitors are created and enabled, you can examine various metrics on the monitor home page. You can also create an alarm on any metric as needed. We selected a few key metrics to show on the ZFS Storage Appliance Monitoring dashboard:

![ZFS Console Monitoring](/images/posts/2025-blogs/blog-oci_db_backup_metrics_explorer.png)

Figure 8. ZFS Console Monitoring

**Create and configure your monitors**

Following are the instructions to create a Browser type and a REST type monitors. Details on how to create these and other types of monitors are in the documentation [here](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/create-monitor.html). We'll list below the fields specific to the ZFS console monitoring.

  
**Configure a Browser Monitor for the ZFS Console**

- Name: ZFS_Console_Browser_Monitor.
- Type: Browser.
- Base URL: https://<IP address>:215/#status/dashboard.
- Select any of the remaining options on the page per the details in the documentation.
- Click Next.
- Choose your dedicated vantage point (or any of the Oracle vantage points if your URL is accessible externally).
- Select any of the remaining options on the page per the details in the documentation.
- Click Next.
- Enable Availability Configuration.
- Click Next.
- Optionally, add tags to organize your resources.
- Click Next.
- Review and Save your monitor.

**Configure a REST Monitor for the ClusterConfig page**

- Name: ZFS_Console_ClusterConfig_REST_Monitor.
- Type: REST.
- Base URL: https://<IP address>:215/#configuration/cluster
- Request Configuration Method: GET
- Authentication: Fill in as appropriate for your environment.
- Select any of the remaining options on the page per the details in the documentation.
- The remaining screens are similar to those in the Browser type monitor.
- Review and Save your monitor.

![ZFS_Console_Browser_Monitor](/images/posts/2025-blogs/blog-oci_db_backup_metrics_explorer.png)

Figure 9. ZFS Console Browser Monitor

![ZFS_Console_ClusterConfig_REST_Monitor](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 10. ZFS Console ClusterConfig REST Monitor

You can click on the "History" link in the left handside navigation bar and select one of th rows. In the 3-dot menu on the right, click "View HAR" to see the HTTP Archive file of this run:

![REST_API_HAR_File](/images/posts/2025-blogs/blog-oci_database_info_log_explorer.png)

Figure 11. REST API HAR File

# Conclusion

Enhancing the observability and monitoring of the Oracle ZFS Storage Appliance is essential for organizations seeking to optimize their storage infrastructure. By integrating Oracle Cloud Infrastructure services such as Logging Analytics, Stack Monitoring, and Monitoring Service, businesses can achieve a unified and comprehensive monitoring solution. This integration enables deeper insights into system performance, proactive issue detection, and streamlined operations. Implementing these advanced monitoring capabilities ensures that critical components—from OCI Audit logs to NFS mount points—are continuously monitored and analyzed. This not only improves system reliability and availability but also supports informed decision-making and efficient resource management.

As data volumes grow and storage technologies evolve, adopting robust monitoring strategies becomes increasingly important. Organizations that leverage these OCI services position themselves to maintain high performance, reduce downtime, and enhance overall operational efficiency. We encourage businesses to explore these integration opportunities to fully realize the benefits of their Oracle ZFS Storage Appliances. By doing so, they can ensure their storage infrastructure remains resilient, efficient, and aligned with their strategic objectives.

# Reference

[Oracle ZFS Storage Appliance RESTful API Guide](http://https://docs.oracle.com/cd/E79446_01/html/E79460/goqri.html#scrolltoc)

[Logging Analytics Set up REST API Log Collection](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/set-rest-api-log-collection.html)

[Management Agent Source Credential](https://docs.oracle.com/en-us/iaas/management-agents/doc/management-agents-administration-tasks.html#OCIAG-GUID-53567BB0-60B9-40DF-BB6A-A24BF825046F)

[OCI Logging Analytics: Collect Logs Using REST API Collection Method](https://www.ateam-oracle.com/post/oci-logging-analytics-collect-logs-using-rest-api-collection-method)

[OCI Application Performance Monitoring Synthetic Monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/use-synthetic-monitoring.html) 

[OCI Stack Monitoring Metric Extension](https://docs.oracle.com/en-us/iaas/stack-monitoring/doc/metric-extensions.html)

[Oracle ZFS Storage Appliance Administration Guide](https://docs.oracle.com/cd/E37831_01/html/E52872/configuration__services__nfs__logs.html)

Oracle ZFS Storage Appliance: SSL certificate problem, Self Signed Certificate in Certificate Chain (Doc ID 2563930.1)

​