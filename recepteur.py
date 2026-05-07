from machine import Pin, SPI
from nrf24l01 import NRF24L01
import time

spi = SPI(0, baudrate=4000000, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
csn = Pin(9, mode=Pin.OUT, value=1)
ce  = Pin(8, mode=Pin.OUT, value=0)

led = Pin(25, Pin.OUT)            # Pico classique. Si Pico W : Pin("LED", Pin.OUT)

nrf = NRF24L01(spi, csn, ce, payload_size=8)

# Adresses INVERSÉES par rapport à l'émetteur
pipe_tx = b"\xd2\xf0\xf0\xf0\xf0"
pipe_rx = b"\xe1\xf0\xf0\xf0\xf0"

nrf.open_tx_pipe(pipe_tx)
nrf.open_rx_pipe(1, pipe_rx)
nrf.start_listening()

print("Recepteur prêt")

while True:
    if nrf.any():
        while nrf.any():
            data = nrf.recv()
            print("Recu:", data)
            led.on()
            time.sleep(0.3)
            led.off()
    time.sleep(0.01)