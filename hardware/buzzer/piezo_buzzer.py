# Imports

import time

import gpiod
from gpiod.line import Direction, Value

CHIP = "/dev/gpiochip0"
BUZZER_PIN = 16

NOTES = {
    "E5": 659,
    "B4": 494,
    "C5": 523,
    "D5": 587,
    "C5b": 554,
    "A4": 440,
    "F4": 349,
    "G4": 392,
    "E4": 330,
}

melody = ["E5", "B4", "C5", "D5", "C5", "B4", "A4", "A4", "C5", "E5", "D5", "C5", "B4", "B4", "C5", "D5", "E5", "C5", "A4", "A4"]

note_durations = [0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5]


def beep(freq_hz=444, duration=1.0):
    period = 1.0 / freq_hz
    half_period = period / 2
    cycles = int(duration * freq_hz)
    with gpiod.request_lines(CHIP, consumer="buzzer-example", config={BUZZER_PIN: gpiod.LineSettings(direction=Direction.OUTPUT)}) as request:
        for _ in range(cycles):
            request.set_values({BUZZER_PIN: Value.ACTIVE})
            time.sleep(half_period)
            request.set_values({BUZZER_PIN: Value.INACTIVE})
            time.sleep(half_period)


if __name__ == "__main__":
    try:
        for i in range(0, len(melody)):
            freq = NOTES[melody[i]]
            duration = note_durations[i] / 2
            beep(freq, duration)
    except KeyboardInterrupt:
        print("Beep interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Exiting buzzer example.")
