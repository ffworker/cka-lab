#!/usr/bin/env bash
set -euo pipefail

ACTION=${1:?usage: lab-factory.sh lab-up|lab-down [runtime-dir]}
REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
RUNTIME_DIR=${2:-"$REPO/.cka-factory"}
mkdir -p "$RUNTIME_DIR"
RUNTIME_DIR=$(cd "$RUNTIME_DIR" && pwd)
chmod 700 "$RUNTIME_DIR"
TF_DIR="$REPO/infrastructure/proxmox"
ANSIBLE_DIR="$REPO/ansible"
ENV_FILE="$RUNTIME_DIR/proxmox.env"
INVENTORY="$RUNTIME_DIR/inventory.yml"
KUBECONFIG_FILE="$RUNTIME_DIR/kubeconfig"
KNOWN_HOSTS="$RUNTIME_DIR/known_hosts"
TUNNEL_SOCKET="$RUNTIME_DIR/kube-api.sock"
TUNNEL_PORT=16443
EXPECTED_STATE=(
  'proxmox_virtual_environment_vm.cka_node["control_plane"]'
  'proxmox_virtual_environment_vm.cka_node["worker"]'
)

fail() {
  printf 'cka-factory: %s\n' "$*" >&2
  exit 1
}

require_file() {
  [[ -f "$1" ]] || fail "missing required local file: $1"
}

require_private_file() {
  require_file "$1"
  [[ ! -L "$1" ]] || fail "$1 must not be a symbolic link"
  [[ "$(stat -c '%u' "$1")" == "$(id -u)" ]] || fail "$1 must be owned by the current user"
  [[ "$(stat -c '%a' "$1")" == "600" ]] || fail "$1 must have mode 0600"
}

load_api_token() {
  local lines
  mapfile -t lines <"$ENV_FILE"
  [[ "${#lines[@]}" -eq 1 ]] || fail "$ENV_FILE must contain exactly one assignment"
  [[ "${lines[0]}" != *REPLACE_WITH_TOKEN_SECRET* ]] ||
    fail "replace REPLACE_WITH_TOKEN_SECRET in $ENV_FILE before running make lab-up"
  [[ "${lines[0]}" =~ ^TF_VAR_proxmox_api_token=cka-factory@pve!terraform=[A-Za-z0-9-]+$ ]] ||
    fail "$ENV_FILE contains an invalid assignment"
  export TF_VAR_proxmox_api_token="${lines[0]#TF_VAR_proxmox_api_token=}"
}

state_list() {
  if [[ ! -f "$TF_DIR/terraform.tfstate" ]]; then
    return 0
  fi
  terraform -chdir="$TF_DIR" state list
}

state_is_exact() {
  local actual expected
  actual=$(state_list | sort)
  expected=$(printf '%s\n' "${EXPECTED_STATE[@]}" | sort)
  [[ "$actual" == "$expected" ]]
}

assert_state_bindings() {
  terraform -chdir="$TF_DIR" show -json |
    python3 -c '
import json, sys
expected = {
    "proxmox_virtual_environment_vm.cka_node[\"control_plane\"]": (110, "cka-cp01", "cka-factory"),
    "proxmox_virtual_environment_vm.cka_node[\"worker\"]": (111, "cka-worker01", "cka-factory"),
}
root = json.load(sys.stdin).get("values", {}).get("root_module", {})
actual = {
    resource["address"]: (
        resource["values"].get("vm_id"),
        resource["values"].get("name"),
        resource["values"].get("pool_id"),
    )
    for resource in root.get("resources", [])
}
if actual != expected:
    raise SystemExit(f"unsafe Terraform state bindings: {actual!r}")
'
}

live_vm_record() {
  local id=$1
  ssh -o BatchMode=yes proxmox \
    "pvesh get /cluster/resources --type vm --output-format json" |
    python3 -c 'import json,sys; vmid=int(sys.argv[1]); rows=[x for x in json.load(sys.stdin) if x.get("vmid")==vmid]; print("" if not rows else "|".join(str(rows[0].get(k,"")) for k in ("name","tags","pool")))' "$id"
}

