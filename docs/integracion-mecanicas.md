# Integración de mecánicas — plan por fases

Resultado de la revisión crítica del gameplay (septiembre 2026) frente a la visión de Inercia. Cada fase es un PR propio, probado en desktop y en teléfono en horizontal antes de pasar a la siguiente.

## Diagnóstico (estado de `main` en 39981bb)

- **Planetas sin peso**: el campo del planeta grande llega solo 178 px más allá de la superficie (`r 72`, `f 250`) y los planetas están a ≥ 2250 px entre sí; a 1300 px/s lo cruzás en ~0,3 s. La órbita al ras va a √(g·r) ≈ 390 px/s, por debajo de `coldSpeed` (400): **orbitar te enfría**.
- **Gancho ≈ Lanzar-me**: los dos pisan la velocidad (`P.vx = ux * 1400` / `1600`) e ignoran la inercia que traés. El gancho llega a 480 px, así que casi nunca alcanza un planeta.
- **Martillazo anulado por los orbes**: `takeOrb` hace `P.vy = min(P.vy * k, −orbLift)`, lo que convierte la caída a 1800 en una subida a −520. Además el martillazo empieza con `P.vx = 0`.
- **Tres monedas desconectadas**: barra, cadenas y cooldowns. Las cartas no cuestan ni dan cadenas, así que se juegan al costado del loop.

## Principios

1. **Pilares**, en orden de desempate: movilidad > decisiones bajo presión > expresividad > velocidad de reacción.
2. **Ninguna mecánica fija tu velocidad**: todas suman, redirigen o convierten la inercia que traés. Única excepción: **Lanzar-me**, la carta de rescate.
3. **Una sola moneda de decisión**: cada carta cuesta 1 ◆ (cadena) y tiene un cooldown mínimo anti-spam de ~1 s. Si acierta, devuelve 1 ◆, **una sola vez por activación** (las ◆ extra salen de los kills u orbes que provoque).

## Fase 1 — Telemetría y línea base

Objetivo: poder comparar economías con datos (hace falta antes de tocar nada).

- Registro por nivel, guardado en `localStorage` y mostrado en la pantalla de victoria o derrota:
  - % del tiempo sobre `coldSpeed`
  - rapidez media y pico
  - cartas por minuto y cartas distintas usadas
  - **cadenas desperdiciadas** (las que se ganan con `P.chain` ya en `chainMax`)
  - reparto de ◆: lanzamientos contra cartas
  - tiempo del nivel, golpes recibidos y causa de muerte
  - nota subjetiva de 1 a 5 al terminar
- **Métrica principal**: % sobre `coldSpeed` × cartas distintas usadas.
- **Métrica de control**: cadenas desperdiciadas. Por encima del ~20 %, la economía está mal calibrada.
- Protocolo: al menos 5 niveles por modo, con las mismas semillas.

## Fase 2 — Economía de ◆ en las cartas

- Interruptor en *Ajustes*: **Economía: cooldown / cadenas**, para el A/B de la fase 1.
- Modo cadenas: las cartas cuestan 1 ◆ y tienen un cooldown mínimo de ~1 s.
- Criterio de acierto (+1 ◆):

| Carta | Acierto |
|---|---|
| Martillazo | Detona en el aire sobre algo, o explota en el suelo (siempre) |
| Gancho | Te soltás a ≥ `killSpeed`, o matás al enemigo enganchado |
| Ricochet | El rebote potenciado sale a ≥ `killSpeed` |
| Escopeta | Mata o marca a ≥ 1 enemigo |
| Uppercut | Atrapa a ≥ 1 enemigo |
| Contraataque | Parry exitoso |
| Estela | Mata a ≥ 1 enemigo durante su duración |
| Tiempo bala | Nunca (utilidad pura) |
| Lanzar-me | Nunca (consume todas las ◆) |

- **Lanzar-me**: funciona con 0 ◆ y 0 de barra, pero **consume todas las ◆**; cooldown de 8 s. Es la única carta que sigue fijando la velocidad.

## Fase 3 — Planetas como honda gravitatoria

