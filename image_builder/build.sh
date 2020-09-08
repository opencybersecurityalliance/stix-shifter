#!/bin/bash
set -e

validate_cmd () {
  if ! command -v $1 &> /dev/null
  then
      echo "$1 could not be found"
      exit
  fi

}

IMAGE_URL="$1"

validate_cmd openssl
validate_cmd python3
validate_cmd pip3
validate_cmd docker
validate_cmd kubectl
validate_cmd oc

FILE_PREFIX=stix_shifter_modules_
NAMESPACE=cp4s
TIMESTAMP=`date '+%Y%m%d%H%M%S'`

if [ ! -z "${IMAGE_URL}" ]; then
  echo "IMAGE_URL found: ${IMAGE_URL}"
  FILENAME=${IMAGE_URL##*/}
  PROJECT_NAME=$FILENAME
  PROJECT_NAME=${PROJECT_NAME:${#FILE_PREFIX}}
  PROJECT_NAME=${PROJECT_NAME%%:*}
  # echo "$FILENAME"
  # exit 1

  PROJECT_VERSION=$FILENAME
  PROJECT_VERSION=${PROJECT_VERSION:${#FILE_PREFIX}}
  PROJECT_VERSION=${PROJECT_VERSION:${#PROJECT_NAME}+1}
  # PROJECT_VERSION=${PROJECT_VERSION%%_*} # ? may be not needed
  TAG=$PROJECT_VERSION
else
  DIST_DIR=./bundle
  DIST_DIR_LIBS=${DIST_DIR}/libs
  
  FILENAME=`find ${DIST_DIR} -name ${FILE_PREFIX}*-*.whl | head -n 1`

  if [ -z "$FILENAME" ]; then
    echo "File is not found, expected file name sample: ${DIST_DIR}/${FILE_PREFIX}cloudsql-1.0.0-py2.py3-none-any.whl"
    exit 1
  fi
  FILENAME=${FILENAME:${#DIST_DIR}+1}
  echo "Found file.. ${FILENAME}"

  PROJECT_NAME=$FILENAME
  PROJECT_NAME=${PROJECT_NAME:${#FILE_PREFIX}}
  PROJECT_NAME=${PROJECT_NAME%%-*}
  PROJECT_NAME=${PROJECT_NAME//_/-}

  PROJECT_VERSION=$FILENAME
  PROJECT_VERSION=${PROJECT_VERSION:${#FILE_PREFIX}}
  PROJECT_VERSION=${PROJECT_VERSION:${#PROJECT_NAME}+1}
  PROJECT_VERSION=${PROJECT_VERSION%%-*}
  TAG=${PROJECT_VERSION}_${TIMESTAMP}
fi

echo "Parsed project name: ${PROJECT_NAME}"
echo "Parsed project version: ${PROJECT_VERSION}"
echo "Project tag: ${TAG}"

# exit 1

OC_REGISTRY_NAMESPACE="openshift-image-registry"
echo 'exposing internal registry... (https://docs.openshift.com/container-platform/4.4/registry/securing-exposing-registry.html)'
oc patch configs.imageregistry.operator.openshift.io/cluster --patch '{"spec":{"defaultRoute":true}}' --type=merge
echo -n "Looking for registry url... "
REPOSITORY=$(oc get route default-route -n $OC_REGISTRY_NAMESPACE --template='{{ .spec.host }}')
echo $REPOSITORY



REPOSITORY_CERT_DIR=/etc/docker/certs.d/$REPOSITORY/
REPOSITORY_CERT_FILE=${REPOSITORY_CERT_DIR}/ca.crt
REPOSITORY_CERT_TMP=ca.crt.tmp

if [ ! -f "$REPOSITORY_CERT_FILE" ]; then
  echo "Internal registry uses a self-signed certificate that needs to be added to ${REPOSITORY_CERT_FILE}"

  echo -n "Fetching self-signed certificate... "
  rm -rf $REPOSITORY_CERT_TMP | true
  openssl s_client -showcerts -connect $REPOSITORY:443 < /dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > $REPOSITORY_CERT_TMP

  if grep -Fq "BEGIN CERTIFICATE" $REPOSITORY_CERT_TMP; then
    echo 'Ok'
  else
    echo 'Fail'
    exit 1
  fi

  if [ ! -d "$REPOSITORY_CERT_DIR" ]; then
    echo "Certificate target directory '${REPOSITORY_CERT_DIR}' does not exist"
    echo 'Please enter sudo password to create it...'
    sudo mkdir -p $REPOSITORY_CERT_DIR

    if [ ! -d "$REPOSITORY_CERT_DIR" ]; then
      echo "Failed to create directory"
      exit 1
    fi
      echo "Directory was created successfully"
  fi

  echo 'Please enter sudo password (if required) to copy certificate..'
  sudo cp $REPOSITORY_CERT_TMP $REPOSITORY_CERT_FILE
  rm -rf $REPOSITORY_CERT_TMP | true
  if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -n "Adding certificate to docker VM... "
    sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain $REPOSITORY_CERT_FILE
    echo 'Ok'
    echo -n "Restarting docker... "
    killall Docker && open /Applications/Docker.app
    sleep 60
    echo 'Ok'
  fi
fi

if [ -z "${IMAGE_URL}" ]; then
  if [ ! -d "$DIST_DIR_LIBS" ]; then
    echo '"libs" folder is not present, trying to generate it'
    mkdir ${DIST_DIR_LIBS}
    pip3 download ${DIST_DIR}/${FILENAME} -d ${DIST_DIR_LIBS}
    rm ${DIST_DIR_LIBS}/${FILENAME}
  fi

  if [ ! -d ${DIST_DIR}/meta ]; then
    if [ -f cert.key ] && [ -f cert.pem ]; then
      echo "Found certificates, signing bundle... "
      python3 ./signer.py sign cert.key cert.pem $DIST_DIR
    else
      echo "${DIST_DIR} is not signed, files cert.key and/or cert.pem not found, skipping signing.."
      sleep 5
    fi
  fi
fi

echo "Logging in into internal registry..."
docker login -u `oc whoami` -p `oc whoami -t` $REPOSITORY

if [ ! -z "${IMAGE_URL}" ]; then
  echo "Pulling ${IMAGE_URL}"
  docker pull ${IMAGE_URL}
  IMAGE_LOCAL_URL=${IMAGE_URL}
  IMAGE_PUSH_URL=${REPOSITORY}/${NAMESPACE}/${FILE_PREFIX}${PROJECT_NAME}:${TAG}
  # exit 0
else
  IMAGE_LOCAL_URL=${FILE_PREFIX}${PROJECT_NAME}:${TAG}
  IMAGE_PUSH_URL=${REPOSITORY}/${NAMESPACE}/${IMAGE_LOCAL_URL}
  echo "Building image..."
  docker build --no-cache -t ${IMAGE_LOCAL_URL} --build-arg APP=${FILENAME%.whl} --build-arg VERSION=${PROJECT_VERSION} .
fi

IMAGE_POD_URL=image-registry.openshift-image-registry.svc:5000/${NAMESPACE}/${FILE_PREFIX}${PROJECT_NAME}:${TAG}

echo "retagging image... ${IMAGE_LOCAL_URL} > ${IMAGE_PUSH_URL}"
docker tag ${IMAGE_LOCAL_URL} ${IMAGE_PUSH_URL}

echo "Pushing image..."
docker push ${IMAGE_PUSH_URL}

CR_FILENAME=udi-${PROJECT_NAME}-NEW.yaml
BACKUP_FOLDER=backup_${TIMESTAMP}
mkdir $BACKUP_FOLDER
cd $BACKUP_FOLDER
kubectl get connector --no-headers -o=custom-columns=NAME:.metadata.name | xargs -I{} -n 1 bash -c "kubectl get connector {} -o yaml > {}.yaml"

cat > $CR_FILENAME << EOL
apiVersion: connector.isc.ibm.com/v1
kind: Connector
metadata:
  name: udi-${PROJECT_NAME}
spec:
  type: "UDI"
  version: "${PROJECT_VERSION}"
  creator: "IBM"
  image: "${IMAGE_POD_URL}"
EOL

echo "CR is written to '${BACKUP_FOLDER}/${CR_FILENAME}', applying it"

cat > _restore.sh << EOL
cd "\$(dirname "\$0")"
kubectl get connector --no-headers -o=custom-columns=NAME:.metadata.name | xargs kubectl delete connector
ls -1 *.yaml | grep -v NEW.yaml | xargs -n 1 kubectl apply -f
EOL
chmod u+x ./_restore.sh

kubectl apply -f ${CR_FILENAME} --force

echo "Done!"
echo "No worries you can rollback it with: ./${BACKUP_FOLDER}/_restore.sh"