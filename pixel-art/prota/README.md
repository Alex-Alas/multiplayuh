# Prota — sprite + portrait

Pixel art hecho con [pixel-art-studio](https://github.com/Gamezxz/pixel-art-studio): cada pixel lo genera un script, así que **nunca edites los PNG**; edita el `build_*.py` y vuelve a correrlo.

| Archivo (`out/`) | Qué es |
|---|---|
| `prota_sprite.png` · `@6x` | sprite chibi 32×32, frontal (frame 1) |
| `prota_idle_sheet.png` + `.json` | idle de 4 frames (respira 260 ms ×3, parpadea 120 ms), padding 1 px, JSON tipo Aseprite |
| `prota_idle@6x.gif` | preview animado |
| `*_oscuro.*` | variantes con contorno exterior `C.edge` para el fondo night del juego (el contorno ciruela se pierde contra `#141219`) |
| `prota_portrait.png` · `@4x` · `_oscuro` | busto 64×64 para cuadros de diálogo |
| `maqueta_dialogo.png` | maqueta con la paleta riso (`C`) |

Paleta compartida en `paleta.py` (25 colores, rampas con hue-shift, luz arriba-izquierda, selout ciruela).

```bash
git clone https://github.com/Gamezxz/pixel-art-studio ../../../pixel-art-studio   # o exporta PIXEL_ART_STUDIO
pip install pillow
python3 build_sprite.py && python3 build_portrait.py
```

Escalado siempre entero y nearest-neighbor (`imageSmoothingEnabled = false` en canvas, filtro *Nearest* en Godot).
