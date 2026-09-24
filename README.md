# 📚 Sistema de Gestión de Cheatsheets

Un sistema completo y elegante para crear, gestionar y consultar hojas de referencia rápida (cheatsheets) directamente desde tu terminal.

> 🌐 **[English version / Versión en inglés](README_EN.md)**

## 📑 Índice

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
  - [Ver un Cheatsheet](#ver-un-cheatsheet)
  - [Buscar Comandos Globalmente](#buscar-comandos-globalmente)
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
- 📝 **Renderizado Rich**: Cheatsheets Markdown renderizados como tablas coloreadas de nombre, comando y descripción
- ▦ **Banners Automáticos**: Cada cheatsheet genera un banner compacto desde su título al abrirse
- 🔄 **Aliases Vivos**: Crea aliases que funcionan tanto como documentación como comandos reales en tu shell
- 📁 **Organización por Categorías**: Selección interactiva de categorías al agregar comandos
- ⌨️ **Preservación Literal**: Conserva exactamente las mayúsculas, símbolos y atajos que escribís
- 🎨 **Emojis Inteligentes**: Asignación automática de emojis según el tipo de comando
- 🔍 **Búsqueda Global**: `csfind` encuentra nombres, comandos y descripciones en todos los cheatsheets
- 🧭 **Hub Interactivo**: `cs` muestra una tabla centrada para seleccionar por número, nombre o Tab
- 🎯 **Íconos Semánticos**: Cada cheatsheet se identifica con un ícono acorde a su herramienta
- 🔧 **Sincronización Automática**: Los aliases se sincronizan automáticamente con Fish shell
- 🐧 **Instalación Portable**: Un instalador prepara macOS y Linux con las mismas dependencias y configuración

## 🔧 Requisitos

El instalador detecta e instala `fish`, `fzf`, `python3`, `less` y Rich. Soporta Homebrew en macOS y `apt`, `dnf`, `pacman` o `apk` en Linux. En macOS necesitás [Homebrew](https://brew.sh) previamente instalado; en Linux puede solicitar tu contraseña de `sudo`.

## 📦 Instalación

Cloná y ejecutá un solo comando:

```bash
git clone https://github.com/jalmosquera/chatsManager.git ~/.cheatsheets && ~/.cheatsheets/install.sh
```

El instalador crea un entorno virtual local en `~/.cheatsheets/.venv` e instala un snippet aislado en `~/.config/fish/conf.d/cheats_manager.fish`; no reemplaza tu `config.fish` ni tu archivo personal de aliases. Abrí una terminal Fish nueva o cargalo ahora:

```fish
source ~/.config/fish/conf.d/cheats_manager.fish
cs
```

Para ver las acciones sin modificar tu sistema:

```bash
~/.cheatsheets/install.sh --dry-run
```

## 📖 Uso

### Ver un Cheatsheet

Para ver un cheatsheet existente:

```bash
cs <nombre-herramienta>
```

Si ejecutas `cs` sin argumentos, se abre un hub centrado con una tabla de acciones y cheatsheets. Escribí `/` para abrir la búsqueda, o su número o nombre y presioná `Enter`; `Tab` completa el nombre y `Esc` cancela. Las acciones CRUD muestran un breadcrumb y, al terminar correctamente, un resumen que se cierra con `Enter` para volver al hub. En el selector de destino de las acciones CRUD, `q` o `Esc` cancelan y regresan al hub. Al abrir un cheatsheet desde este menú, `q` regresa al hub. Cada cheatsheet tiene un ícono semántico, por ejemplo `⚡ warp`, `🪟 tmux`, `⌨️ nvim`, `🐳 docker` y `🔀 git`.

**Ejemplos**:
```bash
cs git          # Ver cheatsheet de git
cs docker       # Ver cheatsheet de docker
cs nvim         # Ver cheatsheet de nvim
```

### Buscar Comandos Globalmente

Busca por nombre de cheatsheet, sección, nombre de registro, comando o descripción, sin distinguir mayúsculas de minúsculas:

```bash
csfind
```

El panel derecho muestra una previsualización. Una vez abierto un `.md`, la misma búsqueda queda disponible dentro del documento: `/texto` o `?texto` busca, `n`/`N` recorre coincidencias y `q` vuelve al hub.

### Crear Nuevo Cheatsheet

Crea un nuevo cheatsheet desde cero:

```bash
csnew <nombre-herramienta>
```

El sistema te pedirá, para cada registro:
1. Nombre
2. Comando
3. Descripción
4. Automáticamente categorizará y creará el archivo

**Ejemplo**:
```bash
csnew kubectl
# Nombre: Listar pods
# Comando: kubectl get pods
# Descripción: Lista todos los pods
```

### Agregar Comandos

Agrega comandos a un cheatsheet existente:

```bash
csadd <nombre-herramienta>
```

**Flujo interactivo**:
1. Ingresa nombre, comando y descripción por separado
2. Selecciona la categoría para cada comando:
   - Elige una categoría existente (por número)
   - O crea una nueva categoría (opción 0)

**Ejemplo**:
```bash
csadd git
# Nombre: Guardar cambios
# Comando: git stash
# Descripción: Guarda cambios temporalmente
# Luego selecciona la categoría
```

### Editar Comandos

Edita comandos existentes en un cheatsheet:

```bash
csedit <nombre-herramienta>
```

El sistema mostrará todos los registros numerados. Selecciona el que quieres editar y modifica el nombre, comando y/o descripción.

**Ejemplo**:
```bash
csedit docker
# Selecciona el número del comando a editar
# Modifica nombre, comando y descripción
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

El flujo pide nombre del alias, comando a ejecutar y descripción en campos separados.

**Ejemplo**:
```bash
csalias
# Nombre del alias: ll
# Comando a ejecutar: ls -lah
# Descripción: Lista detallada con archivos ocultos
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
├── README.md                    # Documentación en español (principal)
├── README_EN.md                 # Documentación en inglés
├── fish_aliases_example.fish   # Funciones Fish: cs, csfind y el hub interactivo
├── install.sh                  # Instalador para macOS y Linux
├── requirements.txt            # Dependencia Python de Rich
├── runtime_paths.py            # Rutas portables de instalación
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
├── render_cheatsheet.py        # Renderizador Rich con tablas y tema de Tmux
├── index_cheatsheets.py        # Índice de búsqueda global para csfind
└── *.md                       # Archivos de cheatsheets
```

## 🚀 Características Avanzadas

### Categorización Interactiva

Al agregar comandos con `csadd`, puedes:
- Ver todas las categorías existentes con conteo de comandos
- Seleccionar una categoría existente por número
- Crear una nueva categoría sobre la marcha

### Preservación de Comandos y Atajos

El sistema guarda el comando exactamente como lo escribís. Esto evita que atajos, flags, mayúsculas o símbolos sean modificados automáticamente:

```
ctrl+a+n - Crear sesión
git status --short - Ver estado compacto
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

Todos los cheatsheets se visualizan con Rich, que proporciona:
- Columnas separadas para nombre, comando y descripción
- Colores sincronizados con el tema activo de Tmux, con Tokyo Night como fallback
- Tablas centradas con bordes y separadores por fila
- Pager compatible con `/`, `?`, `n`, `N` y `q`

## 💡 Ejemplos de Uso

### Ejemplo 1: Crear Cheatsheet de Docker

```bash
# Crear el cheatsheet
csnew docker

# Nombre: Listar contenedores
# Comando: docker ps
# Descripción: Lista contenedores en ejecución

# Ver el resultado
cs docker
```

### Ejemplo 2: Agregar Más Comandos a Git

```bash
# Agregar comandos
csadd git

# Nombre: Aplicar commit
# Comando: git cherry-pick <commit>
# Descripción: Aplica un commit específico

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

# Nombre del alias: gco
# Comando a ejecutar: git checkout
# Descripción: Cambiar de rama

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
