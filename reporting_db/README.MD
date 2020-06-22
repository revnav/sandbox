# Reporting DB install and setup

## Deploy the Instance, install 18c database and configure Apex on port 8080

##Requirements

## First set the environment. cen2020.env file contains the "cen2020" OCI tenancy information. Please make sure update this .env file suitable to your OCI tenancy.
## make sure ~/.oci/config file contains the connection information for the tenancy you are deploying

## Source the env
. ./cen2020.env

## Deploy the db machine.
ansible-playbook DB_Instance_Provision.yaml

## terminate the instance_id. Make sure to provide the instance ocid in the command line below

ansible-playbook teardown.yaml -e "instance_id=ocid1.instance.oc1.xxxxxxxxxxx"
