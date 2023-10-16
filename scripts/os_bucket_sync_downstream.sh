#!/bin/bash

# Function to display usage information
display_usage() {
    echo "Usage: $0 <compartment_id> <instance_name> <bucket_name> <dest_dir>"
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

# Function to retrieve instance OCID and set bucket folder prefix
retrieve_instance_ocid() {
    inst_ocid=$(oci compute instance list -c "$compartment_id" --display-name "$instance_name" | jq -r '.data[].id')
    if [ -z "$inst_ocid" ]; then
        echo "Instance not found"
        exit 1
    else
        bucket_folder_prefix="$instance_name/$inst_ocid/"
    fi

}

# Function to sync source directory files to bucket
bucket_sync_upstream() {
    oci os object sync -bn "$bucket_name" --prefix "$bucket_folder_prefix" --src-dir "$src_dir"
}

# Function to sync bucket with destination directory
bucket_sync_downstream() {
    oci os object sync -bn "$bucket_name" --dest-dir "$dest_dir"
}

# Check if the number of arguments is correct
if [ $# -ne 4 ]; then
    display_usage
    exit 1
fi

# Assign parameters to variables
compartment_id="$1"
instance_name="$2"
bucket_name="$3"
dest_dir="$4"

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

# Validate OCI CLI
check_oci_cli

# Validate jq
check_jq

# Validate each parameter
validate_compartment_id
validate_bucket_name

# Retrieve instance OCID
retrieve_instance_ocid

# Sync bucket to downstream filesystem destination directory
bucket_sync_downstream

# Main logic
echo "Compartment ID: $compartment_id"
echo "Instance Name: $instance_name"
echo "Bucket Name: $bucket_name"
echo "Instance OCID: $inst_ocid"
echo "Destination Directory: $dest_dir"

echo "Destination directory files synced from the bucket"

echo "Script execution completed"
