#!/usr/bin/env python3
"""Prota — sprite chibi 32x32 (frontal) con idle de 4 frames.

Cada fila es (x0, texto): se coloca pixel a pixel desde x0. Leyenda en PAL.
Requiere pixel-art-studio (https://github.com/Gamezxz/pixel-art-studio);
ruta por la variable PIXEL_ART_STUDIO.
"""
import os, sys
sys.path.insert(0, os.path.join(os.environ.get("PIXEL_ART_STUDIO", "../../../pixel-art-studio"), "scripts"))
from pixelstudio import Sprite
from paleta import PAL, rim

ROWS = [
    None,
    (9,  "OOOO.OOOOO.OOOO"),
    (8,  "OHHHHOHHHHHOHHHHO"),
    (7,  "OHHHHHHHHHHHHHHHHHO"),
    (6,  "OHHHHHHHHHHHHHHHHHHHO"),
    (6,  "OHHHHHHHHHHHHHHHHHHHO"),
    (5,  "OHHHHHHHHHHHHHHHHHHHHHO"),
    (5,  "OHHHHHHHHHHHHHHHHHHHHHO"),
    (5,  "OHHHHHHHHHHHHHHHHHHHHHO"),
    (6,  "OHH" "HHHHHHHHHHHSHHH" "HHO"),
    (6,  "OHH" "KKSSSSSSSSSSHSs" "HHO"),
    (6,  "OHH" "SSBBBSSSSBBBSSs" "HHO"),
    (6,  "OH" "K" "KSSSSSSSSSSSSSs" "s" "HO"),
    (6,  "OH" "S" "SSSEWSSSSEWSSSs" "s" "HO"),
    (6,  "OH" "s" "KSSEESSSSEESSss" "s" "HO"),
    (6,  "OHH" "KSSSSSSsSSSSSss" "HHO"),
    (5,  "OHHH" "sSSSSSSMMSSSSs" "HHHHO"),
    (5,  "OHHHHO" "sSSSSSSSss" "OHHHHO"),
    (5,  "OHHO...OsssssO...OHHO"),
    (6,  "OO.OOOOTSSSSSTOOOO.OO"),
    (7,  "OUUUTTTTTTTTTTTTttO"),
    (6,  "OUTTTTTTTTXTTTTTTTttO"),
    (6,  "OtTTTTTTTXXXTTTTTTttO"),
    (6,  "OKSOTTTTTTXTTTTTtOSsO"),
    (6,  "OSsOTTTTTTTTTTTttOSsO"),
    (6,  "OKSOtTTTTTTTTTTttOSsO"),
    (7,  "OOOtttttttttttttOOO"),
    (9,  "OJJJJJJjJJJJjjO"),
    (9,  "OJJJJJjOJJJJJjO"),
    (8,  "OFFFFFfO.OFFFFFfO"),
    (8,  "OOOOOOOO.OOOOOOOO"),
]
# rizos: (x, y, plantilla) estampados solo sobre la masa H del pelo
CURL = ["..LL.", ".Lhhh", "LhhhH", ".hhH."]
FRINGE = [".Lh", "Lhh", "hhH", ".h."]
CURLS = [(9, 2, CURL), (14, 2, CURL), (20, 2, CURL),
         (6, 4, CURL), (11, 5, CURL), (17, 4, CURL), (22, 5, CURL),
         (8, 7, FRINGE), (13, 7, FRINGE), (17, 7, FRINGE), (21, 7, FRINGE),
         (5, 9, [".h", "hh", "hH", ".h"]), (24, 9, [".h", "hh", "Hh", "h."]),
         (6, 14, ["h.", "hh"]), (24, 14, [".h", "hh"])]
UPPER = 27   # filas 0..25 respiran (bajan 1 px); piernas fijas


def draw(s, dy=0, blink=False):
    for y, row in enumerate(ROWS):
        if not row:
            continue
        x0, txt = row
        yy = y + (dy if y < UPPER else 0)
        for i, ch in enumerate(txt):
            if ch == ".":
                continue
            if blink and ch in "EW" and y == 13:
                ch = "S"
            if blink and ch in "EW" and y == 14:
                ch = "O"
            s.px(x0 + i, yy, PAL[ch])
    for cx, cy, st in CURLS:
        yy = cy + (dy if cy < UPPER else 0)
        for j, line in enumerate(st):
            for i, ch in enumerate(line):
                if ch != ".":
                    s.px(cx + i, yy + j, PAL[ch], only=PAL["H"])


s = Sprite(32, 32)
for i, (dy, blink) in enumerate([(0, False), (1, False), (0, False), (0, True)]):
    if i:
        s.add_frame(copy=False)
    s.use(frame=i + 1)
    draw(s, dy, blink)
s.set_duration(260, "all")
s.set_duration(120, [4])
s.tag("idle", 1, 4)

if __name__ == "__main__":
    s.preview("sprite_preview.png", scale=10)
    s.save_silhouette("sprite_silhouette.png", frame=1)
    s.stats()
    os.makedirs("out", exist_ok=True)
    s.save_png("out/prota_sprite.png", frame=1)
    s.save_png("out/prota_sprite@6x.png", frame=1, scale=6)
    s.save_gif("out/prota_idle@6x.gif", scale=6, tag="idle")
    s.save_spritesheet("out/prota_idle_sheet.png", layout="row", padding=1)
    # variante para el fondo oscuro del juego (contorno exterior C.edge)
    from PIL import Image
    frames = [rim(s.composite(i + 1)) for i in range(s.n_frames)]
    sheet = Image.new("RGBA", (33 * len(frames) - 1, 32), (0, 0, 0, 0))
    for i, im in enumerate(frames):
        sheet.paste(im, (33 * i, 0))
    sheet.save("out/prota_idle_sheet_oscuro.png")
    frames[0].save("out/prota_sprite_oscuro.png")
    bg = Image.new("RGBA", (32 * 6, 32 * 6), "#141219")
    gif = [Image.alpha_composite(bg, im.resize((192, 192), Image.NEAREST)).convert("P", palette=Image.ADAPTIVE) for im in frames]
    gif[0].save("out/prota_idle_oscuro@6x.gif", save_all=True, append_images=gif[1:],
                duration=[260, 260, 260, 120], loop=0)
