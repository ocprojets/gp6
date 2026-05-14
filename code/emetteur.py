from machine import Pin, SPI
from nrf24l01 import NRF24L01
import time

spi = SPI(0, baudrate=4000000, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
csn = Pin(9, mode=Pin.OUT, value=1)
ce  = Pin(8, mode=Pin.OUT, value=0)

nrf = NRF24L01(spi, csn, ce, payload_size=8)

# Adresses 5 octets — doivent matcher entre les 2 Picos (inversées)
pipe_tx = b"\xe1\xf0\xf0\xf0\xf0"
pipe_rx = b"\xd2\xf0\xf0\xf0\xf0"

nrf.open_tx_pipe(pipe_tx)
nrf.open_rx_pipe(1, pipe_rx)

print("Emetteur prêt")

while True:
    nrf.stop_listening()
    try:
        nrf.send(b"PING")
        print("-> envoyé")
    except OSError:
        print("-> echec (pas d'ACK)")
    time.sleep(1)