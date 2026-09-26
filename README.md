# multiplayuh — Inercia

Prototipo singleplayer de **Inercia** para validar movimiento, cartas y mapas procedurales antes de pasar a Godot (F0 del plan).

**Jugar:** https://alex-alas.github.io/multiplayuh/ (se despliega solo con cada push a `main`).
También funciona abriendo `index.html` directo en el navegador (desktop o teléfono en horizontal).

- **Pantalla completa**: botón en el menú y en la partida, o `F` en desktop. En Android se entra sola al tocar Jugar. En iPhone (sin Fullscreen API) hay que usar Compartir → Agregar a inicio: el manifest la abre a pantalla completa y en horizontal.

- **Cañón**: cada nivel arranca con el tiempo congelado dentro de un cañón; apuntás y el primer disparo sale gratis y a potencia máxima.
- **Slingshot**: arrastrar y soltar (mitad izquierda en el teléfono, mouse en desktop); toque o Espacio = salto / wall-jump (gratis).
- **Barra de movimiento**: lanzarte cuesta un fijo + un extra según la potencia, y la potencia queda limitada por la barra que te queda. El hover (apuntar en el aire) también gasta barra, cada vez más rápido, hasta un máximo de 2 s.
- **Recarga**: orbes rompibles (una parte), núcleos (completa) y kills, que recargan más cuanto más alto es tu rango de estilo (D → S). El estilo sube con kills, combos, rebotes rápidos, esquivar balas de cerca y variar cartas; decae con el tiempo y con el daño. Cada rango también sube la potencia y la velocidad máxima.
- **Move or die**: ir a menos de 400 px/s llena el medidor de frío; lleno = −1 vida.
- **Objetivo**: romper todos los núcleos chocándolos a ≥ 650 px/s. Desde el nivel 2, un mini-jefe (3 golpes) escuda uno de ellos.
- **Cartas (D-04 / D-07)**: build de 3 de 9 cartas en el menú; fila abajo a la derecha, doble toque = repetir última. Desktop: 1-3 al cursor, Q o clic derecho.
- **Pasivas**: 1 ranura opcional con un trade-off sobre la barra (Tanque grande, Tacaño, Planeador, Adrenalina, Ancla). A futuro se desbloquean con logros; por ahora están todas abiertas.
- **Mapas**: chunks de 16×16 hechos a mano, armados en una grilla 2D por semilla (3×2 en el nivel 1 hasta 4×4).
- **Enemigos**: caminante, volador, torreta y tanque. Se matan chocando a ≥ 650 px/s (tanque y mini-jefe ≥ 1000).
- **Power-ups** (en algunos orbes): turbo, barra congelada y escudo.

Las perillas de calibración están en `CFG`, al inicio del script.

## Look

Impresión riso desregistrada sobre pantalla vieja: tintas hueso, girasol, tomate, teal y cobalto; tipografía pixel (Jersey 10) con IBM Plex Mono. El mundo se dibuja en un buffer de baja resolución (una baldosa = 16 px de arte, `ART`) y pasa por un post-proceso WebGL con aberración cromática que crece con la velocidad, los golpes y el tiempo bala, más glitch al recibir daño, dithering, scanlines y grano. Sin WebGL se dibuja el buffer escalado sin post-proceso.

## Despliegue

`.github/workflows/pages.yml` publica `index.html`, `manifest.webmanifest` e `icon.svg` en GitHub Pages. La primera vez hay que activar Pages en *Settings → Pages → Source: GitHub Actions*.
