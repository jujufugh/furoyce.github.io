#!/bin/bash

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to calculate timestamp from sysdate going back by a number of days
calculate_timestamp() {
    local num_days="$1"
    
    # Calculate the timestamp
    timestamp=$(date -u -d "@$(( $(date -u +%s) - num_days * 24 * 3600 ))" +"%Y-%m-%dT%H:%M:%S.%3NZ")
    
    echo "$timestamp"
}

# Function to retrieve OCI alarm information
get_alarm_info() {
    local compartment_id="$1"

    # Check if OCI CLI is available
    if ! command_exists "oci"; then
        echo "Error: OCI CLI is not installed or not in PATH."
        exit 1
    fi

    # Use OCI CLI to retrieve alarm information including status and suppression fields
    oci monitoring alarm-status list-alarms-status --compartment-id "$compartment_id" --query 'data[*].{AlarmName:"display-name", AlarmID:id, Severity:severity, Status:status, Suppression:suppression}' --raw-output 2>/dev/null
}

# Function to retrieve and aggregate alarm history per AlarmID and group by severity
aggregate_alarm_history() {
    local alarm_data="$1"
    local timestamp_greater_than="$2"

    # Initialize an associative array to store the counts by AlarmID and Severity
    declare -A alarm_counts

    # Check if OCI CLI is available
    if ! command_exists "oci"; then
        echo "Error: OCI CLI is not installed or not in PATH."
        exit 1
    fi

    # Check if jq is available
    if ! command_exists "jq"; then
        echo "Error: jq is not installed or not in PATH. Please install jq."
        exit 1
    fi

    

    # Loop through alarm_data
    while read -r line; do
        alarm_name=$(echo "$line" | awk -F':' '{print $1}')
        alarm_id=$(echo "$line" | awk -F':' '{print $2}')
        severity=$(echo "$line" | awk -F':' '{print $3}')
        status=$(echo "$line" | awk -F':' '{print $4}')

        # Use OCI CLI to retrieve alarm history and count the occurrences
        history_count=$(oci monitoring alarm-history-collection get-alarm-history --alarm-id "$alarm_id" --timestamp-greater-than-or-equal-to "$timestamp_greater_than" --query 'data | entries' --raw-output 2>/dev/null | jq 'length')

        # Aggregate the counts by AlarmID and Severity
        # alarm_counts["$alarm_id,$severity"]="$history_count"
        alarm_counts["$alarm_name,$alarm_id,$severity,$status"]=$((alarm_counts["$alarm_name,$alarm_id,$severity,$status"] + history_count))
        
    done <<< "$alarm_data"

    # Print the aggregated counts
    for key in "${!alarm_counts[@]}"; do
        echo "AlarmName,AlarmID,Severity,Status: $key, Count: ${alarm_counts[$key]}"
    done
}

# Check if the number of arguments is correct
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <compartment_id> <number of days>"
    exit 1
fi

# Store the compartment_id parameter
compartment_id="$1"
hist_days="$2"

# Validate num_days
if ! [[ "$hist_days" =~ ^[0-9]+$ ]]; then
    echo "Error: Number of days must be a positive integer."
    exit 1
fi

# Calculate the timestamp
timestamp_greater_than=$(calculate_timestamp "$hist_days")

# Retrieve alarm information and store it in a variable
alarm_data=$(get_alarm_info "$compartment_id" | jq '.[] | .AlarmName+":"+.AlarmID+":"+.Severity+":"+.Status' | tr -d '"')

# Check if there are any alarms
if [ -z "$alarm_data" ]; then
    echo "No alarms found in the compartment."
else
    # Aggregate and print alarm history per AlarmID and group by severity
    echo "Aggregated alarm history by AlarmID and Severity:"
    aggregate_alarm_history "$alarm_data" "$timestamp_greater_than"
fi

# Add your additional main logic here if needed.
