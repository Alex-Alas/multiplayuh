# multiplayuh — Inercia

Prototipo singleplayer de **Inercia** para validar movimiento, cartas y mapas procedurales antes de pasar a Godot (F0 del plan).

**Jugar:** https://alex-alas.github.io/multiplayuh/ (se despliega solo con cada push a `main`).
También funciona abriendo `index.html` directo en el navegador (desktop o teléfono en horizontal).

- **Pantalla completa**: botón en el menú y en la partida, o `F` en desktop. En Android se entra sola al tocar Jugar. En iPhone (sin Fullscreen API) hay que usar Compartir → Agregar a inicio: el manifest la abre a pantalla completa y en horizontal.

- **Cañón**: cada nivel arranca dentro de un cañón; apuntás y el primer disparo sale gratis y a potencia máxima. Mientras estás adentro sos invisible e invencible.
- **Cadenas**: cada orbe, kill o núcleo te da una cadena (hasta 3): el próximo lanzamiento es gratis y el hover no gasta barra. La idea es encadenar lanzamientos rompiendo cosas, no caminar como en un plataformero.
- **Orbes**: el eslabón del movimiento. Aparecen en cúmulos aleatorios por chunk (a veces pegados, a veces lejos, con zonas vacías). Al tocarlos frenan un poco a toda velocidad y mucho si vas lento, y entonces también te desvían.
- **Planetas**: en el aire no hay paredes ni plataformas, solo planetas con un campo gravitatorio (el anillo punteado) que curva tu trayectoria, las balas y los orbes que los orbitan. Llegando lento te posás y te relanzás desde ahí.
- **Zonas seguras**: posado en un planeta o sobre una baldosa teal del suelo no te enfriás; las baldosas además recargan barra hasta el 60 %.
- **Slingshot**: arrastrar y soltar (mitad izquierda en el teléfono, o derecha si invertís los lados en Ajustes; mouse en desktop); toque o Espacio = salto (gratis).
- **Barra de movimiento**: lanzarte cuesta un fijo + un extra según la potencia, y la potencia queda limitada por la barra que te queda. El hover (apuntar en el aire) también gasta barra, cada vez más rápido, hasta un máximo de 2 s.
- **Recarga**: orbes (poco), núcleos (completa) y kills, que recargan más cuanto más alto es tu rango de estilo (D → S). El estilo sube con kills, combos, rebotes rápidos, esquivar balas de cerca y variar cartas; decae con el tiempo y con el daño. Cada rango también sube la potencia y la velocidad máxima.
- **Move or die**: ir a menos de 400 px/s fuera de una zona segura llena el medidor de frío; lleno = −1 vida.
- **Objetivo**: romper todos los núcleos chocándolos a ≥ 650 px/s. Desde el nivel 2, un mini-jefe (3 golpes) escuda uno de ellos.
- **Cartas (D-04 / D-07)**: build de 3 de 9 cartas en el menú; fila abajo a la derecha (o a la izquierda con los lados invertidos), doble toque = repetir última. Desktop: 1-3 al cursor, Q o clic derecho.
- **Pasivas**: 1 ranura opcional con un trade-off sobre la barra (Tanque grande, Tacaño, Planeador, Adrenalina, Ancla). A futuro se desbloquean con logros; por ahora están todas abiertas.
- **Mapas**: chunks de 16×16 hechos a mano, armados en una grilla 2D por semilla, más anchos que altos: 16×8 chunks en el nivel 1, +2 columnas y +1 fila por nivel hasta 24×12. Lo sólido solo existe en el suelo; arriba hay planetas separados por al menos 2 lanzamientos a tope (2250 px) y cúmulos de orbes. Núcleos: 3 + nivel (tope 8), a 1500 px entre sí.
- **Enemigos**: caminante, volador, torreta y tanque; caminantes, torretas y tanques también viven sobre los planetas. Se matan chocando a ≥ 650 px/s (tanque y mini-jefe ≥ 1000).
- **Power-ups** (en algunos orbes): turbo, barra congelada y escudo.

Las perillas de calibración están en `CFG`, al inicio del script.

## Look

Impresión riso desregistrada: tintas hueso, girasol, tomate, teal y cobalto; tipografía Jersey 10 con IBM Plex Mono. El mundo se dibuja nítido a resolución de pantalla (sin pixel art, para que se lea bien a alta velocidad) y pasa por un post-proceso WebGL con aberración cromática que crece con la velocidad, los golpes y el tiempo bala, glitch al recibir daño y un filtro retro (scanlines, viñeta y grano). La aberración y el filtro retro se apagan en *Ajustes*. No hay desenfoque de movimiento. Sin WebGL se dibuja el buffer sin post-proceso.

## Audio

Música: *The Perfect Lap* (`musica.mp3`), en loop. Pasa por un pasabajos que la apaga en el menú y el cañón, la abre al jugar y la estira como cinta con tiempo bala. Los efectos (lanzamiento, cañón, salto, orbe, kill, núcleo, daño, rebote, cartas, victoria, derrota) se sintetizan con WebAudio, sin archivos: los orbes seguidos suben un semitono cada uno. Música y efectos se apagan por separado en *Ajustes*. Abierto como archivo (`file://`) la música suena sin filtro.

## Despliegue

`.github/workflows/pages.yml` publica `index.html`, `manifest.webmanifest`, `icon.svg` y `musica.mp3` en GitHub Pages. La primera vez hay que activar Pages en *Settings → Pages → Source: GitHub Actions*.
