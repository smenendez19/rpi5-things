import glob
import os
import time

import adafruit_ssd1306
import board
from PIL import Image, ImageDraw, ImageFont


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.05)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


def display_temperature(temperature):
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((10, 10), f"Temperatura: {temperature} C°", font=font, fill=255)
    return image


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

i2c = board.I2C()

WIDTH = 128
HEIGHT = 64
BORDER = 5

display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

display.fill(0)
display.show()


while True:
    temperature, _ = read_temp()
    display.image(display_temperature(round(temperature, 2)))
    display.show()
