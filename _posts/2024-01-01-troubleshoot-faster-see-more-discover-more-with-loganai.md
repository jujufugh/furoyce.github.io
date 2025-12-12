---
title: "Troubleshoot Faster, See More, Discover More with LoganAI"
date: 2024-01-01
last_modified_at: 2024-01-01T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - OCI Log Analytics
  - AI
---

We're thrilled to announce **LoganAI**, a major innovation in Oracle Log Analytics that brings enriched AI-driven insights directly to your logs.

**OCI Log Analytics**—part of the Oracle Cloud Observability and Management platform—helps you ingest, index, and analyze massive volumes of log data from applications, infrastructure, and cloud resources. It provides powerful search, visualization, and anomaly detection tools to troubleshoot issues, monitor system health, and improve operational efficiency. Now, with the addition of LoganAI, these capabilities are augmented with AI-powered summarization, contextual explanations, and intelligent recommendations.

## What Is LoganAI?

LoganAI is Oracle Log Analytics' new **Artificial Intelligence capability**, designed to interpret, summarize, and enhance your log data—no manual parsing required. It can also blend in metrics retrieved via OCI Monitoring (using MQL) and documents from Object Storage to deliver richer analysis ([Documentation](https://docs.oracle.com/en-us/iaas/log-analytics/doc/use-loganai.html)) that is seamlessly integrated with your log exploration and troubleshooting workflows. Here are few things we are excited about:

- **AI-Powered Summaries:**  Quickly grasp complex log data through concise summaries of individual logs, clusters, groups, and charts.
- **Context-Aware Follow-ups:** Need more detail? LoganAI suggests relevant next questions tailored to your data’s context—making exploration intuitive and efficient.
- **Root Cause Detection:** Anomalies and patterns? LoganAI spotlights them fast—helping you dive straight into what matters.
- **Simplified Explanations:** Complex chart patterns and log clusters become easy-to-understand narratives—ideal for both technical and business audiences.

Before diving in, there are some prerequisites and policies needed to setup LoganAI in your tenancy:

