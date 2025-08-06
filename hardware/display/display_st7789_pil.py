import threading
import time

import gpiod
import spidev
from PIL import Image, ImageDraw, ImageFont

# Configuración de pines
SPI_CS = 8  # GPIO 8 (CE0)
SPI_DC = 6  # GPIO 6
RESET = 9  # GPIO 9
BACKLIGHT = 12  # GPIO 12

# Configuración del buzzer
BUZZER_PIN = 18

# Notas musicales para el buzzer
NOTES = {
    "E5": 659,
    "B4": 494,
    "C5": 523,
    "D5": 587,
    "A4": 440,
    "F4": 349,
    "G4": 392,
    "E4": 330,
}

# Tamaño del display
WIDTH = 240
HEIGHT = 135


class BuzzerController:
    def __init__(self):
        self.running = True
        self.thread = None
        self.melody = []
        self.note_durations = []
        self.play_event = threading.Event()  # Evento para controlar cuándo reproducir

        # Iniciar el hilo automáticamente
        self.thread = threading.Thread(target=self.buzzer_thread, daemon=True)
        self.thread.start()
        print("BuzzerController iniciado y esperando comandos")

    def set_melody(self, melody, note_durations):
        """Configurar la melodía a reproducir"""
        self.melody = melody
        self.note_durations = note_durations

    def play_now(self):
        """Solicitar que se reproduzca la melodía ahora"""
        if self.melody and self.note_durations:
            self.play_event.set()  # Activar el evento para reproducir
            print("Comando de reproducción enviado")

    def beep(self, freq_hz=444, duration=1.0):
        """Generar un beep con la frecuencia y duración especificada"""
        period = 1.0 / freq_hz
        half_period = period / 2
        cycles = int(duration * freq_hz)

        with gpiod.request_lines(
            "/dev/gpiochip4", consumer="buzzer-controller", config={BUZZER_PIN: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)}
        ) as request:
            for _ in range(cycles):
                if not self.running:  # Permitir interrumpir el beep
                    break
                request.set_values({BUZZER_PIN: gpiod.line.Value.ACTIVE})
                time.sleep(half_period)
                request.set_values({BUZZER_PIN: gpiod.line.Value.INACTIVE})
                time.sleep(half_period)

    def play_melody(self):
        """Reproducir la melodía completa"""
        if not self.melody or not self.note_durations:
            return

        for i in range(len(self.melody)):
            if not self.running:
                break
            freq = NOTES.get(self.melody[i], 440)  # Usar 440Hz por defecto si la nota no existe
            duration = self.note_durations[i] / 2
            self.beep(freq, duration)
            time.sleep(0.05)  # Pequeña pausa entre notas

    def buzzer_thread(self):
        """Hilo que espera comandos de reproducción"""
        while self.running:
            try:
                # Esperar hasta que se solicite reproducir una melodía
                self.play_event.wait()
                if not self.running:
                    break

                # Reproducir la melodía
                self.play_melody()

                # Limpiar el evento para la próxima reproducción
                self.play_event.clear()

            except Exception as e:
                print(f"Error en buzzer: {e}")
                break

    def start(self):
        """El hilo ya está iniciado automáticamente"""
        print("Buzzer ya está en funcionamiento, use play_now() para reproducir")

    def stop(self):
        """Detener el hilo del buzzer"""
        if self.running:
            self.running = False
            self.play_event.set()  # Despertar el hilo para que pueda terminar
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=2)
            print("Buzzer detenido")


