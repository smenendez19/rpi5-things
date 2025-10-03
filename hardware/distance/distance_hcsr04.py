# Controlar sensor de distancia HC-SR04

import time

import lgpio

# Configurar los pines GPIO
TRIG = 21
ECHO = 20

SOUND_VELOCITY = 34300

# Inicializar lgpio
h = lgpio.gpiochip_open(0)  # chip 0

lgpio.gpio_claim_output(h, TRIG)
lgpio.gpio_claim_input(h, ECHO)


def medir_distancia(timeout_s=1.0):
    """
    Mide la distancia usando HC-SR04.
    Devuelve distancia en cm, o None si hubo timeout.
    """
    # Enviar pulso de trigger de 10us
    lgpio.gpio_write(h, TRIG, 1)
    time.sleep(0.00001)
    lgpio.gpio_write(h, TRIG, 0)

    # Esperar inicio del eco
    start_time = time.time()
    timeout = start_time + timeout_s
    while lgpio.gpio_read(h, ECHO) == 0:
        if time.time() > timeout:
            print("Timeout esperando inicio del eco")
            return None
    inicio = time.time()

    # Esperar fin del eco
    while lgpio.gpio_read(h, ECHO) == 1:
        if time.time() > timeout:
            print("Timeout esperando fin del eco")
            return None
    fin = time.time()

    # Calcular distancia
    duracion = fin - inicio
    distancia = duracion * (SOUND_VELOCITY / 2)
    return distancia


try:
    while True:
        distancia = medir_distancia()
        print(f"Distancia: {distancia:.2f} cm")
        time.sleep(1)
except KeyboardInterrupt:
    print("Medición interrumpida por el usuario.")
finally:
    lgpio.gpiochip_close(h)
    print("Limpieza de GPIO completada.")
