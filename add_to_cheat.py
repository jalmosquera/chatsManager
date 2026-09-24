#!/usr/bin/env python3
import sys
import os
import re
import subprocess
from datetime import datetime

from cheatsheet_format import format_entry, parse_entry
from runtime_paths import cheatsheets_dir as installed_cheatsheets_dir

def get_emoji_for_category(command_text):
    """Determina el emoji apropiado basado en el contenido del comando"""
    command_lower = command_text.lower()
    
    # Mapeo de palabras clave a emojis
    emoji_mapping = {
        'install': '📦',
        'config': '⚙️',
        'create': '🆕',
        'delete': '🗑️',
        'remove': '❌',
        'list': '📋',
        'show': '👁️',
        'view': '👁️',
        'start': '▶️',
        'stop': '⏹️',
        'restart': '🔄',
        'status': '📊',
        'help': '❓',
        'version': '🏷️',
        'update': '🔄',
        'upgrade': '⬆️',
        'build': '🔨',
        'deploy': '🚀',
        'test': '🧪',
        'debug': '🐛',
        'log': '📝',
        'search': '🔍',
        'find': '🔍',
        'clone': '📥',
        'push': '📤',
        'pull': '📥',
        'commit': '💾',
        'branch': '🌳',
        'merge': '🔀',
        'connect': '🔗',
        'disconnect': '🔌',
        'server': '🖥️',
        'database': '🗄️',
        'user': '👤',
        'group': '👥',
        'permission': '🔐',
        'security': '🔒',
        'backup': '💾',
        'restore': '♻️',
        'sync': '🔄',
        'monitor': '📊',
        'analyze': '🔍',
        'optimize': '⚡',
        'clean': '🧹',
        'validate': '✅',
        'check': '✅',
        'verify': '✅',
        'run': '▶️',
        'execute': '▶️',
        'launch': '🚀',
        'init': '🎯',
        'setup': '⚙️',
        'configure': '⚙️',
    }
    
    for keyword, emoji in emoji_mapping.items():
        if keyword in command_lower:
            return emoji
    
    return '💻'

def categorize_command(command, description):
    """Categoriza comandos basado en patrones comunes"""
    command_lower = command.lower()
    desc_lower = description.lower() if description else ''
    
    if any(word in command_lower for word in ['install', 'add', 'create', 'new']):
        return 'Instalación y Configuración'
    elif any(word in command_lower for word in ['list', 'show', 'status', 'info', 'get']):
        return 'Consultas y Estado'
    elif any(word in command_lower for word in ['start', 'stop', 'restart', 'run', 'execute']):
        return 'Ejecución y Control'
    elif any(word in command_lower for word in ['update', 'upgrade', 'modify', 'edit']):
        return 'Actualización y Modificación'
    elif any(word in command_lower for word in ['delete', 'remove', 'clean', 'uninstall']):
        return 'Eliminación y Limpieza'
    elif any(word in command_lower for word in ['help', 'version', 'man', 'doc']):
        return 'Ayuda y Documentación'
    else:
        return 'Comandos Generales'

def format_keyboard_shortcuts(text):
    """Detecta y formatea automáticamente combinaciones de teclas"""
    import re
    
    # Palabras clave comunes para teclas modificadoras
    modifiers = [
        'ctrl', 'control', 'cmd', 'command', 'alt', 'option', 'shift', 
        'meta', 'super', 'win', 'windows', 'fn', 'function'
    ]
    
    # Teclas especiales comunes
    special_keys = [
        'tab', 'enter', 'return', 'space', 'esc', 'escape', 'backspace', 
        'delete', 'del', 'home', 'end', 'pageup', 'pagedown', 'insert',
        'up', 'down', 'left', 'right', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6',
        'f7', 'f8', 'f9', 'f10', 'f11', 'f12'
    ]
    
    # Crear patrón que detecte combinaciones de teclas
    all_keys = modifiers + special_keys + [r'[a-zA-Z0-9]']
    
    # Buscar patrones como "ctrl alt t" o "cmd shift n"
    words = text.lower().split()
    
    # Si hay más de una palabra y parece ser combinación de teclas
    if len(words) >= 2:
        # Verificar si todas las palabras son teclas conocidas
        is_keyboard_combo = True
        for word in words:
            if not (word in modifiers or word in special_keys or len(word) == 1):
                is_keyboard_combo = False
                break
        
        if is_keyboard_combo:
            # Formatear con + entre las teclas, manteniendo capitalización apropiada
            formatted_keys = []
            for word in words:
                if word in ['ctrl', 'control']:
                    formatted_keys.append('Ctrl')
                elif word in ['cmd', 'command']:
                    formatted_keys.append('Cmd')
                elif word in ['alt', 'option']:
                    formatted_keys.append('Alt')
                elif word == 'shift':
                    formatted_keys.append('Shift')
                elif word in ['meta', 'super']:
                    formatted_keys.append('Meta')
                elif word in ['win', 'windows']:
                    formatted_keys.append('Win')
                elif word in ['fn', 'function']:
                    formatted_keys.append('Fn')
                else:
                    # Para teclas especiales y letras, usar capitalización apropiada
                    formatted_keys.append(word.capitalize())
            
            return ' + '.join(formatted_keys)
    
    return text

