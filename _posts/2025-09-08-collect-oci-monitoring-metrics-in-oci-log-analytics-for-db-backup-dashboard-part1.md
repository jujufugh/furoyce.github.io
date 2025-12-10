---
title: "Collecting OCI Monitoring Metrics in OCI Log Analytics for Database Backup Dashboard - Part 1"
date: 2025-09-08
last_modified_at: 2025-09-08T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - Database Backup
  - OCI Log Analytics
  - Cloud Database
---

## Introduction

Monitoring the health and compliance of your Oracle Cloud Infrastructure (OCI) databases requires visibility into key operational metrics such as backup and patching status. While OCI exposes this information through its comprehensive REST APIs, aggregating and analyzing these metrics across a fleet of databases can be complex and time-consuming. In this blog post, we’ll show you how to leverage Oracle Log Analytics’ REST API Log Source to automatically collect database metadata, enabling you to build centralized dashboards for real-time and historical insights into your backup and patching operations.

## Solution Design

Oracle Database Backup and Recovery information is available from three areas: 

- Recovery Service metrics are available from OCI Monitoring service metrics
- Database backup information is available from the OCI Database service REST API

Oracle Log Analytics enables you to collect OCI Monitoring metrics by configuring a REST API Log Source that queries the OCI Monitoring service endpoints. This approach allows you to ingest time-series metrics such as backup job status, backup duration, and success/failure rates directly into Log Analytics for centralized analysis and dashboarding.

Reference Architecture: 

![Reference Architecture for Database Backup and Recovery](/images/posts/2025-oci-backup/blog-oci_db_backup_recovery_ref_architecture.png)

*Figure 1: Reference Architecture showing the flow of Database Backup and Recovery from OCI Monitoring and OCI REST API to OCI Log Analytics*


In the part 1 of the blog series, we will go over the details of collecting OCI monitoring metrics into Log Analytics. We'll implement a comprehensive monitoring solution that combines both OCI Monitoring metrics and Database service API data to provide complete visibility into database backup and recovery operations. This approach allows us to:

- **Collect Recovery Service Metrics**: Leverage OCI Monitoring service to gather metrics about backup job status, success rates, and performance indicators
- **Gather Database Metadata**: Use Database service REST APIs to collect detailed information about database configurations, backup policies, and current status
- **Centralized Analysis**: Aggregate all data in Oracle Log Analytics for unified dashboards and historical trend analysis

### How It Works

- **REST API Log Source**: You define a Log Source in Log Analytics that periodically calls the OCI Monitoring REST API endpoint (e.g., `/20180401/metrics`) to fetch the latest metrics for your databases.
- **Management Agent**: The Oracle Management Agent, running on a VM or as a plugin, acts as the collector and authenticates using resource principal or instance principal.
- **Data Ingestion**: The collected metrics are parsed and ingested into Log Analytics, where you can build dashboards, set up alerts, and perform historical analysis.

### Prerequisites

