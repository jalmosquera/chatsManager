#!/usr/bin/env python3
import sys
import os
import re
import subprocess
from datetime import datetime

from cheatsheet_format import format_entry
from runtime_paths import cheatsheets_dir as installed_cheatsheets_dir, fish_aliases_file

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
        escaped_command = alias['command'].replace("'", "\\'")
        alias_line = f"alias {alias['name']}='{escaped_command}'"
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
    """Format aliases for the shared three-column cheatsheet table."""
    return '\n'.join(
        format_entry(alias['name'], alias['command'], alias['description'])
        for alias in aliases
    )


def add_to_aliases_cheatsheet(content, aliases):
    """Add aliases inside a dedicated tabular section before the footer."""
    section_title = "## 📋 Alias personalizados"
    entries = format_for_cheatsheet(aliases)
    section_pattern = rf"({re.escape(section_title)}\n```tsv\n)(.*?)(\n```)"
    match = re.search(section_pattern, content, re.DOTALL)
    if match:
        existing = match.group(2).rstrip()
        combined = "\n".join(part for part in (existing, entries) if part)
        return content[:match.start(2)] + combined + content[match.end(2):]

    footer_index = content.find("\n---")
    section = f"\n\n{section_title}\n```tsv\n{entries}\n```\n"
    if footer_index == -1:
        return content.rstrip() + section
    return content[:footer_index] + section + content[footer_index:]

def add_aliases_interactively():
    """Agrega aliases de forma interactiva pregunta por pregunta"""
    aliases = []

    print("\n🔧 Agregar Alias Vivo")
    print("=" * 50)
    print("💡 Cada alias se guarda como nombre, comando y descripción.")
    print("   Ejemplo: gs | git status | Muestra el estado del repositorio")

    while True:
        print("\n" + "─" * 50)

        # Preguntar por el nombre del alias
        alias_name = input("\n📛 Nombre del alias: ").strip()
        if not alias_name:
            print("❌ El nombre del alias no puede estar vacío")
            continue

        # Preguntar por el comando
        command = input("💻 Comando a ejecutar: ").strip()
        if not command:
            print("❌ El comando no puede estar vacío")
            continue

        # Preguntar por la descripción
        description = input("📝 Descripción: ").strip()

        # Crear info del alias
        alias_info = {
            'name': alias_name,
            'command': command,
            'description': description
        }

        aliases.append(alias_info)

        desc_text = f" - {description}" if description else ""
        print(f"\n✅ Alias agregado: {alias_name}='{command}'{desc_text}")

        # Preguntar si quiere agregar más
        add_more = input("\n➕ ¿Agregar otro alias? (s/n): ").strip().lower()
        if add_more not in ['s', 'si', 'sí', 'y', 'yes']:
            break

    return aliases

def main():
    cheatsheets_dir = installed_cheatsheets_dir()
    fish_config_path = fish_aliases_file()

    try:
        # Agregar aliases de forma interactiva
        aliases = add_aliases_interactively()

        if not aliases:
            print("❌ No se agregaron aliases")
            sys.exit(1)

        # 1. Agregar al archivo de fish
        print("\n📄 Agregando a fish config...")
        if add_to_fish_config(aliases, fish_config_path):
            print(f"✅ Aliases agregados a: {fish_config_path}")
        else:
            print("❌ Error al agregar aliases a fish config")
            sys.exit(1)

        # 2. Agregar al cheatsheet de aliases
        print("\n📚 Agregando al cheatsheet...")
        aliases_md_path = os.path.join(cheatsheets_dir, "aliases.md")

        # Si no existe el archivo, crearlo
        if not os.path.exists(aliases_md_path):
            with open(aliases_md_path, 'w', encoding='utf-8') as f:
                f.write("# Aliases\n\n")
                f.write(f"---\n*Creado: {datetime.now().strftime('%Y-%m-%d')}*\n")

        with open(aliases_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        updated_content = add_to_aliases_cheatsheet(content, aliases)
        with open(aliases_md_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"✅ Aliases agregados al cheatsheet: {aliases_md_path}")

        print("\n✅ ¡Aliases agregados exitosamente!")
        print("\n💡 Para aplicar los cambios, ejecuta:")
        print("   exec fish")

        print("\n📖 Mostrando aliases.md:\n")
        subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(__file__), "show_cheatsheet.py"), aliases_md_path],
            check=False,
        )
        print(f"\n✓ Resumen: se agregaron {len(aliases)} alias(es).")
        input("Presioná Enter para volver al hub...")

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
