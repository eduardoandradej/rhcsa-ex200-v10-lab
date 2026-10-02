#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

export ANSIBLE_CONFIG="${ROOT}/ansible/ansible.cfg"

cd "$ROOT"

echo "== RHCSA Lab — dependency bootstrap =="
echo
echo "[1/2] Installing baseline dependencies..."
ansible-playbook ansible/playbooks/00-bootstrap-dependencies.yml

echo
echo "[2/2] Validating baseline..."
ansible-playbook ansible/playbooks/00-validate-dependencies.yml

echo
echo "DEPENDENCY BASELINE: READY"
