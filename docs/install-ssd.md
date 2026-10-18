# Instalacion de SSD en Raspberry pi 5

## Componentes

Para poder instalar y usar un SSD en la RPI5 se usaron los siguientes componentes:

- Geekworm X1001 PCIe a M.2 HAT Key-M NVMe SSD PIP Board <https://www.amazon.com/-/es/dp/B0CPPGGDQT>
- Cable flex
- SSD NVMe WD Digital Green 250gb
- Torretas y tornillos m2 para colocar el hat y el ssd.

## Pasos a seguir

0. Tener conectado el microsd con un sistema operativo

1. Actualizar las librerias de rpi5

        sudo apt update && sudo apt upgrade -y

2. Corroborar que la conexion del ssd esta correcta

        lsblk

    Debe salir una particion nvme

3. Agregar las siguientes lineas en /boot/firmware/config.txt

        dtparam=nvme # Habilita el puerto PCIe
        dtparam=pciex1_gen=3

4. Modificar el bootloader

        sudo rpi-eeprom-config --edit

    Debe tener lo siguiente (4=USB, 1=Memoria SD y 6=SSD)

        BOOT_ORDER=0xf416
        PCIE_PROBE=1

5. Quitar el microsd, reiniciar con el SSD, comprobar que la configuracion del wifi este correcta. Comprobar la velocidad del nvme

        sudo apt install hdparm
        sudo hdparm -t --direct /dev/nvme0n1
