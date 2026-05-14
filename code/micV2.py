from machine import Pin, ADC, PWM, Timer
import array, time

SAMPLE_RATE = 8000
DURATION    = 3
NUM_SAMPLES = SAMPLE_RATE * DURATION

mic = ADC(Pin(26))
spk = PWM(Pin(15))
spk.freq(250_000)   # Porteuse plus haute → filtre RC plus efficace
spk.duty_u16(32768)

led = Pin(25, Pin.OUT)
buffer = array.array('H', [0] * NUM_SAMPLES)

# ── Enregistrement via Timer (timing précis) ──────────────────────
idx = 0

def _rec(t):
    global idx
    if idx < NUM_SAMPLES:
        buffer[idx] = mic.read_u16()
        idx += 1
    else:
        t.deinit()

print("Démarrage dans 1 seconde...")
time.sleep(1)
led.on()
print(">> REC")

idx = 0
tim = Timer()
tim.init(freq=SAMPLE_RATE, mode=Timer.PERIODIC, callback=_rec)

while idx < NUM_SAMPLES:   # attente non-bloquante
    time.sleep_ms(50)

led.off()
print("Fin enregistrement")
time.sleep(1)

# ── Correction offset DC ──────────────────────────────────────────
# Calcule la moyenne (offset DC) et recentre autour de 32768
total = 0
for v in buffer:
    total += v
dc_offset = total // NUM_SAMPLES

for i in range(NUM_SAMPLES):
    # Recentre + applique un gain réduit pour éviter la saturation
    val = (buffer[i] - dc_offset) + 32768
    # Clamp 0..65535
    buffer[i] = max(0, min(65535, val))

# ── Lecture via Timer ─────────────────────────────────────────────
idx = 0

def _play(t):
    global idx
    if idx < NUM_SAMPLES:
        spk.duty_u16(buffer[idx])
        idx += 1
    else:
        t.deinit()
        spk.duty_u16(32768)

led.on()
print(">> PLAY")

idx = 0
tim = Timer()
tim.init(freq=SAMPLE_RATE, mode=Timer.PERIODIC, callback=_play)

while idx < NUM_SAMPLES:
    time.sleep_ms(50)

led.off()
print("Fin lecture")