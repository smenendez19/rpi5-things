# Imports

import time

import gpiod

BUTTON_PIN = 22


def connect_button(pin):
    request = gpiod.request_lines(
        "/dev/gpiochip4", consumer="boton", config={pin: gpiod.LineSettings(direction=gpiod.line.Direction.INPUT, bias=gpiod.line.Bias.PULL_UP)}
    )
    return request


if __name__ == "__main__":
    button_request = connect_button(BUTTON_PIN)
    print(f"Button connected on GPIO pin {BUTTON_PIN}")

    last_state = gpiod.line.Value.ACTIVE

    try:
        while True:
            current_state = button_request.get_value(BUTTON_PIN)

            if current_state != last_state:
                if current_state == gpiod.line.Value.INACTIVE:
                    print("Button pressed at ", time.strftime("%Y-%m-%d %H:%M:%S"))

            last_state = current_state

            time.sleep(0.05)  # Debouncing

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        button_request.release()
