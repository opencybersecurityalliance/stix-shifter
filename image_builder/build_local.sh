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

FILE_PREFIX=stix_shifter_modules_
TIMESTAMP=`date '+%Y%m%d%H%M%S'`


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


echo "Parsed project name: ${PROJECT_NAME}"
echo "Parsed project version: ${PROJECT_VERSION}"
echo "Project tag: ${TAG}"


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

IMAGE_LOCAL_URL=${FILE_PREFIX}${PROJECT_NAME}:${TAG}
echo "Building image..."
docker build --no-cache -t ${IMAGE_LOCAL_URL} --build-arg APP=${FILENAME%.whl} --build-arg VERSION=${PROJECT_VERSION} .


echo "Done!"
