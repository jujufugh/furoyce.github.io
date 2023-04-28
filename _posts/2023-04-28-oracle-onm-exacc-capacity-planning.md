---
title: "OCI Observability and Management - 3 Keys to optimize operational efficiency for Exadata Cloud Service and Exadata Cloud@Customer"
date: 2023-04-28
last_modified_at: 2023-04-28T16:20:02-05:00
categories:
  - Blog
tags:
  - Observerability and Monitoring
  - Cloud Databases
---

### Introduction
As more organizations started OCI Cloud journey, the importance of optimizing operational efficiency becomes paramount. In the blog, we will explore 3 key strategies for maximizing the resource and performance of the Exadata Cloud Service and Exadata Cloud@Customer deployments, two most popular database cloud solutions among our Exadata customers. 

Capacity planning involves forecasting future resource needs and scaling infrastructure accordingly to avoid performance issues and ensure adepuate capacity for growth. By implementing these strategies, organizations can maximize the performance of their Exadata Cloud Service or Exadata Cloud@Customer solutions, resulting in improved uptime, faster performance, and efficient resource utilization. 

**Workload Management and Capacity Planning Strategies**

* Exadata Capacity Planning using OCI Operations Insights 
* Exadata Workload Forecast and Analysis using OCI Analytic Cloud and Exadata Warehouse
* Exadata Performance Management via OCI Database Management Service


### ExaC@C Architecture

Exadata Cloud@Customer aka. ExaC@C is a one of most popular hybrid cloud solution among Oracle's customers. It combines the best features from the Oracle cloud and keep customers' on-prem requirements in mind. Customer can keep their data within the customers' security perimeter while enabling the full out of box automoation from Oracle's most powerful database platform. 

Exadata Cloud@Customer embodies the concept of the Dom0 and DomU hypervisor concept to segregate cloud control plane from the users' DomU domain space. Oracle Cloud Infrastructure has built in API endpoints and authentication and authorization security model to ensure customers' data security without compromising on platform automation and operational efficiency. 

Here is the Exadata Cloud @ Customer architecture: <img src='/images/posts/2023-04/royce-blog-2023-04-exacc_overview_architecture.png'/>

Many customers who have migrated to the ExaCC platforms raised the same request in terms of the ExaCC platform capacity and resource planning, especially on the OCPU and Storage to have accurate cloud cost impact analysis and prediction. The good news is that Oracle has the solution for the customers in OCI O&M - Operations Insights. 

### Operations Insights
Operations Insights is an OCI native service that provides holistic insight into database and host resource utilization and capacity.

Operations Insights cnosists of the following integrated applications: 
* **Capacity Planning**
* **Oracle SQL Warehouse**
* **Exadata Insights**
* **ADDM Spotlight**
* **AWR Hub**
* **Enterprise Manager Warehouse**
* **Exadata Warehouse**

In this blog, we are going to focus on the use cases about how to use Capacity Planning and Exadata Warehouse to maximize the operational efficiency in our Exadata fleet.

### Exadata Warehouse
Exadata Warehouse provides intelligent analytics that let you maximize performance and utilization for both on-premises and cloud-based Oracle Engineered Systems, such as Exadata Database Machine.

Exadata Warehouse functions as a long-term storage repository for fine-grained performance and utilization metrics from both on-premises and cloud-based Oracle Engineered Systems monitored by Enterprise Manager Cloud Control.
<img src='/images/posts/2023-04/royce-blog-2023-04-xawh-architecture.png'/>

**Prerequisits of using Exadata Warehouse**

* **EM Side:** ExaC@C Exadata Infrastructure is discovered within EM

