---
title: "Simplify Cross-Region Log Consolidation in OCI with Logging Analytics REST API"
date: 2024-01-01
last_modified_at: 2024-01-01T09:00:00-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
  - OCI Log Analytics
  - Cross-Region
---

## Introduction

Organizations operating across multiple Oracle Cloud Infrastructure (OCI) regions often need a centralized logging solution for unified monitoring, security analysis, and compliance reporting. Traditionally, consolidating logs from different regions involved setting up complex data pipelines using services like OCI Streaming and OCI Functions. This approach, while functional, introduced additional infrastructure to manage, potential points of failure, and increased latency.

This blog post introduces a simplified and more efficient paradigm for cross-region log consolidation using the OCI Logging Analytics REST API ingestion method, powered by the OCI Management Agent.

## The Challenge with Traditional Cross-Region Logging

Consolidating logs across regions typically required:

1. **Service Connector Hub (SCH)** in each source region to send logs (e.g., Audit Logs, VCN Flow Logs) to OCI Streaming.
2. **OCI Streaming** service in each source region to act as a message bus.
3. **OCI Functions** triggered by messages in the streams, responsible for reading logs and pushing them to a central Logging Analytics instance in the designated "home" region.
4. **Cross-Region Networking**: Ensuring connectivity and managing permissions between Functions in source regions and the Logging Analytics service in the home region.

This architecture involved multiple moving parts, configuration overhead, and potential latency introduced by the intermediate services.

## A New Paradigm: Direct Ingestion via Management Agent and REST API

OCI Logging Analytics now offers a more direct and streamlined approach leveraging the Management Agent and its ability to interact with REST APIs using secure resource principal authentication.

Here's how it works:

1. **Central Logging Analytics Instance**: Designate one OCI region as your "home" region where your primary Logging Analytics instance resides.
2. **Management Agents in Source Regions**: Deploy OCI Management Agents (either standalone or via Oracle Cloud Agent) on VMs in each of your _source_ OCI regions.
3. **Dynamic Groups and Policies**: Create dynamic groups for the Management Agents in each source region and configure IAM policies to allow these agents (via resource principal) to read logs (e.g., Audit Logs) _within their own region_.
4. **Logging Analytics REST API Endpoint Configuration**: In the central Logging Analytics instance (home region), configure a REST API Log Source and Endpoint. Crucially, the Endpoint URL will point to the OCI Logging service API endpoint _in the source region_ (e.g., `https://logging.{source_region}.oci.oraclecloud.com/...`).
5. **Association**: Associate the Management Agent entity (representing the agent running in the source region) with this REST API Log Source in the central Logging Analytics instance.

**The Flow:**

- The Management Agent, running in the source region, receives the configuration pushed from the central Logging Analytics instance.
- It uses its resource principal to authenticate _within the source region_ and calls the OCI Logging API endpoint defined in the configuration (which points to the source region's Logging API).
- It pulls the required logs (e.g., Audit Logs for the last N minutes/hours/days) from the source region's Logging service.
- The Management Agent then securely transmits these collected logs directly to the central Logging Analytics instance in the home region via the established secure connection.

 _Figure 1: Simplified architecture showing Management Agent pulling logs from source region and pushing directly to central Logging Analytics via REST API_

## Benefits of the New Approach

- **Simplified Architecture**: Eliminates the need for OCI Streaming and Functions for log transport, reducing complexity and management overhead.
- **Reduced Latency**: Direct ingestion minimizes hops, potentially lowering the time it takes for logs to appear in the central instance.
- **Enhanced Security**: Leverages Management Agent's resource principal authentication, avoiding the need to store or manage credentials for cross-region communication.
- **Cost Efficiency**: Reduces potential costs associated with running Streaming and Functions services solely for log transport.
- **Scalability**: Scales with the Management Agent infrastructure.
- **Versatility**: Applicable to various log types available via OCI Logging APIs, not just Audit Logs.

## Implementation Considerations

- **Management Agent Deployment**: Ensure Management Agents are deployed and configured correctly in each source region.
- **IAM Policies**: Carefully craft IAM policies to grant least privilege access for agents to read necessary logs in their respective regions.
- **Endpoint Configuration**: Double-check that the REST API Endpoint URL in the central Logging Analytics configuration correctly points to the Logging API of the _source_ region from which logs are being collected.
- **Network Connectivity**: Ensure the Management Agents in source regions can reach the central Logging Analytics ingestion endpoints in the home region (typically requires standard internet egress or Service Gateway configuration).
- **Log Source/Parser**: Define appropriate log sources and parsers in the central Logging Analytics instance to handle the incoming logs correctly.

## Getting Started

The core steps involve adapting the process described in the [historical OCI Audit Log collection blog post](https://file+.vscode-resource.vscode-cdn.net/Users/jujufu/work/ainotes/LA_cross_region_consolidation/LINK_TO_PREVIOUS_BLOG_POST_URL):

1. **Install/Configure Management Agent** in the source region(s).
2. **Create Dynamic Group(s) and Policies** for the agent(s) in the source region(s) to read local logs.
3. **In the Home Region Logging Analytics:** a. Create a **Host Entity** representing the agent in the source region. b. Create or import the required **Log Parser** and **Log Source** (Type: REST API). c. Create a **Collection Endpoint**: - **URL**: `https://logging.{source_region}.oci.oraclecloud.com/20190909/search` (replace `{source_region}`) - **Method**: POST - **Payload**: Define the query to fetch logs from the source region (e.g., Audit Logs). - **Credential Type**: None (uses resource principal). d. **Associate** the source region's Host Entity with the Log Source.

## Conclusion

The ability to use the OCI Management Agent with REST API ingestion for cross-region log consolidation marks a significant simplification over previous methods. By leveraging secure resource principal authentication and direct API interaction, organizations can build a robust, efficient, and secure centralized logging solution in OCI Logging Analytics without the overhead of intermediate data pipelines.

This pattern streamlines operations, potentially reduces costs, and provides a unified platform for analyzing logs from across your entire OCI multi-region footprint.

## References

- [OCI Logging Analytics: Collect Logs Using REST API Collection Method](https://www.ateam-oracle.com/post/oci-logging-analytics-collect-logs-using-rest-api-collection-method)
- [OCI Documentation: Set Up REST API Log Collection](https://docs.oracle.com/en-us/iaas/logging-analytics/doc/set-rest-api-log-collection.html)
- [OCI Documentation: Management Agent Overview](https://docs.oracle.com/en-us/iaas/management-agents/doc/management-agent-overview.html)
- [OCI Documentation: Dynamic Groups](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingdynamicgroups.htm)