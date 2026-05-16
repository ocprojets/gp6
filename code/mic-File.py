from machine import Pin, ADC
import time

mic = ADC(Pin(26))
SAMPLE_RATE = 1500
DURATION    = 2
NUM_SAMPLES = SAMPLE_RATE * DURATION
PERIOD_US   = 1_000_000 // SAMPLE_RATE

print("Démarre dans 2s — applaudis pendant l'enregistrement")
time.sleep(2)
print("REC...")

samples = []
start = time.ticks_us()
for i in range(NUM_SAMPLES):
    target = time.ticks_add(start, i * PERIOD_US)
    while time.ticks_diff(target, time.ticks_us()) > 0:
        pass
    samples.append(mic.read_u16())

with open('mic1k.csv', 'w') as f:
    for v in samples:
        f.write(str(v) + '\n')
print("Terminé")