---
title: "OCI Observability and Management - Disaster Recovery Considerations "
date: 2023-03-07
last_modified_at: 2023-03-07T16:20:02-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
---

### Introduction
When we have increasingly more of the IT infrastructure workload migrated over to the cloud, we see the importance of getting the proper Observability and Monitoring in place so that we can have 24/7 insights about our cloud operation, and we can take immediate action when anything is going south. The important compoenent to collect and stream the metrics to the monitoring control plane is the Cloud Agent, it is a lightweight software agent which manages plugins running on compute instances. Plugins collect performance metrics, install OS updates, and perform other instance management tasks. 

Following are the functionalities that Cloud Agent Plugins provide: 



