#!/usr/bin/env python3
import sys
import os
import re
import subprocess
from datetime import datetime

from cheatsheet_format import format_entry, parse_entry
from runtime_paths import cheatsheets_dir as installed_cheatsheets_dir

def parse_existing_cheatsheet(content):
    """Parsea un cheatsheet existente y retorna comandos con sus ubicaciones"""
    lines = content.split('\n')
    commands = []
    current_section = None
    in_code_block = False
    line_number = 0
    
    for line in lines:
        line_number += 1
        line_stripped = line.strip()
        
        # Detectar encabezados de sección
        if line_stripped.startswith('## ') and not in_code_block:
            current_section = line_stripped[3:].strip()
            
        # Detectar bloques de código
        elif line_stripped.startswith('```'):
            in_code_block = not in_code_block
            
        # Extraer comandos del bloque de código
        elif in_code_block and line_stripped and not line_stripped.startswith('```'):
            entry = parse_entry(line)
                
            commands.append({
                'name': entry.name,
                'command': entry.command,
                'description': entry.description,
                'section': current_section,
                'line_number': line_number,
                'original_line': line
            })
    
    return commands

def display_commands(commands):
    """Muestra todos los comandos con números para selección"""
    print("📋 Comandos disponibles:\n")
    
    current_section = None
    for i, cmd in enumerate(commands, 1):
        if cmd['section'] != current_section:
            current_section = cmd['section']
            print(f"\n🔸 {current_section}")
            print("-" * 50)
        
        print(f"{i:2d}. {cmd['name']} | {cmd['command']} | {cmd['description']}")
    
    print()

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

def edit_command_interactive(cmd_info):
    """Permite editar un comando de forma interactiva"""
    print(f"\n✏️  Editando comando:")
    print(f"Sección: {cmd_info['section']}")
    print(f"Nombre actual: {cmd_info['name']}")
    print(f"Comando actual: {cmd_info['command']}")
    print(f"Descripción actual: {cmd_info['description'] or '(sin descripción)'}")
    print("💡 Escribí el nuevo valor o presioná Enter para conservar el actual.")
    print("   El comando conserva exactamente las mayúsculas y símbolos que escribís.")
    print()
    
    new_name = input(f"Nuevo nombre [{cmd_info['name']}]: ").strip()
    if not new_name:
        new_name = cmd_info['name']

    new_command = input(f"Nuevo comando [{cmd_info['command']}]: ").strip()
    if not new_command:
        new_command = cmd_info['command']
    
    # Editar descripción
    current_desc = cmd_info['description'] or ""
    new_description = input(f"Nueva descripción [{current_desc}]: ").strip()
    if new_description == "" and current_desc:
        # Si el usuario presiona enter y había descripción, mantenerla
        new_description = current_desc
    
    return new_name, new_command, new_description

def update_cheatsheet_content(original_content, commands, edited_index, new_name, new_command, new_description):
    """Actualiza el contenido del cheatsheet con el comando editado"""
    lines = original_content.split('\n')
    edited_cmd = commands[edited_index]
    line_to_edit = edited_cmd['line_number'] - 1  # -1 porque las líneas son 0-indexed
    
    new_line = format_entry(new_name, new_command, new_description)
    
    # Mantener la indentación original
    original_indent = len(edited_cmd['original_line']) - len(edited_cmd['original_line'].lstrip())
    new_line = ' ' * original_indent + new_line
    
    # Reemplazar la línea
    lines[line_to_edit] = new_line
    
    # Actualizar fecha
    updated_content = '\n'.join(lines)
    update_date = datetime.now().strftime("%Y-%m-%d")
    
    # Buscar y reemplazar la línea de fecha
    if "*Creado:" in updated_content:
        updated_content = re.sub(r'\*Creado: \d{4}-\d{2}-\d{2}\*', f'*Actualizado: {update_date}*', updated_content)
    elif "*Actualizado:" in updated_content:
        updated_content = re.sub(r'\*Actualizado: \d{4}-\d{2}-\d{2}\*', f'*Actualizado: {update_date}*', updated_content)
    
    return updated_content

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 edit_cheat.py <nombre_herramienta>")
        print("Edita comandos específicos en un cheatsheet existente")
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
    
    try:
        # Leer archivo existente
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parsear comandos
        commands = parse_existing_cheatsheet(content)
        
        if not commands:
            print(f"❌ No se encontraron comandos en {filename}")
            sys.exit(1)
        
        # Mostrar comandos
        display_commands(commands)
        
        # Solicitar selección
        while True:
            try:
                selection = input(f"Selecciona el comando a editar (1-{len(commands)}) o 'q' para salir: ").strip()
                
                if selection.lower() == 'q':
                    print("👋 ¡Hasta luego!")
                    sys.exit(0)
                
                cmd_index = int(selection) - 1
                
                if 0 <= cmd_index < len(commands):
                    break
                else:
                    print(f"❌ Por favor ingresa un número entre 1 y {len(commands)}")
                    
            except ValueError:
                print("❌ Por favor ingresa un número válido o 'q' para salir")
        
        # Editar comando seleccionado
        new_name, new_command, new_description = edit_command_interactive(commands[cmd_index])
        
        # Confirmación
        print(f"\n📝 Cambios a realizar:")
        print(f"Nombre: {commands[cmd_index]['name']} → {new_name}")
        print(f"Comando: {commands[cmd_index]['command']} → {new_command}")
        print(f"Descripción: {commands[cmd_index]['description'] or '(vacía)'} → {new_description or '(vacía)'}")
        
        confirm = input("\n¿Confirmar cambios? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("❌ Cambios cancelados")
            sys.exit(0)
        
        # Actualizar contenido
        updated_content = update_cheatsheet_content(content, commands, cmd_index, new_name, new_command, new_description)
        
        # Escribir archivo actualizado
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"✅ Comando actualizado exitosamente en {filepath}")

        # Si estamos editando aliases, sincronizar con fish
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
        print(f"\n✓ Resumen: se actualizó «{new_name}» en {tool_name}.")
        input("Presioná Enter para volver al hub...")
        
    except KeyboardInterrupt:
        print("\n❌ Operación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
