# Configuracion de Ollama

## Instalacion

        curl -fsSL https://ollama.com/install.sh | sh
        ollama --version

## Instalacion de modelos

        ollama run gemma3:1b

## Open webui

Open-webui es una aplicacion web con interfaz para visualizar llms instalados localmente.
Se puede instalar desde un container de docker.

## Abrir conexion a ollama desde terminal

1. Abrir el editor del service

        sudo systemctl edit ollama.service

2. Agregar lo siguiente

        [Service]
        Environment="OLLAMA_HOST=0.0.0.0:11434"
        Environment="OLLAMA_ORIGINS=*"

3. Ejecutar

        sudo systemctl daemon-reload
        sudo systemctl restart ollama
