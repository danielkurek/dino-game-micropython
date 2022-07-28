# Dinosaur hra pro Pi Pico

- soubory:
  - `images/` - obrázky - hra využívá pouze `dino-cropped-20-22.pbm` a `cactus.pbm`
  - `dino.py` - samotná hra
  - `game_engine.py` - základní herní engine
  - `image_lib.py` - načítání `.pbm` obrázků
  - `ssd1306.py` - knihovna na ovládání displeje


# Herní engine (game_engine.py)
 - rozděleno do 3 tříd

## Image
 - načtení obrázku a uchování dat o něm
 - použití
   - do konstruktoru předat cestu k souboru
     - např. `Image("/cactus.pbm")`
 - objekt obsahuje
   - `bitmap` - samotný obrázek, který se předává funkce na vykreslení na displej `framebuf.blit()`
   - `width` - šířka v pixelech
   - `height` - výška v pixelech
## Sprite
 - nepohybující se obrázek
 - souřadnice můžou být desetinná čísla, při vykreslování se souřadnice zaokrouhlí (odstraní se všechny čísla za desetinnou tečkou (čárkou))
 - použití
   - do konstruktoru předat výchozí pozice `x` a `y`, obrázek `image` a objekt displeje `display` (pro nás objekt SSD1306)
 - metody
   - `change_image(image)` - změní obrázek - lze použít na animace
   - `draw()` - vykreslí obrázek na displej s levým horním rohem na souřadnicích tohoto objektu
   - `set_pos(x, y)` - nastaví pozici objektu
     - lze nastavit i pouze jednu souřadnici např.: `set_pos(x=10)` nebo `set_pos(y=5)` 

## MovingObject
 - je to potomek třídy `Sprite`, takže jsou dostuné všechny metody z `Sprite`
 - použití
   - do konstruktoru předat stejné věci jako ve `Sprite`
     - navíc lze změnit kde je zem a sílu gravitace pomocí `ground=64` a `gravity=0.15`
   - poté v hlavní herní smyčce volat pokaždé `physics_tick(now)`
   - nastavení pohybu pomocí `set_motion_vector(x, y)` - pohybuje se pořád v zadaném směru
     - směr `y` je pod vlivem gravitace (pokud je nastavená gravitace na nenulovou hodnotu)
 - metody
   - `physics_tick(now)` - udělá výpočet pozice pro dálší snímek
     - `now` je čas, mělo by se používat `time.ticks_ms()`
     - uchovává si čas posledního zavolání, takže pokud se delší dobu funkce nevolá, tak bude velký skok v pohybu (nemusí třeba dojít ke kolizi)
   - `on_ground()` - zkontroluje jestli je objekt na zemi (musí být přesně na zemi, pokud není, tak vratí `False`)
   - `collision_test(obstacles)` - zkontroluje, jestli se dotýká/překrývá s nějakými objekty v seznamu `obstacles` (kolize se detekuje pomocí obdélníků)
     - vrátí první objekt se kterým se překrývá, nebo `None` pokud se s ničím nepřekrývá

# TODO
 - [ ] better collision detection - pixel based
 - [ ] aligned text - center, right, (left)
   - every char should be 8x8 pixels
 - [ ] invert colors - periodically (when score is divisible by 10)
 - [ ] sound engine??
 - [ ] animations - functions (for Sprite)
 - [ ] change coordinate rounding??