**NOTE: Aflredo Krieg** has a great blog post about discovering Exadata Cloud@Customer within Enterprise Manager 13.5, please check [here](https://alfredokriegdba.com/2023/04/21/maximize-your-exadata-cloud-at-customer-efficiency-using-oracle-enterprise-manager-13-5/)

* Set up OCI service connectivity.
  * **OCI Side:** Ensure an OCI Object Storage Bucket has already been created
  * **EM Side:** Define a Global Named Credential in Enterprise Manager for OCI
  * **EM Side:** Define a Host Preferred Credentials for all Database Machine Monitoring Agent hosts and OMS host
  * **EM Side:** Set up an exclusive Enterprise Manager Super Administrator user for the Enterprise Manager login
  * **EM Side:** Create an Enterprise Manager group containing the targets for which you want data exported
  * **OCI Side:** Set up the requisite OCI Policies needed for Enterprise Manager to push data into Object Storage
* **OCI Side:** Provision Autonomous Data Warehouse (ADW) and create an Analytics User to hold the Analytics Schema.
* **EM Side:** Discover the ADW on EM.
* **EM Side:** If you are using CellCli to monitor the database machine storage servers, then we recommend that you switch to using REST API for monitoring.
* **EM Side:** Configure the Cloud Bridge 
* **OCI Side:** Configure EM Bridge
* **OCI Side:** Kick off the Data Export
* **OCI Side:** Verify the Exadata Warehouse data in ADW database
* **OCI Side:** Create Oracle Analytics Cloud 

Let's start with the prerequisites from the OCI side!

**OCI Side: Create OCI service user**
* Under Identity & Security, select Identity -> Users
* Create new serivce user, for example emcloudbridge
* Under Identity & Security, select Identity -> Groups
* Create new service user group, for example emcloudbridgegroup
* Grant Permissions required for configuraion of Cloud Bridge, EM Bridge, Object Storage, Operations Insights
* An example of the policy for the emcloudbridgegroup 
```bash
Allow group emcloudbridgegroup to manage buckets in compartment exacc9vm1
Allow group emcloudbridgegroup to manage buckets in compartment exacc9vm1
Allow group emcloudbridgegroup to manage objects in compartment exacc9vm1
Allow group emcloudbridgegroup to manage objects in compartment exacc9vm1
Allow service dbx-dev to read objects in compartment exacc9vm1
Allow service dbx-dev to read objects in compartment exacc9vm1
Allow group emcloudbridgegroup to manage database-family in compartment exacc9vm1
```
* Use the OpenSSL command to generate key pair in required PEM format on Linux, for example
```bash
openssl genrsa -out ~/.oci/oci_api_key.pem 2048
chmod go-rwx ~/.oci/oci_api_key.pem               
openssl rsa -pubout -in ~/.oci/oci_api_key.pem -out ~/.oci/oci_api_key_public.pem             
cat ~/.oci/oci_api_key_public.pem | pbcopy           
```
* Create API key for the service user, under Identity -> Users, select emcloudbridge user
* Under Resources, select API Keys
* Select Add API Key and provide public key file location or paste the public key content <img src='/images/posts/2023-04/royce-blog-2023-04-xawh-api-key.png'/>
* Copy and save the fingerprint for later use

**IMPORTANT:** in order to create compatible API key between OCI and EM, we can follow [document](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm)

**OCI Side: Create an OCI Object Storage Bucket**
* From Storage menu, select Object Storage & Archive Storage
* Create Bucket
* Select Standard Tier and Encrypt using Oracle managed keys <img src='/images/posts/2023-04/royce-blog-2023-04-xawh-oob-create.png'/>

**EM Side: Define a Global Named Credential in Enterprise Manager for OCI**
* From the Setup menu, choose Security and then Named Credentials
* Use the private key, public key fingerprint and tenancy and user ocid to create the Named Credential to connect to OCI <img src='/images/posts/2023-04/royce-blog-2023-04-oci-named-cred.png'/>

**EM Side: Define a Preferred Credentials for Agent hosts and OMS host**
* Under Security, click Preferred Credentials and select Host.
* Set Normal Host Credential and Privileged Host Credential (REST API credential used for compute node).
* For the OMS host, set credentials of the user.<img src='/images/posts/2023-04/royce-blog-2023-04-oci-preferred-cred.png'/>

**EM Side: Create and Test REST API for Storage and Compute nodes**
* Create REST API user for compute nodes
```bash
dbmcli -e 'CREATE ROLE monitor;  GRANT PRIVILEGE list ON ALL OBJECTS ALL ATTRIBUTES WITH ALL OPTIONS TO ROLE monitor;'
dbmcli -e 'create user restapi_user password=your_password';
dbmcli -e 'grant role monitor to user restapi_user';
```
* Cell Storage servers access is in Dom0, so we need to set server credentials to use REST API to access the cell storage metrics
**See More Details in [Discover the Exadata Database on Cloud@Customer Target Using Console](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/13.5/emxcs/discover-exadata-cloud-targets.html#GUID-9876946B-61DC-4591-A669-E05EA3A8E1F1)** 
* Test REST API with cell storage server
```
[oracle@ecc9c1n2 ~]$ curl -k -u cloud_user_cluclu062f2:xxxxxxxxxxxxx https://10.0.10.10/MS/RESTService?cmd=list%20metrichistory%20CD_IO_LOAD
```
	 CD_IO_LOAD	 FD_02_iad160204exdcl04	 0.0	 2023-04-16T16:00:35+00:00
	 CD_IO_LOAD	 CD_00_iad160204exdcl04	 0.0	 2023-04-16T16:00:35+00:00
	 CD_IO_LOAD	 CD_02_iad160204exdcl04	 0.0	 2023-04-16T16:00:35+00:00
	 CD_IO_LOAD	 CD_04_iad160204exdcl04	 0.0	 2023-04-16T16:00:35+00:00
	 CD_IO_LOAD	 CD_05_iad160204exdcl04	 0.0	 2023-04-16T16:00:35+00:00
	 CD_IO_LOAD	 CD_06_iad160204exdcl04	 0.2	 2023-04-16T16:00:35+00:00
	 CD_IO_LOAD	 CD_08_iad160204exdcl04	 0.0	 2023-04-16T16:00:35+00:00
	 CD_IO_LOAD	 CD_10_iad160204exdcl04	 0.0	 2023-04-16T16:00:35+00:00
* Test REST API with compute node
```
[oracle@ecc9c1n2 ~]$ curl -k -u restapi_user:xxxxxxxxxxxxxhttp://10.0.10.9:7879/MS/RESTService?cmd=list%20metrichistory%20DS_CPUT%20where%20ageInMinutes < 10
```

**EM Side: Create an Enterprise Manager group containing the targets for which you want data exported**
* From the Target menu, select Groups. The Groups page opens
* Click Create and select Group
* Select Targt type Oracle Exadata Infrastructure to be added to the group <img src='/images/posts/2023-04/royce-blog-2023-04-em-group.png'/>

**OCI Side: Provision Autonomous Data Warehouse (ADW) and create an Analytics User to hold the Analytics Schema**
* Go to OCI tenancy console
* Oracle Database -> Autonomous Database
* Create Autonomous Database 
* Select Data Warehouse type database
* Configure proper network access make sure your EM can discover the ADW database
* Once the ADW is created, click Database connection, download the wallet for connection <img src='/images/posts/2023-04/royce-blog-2023-04-xawh-adw-wallet.png'/>
* Go to Database Actions
* In Administration, select Database Users
* Create User - EMCLOUDBRIDGE

Some [considerations](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/13.5/emadb/prerequisite-tasks-autonomous-databases-shared.html#GUID-3B415134-6B5E-44A5-BFAA-A3473BDBFE31) when onboarding Autonomous Databases to Oracle Enterprise Manager Deployed in OCI or on-prem

**EM Side: Discover the ADW on EM**
* Under EM Secuirty, select **Named Credentials**. Create a new named credential with for EMCLOUDBRIDGE user within the ADW <img src='/images/posts/2023-04/royce-blog-2023-04-xawh-adw-named-credential.png'/>
* Onboard ADW to EM target 
* From Setup menu, select Add Target, Add Targets Manually
* Add Non-Host Targets Manually
* Seelect Autonomous Data Warehouse as Target Type
* Provide Target Name, Wallet and Wallet Password
* Verify the connection string for the ADW <img src='/images/posts/2023-04/royce-blog-2023-04-xawh-adw-discover.png'/><img src='/images/posts/2023-04/royce-blog-2023-04-xawh-adw-em-target.png'/>

  **More Details** check [EM 13.5 documentation](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/13.5/emadb/discover-autonomous-databases.html) to discover Autonomous Database 

**EM Side: If you are using CellCli to monitor the database machine storage servers, then we recommend that you switch to using REST API for monitoring**

**EM Side: Configure the Cloud Bridge**

**OCI Side: Configure EM Bridge**

**OCI Side: Kick off the Data Export**

**OCI Side: Verify the Exadata Warehouse data in ADW database**

**OCI Side: Create Oracle Analytics Cloud**


**EM Side: additional configuration to ingest metric for xawh_forecast_settings.csv
```csv
forecast_steps=168
model_history=840
min_model_history=148
granularity=HOURLY
```

### Reference
**[Operations Insights Doc](https://docs.oracle.com/en-us/iaas/operations-insights/doc/get-started-operations-insights.html#GUID-457A50BA-2C88-429B-A0FC-41ACBA55737E)** 
**[Exadata Warehouse Configuration](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/13.5/emexw/index.html#before_you_begin)**
[Integrating Enterprise Manager 13.5 with OCI Services](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/13.5/emadm/using-oci-services-enterprise-manager.html#GUID-1F310CD9-23FD-4CF3-8E32-0943F7DB3762)