- **Campo** = 4,5 × r (grande: ~324; chico: ~190).
- **g** calibrada para que la órbita al ras vaya a ~550 px/s, por encima de `coldSpeed`. Para el grande, g ≈ 4200 en la superficie.
- **Honda**: salir del campo tras recorrer ≥ 120° de arco alrededor del centro da +15 % de rapidez, estilo y +1 ◆.
- **Posarse**: pausa el frío, pero ya no lo descarga (el planeta deja de ser zona de descanso).
- **`planetGap`**: de 2250 a ~1200 px entre superficies, para que el hueco entre campos (~700 px) quede a un lanzamiento o a un gancho.
- **Núcleos en órbita**: algunos núcleos orbitan planetas. Romperlos a ≥ 650 exige ir contra su órbita o usar la honda.
- *Segunda iteración, condicionada a que la telemetría muestre uso de la honda*: enemigo **"Luna"**, que orbita y escuda lo que hay en la superficie.

## Fase 4 — Cartas de "mantener" (`hold: 1`)

Nuevo tipo de carta con fase activa y liberación. En desktop se mantiene la tecla 1–3 o Q; en el teléfono, el dedo sobre la carta. El doble toque para repetir sigue igual para las cartas de toque.

### Martillazo

- **Al activarlo**: empujón de ~900 en la dirección de la gravedad local. Se conserva el 70 % de la velocidad tangencial.
- **Aceleración**: 3 × el vector de gravedad total en ese punto (global + planetas, con la global atenuada dentro de un campo). Si la caída entra en el campo de un planeta, se curva hacia él: no siempre es "hacia abajo".
- **Mientras se mantiene**: atraviesa orbes y enemigos **sin cobrar nada** (la recompensa llega al final). Es invulnerable al contacto, **pero no a las balas**.
- **Al tocar un planeta** (manteniendo o no): detona y rebota. El planeta cuenta como objeto.
- **Al soltar en el aire**: sigue cayendo hasta el primer objeto (orbe, enemigo, núcleo, planeta), detona y rebota en sentido opuesto a la gravedad local a 0,8 × la rapidez del impacto, con un mínimo que asegure salir del campo de un planeta chico. Da +1 ◆ si mata o rompe algo.
- **Al tocar el suelo sólido**: gran explosión, con radio que escala con la caída, **sin impulso**: hay que volver a arrancar desde el suelo. **Siempre da +1 ◆.**
- Cuesta 1 ◆.

### Gancho (péndulo)

- Mantener: la cuerda se engancha al primer planeta, enemigo u orbe en la dirección apuntada (alcance ~700 px).
- Girás alrededor del punto **conservando la rapidez**. La cuerda se recoge sola, acorta el radio y **te acelera** (conservación del momento angular).
- Soltar: salís por la tangente. Combina con la honda de la fase 3.
- Enganchado a un enemigo: lo aturde. Si soltás a ≥ `killSpeed` en su dirección, lo matás.
- Cuesta 1 ◆.

## Fase 5 — Resto de las cartas

- **Ricochet**: sin timer. Queda activo hasta la próxima superficie sólida (planeta, pared, techo o **suelo**; en el suelo hostil también rebota ×1,3). Si estás posado, falla (`return false`) y no gasta la ◆.
- **Escopeta** (reemplaza a Spray): cono de ~70°, alcance 450, ralentiza y marca, con **retroceso** de +700 opuesto a donde apuntás. Sin sistema de supers por ahora. Queda anotado como posible sumidero de ◆ ("activar con 3 ◆ = versión super") si la telemetría muestra que sobran cadenas.
- **Uppercut**:
  1. Atracción: 0,25 s, radio de 240 px.
  2. Elevación: 0,35 s, los enemigos quedan aturdidos y el jugador **suma** −600 a `vy` (ya no lo fija).
  3. Explosión: `strike()` a todos los atrapados. Tanques y mini-jefe sí se atrapan: el tanque muere y el jefe pierde 1 de vida.
  - Si no atrapa a nadie, no mata ni da recompensa.
- **Contraataque**: ventana de **0,35 s**. **Elimina al enemigo** (`strike()`: el tanque muere y el jefe pierde 1 de vida). Cuesta 1 ◆ y da +1 ◆ si acierta. Cooldown condicional: **0,5 s si acierta** (permite encadenar parries contra la ráfaga de 3 balas) y **10 s si falla**.
  - Contra una bala, el parry la **devuelve** a ×2 de velocidad hacia el que disparó y lo mata si le pega.
- **Estela** y **Tiempo bala**: sin cambios.
