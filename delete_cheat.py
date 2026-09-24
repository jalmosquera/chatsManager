#!/usr/bin/env python3
import sys
import os
import re
import subprocess
from datetime import datetime

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
        elif line_stripped == '```bash' or line_stripped == '```':
            in_code_block = not in_code_block
            
        # Extraer comandos del bloque de código
        elif in_code_block and line_stripped and not line_stripped.startswith('```'):
            # Parsear comando con comentario
            if '  # ' in line:
                parts = line.split('  # ', 1)
                command = parts[0].strip()
                description = parts[1].strip()
            else:
                command = line.strip()
                description = ''
                
            commands.append({
                'command': command,
                'description': description,
                'section': current_section,
                'line_number': line_number,
                'original_line': line
            })
    
    return commands

def display_commands(commands):
    """Muestra todos los comandos con números para selección"""
    print("📋 Comandos disponibles para eliminar:\n")
    
    current_section = None
    for i, cmd in enumerate(commands, 1):
        if cmd['section'] != current_section:
            current_section = cmd['section']
            print(f"\n🔸 {current_section}")
            print("-" * 50)
        
        desc_text = f" - {cmd['description']}" if cmd['description'] else ""
        print(f"{i:2d}. {cmd['command']}{desc_text}")
    
    print()

def delete_command_from_content(original_content, command_to_delete):
    """Elimina un comando específico del contenido del cheatsheet"""
    lines = original_content.split('\n')
    line_to_delete = command_to_delete['line_number'] - 1  # -1 porque las líneas son 0-indexed
    
    # Eliminar la línea
    del lines[line_to_delete]
    
    # Actualizar fecha
    updated_content = '\n'.join(lines)
    update_date = datetime.now().strftime("%Y-%m-%d")
    
    # Buscar y reemplazar la línea de fecha
    if "*Creado:" in updated_content:
        updated_content = re.sub(r'\*Creado: \d{4}-\d{2}-\d{2}\*', f'*Actualizado: {update_date}*', updated_content)
    elif "*Actualizado:" in updated_content:
        updated_content = re.sub(r'\*Actualizado: \d{4}-\d{2}-\d{2}\*', f'*Actualizado: {update_date}*', updated_content)
    
    return updated_content

def clean_empty_sections(content):
    """Elimina secciones que quedan vacías después de eliminar comandos"""
    lines = content.split('\n')
    cleaned_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Si encontramos un encabezado de sección
        if line.strip().startswith('## '):
            section_start = i
            i += 1
            
            # Buscar el contenido de la sección
            has_commands = False
            
            # Revisar las siguientes líneas hasta encontrar otra sección o el final
            while i < len(lines) and not lines[i].strip().startswith('## '):
                if lines[i].strip() and not lines[i].strip().startswith('```') and not lines[i].strip().startswith('---'):
                    # Si encontramos contenido que no sea bash block markers o separadores
                    if '```bash' not in lines[i] and '```' != lines[i].strip():
                        has_commands = True
                        break
                i += 1
            
            # Si la sección tiene comandos, agregarla
            if has_commands:
                # Agregar desde section_start hasta la posición actual (sin incluir)
                for j in range(section_start, i):
                    cleaned_lines.append(lines[j])
            # Si no tiene comandos, omitir toda la sección
            else:
                # Continuar sin agregar nada
                pass
        else:
            # Si no es un encabezado de sección, agregar la línea
            cleaned_lines.append(line)
            i += 1
    
    return '\n'.join(cleaned_lines)

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 delete_cheat.py <nombre_herramienta>")
        print("Elimina comandos específicos de un cheatsheet existente")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    cheatsheets_dir = os.path.expanduser("~/.cheatsheets")
    filename = f"{tool_name.lower().replace(' ', '_').replace('-', '_')}.md"
    filepath = os.path.join(cheatsheets_dir, filename)
    
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
        
        # Permitir selección múltiple
        print("💡 Estructura de selección: números separados por comas o rangos")
        print("   Ejemplos: 1,3,5  ·  1-3,5,7-9  ·  q para cancelar")
        
        # Solicitar selección
        while True:
            try:
                selection = input(f"Selecciona comando(s) a eliminar (1-{len(commands)}) o 'q' para salir: ").strip()
                
                if selection.lower() == 'q':
                    print("👋 ¡Hasta luego!")
                    sys.exit(0)
                
                # Parsear selección múltiple
                selected_indices = []
                
                # Dividir por comas
                parts = selection.split(',')
                for part in parts:
                    part = part.strip()
                    if '-' in part:
                        # Manejar rangos
                        try:
                            start, end = map(int, part.split('-'))
                            selected_indices.extend(range(start-1, end))  # -1 porque son 0-indexed
                        except ValueError:
                            print(f"❌ Formato de rango inválido: {part}")
                            continue
                    else:
                        # Manejar números individuales
                        try:
                            selected_indices.append(int(part) - 1)  # -1 porque son 0-indexed
                        except ValueError:
                            print(f"❌ Número inválido: {part}")
                            continue
                
                # Validar índices
                valid_indices = []
                for idx in selected_indices:
                    if 0 <= idx < len(commands):
                        if idx not in valid_indices:  # Evitar duplicados
                            valid_indices.append(idx)
                    else:
                        print(f"❌ Índice fuera de rango: {idx + 1}")
                
                if valid_indices:
                    break
                else:
                    print("❌ No se seleccionaron comandos válidos")
                    
            except ValueError:
                print("❌ Por favor ingresa números válidos, rangos o 'q' para salir")
        
        # Mostrar comandos a eliminar
        print(f"\n🗑️  Comandos a eliminar:")
        for idx in sorted(valid_indices):
            cmd = commands[idx]
            desc_text = f" - {cmd['description']}" if cmd['description'] else ""
            print(f"  • {cmd['command']}{desc_text} (Sección: {cmd['section']})")
        
        # Confirmación
        confirm = input(f"\n⚠️  ¿Confirmar eliminación de {len(valid_indices)} comando(s)? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("❌ Eliminación cancelada")
            sys.exit(0)
        
        # Eliminar comandos (empezando desde el final para no alterar los índices)
        updated_content = content
        for idx in sorted(valid_indices, reverse=True):
            updated_content = delete_command_from_content(updated_content, commands[idx])
        
        # Limpiar secciones vacías
        updated_content = clean_empty_sections(updated_content)
        
        # Escribir archivo actualizado
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ {len(valid_indices)} comando(s) eliminado(s) exitosamente de {filepath}")
        
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
