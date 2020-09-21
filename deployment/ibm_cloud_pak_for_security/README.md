# Build and deploy connector images into IBM Cloud Pak for Security (CP4S)

The scripts contained here allow you to build an image of a new or existing connector, and deploy that image into your Kubernetes cluster on your CP4S environment. The are also options for deploying an existing image from a Docker registry and for building an image locally so that you may publish it to a registry of your choice. 

The `deploy` script automatically: 

1. Installs the required Python libraries.
2. [Packages the desired stix-shifter module](https://github.com/opencybersecurityalliance/stix-shifter/blob/master/adapter-guide/develop-stix-adapter.md#Packaging-individual-connectors) into a wheel file.
3. Builds a Docker image from that wheel file.
4. Signs the image if a certificate is present.
5. Deploys the image into your cluster.

## Prerequisites

The following needs to be installed on your local machine: 
* Python 3
* Docker
* OpenShift CLI (`oc`)
* Kubernetes CLI (`kubectl`)
* OpenSSL (`openssl`)

Since the primary use-case for these scripts is to install a new or updated connector, it is assumed you have already cloned the [stix-shifter github project](https://github.com/opencybersecurityalliance/stix-shifter).

## Installing a stix-shifter connector into CP4S

1. Open a terminal
2. CD into `stix-shifter/deployment/ibm_cloud_pak_for_security`
3. For an IBM validated connector, copy the `cert.key` and `cert.pem` files that you received from IBM into the current `ibm_cloud_pak_for_security` directory.
4. Log into your CP4S cluster: 

    `cloudctl login -a <ICP CLUSTER URL> -u <USERNAME> -p <PASSWORD> -n <NAMESPACE>`

5. Run the deployment script based on one of the following scenarios:

    ### A. Build the connector image and then deploy into your Kubernetes cluster
    ```
    ./deploy.sh <MODULE NAME> remote
    ```  
    (Ex: `./deploy.sh elastic_ecs remote`)

    ### B. Deploy an existing connector image from a registry into your Kubernetes cluster
    ```
    ./deploy.sh <MODULE NAME> remote <IMAGE PATH>
    ```
    (Ex: `./deploy.sh elastic_ecs remote docker.io/<REPOSITORY>/stix_shifter_modules_CONNECTORNAME:tag`)

    ### C. Build the connector image locally without deployment
    ```
    ./deploy.sh <MODULE NAME> local
    ``` 
    (Ex: `./deploy.sh elastic_ecs local`)

