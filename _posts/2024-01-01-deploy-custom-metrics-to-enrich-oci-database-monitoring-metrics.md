---
title: "Deploy Custom Metrics to Enrich OCI Database Monitoring Metrics"
date: 2024-01-01
last_modified_at: 2024-01-01T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - OCI Monitoring
  - Custom Metrics
---

# Introduction

Oracle Cloud Infrastructure Observability and Management ([OCI O&M](https://www.oracle.com/manageability/)) offers a range of functions and capabilities for monitoring the health and performance of your cloud infrasturcture and resources, including your databases, compute instances, network, application stack. Highly scalable and resilient observability and monitoring solution is an essential part of any cloud deployment. While OCI provides default metrics for databases, there may be instances where custom metrics need to be used to monitor databases that are not monitored by default. **Custom metrics** allow you to monitor specific aspects of your databases that are critical to your business, but that are not captured by out-of-box monitoring. For example, you may want to monitor the transport and apply lag between your primary database and standby database in Data Guard configuration or the performance specific metrics monitoring such as shared_pool memory utilization.

**Todd Sharp** started with an awesome blog [Publishing and Analyzing Custom Applicatino Metrics with The Oracle Cloud Monitoring Service](https://blogs.oracle.com/developers/post/publishing-and-analyzing-custom-application-metrics-with-the-oracle-cloud-monitoring-service) with [GitHub code example](https://github.com/recursivecodes/oci-custom-metrics) demonstrating how to create user defined custom metrics and publish them to user defined metric namespace in OCI Monitoring Service. This blog will focus on taking Todd’s code into the OCI O&M environment and deploy the Java application into OCI Cloud.

**Read more about OCI Monitoring service [here](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Concepts/monitoringoverview.htm)**

# Deployment Options

[OCI SDK and CLI](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/publishingcustommetrics.htm) provides very flexible development and deployment options for publishing custom metrics. Not only we can run the Java application in compute instance, we can also build the jar file and run the jar file directly within the cron job. Even we can use Fn project to deploy the java application into Oracle Functions. The implementation and deployment examples are no limited to above, for example, we can also use a shell script deployed in cronjob periodically connect to the database and run the SQL queries to check the long running session and spool the result into log file which subsequently stream log file into logging service and LA. Then we will create detection rule to publish the metrics pass the threshold into the monitoring service custom metric namespaces.

We will discuss two options here:

- **Run Java program locally in Inellij**
- **Build Jar file and schedule the jar file in the cronjob in compute instance**

## Run the Java program locally

After downloading Todd’s GitHub code [repo](https://github.com/recursivecodes/oci-custom-metrics), you can open the folder in the [Intellij](https://www.jetbrains.com/help/idea/installation-guide.html).

**Prerequisits**

- User account which has the permission to manage metrics
- User account belongs to groups which have manage metrics permission for the compartment to publish custom metrics
- Database schema user account created for monitoring and retrieve database table or view data
- Database connection is accessible from local laptop environment to the database in OCI
- VCN subnet security list is updated to allow connection from local laptop

A few configuration changes are required before running the program locally

## Run the Java web application in compute instance

**Prerequisits**

- Create dynamic group for the compute instance
- Grant permissions to the dynamic group
- Dynamic group needs to have the permission to manage metrics
- Database schema user account created for monitoring and retrieve database table or view data
- Database connection is accessible from local laptop environment to the database in OCI
- VCN subnet security list is updated to allow connection from local laptop

The example code has option to be built the application using Gradle. You can follow the Intellij Gradle documentation - [Getting Started with Gradle](https://www.jetbrains.com/help/idea/getting-started-with-gradle.html).

## Troubleshooting

You may see exception about Authorization failure when publishing the metrics. The root cause is related to the compute instance instance principal dynamic group permission. You can read more about instance principal [here](https://docs.public.oneportal.content.oci.oraclecloud.com/en-us/iaas/Content/Identity/Tasks/callingservicesfrominstances.htm)

**INSTANCE PRINCIPALS** The IAM service feature that enables instances to be authorized actors (or principals) to perform actions on service resources. Each compute instance has its own identity, and it authenticates using the certificates that are added to it. These certificates are automatically created, assigned to instances and rotated, preventing the need for you to distribute credentials to your hosts and rotate them.

After updating the policies for the dynamic group of the compute instance to enable the capabilities of manage metrics in the compartment, the issue is fixed.

**Example of required dynmaic groups and permissions**

  

```
ALL {instance.compartment.id='ocid1.compartment.oc1..aaaaaaaaexamplecompartmentocid'}
Allow dynamic-group obs-mgmt-compute-dg  to manage metrics in compartment obs_mgmt_comp
```

# Conclusion