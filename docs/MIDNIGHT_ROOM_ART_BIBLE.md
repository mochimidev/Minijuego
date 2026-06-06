# Midnight Room - Art Bible

## Vision

Midnight Room is a cozy, spooky cute and pastel goth 2D platform game about collecting decorative objects during autumn nights. The existing movement, jumps, enemies, counters and level progression stay intact; the new identity reframes collectibles as room decor rewards.

## Art Direction

- Mood: cozy exploration, soft Halloween, indie visual novel, room decoration fantasy.
- Palette: lavender `#c8a7ff`, deep purple `#24142f`, dusty pink `#e8a7bd`, soft black `#17131d`, autumn orange `#f28c45`, warm cream `#fff3dc`.
- Shape language: rounded silhouettes, chunky readable props, soft outlines, moon/star accents.
- Avoided references: no Sanrio, Monster High, Hannah Montana, Tamagotchi, Chiikawa or direct brand mimicry.

## Character

Main character: Mara Noctua.

- Dark hair with bangs.
- Expressive eyes and soft alternative styling.
- Autumn/Halloween outfit: deep purple coat, orange scarf, lavender socks, black boots.
- Portfolio assets:
  - `Assets/Images/MidnightRoom/Character/mara_front_concept.png`
  - `Assets/Images/MidnightRoom/Character/mara_side_concept.png`
  - `Assets/Images/MidnightRoom/Character/mara_expressions.png`
  - `Assets/Images/MidnightRoom/Character/mara_sprite_sheet_idle_walk_jump_fall.png`

Direct Unity replacement:

- `Assets/Images/Hanna.png` now contains Mara front art while preserving the original Unity `.meta` GUID.

## Collectibles

Diamonds are reinterpreted as special room finds. The gameplay counter can keep its internal script name, but the visual object is now a decor collectible.

Portfolio set:

- Black lipstick: `Collectibles/lipstick.png`
- Brown eyeliner: `Collectibles/liner.png`
- Scented candle: `Collectibles/candle.png`
- Kawaii plush: `Collectibles/plush.png`
- Moon lamp: `Collectibles/moonlamp.png`
- Alternative poster: `Collectibles/poster.png`
- Music vinyl: `Collectibles/vinyl.png`
- Decorative plant: `Collectibles/plant.png`
- Vintage mirror: `Collectibles/mirror.png`
- Stickers: `Collectibles/stickers.png`
- Room accessory: `Collectibles/accessory.png`
- Full atlas: `Collectibles/collectibles_atlas.png`

Direct Unity replacement:

- `Assets/Images/Diamante.png` is now a stylized room find icon.

## Environments

Scene concepts:

- Autumn forest: `Backgrounds/Fondo.png`
- Night street: `Backgrounds/Fondo2.png`
- Vintage shop: `Backgrounds/Fondo3.png`
- Halloween market: `Backgrounds/Fondo4.png`
- Customizable bedroom: `Backgrounds/Fondo5.png`
- Moon rooftop: `Backgrounds/rooftop_moon.png`

Direct Unity replacements:

- Existing `Assets/Images/Fondos/Fondo*.png` files were overwritten with Midnight Room backgrounds while preserving their `.meta` references.

## Tiles And Props

Direct Unity replacements:

- `Assets/Images/Piso.png`: autumn platform.
- `Assets/Images/Gran piso.png`: moon platform.
- `Assets/Images/Torre piso.png`: vintage/dark platform.
- `Assets/Images/Espantapajaros.png`: cute plush-like hazard replacement.
- `Assets/Images/Estrella.png`: goal/reward icon.
- `Assets/Images/Reloj.png`: cozy clock HUD icon.
- `Assets/Images/Intento.png`: attempt/charm HUD icon.

Portfolio tiles:

- `Tilesets/autumn_platform.png`
- `Tilesets/moon_platform.png`
- `Tilesets/vintage_platform.png`

Props:

- `Props/lamp.png`
- `Props/poster_alt.png`
- `Props/vinyl_player.png`
- `Props/plant_pot.png`
- `Props/mirror_vintage.png`
- `Props/sticker_pack.png`

## UI

Mockups:

- Main menu: `UI/main_menu_mockup.png`
- Pause menu: `UI/pause_menu_mockup.png`
- Victory screen: `UI/victory_mockup.png`
- Collection screen: `UI/collection_mockup.png`
- Room screen: `UI/room_mockup.png`
- HUD progress indicators: `UI/hud_progress_indicators.png`

In-game copy updated:

- Main title: Midnight Room.
- Victory message: Habitacion actualizada.
- Pause title: Pausa cozy.
- Level buttons reframed as themed searches/locations.

## Progression Fantasy

Room progression states:

- `RoomProgress/room_progress_00.png`
- `RoomProgress/room_progress_01.png`
- `RoomProgress/room_progress_02.png`
- `RoomProgress/room_progress_03.png`
- `RoomProgress/room_progress_04.png`
- `RoomProgress/room_progress_05.png`

These represent how collected objects unlock visible decoration in Mara's room. The current code does not implement persistent decoration unlocks; these assets are ready for a future non-destructive UI/progression layer.

## Production Notes

The asset generator lives in `tools/generate_midnight_room_assets.py`. Run it to reproduce the full visual package:

```powershell
& 'C:\Users\Softm\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools\generate_midnight_room_assets.py
```

No files in `Assets/Scripts` were modified.
