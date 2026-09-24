#!/bin/bash

# Wrapper script for create_cheatsheet.py
# Usage: cs <tool_name> or csnew <tool_name>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/create_cheatsheet.py"

if [ $# -eq 0 ]; then
    echo "🔧 Generador de Cheatsheets"
    echo ""
    echo "Uso: cs <nombre_herramienta> o csnew <nombre_herramienta>"
    echo ""
    echo "Ejemplos:"
    echo "  cs kubectl"
    echo "  csnew terraform"
    echo "  cs 'aws cli'"
    echo ""
echo "Después de ejecutar el comando, cada registro pide:"
echo "  1. Nombre"
echo "  2. Comando"
echo "  3. Descripción"
    exit 1
fi

python3 "$PYTHON_SCRIPT" "$@"