class ST7789Display:
    def __init__(self):
        # Configurar SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Bus 0, Device 0
        self.spi.max_speed_hz = 24000000
        self.spi.mode = 0

        # Configurar GPIO usando gpiod
        self.chip = gpiod.Chip("/dev/gpiochip4")  # En RPi 5 es gpiochip4

        # Configurar líneas GPIO
        self.dc_line = self.chip.request_lines(consumer="st7789", config={SPI_DC: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)})

        self.reset_line = self.chip.request_lines(consumer="st7789", config={RESET: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)})

        self.backlight_line = self.chip.request_lines(
            consumer="st7789", config={BACKLIGHT: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)}
        )

        self.init_display()

    def write_command(self, cmd):
        """Enviar comando al display"""
        self.dc_line.set_value(SPI_DC, gpiod.line.Value.INACTIVE)  # DC low para comando
        self.spi.xfer2([cmd])

    def write_data(self, data):
        """Enviar datos al display"""
        self.dc_line.set_value(SPI_DC, gpiod.line.Value.ACTIVE)  # DC high para datos
        if isinstance(data, list):
            self.spi.xfer2(data)
        else:
            self.spi.xfer2([data])

    def reset_display(self):
        """Reset del display"""
        self.reset_line.set_value(RESET, gpiod.line.Value.ACTIVE)
        time.sleep(0.1)
        self.reset_line.set_value(RESET, gpiod.line.Value.INACTIVE)
        time.sleep(0.1)
        self.reset_line.set_value(RESET, gpiod.line.Value.ACTIVE)
        time.sleep(0.1)

    def init_display(self):
        """Inicializar el display ST7789"""
        # Encender backlight
        self.backlight_line.set_value(BACKLIGHT, gpiod.line.Value.ACTIVE)

        # Reset
        self.reset_display()

        # Comandos de inicialización ST7789
        self.write_command(0x01)  # Software reset
        time.sleep(0.15)

        self.write_command(0x11)  # Sleep out
        time.sleep(0.5)

        self.write_command(0x3A)  # Pixel format
        self.write_data(0x05)  # 16-bit color

        self.write_command(0x36)  # Memory access control
        self.write_data(0x70)  # RGB color filter panel

        # Configurar área de display
        self.write_command(0x2A)  # Column address set
        self.write_data([0x00, 0x00, 0x00, 0xEF])  # 0-239

        self.write_command(0x2B)  # Row address set
        self.write_data([0x00, 0x00, 0x00, 0x87])  # 0-135

        self.write_command(0x21)  # Invert display
        self.write_command(0x13)  # Normal display mode
        self.write_command(0x29)  # Display on
        time.sleep(0.1)

    def set_window(self, x0, y0, x1, y1):
        """Configurar ventana de escritura"""
        self.write_command(0x2A)  # Column address set
        self.write_data([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF])

        self.write_command(0x2B)  # Row address set
        self.write_data([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF])

        self.write_command(0x2C)  # Memory write

    def display_image(self, image):
        """Mostrar imagen en el display"""
        # Redimensionar imagen si es necesario
        if image.size != (WIDTH, HEIGHT):
            image = image.resize((WIDTH, HEIGHT))

        # Convertir a RGB565
        rgb_image = image.convert("RGB")
        pixels = list(rgb_image.getdata())

        # Configurar ventana completa
        self.set_window(0, 0, WIDTH - 1, HEIGHT - 1)

        # Convertir pixels a formato RGB565
        data = []
        for pixel in pixels:
            r, g, b = pixel
            # Convertir a RGB565
            r565 = (r >> 3) << 11
            g565 = (g >> 2) << 5
            b565 = b >> 3
            rgb565 = r565 | g565 | b565

            # Dividir en bytes (big endian)
            data.append((rgb565 >> 8) & 0xFF)
            data.append(rgb565 & 0xFF)

        # Enviar datos en chunks para evitar problemas de memoria
        chunk_size = 4096
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            self.write_data(chunk)

    def cleanup(self):
        """Limpiar recursos"""
        # Apagar el display
        self.write_command(0x28)  # Display off
        time.sleep(0.1)
        self.write_command(0x10)  # Sleep in
        time.sleep(0.1)
        # Apagar backlight
        self.backlight_line.set_value(BACKLIGHT, gpiod.line.Value.INACTIVE)
        # Ignorar errores si ya está desconectado

        # Cerrar recursos
        self.spi.close()
        self.dc_line.release()
        self.reset_line.release()
        self.backlight_line.release()
        self.chip.close()


def main():
    # Crear display
    display = ST7789Display()
    buzzer = BuzzerController()

    try:
        # Crear imagen con fondo negro
        image = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibujar rectángulo blanco centrado
        rect_width = 180
        rect_height = 80
        rect_x = (WIDTH - rect_width) // 2
        rect_y = (HEIGHT - rect_height) // 2

        draw.rectangle([rect_x, rect_y, rect_x + rect_width, rect_y + rect_height], fill=(255, 255, 255), outline=(255, 255, 255))

        font = ImageFont.load_default()

        text = "Hola Mundo"

        # Calcular posición centrada del texto
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = rect_x + (rect_width - text_width) // 2
        text_y = rect_y + (rect_height - text_height) // 2

        # Dibujar texto en negro
        draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)

        # Mostrar en el display
        display.display_image(image)

        # Configurar melodía
        buzzer.set_melody(
            melody=["E5", "B4", "C5", "D5", "C5", "B4", "A4", "A4", "C5", "E5", "D5", "C5", "B4", "B4", "C5", "D5", "E5", "C5", "A4", "A4"],
            note_durations=[0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5],
        )

        print("Imagen mostrada en el display. Buzzer listo para reproducir.")

        # Mantener el programa corriendo
        while True:
            buzzer.play_now()
            time.sleep(3)

    except KeyboardInterrupt:
        print("\nSaliendo...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Detener buzzer primero
        buzzer.stop()
        # Luego limpiar display
        display.cleanup()


if __name__ == "__main__":
    main()
