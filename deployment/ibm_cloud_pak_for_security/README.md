# Build and deploy connector images into IBM Cloud Pak for Security (CP4S)

The scripts contained here allow you to build an image of a new or existing connector, and deploy that image into your Kubernetes cluster on your CP4S environment. The are also options for deploying an existing image from a Public registry such as docker hub and for building an image locally so that you may publish it to a registry of your choice. 

The `deploy` script automatically: 

1. Installs the required Python libraries.
2. [Packages the desired stix-shifter module](https://github.com/opencybersecurityalliance/stix-shifter/blob/master/adapter-guide/develop-stix-adapter.md#Packaging-individual-connectors) into a wheel file.
3. Builds a container image from that wheel file.
4. Signs the image if a certificate is present.
5. Deploys the image into your cluster.

## Prerequisites

The following needs to be installed on your local machine: 
* Python 3
* Podman (Other Container manangement tool can be used such as Docker)
* OpenShift CLI (`oc`)
* Kubernetes CLI (`kubectl`)
* OpenSSL (`openssl`)

Since the primary use-case for these scripts is to install a new or updated connector, it is assumed you have already cloned the [stix-shifter github project](https://github.com/opencybersecurityalliance/stix-shifter).

## Installing a stix-shifter connector into CP4S

1. Open a terminal
2. CD into the root `stix-shifter` directory
3. Build the `requirements.txt` file using the supplied script: `python3 generate_requirements.py`
4. Install the python libraries required by stix-shifter: `pip3 install -r requirements.txt`
5. Install the python libraries required for packaging: `pip3 install setuptools wheel twine jsonmerge`
6. CD into `stix-shifter/deployment/ibm_cloud_pak_for_security`
7. For an IBM validated connector, copy the `cert.key` and `cert.pem` files that you received from IBM into the current `ibm_cloud_pak_for_security` directory.
8. Log into your CP4S cluster: 

    `cloudctl login -a <ICP CLUSTER URL> -u <USERNAME> -p <PASSWORD> -n <NAMESPACE>`

    OR

    `oc login -u <USER> --server=<SERVER URL>`

    Note: there is a known issue when logged in as `kubeadmin` user via oc command, `oc login -u kubeadmin`

9. Run the deployment script based on one of the following scenarios:

    ### A. Build the connector image and then deploy into your Kubernetes cluster
    ```
    ./deploy.sh <MODULE NAME> remote [-n <NAMESPACE>]
    ```  
    (Ex: `./deploy.sh elastic_ecs remote -n cp4s`)

    ### B. Deploy an existing connector image from a registry into your Kubernetes cluster
    ```
    ./deploy.sh <MODULE NAME> remote <IMAGE PATH> [-n <NAMESPACE>]
    ```
    (Ex: `./deploy.sh elastic_ecs remote docker.io/<REPOSITORY>/stix_shifter_modules_CONNECTORNAME:tag`)

    ### C. Build the connector image locally without deployment
    ```
    ./deploy.sh <MODULE NAME> local
    ``` 
    (Ex: `./deploy.sh elastic_ecs local`)

    When making a remote build, [-n < NAMESPACE >] flag is optional. If not supplied, the namespace will be obtained from the current namespace project of the cluster you are logged in.

