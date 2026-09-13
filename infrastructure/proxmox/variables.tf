variable "proxmox_endpoint" {
  description = "Proxmox API URL, for example https://proxmox.example.com:8006/"
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
  description = "Proxmox node that hosts the disposable factory guests"
  type        = string
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

  validation {
    condition     = var.network_bridge == "vmbr1"
    error_message = "The CKA factory is restricted to the isolated vmbr1 bridge."
  }
}

variable "gateway" {
  type = string
}

variable "dns_servers" {
  description = "Resolvers reachable from the isolated lab subnet"
  type        = list(string)
  default     = ["1.1.1.1", "9.9.9.9"]
}

variable "control_plane_address" {
  type = string
}

variable "worker_address" {
  type = string
}

variable "admin_username" {
  description = "Cloud-init account used by Ansible"
  type        = string

  validation {
    condition     = can(regex("^[a-z_][a-z0-9_-]{0,31}$", var.admin_username))
    error_message = "admin_username must be a valid Linux account name using lowercase letters, digits, underscores, or hyphens."
  }
}

variable "ssh_public_keys" {
  type = list(string)
}
