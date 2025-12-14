#!/bin/bash

# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



# Capture arguments from Python
PROJECT_ID=$1
REGION=$2
PASSWORD=$3
CLUSTER_ID=$4
INSTANCE_ID=$5
VPC_NAME="easy-alloydb-vpc"
SUBNET_NAME="easy-alloydb-subnet"
PSA_RANGE_NAME="easy-alloydb-psa-range"

echo "Starting deployment for Project: $PROJECT_ID..."

# 1. Config Project
gcloud config set project $PROJECT_ID

# 2. Enable APIs
gcloud services enable alloydb.googleapis.com servicenetworking.googleapis.com compute.googleapis.com

# 3. Network Setup
# Check if VPC exists to avoid errors on re-runs
if ! gcloud compute networks describe $VPC_NAME --global > /dev/null 2>&1; then
    gcloud compute networks create $VPC_NAME --subnet-mode=custom --bgp-routing-mode=global
fi

if ! gcloud compute networks subnets describe $SUBNET_NAME --region=$REGION > /dev/null 2>&1; then
    gcloud compute networks subnets create $SUBNET_NAME --region=$REGION --network=$VPC_NAME --range="10.0.0.0/24"
fi

# 4. Private Services Access
if ! gcloud compute addresses describe $PSA_RANGE_NAME --global > /dev/null 2>&1; then
    gcloud compute addresses create $PSA_RANGE_NAME --global --purpose=VPC_PEERING --prefix-length=16 --network=$VPC_NAME
    gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --ranges=$PSA_RANGE_NAME --network=$VPC_NAME
fi

# 5. Create Cluster
gcloud alloydb clusters create $CLUSTER_ID --region=$REGION --network=$VPC_NAME --password=$PASSWORD

# 6. Create Instance
gcloud alloydb instances create $INSTANCE_ID --cluster=$CLUSTER_ID --region=$REGION --cpu-count=2 --instance-type=PRIMARY

echo "Deployment Complete. Check Console."
