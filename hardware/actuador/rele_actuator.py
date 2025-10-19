import time

import gpiod

RELE_PIN = 20


def connect_rele(pin):
    request = gpiod.request_lines(
        "/dev/gpiochip4", consumer="rele-actuator", config={pin: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)}
    )
    return request


if __name__ == "__main__":
    request = connect_rele(RELE_PIN)

    print(f"Actuator connected on GPIO pin {RELE_PIN}")

    try:
        while True:
            print("RELE OPENED")
            request.set_value(RELE_PIN, gpiod.line.Value.ACTIVE)
            time.sleep(20)
            print("RELE CLOSED")
            request.set_value(RELE_PIN, gpiod.line.Value.INACTIVE)
            time.sleep(3)
    except KeyboardInterrupt:
        print("SHUTTING DOWN")
        request.set_value(RELE_PIN, gpiod.line.Value.INACTIVE)
    finally:
        request.release()
