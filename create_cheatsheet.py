#!/usr/bin/env python3
import sys
import os
import re
import subprocess
from datetime import datetime

from cheatsheet_format import format_entry
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
    
    # Emoji por defecto
    return '💻'

def categorize_command(command, description):
    """Categoriza comandos basado en patrones comunes"""
    command_lower = command.lower()
    desc_lower = description.lower() if description else ''
    
    # Categorías comunes
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

def collect_commands_interactively():
    """Collect command records with separate name, command, and description fields."""
    commands = []
    print("\n📝 Agregá cada comando con sus tres datos.")

    while True:
        name = input("📛 Nombre: ").strip()
        if not name:
            print("❌ El nombre no puede estar vacío")
            continue

        command = input("💻 Comando: ").strip()
        if not command:
            print("❌ El comando no puede estar vacío")
            continue

        description = input("📝 Descripción: ").strip()
        commands.append({"name": name, "command": command, "description": description})

        add_more = input("➕ ¿Agregar otro comando? (s/n): ").strip().lower()
        if add_more not in ("s", "si", "sí", "y", "yes"):
            return commands
    
    return commands

def group_commands_by_category(commands):
    """Agrupa comandos por categoría"""
    categories = {}
    
    for cmd_info in commands:
        category = categorize_command(cmd_info['command'], cmd_info['description'])
        if category not in categories:
            categories[category] = []
        categories[category].append(cmd_info)
    
    return categories

def generate_markdown(tool_name, commands):
    """Genera el contenido markdown del cheatsheet"""
    # Determinar emoji principal para la herramienta
    tool_emojis = {
        'docker': '🐳',
        'kubernetes': '☸️',
        'git': '🔀',
        'npm': '📦',
        'yarn': '🧶',
        'pip': '🐍',
        'maven': '🔶',
        'gradle': '🐘',
        'ansible': '🔧',
        'terraform': '🏗️',
        'aws': '☁️',
        'azure': '☁️',
        'gcp': '☁️',
        'mysql': '🗄️',
        'postgresql': '🐘',
        'mongo': '🍃',
        'redis': '🔴',
        'nginx': '🌐',
        'apache': '🌐',
        'vim': '📝',
        'tmux': '🖥️',
        'ssh': '🔐',
    }
    
    tool_emoji = tool_emojis.get(tool_name.lower(), '🛠️')
    
    # Generar encabezado
    markdown = f"# {tool_emoji} {tool_name.title()} - Comandos Esenciales\n\n"
    
    # Agrupar comandos por categoría
    categories = group_commands_by_category(commands)
    
    # Generar contenido por categoría
    for category, cmd_list in categories.items():
        # Emoji para la categoría
        category_emoji = '📁'  # Emoji por defecto para categorías
        if 'instalación' in category.lower() or 'configuración' in category.lower():
            category_emoji = '⚙️'
        elif 'consultas' in category.lower() or 'estado' in category.lower():
            category_emoji = '📊'
        elif 'ejecución' in category.lower() or 'control' in category.lower():
            category_emoji = '▶️'
        elif 'actualización' in category.lower() or 'modificación' in category.lower():
            category_emoji = '🔄'
        elif 'eliminación' in category.lower() or 'limpieza' in category.lower():
            category_emoji = '🗑️'
        elif 'ayuda' in category.lower() or 'documentación' in category.lower():
            category_emoji = '❓'
        
        markdown += f"## {category_emoji} {category}\n"
        markdown += "```tsv\n"
        
        for cmd_info in cmd_list:
            markdown += f"{format_entry(cmd_info['name'], cmd_info['command'], cmd_info['description'])}\n"
        
        markdown += "```\n\n"
    
    # Agregar footer con fecha de creación
    creation_date = datetime.now().strftime("%Y-%m-%d")
    markdown += f"---\n*Creado: {creation_date}*\n"
    
    return markdown

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 create_cheatsheet.py <nombre_herramienta>")
        print("Luego ingresá nombre, comando y descripción para cada registro")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    cheatsheets_dir = installed_cheatsheets_dir()
    filename = f"{tool_name.lower().replace(' ', '_').replace('-', '_')}.md"
    filepath = cheatsheets_dir / filename

    # Confirm before reading stdin so the response is not consumed as a command.
    if os.path.exists(filepath):
        response = input(f"⚠️  El archivo {filename} ya existe. ¿Sobrescribir? (y/n): ")
        if response.lower() != 'y':
            print("❌ Operación cancelada")
            sys.exit(1)
    
    print(f"📝 Creando cheatsheet para {tool_name}")
    print("💡 Cada registro pide nombre, comando y descripción por separado.")
    
    try:
        commands = collect_commands_interactively()
        
        if not commands:
            print("❌ No se pudieron parsear los comandos")
            sys.exit(1)
        
        # Generar markdown
        markdown_content = generate_markdown(tool_name, commands)
        
        # Escribir archivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Cheatsheet creado exitosamente: {filepath}")
        print(f"📄 Se procesaron {len(commands)} comandos")
        
        # Mostrar vista previa de las primeras líneas
        lines = markdown_content.split('\n')
        print("\n📋 Vista previa:")
        print("=" * 40)
        for line in lines[:10]:
            print(line)
        if len(lines) > 10:
            print("...")
        print("=" * 40)
        
        # Mostrar el archivo en la terminal
        print(f"\n📖 Mostrando {filename}:\n")
        subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(__file__), "show_cheatsheet.py"), filepath],
            check=False,
        )
        print(f"\n✓ Resumen: {filename} creado con {len(commands)} comandos.")
        input("Presioná Enter para volver al hub...")
        
    except KeyboardInterrupt:
        print("\n❌ Operación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