- Set up service policies for Oracle Cloud Log Analytics. See [Enable Access to Log Analytics and Its Resources](https://docs.oracle.com/iaas/logging-analytics/doc/enable-access-logging-analytics-and-its-resources.html) and Prerequisite IAM Policies in Oracle Cloud Infrastructure Documentation.
- Install the [Management Agent](https://docs.oracle.com/en-us/iaas/management-agents/doc/install-management-agent.html) on a client host VM which has http or https access to your endpoint server, we will use this host for Log Source entity association. See [Set Up Continuous Log Collection From Your Hosts](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/set-continuous-log-collection-form-your-hosts.html#GUID-310D58A5-9F27-48C9-AE62-009BD094AB69).
- On Unix-based hosts, the user that installs management agent is mgmt_agent for the [manually installed management agent](https://docs.oracle.com/en-us/iaas/management-agents/doc/install-management-agent-manually.html), and oracle-cloud-agent when the management agent is a plugin enabled with [Oracle Cloud Agent](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/manage-plugins.htm).

## Implementation Overview

Let's walk through the implementation process for collecting historical OCI audit logs using the REST API ingestion method.

* Create a dynamic group for the Management Agent to enable resource principal authentication
* Configure IAM policies to grant the dynamic group access to audit logs and Log Analytics resources
* Create a host entity in Log Analytics to represent the Management Agent
* Configure a custom log source and parser for historical OCI audit logs
* Associate the Management Agent with the log source using resource principal authentication
* Verify Ingestion and Use Security Fundamentals Dashboards

### Step 1: Create dynmaic group for the Management Agent

1. Create Dynamic Group for the Management Agent installed on the VM or enabled via Oracle Cloud Agent:
   - Navigate to the OCI Console
   - Go to Identity & Security > Domains > Default domain > Dynamic Groups
   - Click **Create Dynamic Group**
   - Enter a name (e.g., **ManagementAgentDynamicGroup**)
   - Enter a description (e.g., **Dynamic group for Management Agents in specific compartment**)
   - In the matching rules section, add the following rule:
     ```
     ALL {resource.type='managementagent', resource.compartment.id='ocid1.compartment.oc1..aaaaaa[REDACTED]'}
     ```
   - Click **Create**

2. Create OCI policy for management agent dynamic group resource principal
   - Navigate to the OCI Console
   - Go to Identity & Security > Policies
   - Click **Create Policy**
   - Enter a name (e.g., **ManagementAgentAuditLogPolicy**)
   - Enter a description (e.g., **Policy to allow Management Agent to read audit logs and manage log groups**)
   - Select the compartment (typically the root compartment or tenancy)
   - In the policy builder section, add the following policy statements:
     ```
      allow dynamic-group ManagementAgentDynamicGroup to manage log-groups in tenancy
      allow dynamic-group ManagementAgentDynamicGroup to use log-content in tenancy
      allow dynamic-group ManagementAgentDynamicGroup to {AUDIT_EVENT_READ} in tenancy
      allow dynamic-group ManagementAgentDynamicGroup to use metrics in tenancy
      allow dynamic-group ManagementAgentDynamicGroup to {LOG_ANALYTICS_LOG_GROUP_UPLOAD_LOGS} in tenancy

     ```
   - Click **Create**

   Note: The policy statements above use the dynamic group name **ManagementAgentDynamicGroup** that we created in the previous step. These policies grant the necessary permissions for the Management Agent to read audit logs and manage log groups within the tenancy.


### Step 2: Update the Agent Configuration 

To enable the Management Agent to use the REST API for log collection, you need to update its configuration properties:

1. SSH to the VM host where the Management Agent is installed:
   ```
   ssh opc@<your-vm-ip-address>
   ```

2. Switch to the root user:
   ```
   sudo su -
   ```

3. Navigate to the agent configuration directory:
   - If you're using Oracle Cloud Agent:
     ```
     cd /var/lib/oracle-cloud-agent/plugins/oci-managementagent/polaris/agent_inst/config/
     ```
   
   - If you manually installed the Management Agent (standalone installation):
     ```
     cd /opt/oracle/mgmt_agent/agent_inst/config
     ```

4. Open the emd.properties file for editing:
   ```
   vi emd.properties
   ```

5. Append the following two parameters to the bottom of the file:
   ```
   loganalytics.rest_api.enable_oci_api=true
   loganalytics.rest_api.report_interval=600
   ```

   Note: The `loganalytics.rest_api.report_interval` parameter sets the collection interval in seconds. The default is 300 seconds (5 minutes), but in this example, we've set it to 600 seconds (10 minutes). You can adjust this value based on your requirements.

6. Save the file and exit the editor.

7. Restart the Management Agent to apply the changes.
   
   - If you're using Oracle Cloud Agent:
      ```
      systemctl restart oracle-cloud-agent
      ```
   
   -  If you manually installed the Management Agent (standalone installation):
      ```
      systemctl restart mgmt_agent
      ```

### Step 3: Verify the Monitoring Metrics in OCI Monitoring Metrics Explorer

1. Navigate to OCI Monitoring > Metrics Explorer
2. Select the Metrics Namespace: **oracle_oci_database**
**NOTE**: **oracle_oci_database** metric namespace is ONLY available when you enable OCI Database Management Service for your database.
3. Select the Metrics: **BackupSize** or **BackupDuration**
4. Click **Update Chart**
5. Verify the metrics are being collected

![OCI Monitoring Metrics Explorer](/images/posts/2025-oci-backup/blog-oci_db_backup_metrics_explorer.png)

*Figure 2: Verify the Monitoring Metrics in OCI Monitoring Metrics Explorer*

Or you can use the Advanced Mode to create a custom chart with the metrics via the MQL (Monitoring Query Language) query.

![OCI Monitoring Metrics Explorer](/images/posts/2025-oci-backup/blog-oci_db_backup_metrics_explorer_mql.png)

*Figure 3: Verify the Monitoring Metrics in OCI Monitoring Metrics Explorer*

### Step 4: Configure the REST API Source for OCI Monitoring Service and Autonomous Recovery Service REST API endpoint

- OCI Monitoring Service REST API endpoint

**NOTE**: The OCI Monitoring Service REST API endpoint reference doc: [OCI Monitoring Service REST API](https://docs.oracle.com/en-us/iaas/api/#/en/monitoring/20180401/).

1. **Access Log Analytics Administration Console**
   - Log in to the Oracle Cloud Console.
   - Navigate to **Observability & Management** > **Log Analytics**.
   - Click on the **Administration** tab.

2. **Create a New Log Source**
   - In the left navigation pane, select **Sources**.
   - Click **Create Source**.

3. **Configure Source Details**
   - **Name**: Enter a descriptive name for your source (e.g., "OCI_Backup_Duration"). 
   - **(Optional)** Download OCI_Backup_Duration example log source from Github repo: [here](https://github.com/jujufugh/oci-o11y-solutions/blob/main/knowledge-content/oracle-database/backup-duration/log-sources/OCI_Backup_Duration_1757371121751.zip), and import the Log Source by following the [doc](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/import-configuration-content.html).
   - **Source Type**: Select **REST API**.
   - **Entity Type**: Choose "Host(Linux)" as the Entity Type.
   - **Parser**: Select "OCI_Backup_Duration" as the Parser.

4. **Define REST API Endpoint**
   - In the **Endpoints** tab, click **Add log endpoint**.
   - Enter a name for the endpoint: **db backup duration endpoint**
   - Enter the Log URL for the OCI Monitoring Service endpoint you want to collect metrics from.
     - Example for OCI Monitoring Service SummarizeMetricsData endpoint:
       ```
       https://telemetry.us-ashburn-1.oraclecloud.com/20180401/metrics/actions/summarizeMetricsData?compartmentId={COMPARTMENT_ID}
       ```
   - Request content type: **JSON**
   - HTTP Method: **POST**
   - Request headers
     - **Accept: application/json**
   - Credentials
     - **Log credentials type: None**
   - POST Payload: 
      ```
      {
        "namespace": "oracle_oci_database",
        "startTime": "{CURR_TIME-10m:yyyy-MM-dd'T'HH:mm:00.000}Z",
        "endTime": "{CURR_TIME:yyyy-MM-dd'T'HH:mm:00.000}Z",
        "query": "BackupDuration[1h].groupBy(resourceName,deviceType).mean()"
      }

   ![OCI Backup Duration Logs Source Configuration](/images/posts/2025-oci-backup/blog-oci_db_backup_duration_logs_source_config.png)

   *Figure 4: Configure the OCI Backup Duration logs source settings*

4. **Validate** configuration and click **Save changes**

- Autonomous Recovery Service REST API endpoint
To create an OCI Log Analytics REST API-based log source, follow these steps:

1. **Access Log Analytics Administration Console**
   - Log in to the Oracle Cloud Console.
   - Navigate to **Observability & Management** > **Log Analytics**.
   - Click on the **Administration** tab.

2. **Create a New Log Source**
   - In the left navigation pane, select **Sources**.
   - Click **Create Source**.

3. **Configure Source Details**
   - **Name**: Enter a descriptive name for your source (e.g., "OCI_DB_recovery_Logs").
   - **(Optional)** Download OCI_Backup_Duration example log source from Github repo: [here](https://github.com/jujufugh/oci-o11y-solutions/blob/main/knowledge-content/oracle-database/recovery/log-sources/OCI_DB_recovery_Logs_1757371175920.zip), and import the Log Source by following the [doc](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/import-configuration-content.html).
   - **Source Type**: Select **REST API**.
   - **Entity Type**: Choose "Host(Linux)" as the Entity Type.
   - **Parser**: Select "OCI_DB_Recovery_Logs" as the Parser.

   ![OCI DB Recovery Logs Source Configuration](/images/posts/2025-oci-backup/blog-oci_db_recovery_logs_source_config.png)
   *Figure 5: Configure the OCI DB recovery logs source settings*

4. **Define REST API Endpoint**
   - In the **Endpoints** tab, click **Add log endpoint**.
   - Enter a name for the endpoint: **db recovery endpoint**
   - Enter the Log URL for the OCI Recovery Service endpoint you want to collect logs from.
     - Example for listing protected databases:
       ```
       https://recovery.us-ashburn-1.oci.oraclecloud.com/20210216/protectedDatabases?compartmentId={COMPARTMENT_ID}
       ```
   - Request headers
     - **Accept: application/json**
   - Credentials
     - **Log credentials type: None**

   ![OCI DB Recovery Logs Source Configuration](/images/posts/2025-oci-backup/blog-oci_db_recovery_logs_source_config2.png)
   *Figure 6: Configure the OCI DB recovery logs source settings*

5. **Validate** configuration and click **Save changes**

### Step 5: Associate the Management Agent with the log source

1. Navigate to Log Analytics > Administration > Sources
2. Select Log Source **OCI_Backup_Duration**
3. Select the **Unassociated Entities** menu
4. Select your Management Agent host entity
5. Click **Add Association**
6. Verify the **Management Agent** information is displayed
6. In the **Log Group** section, select an existing log group or create a new one for your log source data
6. Click **Submit** to finalize the association

![OCI Backup Duration Logs Source Association](/images/posts/2025-oci-backup/blog-oci_db_backup_duration_logs_source_association.png)

*Figure 7: Associate the Management Agent host entity with the OCI_Backup_Duration log source and configure log group*

### Step 6: Use Log Analytics query language to get backup and recovery insights

1. Navigate to Log Analytics > Log Explorer
3. Enter the following query as a example: 
```
'Log Source' = OCI_Backup_Duration | link 'OCI Resource Name', BackupDestinationType, Metric_Value
```
4. Click **Run**
5. Verify the query results

![OCI Backup Duration query results](/images/posts/2025-oci-backup/blog-oci_db_backup_duration_query_results.png)

*Figure 8: OCI Backup Duration query results*

## Conclusion

By ingesting OCI Monitoring metrics data into Log Analytics using the REST API Source approach, organizations can transform their observability strategy through several key value propositions:

### Unified Data Platform
The integration creates a single pane of glass where metrics data becomes searchable, filterable log entries. This transformation enables teams to apply Log Analytics' advanced query capabilities to time-series data, breaking down traditional silos between metrics and logs monitoring.

### Dimensional Data Enrichment
OCI Monitoring metrics contain rich dimensional information (resourceName, deviceType, compartmentId, etc.) that becomes fully exploitable when converted to log format. Users can:
- Create custom fields from metric dimensions
- Build dynamic filters based on resource attributes  
- Perform granular analysis across multiple dimension combinations
- Generate insights that aren't readily available in standard metrics dashboards

### Cross-Domain Correlation
The most significant advantage lies in correlating metrics with operational data streams:
- **Performance Analysis**: Link database backup duration spikes with system resource contention logs
- **Root Cause Analysis**: Correlate backup failures with infrastructure events, application errors, and audit activities
- **Predictive Insights**: Identify patterns between backup performance degradation and preceding system anomalies
- **Compliance Reporting**: Combine backup SLA metrics with audit logs for comprehensive governance dashboards

### Operational Intelligence at Scale
This approach enables advanced analytics scenarios:
- Historical trend analysis using Log Analytics' extended retention capabilities
- Custom alerting rules that consider both metrics thresholds and log event patterns
- Machine learning-ready datasets that combine structured metrics with unstructured log data
- Automated incident response workflows triggered by correlated metrics and log events

The result is a comprehensive observability ecosystem where OCI database operations become fully transparent, predictable, and optimizable through data-driven insights.

## References

1. [Oracle Log Analytics REST API Documentation](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/set-rest-api-log-collection.html)
2. [OCI Database Service API Documentation](https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/)
3. [OCI Log Analytics Dashboard Creation Guide](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/create-dashboard.html) 




