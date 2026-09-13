variable "proxmox_endpoint" {
  description = "Proxmox API URL, for example https://proxmox.example:8006/"
  type        = string
}

variable "proxmox_api_token" {
  description = "API token supplied through TF_VAR_proxmox_api_token"
  type        = string
  sensitive   = true
}

variable "proxmox_insecure" {
  type    = bool
  default = false
}

variable "proxmox_node_name" {
  type    = string
  default = "proxmox.example"
}

variable "template_vm_id" {
  description = "Cloud-init template VM ID reserved for the disposable factory"
  type        = number
}

variable "datastore_id" {
  type    = string
  default = "local-lvm"
}

variable "network_bridge" {
  type    = string
  default = "vmbr1"
}

variable "gateway" {
  type = string
}

variable "control_plane_address" {
  type = string
}

variable "worker_address" {
  type = string
}

variable "admin_username" {
  type    = string
  default = "cka"
}

variable "ssh_public_keys" {
  type = list(string)
}
