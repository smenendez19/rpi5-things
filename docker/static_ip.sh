#!/bin/bash

# Comprobar si se ejecuta con privilegios de administrador (sudo)
if [ "$EUID" -ne 0 ]; then
  echo "[-] Por favor, ejecuta este script usando sudo: sudo ./configurar_ip_estatica.sh"
  exit 1
fi

echo "[+] Buscando la conexión Wi-Fi activa..."

# Obtener el nombre de la conexión activa de tipo inalámbrico (wireless)
CONNECTION_NAME=$(nmcli -t -f NAME,TYPE,ACTIVE connection show --active | grep 'wireless' | cut -d: -f1)

if [ -z "$CONNECTION_NAME" ]; then
  echo "[-] No se encontró ninguna conexión Wi-Fi activa. Asegúrate de estar conectado a una red."
  exit 1
fi

echo "[+] Conexión Wi-Fi detectada: $CONNECTION_NAME"

# Solicitar los datos de red al usuario

STATIC_IP="192.168.0.210/24"
GATEWAY="192.168.0.1"
DNS="8.8.8.8,8.8.4.4"

echo "[+] Aplicando la configuración estática en NetworkManager..."

# Modificar la conexión con los parámetros proporcionados
nmcli connection modify "$CONNECTION_NAME" ipv4.addresses "$STATIC_IP" ipv4.method manual
nmcli connection modify "$CONNECTION_NAME" ipv4.gateway "$GATEWAY"
nmcli connection modify "$CONNECTION_NAME" ipv4.dns "$DNS"

echo "[+] Reiniciando la conexión Wi-Fi para aplicar los cambios..."
nmcli connection down "$CONNECTION_NAME" && nmcli connection up "$CONNECTION_NAME"

echo "[✓] ¡Configuración completada con éxito! Tu Raspberry Pi ahora tiene la IP estática configurada."