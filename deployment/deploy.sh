#!/bin/bash

# set -x
set -e

# SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

help() {
    echo -e "\n"
    cat "deployment/deploy-help.txt"
    echo -e "\n" 
}

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    --subscriptionId)
      subscription_id="$2"
      shift # past argument
      shift # past value
      ;;
    --rg-name)
      rg_name="$2"
      shift # past argument
      shift # past value
      ;;
    --location)
      location="$2"
      shift # past argument
      shift # past value
      ;;
    --iotHubName)
      iot_hub_name="$2"
      shift # past argument
      shift # past value
      ;;
    --webAppName)
      web_app_name="$2"
      shift # past argument
      shift # past value
      ;;
    --branchName)
      branch_name="$2"
      shift # past argument
      shift # past value
      ;;
    --targetDevice)
      target_device="$2"
      shift # past argument
      shift # past value
      ;;
    --help)
      help
      exit 0
      ;;
    *)    # unknown option
      echo "Unknown option - $key"
      help
      exit 1;
      ;;
  esac
done

if [ -z "$subscription_id" ]; then
    echo "Subscription ID is a required field"
    help
    exit 1
fi

if [ -z "$rg_name" ]; then
    echo "Resource group name is a required field"
    help
    exit 1
fi

if [ -z "$location" ]; then
    echo "Location is a required field"
    help
    exit 1
fi

if [ -z "$iot_hub_name" ]; then
    echo "IOT Hub Name is a required field"
    help
    exit 1
fi

if [ -z "$web_app_name" ]; then
    echo "Web app Name is a required field"
    help
    exit 1
fi

if [ -z "$branch_name" ]; then
    branch_name="master"
fi

if [ -z "$target_device" ]; then
    echo "Target device is a required field"
    help
    exit 1
fi

az account show

if ! az account show ; then
    az login
fi

az account set --subscription "$subscription_id"

echo "Creating resource group"
az group create --name "$rg_name" --location "$location"
echo "Resource group creation is successful"

echo "Starting the infra deployment"
az deployment group create --name "$web_app_name-infra-deployment" --resource-group "$rg_name" --template-file "deployment/azuredeploy.json" --parameters iotHubName="$iot_hub_name" webAppName="$web_app_name" location="$location" branchName="$branch_name" targetDevice="$target_device"
echo "Infra deployment is successful"

echo "Adding IOT device - $target_device"
az iot hub device-identity create -d "$target_device" --hub-name "$iot_hub_name" -g "$rg_name"
echo "IOT device addition - $target_device was succesful"

echo "Printing the connection string to be used by PIs python code"
az iot hub device-identity connection-string show  -d "$target_device" --hub-name "$iot_hub_name" -g "$rg_name"