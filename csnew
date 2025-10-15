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
    echo "Después de ejecutar el comando, ingresa los comandos en el formato:"
    echo "  comando - descripción"
    echo "  otro_comando # otra descripción"
    echo "  comando_sin_descripción"
    echo ""
    echo "Presiona Ctrl+D cuando termines."
    exit 1
fi

python3 "$PYTHON_SCRIPT" "$@"