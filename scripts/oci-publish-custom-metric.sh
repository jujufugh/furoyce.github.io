#!/usr/bin/env bash
#
# This script publishes a custom metric to Oracle Cloud Infrastructure (OCI) Monitoring service.
# It retrieves the count of Java server processes running on the host and sends it as a metric data point.
# The script requires three input parameters: OC_TELEMETRY_URL, COMPARTMENT, and NAMESPACE.
# The script uses the OCI CLI to interact with OCI services.
#
# Usage: oci-publish-custom-metric.sh OC_TELEMETRY_URL COMPARTMENT NAMESPACE
# 
# Developed by: Royce Fu
#
# Example: oci-publish-custom-metric.sh https://telemetry-ingestion.us-ashburn-1.oraclecloud.com TESTCOMPARTMENT MyMetricsNamespace
# 
# DISCLAIMER – This is not an official Oracle application, It is provided for educational purposes only. 
# It does not supported by Oracle Support. It's your sole responsibility to verify the script and its output before running it on any environment.
#

validate_return_code() {
  if [ $1 -ne 0 ]; then
    echo "Command failed with return code: $1"
    exit $1
  fi
}

procCount=`/usr/bin/ps -ef | grep java | grep -v "grep" | grep -v "java_process_monitor" |  wc -l`
echo ${procCount}

WORK_DIR=$(cd $(dirname "$0"); pwd -P)
OC_TELEMETRY_URL=$1
COMPARTMENT=$2
NAMESPACE=$3
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")

# Retrieve the resource name and compute resource ID
RESOURCENAME=`hostname`
COMPUTERESOURCEID=`oci compute instance list -c "${COMPARTMENT}" --display-name ${RESOURCENAME} | jq '.data[].id'`
validate_return_code $?

METRICNAME="JavaServerProcessCount"
RESOURCEGROUP="host"

# Create a JSON file with the metric data
cat <<EOF>oci_metric_data.json
[
  {
    "compartmentId": "${COMPARTMENT}",
    "datapoints": [
      {
        "timestamp": "${TIMESTAMP}",
        "value": ${procCount}
      }
    ],
    "dimensions": {
      "resourceName": "${RESOURCENAME}",
      "computeResourceId": ${COMPUTERESOURCEID}
    },
    "metadata": {
      "category": "CustomMetrics"
    },
    "name": "${METRICNAME}",
    "namespace": "${NAMESPACE}",
    "resourceGroup": "${RESOURCEGROUP}"
  }
]
EOF
validate_return_code $?

# Post the metric data to OCI Monitoring service
oci monitoring metric-data post --metric-data file://oci_metric_data.json --endpoint "${OC_TELEMETRY_URL}"
validate_return_code $?

/bin/echo "INFO: Custom Metric ${METRICNAME} posted successfully to OCI Monitoring service"

# END
