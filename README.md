# multiplayuh — Inercia

Prototipo singleplayer de **Inercia** para validar movimiento, cartas y mapas procedurales antes de pasar a Godot (F0 del plan).

Es un solo archivo sin dependencias: abrí `index.html` en el navegador (desktop o teléfono en horizontal).

- **Slingshot**: arrastrar y soltar (mitad izquierda en el teléfono, mouse en desktop); toque o Espacio = salto / wall-jump.
- **Hover (D-03)**: apuntar en el aire te frena y la gravedad vuelve en 1.5 s; 1 por salida del suelo.
- **Cartas (D-04 / D-07)**: build de 3 de 9 cartas en el menú; fila abajo a la derecha, doble toque = repetir última. Desktop: 1-3 al cursor, Q o clic derecho.
- **Mapas**: chunks hechos a mano, encadenados por semilla; la dificultad sube por nivel.
- **Enemigos**: caminante, volador, torreta y tanque. Se matan chocando a ≥ 650 px/s (tanque ≥ 1000).
- **Power-ups**: turbo, lanzamientos infinitos y escudo.

Las perillas de calibración están en `CFG`, al inicio del script.
