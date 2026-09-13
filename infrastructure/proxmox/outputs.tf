output "nodes" {
  description = "Disposable CKA nodes; VMs remain stopped after creation"
  value = {
    for key, vm in proxmox_virtual_environment_vm.cka_node : key => {
      name       = vm.name
      vm_id      = vm.vm_id
      ip_address = local.nodes[key].ip_address
    }
  }
}
