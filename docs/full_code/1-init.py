from machine import Pin, SPI
import time
from game_engine import *
import ssd1306

# inicializace tlacitek
tlacitko_nahoru = Pin(0, Pin.IN, Pin.PULL_DOWN)
# ... dalsi tlacitka

# velikost displeje
displej_vyska = 64
displej_sirka = 128

# inicializace tlacitek
spi = SPI(1, 80_000_000, sck=Pin(10), mosi=Pin(11))
display = ssd1306.SSD1306_SPI(displej_vyska, displej_sirka, spi, dc=Pin(8), res=Pin(7), cs=Pin(9))

# cesty k obrazkum
dino_path = "/images/dino-cropped-20-22.pbm"
kaktus_path = "/images/cactus.pbm"

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

# herni smycka
# ...