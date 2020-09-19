# Build and deploy connector images into IBM Cloud Pak for Security (CP4S)

You can build and publish a docker image of your own connector to any repository. You can also deploy the image to your CP4S cluster with the following steps:

### Prerequisites

1. The following needs to be installed on your local machine: Python 3, Docker, OpenShift CLI (`oc`), Kubernetes CLI (`kubectl`), and OpenSSL (`openssl`).
2. You have built a python wheel distribution artifact of your connector module. Steps are outlined in the [Packaging individual connectors](https://github.com/opencybersecurityalliance/stix-shifter/blob/master/adapter-guide/develop-stix-adapter.md#Packaging-individual-connectors) section of the stix-shifter GitHub project. 

### Installation into CP4S

1. Open a terminal
2. Clone the [stix-shifter github project](https://github.com/opencybersecurityalliance/stix-shifter)
3. CD into the root of the stix-shifter project
4. Generate the requirements file: `python3 generate_requirements.py`
5. Install the required Python libraries: `pip3 install -r requirements.txt`
6. Install the required Python libraries for packaging: `pip3 install setuptools wheel twine jsonmerge` 
7. CD into the `image-builder` directory of the stix-shifter project, this contains the required scripts that will automatically build the connector image.
8. Create a folder named `bundle` inside the `image_builder` directory: (`image_builder/bundle`).
9. Move your connector wheel file (`stix_shifter_modules_<MODULE_NAME>-<VERSION>-py2.py3-none-any.whl`) to the bundle folder created in step 8.
10. For an IBM validated connector, copy the cert and key files that you received from IBM into the `image_builder` folder.
11. Log into your CP4S cluster: 
    ```
    cloudctl login -a <ICP CLUSTER URL> -u <USERNAME> -p <PASSWORD> -n <NAMESPACE>
   ```
12. Run the `build.sh` script.

The image will be built and deployed to your CP4S cluster after successfully running the script.

Instead of building the image from a wheel file, you may deploy an existing image that is already in a repository. In step 12, run `build.sh <IMAGE PATH>`. (Ex: `./build.sh docker.io/<REPOSITORY>/imagename:tag`).

You can also build your docker image without deploying to CP4S. In step 12, run `build_local.sh` instead of `build.sh`. You can then publish the image to your desired repository.