def parse_commands_input(input_text):
    """Parsea el texto de entrada y extrae comandos con descripciones"""
    commands = []
    lines = input_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if ' - ' in line:
            parts = line.split(' - ', 1)
            command = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ''
        elif ' # ' in line:
            parts = line.split(' # ', 1)
            command = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ''
        else:
            command = line.strip()
            description = ''

        if command:
            commands.append({'command': command, 'description': description, 'category': None})

    return commands

def select_category_for_command(cmd_info, existing_sections):
    """Permite seleccionar categoría para un comando"""
    # Mostrar categorías existentes
    print("\n📁 Categorías existentes:")
    section_list = list(existing_sections.keys())
    for i, section in enumerate(section_list, 1):
        cmd_count = len(existing_sections[section])
        print(f"  {i}. {section} ({cmd_count} comandos)")
    print(f"  0. [Crear nueva categoría]")

    while True:
        try:
            choice = input(f"\n¿En qué categoría agregarlo? (1-{len(section_list)}, 0 para nueva): ").strip()

            if choice == '0':
                # Crear nueva categoría
                new_category = input("📂 Nombre de la nueva categoría: ").strip()
                if new_category:
                    cmd_info['category'] = new_category
                    if new_category not in existing_sections:
                        existing_sections[new_category] = []
                        section_list.append(new_category)
                    return cmd_info
                else:
                    print("❌ El nombre de la categoría no puede estar vacío")
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(section_list):
                    cmd_info['category'] = section_list[idx]
                    return cmd_info
                else:
                    print(f"❌ Por favor ingresa un número entre 0 y {len(section_list)}")
        except ValueError:
            print("❌ Por favor ingresa un número válido")

def add_commands_interactively(existing_sections):
    """Agrega comandos de forma interactiva pregunta por pregunta"""
    commands = []

    print("\n📝 Vamos a agregar comandos de forma interactiva")
    print("=" * 50)
    print("💡 Cada registro pide nombre, comando y descripción por separado.")

    while True:
        print("\n" + "─" * 50)

        name = input("\n📛 Nombre: ").strip()
        if not name:
            print("❌ El nombre no puede estar vacío")
            continue

        command = input("💻 Comando: ").strip()
        if not command:
            print("❌ El comando no puede estar vacío")
            continue

        # Preguntar por la descripción
        description = input("📝 Descripción: ").strip()

        # Crear info del comando
        cmd_info = {
            'name': name,
            'command': command,
            'description': description,
            'category': None
        }

        # Seleccionar categoría
        cmd_info = select_category_for_command(cmd_info, existing_sections)
        commands.append(cmd_info)

        print(f"\n✅ Agregado: {name} → {command}")

        # Preguntar si quiere agregar más
        add_more = input("\n➕ ¿Agregar otro comando? (s/n): ").strip().lower()
        if add_more not in ['s', 'si', 'sí', 'y', 'yes']:
            break

    return commands

def parse_existing_cheatsheet(content):
    """Parsea un cheatsheet existente para extraer su estructura"""
    lines = content.split('\n')
    sections = {}
    current_section = None
    current_commands = []
    in_code_block = False
    
    for line in lines:
        line_stripped = line.strip()
        
        # Detectar encabezados de sección
        if line_stripped.startswith('## ') and not in_code_block:
            # Guardar sección anterior si existe
            if current_section:
                sections[current_section] = current_commands
            
            # Iniciar nueva sección
            current_section = line_stripped[3:].strip()  # Remover "## "
            current_commands = []
            
        # Detectar bloques de código
        elif line_stripped.startswith('```'):
            in_code_block = not in_code_block
            
        # Extraer comandos del bloque de código
        elif in_code_block and line_stripped and not line_stripped.startswith('```'):
            entry = parse_entry(line)
            current_commands.append({
                'name': entry.name,
                'command': entry.command,
                'description': entry.description,
            })
    
    # Guardar la última sección
    if current_section:
        sections[current_section] = current_commands
    
    return sections

