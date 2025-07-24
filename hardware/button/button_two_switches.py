# Imports

import time

import gpiod

BUTTON_1_PIN = 22
BUTTON_2_PIN = 27


def connect_button(pin):
    request = gpiod.request_lines(
        "/dev/gpiochip4", consumer=f"button-test-gpio{pin}", config={pin: gpiod.LineSettings(direction=gpiod.line.Direction.INPUT, bias=gpiod.line.Bias.PULL_UP)}
    )
    return request


if __name__ == "__main__":
    button_1_request = connect_button(BUTTON_1_PIN)
    button_2_request = connect_button(BUTTON_2_PIN)

    print(f"Buttons connected on GPIO pins {BUTTON_1_PIN} and {BUTTON_2_PIN}")

    last_state_1 = gpiod.line.Value.ACTIVE
    last_state_2 = gpiod.line.Value.ACTIVE

    try:
        while True:
            current_state_1 = button_1_request.get_value(BUTTON_1_PIN)
            current_state_2 = button_2_request.get_value(BUTTON_2_PIN)

            if current_state_1 != last_state_1:
                if current_state_1 == gpiod.line.Value.INACTIVE:
                    print("Button 1 pressed at ", time.strftime("%Y-%m-%d %H:%M:%S"))
                elif current_state_1 == gpiod.line.Value.ACTIVE:
                    print("Button 1 released at ", time.strftime("%Y-%m-%d %H:%M:%S"))

            if current_state_2 != last_state_2:
                if current_state_2 == gpiod.line.Value.INACTIVE:
                    print("Button 2 pressed at ", time.strftime("%Y-%m-%d %H:%M:%S"))
                elif current_state_2 == gpiod.line.Value.ACTIVE:
                    print("Button 2 released at ", time.strftime("%Y-%m-%d %H:%M:%S"))

            last_state_1 = current_state_1
            last_state_2 = current_state_2

            time.sleep(0.05)  # Debouncing

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        button_1_request.release()
        button_2_request.release()
