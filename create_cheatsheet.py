#!/usr/bin/env python3
import sys
import os
import re
import subprocess
from datetime import datetime

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

def parse_commands_input(input_text):
    """Parsea el texto de entrada y extrae comandos con descripciones"""
    commands = []
    lines = input_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Buscar patrones como "comando - descripción" o "comando # descripción"
        if ' - ' in line:
            parts = line.split(' - ', 1)
            command = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ''
        elif ' # ' in line:
            parts = line.split(' # ', 1)
            command = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ''
        else:
            # Si no hay separador claro, todo es el comando
            command = line.strip()
            description = ''
            
        if command:
            commands.append({'command': command, 'description': description})
    
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
        markdown += "```bash\n"
        
        for cmd_info in cmd_list:
            if cmd_info['description']:
                # Alinear comentarios para que se vean ordenados
                command_part = cmd_info['command']
                comment_part = f"  # {cmd_info['description']}"
                
                # Ajustar espaciado para alineación (máximo 30 caracteres para el comando)
                if len(command_part) < 30:
                    spaces_needed = 30 - len(command_part)
                    command_line = command_part + ' ' * spaces_needed + comment_part
                else:
                    command_line = command_part + comment_part
                    
                markdown += f"{command_line}\n"
            else:
                markdown += f"{cmd_info['command']}\n"
        
        markdown += "```\n\n"
    
    # Agregar footer con fecha de creación
    creation_date = datetime.now().strftime("%Y-%m-%d")
    markdown += f"---\n*Creado: {creation_date}*\n"
    
    return markdown

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 create_cheatsheet.py <nombre_herramienta>")
        print("Luego ingresa los comandos (uno por línea) y presiona Ctrl+D para finalizar")
        print("\nFormato sugerido:")
        print("comando - descripción")
        print("otro_comando # otra descripción")
        print("comando_sin_descripción")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    cheatsheets_dir = os.path.expanduser("~/.cheatsheets")
    filename = f"{tool_name.lower().replace(' ', '_').replace('-', '_')}.md"
    filepath = os.path.join(cheatsheets_dir, filename)

    # Confirm before reading stdin so the response is not consumed as a command.
    if os.path.exists(filepath):
        response = input(f"⚠️  El archivo {filename} ya existe. ¿Sobrescribir? (y/n): ")
        if response.lower() != 'y':
            print("❌ Operación cancelada")
            sys.exit(1)
    
    print(f"📝 Creando cheatsheet para {tool_name}")
    print("💡 Estructura por línea: comando - descripción")
    print("   Ejemplos: git status - Muestra el estado del repositorio")
    print("             git log --oneline # Historial compacto")
    print("Presiona Ctrl+D cuando termines:\n")
    
    try:
        # Leer entrada del usuario
        input_text = sys.stdin.read()
        
        if not input_text.strip():
            print("❌ No se ingresaron comandos")
            sys.exit(1)
        
        # Parsear comandos
        commands = parse_commands_input(input_text)
        
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
        
    except KeyboardInterrupt:
        print("\n❌ Operación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