def merge_commands_into_sections(existing_sections, new_commands):
    """Mezcla comandos nuevos con secciones existentes usando la categoría seleccionada"""
    for cmd_info in new_commands:
        # Usar la categoría seleccionada por el usuario
        category = cmd_info.get('category')

        if not category:
            # Fallback: categorizar automáticamente si no hay categoría
            category = categorize_command(cmd_info['command'], cmd_info['description'])

        # Agregar a la categoría correspondiente
        if category not in existing_sections:
            existing_sections[category] = []

        existing_sections[category].append(cmd_info)

    return existing_sections

def generate_updated_markdown(tool_name, sections, original_header):
    """Genera el markdown actualizado manteniendo el formato original"""
    markdown = original_header + "\n\n"
    
    # Generar contenido por sección
    for section_name, cmd_list in sections.items():
        if not cmd_list:  # Saltar secciones vacías
            continue
            
        # Determinar emoji para la sección
        category_emoji = '📁'
        if 'instalación' in section_name.lower() or 'configuración' in section_name.lower():
            category_emoji = '⚙️'
        elif 'consultas' in section_name.lower() or 'estado' in section_name.lower():
            category_emoji = '📊'
        elif 'ejecución' in section_name.lower() or 'control' in section_name.lower():
            category_emoji = '▶️'
        elif 'actualización' in section_name.lower() or 'modificación' in section_name.lower():
            category_emoji = '🔄'
        elif 'eliminación' in section_name.lower() or 'limpieza' in section_name.lower():
            category_emoji = '🗑️'
        elif 'ayuda' in section_name.lower() or 'documentación' in section_name.lower():
            category_emoji = '❓'
        
        # Si la sección ya tenía emoji, mantenerlo
        if not section_name.startswith(('📁', '⚙️', '📊', '▶️', '🔄', '🗑️', '❓')):
            section_title = f"## {category_emoji} {section_name}"
        else:
            section_title = f"## {section_name}"
            
        markdown += f"{section_title}\n"
        markdown += "```tsv\n"
        
        for cmd_info in cmd_list:
            markdown += f"{format_entry(cmd_info['name'], cmd_info['command'], cmd_info['description'])}\n"
        
        markdown += "```\n\n"
    
    # Agregar footer actualizado
    update_date = datetime.now().strftime("%Y-%m-%d")
    markdown += f"---\n*Actualizado: {update_date}*\n"
    
    return markdown

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 add_to_cheat.py <nombre_herramienta>")
        print("Agrega comandos a un cheatsheet existente")
        print("Cada registro solicita nombre, comando y descripción")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    cheatsheets_dir = installed_cheatsheets_dir()
    filename = f"{tool_name.lower().replace(' ', '_').replace('-', '_')}.md"
    filepath = cheatsheets_dir / filename
    
    # Verificar que el archivo existe
    if not os.path.exists(filepath):
        print(f"❌ El cheatsheet '{filename}' no existe")
        print(f"💡 Usa 'newcheat {tool_name}' para crearlo")
        sys.exit(1)
    
    print(f"📝 Agregando comandos a '{tool_name}'")

    try:
        # Leer archivo existente
        with open(filepath, 'r', encoding='utf-8') as f:
            existing_content = f.read()

        # Extraer header original
        lines = existing_content.split('\n')
        original_header = lines[0] if lines else f"# {tool_name.title()}"

        # Parsear contenido existente
        existing_sections = parse_existing_cheatsheet(existing_content)

        # Agregar comandos de forma interactiva
        new_commands = add_commands_interactively(existing_sections)

        if not new_commands:
            print("❌ No se agregaron comandos")
            sys.exit(1)

        # Mezclar comandos
        updated_sections = merge_commands_into_sections(existing_sections, new_commands)
        
        # Generar markdown actualizado
        updated_content = generate_updated_markdown(tool_name, updated_sections, original_header)
        
        # Escribir archivo actualizado
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"✅ Cheatsheet actualizado exitosamente: {filepath}")
        print(f"➕ Se agregaron {len(new_commands)} comando(s)")

        # Mostrar resumen
        total_commands = sum(len(commands) for commands in updated_sections.values())
        print(f"📄 Total de comandos en el cheatsheet: {total_commands}")

        # Si estamos agregando aliases, sincronizar con fish
        if tool_name.lower() == 'aliases':
            print(f"\n🔄 Sincronizando aliases con fish...")
            sync_script = cheatsheets_dir / "sync_aliases.py"
            os.system(f'python3 "{sync_script}"')

        # Mostrar el archivo en la terminal
        print(f"\n📖 Mostrando {filename}:\n")
        subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(__file__), "show_cheatsheet.py"), filepath],
            check=False,
        )
        print(f"\n✓ Resumen: {tool_name} recibió {len(new_commands)} comandos; ahora tiene {total_commands} en total.")
        input("Presioná Enter para volver al hub...")
        
    except KeyboardInterrupt:
        print("\n❌ Operación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
