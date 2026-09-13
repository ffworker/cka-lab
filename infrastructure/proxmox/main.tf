locals {
  nodes = {
    control_plane = {
      name       = "cka-cp01"
      vm_id      = 110
      cores      = 2
      memory_mb  = 2048
      disk_gb    = 24
      ip_address = var.control_plane_address
      role       = "control-plane"
    }
    worker = {
      name       = "cka-worker01"
      vm_id      = 111
      cores      = 1
      memory_mb  = 2048
      disk_gb    = 24
      ip_address = var.worker_address
      role       = "worker"
    }
  }
}

resource "proxmox_virtual_environment_vm" "cka_node" {
  for_each = local.nodes

  name            = each.value.name
  node_name       = var.proxmox_node_name
  vm_id           = each.value.vm_id
  pool_id         = "cka-factory"
  started         = true
  on_boot         = false
  stop_on_destroy = true
  tags            = ["cka", "cka-factory", "disposable", each.value.role]

  clone {
    vm_id = var.template_vm_id
    full  = true
  }

  agent {
    enabled = true
  }

  cpu {
    cores = each.value.cores
    type  = "host"
  }

  memory {
    dedicated = each.value.memory_mb
    floating  = each.value.memory_mb
  }

  disk {
    datastore_id = var.datastore_id
    interface    = "scsi0"
    size         = each.value.disk_gb
  }

  network_device {
    bridge = var.network_bridge
    model  = "virtio"
  }

  initialization {
    datastore_id = var.datastore_id

    dns {
      servers = var.dns_servers
    }

    ip_config {
      ipv4 {
        address = each.value.ip_address
        gateway = var.gateway
      }
    }

    user_account {
      username = var.admin_username
      keys     = var.ssh_public_keys
    }
  }

  lifecycle {
    precondition {
      condition     = contains([110, 111], each.value.vm_id)
      error_message = "The CKA factory may manage only reserved VM IDs 110 and 111."
    }
  }
}
