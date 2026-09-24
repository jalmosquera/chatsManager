# 🔧 Mis Alias Personalizados

## 📁 ✏️ Editores y FZF
```tsv
v	nvim	Abrir Neovim
fzfbat	fzf --preview="bat --theme=gruvbox-dark --color=always {}"	-
fzfnvim	nvim (fzf --preview="bat --theme=gruvbox-dark --color=always {}")	-
```

## 📁 Listado y navegación
```tsv
ls	ls -la	-
l	lsd -l	-
la	lsd -a	-
lla	lsd -la	-
lt	lsd --tree	-
l1	tree -L 1	-
l2	tree -L 2	-
l3	tree -L 3	-
pj <proyecto>	pj <proyecto>	Saltar a un proyecto definido en $PROJECT_PATHS
pj open <proyecto>	pj open <proyecto>	Saltar a un proyecto y abrirlo con $EDITOR
antigravity [ruta]	antigravity [ruta]	Abrir ruta en Finder; por defecto abre el directorio actual
```

## 📁 🐍 Python / Entornos virtuales
```tsv
cvenv	python3 -m venv .venv	-
avenv	source .venv/bin/activate.fish	-
```

## 📁 🐍 Django Management Commands
```tsv
runserver	python3 manage.py runserver	-
createsuperuser	python3 manage.py createsuperuser	-
check	python3 manage.py check	-
migrate	python3 manage.py makemigrations;python3 manage.py migrate	python3 manage.py makemigrations; python3 manage.py migrate
```

## 📁 🐳 Docker
```tsv
dk	docker	-
dkps	docker ps	-
dkpsa	docker ps -a	-
dkstart	docker start	-
dkstarti	dkstarti	docker start
dkcdown	docker compose down	-
dkcupd	docker compose up -d	-
dkcupi	docker compose up -d -i	-
dkcps	docker compose ps	-
dkclog	docker compose logs -f	-
dkcbuild	docker compose build	-
```

## 📁 🖥️ Servidores y utilidades locales
```tsv
cserver	cserver	ssh jserver
commit	commit	/Users/jalberth/Documents/customUtils/customsGIT.bash $argv
tmux	tmux	command tmux -2 $argv
```

## 📁 📚 Sistema de Cheat Sheets
```tsv
cs	cs	Mostrar menú de cheatsheets
cs <herramienta>	cs <herramienta>	Ver cheatsheet de herramienta
cheat	cheat	Compatibilidad: llama a cs
cheat <herramienta>	cheat <herramienta>	Compatibilidad: llama a cs <herramienta>
csnew <herramienta>	csnew <herramienta>	~/.cheatsheets/csnew - Crear cheatsheet nuevo
csadd <herramienta>	csadd <herramienta>	~/.cheatsheets/csadd - Agregar comandos a cheatsheet existente
csedit <herramienta>	csedit <herramienta>	~/.cheatsheets/csedit - Editar comandos de un cheatsheet
csdel <herramienta>	csdel <herramienta>	~/.cheatsheets/csdel - Eliminar comandos de un cheatsheet
cshelp	~/.cheatsheets/cshelp	Mostrar ayuda completa
csalias	~/.cheatsheets/csalias	Agregar alias vivo
```

## 📁 Tmux
```tsv
recarga de tmux	source ~/.config/fish/conf.d/aliases.fish	recarga de tmux
```

---
*Actualizado: 2026-09-24*
