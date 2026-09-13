# Ansible kubeadm bootstrap

`site.yml` installs containerd and Kubernetes packages, initializes the control
plane, installs pinned Flannel, joins the worker, and fetches kubeconfig.

The factory generates ignored inventory under `.cka-factory/` and reaches the
private `vmbr1` subnet through the `proxmox` SSH jump host.
