"""Paleta compartida sprite/portrait (rampas con hue-shift, luz arriba-izquierda)."""
PAL = {
    "O": "#150f1c",  # contorno ciruela oscuro
    "H": "#1d1927", "h": "#2c2739", "L": "#4b4562",  # pelo negro con brillo lavanda
    "B": "#1d1927",  # cejas
    "s": "#a86650", "S": "#d4966f", "K": "#edb993",  # piel
    "E": "#24130e", "I": "#6b3a26", "W": "#efe2d8", "g": "#fff6ee",  # ojos (pupila, iris, blanco, brillo)
    "M": "#bf6e60", "m": "#8a4640",  # labios
    "t": "#1f1e24", "T": "#2e2c33", "U": "#4a4750",  # camiseta negra
    "X": "#e8452b",  # cruz
    "J": "#3f5a86", "j": "#2b3e62",  # jeans
    "F": "#efe8dc", "f": "#b2a898",  # tenis
}

EDGE = "#5d5667"  # C.edge del juego: contorno exterior para fondos oscuros


def rim(im, color=EDGE):
    """Copia de la imagen con el contorno exterior (píxeles opacos que tocan
    transparencia) recoloreado — se lee sobre el fondo night del juego."""
    from PIL import ImageColor
    c = ImageColor.getrgb(color) + (255,)
    out = im.copy(); px = im.load(); o = out.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and any(not (0 <= x + dx < w and 0 <= y + dy < h) or px[x + dx, y + dy][3] == 0
                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                o[x, y] = c
    return out
