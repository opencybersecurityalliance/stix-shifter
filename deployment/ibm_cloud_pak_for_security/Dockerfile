FROM registry.access.redhat.com/ubi8/ubi-minimal
ARG APP
ARG VERSION

USER root

RUN microdnf update -y && rm -fr /var/cache/yum && \
    microdnf update -y gnutls systemd kernel-headers && \
    microdnf install --nodocs python3 python3-devel unzip openssl && \
    rm -fr /var/cache/yum && microdnf update -y && rm -rf /var/cache/yum && \
    microdnf clean all

COPY ./bundle/ /opt/app/
RUN chown -R 1001 /opt/app/
RUN python3 -m pip install --upgrade pip
RUN pip3 install 'cryptography==3.4.7'
RUN pip3 install 'pyopenssl==21.0.0'

USER 1001

WORKDIR /opt/app

LABEL name=${APP} \
	vendor="IBM" \
	summary="${APP} connector for CP4S UDI service." \
  # CP4S release
	release="1.10.0.0" \
  # Connector version taken from STIX-shifter release
	version="4.0.8" \
	description="${APP} connector for CP4S UDI service." \
	# Comma-delineated list of compatible CP4S releases
	compatibleReleases="1.10.0.0" 
