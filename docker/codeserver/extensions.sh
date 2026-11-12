#!/usr/bin/env bash
set -uo pipefail

CODE_SERVER="${CODE_SERVER:-code-server}"
TARGET_PLATFORM="${TARGET_PLATFORM:-linux-arm64}"
EXTENSIONS_DIR="${EXTENSIONS_DIR:-}"
CACHE_DIR="${CACHE_DIR:-/tmp/code-server-vsix}"
mkdir -p "$CACHE_DIR"

CS_ARGS=()
[ -n "$EXTENSIONS_DIR" ] && CS_ARGS+=(--extensions-dir "$EXTENSIONS_DIR")

EXTENSIONS=$(cat <<'EOF'
4ops.terraform	0.2.5
arjun.swagger-viewer	3.2.0
aykutsarac.jsoncrack-vscode	5.1.0
continue.continue	2.0.0
davidanson.vscode-markdownlint	0.62.1
dbaeumer.vscode-eslint	3.0.34
esbenp.prettier-vscode	12.4.0
formulahendry.code-runner	0.12.2
foxundermoon.shell-format	7.2.8
george-alisson.html-preview-vscode	0.2.5
github.vscode-github-actions	0.32.3
golang.go	0.58.0
hashicorp.hcl	0.6.0
hediet.vscode-drawio	1.19.0
humao.rest-client	0.25.1
igorsbitnev.error-gutters	1.0.1
jebbs.plantuml	2.18.1
kamikillerto.vscode-colorize	0.17.1
kevinrose.vsc-python-indent	1.21.0
kisstkondoros.vscode-gutter-preview	0.32.2
mark-tucker.aws-cli-configure	0.3.0
mechatroner.rainbow-csv	3.24.1
mhutchie.git-graph	1.30.0
ms-azuretools.vscode-containers	2.5.3
ms-azuretools.vscode-docker	2.0.0
ms-python.black-formatter	2026.6.0
ms-python.debugpy	2026.6.0
ms-python.flake8	2026.8.0
ms-python.isort	2026.8.0
ms-python.python	2026.10.0
ms-python.vscode-pylance	2026.4.1
ms-python.vscode-python-envs	1.42.0
ms-toolsai.jupyter	2025.9.1
ms-toolsai.jupyter-keymap	1.1.2
ms-toolsai.jupyter-renderers	1.3.0
ms-toolsai.vscode-jupyter-cell-tags	0.1.9
ms-toolsai.vscode-jupyter-slideshow	0.1.6
ms-vscode-remote.remote-ssh	0.128.0
ms-vscode-remote.remote-ssh-edit	0.87.0
ms-vscode-remote.remote-wsl	1.104.7
ms-vscode.powershell	2025.4.0
ms-vscode.remote-explorer	0.5.0
ms-vsliveshare.vsliveshare	1.1.122
mutantdino.resourcemonitor	1.0.7
njpwerner.autodocstring	0.6.1
oderwat.indent-rainbow	8.3.1
oracle.oracle-java	27.0.0
pflannery.vscode-versionlens	1.28.0
quicktype.quicktype	23.0.170
qwtel.sqlite-viewer	26.9.1
redhat.vscode-yaml	2.0.0
ritwickdey.liveserver	5.7.10
seyyedkhandon.firacode	2.2.2
shd101wyy.markdown-preview-enhanced	0.8.40
shyykoserhiy.git-autoconfig	0.0.2
sst-dev.opencode	1.0.0
tomoki1207.pdf	1.2.2
usernamehw.errorlens	3.30.0
vscode-icons-team.vscode-icons	13.0.0
vue.volar	3.3.14
EOF
)

ok_list=(); fail_list=()

install_ext() {
  local id="$1" ver="$2" pub name url vsix
  pub="${id%%.*}"
  name="${id#*.}"

  if "$CODE_SERVER" --install-extension "$id" --force "${CS_ARGS[@]}" >/dev/null 2>&1; then
    echo "[openvsx] ok    $id"
    return 0
  fi

  for tp in "$TARGET_PLATFORM" "universal"; do
    url="https://marketplace.visualstudio.com/_apis/public/gallery/publishers/${pub}/vsextensions/${name}/${ver}/vspackage"
    [ "$tp" != "universal" ] && url="${url}?targetPlatform=${tp}"
    vsix="${CACHE_DIR}/${id}-${ver}-${tp}.vsix"
    if curl -fsSL --retry 3 --max-time 300 -o "$vsix" "$url" \
       && "$CODE_SERVER" --install-extension "$vsix" --force "${CS_ARGS[@]}" >/dev/null 2>&1; then
      echo "[vsix:$tp] ok    $id@$ver"
      return 0
    fi
  done

  echo "[fail]     $id@$ver"
  return 1
}

while IFS=$'\t' read -r id ver; do
  [ -z "${id:-}" ] && continue
  if install_ext "$id" "$ver"; then ok_list+=("$id"); else fail_list+=("$id"); fi
done <<< "$EXTENSIONS"

echo
echo "Instaladas: ${#ok_list[@]}   Fallidas: ${#fail_list[@]}"
if ((${#fail_list[@]})); then
  printf '  - %s\n' "${fail_list[@]}"
  echo "Nota: ms-vscode-remote.* , ms-vscode.remote-explorer y ms-vsliveshare no tienen build"
  echo "      para linux-arm64/utilizable en code-server; son esperables como fallo."
fi