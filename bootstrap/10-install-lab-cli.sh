#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-${HOME}/rhcsa-ex200-v10-lab}"
SOURCE="${PROJECT_ROOT}/bin/lab"
DEST_DIR="${HOME}/.local/bin"
DEST="${DEST_DIR}/lab"

die() {
    echo "ERRO: $*" >&2
    exit 1
}

[[ -f "$SOURCE" ]] || die "CLI não encontrado: $SOURCE"

command -v python3 >/dev/null 2>&1 || die "python3 não encontrado"
command -v ansible >/dev/null 2>&1 || die "ansible não encontrado"
command -v ssh >/dev/null 2>&1 || die "ssh não encontrado"

python3 -c 'import yaml' >/dev/null 2>&1 || \
    die "Módulo Python PyYAML não encontrado"

# Garante execução mesmo quando o pacote foi extraído de formato
# que não preserva permissões Unix.
chmod +x "$SOURCE"

mkdir -p "$DEST_DIR"
ln -sfn "$SOURCE" "$DEST"

PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'

if ! grep -Fqx "$PATH_LINE" "${HOME}/.bashrc"; then
    echo "$PATH_LINE" >> "${HOME}/.bashrc"
fi

export PATH="${DEST_DIR}:${PATH}"

echo "RHCSA Lab CLI instalado:"
echo "  $DEST -> $(readlink -f "$DEST")"
echo

"$DEST" --version

echo
echo "Execute:"
echo "  lab status"
echo "  lab list"
