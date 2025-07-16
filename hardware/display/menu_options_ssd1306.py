# Imports

import time

import adafruit_ssd1306
import board
import busio
from digitalio import DigitalInOut, Direction, Pull

# Configuración de la pantalla OLED (ajusta según tu pantalla Adafruit)
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuración de los pulsadores
button_up = DigitalInOut(board.D5)  # Botón para subir
button_up.direction = Direction.INPUT
button_up.pull = Pull.UP

button_down = DigitalInOut(board.D6)  # Botón para bajar
button_down.direction = Direction.INPUT
button_down.pull = Pull.UP

button_select = DigitalInOut(board.D7)  # Botón para seleccionar
button_select.direction = Direction.INPUT
button_select.pull = Pull.UP

# Lista de opciones del menú (puedes agregar más)
menu_options = ["Opción 1", "Opción 2", "Opción 3", "Opción 4", "Opción 5", "Opción 6", "Opción 7", "Opción 8"]

# Variables de control del menú
selected_index = 0  # Índice de la opción seleccionada
top_index = 0  # Índice de la primera opción visible
max_display = 4  # Máximo de opciones visibles en pantalla


# Función para mostrar el menú
def display_menu():
    display.fill(0)  # Limpia la pantalla
    for i in range(max_display):
        if top_index + i < len(menu_options):
            option = menu_options[top_index + i]
            if top_index + i == selected_index:
                # Resalta la opción seleccionada
                display.text("> " + option, 0, i * 15, 1)
            else:
                display.text("  " + option, 0, i * 15, 1)
    display.show()


# Función para mostrar la pantalla de una opción seleccionada
def show_option_screen(option):
    display.fill(0)
    display.text("Seleccionaste:", 0, 10, 1)
    display.text(option, 0, 30, 1)
    display.show()
    time.sleep(2)  # Muestra la pantalla por 2 segundos
    # Aquí puedes agregar código personalizado para cada opción
    # Por ejemplo:
    if option == "Opción 1":
        display.fill(0)
        display.text("Acción para Opción 1", 0, 30, 1)
        display.show()
        time.sleep(2)
    # Agrega más casos según las opciones


# Función para detectar flancos de bajada (pulsador presionado)
def button_pressed(button, last_state):
    current_state = button.value
    pressed = last_state and not current_state
    return pressed, current_state


# Estados iniciales de los pulsadores
last_up_state = True
last_down_state = True
last_select_state = True

# Bucle principal
while True:
    # Detectar pulsadores
    up_pressed, last_up_state = button_pressed(button_up, last_up_state)
    down_pressed, last_down_state = button_pressed(button_down, last_down_state)
    select_pressed, last_select_state = button_pressed(button_select, last_select_state)

    # Subir en el menú
    if up_pressed:
        if selected_index > 0:
            selected_index -= 1
            if selected_index < top_index:
                top_index -= 1

    # Bajar en el menú
    if down_pressed:
        if selected_index < len(menu_options) - 1:
            selected_index += 1
            if selected_index >= top_index + max_display:
                top_index += 1

    # Seleccionar opción
    if select_pressed:
        show_option_screen(menu_options[selected_index])

    # Actualizar pantalla
    display_menu()

    # Pequeña pausa para evitar rebotes
    time.sleep(0.1)
