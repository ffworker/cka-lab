# Ansible kubeadm skeleton

`site.yml` establishes the common, control-plane, and worker role boundaries for
future kubeadm automation. The roles currently stop at explicit debug markers;
they do not install packages, initialize Kubernetes, or change any host.

Copy `inventory.example.yml` to an ignored local inventory before future use.
