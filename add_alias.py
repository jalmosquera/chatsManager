#!/usr/bin/env python3
import sys
import os
import re
from datetime import datetime

def parse_alias_input(input_text):
    """Parsea el input de alias en formato: nombre='comando' - descripción"""
    aliases = []
    lines = input_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Formato: nombre='comando' - descripción
        # o: nombre="comando" - descripción
        # o: nombre=comando - descripción
        match = re.match(r"^(\w+)=(['\"]?)(.+?)\2\s*(?:-\s*(.*))?$", line)

        if match:
            alias_name = match.group(1)
            command = match.group(3)
            description = match.group(4) if match.group(4) else ''

            aliases.append({
                'name': alias_name,
                'command': command,
                'description': description.strip()
            })
        else:
            print(f"⚠️  Formato incorrecto en: {line}")
            print("   Formato esperado: nombre='comando' - descripción")

    return aliases

def add_to_fish_config(aliases, fish_config_path):
    """Agrega los aliases al archivo de configuración de fish"""
    # Leer archivo existente
    with open(fish_config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Encontrar la sección de Custom aliases
    custom_section_match = re.search(r'(# Custom aliases.*?)(?=\n# |\Z)', content, re.DOTALL)

    if not custom_section_match:
        print("⚠️  No se encontró la sección de Custom aliases")
        return False

    # Preparar los nuevos aliases
    new_aliases_lines = []
    for alias in aliases:
        alias_line = f"alias {alias['name']}='{alias['command']}'"
        if alias['description']:
            alias_line += f"  # {alias['description']}"
        new_aliases_lines.append(alias_line)

    new_aliases_text = '\n'.join(new_aliases_lines)

    # Insertar antes de la sección de Cheat sheets aliases
    cheat_section_pos = content.find('# Cheat sheets aliases')

    if cheat_section_pos != -1:
        # Insertar antes de la sección de cheat sheets
        before = content[:cheat_section_pos]
        after = content[cheat_section_pos:]

        # Asegurarse de que hay una línea en blanco antes
        if not before.endswith('\n\n'):
            before = before.rstrip() + '\n\n'

        updated_content = before + new_aliases_text + '\n\n' + after
    else:
        # Si no existe la sección de cheat sheets, agregar al final
        updated_content = content.rstrip() + '\n\n' + new_aliases_text + '\n'

    # Escribir archivo actualizado
    with open(fish_config_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    return True

def format_for_cheatsheet(aliases):
    """Formatea los aliases para el cheatsheet markdown"""
    lines = []
    for alias in aliases:
        if alias['description']:
            lines.append(f"{alias['name']} - {alias['description']}")
        else:
            lines.append(f"{alias['name']} - {alias['command']}")
    return '\n'.join(lines)

def main():
    cheatsheets_dir = os.path.expanduser("~/.cheatsheets")
    fish_config_path = os.path.expanduser("~/.config/fish/conf.d/aliases.fish")

    print("🔧 Agregar Alias Vivo")
    print("Formato: nombre='comando' - descripción")
    print("Ejemplo: ll='ls -la' - Listar todo con detalles")
    print("\nIngresa los aliases (Ctrl+D para finalizar):\n")

    try:
        # Leer entrada del usuario
        input_text = sys.stdin.read()

        if not input_text.strip():
            print("❌ No se ingresaron aliases")
            sys.exit(1)

        # Parsear aliases
        aliases = parse_alias_input(input_text)

        if not aliases:
            print("❌ No se pudieron parsear los aliases")
            sys.exit(1)

        print(f"\n📝 Se encontraron {len(aliases)} alias(es):")
        for alias in aliases:
            desc_text = f" - {alias['description']}" if alias['description'] else ""
            print(f"  • {alias['name']}='{alias['command']}'{desc_text}")

        # Confirmar
        confirm = input("\n¿Agregar estos aliases? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Operación cancelada")
            sys.exit(0)

        # 1. Agregar al archivo de fish
        print("\n📄 Agregando a fish config...")
        if add_to_fish_config(aliases, fish_config_path):
            print(f"✅ Aliases agregados a: {fish_config_path}")
        else:
            print("❌ Error al agregar aliases a fish config")
            sys.exit(1)

        # 2. Agregar al cheatsheet usando add_to_cheat.py
        print("\n📚 Agregando al cheatsheet...")
        formatted_input = format_for_cheatsheet(aliases)

        # Crear archivo temporal con el input formateado
        temp_file = "/tmp/aliases_input.txt"
        with open(temp_file, 'w') as f:
            f.write(formatted_input)

        # Llamar a add_to_cheat.py
        result = os.system(f'python3 "{cheatsheets_dir}/add_to_cheat.py" aliases < {temp_file}')

        # Limpiar archivo temporal
        os.remove(temp_file)

        if result == 0:
            print("\n✅ ¡Aliases agregados exitosamente!")
            print("\n💡 Para aplicar los cambios, ejecuta:")
            print("   source ~/.config/fish/config.fish")
            print("   o simplemente: exec fish")
        else:
            print("\n⚠️  Los aliases se agregaron a fish pero hubo un problema con el cheatsheet")

    except KeyboardInterrupt:
        print("\n❌ Operación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
