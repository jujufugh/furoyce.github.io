---
title: "OCI Observability and Management - Oracle Cloud Agent and Management Agent "
date: 2023-02-22
last_modified_at: 2023-02-22T16:20:02-05:00
categories:
  - Blog
tags:
  - Observerability and Monitoring
---

### Introduction
When we have increasingly more of the IT infrastructure workload migrated over to the cloud, we see the importance of getting the proper Observability and Monitoring in place so that we can have 24/7 insights about our cloud operation, and we can take immediate action when anything is going south. The important compoenent to collect and stream the metrics to the monitoring control plane is the Cloud Agent, it is a lightweight software agent which manages plugins running on compute instances. Plugins collect performance metrics, install OS updates, and perform other instance management tasks. 

Following are the functionalities that Cloud Agent Plugins provide: 



### Logging architecture
The logging architecture on OKE typically involves two main components: Fluentd and Elasticsearch. Fluentd is a log collector that gathers log data from containers running on Kubernetes, while Elasticsearch is a search and analytics engine that indexes and stores the logs.
Fluentd runs as a DaemonSet on your Kubernetes cluster, with one instance running on each node. Each Fluentd instance collects logs from the containers running on its node, and sends them to Elasticsearch. Elasticsearch then indexes and stores the logs, making them available for searching and analysis.

### Setting up logging
To set up logging on OKE, you'll need to perform the following steps:
1. Configure Fluentd: You'll need to create a Fluentd configuration file that specifies how Fluentd should collect logs from the containers running on your cluster. This file should specify which logs to collect, where to send them, and any transformations or filters that should be applied.
2. Deploy Fluentd: Once you have a Fluentd configuration file, you can deploy a Fluentd DaemonSet on your Kubernetes cluster. The DaemonSet ensures that there is a Fluentd instance running on each node in the cluster, so that all logs are collected.
3. Configure Elasticsearch: After the logs are collected by Fluentd, you'll need to configure Elasticsearch to index and store them. You can do this by deploying an Elasticsearch cluster on your Kubernetes cluster, and configuring Fluentd to send the logs to it.

### Customizing logging
You can customize logging on OKE in several ways. For example, you can add custom fields to log records to provide more information about your applications. You can also use Fluentd to filter and transform logs before they are sent to Elasticsearch.
Fluentd has a powerful filtering system that allows you to modify log data before it is sent to Elasticsearch. You can use filters to add, remove, or modify fields in log records, and to drop or route log data based on specific criteria.

### Monitoring architecture
The monitoring architecture on OKE typically involves two main components: Prometheus and Grafana. Prometheus is a monitoring and alerting toolkit that collects metrics from Kubernetes and other sources, while Grafana is a visualization tool that allows you to create dashboards and visualizations based on the metrics.
Prometheus runs as a set of stateful containers on your Kubernetes cluster, and collects metrics from Kubernetes itself, as well as from any applications that expose Prometheus-compatible metrics. Once the metrics are collected, they are stored in a time-series database.
Grafana runs as a set of stateless containers on your Kubernetes cluster, and provides a web-based interface for creating dashboards and visualizations based on the metrics collected by Prometheus.

### Setting up monitoring
To set up monitoring on OKE, you'll need to perform the following steps:
1. Deploy Prometheus: You can deploy Prometheus on your Kubernetes cluster using the Prometheus Operator, which simplifies the process of creating and managing a Prometheus instance. The Prometheus Operator will create and manage the necessary Kubernetes objects to run a Prometheus server.
2. Configure Prometheus: Once you have a Prometheus server running, you'll need to configure it to collect metrics from your Kubernetes cluster and any applications that expose Prometheus-compatible metrics. You can do this by creating Prometheus configuration files that specify which metrics to collect and where to collect them from.
3. Deploy Grafana: You can deploy Grafana on your Kubernetes cluster using the Grafana Operator, which simplifies the process of creating and managing a Grafana instance. The Grafana Operator will create and manage the necessary Kubernetes objects to run a Grafana server.
4. Configure Grafana: After you have Grafana running, you'll need to configure it to connect to your Prometheus server and create dashboards and visualizations based on the metrics collected by Prometheus. Grafana provides a web-based interface for creating and managing dashboards, which you can use to create custom dashboards that show the metrics that are most important to your applications.

### Customizing monitoring
You can customize monitoring on OKE in several ways. For example, you can create custom Prometheus rules to define alerts based on specific metrics. You can also create custom Grafana dashboards to visualize metrics in the way that makes the most sense for your applications.
Prometheus provides a powerful expression language that allows you to define complex rules for alerting. You can use these rules to define alerts based on specific metrics and conditions, such as when the number of requests to a service exceeds a certain threshold.
Grafana provides a flexible interface for creating and managing dashboards. You can create custom dashboards that show the metrics that are most important to your applications, and use a variety of visualizations and widgets to display the data.

### Best Practices

#### Log retention
It's important to set up log retention policies to ensure that you're storing logs for the appropriate amount of time. You can configure Elasticsearch to automatically delete old log data after a certain period of time, or you can use a tool like Curator to manage log retention.
Curator is a tool that allows you to manage Elasticsearch indices based on a variety of criteria, such as age, size, or number of documents. You can use Curator to automatically delete old log data and ensure that you're not storing logs longer than necessary.

#### Alerting
Setting up alerts is essential for detecting and responding to issues with your applications. You can configure Prometheus to send alerts when certain conditions are met (such as when a container crashes), and you can use a tool like Alertmanager to manage and route alerts.
Alertmanager is a tool that allows you to manage alerts sent by Prometheus. You can use Alertmanager to route alerts to different notification channels (such as email, Slack, or PagerDuty), and to deduplicate and group alerts based on specific criteria.

#### Scaling
As your applications grow, you may need to scale your logging and monitoring components to handle larger amounts of data. You can use Kubernetes scaling features to scale up or down the number of Fluentd or Prometheus instances running in your cluster.
For example, you can use a Horizontal Pod Autoscaler (HPA) to automatically scale the number of Fluentd instances based on the amount of log data being generated. Similarly, you can use a Prometheus Remote Write feature to send metrics to an external monitoring system (such as a hosted Prometheus service), allowing you to scale Prometheus independently of your Kubernetes cluster.

## Conclusion
In the conclusion, you should summarize the key points of the article and emphasize the importance of logging and monitoring for applications running on OKE. You can also offer some resources for readers who want to learn more about logging and monitoring on OKE.
Overall, logging and monitoring are essential for ensuring the health and availability of your applications on OKE. By setting up logging and monitoring components, and customizing them to meet your specific needs, you can quickly identify and resolve issues before they impact your users.