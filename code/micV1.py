from machine import Pin, ADC, PWM
import array
import time

# === Paramètres ===
SAMPLE_RATE = 8000          # 8 kHz : voix correcte, peu gourmand
DURATION    = 3             # secondes
NUM_SAMPLES = SAMPLE_RATE * DURATION
PERIOD_US   = 1_000_000 // SAMPLE_RATE   # 125 µs entre samples

# === Hardware ===
mic = ADC(Pin(26))                  # GP26 = ADC0, entrée micro /// pin20 physique
spk = PWM(Pin(15))                  # GP15 vers filtre RC + LM386 /// pin31 physique
spk.freq(60000)                    # porteuse 60 kHz, inaudible
spk.duty_u16(32768)                 # silence = duty 50%

led = Pin(25, Pin.OUT)              # Pico classique. Si Pico W : Pin("LED", Pin.OUT)

# Buffer en RAM (48 KB pour 3s à 8 kHz, OK sur Pico)
buffer = array.array('H', [0] * NUM_SAMPLES)

# === Enregistrement ===
print("Démarrage dans 1 seconde...")
time.sleep(1)
led.on()
print(">> REC : parle maintenant pendant 3 secondes")

start = time.ticks_us()
for i in range(NUM_SAMPLES):
    target = time.ticks_add(start, i * PERIOD_US)
    while time.ticks_diff(target, time.ticks_us()) > 0:
        pass
    buffer[i] = mic.read_u16()


min_val = min(buffer)
max_val = max(buffer)
avg_val = sum(buffer) // len(buffer)
variance = max_val - min_val

print(f"Min={min_val}  Max={max_val}  Avg={avg_val}  Écart={variance}")

led.off()
print("Fin enregistrement")
time.sleep(1)


# === Lecture ===
led.on()
print(">> PLAY")


for i in range(NUM_SAMPLES):
    target = time.ticks_add(start, i * PERIOD_US)
    while time.ticks_diff(target, time.ticks_us()) > 0:
        pass
    spk.duty_u16(buffer[i])

spk.duty_u16(32768)                 # retour silence
led.off()
print("Fin lecture")