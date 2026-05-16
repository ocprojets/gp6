from machine import Pin, PWM
import time, math

# D0 du SE019
son = Pin(26, Pin.IN, Pin.PULL_DOWN)

# Haut-parleur
spk = PWM(Pin(15))
spk.freq(60000)
spk.duty_u16(32768)
led = Pin(25, Pin.OUT)

# Bip
SAMPLE_RATE = 8000
PERIOD_US   = 1_000_000 // SAMPLE_RATE
N    = SAMPLE_RATE // 1000
sine = [int(32768 + 16000 * math.sin(2 * math.pi * i / N)) for i in range(N)]
n_bip = SAMPLE_RATE * 200 // 1000

def jouer_bip():
    led.on()
    start = time.ticks_us()
    for i in range(n_bip):
        target = time.ticks_add(start, i * PERIOD_US)
        while time.ticks_diff(target, time.ticks_us()) > 0:
            pass
        spk.duty_u16(sine[i % N])
    spk.duty_u16(32768)
    led.off()

COOLDOWN_MS  = 300
dernier_clap = time.ticks_ms()

print("En écoute — ajuste le potentiomètre du SE019 si besoin")

while True:
    if son.value() == 1:
        maintenant = time.ticks_ms()
        if time.ticks_diff(maintenant, dernier_clap) > COOLDOWN_MS:
            print("Clap détecté!")
            dernier_clap = maintenant
            jouer_bip()
    time.sleep_ms(2)