record_guest_host_key() {
  local id=$1 ip=$2 response key_record
  for _ in $(seq 1 60); do
    if response=$(ssh -o BatchMode=yes proxmox \
      "qm guest exec $id -- cat /etc/ssh/ssh_host_ed25519_key.pub" 2>/dev/null) &&
      key_record=$(python3 -c '
import json, sys
ip = sys.argv[1]
payload = json.load(sys.stdin)
parts = payload.get("out-data", "").split()
if payload.get("exitcode") != 0 or len(parts) < 2 or parts[0] != "ssh-ed25519":
    raise SystemExit(1)
print(f"{ip} {parts[0]} {parts[1]}")
' "$ip" <<<"$response"); then
      printf '%s\n' "$key_record" >>"$KNOWN_HOSTS"
      return 0
    fi
    sleep 5
  done
  fail "could not retrieve the trusted SSH host key for VM $id"
}

assert_live_ownership() {
  local id=$1 expected_name=$2 record name tags pool
  record=$(live_vm_record "$id")
  [[ -n "$record" ]] || fail "expected VM $id is absent"
  IFS='|' read -r name tags pool <<<"$record"
  [[ "$name" == "$expected_name" ]] || fail "VM $id name mismatch: $name"
  [[ ";$tags;" == *';cka-factory;'* ]] || fail "VM $id lacks cka-factory ownership tag"
  [[ "$pool" == "cka-factory" ]] || fail "VM $id is not in the cka-factory pool"
}

assert_no_untracked_collisions() {
  local actual record
  actual=$(state_list) || fail "unable to read Terraform state"
  if [[ -z "$actual" ]]; then
    for id in 110 111; do
      record=$(live_vm_record "$id")
      [[ -z "$record" ]] || fail "VM ID $id already exists but is not tracked by this factory state"
    done
  else
    state_is_exact || fail "Terraform state contains resources outside the two CKA VMs"
    assert_state_bindings || fail "Terraform state is not bound to the reserved CKA IDs"
    assert_live_ownership 110 cka-cp01
    assert_live_ownership 111 cka-worker01
  fi
}

close_tunnel() {
  if [[ -S "$TUNNEL_SOCKET" ]]; then
    ssh -S "$TUNNEL_SOCKET" -O exit proxmox >/dev/null 2>&1 || true
    rm -f "$TUNNEL_SOCKET"
  fi
}

case "$ACTION" in
  lab-up)
    require_private_file "$ENV_FILE"
    require_file "$TF_DIR/terraform.tfvars"
    load_api_token

    terraform -chdir="$TF_DIR" init -input=false
    assert_no_untracked_collisions
    terraform -chdir="$TF_DIR" apply -input=false -auto-approve
    state_is_exact || fail "post-apply Terraform state is not limited to the two CKA VMs"
    assert_state_bindings || fail "post-apply state is not bound to the reserved CKA IDs"
    assert_live_ownership 110 cka-cp01
    assert_live_ownership 111 cka-worker01

    cp_ip=$(terraform -chdir="$TF_DIR" output -json nodes | python3 -c 'import json,sys; print(json.load(sys.stdin)["control_plane"]["ip_address"].split("/")[0])')
    worker_ip=$(terraform -chdir="$TF_DIR" output -json nodes | python3 -c 'import json,sys; print(json.load(sys.stdin)["worker"]["ip_address"].split("/")[0])')
    admin_username=$(terraform -chdir="$TF_DIR" output -raw admin_username)
    : >"$KNOWN_HOSTS"
    chmod 600 "$KNOWN_HOSTS"
    record_guest_host_key 110 "$cp_ip"
    record_guest_host_key 111 "$worker_ip"
    for ip in "$cp_ip" "$worker_ip"; do
      printf 'Waiting for SSH on %s...\n' "$ip"
      ready=false
      for _ in $(seq 1 60); do
        if ssh -o BatchMode=yes -o ConnectTimeout=5 -o ProxyJump=proxmox \
          -o StrictHostKeyChecking=yes -o UserKnownHostsFile="$KNOWN_HOSTS" \
          "${admin_username}@$ip" true >/dev/null 2>&1; then
          ready=true
          break
        fi
        sleep 5
      done
      [[ "$ready" == true ]] || fail "SSH did not become ready on $ip"
      set +e
      ssh -o BatchMode=yes -o ProxyJump=proxmox \
        -o StrictHostKeyChecking=yes -o UserKnownHostsFile="$KNOWN_HOSTS" \
        "${admin_username}@$ip" sudo cloud-init status --wait >/dev/null
      cloud_init_rc=$?
      set -e
      [[ "$cloud_init_rc" -le 2 ]] || fail "cloud-init failed on $ip (status $cloud_init_rc)"
    done

    cat >"$INVENTORY" <<EOF
