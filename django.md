# 🌐 Django - Comandos Esenciales

## 🏗️ Proyecto y Apps
```tsv
django-admin startproject nombre	django-admin startproject nombre	Crear proyecto
python manage.py startapp nombre	python manage.py startapp nombre	Crear app
python manage.py runserver	python manage.py runserver	Servidor desarrollo
python manage.py runserver 8080	python manage.py runserver 8080	Servidor en puerto específico
```

## 🔄 Migraciones
```tsv
python manage.py makemigrations	python manage.py makemigrations	Crear migraciones
python manage.py migrate	python manage.py migrate	Aplicar migraciones
python manage.py showmigrations	python manage.py showmigrations	Ver estado migraciones
python manage.py sqlmigrate app 0001 # Ver SQL de migración	python manage.py sqlmigrate app 0001 # Ver SQL de migración	-
```

## 🗄️ Base de datos
```tsv
python manage.py dbshell	python manage.py dbshell	Consola de BD
python manage.py dumpdata > data.json # Exportar datos	python manage.py dumpdata > data.json # Exportar datos	-
python manage.py loaddata data.json	python manage.py loaddata data.json	Importar datos
python manage.py flush	python manage.py flush	Vaciar BD
```

## 👤 Usuarios y Admin
```tsv
python manage.py createsuperuser	python manage.py createsuperuser	Crear superusuario
python manage.py changepassword user # Cambiar contraseña	python manage.py changepassword user # Cambiar contraseña	-
python manage.py collectstatic	python manage.py collectstatic	Recopilar archivos estáticos
```

## 🔧 Desarrollo y Debug
```tsv
python manage.py shell	python manage.py shell	Consola Django
python manage.py test	python manage.py test	Ejecutar tests
python manage.py check	python manage.py check	Verificar proyecto
python manage.py diffsettings	python manage.py diffsettings	Ver diferencias en settings
```

## 📊 Modelos
```tsv
# En shell de Django	# En shell de Django	-
from app.models import Modelo	from app.models import Modelo	-
Modelo.objects.all()	Modelo.objects.all()	Todos los objetos
Modelo.objects.filter(campo=valor)	Modelo.objects.filter(campo=valor)	Filtrar
Modelo.objects.get(id=1)	Modelo.objects.get(id=1)	Obtener uno
obj = Modelo(campo=valor)	obj = Modelo(campo=valor)	Crear objeto
obj.save()	obj.save()	Guardar
obj.delete()	obj.delete()	Eliminar
```
