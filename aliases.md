# 🔧 Mis Alias Personalizados

> Fuente de verdad: aliases y funciones reales de Fish en `~/.config/fish/config.fish`, `~/.config/fish/conf.d/aliases.fish` y `~/.config/fish/functions/`.

## ✏️ Editores y FZF
```bash
v                               # nvim - Abrir Neovim
fzfbat                          # fzf --preview="bat --theme=gruvbox-dark --color=always {}"
fzfnvim                         # nvim (fzf --preview="bat --theme=gruvbox-dark --color=always {}")
```

## 📁 Listado y navegación
```bash
ls                              # ls -la
l                               # lsd -l
la                              # lsd -a
lla                             # lsd -la
lt                              # lsd --tree
l1                              # tree -L 1
l2                              # tree -L 2
l3                              # tree -L 3
pj <proyecto>                   # Saltar a un proyecto definido en $PROJECT_PATHS
pj open <proyecto>              # Saltar a un proyecto y abrirlo con $EDITOR
antigravity [ruta]              # Abrir ruta en Finder; por defecto abre el directorio actual
```

## 🐍 Python / Entornos virtuales
```bash
cvenv                           # python3 -m venv .venv
avenv                           # source .venv/bin/activate.fish
```

## 🐍 Django Management Commands
```bash
runserver                       # python3 manage.py runserver
createsuperuser                 # python3 manage.py createsuperuser
check                           # python3 manage.py check
migrate                         # python3 manage.py makemigrations; python3 manage.py migrate
```

## 🐳 Docker
```bash
dk                              # docker
dkps                            # docker ps
dkpsa                           # docker ps -a
dkstart                         # docker start
dkstarti                        # docker start
dkcdown                         # docker compose down
dkcupd                          # docker compose up -d
dkcupi                          # docker compose up -d -i
dkcps                           # docker compose ps
dkclog                          # docker compose logs -f
dkcbuild                        # docker compose build
```

## 🖥️ Servidores y utilidades locales
```bash
cserver                         # ssh jserver
commit                          # /Users/jalberth/Documents/customUtils/customsGIT.bash $argv
tmux                            # command tmux -2 $argv
```

## 📚 Sistema de Cheat Sheets
```bash
cs                              # Mostrar menú de cheatsheets
cs <herramienta>                # Ver cheatsheet de herramienta
cheat                           # Compatibilidad: llama a cs
cheat <herramienta>             # Compatibilidad: llama a cs <herramienta>
csnew <herramienta>             # ~/.cheatsheets/csnew - Crear cheatsheet nuevo
csadd <herramienta>             # ~/.cheatsheets/csadd - Agregar comandos a cheatsheet existente
csedit <herramienta>            # ~/.cheatsheets/csedit - Editar comandos de un cheatsheet
csdel <herramienta>             # ~/.cheatsheets/csdel - Eliminar comandos de un cheatsheet
cshelp                          # ~/.cheatsheets/cshelp - Mostrar ayuda completa
csalias                         # ~/.cheatsheets/csalias - Agregar alias vivo
```

---
*Actualizado: 2026-07-15*
