#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo "alias google='python "$SCRIPT_DIR"/main.py \$@'" >> ~/.zshrc
. ~/.zshrc

echo 'Installation Complete!'