1. Your tenancy must be subscribed to an OCI Region where OCI Generative AI service is [available](https://docs.oracle.com/en-us/iaas/Content/generative-ai/overview.htm#regions). 
2. _Configure LoganAI Settings_ in [Log Analytics Administration](https://cloud.oracle.com/loganalytics/service) by selecting the OCI Generative AI region you want to use and create required service and user group policies
3. Open [**Log Explorer**](https://cloud.oracle.com/loganalytics/explorer) in OCI Log Analytics.
4. Once enabled, the LoganAI icon ![LoganAI Icon](/images/posts/2025-blogs/logan-ll-aiw-saas-blog-ss1.png) will show up in various placed in Log Explorer. Just click and follow-the-prompts!

See detailed steps [here](https://docs.oracle.com/en-us/iaas/log-analytics/doc/prerequisites-using-loganai.html).  

# LoganAI in Action

## Instant Clarity: AI Powered Explanation of Any Log with _Log Explain_

Summarize patterns and insights from groups of logs. LoganAI provides top-level views and can guide deeper exploration with follow-up questions. In the example below, LoganAI analyzed over 1,300 Oracle Database trace log records, quickly uncovering key operational patterns and anomalies. It identified frequent memory management activities—such as packet and chunk deallocation—and highlighted a correlation between specific trace files and RM lock upconversion functions. LoganAI also flagged unusual error occurrences, like error code 604 in _kpongetmsgcount()_ calls and repeated _Reconnect to box_ failures, which could indicate underlying connectivity issues. By distilling complex log data into clear patterns and actionable alerts, LoganAI enables faster diagnosis and more efficient troubleshooting.

![Multi-log Explain - "Analyzing Oracle Database Trace Logs: Memory Management, RM Locks, and Anomalies"](/images/posts/2025-blogs/db-trace-multi-log (2).png)

Figure 1: Multi-log Explain - "Analyzing Oracle Database Trace Logs: Memory Management, RM Locks, and Anomalies"

Click the LoganAI icon next to a single log entry to get a clean, concise explanation—and probe further with AI-suggested or custom questions. Below, LoganAI analyzed Fusion Apps ESS Audit Log record, instantly highlighting patterns in user assertion events and security-related activity. By parsing complex JSON log data, LoganAI extracted key details such as event type, category, target user, and timestamp, transforming dense audit records into clear, actionable insights. This automation eliminates the need for manual log inspection, allowing teams to quickly pinpoint account switches, track security events, and ensure compliance monitoring is both efficient and accurate.

![Single Log Explain - Fusion ESS Audit Log Explanation](/images/posts/2025-blogs/fusion-ess-single-log (2).png)

Figure 2: Fusion ESS Audit Log Explanation 

## Unstructured to Clarity: AI Insights Across Entire Log Clusters with _Cluster Explain_

LoganAI helps uncover trends, outliers, and anomalies across clustered log sets—ideal for large-scale troubleshooting. In this case, LoganAI rapidly processed over 9,500 OCI Audit Log records, clustering similar events and spotlighting anomalies that could indicate operational or security concerns. By automatically surfacing patterns—such as the unusually high frequency of _ListEnrollmentStatuses failed_—and correlating them with other related security events, LoganAI enabled quick identification of potential problem areas without the need for manual log combing. This capability turns a flood of raw audit data into focused, actionable insights, helping teams prioritize investigations and address issues faster.

![Cluster Explain - OCI Audit Log Insights: User Management Trends, Security Checks, and Anomalies](/images/posts/2025-blogs/oci-audit-cluster-explain (2).png)

Figure 3: OCI Audit Log Insights: User Management Trends, Security Checks, and Anomalies

Let's look at Database Trace Logs once more, below LoganAI quickly sifted through hundreds of database trace log records, automatically grouping related entries, surfacing patterns, and highlighting anomalies that might otherwise go unnoticed. By identifying frequent events, correlating them with specific errors, and pinpointing affected containers, the AI accelerated root cause analysis and reduced the time spent on manual log review. This kind of automated insight transforms raw logs into actionable intelligence, enabling teams to focus on resolving issues rather than wading through endless lines of data.

![Cluster Explain (Potential Issues) - Database Trace Log Analysis: Device Reopens, Connectivity Errors, and Multi-Container Insights](/images/posts/2025-blogs/db-trace-cluster-potential-issues (2).png)

Figure 4: Database Trace Log Analysis- Device Reopens, Connectivity Errors, and Multi-Container Insights

## Story of Logs Behind the Charts with Link _Chart Explain_

In “link” visualizations, LoganAI analyzes bubbles, trends, and regions—making complex charts instantly intelligible. Here LoganAI analyzed over 30M log records from link generated 470 groups, which automatically clusters them by size and behavior to highlight anomalies. LoganAI flagged group 26 from OCI VCN Flow Unified Schema Logs having unusual size and count. LoganAI also identified key log sources, such as multiple Oracle Fusion Apps audit logs, and highlighted which sources appeared most frequently. By combining anomaly detection with log classification at scale, LoganAI provides a clear view of both normal and abnormal activity, helping teams zero in on issues that warrant deeper investigation.

![Chart Explain - LoganAI Spotlights Anomalous OCI VCN Flow and Fusion Apps Log Activity](/images/posts/2025-blogs/chart-explain-link (2).png)

Figure 5: LoganAI Spotlights Anomalous OCI VCN Flow and Fusion Apps Log Activity

## **How LoganAI Works and Pricing**

LoganAI runs entirely within your OCI tenancy, leveraging **OCI Generative AI Services** to process and interpret logs. When you click ![LoganAI Icon](/images/posts/2025-blogs/logan-ll-aiw-saas-blog-ss1.png) in the Log Explorer UI, the analysis happens directly in your environment—no log data is sent to an Log Analytics backend. LoganAI applies natural language models to your selected logs, clusters, or charts to detect patterns, summarize key activity, and highlight anomalies. It can also enrich insights by correlating logs with related metrics or documents stored in OCI Object Storage, all without leaving the Log Analytics interface. To use LoganAI, your tenancy must have OCI Generative AI Services configured and accessible.

The cost of using LoganAI is directly tied to your **OCI Generative AI Services** usage. Each Explain action consumes Generative AI resources, so charges will depend on how often you run explanation, the complexity & volume of the data analyzed and number of follow-up requests. These costs are in addition to standard OCI Log Analytics. Full pricing details can be found in the [OCI Pricing](https://www.oracle.com/cloud/pricing/) guide under **Generative AI Services**.

LoganAI is more than a feature—it’s a leap forward in log intelligence. It makes troubleshooting faster, insights clearer, and log analytics more accessible. Whether you're an engineer, analyst, or business stakeholder, LoganAI transforms how you understand and act on your log data.

## Resources

- [LoganAI Documentation](https://docs.oracle.com/en-us/iaas/log-analytics/doc/use-loganai.html)
- [Getting started with Log Analytics](https://docs.oracle.com/en-us/iaas/log-analytics/doc/quick-start.html)
- [OCI Generative AI Regions](https://docs.oracle.com/en-us/iaas/Content/generative-ai/overview.htm#regions)
- [OCI Generative AI Pricing](https://docs.oracle.com/en-us/iaas/Content/generative-ai/pay-on-demand.htm) 

​