FROM ubuntu:14.04

MAINTAINER Quanlong He <kyan.ql.he@gmail.com>

RUN echo "deb http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse" > /etc/apt/sources.list && \
echo "deb http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y dnsmasq syslinux wget

# Install pxelinux.0
RUN mkdir /app && cp /usr/lib/syslinux/pxelinux.0 /app/

# s,10.0.1.6:8000,10.0.1.6:8000,gI
# Install coreos pxe images
# RUN cd /app && \
#     wget -q http://10.0.1.6:8000/coreos_production_pxe.vmlinuz && \
#     wget -q http://10.0.1.6:8000/coreos_production_pxe.vmlinuz.sig && \
#     wget -q http://10.0.1.6:8000/coreos_production_pxe_image.cpio.gz && \
#     wget -q http://10.0.1.6:8000/coreos_production_pxe_image.cpio.gz.sig

#     wget -qO- https://coreos.com/security/image-signing-key/CoreOS_Image_Signing_Key.pem | gpg --import && \
#     gpg --verify coreos_production_pxe.vmlinuz.sig && \
#     gpg --verify coreos_production_pxe_image.cpio.gz.sig

COPY app /app
COPY config /config

# RUN chmod 644 pxe/pxelinux.cfg/default && \
#     chmod 644 pxe/pxelinux.0 && \
#     chmod 644 pxe/coreos_production_pxe_image.cpio.gz && \
#     chmod 644 pxe/coreos_production_pxe.vmlinuz

# Customizations
ENV INTERFACE=eth1

CMD /app/init
