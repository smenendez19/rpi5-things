# Containers de docker para servidores en rpi5

## Dockhand

- **Función**: Servicio para gestion de containers de docker
- **Puerto**: 3000
- **Ubicación**: `docker/dockhand/docker-compose.yml`
- **Uso**:

    cd docker/dockhand
    docker compose up -d

## AdGuard Home

- **Función**: Servidor DNS que bloquea anuncios y trackers a nivel de red
- **Puerto**: 80 (Admin Panel), 53 (DNS)
- **Ubicación**: `docker/adguardhome/docker-compose.yml`
- **Uso**:

        cd docker/adguardhome
        docker-compose up -d

## Home Assistant

- **Función**: Plataforma de domótica para automatización del hogar
- **Puerto**: 8123
- **Ubicación**: `docker/homeassistant/docker-compose.yml`
- **Uso**:

        cd docker/homeassistant
        docker-compose up -d

## Minecraft Server

- **Función**: Servidor de Minecraft Java Edition
- **Puerto**: 25565
- **Versión**: 1.21.4
- **Memoria**: 4GB
- **Ubicación**: `docker/minecraftserver/docker-compose.yml`
- **Uso**:

        cd docker/minecraftserver
        docker-compose up -d

## WatchYourLAN

- **Función**: Monitor de red que detecta dispositivos conectados
- **Puerto**: 8840
- **Interfaces**: wlan0, eth0
- **Ubicación**: `docker/watchyourlan/docker-compose.yml`
- **Uso**:

        cd docker/watchyourlan
        docker-compose up -d

## Comandos útiles de Docker

    # Ver contenedores en ejecución
    docker ps

    # Ver todos los contenedores
    docker ps -a

    # Detener un contenedor
    docker stop <nombre_contenedor>

    # Eliminar un contenedor
    docker rm <nombre_contenedor>

    # Ver logs de un contenedor
    docker logs <nombre_contenedor>

    # Acceder a un contenedor
    docker exec -it <nombre_contenedor> /bin/bash
