#!/usr/bin/env python3
"""
Sincroniza aliases del cheatsheet aliases.md con la configuración de fish
"""
import sys
import os
import re

def parse_aliases_from_cheatsheet(cheatsheet_path):
    """Extrae todos los aliases del cheatsheet"""
    aliases = []

    if not os.path.exists(cheatsheet_path):
        return aliases

    with open(cheatsheet_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar bloques de código bash
    in_code_block = False
    for line in content.split('\n'):
        line_stripped = line.strip()

        if line_stripped == '```bash' or line_stripped == '```':
            in_code_block = not in_code_block
            continue

        if in_code_block and line_stripped:
            # Parsear línea: nombre - descripción  o  comando  # descripción
            if ' - ' in line_stripped:
                parts = line_stripped.split(' - ', 1)
                alias_name = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ''
            elif '  # ' in line_stripped:
                parts = line_stripped.split('  # ', 1)
                alias_name = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ''
            else:
                alias_name = line_stripped
                description = ''

            # Inferir el comando desde la descripción o el nombre
            # Formato esperado: l4 - Árbol nivel 4
            # El comando real sería: tree -L 4

            # Para ahora, solo guardamos lo que tenemos
            if alias_name and not alias_name.startswith('#'):
                aliases.append({
                    'name': alias_name,
                    'description': description
                })

    return aliases

def infer_alias_command(alias_name, description):
    """Intenta inferir el comando completo del alias"""
    # Patrones comunes
    if alias_name.startswith('l') and alias_name[1:].isdigit():
        # l1, l2, l3, etc. -> tree -L N
        level = alias_name[1:]
        return f"tree -L {level}"

    # Si no podemos inferir, devolver None
    return None

def read_fish_aliases(fish_config_path):
    """Lee todos los aliases existentes en fish"""
    aliases = {}

    if not os.path.exists(fish_config_path):
        return aliases

    with open(fish_config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar líneas que empiecen con alias
    for line in content.split('\n'):
        match = re.match(r"^alias\s+(\w+)='([^']+)'", line)
        if match:
            name = match.group(1)
            command = match.group(2)
            aliases[name] = command

    return aliases

def sync_aliases_to_fish(cheatsheet_path, fish_config_path):
    """Sincroniza aliases del cheatsheet a fish"""
    print("🔄 Sincronizando aliases del cheatsheet a fish...")

    # Leer aliases del cheatsheet
    cheatsheet_aliases = parse_aliases_from_cheatsheet(cheatsheet_path)

    if not cheatsheet_aliases:
        print("⚠️  No se encontraron aliases en el cheatsheet")
        return False

    # Leer aliases actuales de fish
    fish_aliases = read_fish_aliases(fish_config_path)

    # Determinar qué aliases faltan o necesitan actualización
    missing_aliases = []

    for alias_info in cheatsheet_aliases:
        name = alias_info['name']

        if name not in fish_aliases:
            # Intentar inferir el comando
            command = infer_alias_command(name, alias_info['description'])

            if command:
                missing_aliases.append({
                    'name': name,
                    'command': command,
                    'description': alias_info['description']
                })

    if not missing_aliases:
        print("✅ Todos los aliases están sincronizados")
        return True

    # Agregar los aliases faltantes a fish
    print(f"\n📝 Agregando {len(missing_aliases)} alias(es) a fish:")
    for alias in missing_aliases:
        print(f"  • {alias['name']}='{alias['command']}'")

    # Leer contenido actual
    with open(fish_config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Encontrar la sección de Listing
    listing_section_match = re.search(r'(# Listing\n(?:alias [^\n]+\n)+)', content)

    if listing_section_match:
        old_listing_section = listing_section_match.group(1)

        # Construir la nueva sección con los aliases agregados
        new_listing_lines = []
        for line in old_listing_section.split('\n'):
            new_listing_lines.append(line)
            if line.startswith('# Listing'):
                continue
            # Agregar después de la última línea de alias existente

        # Agregar los nuevos aliases
        for alias in missing_aliases:
            new_line = f"alias {alias['name']}='{alias['command']}'"
            new_listing_lines.append(new_line)

        new_listing_section = '\n'.join(new_listing_lines)

        # Reemplazar en el contenido
        content = content.replace(old_listing_section, new_listing_section)
    else:
        # Si no encontramos la sección, agregar los aliases antes de los cheatsheets
        cheat_section_pos = content.find('# Cheat sheets aliases')
        if cheat_section_pos != -1:
            before = content[:cheat_section_pos]
            after = content[cheat_section_pos:]

            new_aliases_text = '\n'.join([
                f"alias {alias['name']}='{alias['command']}'"
                for alias in missing_aliases
            ])

            content = before + new_aliases_text + '\n\n' + after

    # Escribir el archivo actualizado
    with open(fish_config_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Aliases sincronizados exitosamente")
    print("💡 Ejecuta 'exec fish' para aplicar los cambios")

    return True

def main():
    cheatsheets_dir = os.path.expanduser("~/.cheatsheets")
    fish_config_path = os.path.expanduser("~/.config/fish/conf.d/aliases.fish")
    cheatsheet_path = os.path.join(cheatsheets_dir, "aliases.md")

    try:
        success = sync_aliases_to_fish(cheatsheet_path, fish_config_path)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
