from machine import Pin, SPI
import time

spi = SPI(0, baudrate=4000000, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
csn = Pin(9, mode=Pin.OUT, value=1)
ce  = Pin(8, mode=Pin.OUT, value=0)

# Lecture du registre CONFIG (adresse 0x00)
csn.value(0)
spi.write(b'\x00')              # commande R_REGISTER + adresse 0x00
result = spi.read(1)
csn.value(1)
print("STATUS register:", hex(result[0]))

# Lecture du registre RF_CH (adresse 0x05) — devrait être 0x02 par défaut
csn.value(0)
spi.write(b'\x05')
rf_ch = spi.read(1)
csn.value(1)
print("RF_CH register:", hex(rf_ch[0]))