# 🐳 Docker - Comandos Esenciales

## 📦 Contenedores
```bash
docker run imagen               # Ejecutar contenedor
docker run -d imagen            # Ejecutar en background
docker run -p 8080:80 imagen    # Mapear puertos
docker ps                       # Contenedores corriendo
docker ps -a                    # Todos los contenedores
docker stop container_id        # Detener contenedor
docker start container_id       # Iniciar contenedor
docker rm container_id          # Eliminar contenedor
docker logs container_id        # Ver logs
docker exec -it container_id bash  # Conectar a contenedor
```

## 🖼️ Imágenes
```bash
docker images                   # Listar imágenes
docker pull imagen              # Descargar imagen
docker build -t nombre .        # Construir imagen
docker rmi imagen_id            # Eliminar imagen
docker tag imagen nuevo_tag     # Etiquetar imagen
```

## 📋 Docker Compose
```bash
docker-compose up               # Levantar servicios
docker-compose up -d            # Levantar en background
docker-compose down             # Bajar servicios
docker-compose logs             # Ver logs
docker-compose ps               # Ver servicios corriendo
docker-compose restart          # Reiniciar servicios
```

## 🧹 Limpieza
```bash
docker system prune             # Limpiar recursos no usados
docker container prune          # Limpiar contenedores
docker image prune              # Limpiar imágenes
docker volume prune             # Limpiar volúmenes
```