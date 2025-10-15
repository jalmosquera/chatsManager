# 🐍 Django - Comandos Esenciales

## 🏗️ Proyecto y Apps
```bash
django-admin startproject nombre     # Crear proyecto
python manage.py startapp nombre     # Crear app
python manage.py runserver           # Servidor desarrollo
python manage.py runserver 8080      # Servidor en puerto específico
```

## 🔄 Migraciones
```bash
python manage.py makemigrations      # Crear migraciones
python manage.py migrate             # Aplicar migraciones  
python manage.py showmigrations      # Ver estado migraciones
python manage.py sqlmigrate app 0001 # Ver SQL de migración
```

## 🗄️ Base de datos
```bash
python manage.py dbshell             # Consola de BD
python manage.py dumpdata > data.json # Exportar datos
python manage.py loaddata data.json  # Importar datos
python manage.py flush               # Vaciar BD
```

## 👤 Usuarios y Admin
```bash
python manage.py createsuperuser     # Crear superusuario
python manage.py changepassword user # Cambiar contraseña
python manage.py collectstatic       # Recopilar archivos estáticos
```

## 🔧 Desarrollo y Debug
```bash
python manage.py shell               # Consola Django
python manage.py test                # Ejecutar tests
python manage.py check               # Verificar proyecto
python manage.py diffsettings        # Ver diferencias en settings
```

## 📊 Modelos
```python
# En shell de Django
from app.models import Modelo
Modelo.objects.all()                 # Todos los objetos
Modelo.objects.filter(campo=valor)   # Filtrar
Modelo.objects.get(id=1)            # Obtener uno
obj = Modelo(campo=valor)           # Crear objeto
obj.save()                          # Guardar
obj.delete()                        # Eliminar
```