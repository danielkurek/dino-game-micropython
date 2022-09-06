from machine import Pin, SPI
import time
from game_engine import *
import ssd1306

# inicializace tlacitek
tlacitko_nahoru = Pin(0, Pin.IN, Pin.PULL_DOWN)
# ... dalsi tlacitka

tlacitko_skok = tlacitko_nahoru

# velikost displeje
displej_vyska = 64
displej_sirka = 128

# inicializace tlacitek
spi = SPI(1, 80_000_000, sck=Pin(10), mosi=Pin(11))
display = ssd1306.SSD1306_SPI(displej_vyska, displej_sirka, spi, dc=Pin(8), res=Pin(7), cs=Pin(9))

spi = SPI(1, 80_000_000, sck=Pin(10), mosi=Pin(11))
display = ssd1306.SSD1306_SPI(128, 64, spi, dc=Pin(8), res=Pin(7), cs=Pin(9))

# cesty k obrazkum
dino_path = "/images/dino-cropped-20-22.pbm"
kaktus_path = "/images/kaktus.pbm"

# nacteni obrazku
dino_img = Image(dino_path)
kaktus_img = Image(kaktus_path)

# vytvoreni pohybujicich se postav/objektu
hrac = MovingObject(10, displej_vyska - dino_img.height, dino_img, display)
kaktus = MovingObject(120, displej_vyska - kaktus_img.height, kaktus_img, display)

# cas od zacatku v ms
now = time.ticks_ms()

# aktualizace casu ve vypoctu pozic
hrac.physics_tick(now)
kaktus.physics_tick(now)

# reset pozic, kdyby se nahodnou pohnuly
hrac.set_pos(10, displej_vyska - dino_img.height)
kaktus.set_pos(120, displej_vyska - kaktus_img.height)

# pohyb kaktusu
kaktus.set_motion_vector(-1.5,0)

# herni smycka
while True:
  display.fill(0)

  # cas od zacatku v ms
  now = time.ticks_ms()
  if tlacitko_skok.value() and hrac.on_ground():
    # skoc
    hrac.set_motion_vector(0,-3.5)
  
  # aktualizace pozice
  hrac.physics_tick(now)
  kaktus.physics_tick(now)

  if kaktus.x <= -kaktus_img.width:
    # premysteni kaktusu
    kaktus.set_pos(x=128)

  # vykresleni kaktusu a hrace
  kaktus.draw()
  hrac.draw()
  
  # zobrazeni na displej
  display.show()