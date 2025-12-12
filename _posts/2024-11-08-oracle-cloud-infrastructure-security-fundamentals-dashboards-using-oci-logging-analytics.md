---
title: "Oracle Cloud Infrastructure Security Fundamentals Dashboards using OCI Logging Analytics"
date: 2024-11-08
last_modified_at: 2024-11-08T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - Security
  - OCI Log Analytics
---

# Introduction

Oracle Cloud Infrastructure(OCI) and services provide effective and manageable security that enables you to run your mission-critical workloads and to store your data with confidence. To achieve cloud security operational excellence, it is crucial to continuously monitor and improve the security posture of our customers' OCI tenancy and adopt essential cyber hygiene practices. For our customers navigating the dynamic cloud security landscape without a dedicated Security Information and Event Management (SIEM) system, the Security Fundamentals Dashboards are set to support our customers to build and maintain strong security observability and governance around the OCI cloud resources so that our customers can stay vigilant in an ever-evolving cyber landscape. The Security Fundamentals Dashboards proactively aggregate and analyze OCI logs related to security events by leveraging the advanced capabilities of OCI Logging Analytics, coupled with near real-time monitoring and alerting allows security operations teams to detect security risks faster, focus on the key information based upon the tuning of the systems, and take appropriate actions to mitigate the risks.

# Dashboard Artifacts

The first release of the Security Fundamentals Dashboards contains following three dashboards:

- Identity Security Dashboard
- Network Security Dashboard
- Security Operations Dashboard

