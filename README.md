# Cosas de la Raspberry PI 5

## Indice

(A COMPLETAR)

## Instalacion de dependencias Python

### Creacion de entorno virtual con venv

Se recomienda utilizar un entorno virtual para instalar las librerias necesarias

    python -m venv venv

Luego se debe activar el entorno virtual en la terminal

    source venv/bin/activate

Si se cuenta con Python 3 para instalar las dependencias para utilizar GPIO hay que escribir lo siguiente:

    sudo apt-get install python3-dev
    pip install gpiod

## Docker y Portainer

(A COMPLETAR)

## Utilizacion de scripts

(A COMPLETAR)

## Actuadores probados

### Buzzer Pasivo

- Es un sensor que funciona con voltajes bajos a 5v produciendo diferentes sonidos debido a la oscilacion entre los voltajes
- Se debe conectar el positivo (marcado con un +) a uno de los pines GPIO y el negativo a uno de los GND (Ground)

(FOTO)
(IMAGEN DE CONEXION)
(VIDEO DE FUNCIONAMIENTO)

### Display OLED SSD1306

- Es un actuador que funciona con 5v y 4 pines conectados.
- Produce una imagen pixelada de 128x64 px
- Se deben soldar los 4 pines (si se necesita ya que vienen desarmados por lo general).
- Para poder programarlo con Python hay que instalar lo siguiente:

        pip install adafruit-circuitpython-displayio-ssd1306
        pip install adafruit-circuitpython-ssd1306
        pip install lgpio
- Es monocromatico, solo tiene color blanco y negro.
- Como opcional se puede utilizar la libreria pillow para trabajar con texto e imagenes.

        pip install pillow

(FOTO)
(IMAGEN DE CONEXION)
(VIDEO DE FUNCIONAMIENTO)

## Sensores probados

### Camara Raspberry PI Camera v1.3 5MP OV5647

- Una camara para la Raspberry PI sin necesidad de usar pines.
- Se conecta con un cable flex de 22 a 15 pines.
- Para poder utilizarlo se puede iniciar desde rpicam.

        rpicam-hello # Prueba de que la camara funciona
- Para poder realizar scripts y codigo con la camara se utiliza picamera2 en Python:

        pip install picamera2

### Sensor de temperatura sumergible DS18B20

- Sensor digital de temperatura sumergible para liquidos.
- Utiliza 3 pines: 5v, GND y DQ (O pin gpio compatible con one-wire).
- Antes de utilizarlo se debe activar la comunicacion One-Wire desde la configuracion de Raspberry Pi en la terminal:

        sudo raspi-config

- Para obtener la temperatura se tiene que leer el archivo en hexadecimal que otorga la lectura y transformarlo a celsius o segun convenga.
- Para iniciar el sensor requiere ejecutar los comandos:

        modprobe w1-gpio # Inicia el pin one-wire
        modprobe w1-therm # Inicia la lectura termica del sensor

## Ruta de carpetas

(A COMPLETAR)

## Links utils

- Pinout: <https://pinout.xyz/>
- Video de conexion y uso de display oled: <https://www.youtube.com/watch?app=desktop&v=n0dHQSTSilM>
- Video de uso de PiCamera: <https://www.youtube.com/watch?v=VeWBYRpodnI>
- Articulo de uso de DS18B20 en Raspberry PI: <https://randomnerdtutorials.com/raspberry-pi-ds18b20-python/>
