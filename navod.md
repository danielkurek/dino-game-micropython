# Rychlé odkazy

- [Rychlé odkazy](#rychlé-odkazy)
- [Základní hra](#základní-hra)
  - [Zprovoznení tlačítek](#zprovoznení-tlačítek)
  - [Zprovoznění displeje](#zprovoznění-displeje)
  - [Kreslení na displej](#kreslení-na-displej)
  - [Pokročilé ovládání displeje](#pokročilé-ovládání-displeje)
  - [Herní logika](#herní-logika)
    - [Inicializace](#inicializace)
    - [Herní smyčka](#herní-smyčka)
  - [Pohyb kaktusu](#pohyb-kaktusu)
  - [Skákání](#skákání)
  - [Ukončení hry](#ukončení-hry)
  - [Opakování hry](#opakování-hry)
- [Rozšíření](#rozšíření)
  - [Text pro spuštění](#text-pro-spuštění)
  - [Náhodnost kaktusů](#náhodnost-kaktusů)
  - [Skóre](#skóre)
  - [Ukládání nejlepšího skóre](#ukládání-nejlepšího-skóre)
  - [Invertování barev](#invertování-barev)
  - [Zvuky](#zvuky)

# Základní hra

## Zprovoznení tlačítek

| Tlačítko    | Pin |
|-------------|-----|
| Nahoře (UP) | GP0 |
| Dole (DWN)  | GP1 |
| Levé (L)    | GP2 |
| Pravé (R)   | GP3 |
| Zpět (BCK)  | GP4 |
| Akce (ACT)  | GP5 |

 - je potřeba importovat z knihovny `machine` třídu `Pin` - `from machine import Pin`
 - každé tlačítko, které se bude ve hře používat se musí inicializovat
  - `tlacitko_1 = Pin(0, Pin.IN, Pin.PULL_DOWN)` 
    - místo `0` bude číslo pinu (bez **GP**)
    - nemusí být `talcitko_1`, název proměnné může být i jiný
 - po inicializaci lze zjistit, jestli je tlačítko zmačknuté pomocí funkce `value()`, která vrací `True` nebo `False`
  - např.: `tlacitko_1.value()
 - (pokud je potřeba, aby tlačítko nemělo dvojkliky při zmáčknutí, musí se po přečtení stavu tlačítka počkat třeba 30ms, poté přečíst znovu a pokud jsou obě hodnoty, že je tlačítko zmáčknuté, tak provedeme to, co jsme chtěli při zmáčknutí)

## Zprovoznění displeje
 - je potřeba importovat z knihovny `machine` třídu `Pin` a `SPI` - `from machine import Pin, SPI`
 - je také potřeba knihovnu `ssd1306`, která dokáže ovládat displej - `import ssd1306`
 - napřed inicializujeme `SPI`, abychom mohli nějak komunikovat s displejem
  - na komunikaci používáme `SPI1` a piny `GP10` a `GP11`
  - `spi = SPI(1, 80_000_000, sck=Pin(10), mosi=Pin(11))`
 - poté můžeme inicializovat přímo knihovnu na komunikaci s displejem
  - používáme piny `GP8` na D/C (`Data/command`), `GP9` na `CS` (`Chip select`) a `GP7` na `RESET`
  - `display = ssd1306.SSD1306_SPI(128, 64, spi, dc=Pin(8), res=Pin(7), cs=Pin(9))`
    - 128 je výška displeje
    - 64 je šířka displeje
    - výšku i šířku doporučuji dát zvlášť do proměnné
 - můžeme tedy už zobrazovat na displej cokoliv

## Kreslení na displej
Když chceme něco zobrazit na displeje, tak napřed voláme funkce na kreslení, které pouze připravují obraz, ale na displeji se nic nebude zobrazovat. Musíme zavolat `display.show()`, aby se zobrazil připravený obraz.

 - displej má souřadnice ve tvaru `x,y`,`0,0` je v levém horním rohu, doprava se přičítá `x` (max 128), dolů se přičítá `y` (max 64)
 - na displeji zůstává předchozí snímek, takže pokud chceme zobrazit nový, tak musíme napřed vyplnit obraz barvou `display.fill(0)` - vyplní obraz černou (0=černá, 1=bílá)
 - funkce na kreslení (vždy se musí volat na objekt trídy `SSD1306`, neboli v této ukázce se musí před funkci psát `display.`)
  - `fill(c)` - vyplní obraz jednou barvou, `c` je barva - 0=černá, 1=bílá
  - `pixel(x,y)` - vrátí barvu pixelu na pozici `x` a `y`
  - `pixel(x,y,c)` - nastaví pixel na pozici `x` a `y` na barvu `c`
  - `hline(x,y,w,c)` - nakreslí vodorovnou čáru, začátek je na pozici `x,y` a délka čáry je `w` (směrem doprava), barva je `c`
  - `vline(x,y,h,c)` - nakreslí svislou čáru, začátek je na pozici `x,y` a délka čáry je `h` (směrem dolů), barva je `c`
  - `line(x1,y1,x2,y2,c)` - nakreslí rovnou čáru z pozice `x1,y1` do `x2,y2`, barva čáry je `c`
  - `rect(x,y,w,h,c)` - nakreslí obdélník (pouze obrys), levý horní roh je na pozici `x,y` a má šířku `w` a výšku `h`, barva čar je `c`
  - `fill_rect(x,y,w,h,c)` - stejné jako `rect`, ale nakraslí vyplněný obdélník
  - `text(s,x,y)` - vykreslí text (`string`) `s` na pozici `x,y`
    - barva textu je bíla
    - pozice je levý horní roh (kreslí dolů a doprava)
    - font neumí diakritiku (a nějaké speciální znaky)
    - každé písmeno má rozměry 8x8 px
  - `text(s,x,y,c)` - stejné jako `text`, ale text bude barvou `c`
  - `scroll(xstep,ystep)` - posune celý obraz o `xstep` v souřadnici `x` a `ystep` v souřadnici `y`
    - zanechává pixely, které jsou mimo posunutý obraz
      - např. pokud posuneme obraz o 10 pixelů doprava (`x`) a o 5 pixelů dolů (`y`), tak pixely se souřadnicí `x` 0 až 10 zůstanou, tak jak byly, stejně pro souřadnice s `y` 0 až 5
  - `blit(fbuf,x,y)` - pokud máme načtený obrázek v `fbuf`, tak ho můžeme zobrazit na stávající snímek
    - souřadnice `x,y` udávají levý horní roh (kreslí doprava dolů)

## Pokročilé ovládání displeje
 - metody trídy `SSD1306`
  - `poweroff()` - vypne displej
  - `poweron()` - zapne displej
  - `contrast(value)` - nastaví kontrast, `value` je číslo mezi 0 a 255 (0xFF)
  - `invert(value)` - invertuje barvy, `value` je `True` (invertováno) nebo `False`

## Herní logika
 - rozdělení
  - inicializace
  - herní smyčka

### Inicializace
 - načteme obrázky pro dinosaura a cactus (pomocí třídy `Image` z knihovny `game_engine`)
  ```python
  dino_path = "/images/dino-cropped-20-22.pbm"
  kaktus_path = "/images/cactus.pbm"

  dino_img = Image(dino_path)
  kaktus_img = Image(cactus_path)
  ```
 - vytvoříme pohybujicí se objekty pro kaktus i dinosaura, protože kaktus bude jezdit zprava doleva a dinosaurus bude skákat
  ```python
  hrac = MovingObject(10, display_height - dino_img.height, dino_img, display)
  kaktus = MovingObject(120, display_height - cactus_img.height, cactus_img, display)
  ```
  - `display_height - dino_img.height` je výpočet souřadnice `y`, aby dinosaurus byl přímo na spodním okraji displeje
  - podobně pro kaktus
  - když budou nad tak pomale spadnou až na zem, nevypadá to ale dobře, takže je lepší to přesně vypočítat
 - těsně před spuštěním herní smyčky, musíme provést jeden krok výpočtu pozic pro pohybující se objekty `physics_tick(now)` (pokud bychom to neudělaly, tak by byl při prvním snímku velký skok postav)
  ```python
  # cas od spusteni v ms
  now = time.ticks_ms()
  
  # aktualizace casu ve vypoctu pozic
  hrac.physics_tick(now)
  kaktus.physics_tick(now)

  # reset pozic, kdyby se nahodnou pohnuly
  hrac.set_pos(10, display_height - dino_img.height)
  kaktus.set_pos(120, display_height - kaktus_img.height)

  # herni smycka ...
  ```

[Celý kód 1-init.py](docs/full_code/1-init.py)

### Herní smyčka
 - jelikož nevíme kdy se hra ukončí, musíme udělat nekonečnou smyčku
 - je doporučované nezdržovat nijak tuto smyčku, jelikož každé zdržení se projeví jako sekání
 - ideálně by celá smyčka měla trvat maximálně 16ms (aby bylo 60 snímků/s)
 - budeme chtít pokaždé vytvořit nový snímek, takže na začátku smyčky vyplníme displej černou (`display.fill(0)`)
 - také budeme chtít zobrazit každý snímek poté, co ho dokončíme (`display.show()`)
  ```python
  # herni smycka
  while True:
    display.fill(0)
    # obsah herni smycky
    display.show()
  ```

## Pohyb kaktusu
Můžeme rozpohybovat kaktus a to tak, že mu nastavíme směr a rychlost ve kterém se bude pohybovat. Chceme aby se pohyboval pouze zprava doleva, takže nastavíme směr přímo doleva, neboli záporné číslo `x`. A samozřejmě, že kaktus neskáče, takže hodnota `y` bude 0.
```python
kaktus.set_motion_vector(-1.5,0)
# herni smycka...
```
Na to abychom ale kaktus viděli se pohybovat, musíme v každé herní smyčce zavolat metodu `physics_tick(now)` a `draw()`.

```python
display.fill(0)
#obsah herni smycky
now = time.ticks_ms()
kaktus.physics_tick(now)
kaktus.draw()
display.show()
```

Poté by nebylo špatné, kdyby kaktus neprojel pouze jednou, ale vícekrát. Takže musíme detekovat, že kaktus projel celou obrazovku, a poté ho přemístit doprava.
```python
# ...
# obsah herni smycky
if kaktus.x <= -kaktus_img.width:
  # premysteni kaktusu
  kaktus.set_pos(x=128)
# ...
```
 - v podmínce je `-kaktus_img.width`, aby se kaktus přesunul až po tom, co je úplně mimo obrazovku

[Celý kód: 2-obstacle.py](docs/full_code/2-obstacle.py)

## Skákání
Budeme chtít, aby dinosaurus skočil pouze při stisknutí tlačítka, takže musíme detekovat, jestli je tlačítko zmáčknuté. To se dělá pomocí `tlacitko_skok.value()`, ale napřed `tlacitko_skok` musí být [inicialozované tlačítko](#zprovoznení-tlačítek)
```python
# ...
# obsah herni smycky
now = time.ticks_ms()
if tlacitko_skok.value() and hrac.on_ground():
  # skoc
  hrac.set_motion_vector(0,-3.5)
hrac.physics_tick(now)
# ...
hrac.draw()
```
 - do podmínky musíme přidat `and hrac.on_ground()`, aby hráč nemohl skákat když už skáče
 - bylo by dobré mít v té jedné smyčce pouze jednou `now = time.ticks_ms()`, abychom nedělali práci zbytečně
 - pro přehlednost kódu je dobré udělat napřed `physics_tick` u všech objektů a až poté `draw` (ale není to potřeba)

[Celý kód: 3-jump.py](docs/full_code/3-jump.py)


## Ukončení hry
Hra není moc zábavná, když není žádná výzva. Přidáme tedy kolizi s kaktusy. Takže po tom, co se dotkneme kaktusu, tak se hra ukončí.
Musíme tedy detekovat, že se dotkneme kaktusu. Na to už máme připravenou funkci `collision_test`.
```python
# obsah herni smycky
# ...
display.show()
if hrac.collision_test([kaktus]) != None:
  break
```

[Celý kód: 4-game-over.py](docs/full_code/4-game-over.py)


## Opakování hry
Abychom nemuseli po každé smrti restartovat celý program, tak si doděláme restart hry. Navíc se hra nebude spouštět hned při spuštění programu, ale až po stisku tlačítka.

Napřed si celou herní smyčku přesuneme do funkce, kód bude takhle čitelnější.
```python
def herni_smycka():
  # inicializace
  # herni smycka
```
Poté uděláme nekonečný cyklus, který po stisknutí tlačítka spustí herní smyčku.
```python
while True:
  if tlacitko_start.value():
    herni_smycka()
```

[Celý kód: 5-repeat-game.py](docs/full_code/5-repeat-game.py)

# Rozšíření

## Text pro spuštění

Zobrazit text před začátkem hry a po ukočnění každého pokusu.
```python
display.text("Press ACT", 25, 20, 1)
display.show()
while True:
  if tlacitko_start.value():
    herni_smycka()
    display.text("Press ACT", 25, 20, 1)
    display.show()
```
Nebo lépe udělat funkci, která ten text zobrazí.
```python
def start_text():
  display.text("Press ACT", 25, 20, 1)
  display.show()

start_text()
while True:
  if tlacitko_start.value():
    herni_smycka()
    start_text()
```

## Náhodnost kaktusů

Nechceme, aby kaktus jezdil pravidelně po obrazovce. Takže musíme přidat nějakou náhodu. Lze to udělat několika způsoby, ale nejjednodušší se mi zdá přemístit kaktus na nějaké náhodné souřadnice mimo displej a kaktus sám dojede do displeje.
V pythonu jsou funkce na generaci náhodných čisel v knihovně `random`, takže na začátek souboru musíme přidat `import random`, poté můžeme vygenerovat náhodné číslo mezi `a` a `b` pomocí funkce `random.randint(a,b)`. Takže přepíšeme řádek, kde se přemiťuje kaktus, aby zahrnoval náhodu.
```python
# premysteni kaktusu
kaktus.set_pos(x=random.randint(display_width, 2*display_width))
```

## Skóre

Máme dvě možnosti, jak počítat skóre. Buď se můžeme držet originálu a počítat uběhlou vzdálenost dinosaura, nebo můžeme počítat počet přeskočených kaktusů. Ukážeme si druhou možnost.
Založíme si proměnnou, ve které si budeme uchovávat kolik skóre hrač má. Před začátkem hry musíme skóre vynulovat a při každém přeskočeném kaktusu připočítat jedničku. A samozřejmě musíme zobrazovat aktuální skóre.
```python
skore = 0
# herni smycka 
  # ...
  # kaktus je mimo obrazovku
    #premysteni kaktusu
    skore += 1
  # ...
  display.text(str(skore), 64, 0)
  # ...
```

## Ukládání nejlepšího skóre

Čtení ze souboru
```python
try:
    with io.open(best_score_path, "r") as f:
        try:
            best_score = int(f.readline())
        except ValueError:
            print("cannot read best score")
except OSError:
    print("file not found")
```
Zápis do souboru
```python
with io.open(best_score_path, "w") as f:
  f.write(str(score))
```

## Invertování barev

Každých 10 skóre budeme invertovat barvy.

Založíme novou proměnnou, která bude znamenat, jestli jsou invertované barvy. A po každé změně skóre musíme aktualizovat tuto proměnnou.

Invertování provedeme pomocí `display.invert(hodnota)`, kde `hodnota` je buď `True` nebo `False`
```python
invertovano = False
skore = 0
# herni smycka 
  # ...
  # kaktus je mimo obrazovku
    #premysteni kaktusu
    skore += 1
  # ...
  display.text(str(skore), 64, 0)
  # ...
```
## Zvuky
