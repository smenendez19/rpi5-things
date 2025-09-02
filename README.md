# Cosas de la Raspberry PI 5

## Índice

- [Instalación de dependencias Python](#instalacion-de-dependencias-python)
  - [Creación de entorno virtual con venv](#creacion-de-entorno-virtual-con-venv)
- [Docker y Portainer](#docker-y-portainer)
- [Actuadores probados](#actuadores-probados)
  - [Buzzer Pasivo](#buzzer-pasivo)
  - [Display OLED SSD1306](#display-oled-ssd1306)
  - [Display IPS SPI ST7789](#display-ips-spi-st7789)
- [Sensores probados](#sensores-probados)
  - [Cámara Raspberry PI Camera v1.3 5MP OV5647](#camara-raspberry-pi-camera-v13-5mp-ov5647)
  - [Sensor de temperatura sumergible DS18B20](#sensor-de-temperatura-sumergible-ds18b20)
  - [Sensor de ultrasonido HC-SR04](#sensor-de-ultrasonido-hc-sr04)
  - [Celda de carga con controlador HX711](#celda-de-carga-con-controlador-hx711)
- [Ruta de carpetas](#ruta-de-carpetas)
- [Links útiles](#links-utiles)

## Instalacion de dependencias Python

### Creacion de entorno virtual con venv

Se recomienda utilizar un entorno virtual para instalar las librerias necesarias

    python -m venv venv

Luego se debe activar el entorno virtual en la terminal

    source venv/bin/activate

Si se cuenta con Python 3 para instalar las dependencias para utilizar GPIO hay que escribir lo siguiente:

    sudo apt-get install python3-dev
    pip install gpiod

Para instalar las dependencias de los sensores y actuadores de este repositorio se debe ejecutar el siguiente comando:

    pip install -r hardware/requirements.txt

## Docker y Portainer

Docker es una plataforma de contenedores que permite ejecutar aplicaciones de forma aislada y reproducible. Portainer es una interfaz web para gestionar contenedores Docker de manera visual.

### Instalación de Docker

Para instalar Docker en Raspberry Pi 5, ejecuta el script de instalación incluido en el repositorio:

    bash docker/install_docker.sh

Este script realiza las siguientes acciones:

- Actualiza el sistema operativo
- Descarga e instala Docker usando el script oficial
- Añade el usuario actual al grupo docker
- Reinicia el sistema para aplicar los cambios

### Instalación de Portainer

Después de instalar Docker y reiniciar el sistema, ejecuta el script de instalación de Portainer:

    bash docker/install_portainer.sh

Portainer estará disponible en:

- **HTTPS**: `https://IP_DE_TU_RASPBERRY:9443`
- **HTTP**: `http://IP_DE_TU_RASPBERRY:8000`

### Servicios Docker disponibles

Este repositorio incluye configuraciones Docker Compose para los siguientes servicios:

#### AdGuard Home

- **Función**: Servidor DNS que bloquea anuncios y trackers a nivel de red
- **Puerto**: 80 (Admin Panel), 53 (DNS)
- **Ubicación**: `docker/adguardhome/docker-compose.yml`
- **Uso**:

        cd docker/adguardhome
        docker-compose up -d

#### Home Assistant

- **Función**: Plataforma de domótica para automatización del hogar
- **Puerto**: 8123
- **Ubicación**: `docker/homeassistant/docker-compose.yml`
- **Uso**:

        cd docker/homeassistant
        docker-compose up -d

#### Minecraft Server

- **Función**: Servidor de Minecraft Java Edition
- **Puerto**: 25565
- **Versión**: 1.21.4
- **Memoria**: 4GB
- **Ubicación**: `docker/minecraftserver/docker-compose.yml`
- **Uso**:

        cd docker/minecraftserver
        docker-compose up -d

#### Watchtower

- **Función**: Actualización automática de contenedores Docker
- **Intervalo**: Cada hora (3600 segundos)
- **Ubicación**: `docker/watchtower/docker-compose.yml`
- **Uso**:

        cd docker/watchtower
        docker-compose up -d

#### WatchYourLAN

- **Función**: Monitor de red que detecta dispositivos conectados
- **Puerto**: 8840
- **Interfaces**: wlan0, eth0
- **Ubicación**: `docker/watchyourlan/docker-compose.yml`
- **Uso**:

        cd docker/watchyourlan
        docker-compose up -d

### Comandos útiles de Docker

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

## Actuadores probados

### Buzzer Pasivo

- Es un sensor que funciona con voltajes bajos a 5v produciendo diferentes sonidos debido a la oscilacion entre los voltajes

#### Conexiones

Se debe conectar el positivo (marcado con un +) a uno de los pines GPIO y el negativo a uno de los GND (Ground)

| Buzzer Pin | Raspberry Pi 5 | GPIO | Función |
|------------|----------------|------|---------|
| +          | Pin 11         | 17   | Positivo (GPIO 17) |
| -          | GND            | -    | Negativo (GND) |

### Display OLED SSD1306

- Es un actuador que funciona con 5v.
- Produce una imagen pixelada de 128x64.
- Es monocromatico, solo tiene color blanco y negro.
- Para poder programarlo con Python hay que instalar lo siguiente:

        pip install adafruit-circuitpython-ssd1306
        pip install lgpio
- Se debe habilitar I2C para el funcionamiento del display, para eso se accede a la configuracion de Raspberry Pi en la terminal:

        sudo raspi-config

- Como opcional se puede utilizar la libreria pillow para trabajar con texto e imagenes.

        pip install pillow

#### Conexiones

| SSD1306 Pin | Raspberry Pi 5 | GPIO | Función |
|------------|----------------|------|---------|
| VCC        | 5v             | -    | Alimentación |
| GND        | GND            | -    | Tierra |
| SCL        | Pin 5         | 3   | I2C Clock |
| SDA        | Pin 3         | 2   | I2C Data |

### Display IPS SPI ST7789

- Es un display RGB
- Funciona con 3.3v y tambien se adapta a 5v
- Tiene un pin Blacklight que permite configurar el brillo de la pantalla incluso apagarla mientras tiene corriente.
- Es de 135x240 pixeles
- Para poder programarlo con Python hay que instalar lo siguiente:

        pip install adafruit-circuitpython-st7789
        pip install lgpio

#### Conexiones

Utiliza 8 pines en total

| ST7789 Pin | Raspberry Pi 5 | GPIO | Función |
|------------|----------------|------|---------|
| VCC        | 5v             | -    | Alimentación |
| GND        | GND            | -    | Tierra |
| SCL        | Pin 23         | 11   | SPI Clock (SCK) |
| SDA        | Pin 19         | 10   | SPI Data (MOSI) |
| RES        | Pin 16         | 23   | Reset |
| DC         | Pin 18         | 24   | Data/Command |
| CS         | Pin 29         | 5    | Chip Select |
| BLK        | Pin 32         | 12   | Backlight |

### Pulsador Tact Switch

- Es un pulsador que funciona con voltajes bajos a 5v.
- Se utiliza para detectar eventos de pulsación.
- Al conectarlo por defecto se encuentra en estado alto (HIGH) y al presionarlo se pone en estado bajo (LOW).

#### Conexiones

| Tact Switch Pin | Raspberry Pi 5 | GPIO | Función |
|-----------------|----------------|------|---------|
| GND             | GND            | -    | Tierra |
| GPIO            | Pin 15         | 22   | Entrada (GPIO 22) |

## Sensores probados

### Camara Raspberry PI Camera v1.3 5MP OV5647

- Una camara para la Raspberry PI sin necesidad de usar pines.
- Se conecta con un cable flex de 22 a 15 pines al puerto CSI de la Raspberry PI 5.
- Para poder utilizarlo se puede iniciar desde rpicam.

        rpicam-hello # Prueba de que la camara funciona

- Para poder realizar scripts y codigo con la camara se utiliza picamera2 en Python:

        pip install picamera2

### Sensor de temperatura sumergible DS18B20

- Sensor digital de temperatura sumergible para liquidos.
- Utiliza 3 pines: 5v, GND y DQ (O pin gpio compatible con one-wire).
- Antes de utilizarlo se debe activar la comunicacion One-Wire desde la configuracion de Raspberry Pi en la terminal:

        sudo raspi-config

- A su vez se debe activar la configuracion desde /boot/firmware/config.txt (Raspberry PI 5) y modificar la siguiente linea:

        dtoverlay=w1-gpio,gpiopin=x

Por defecto el pin gpio es el 4, pero se puede configurar por otro reemplazando la x

- Para obtener la temperatura se tiene que leer el archivo en hexadecimal que otorga la lectura y transformarlo a celsius o segun convenga.
- Para iniciar el sensor requiere ejecutar los comandos:

        modprobe w1-gpio # Inicia el pin one-wire
        modprobe w1-therm # Inicia la lectura termica del sensor

#### Conexiones

| DS18B20 Pin | Raspberry Pi 5 | GPIO | Función |
|-------------|----------------|------|---------|
| VCC         | 5v             | -    | Alimentación |
| GND         | GND            | -    | Tierra |
| DQ          | Pin 4          | 4    | One-Wire Data |

### Sensor de ultrasonido HC-SR04

- Sensor de distancia que utiliza ultrasonido para medir distancias.
- El pin Trigger se utiliza para enviar un pulso de 10us y el pin Echo recibe el pulso de retorno.
- Para utilizarlo en la Raspberry PI 5 se debe utilizar la libreria lpgio para Python:

        pip install lgpio

- El pin Trigger se puede conectar a cualquier pin GPIO y el pin Echo se conecta a un pin GPIO que soporte interrupciones.

#### Conexiones

Utiliza 4 pines: VCC, GND, Trigger y Echo.

| HC-SR04 Pin | Raspberry Pi 5 | GPIO | Función |
|-------------|----------------|------|---------|
| VCC         | 5v             | -    | Alimentación |
| GND         | GND            | -    | Tierra |
| Trigger     | Pin 23         | 11   | Trigger (GPIO 11) |
| Echo        | Pin 24         | 8    | Echo (GPIO 8) |

### Celda de carga con controlador HX711

- Amplificador de señal de 24 bits para celdas de carga y sensores de peso.
- Convierte señales analógicas muy pequeñas de la celda de carga a valores digitales.
- Soporta ganancias de 32, 64 y 128 para diferentes canales.
- Para utilizarlo en la Raspberry PI 5 se debe utilizar la libreria lgpio para Python:

        pip install lgpio

- Requiere calibración con un peso de referencia conocido para obtener mediciones precisas.
- El proceso incluye tarado (establecer punto cero) y calibración con peso conocido.

#### Conexiones

Utiliza 4 pines: VDD, VSS, DOUT y PD_SCK.

| HX711 Pin | Raspberry Pi 5 | GPIO | Función |
|-----------|----------------|------|---------|
| VDD       | 5v             | -    | Alimentación |
| VSS       | GND            | -    | Tierra |
| DOUT      | Pin 16         | 23   | Data Output (GPIO 23) |
| PD_SCK    | Pin 18         | 24   | Power Down/Serial Clock (GPIO 24) |

#### Conexiones de la celda de carga

La celda de carga se conecta al HX711 usando 4 cables (colores pueden variar):

| Cable      | HX711 Pin | Función |
|------------|-----------|---------|
| Rojo       | E+        | Excitación positiva |
| Negro      | E-        | Excitación negativa |
| Blanco     | A-        | Señal negativa |
| Verde      | A+        | Señal positiva |

## Ruta de carpetas

        pi-things/
        ├─ docker
        ├─ hardware
        |  ├─ requirements.txt
        ├─ .gitignore
        ├─ README.md

## Links utiles

- Pinout: <https://pinout.xyz/>
- Video de conexion y uso de display OLED SSD 1306: <https://www.youtube.com/watch?app=desktop&v=n0dHQSTSilM>
- Video de uso de PiCamera: <https://www.youtube.com/watch?v=VeWBYRpodnI>
- Articulo de uso de DS18B20 en Raspberry PI: <https://randomnerdtutorials.com/raspberry-pi-ds18b20-python/>
- Luma LCD: <https://luma-lcd.readthedocs.io/en/latest/index.html>
- Luma OLED: <https://luma-oled.readthedocs.io/en/latest/index.html>
- Video de uso de balanza con celda de carga y hx711: <https://www.youtube.com/watch?v=Z01gjTLE5eE>
- Uso del sensor de ultrasonido HC-SR04: <https://docs.sunfounder.com/projects/umsk/es/latest/05_raspberry_pi/pi_lesson23_ultrasonic.html>
