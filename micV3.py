from machine import Pin, ADC, PWM
import array, time
import math

SAMPLE_RATE = 8000
DURATION    = 3
NUM_SAMPLES = SAMPLE_RATE * DURATION
PERIOD_US   = 1_000_000 // SAMPLE_RATE

mic = ADC(Pin(26))
spk = PWM(Pin(15))
spk.freq(60000)
spk.duty_u16(32768)
led = Pin(25, Pin.OUT)

buffer = array.array('H', [0] * NUM_SAMPLES)

# Enregistrement
print("Démarrage dans 1s...")
time.sleep(1)
led.on()
print(">> REC")
start = time.ticks_us()
for i in range(NUM_SAMPLES):
    target = time.ticks_add(start, i * PERIOD_US)
    while time.ticks_diff(target, time.ticks_us()) > 0:
        pass
    buffer[i] = mic.read_u16()

mn, mx = buffer[0], buffer[0]
for v in buffer:
    if v < mn: mn = v
    if v > mx: mx = v
amplitude = (mx - mn) // 2
print(f"Min={mn}  Max={mx}  Amplitude=±{amplitude}  (idéal: >5000)")

led.off()

# Vérification rapide
mn, mx = buffer[0], buffer[0]
for v in buffer:
    if v < mn: mn = v
    if v > mx: mx = v
print(f"Min={mn}  Max={mx}  Centre théorique={(mn+mx)//2}")
# Attendu après fix : min≈20000, max≈45000, centre≈32768

time.sleep(1)


# Amplifier le signal autour du centre
centre = 32768
gain = 4  # x4 : commence ici, monte à x6 si trop faible

for i in range(NUM_SAMPLES):
    v = (buffer[i] - centre) * gain + centre
    if v < 0:      v = 0
    elif v > 65535: v = 65535
    buffer[i] = v

# Lecture


led.on()
print(">> PLAY")
start = time.ticks_us()
for i in range(NUM_SAMPLES):
    target = time.ticks_add(start, i * PERIOD_US)
    while time.ticks_diff(target, time.ticks_us()) > 0:
        pass
    spk.duty_u16(buffer[i])
spk.duty_u16(32768)
led.off()
print("Fin")