#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="dragon.py"
OLD_NAME="thefirst.py"
WRAPPER="$REPO_DIR/dragon"
GLOBAL_LINK="/usr/local/bin/dragon"
PROFILE_FILES=("$HOME/.bashrc" "$HOME/.zshrc")

check_command() {
  command -v "$1" >/dev/null 2>&1
}

if [ -f "$REPO_DIR/$OLD_NAME" ] && [ ! -f "$REPO_DIR/$SCRIPT_NAME" ]; then
  mv "$REPO_DIR/$OLD_NAME" "$REPO_DIR/$SCRIPT_NAME"
  echo "Renamed $OLD_NAME -> $SCRIPT_NAME"
fi

chmod +x "$REPO_DIR/$SCRIPT_NAME"

cat > "$WRAPPER" <<'EOF'
#!/usr/bin/env bash
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
SCRIPT_DIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
exec python3 "$SCRIPT_DIR/dragon.py" --dragon "$@"
EOF

chmod +x "$WRAPPER"
echo "Created wrapper: $WRAPPER"

MISSING=()
for tool in python3 git nikto gobuster ffuf whatweb nslookup dig nuclei amass dirbuster; do
  if ! check_command "$tool"; then
    MISSING+=("$tool")
  fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "\nMissing tools or commands: ${MISSING[*]}"
  if check_command apt; then
    read -p "Install missing packages using sudo apt install? [y/N] " install_deps
    if [[ "$install_deps" =~ ^[Yy]$ ]]; then
      sudo apt update
      sudo apt install -y "${MISSING[@]}"
    fi
  else
    echo "Please install missing dependencies manually."
  fi
fi

if [ -d "/usr/local/bin" ]; then
  if [ -w "/usr/local/bin" ]; then
    ln -sf "$WRAPPER" "$GLOBAL_LINK"
    echo "Installed global command: $GLOBAL_LINK"
  elif check_command sudo; then
    read -p "Install global command with sudo? [y/N] " install_global
    if [[ "$install_global" =~ ^[Yy]$ ]]; then
      sudo ln -sf "$WRAPPER" "$GLOBAL_LINK"
      echo "Installed global command: $GLOBAL_LINK"
    fi
  fi
fi

for profile in "${PROFILE_FILES[@]}"; do
  if [ -f "$profile" ] && ! grep -Fq "export PATH=\"\$PATH:$REPO_DIR\"" "$profile"; then
    printf '\n# DRAGON recon CLI\nexport PATH="\$PATH:%s"\n' "$REPO_DIR" >> "$profile"
    echo "Added PATH entry to $profile"
  fi
done

echo "\nSetup complete."
echo "Run 'source ~/.bashrc' or open a new shell to use 'dragon' anywhere."
