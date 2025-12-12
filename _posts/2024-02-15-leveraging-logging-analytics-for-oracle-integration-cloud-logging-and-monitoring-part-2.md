---
title: "Leveraging Logging Analytics for Oracle Integration Cloud Logging and Monitoring - Part 2"
date: 2024-02-15
last_modified_at: 2024-02-15T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - Oracle Integration Cloud
  - OCI Log Analytics
---

As more customers are onboarded to Oracle Cloud Infrastructure (OCI) and run their critical integrations between OCI cloud services. Having a robust observability and monitoring solution for Oracle Integration Cloud (OIC) is pivotal for ensuring the efficiency, reliability, and security of Oracle Integration solutions. It enables the organizations to maintain oversight over their integrations, diagnose issues promptly, and optimize performance.


 Oracle Integration Cloud is a fully managed, preconfigured environment that gives you the power to integrate your Oracle Cloud Infrastructure applications and services and on-premises applications. As more customers are onboarded to Oracle Cloud Infrastructure (OCI) and run their critical integrations between OCI cloud services. Having a robust observability and monitoring solution for Oracle Integration Cloud (OIC) is pivotal for ensuring the efficiency, reliability, and security of Oracle Integration solutions. It enables the organizations to maintain oversight over their integrations, diagnose issues promptly, and optimize performance. 

In the part 1 of the blog Leveraging Logging Analytics for Oracle Integration Cloud Logging and Monitoring, we talked about the observability and monitoring features for Oracle Integration Cloud (OIC). We can use the OIC metrics data, activitiy stream log data as well as ingesting the OIC Design Time Audit Log data into Logging Analytics to unlock the potential to transform raw OIC telemetry data into actionable insights so that we can maximize the operational intelligence and security posture of cloud integration environments. 

In this blog, we will deep dive into the details of the push method via OIC custom integration to ingest OIC Audit Logs into Logging Analytics.  

**Architecture Diagram**

![Figure 1. OIC Audit Log Ingestion Push Method Architecture Diagram](/images/posts/2025-blogs/oci_loganalytics_metrics_api_ref_architecture_oci.drawio.png)

Figure 1. OIC Audit Log Ingestion Push Method Architecture Diagram

**Integration connection details**

- Get OIC Audit Logs using OIC REST API endpoint (/ic/api/integration/v1/monitoring/auditRecords) and OAuth2.0 Client Credentials
- Stage the content of the OIC Audit Log into a stage file
- (Optional) Push OIC Audit Log stage file into Object Storage bucket using OCI API key
- Push OIC stage file to Logging Analytics via LA Log Upload REST API /20200601/namespaces/{namespaceName}/actions/uploadLogFile

## Step 1. Setup OAuth 2.0 Client Credentials for Oracle Integration Cloud instance

**Note: Beginning in March 2023, Oracle began a region-by-region migration of all tenancies to use identity domains. Tenancy owners will be notified two weeks prior to the migration of their tenancy. All IDCS instances in the tenancy will be converted at the same time regardless of the IDCS home region.**

Configure the OAuth Client Credentials (Required in OIC Gen3, basic authentication is no longer supported in Gen3 Oracle defined REST API endpoints)

### Determine Whether a Cloud Account Uses Identity Domains

To determine whether your cloud account uses identity domains, open the Oracle Cloud Infrastructure navigation menu, and click Identity & Security. Under Identity, check for Domains:

