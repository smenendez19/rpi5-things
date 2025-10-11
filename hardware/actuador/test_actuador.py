import time

import gpiod

RELE_PIN = 20


def connect_rele(pin):
    request = gpiod.request_lines(
        "/dev/gpiochip4", consumer="rele-actuador", config={pin: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)}
    )
    return request


if __name__ == "__main__":
    request = connect_rele(RELE_PIN)

    print(f"Actuator connected on GPIO pin {RELE_PIN}")

    try:
        while True:
            print("RELE ENCENDIDO")
            request.set_value(RELE_PIN, gpiod.line.Value.ACTIVE)
            time.sleep(20)
            print("RELE APAGADO")
            request.set_value(RELE_PIN, gpiod.line.Value.INACTIVE)
            time.sleep(3)
    except KeyboardInterrupt:
        print("APAGANDO")
        request.set_value(RELE_PIN, gpiod.line.Value.INACTIVE)
    finally:
        request.release()
