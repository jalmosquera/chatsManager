# 🔀 Git - Comandos Esenciales

## ⚙️ Configuración inicial
```tsv
git config --global user.name "Tu Nombre"	git config --global user.name "Tu Nombre"	-
git config --global user.email "tu@email.com"	git config --global user.email "tu@email.com"	-
```

## 📁 Repositorio local
```tsv
git init	git init	Inicializar repositorio
git status	git status	Ver estado de archivos
git add .	git add .	Agregar todos los archivos
git add archivo.txt	git add archivo.txt	Agregar archivo específico
git commit -m "mensaje"	git commit -m "mensaje"	Confirmar cambios
git log	git log	Ver historial
git log --oneline	git log --oneline	Historial resumido
```

## 🌳 Ramas (Branches)
```tsv
git branch	git branch	Listar ramas
git branch nueva-rama	git branch nueva-rama	Crear rama
git checkout rama	git checkout rama	Cambiar a rama
git checkout -b nueva-rama	git checkout -b nueva-rama	Crear y cambiar a rama
git merge rama	git merge rama	Fusionar rama
git branch -d rama	git branch -d rama	Eliminar rama
```

## 🌐 Repositorio remoto
```tsv
git remote add origin url	git remote add origin url	Agregar origen remoto
git push origin main	git push origin main	Subir cambios
git pull origin main	git pull origin main	Descargar cambios
git clone url	git clone url	Clonar repositorio
git fetch	git fetch	Descargar sin fusionar
```

## ↩️ Deshacer cambios
```tsv
git reset HEAD archivo	git reset HEAD archivo	Quitar de staging
git checkout -- archivo	git checkout -- archivo	Descartar cambios
git reset --hard HEAD~1	git reset --hard HEAD~1	Deshacer último commit
git revert commit-hash	git revert commit-hash	Revertir commit específico
```
