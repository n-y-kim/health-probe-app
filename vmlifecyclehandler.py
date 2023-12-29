#!/usr/bin/python3

from logconfig import logger
from configuration import config
# from vminstance import VMInstance
import requests, json, os
import datetime

from InstanceMetadata import InstanceMetadata
from bearer_token import BearerAuth

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

vmInstance = InstanceMetadata().populate()
logger.info(vmInstance)

def get_blob_service_client_token_credential():
    # TODO: Replace <storage-account-name> with your actual storage account name
    account_url = "https://scloudstorage.blob.core.windows.net"
    credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    return blob_service_client

def upload_blob_file(blob_service_client: BlobServiceClient, container_name: str):
    container_client = blob_service_client.get_container_client(container=container_name)
    with open(file=os.path.join('/app/log', 'delete_vmss_instance.log'), mode="rb") as data:
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        blob_client = container_client.upload_blob(name="delete_vmss_instance(" + time + ").log", data=data, overwrite=True)

class VMLifecycleHandler:
    """
        Here is where we need to put all the custom tasks that need to be performed
    """
    def  performCustomOperation():
        logger.info("Performing custom operation")

        ## This is where the custom logic will go
        logger.info("Saving log files to Blob storage...")
        blob_service_client = get_blob_service_client_token_credential()
        upload_blob_file(blob_service_client, "log-drop")

    """
    This will call the health Probe URL and fail it
    """
    def failLoadBalancerProbes():
        logger.info("Failing Health Probes")
        try:
            kill_health_probe = config.get('shell-commands', 'kill_health_probe_process')
            # Delete all cron jobs
            kill_process = os.system(kill_health_probe)

            if kill_process != 0:
                logger.error("Error killing health probe")
        except:
            logger.error("Error in failing health probe")

    """
    This will kill the cron job which collects and submits custom metric to Azure Monitor
    """
    def stopCustomMetricFlow():
        logger.info("Stopping the Custom Metrics")
        removeCrontab = config.get('shell-commands', 'remove_all_crontab')

        #removeCrontab = "crontab -r"
        # Print the current user
        logger.info("Current user: " + os.getlogin())
        
        logger.info("Deleting all cron jobs")
    
        # Delete all cron jobs
        areCronsRemoved = os.system(removeCrontab)

        if areCronsRemoved != 0:
            logger.error("Error deleting Cron jobs, health probe will not fail")

    if(vmInstance.isPendingDelete()):
        logger.info("Pending Delete is true ...starting custom clean up logic")
        stopCustomMetricFlow()
        performCustomOperation()
    else: 
        logger.info("Instance not in Pending Delete, nothing to do")
