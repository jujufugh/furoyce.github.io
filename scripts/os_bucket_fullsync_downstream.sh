#!/bin/bash

# Function to display usage information
display_usage() {
    echo "Usage: $0 <compartment_id> <bucket_name> <dest_dir>"
}

# Function to check if OCI CLI executable exists
check_oci_cli() {
    if ! command -v oci &> /dev/null; then
        echo "OCI CLI is not installed or not in the PATH"
        exit 1
    fi
}

# Function to check if jq executable exists
check_jq() {
    if ! command -v jq &> /dev/null; then
        echo "jq is not installed or not in the PATH"
        exit 1
    fi
}

# Function to sync bucket with destination directory
bucket_sync_downstream() {
    oci os object sync -bn "$bucket_name" --dest-dir "$dest_dir"
}

# Check if the number of arguments is correct
if [ $# -ne 3 ]; then
    display_usage
    exit 1
fi

# Assign parameters to variables
compartment_id="$1"
bucket_name="$2"
dest_dir="$3"

# Function to validate compartment ID format
validate_compartment_id() {
    comp_id_check=$(oci iam compartment list -c "$compartment_id" | grep -i "ServiceError" | wc -l)
    if [ $comp_id_check -gt 0 ]; then
        echo "Compartment not found"
        exit 1
    fi
}

# Function to validate bucket name format
validate_bucket_name() {
    bucket_name_check=$(oci os object list --bucket-name "$bucket_name" | grep -i "ServiceError" | wc -l)
    if [ $bucket_name_check -gt 0 ]; then
        echo "Bucket Name not found"
        exit 1
    fi
}


# Main logic

# Validate OCI CLI
check_oci_cli

# Validate jq
check_jq

# Validate each parameter
validate_compartment_id
validate_bucket_name

# Sync bucket to downstream filesystem destination directory
bucket_sync_downstream

echo "Compartment ID: $compartment_id"
echo "Bucket Name: $bucket_name"
echo "Destination Directory: $dest_dir"

echo "Destination directory files synced from the bucket"

echo "Script execution completed"
