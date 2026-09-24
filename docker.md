# 🐳 Docker - Comandos Esenciales

## 📦 Contenedores
```tsv
docker run imagen	docker run imagen	Ejecutar contenedor
docker run -d imagen	docker run -d imagen	Ejecutar en background
docker run -p 8080:80 imagen	docker run -p 8080:80 imagen	Mapear puertos
docker ps	docker ps	Contenedores corriendo
docker ps -a	docker ps -a	Todos los contenedores
docker stop container_id	docker stop container_id	Detener contenedor
docker start container_id	docker start container_id	Iniciar contenedor
docker rm container_id	docker rm container_id	Eliminar contenedor
docker logs container_id	docker logs container_id	Ver logs
docker exec -it container_id bash	docker exec -it container_id bash	Conectar a contenedor
```

## 🖼️ Imágenes
```tsv
docker images	docker images	Listar imágenes
docker pull imagen	docker pull imagen	Descargar imagen
docker build -t nombre .	docker build -t nombre .	Construir imagen
docker rmi imagen_id	docker rmi imagen_id	Eliminar imagen
docker tag imagen nuevo_tag	docker tag imagen nuevo_tag	Etiquetar imagen
```

## 📋 Docker Compose
```tsv
docker-compose up	docker-compose up	Levantar servicios
docker-compose up -d	docker-compose up -d	Levantar en background
docker-compose down	docker-compose down	Bajar servicios
docker-compose logs	docker-compose logs	Ver logs
docker-compose ps	docker-compose ps	Ver servicios corriendo
docker-compose restart	docker-compose restart	Reiniciar servicios
```

## 🧹 Limpieza
```tsv
docker system prune	docker system prune	Limpiar recursos no usados
docker container prune	docker container prune	Limpiar contenedores
docker image prune	docker image prune	Limpiar imágenes
docker volume prune	docker volume prune	Limpiar volúmenes
```