The code is available [here](https://github.com/oracle-quickstart/oci-o11y-solutions/tree/main/knowledge-content/MAP/security-fundamentals-dashboards) and is provided as sample code for reference. The sample code can be customized for additional enhancements.

# Security Fundamentals Dashboards Details

- Out-of-Box dashboards for rapid security threats detection
- Designed for customers interested in observing critical security events in their tenancies
- Dashboards are based on Oracle security analytics and monitoring best practices
- The dashboards query data from the OCI native Audit and Network related Logs(VCN Flow Logs, Load Balancer Logs, WAF Logs, Network Firewall Logs) for continuous Identity and Network security events monitoring
- Meets the Maturity Acceleration Program-Foundation (MAP-F) capabilities related to Logging Monitoring and Alerting and provide visibility into key security metrics
- Observability and Management Logging Analytics is the main service for the solution
- Consumption is based on the size and retention of the underlying logs

Note: OCI Maturity Acceleration Program-Foundation (MAP-F) is a collaborative customer engagement that seeks to help organizations in building, deploying, and maintaining their foundational security capabilities, to support secure operations in OCI.

Dashboards Screenshots:

![Security Fundamentals Dashboards - Identity Security](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 1. Security Fundamentals Dashboards - Identity Security - part 1

![Security Fundamentals Dashboards - Identity Security](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 2. Security Fundamentals Dashboards - Identity Security - part 2

![Security Fundamentals Dashboards - Network Security](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 3. Security Fundamentals Dashboards - Network Security

![Security Fundamentals Dashboards - Security Operations Dashboard](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 4. Security Fundamentals Dashboards - Security Operations Dashboard

Security Fundamentals Dashboards Widgets:

|Category|Widgets|Description|
|---|---|---|
|IAM|User Password reset|Bar Chart showing count of successful Local Password resets aggregated over 1 day.|
|---|---|---|
|IAM|User Creation|Bar Chart showing count of successful or unsuccessful  Local User creations aggregated over 1 day.|
|---|---|---|
|IAM|User Changes|Bar Chart showing count of successful or unsuccessful  Local User changes aggregated over 1 day. This includes Deactivate User, Delete User, Update User, Update User Capabilities, Update User State, Update User Password via UI|
|---|---|---|
|IAM|Dormant Users|Tile showing count of dormant users that haven't successfully logged in to the OCI console within the last 30 days|
|---|---|---|
|IAM|Group Changes|Bar Chart showing count of successful or unsuccessful Local group changes aggregated over 1 day. This includes "Add user to group" and "Remove user from group"|
|---|---|---|
|IAM|IAM Policy Update|Bar Chart showing count of successful or unsuccessful IAM policy changes across the tenancy aggregated over 1 day. This includes Create Policy, Update Policy, Delete Policy.|
|---|---|---|
|IAM|IDP Group mapping update|Bar Chart showing count of successful or unsuccessful IDP group mapping change across the tenancy aggregated over 1 day. This includes "Add user to idpgroup", "Remove user from idpgroup", "Create idpgroup mapping", "Delete idpgroup mapping, "Update idpgroup mapping"|
|---|---|---|
|IAM|IDP Changes|Bar Chart showing count of successful or unsuccessful Identity Provider changes across the tenancy aggregated over 1 day. This includes Create, Update , Delete IDP.|
|---|---|---|
|IAM|Successful Logins|Bar Chart showing count of successful Local Logins aggregated over 1 day.|
|---|---|---|
|IAM|Failed Logins|Bar Chart showing count of unsuccessful Local Logins aggregated over 1 day. This includes failed login due to wrong password or disabled user.|
|---|---|---|
|IAM|API Key Creation|Bar Chart showing count of successful or unsuccessful API key creations(additions to a user) aggregated over 1 day.|
|---|---|---|
|IAM|Top Identity Events Producers|Pie Chart identifying the top producers of Identity related audit events. Internal users and services have been filtered out. Otherwise the result could be skewed heavily.|
|---|---|---|
|Network|Total Network Traffic|Graph showing the total network traffic across all VCN Flow logs. Aggregated over 5 mins spans and shown in KB.|
|---|---|---|
|Network|Network Ingress Traffic from Public|Graph showing the total Ingress network traffic across all VCN Flow logs originating from a Public IP. Aggregated over 5 mins spans and shown in KB.|
|---|---|---|
|Network|Security list changes|Bar Chart showing any changes to Security Lists in the tenancy. This includes create, delete and updates to security lists and rules.|
|---|---|---|
|Network|NSG changes|Bar Chart showing any changes to Network Security Groups in the tenancy. This includes create, delete and updates to Network Security Groups.|
|---|---|---|
|Network|Changes to Gateways|Bar Chart showing any changes to Gateways in the tenancy. This includes create, update and delete of DRGs, NAT GW, IGW, SGW and Peering Gateways|
|---|---|---|
|Network|Threat IPs - Timeline|Graph showing the count of Threat IPs over time across Flow logs and the OCI Audit log from both egress and ingress traffic.|
|---|---|---|
|Operations|Data freshness|Time stats showing the last collection time for Audit and Flowlogs. The number should be small typically < 3 mins.|
|---|---|---|
|Operations|Service Connector errors|Based on the Service Connector Hub metric namespace and showing errors related to reading from OCI Logging(Source), writing to Logging Analytics(Target) and Service Connector Errors.|
|---|---|---|
|Operations|Logging Analytics Active Storage Used(GB)|Based on the metrics of the Logging Analytics service details for the total size used in the Logging Analytics Active Storage Unit for ingested log data|
|---|---|---|
|Operations|Logging Analytics Archival Storage Used|Based on the metrics of Logging Analytics service details for the total size used in the Logging Analytics Archival Storage Unit for ingested log data|
|---|---|---|

## Security Fundamentals Dashboards Onboarding

Logging Analytics should be set up in your tenancy 

- [Logging Analytics](https://docs.oracle.com/en-us/iaas/logging-analytics/index.html)

Configure Logging Analytics

- [Configure Your Service](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/configure-your-service.html)
- [Prerequisite IAM Policies](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/prerequisite-iam-policies.html)
- [Enable Access to Logging Analytics and Its Resources](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/enable-access-logging-analytics-and-its-resources.html)

## Audit and Network Logs Ingestion

- [Ingest OCI VCN Flow Logs into OCI Logging Analytics](https://blogs.oracle.com/observability/post/how-to-ingest-oci-vcn-flow-logs-into-oci-logging-analytics)
    
- [Ingest OCI Audit logs into OCI Logging Analytics](https://redthunder.blog/2021/06/01/getting-insights-with-oci-audit-log-with-logging-analytics-via-service-connector/)

Logging Analytics is integrated with Oracle Threat Intelligence to automatically receive the threat feed as the logs are ingested. The feature is available for all the log sources in the regions where both Logging Analytics and Oracle Threat Intelligence services are enabled. The Threat IPs widget makes use of this feature, which is not enabled by default. 

To enable:

1. In OCI console, Navigate to **Observability and Management** -> **Logging Analytics** -> **Administration**
2. Click on **Sources**. in search box in the top right, search for “**vcn**”. You should get 2 sources: **OCI VCN Flow Logs** and **OCI VCN Flow Unified Schema Logs**
3. Edit each source. On the Edit screen, click the **Field Enrichment** tab. Ensure the **Enabled** checkbox is checked for the **Geo location** function
4. Edit the **Geo location** function by clicking the three dots, and check **Threat Intelligence Enrichment** checkbox. 
5. If it is not, check the checkbox and click **Save Changes**
6. Repeat above 5 steps for **OCI Network Firewall Traffic Logs**, **OCI Network Firewall Threat Logs**, **OCI Load Balancer Access Logs**, **OCI Load Balancer Error Logs**, **OCI WAF Logs**, **OCI Audit Logs** Sources. 

## Security Fundamentals Dashboards Deployment using OCI Marketplace App

Security Fundamentals Dashboards (SFD) OCI Marketplace App offers a seamless, one-click solution for customers to effortlessly deploy SFD dashboards and automate the collection of essential security-related logs in Logging Analytics. This streamlined approach simplifies the setup of comprehensive security monitoring across OCI environments, empowering customers to enhance their cloud security posture with minimal effort.

To launch the Marketplace app:

- In OCI console, Navigate to **Marketplace** -> **All Applications**
- Search “**Security Fundamentals Dashboards**”
- Check **I have reviewed and accept the Oracle standard Terms and Restrictions.**
- ![Figure 5. Security Fundamentals Dashboards Marketplace App](/images/posts/2025-blogs/blog-oci_database_info_listdatabases_review_and_add.png)
    
    Figure 5. Security Fundamentals Dashboards Marketplace App
    
    
- Click **Launch Stack**
- Review the Stack Information and Click **Next**
- Select the **Dashboard Compartment** from the dropdown to deploy the dashboards
- Check **Create Service Connector for IAM Identity Domain Audit?**
- Update the Logging Analytics Log Group Name if needed
- Switch **Service Connector Hub State** from INACTIVE to ACTIVE
- Check **Include Network Related Logs?** checkbox
- Add the Logging service Network related logs Log Group OCIDs 
- Click **Next** for the final Review, Click **Create** to run the stack 
- ![Figure 6. Security Fundamentals Dashboards Launch the Stack](/images/posts/2025-blogs/blog-oci_database_info_listdatabases_review_and_add.png)
    
    Figure 6. Security Fundamentals Dashboards Launch the Stack
    
    

## Manual Deployment of Security Fundamentals Dashboards

The required files for the security dashboards are stored in the following GitHub repo:

[https://github.com/oracle-quickstart/oci-o11y-solutions/tree/main/knowledge-content/MAP/security-fundamentals-dashboards](https://github.com/oracle-quickstart/oci-o11y-solutions/tree/main/knowledge-content/MAP/security-fundamentals-dashboards)

Download the files to your local workstation. There are 3 files with “.json” extension corresponding to the 3 security dashboards

1. Identity Security: Identity Security.json
2. Network Security: Network Security.json
3. Security Operations: Security Operations.json

Follow these steps to import the JSON files:

1. Login to tenancy
2. Navigate to LA Dashboards Console -> Observability & Management -> Logging Analytics -> Dashboards
3. Click on “Import Dashboards”
4. Navigate to folder containing dashboards and select the first dashboard JSON file
5. Select “Specify a compartment for all dashboards” and choose compartment
6. Select “Specify a compartment for all saved searches” and choose compartment
7. Click on “Import”
8. Repeat steps 3-7 for the second JSON file
9. (Optional) Follow the above steps to enable the Threat Intelligence service integration with Logging Analytics

It may take some time for the data to start flowing into the dashboard. You will not see any data unless there are activities on the target system(s) that would be picked up by the corresponding widget/query.

### Security Fundamentals Dashboards Visulization

You can now use Security Fundamentals Dashboards to detect security threats and issues in your OCI tenany. For example, Threat IPs detected in VCN Flow Logs accessing OCI cloud resources or spikes detected in Network Ingress Traffic from Public IPs need further investigation from the security teams to mitigate security risks across your tenancy. 

![Security Analytics Dashboards - Threat IPs Widget](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

![Security Analytics Dashboards - Network Ingress Traffic from Public Widget](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

# Conclusion

Security Fundamentals Dashboards provide a great starting point to monitor security events using Network logs and Audit logs via Logging Analytics for our OCI customers. By leveraging these OCI features, organizations can gain valuable insights into their OCI security posture, and make informed decisions to secure and manage cloud resources.

Sign up for an [Oracle Cloud Infrastructure free trial account](https://www.oracle.com/cloud/free/) today to try out new Oracle Cloud Infrastructure features!

# Further Reading

- [Elevating Network Security: Introducing New SFD Network Security Dashboard](https://www.ateam-oracle.com/post/elevating-network-security-introducing-new-sfd-network-security-dashboard)
- [Enable Logs for VCN Flow Logs](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/vcn-flow-logs-enable.htm#:~:text=Enable%20VCN%20Flow%20Logs%20for,balancers%2C%20or%20network%20load%20balancers.&text=Open%20the%20navigation%20menu%2C%20click,Click%20Enable%20flow%20logs.) 
- [Enable Logs for OCI Network Firewall Traffic Logs and Threat Logs](https://docs.oracle.com/en-us/iaas/Content/network-firewall/enable-logs.htm#:~:text=Enable%20the%20Oracle%20Cloud%20Infrastructure,Click%20Enable%20Service%20Log.)
- [Enable Logs for OCI Load Balancer Access Logs and Error Logs](https://docs.oracle.com/en-us/iaas/Content/Balance/Tasks/enable_log.htm)
- [Enable Logs for OCI Web Application Firewall](https://docs.oracle.com/en-us/iaas/Content/Logging/Reference/details_for_lbwaf.htm) 
- [Monitoring OCI Web Application Firewall (WAF) with Logging Analytics](https://blogs.oracle.com/observability/post/monitoring-oci-waf--la)
- [Logging Analytics - Configure Your Service](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/configure-your-service.html)
- [Logging Analytics - Prerequisite IAM Policies](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/prerequisite-iam-policies.html)
- [Logging Analytics - Enable Access to Logging Analytics and Its Resources](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/enable-access-logging-analytics-and-its-resources.html)

​