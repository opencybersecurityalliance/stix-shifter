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
RUN pip3 install 'cryptography==2.9.2'
RUN pip3 install 'pyopenssl==19.1.0'

USER 1001

WORKDIR /opt/app

LABEL name=${APP} \
	vendor="IBM" \
	summary="${APP} connector for CP4S UDI service." \
	release="1.4.0.0" \
	version=${VERSION} \
	description="${APP} connector for CP4S UDI service."
