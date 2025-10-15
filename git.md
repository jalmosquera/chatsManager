# 🔀 Git - Comandos Esenciales

## ⚙️ Configuración inicial
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

## 📁 Repositorio local
```bash
git init                    # Inicializar repositorio
git status                  # Ver estado de archivos
git add .                   # Agregar todos los archivos
git add archivo.txt         # Agregar archivo específico
git commit -m "mensaje"     # Confirmar cambios
git log                     # Ver historial
git log --oneline           # Historial resumido
```

## 🌳 Ramas (Branches)
```bash
git branch                  # Listar ramas
git branch nueva-rama       # Crear rama
git checkout rama           # Cambiar a rama
git checkout -b nueva-rama  # Crear y cambiar a rama
git merge rama              # Fusionar rama
git branch -d rama          # Eliminar rama
```

## 🌐 Repositorio remoto
```bash
git remote add origin url   # Agregar origen remoto
git push origin main        # Subir cambios
git pull origin main        # Descargar cambios
git clone url               # Clonar repositorio
git fetch                   # Descargar sin fusionar
```

## ↩️ Deshacer cambios
```bash
git reset HEAD archivo      # Quitar de staging
git checkout -- archivo    # Descartar cambios
git reset --hard HEAD~1    # Deshacer último commit
git revert commit-hash      # Revertir commit específico
```