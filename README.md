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
- Produce una imagen pixelada de 128x64
- Se deben soldar los 4 pines (si se necesita ya que vienen desarmados por lo general).
- Para poder programarlo con Python hay que instalar lo siguiente:

        pip install adafruit-circuitpython-ssd1306
        pip install lgpio
- Es monocromatico, solo tiene color blanco y negro.
- Como opcional se puede utilizar la libreria pillow para trabajar con texto e imagenes.

        pip install pillow

(FOTO)
(IMAGEN DE CONEXION)
(VIDEO DE FUNCIONAMIENTO)

### Display TFT ST7789

- Es un display RGB
- Utiliza 8 pines
- Funciona con 3.3v y tambien se adapta a 5v
- Tiene un pin Blacklight que permite configurar el brillo de la pantalla incluso apagarla mientras tiene corriente.
- Es de 135x240 pixeles
- Para poder programarlo con Python hay que instalar lo siguiente:

        pip install adafruit-circuitpython-st7789
        pip install lgpio

#### Conexiones

| ST7789 Pin | Raspberry Pi 5 | GPIO | Función |
|------------|----------------|------|---------|
| VCC        | 3.3V (Pin 1)   | -    | Alimentación |
| GND        | GND (Pin 6)    | -    | Tierra |
| SCL        | Pin 23         | 11   | SPI Clock (SCK) |
| SDA        | Pin 19         | 10   | SPI Data (MOSI) |
| RES        | Pin 16         | 23   | Reset |
| DC         | Pin 18         | 24   | Data/Command |
| CS         | Pin 29         | 5    | Chip Select |
| BLK        | Pin 32         | 12   | Backlight |

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

- A su vez se debe activar la configuracion desde /boot/firmware/config.txt (Raspberry PI 5) y modificar la siguiente linea:

        dtoverlay=w1-gpio,gpiopin=x

Por defecto el pin gpio es el 4, pero se puede configurar por otro reemplazando la x

- Para obtener la temperatura se tiene que leer el archivo en hexadecimal que otorga la lectura y transformarlo a celsius o segun convenga.
- Para iniciar el sensor requiere ejecutar los comandos:

        modprobe w1-gpio # Inicia el pin one-wire
        modprobe w1-therm # Inicia la lectura termica del sensor

### Sensor de ultrasonido HC-SR04

- Sensor de distancia que utiliza ultrasonido para medir distancias.
- Utiliza 4 pines: VCC, GND, Trigger y Echo.
- El pin Trigger se utiliza para enviar un pulso de 10us y el pin Echo recibe el pulso de retorno.
- Para utilizarlo en la Raspberry PI 5 se debe utilizar la libreria lpgio para Python:

        pip install lgpio

- El pin Trigger se puede conectar a cualquier pin GPIO y el pin Echo se conecta a un pin GPIO que soporte interrupciones.

## Ruta de carpetas

        pi-things/
        ├─ docker
        ├─ hardware
        |  ├─ requirements.txt
        ├─ .gitignore
        ├─ README.md

## Links utils

- Pinout: <https://pinout.xyz/>
- Video de conexion y uso de display oled: <https://www.youtube.com/watch?app=desktop&v=n0dHQSTSilM>
- Video de uso de PiCamera: <https://www.youtube.com/watch?v=VeWBYRpodnI>
- Articulo de uso de DS18B20 en Raspberry PI: <https://randomnerdtutorials.com/raspberry-pi-ds18b20-python/>
