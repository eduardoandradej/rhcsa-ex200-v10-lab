#!/usr/bin/env bash
set -Eeuo pipefail
PROJECT="${HOME}/rhcsa-ex200-v10-lab"
[[ -d "$PROJECT" ]] || { echo "ERRO: $PROJECT não existe" >&2; exit 1; }
mkdir -p "$PROJECT"/{assets,graders,reports,mocks,host-control,bin,labctl,docs/architecture,docs/setup,ansible/playbooks}
echo "Estrutura pública base validada em $PROJECT"
