import math
from machine import Pin, PWM
import time

spk = PWM(Pin(15))
spk.freq(60000)

SAMPLE_RATE = 8000
FREQ_HZ     = 1000  # bip à 1 kHz, facile à reconnaître
DURATION_S  = 2

# Table sinusoïdale précalculée
N = SAMPLE_RATE // FREQ_HZ   # 8 samples par cycle
sine = [int(32768 + 16000 * math.sin(2 * math.pi * i / N)) for i in range(N)]

print("Bip test 1 kHz...")
period_us = 1_000_000 // SAMPLE_RATE
total = SAMPLE_RATE * DURATION_S

start = time.ticks_us()
for i in range(total):
    target = time.ticks_add(start, i * period_us)
    while time.ticks_diff(target, time.ticks_us()) > 0:
        pass
    spk.duty_u16(sine[i % N])

spk.duty_u16(32768)
print("Fin bip")