all:
  children:
    control_plane:
      hosts:
        cka-cp01:
          ansible_host: $cp_ip
    workers:
      hosts:
        cka-worker01:
          ansible_host: $worker_ip
  vars:
    ansible_user: '$admin_username'
    ansible_become: true
    ansible_ssh_common_args: '-o ProxyJump=proxmox -o UserKnownHostsFile=$KNOWN_HOSTS -o StrictHostKeyChecking=yes'
    kubernetes_version: v1.37
    pod_network_cidr: 10.244.0.0/16
    flannel_version: v0.28.8
    local_kubeconfig_path: $KUBECONFIG_FILE
EOF
    chmod 600 "$INVENTORY"

    ANSIBLE_CONFIG="$ANSIBLE_DIR/ansible.cfg" ansible-playbook -i "$INVENTORY" "$ANSIBLE_DIR/site.yml"
    chmod 600 "$KUBECONFIG_FILE"

    close_tunnel
    ssh -M -S "$TUNNEL_SOCKET" -fNT -o ExitOnForwardFailure=yes \
      -L "127.0.0.1:${TUNNEL_PORT}:${cp_ip}:6443" proxmox
    KUBECONFIG="$KUBECONFIG_FILE" kubectl config set-cluster kubernetes \
      --server="https://127.0.0.1:${TUNNEL_PORT}" --tls-server-name="$cp_ip" >/dev/null
    KUBECONFIG="$KUBECONFIG_FILE" kubectl wait --for=condition=Ready \
      node/cka-cp01 node/cka-worker01 --timeout=300s
    KUBECONFIG="$KUBECONFIG_FILE" kubectl rollout status \
      daemonset/kube-flannel-ds -n kube-flannel --timeout=180s
    KUBECONFIG="$KUBECONFIG_FILE" kubectl rollout status \
      deployment/coredns -n kube-system --timeout=180s
    count=$(KUBECONFIG="$KUBECONFIG_FILE" kubectl get nodes -o name | wc -l)
    [[ "$count" -eq 2 ]] || fail "expected exactly two Kubernetes nodes, found $count"
    KUBECONFIG="$KUBECONFIG_FILE" kubectl get nodes -o wide
    ;;
  lab-down)
    require_private_file "$ENV_FILE"
    require_file "$TF_DIR/terraform.tfvars"
    load_api_token
    terraform -chdir="$TF_DIR" init -input=false
    current_state=$(state_list) || fail "unable to read Terraform state"
    if [[ -z "$current_state" ]]; then
      for id in 110 111; do
        [[ -z "$(live_vm_record "$id")" ]] ||
          fail "refusing empty-state teardown: untracked VM ID $id exists"
      done
      printf 'lab-down: no factory resources are tracked; nothing removed\n'
      close_tunnel
      exit 0
    fi
    state_is_exact || fail "refusing destroy: Terraform state is not exactly the two CKA VMs"
    assert_state_bindings || fail "refusing destroy: state is not bound to reserved IDs 110 and 111"
    assert_live_ownership 110 cka-cp01
    assert_live_ownership 111 cka-worker01
    close_tunnel
    terraform -chdir="$TF_DIR" destroy -input=false -auto-approve
    current_state=$(state_list) || fail "unable to read post-destroy Terraform state"
    [[ -z "$current_state" ]] || fail "Terraform state is not empty after destroy"
    [[ -z "$(live_vm_record 110)" ]] || fail "VM 110 still exists after destroy"
    [[ -z "$(live_vm_record 111)" ]] || fail "VM 111 still exists after destroy"
    rm -f "$INVENTORY" "$KUBECONFIG_FILE" "$KNOWN_HOSTS"
    printf 'lab-down: removed only cka-cp01 (110) and cka-worker01 (111)\n'
    ;;
  *)
    fail "unsupported action: $ACTION"
    ;;
esac
