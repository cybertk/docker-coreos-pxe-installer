# docker-coreos-pxe-installer

> Bootstrap CoreOS cluster via PXE in seconds

[![Docker Repository on Quay.io](https://quay.io/repository/quanlong/coreos-pxe-installer/status "Docker Repository on Quay.io")](https://quay.io/repository/quanlong/coreos-pxe-installer)

## Getting started

    docker run --net=host quanlong/coreos-pxe-installer

If you run docker under VM, make sure the VM's network is bridged to the network of your DHCP server. For vagrant, it's `config.vm.network "public_network"`

Use `ENV INTERFACE` to customize your interface if it's not eth1 in your host

    docker run --net=host -e INTERFACE=eth0 quanlong/coreos-pxe-installer

## Customizations

You can override /config dir to customize **coreos-pxe-installer**'s behavior. To get started you can simply link via

    docker run -v myconfig:/config quanlong/coreos-pxe-installer

The default configurations will installed under `myconfig` dir, you can edit the default config to start quickly.

There are some template variables you can use in the configurations, **coreos-pxe-installer** will replace them to real value when provisioning.

### Templates variables

- `server_ip`, current server ipv4 address
- `client_ip`, current client ipv4 address
- `client_ip_dash`, replace `.` to `-` of `client_ip`
- `etcd_discovery_token`, etcd Discovery Token

### Adding a Custom OEM

To add cloud config in initramfs, see https://coreos.com/docs/running-coreos/bare-metal/booting-with-pxe/

## Install on disk

## Test

test cloud-config with `coreos-cloudinit -validate`, see https://coreos.com/validate

## Contribution

vagrant for dev environment, link `app/config` into container for quick debuging

    vagrant up; vagrant ssh
    cd /vagrant
    docker build -t installer .
    docker run -v /vagrant/app/config:/config --net=host installer

## References

- https://coreos.com/docs/running-coreos/platforms/vagrant/
- https://github.com/dsbaars/vagrant-pxe
- https://support.microsoft.com/en-us/kb/244036
- http://www.syslinux.org/wiki/index.php/PXELINUX
- http://blog.turret.io/launch-coreos-instances-with-pixe-and-cloud-config/