- If Domains is listed, then your cloud account uses identity domains. See [Set Up Users, Groups, and Policies in Cloud Accounts That Use Identity Domains](https://docs.oracle.com/en/cloud/paas/integration-cloud/oracle-integration-oci/henosis-setting-users-groups-and-policies-cloud-accounts-that-use-identity-domains.html).

![Figure 2. Determine Whether a Cloud Account Uses Identity Domains](/images/posts/2025-blogs/blog-oci_database_info_listdatabases_review_and_add.png)

Figure 2. Determine Whether a Cloud Account Uses Identity Domains

- If Domains is not listed, then your cloud account is still configured to link identities in IDCS and Oracle Cloud Infrastructure IAM using federation. See [Set Up Users, Groups, and Policies in Cloud Accounts That Do Not Use Identity Domains](https://docs.oracle.com/en/cloud/paas/integration-cloud/oracle-integration-oci/setting-users-groups-and-policies-cloud-accounts-that-do-not-use-identity-domains.html).

My cloud account uses the IDCS, so the following steps will be followed:

- [Understand Oracle Integration Federation](https://docs.oracle.com/en/cloud/paas/integration-cloud/oracle-integration-oci/understanding-oracle-integration-federation.html#GUID-4BDBF329-9DBA-4F45-9B9F-D0B7DBC45E7C "If your cloud account does not use identity domains, Oracle Cloud Infrastructure Identity and Access Management (IAM) must be federated with Oracle Identity Cloud Service (IDCS) for your tenancy.")
- [Create an IDCS Group](https://docs.oracle.com/en/cloud/paas/integration-cloud/oracle-integration-oci/creating-idcs-group.html "You can create Oracle Identity Cloud Service groups for later mapping them to Oracle Cloud Infrastructure Identity and Access Management identities.")
- [Create an IAM Group](https://docs.oracle.com/en/cloud/paas/integration-cloud/oracle-integration-oci/creating-iam-group.html "Create an instance administrator group in Oracle Cloud Infrastructure IAM and map it to your previously created IDCS group.")
- [Create an IAM Policy](https://docs.oracle.com/en/cloud/paas/integration-cloud/oracle-integration-oci/creating-iam-policy.html "Create a policy to grant permission to the users in a group to work with Oracle Integration instances within a specified tenancy or compartment.")
- [Map the IDCS and IAM Groups](https://docs.oracle.com/en/cloud/paas/integration-cloud/oracle-integration-oci/mapping-idcs-and-iam-groups.html "Map your instance administrator group in Oracle Cloud Infrastructure IAM to your previously created IDCS group.")
- [Create IDCS Users](https://docs.oracle.com/en/cloud/paas/integration-cloud/oracle-integration-oci/creating-idcs-users.html "You can create Oracle Identity Cloud Service users to add to Oracle Cloud Infrastructure IAM groups for specific access. To simplify access and permission management, grant permissions to groups instead of directly to users.")
- [Create IAM Users](https://docs.oracle.com/en/cloud/paas/integration-cloud/oracle-integration-oci/creating-iam-users.html "You can create Oracle Cloud Infrastructure Identity and Access Management (IAM) users for less typical user scenarios, such as emergency administrator access.")
- [Assign Oracle Integration Roles to Groups](https://docs.oracle.com/en/cloud/paas/integration-cloud/oracle-integration-oci/assigning-oic-roles-groups.html#GUID-B839F41C-445D-4137-8F2C-BF5CCBEC3D5C "After an Oracle Integration instance has been created, assign Oracle Integration roles to groups of users in Oracle Identity Cloud Service to allow them to work with the features of the Oracle Integration instance.")

Authentication and authorization in Oracle Integration is managed by Oracle Identity Cloud Service. Oracle Integration REST APIs as well as REST endpoints exposed in integrations are protected using OAuth token-based authentication.

Oracle Integration supports various OAuth authentication grant types, we will use the Client Credentials grant type to authenticate and get the authorization to Oracle Integration Cloud service. This type of authentication is used for applications which need to access its owner resources, not on behalf of a particular user. It is suitable for machine-to-machine communication where an application needs to access services or data without human interaction. You don't need to share usernames and passwords with clients or manage user passwords that expire.

### OAuth Client Credentials Flow

![Figure 3. OAuth 2.0 Client Credentials Flow Diagram](/images/posts/2025-blogs/oci_loganalytics_metrics_api_ref_architecture_oci.drawio.png)

Figure 3. OAuth 2.0 Client Credentials Flow Diagram

**Note: Oracle Integration Cloud also supports other OAuth authentication grant types, for instance, Authorization Code, JWT user Assertion.**

Oracle Integration REST APIs, integrations with REST adapters, and integrations with application adapters exposing REST endpoints are protected using OAuth.

- **The trusted application provides access to REST endpoints in Oracle Integration.** You register a trusted application with Oracle Identity Cloud Service for each Oracle Integration instance. This trusted application provides access to the OAuth protected REST endpoints in Oracle Integration.
- **Clients use the trusted application client ID and secret.** You provide clients with the client ID and client secret of your trusted application along with the Oracle Identity Cloud Service URL, and the Oracle Integration instance scope. The scope represents all the resources the trusted application can access. In the case of Oracle Integration, the scope provides access to all REST APIs and REST APIs exposed in integrations.
- **Clients get an access token.** With the information you provide clients, each client can request an authorization code and access token from Oracle Identity Cloud Service. The authorization code is short-lived. Once the client receives the authorization code, it exchanges the code for an access token. Each user has a different access token. The access token contains information about the client application and who the end user is.
- **Clients use the access token to access Oracle Integration REST APIs.** The client application uses the access token it received from Oracle Identity Cloud Service to call Oracle Integration REST APIs or REST endpoints exposed in integrations.
- **Clients can refresh expired access tokens.** If an access token expires, the client can refresh it. Access tokens expire after one hour by default, but you can change this in the trusted application configuration.
- **Identity Domain Administrators can revoke access tokens for users.** If security issues arise, you can revoke the access token for a specific user.

The OAuth Client Configuration in IDCS Trusted Application:

![Figure 4. IDCS Trusted Application for OAuth Client Credentials](/images/posts/2025-blogs/blog-oci_database_info_listdatabases_review_and_add.png)

Figure 4. IDCS Trusted Application for OAuth Client Credentials

### Test the OIC REST API endpoint using Postman

Once you have the Trusted Application created and configured with OAuth, you can start to test the REST API endpoint via Postman.

- **URL:** https:// <oicgen2-instance-name>.integration.ocp.oraclecloud.com/ic/api/integration/v1/monitoring/auditRecords
- **Grant type:** Client Credentials
- **Auth URL:** https://<IDCS_URL>.identity.oraclecloud.com/oauth2/v1/authorize
- **Access Token URL:** [https:// <IDCS_URL>.identity.oraclecloud.com/oauth2/v1/token](https://idcs-bc1a4522aa4547f98a1a3ec8faa93744.identity.oraclecloud.com/oauth2/v1/token)
- **Client ID:** Retrieve from the trusted application page
- **Client Secret:** Retrieve from the trusted application page
- **Scope:** https://<OIC_INSTANCE_ID>.integration.ocp.oraclecloud.com:443urn:opc:resource:consumer::all
- **Client Authentication:** Send client credentials in body

![Figure 5. OIC AuditRecords REST API testing using Postman](/images/posts/2025-blogs/blog-oci_database_info_log_explorer.png)

Figure 5. OIC AuditRecords REST API testing using Postman

Postman test result:

![Figure 6. Postman OIC AuditRecords API test result](/images/posts/2025-blogs/blog-oci_database_info_log_explorer.png)

Figure 6. Postman OIC AuditRecords API test result 

## Step 2. Create Connections in Oracle Integration Cloud

- Login OIC GEN2 service console
- Create OIC connection to interact with Oracle Integration Cloud API – OAuth Client Credentials
    - Select Integrations within Oracle Integration
    - Select Connections
    - Create a Connection using the REST Adapter
    - Connection Type: REST API Base URL
    - Connection URL: https:// <oicgen2-instance-name>.integration.ocp.oraclecloud.com
    - Security: OAuth Client Credentials
    - Access Token URI: [https:// <IDCS_URL>.identity.oraclecloud.com/oauth2/v1/token](https://idcs-bc1a4522aa4547f98a1a3ec8faa93744.identity.oraclecloud.com/oauth2/v1/token)
    - Client Id
    - Client Secret
    - Scope: https://<OIC_INST_ID>.integration.ocp.oraclecloud.com:443urn:opc:resource:consumer::all
    - Client Authentication: Send client credentials in body
    - Click Test and Save

![Figure 7. OIC OAuth Client Credentials Connection Configuration](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 7. OIC OAuth Client Credentials Connection Configuration

- Create OIC connection to interact with OCI Logging Analytics API – OCI API Signature
    - Connection Type: REST API Base URL
    - Connection URL: [https://loganalytics.us-ashburn-1.oci.oraclecloud.com](https://loganalytics.us-ashburn-1.oci.oraclecloud.com/)
    - Security: OCI Signature Version 1
    - Tenancy OCID
    - User OCID
    - Private key
    - Finger Print
    - Click Test and Save

![Figure 8. OCI Logging Analytics UploadLogFile REST API Connection via OCI API Key](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 8. OCI Logging Analytics UploadLogFile REST API Connection via OCI API Key

## Step 3. Create Oracle Integration Cloud Audit Log Source in OCI Logging Analytics

Logging Analytics [GitHub community Repo for OIC](https://github.com/oracle-quickstart/oci-o11y-solutions/tree/main/knowlege-content/oracle-integration-cloud)

- Download the OIC AuditLog log source from log-sources
- Import the OIC Audit Log log source in OCI Logging Analytics
- Select Import Configuration Content from Logging Analytics Administration

![Figure 9. Logging Analytics Import Configuration Content Item](/images/posts/2025-blogs/blog-oci_database_info_listdatabases_review_and_add.png)

Figure 9. Logging Analytics Import Configuration Content Item

- Select the downloaded Oracle Integration Cloud log source zip file and import

![Figure 10. Select the downloaded Oracle Integration Audit Log Source zip file](/images/posts/2025-blogs/blog-oci_database_info_listdatabases_review_and_add.png)

Figure 10. Select the downloaded Oracle Integration Audit Log Source zip file

- Select Sources and search “Integration”, you will find the OCI Integration Audit Logs imported

![Figure 11. OCI Integration Audit Logs Source](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 11. OCI Integration Audit Logs Source

## Step 4. Create Custom Integration in Oracle Integration Cloud

With all the ingredients ready, you can start to create the custom integration flow.

![Figure 12. OIC Custom Integration to Push Audit Logs to Logging Analytics](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 12. OIC Custom Integration to Push Audit Logs to Logging Analytics

- Retrieve OIC Audit Log records from the Oracle Integration Cloud via REST API endpoint
    - Configure REST connection endpoint to Fetch Audit Logs
    - Configure Query Parameter
    - Configure REST response
    - Verify the configuration summary

![Figure 13. OIC REST Endpoint response](/images/posts/2025-blogs/blog-oci_database_info_log_explorer.png)

Figure 13. OIC REST Endpoint response

![Figure 14. OIC REST Endpoint Verify Configuration Summary](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 14. OIC REST Endpoint Verify Configuration Summary

- Save the OIC Audit Log records as json format
    - Add and configure Stage File Action
    - Specify the Filename
    - Configure Schema options
    - Specify the JSON Format
    - Configuration Summary for Stage File

![Figure 15. Stage File Action Specify the Filename](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 15. Stage File Action Specify the Filename​​​

![Figure 16. Stage File Action Summary](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 16. Stage File Action Summary 

- Send the OIC Audit Log records json file to OCI Logging Analytics
    - Logging Analytics REST Endpoint Configuration
    - Provide Query Parameter
    - Configure the Payload
    - Configure the Logging Analytics log group id in the request header
    - REST Endpoint Configuration Summary

![Figure 17. Logging Analytics UploadLogFile REST API Endpoint Configuration](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 17. Logging Analytics UploadLogFile REST API Endpoint Configuration

![Figure 18. Logging Analytics UploadLogFile REST API Summary](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 18. Logging Analytics UploadLogFile REST API Summary

## Step 5. Explore Oracle Integration Cloud Audit Log in Logging Analytics

- Kick off the Custom Integration to Push the OIC Audit Records to Logging Analytics

![Figure 19. Kick off the OIC Custom Integration to Push Audit Log to Logging Analytics](/images/posts/2025-blogs/blog-oci_db_recovery_logs_source_config.png)

Figure 19. Kick off the OIC Custom Integration to Push Audit Log to Logging Analytics

- Check the details of the custom integration
- Check the result of the invocation of Fetching Audit Records from OIC
- Expand each step for more details
- Verify the Audit Records from OIC REST API

![Figure 20. Check the Custom Integration Invocation Details](/images/posts/2025-blogs/blog-oci_database_info_log_explorer.png)

Figure 20. Check the Custom Integration Invocation Details 

- Verify the OIC Audit Log records are successfully ingested and parsed within OCI Logging Analytics

![Figure 21. Use Logging Analytics Log Explore Query OIC Audit Logs](/images/posts/2025-blogs/blog-oci_database_info_log_explorer.png)

Figure 21. Use Logging Analytics Log Explore Query OIC Audit Logs

- Visualize the OIC Audit Logs in Dashboard

![Figure 22. Oracle Integration Audit Log Analysis Sample Dashboard](/images/posts/2025-blogs/blog-oci_database_backup_report.png)

Figure 22. Oracle Integration Audit Log Analysis Sample Dashboard

## Reference

- [Configure a Trusted Application to Authenticate with OAuth](https://docs.oracle.com/en/cloud/paas/integration-cloud/rest-api/OAuth_prereq.html)
- [OAuth Authentication and Authorization in Oracle Integration Cloud](https://docs.oracle.com/en/cloud/paas/integration-cloud/rest-api/Authentication.html)
- [OIC AuditRecords API Reference](https://docs.oracle.com/en/cloud/paas/integration-cloud/rest-api/op-ic-api-integration-v1-monitoring-auditrecords-get.html)
- [Logging Analytics UploadLogFile API Reference](https://docs.oracle.com/en-us/iaas/api/#/en/logan-api-spec/20200601/Upload/UploadLogFile)
- IDCS OAuth Access Token Expiration Time Behaviour with IDCS Scopes and Custom Scopes (Doc ID 2580015.1)
- [Use OAuth 2.0 Grants in Oracle Identity Cloud Service Environments](https://docs.oracle.com/en/cloud/paas/integration-cloud/rest-adapter/authentication-support.html#GUID-33BDEC15-CEC5-4535-8C71-FBA1A37BD7A3)
- [Using the REST Adapter with Oracle Integration Generation 2](https://docs.oracle.com/en/cloud/paas/integration-cloud/rest-adapter/understand-rest-adapter.html#GUID-216FBA19-17CC-486B-9C88-A2E96CB32B66)
- [Identity Cloud Services OAuth 2.0 and REST API](https://www.ateam-oracle.com/post/identity-cloud-services-oauth-20-and-rest-api)
- [Demystifying OAuth Using the JWT User Assertion in OIC](https://blogs.oracle.com/integration/post/oic-oauth-using-jwt-user-assertion)

## Acknowledgements

- **Contributor:** Nolan Trouvé

​