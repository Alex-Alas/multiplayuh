# multiplayuh — Inercia

Prototipo singleplayer de **Inercia** para validar movimiento, cartas y mapas procedurales antes de pasar a Godot (F0 del plan).

**Jugar:** https://alex-alas.github.io/multiplayuh/ (se despliega solo con cada push a `main`).
También funciona abriendo `index.html` directo en el navegador (desktop o teléfono en horizontal).

- **Pantalla completa**: botón en el menú y en la partida, o `F` en desktop. En Android se entra sola al tocar Jugar. En iPhone (sin Fullscreen API) hay que usar Compartir → Agregar a inicio: el manifest la abre a pantalla completa y en horizontal.

- **Slingshot**: arrastrar y soltar (mitad izquierda en el teléfono, mouse en desktop); toque o Espacio = salto / wall-jump.
- **Hover (D-03)**: apuntar en el aire te frena y la gravedad vuelve en 1.5 s; 1 por salida del suelo.
- **Cartas (D-04 / D-07)**: build de 3 de 9 cartas en el menú; fila abajo a la derecha, doble toque = repetir última. Desktop: 1-3 al cursor, Q o clic derecho.
- **Mapas**: chunks hechos a mano, encadenados por semilla; la dificultad sube por nivel.
- **Enemigos**: caminante, volador, torreta y tanque. Se matan chocando a ≥ 650 px/s (tanque ≥ 1000).
- **Power-ups**: turbo, lanzamientos infinitos y escudo.

Las perillas de calibración están en `CFG`, al inicio del script.

## Look

Impresión riso desregistrada sobre pantalla vieja: tintas hueso, girasol, tomate, teal y cobalto; tipografía pixel (Jersey 10) con IBM Plex Mono. El mundo se dibuja en un buffer de baja resolución (una baldosa = 16 px de arte, `ART`) y pasa por un post-proceso WebGL con aberración cromática que crece con la velocidad, los golpes y el tiempo bala, más glitch al recibir daño, dithering, scanlines y grano. Sin WebGL se dibuja el buffer escalado sin post-proceso.

## Despliegue

`.github/workflows/pages.yml` publica `index.html`, `manifest.webmanifest` e `icon.svg` en GitHub Pages. La primera vez hay que activar Pages en *Settings → Pages → Source: GitHub Actions*.
