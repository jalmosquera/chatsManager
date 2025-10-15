# 📚 Sistema de Gestión de Cheatsheets

Un sistema completo y elegante para crear, gestionar y consultar hojas de referencia rápida (cheatsheets) directamente desde tu terminal.

## 📑 Índice

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
  - [Ver un Cheatsheet](#ver-un-cheatsheet)
  - [Crear Nuevo Cheatsheet](#crear-nuevo-cheatsheet)
  - [Agregar Comandos](#agregar-comandos)
  - [Editar Comandos](#editar-comandos)
  - [Eliminar Comandos](#eliminar-comandos)
  - [Agregar Aliases Vivos](#agregar-aliases-vivos)
  - [Ayuda](#ayuda)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Características Avanzadas](#-características-avanzadas)
- [Ejemplos de Uso](#-ejemplos-de-uso)

## ✨ Características

- 🎯 **Gestión Intuitiva**: Sistema de comandos simple y coherente con prefijo `cs`
- 📝 **Formato Markdown**: Cheatsheets en formato Markdown con visualización elegante usando `glow`
- 🔄 **Aliases Vivos**: Crea aliases que funcionan tanto como documentación como comandos reales en tu shell
- 📁 **Organización por Categorías**: Selección interactiva de categorías al agregar comandos
- ⌨️ **Detección Automática de Atajos**: Formatea automáticamente combinaciones de teclas (Ctrl+C, Cmd+Shift+N, etc.)
- 🎨 **Emojis Inteligentes**: Asignación automática de emojis según el tipo de comando
- 🔍 **Búsqueda Fácil**: Lista todos los cheatsheets disponibles y permite búsqueda rápida
- 🔧 **Sincronización Automática**: Los aliases se sincronizan automáticamente con Fish shell

## 🔧 Requisitos

- **Fish Shell**: El sistema está diseñado para funcionar con Fish shell
- **Python 3**: Para los scripts de gestión
- **glow**: Para visualización elegante de Markdown en terminal
  ```bash
  brew install glow
  ```
- **tree** (opcional): Para los aliases de visualización de directorios

## 📦 Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/jalmosquera/chatsManager.git ~/.cheatsheets
   ```

2. **Haz ejecutables los scripts**:
   ```bash
   chmod +x ~/.cheatsheets/cs*
   chmod +x ~/.cheatsheets/*.py
   ```

3. **Configura Fish shell**:

   Copia o fusiona el contenido del archivo de aliases con tu configuración de Fish:
   ```bash
   # Si no existe el directorio, créalo
   mkdir -p ~/.config/fish/conf.d/

   # Copia o fusiona los aliases
   cp ~/.cheatsheets/fish_aliases_example.fish ~/.config/fish/conf.d/aliases.fish
   ```

4. **Recarga Fish**:
   ```bash
   exec fish
   ```

5. **Verifica la instalación**:
   ```bash
   cs
   ```

## 📖 Uso

### Ver un Cheatsheet

Para ver un cheatsheet existente:

```bash
cs <nombre-herramienta>
```

Si ejecutas `cs` sin argumentos, verás el menú principal con todos los comandos disponibles y la lista de cheatsheets existentes.

**Ejemplos**:
```bash
cs git          # Ver cheatsheet de git
cs docker       # Ver cheatsheet de docker
cs nvim         # Ver cheatsheet de nvim
```

### Crear Nuevo Cheatsheet

Crea un nuevo cheatsheet desde cero:

```bash
csnew <nombre-herramienta>
```

El sistema te pedirá:
1. Ingresar los comandos (formato: `comando - descripción`)
2. Presionar Ctrl+D cuando termines
3. Automáticamente categorizará y creará el archivo

**Ejemplo**:
```bash
csnew kubectl
# Luego ingresa:
kubectl get pods - Lista todos los pods
kubectl describe pod <nombre> - Muestra detalles de un pod
kubectl logs <pod> - Muestra logs de un pod
# Presiona Ctrl+D
```

### Agregar Comandos

Agrega comandos a un cheatsheet existente:

```bash
csadd <nombre-herramienta>
```

**Flujo interactivo**:
1. Ingresa los comandos (formato: `comando - descripción`)
2. Presiona Ctrl+D cuando termines
3. Selecciona la categoría para cada comando:
   - Elige una categoría existente (por número)
   - O crea una nueva categoría (opción 0)

**Ejemplo**:
```bash
csadd git
# Ingresa:
git stash - Guarda cambios temporalmente
git stash pop - Recupera cambios guardados
# Presiona Ctrl+D
# Luego selecciona la categoría
```

### Editar Comandos

Edita comandos existentes en un cheatsheet:

```bash
csedit <nombre-herramienta>
```

El sistema mostrará todos los comandos numerados. Selecciona el que quieres editar y modifica el comando y/o descripción.

**Ejemplo**:
```bash
csedit docker
# Selecciona el número del comando a editar
# Modifica el comando y descripción
# Confirma los cambios
```

### Eliminar Comandos

Elimina comandos de un cheatsheet:

```bash
csdel <nombre-herramienta>
```

Muestra todos los comandos y te permite seleccionar cuáles eliminar.

### Agregar Aliases Vivos

Los **aliases vivos** son alias que funcionan tanto como documentación en el cheatsheet como comandos reales en tu shell:

```bash
csalias
```

**Formato de entrada**:
```
nombre='comando' - descripción
```

**Ejemplo**:
```bash
csalias
# Ingresa:
ll='ls -lah' - Lista detallada con archivos ocultos
gst='git status' - Estado de git
# Presiona Ctrl+D
```

Los aliases se agregarán automáticamente:
- ✅ Al cheatsheet `aliases.md` (documentación)
- ✅ A tu configuración de Fish (funcionalidad)

### Ayuda

Ver ayuda completa del sistema:

```bash
cshelp
```

## 📂 Estructura del Proyecto

```
~/.cheatsheets/
├── README_ES.md                 # Documentación en español
├── README.md                    # Documentación en inglés
├── cs                          # Comando principal: ver cheatsheets
├── csnew                       # Crear nuevo cheatsheet
├── csadd                       # Agregar comandos
├── csedit                      # Editar comandos
├── csdel                       # Eliminar comandos
├── csalias                     # Agregar aliases vivos
├── cshelp                      # Ver ayuda
├── create_cheatsheet.py        # Script para crear cheatsheets
├── add_to_cheat.py            # Script para agregar comandos
├── edit_cheat.py              # Script para editar comandos
├── delete_cheat.py            # Script para eliminar comandos
├── add_alias.py               # Script para agregar aliases
├── sync_aliases.py            # Script para sincronizar aliases con Fish
└── *.md                       # Archivos de cheatsheets
```

## 🚀 Características Avanzadas

### Categorización Interactiva

Al agregar comandos con `csadd`, puedes:
- Ver todas las categorías existentes con conteo de comandos
- Seleccionar una categoría existente por número
- Crear una nueva categoría sobre la marcha

### Formateo Automático de Atajos de Teclado

El sistema detecta y formatea automáticamente combinaciones de teclas:

**Entrada**:
```
ctrl c - Copiar
cmd shift n - Nueva ventana
```

**Salida**:
```
Ctrl + C - Copiar
Cmd + Shift + N - Nueva ventana
```

### Emojis Contextuales

Los comandos reciben emojis automáticamente según su función:
- 📦 Install, add
- ⚙️ Config, setup
- 🆕 Create, new
- 🗑️ Delete, remove
- 📋 List, show
- ▶️ Start, run
- 🔨 Build
- 🚀 Deploy
- Y muchos más...

### Sincronización de Aliases

Cuando editas el cheatsheet de aliases con `csedit aliases` o `csadd aliases`, el sistema:
1. Detecta que estás modificando aliases
2. Ejecuta automáticamente el script de sincronización
3. Actualiza tu configuración de Fish
4. Te informa de los cambios

### Visualización Elegante

Todos los cheatsheets se visualizan con `glow`, que proporciona:
- Sintaxis resaltada
- Formato Markdown renderizado
- Código con colores
- Navegación fácil

## 💡 Ejemplos de Uso

### Ejemplo 1: Crear Cheatsheet de Docker

```bash
# Crear el cheatsheet
csnew docker

# Ingresar comandos
docker ps - Lista contenedores en ejecución
docker images - Lista imágenes disponibles
docker run <imagen> - Ejecuta un contenedor
docker stop <id> - Detiene un contenedor
docker rm <id> - Elimina un contenedor
# Presiona Ctrl+D

# Ver el resultado
cs docker
```

### Ejemplo 2: Agregar Más Comandos a Git

```bash
# Agregar comandos
csadd git

# Ingresar nuevos comandos
git cherry-pick <commit> - Aplica un commit específico
git rebase -i HEAD~3 - Rebase interactivo últimos 3 commits
# Presiona Ctrl+D

# Seleccionar categoría
# 1. Comandos Básicos (15 comandos)
# 2. Branching (8 comandos)
# 3. Comandos Avanzados (5 comandos)
# 0. [Crear nueva categoría]
# ¿En qué categoría agregarlo? (1-3, 0 para nueva): 3
```

### Ejemplo 3: Agregar Aliases Personalizados

```bash
# Agregar aliases que funcionan inmediatamente
csalias

# Ingresar aliases
gco='git checkout' - Cambiar de rama
gpl='git pull' - Actualizar rama
gps='git push' - Subir cambios
dc='docker-compose' - Docker compose corto
# Presiona Ctrl+D

# Los aliases ya funcionan:
gco main          # Cambia a rama main
dc up -d          # Ejecuta docker-compose up -d
```

### Ejemplo 4: Editar un Comando Existente

```bash
# Editar cheatsheet
csedit nvim

# Ver lista numerada de comandos
# 1. :w - Guardar archivo
# 2. :q - Salir
# 3. :wq - Guardar y salir
# ...

# Seleccionar comando: 1

# Editar:
# Nuevo comando [:w]: :w!
# Nueva descripción [Guardar archivo]: Guardar archivo forzadamente
# ¿Confirmar cambios? (y/n): y
```

## 🎯 Consejos y Trucos

1. **Usa descripciones claras**: Las descripciones ayudan a recordar para qué sirve cada comando
2. **Organiza por categorías**: Usa categorías lógicas para facilitar la búsqueda
3. **Aliases cortos**: Para aliases vivos, usa nombres cortos y memorables
4. **Actualiza regularmente**: Agrega comandos nuevos cuando los aprendas
5. **Sincroniza tu configuración**: Guarda el directorio `.cheatsheets` en un repo para usar en múltiples máquinas

## 🤝 Contribuciones

Este proyecto está diseñado para uso personal, pero siéntete libre de hacer fork y adaptarlo a tus necesidades.

## 📄 Licencia

MIT License - Siéntete libre de usar y modificar según tus necesidades.

---

*Creado para mantener tus comandos organizados y accesibles desde cualquier terminal* 🚀
