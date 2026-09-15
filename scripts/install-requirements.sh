#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: scripts/install-requirements.sh [--check|--install]

  --check    Report missing workstation commands without changing the system.
  --install  Install missing commands with the detected Linux package manager.

The installer covers the local workstation tools. It does not create Proxmox
templates, pools, networks, API tokens, or SSH credentials.
EOF
}

MODE=check
case "${1:-}" in
    "") ;;
    --check) MODE=check ;;
    --install) MODE=install ;;
    --help|-h) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
esac

REQUIRED_COMMANDS=(bash python3 make ssh git terraform ansible-playbook kubectl)
MISSING_COMMANDS=()
MISSING_PACKAGES=()
UNAVAILABLE_COMMANDS=()

for command_name in "${REQUIRED_COMMANDS[@]}"; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        MISSING_COMMANDS+=("$command_name")
    fi
done

if [[ "$MODE" == check ]]; then
    if ((${#MISSING_COMMANDS[@]} == 0)); then
        printf 'cka-lab requirements: all workstation commands are available\n'
        exit 0
    fi
    printf 'cka-lab requirements: missing workstation commands:\n'
    printf '  - %s\n' "${MISSING_COMMANDS[@]}"
    printf '\nRun this script with --install to add packages through the detected package manager.\n'
    exit 1
fi

if [[ "$(id -u)" -eq 0 ]]; then
    SUDO=()
elif command -v sudo >/dev/null 2>&1; then
    SUDO=(sudo)
else
    printf 'cka-lab requirements: sudo is required to install system packages\n' >&2
    exit 1
fi

PACKAGE_MANAGER=""
if command -v apt-get >/dev/null 2>&1; then
    PACKAGE_MANAGER=apt
elif command -v dnf >/dev/null 2>&1; then
    PACKAGE_MANAGER=dnf
elif command -v pacman >/dev/null 2>&1; then
    PACKAGE_MANAGER=pacman
elif command -v zypper >/dev/null 2>&1; then
    PACKAGE_MANAGER=zypper
fi

if [[ -z "$PACKAGE_MANAGER" ]]; then
    printf 'cka-lab requirements: no supported package manager found\n' >&2
    printf 'Supported managers: apt-get, dnf, pacman, zypper\n' >&2
    exit 1
fi

package_for_command() {
    local command_name=$1
    case "$PACKAGE_MANAGER:$command_name" in
        apt:bash|dnf:bash|pacman:bash|zypper:bash) printf 'bash' ;;
        apt:python3|dnf:python3|pacman:python3|zypper:python3) printf 'python3' ;;
        apt:make|dnf:make|pacman:make|zypper:make) printf 'make' ;;
        apt:ssh) printf 'openssh-client' ;;
        dnf:ssh) printf 'openssh-clients' ;;
        pacman:ssh) printf 'openssh' ;;
        zypper:ssh) printf 'openssh-clients' ;;
        apt:git|dnf:git|pacman:git|zypper:git) printf 'git' ;;
        apt:terraform|dnf:terraform|pacman:terraform|zypper:terraform) printf 'terraform' ;;
        apt:ansible-playbook|zypper:ansible-playbook) printf 'ansible' ;;
        dnf:ansible-playbook) printf 'ansible-core' ;;
        pacman:ansible-playbook) printf 'ansible' ;;
        apt:kubectl|zypper:kubectl) printf 'kubectl' ;;
        dnf:kubectl) printf 'kubernetes-client' ;;
        pacman:kubectl) printf 'kubectl' ;;
        *) return 1 ;;
    esac
}

package_available() {
    local package_name=$1
    case "$PACKAGE_MANAGER" in
        apt) apt-cache show "$package_name" >/dev/null 2>&1 ;;
        dnf) dnf -q list --available "$package_name" >/dev/null 2>&1 || dnf -q list installed "$package_name" >/dev/null 2>&1 ;;
        pacman) pacman -Si "$package_name" >/dev/null 2>&1 ;;
        zypper) zypper --non-interactive info "$package_name" >/dev/null 2>&1 ;;
    esac
}

for command_name in "${MISSING_COMMANDS[@]}"; do
    if package_name=$(package_for_command "$command_name") && package_available "$package_name"; then
        MISSING_PACKAGES+=("$package_name")
    else
        UNAVAILABLE_COMMANDS+=("$command_name")
    fi
done

if ((${#MISSING_PACKAGES[@]} > 0)); then
    unique_packages=()
    for package_name in "${MISSING_PACKAGES[@]}"; do
        if [[ ! " ${unique_packages[*]} " == *" $package_name "* ]]; then
            unique_packages+=("$package_name")
        fi
    done
    printf 'Installing with %s: %s\n' "$PACKAGE_MANAGER" "${unique_packages[*]}"
    case "$PACKAGE_MANAGER" in
        apt)
            "${SUDO[@]}" apt-get update
            "${SUDO[@]}" apt-get install -y --no-install-recommends "${unique_packages[@]}"
            ;;
        dnf) "${SUDO[@]}" dnf install -y "${unique_packages[@]}" ;;
        pacman) "${SUDO[@]}" pacman -S --needed --noconfirm "${unique_packages[@]}" ;;
        zypper) "${SUDO[@]}" zypper --non-interactive install "${unique_packages[@]}" ;;
    esac
fi

if ((${#UNAVAILABLE_COMMANDS[@]} > 0)); then
    printf '\nThese commands were not available from the configured %s repositories:\n' "$PACKAGE_MANAGER" >&2
    printf '  - %s\n' "${UNAVAILABLE_COMMANDS[@]}" >&2
    printf '\nInstall them from the official vendor instructions, then rerun --check:\n' >&2
    for command_name in "${UNAVAILABLE_COMMANDS[@]}"; do
        case "$command_name" in
            terraform) printf '  Terraform: https://developer.hashicorp.com/terraform/install\n' >&2 ;;
            kubectl) printf '  kubectl:   https://kubernetes.io/docs/tasks/tools/\n' >&2 ;;
            ansible-playbook) printf '  Ansible:   https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html\n' >&2 ;;
            *) printf '  %s: install the package that provides this command\n' "$command_name" >&2 ;;
        esac
    done
fi

if [[ "$MODE" == install ]]; then
    remaining=()
    for command_name in "${REQUIRED_COMMANDS[@]}"; do
        command -v "$command_name" >/dev/null 2>&1 || remaining+=("$command_name")
    done
    if ((${#remaining[@]} > 0)); then
        printf '\ncka-lab requirements: still missing after installation: %s\n' "${remaining[*]}" >&2
        exit 1
    fi
    printf '\ncka-lab requirements: all workstation commands are ready\n'
fi
