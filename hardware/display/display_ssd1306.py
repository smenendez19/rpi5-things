# Imports

import os
import time

import adafruit_ssd1306
import board
from PIL import Image, ImageDraw, ImageFont

i2c = board.I2C()

WIDTH = 128
HEIGHT = 64
BORDER = 5

display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

display.fill(0)
display.show()


def display_text():
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((50, 10), "Hola", font=font, fill=255)
    draw.text((50, 30), "Mundo", font=font, fill=255)
    return image


def display_image(image_path):
    image = Image.open(image_path).convert("1")
    image = image.rotate(-90, expand=True)
    image = image.resize((WIDTH, HEIGHT))
    return image


while True:
    display.image(display_text())
    display.show()
    time.sleep(2)
