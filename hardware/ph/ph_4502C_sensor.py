import struct
import time

import lgpio

# --- Config I²C ---
I2C_BUS = 1
ADS1115_ADDR = 0x48
CONFIG_REG = 0x01
CONVERSION_REG = 0x00

# --- Calibración pH ---
V_PH7 = 2.5625
V_PH4 = 3.00  # voltaje en pH 4 (ajusta con tus mediciones)
SLOPE = (4.0 - 7.0) / (V_PH4 - V_PH7)


# --- Función para leer el canal A0 del ADS1115 ---
def leer_ads1115(handle):
    # Configuración: single-shot, canal A0, ±4.096 V, 128 SPS
    config = 0x4000 | 0x0200 | 0x0100 | 0x8000 | 0x0003
    # Escribir configuración
    lgpio.i2c_write_device(handle, bytes([CONFIG_REG, (config >> 8) & 0xFF, config & 0xFF]))
    time.sleep(0.2)
    # Leer resultado
    lgpio.i2c_write_device(handle, bytes([CONVERSION_REG]))
    _, data = lgpio.i2c_read_device(handle, 2)
    raw = struct.unpack(">h", data)[0]
    voltage = (raw * 4.096) / 32768.0
    return voltage


# --- Inicialización ---
chip = lgpio.gpiochip_open(0)
handle = lgpio.i2c_open(I2C_BUS, ADS1115_ADDR, 0)

print("Leyendo sensor de pH (Ctrl+C para salir)...")
try:
    while True:
        voltaje = leer_ads1115(handle)
        ph = 7.0 + SLOPE * (voltaje - V_PH7)
        print(f"V = {voltaje:.4f} V  |  pH ≈ {ph:.2f}")
        time.sleep(1.0)
except KeyboardInterrupt:
    pass
finally:
    lgpio.i2c_close(handle)
    lgpio.gpiochip_close(chip)
    print("\nFinalizado.")
