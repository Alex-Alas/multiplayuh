#!/usr/bin/env python3
"""Prota — portrait 64x64 (busto) para cuadros de diálogo.

Capas: back (mullet) · body (camiseta/cuello) · face · hair. Luz arriba-izquierda.
Los rizos usan la receta shifted-shape: H completo → h desplazado → L desplazado,
recortados a la capa del pelo con only="opaque".
"""
import os, sys
sys.path.insert(0, os.path.join(os.environ.get("PIXEL_ART_STUDIO", "../../../pixel-art-studio"), "scripts"))
from pixelstudio import Sprite
from paleta import PAL, rim

P = PAL
s = Sprite(64, 64)


def stamp(x0, y0, rows, only=None):
    for j, line in enumerate(rows):
        for i, ch in enumerate(line):
            if ch != ".":
                s.px(x0 + i, y0 + j, P[ch], only=only)


# trazos de rizo (L arriba = luz arriba-izquierda); '.' deja la masa H
CURLS = [
    [".Lh.", "L..h", "h...", ".hh."],     # C abierta a la derecha
    [".Lh.", "h..h", "...h", ".hh."],     # C abierta a la izquierda
    ["LLh..", "...hh", "....h"],          # ola
]
TIP = ["Lh", "hh", ".h", "h."]             # punta de mechón que cuelga


def curls(cells, only="opaque"):
    for i, (x, y) in enumerate(cells):
        stamp(x, y, CURLS[(i * 7 + y) % 3], only=only)


# --- mullet detrás del cuello y las orejas --------------------------------
s.layer("back")
s.polygon([(11, 22), (21, 26), (23, 50), (18, 53), (12, 49), (10, 36)], P["H"])
s.polygon([(53, 22), (43, 26), (41, 50), (46, 53), (52, 49), (54, 36)], P["H"])
curls([(12, 38), (16, 45), (46, 38), (44, 45), (11, 30), (49, 30)])

# --- cuello + camiseta ----------------------------------------------------
s.layer("body")
s.rect(25, 40, 39, 55, P["S"])
s.polygon([(33, 40), (39, 40), (39, 55), (30, 55)], P["s"], only="opaque")
s.rect(25, 46, 39, 48, P["s"])                      # sombra bajo la barbilla
s.polygon([(2, 63), (6, 56), (16, 52), (25, 51), (39, 51), (48, 52), (58, 56), (62, 63)], P["T"])
s.polygon([(40, 51), (48, 52), (58, 56), (62, 63), (44, 63)], P["t"], only="opaque")
s.polygon([(4, 60), (7, 55), (17, 52), (21, 52), (10, 57)], P["U"], only="opaque")
s.ellipse(23, 51, 41, 58, P["U"], only="opaque")    # cuello redondo
s.ellipse(25, 49, 39, 55, P["s"], only="opaque")
stamp(31, 58, [".X.", "XXX", ".X.", ".X.", ".X."])  # cruz

# --- cara + orejas ----------------------------------------------------------
s.layer("face")
s.ellipse(14, 27, 20, 40, P["S"]); s.ellipse(44, 27, 50, 40, P["s"])
stamp(15, 30, ["sss", "s..", "s..", ".ss"]); stamp(46, 30, ["mmm", "..m", "..m", "mm."])
s.polygon([(18, 20), (46, 20), (46, 35), (43, 43), (37, 48), (27, 48), (21, 43), (18, 35)], P["S"])
# sombra lateral derecha y bajo el flequillo; luz en mejilla izquierda
s.polygon([(41, 22), (46, 22), (46, 35), (43, 43), (37, 48), (34, 48), (40, 42), (42, 34)], P["s"], only="opaque")
s.rect(18, 20, 46, 25, P["s"], only=P["S"])
s.line(21, 35, 24, 35, P["K"], only=P["S"]); s.line(20, 36, 22, 36, P["K"], only=P["S"])
s.line(31, 32, 31, 35, P["K"], only=P["S"])         # puente de la nariz

# cejas gruesas y rectas
stamp(20, 26, [".BBBBBBB", "BBBBBBB."])
stamp(37, 26, ["BBBBBBB.", ".BBBBBBB"])
# ojos (párpado pesado)
EYE = [".OOOOO", "OWIEgW", ".sIIs."]
stamp(22, 29, EYE)
stamp(37, 29, EYE)
# nariz
stamp(29, 33, ["...K.s", "...K.s", "....ss", ".s...ss", "..sss."])
# boca (labios un poco fruncidos)
stamp(28, 41, [".mmmmmmm.", "..MMMMM..", "...sss..."])

# --- pelo -------------------------------------------------------------------
s.layer("hair")
s.ellipse(10, 3, 54, 23, P["H"])
for cx, cy, r in ((17, 8, 5), (26, 5, 5), (36, 5, 5), (45, 7, 5), (51, 12, 4), (13, 13, 4)):
    s.circle(cx, cy, r, P["H"], fill=True)
s.ellipse(9, 10, 21, 27, P["H"]); s.ellipse(43, 10, 55, 27, P["H"])
# flequillo: mechones hasta las cejas, con huecos de frente
for pts in ([(18, 20), (25, 20), (20, 25)], [(23, 20), (30, 20), (27, 24)],
            [(30, 20), (36, 20), (33, 23)], [(35, 20), (42, 20), (40, 24)], [(41, 20), (47, 20), (46, 25)]):
    s.polygon(pts, P["H"])
curls([(14, 6), (22, 4), (31, 3), (40, 4), (47, 8),
       (11, 12), (18, 10), (26, 9), (34, 9), (42, 11), (50, 14),
       (13, 18), (21, 15), (30, 14), (38, 15), (46, 18), (52, 20),
       (10, 23), (49, 24)])
s.polygon([(22, 21), (27, 21), (24, 27)], P["H"])      # mechón suelto sobre la frente
s.polygon([(38, 21), (42, 21), (41, 25)], P["H"])
for x, y in ((19, 19), (26, 18), (33, 18), (38, 19), (44, 19)):
    stamp(x, y, TIP, only="opaque")
stamp(23, 22, TIP, only="opaque")

s.flatten()
s.outline(P["O"], where="outside")

if __name__ == "__main__":
    s.preview("portrait_preview.png", scale=8)
    s.save_silhouette("portrait_silhouette.png")
    s.stats()
    os.makedirs("out", exist_ok=True)
    s.save_png("out/prota_portrait.png")
    s.save_png("out/prota_portrait@4x.png", scale=4)
    rim(s.composite(1)).save("out/prota_portrait_oscuro.png")
    # maqueta de cuadro de diálogo con la paleta riso del juego (C)
    from PIL import Image, ImageDraw
    k = 4
    box = Image.new("RGBA", (220 * k, 76 * k), "#141219")
    d = ImageDraw.Draw(box)
    d.rectangle([2 * k, 2 * k, 218 * k - 1, 74 * k - 1], outline="#f3e9d2", width=k)
    d.rectangle([6 * k, 6 * k, 70 * k - 1, 70 * k - 1], fill="#22c4b0")
    face = s.composite(1).resize((64 * k, 64 * k), Image.NEAREST)
    box.alpha_composite(face, (6 * k, 6 * k))
    d.rectangle([6 * k, 6 * k, 70 * k - 1, 70 * k - 1], outline="#0f0e13", width=k)
    for i, w in enumerate((120, 96, 132)):           # líneas de texto de relleno
        d.rectangle([80 * k, (16 + i * 14) * k, (80 + w) * k, (19 + i * 14) * k], fill="#f3e9d2")
    box.save("out/maqueta_dialogo.png")
