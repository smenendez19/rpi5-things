import time

import lgpio


class HX711:
    def __init__(self, dout_pin, pd_sck_pin, chip=0):
        """
        dout_pin: GPIO conectado a DOUT
        pd_sck_pin: GPIO conectado a SCK
        chip: normalmente 0 en Raspberry Pi
        """
        self.dout = dout_pin
        self.sck = pd_sck_pin
        self.chip = chip

        # Abrir handle al chip GPIO
        self.h = lgpio.gpiochip_open(chip)

        # Configurar pines
        lgpio.gpio_claim_input(self.h, self.dout)
        lgpio.gpio_claim_output(self.h, self.sck)
        # Asegurar SCK en bajo al iniciar (recomendado por datasheet)
        lgpio.gpio_write(self.h, self.sck, 0)

        # Ganancia por defecto = 128 (canal A)
        # HX711: 1 pulso extra -> A128, 2 -> B32, 3 -> A64
        self.gain = 1

        # Valores por defecto seguros
        self.offset = 0
        self.scale = 1

    def is_ready(self):
        """Devuelve True si DOUT está en LOW"""
        return lgpio.gpio_read(self.h, self.dout) == 0

    def read(self):
        """Lee un valor crudo de 24 bits del HX711"""
        # Esperar a que esté listo
        while not self.is_ready():
            time.sleep(0.001)

        data = 0
        for _ in range(24):
            lgpio.gpio_write(self.h, self.sck, 1)
            data = (data << 1) | lgpio.gpio_read(self.h, self.dout)
            lgpio.gpio_write(self.h, self.sck, 0)

        # Pulsos extra para configurar ganancia
        for _ in range(self.gain):
            lgpio.gpio_write(self.h, self.sck, 1)
            lgpio.gpio_write(self.h, self.sck, 0)

        # Convertir a número con signo de 24 bits
        if data & 0x800000:
            data -= 1 << 24
        return data

    def read_average(self, times=10):
        return sum(self.read() for _ in range(times)) / times

    def read_median(self, times=11):
        """Devuelve la mediana de N lecturas (mejor contra ruido)."""
        vals = [self.read() for _ in range(times)]
        vals.sort()
        mid = len(vals) // 2
        if len(vals) % 2:
            return vals[mid]
        return (vals[mid - 1] + vals[mid]) / 2

    def tare(self, times=15):
        # Usar mediana para minimizar el efecto de fluctuaciones durante el tarado
        self.offset = self.read_median(times if times % 2 == 1 else times + 1)
        return self.offset

    def get_units(self, times=5):
        raw = self.read_average(times) - self.offset
        if self.scale == 0:
            return 0.0
        return raw / self.scale

    def set_scale(self, scale):
        self.scale = scale

    def set_offset(self, offset):
        self.offset = offset

    def close(self):
        lgpio.gpiochip_close(self.h)


if __name__ == "__main__":
    DT = 23
    SCK = 24
    hx = HX711(DT, SCK)

    try:
        print("Tareando (celda vacía)...")
        offset = hx.tare()
        print(offset)
        input("Pon un peso de referencia y ENTER...")
        ref = float(input("Peso de referencia (g): "))
        if ref == 0:
            raise ValueError("El peso de referencia no puede ser 0")
        # Calibración correcta: usar delta crudo con peso de referencia (mediana para robustez)
        raw_con_ref = hx.read_median(15)
        delta_raw = raw_con_ref - offset
        print(f"Offset (tare): {offset:.0f} | Raw con ref: {raw_con_ref:.0f} | Delta: {delta_raw:.0f}")
        if abs(delta_raw) < 50:
            print("ADVERTENCIA: Delta de calibración muy pequeño (<50 cuentas). Revisar ganancia/conexiones/patrón.")
        hx.set_scale(delta_raw / ref)
        print(f"Calibración: scale = {hx.scale:.3f} (cuentas por gramo)")
        # Verificación rápida
        verif = hx.get_units(10)
        print(f"Verificación inmediata: {verif:.2f} g (ref {ref} g)")

        while True:
            peso = hx.get_units(10)
            print(f"Peso = {peso:.2f} g")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Saliendo...")
    finally:
        hx.close()
