# Controlar sensor de distancia HC-SR04

import time

import lgpio

# Configurar los pines GPIO
TRIG = 27
ECHO = 22

# Abrir el chip GPIO
h = lgpio.gpiochip_open(0)

# Configurar los pines
lgpio.gpio_claim_output(h, TRIG)
lgpio.gpio_claim_input(h, ECHO)


def medir_distancia():
    # Enviar pulso de trigger
    lgpio.gpio_write(h, TRIG, 1)
    time.sleep(0.00001)
    lgpio.gpio_write(h, TRIG, 0)

    # Esperar inicio del eco
    while lgpio.gpio_read(h, ECHO) == 0:
        inicio = time.time()

    # Esperar fin del eco
    while lgpio.gpio_read(h, ECHO) == 1:
        fin = time.time()

    # Calcular distancia
    duracion = fin - inicio
    distancia = duracion * 17150
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
