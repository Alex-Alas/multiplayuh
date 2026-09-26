# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**Inercia** — a singleplayer browser prototype (phase F0 of a larger plan) used to validate movement, cards and procedural maps before porting to Godot. The whole game lives in one file, `index.html` (inline CSS + one `'use strict'` script, vanilla JS, Canvas 2D + WebGL). No build step, no dependencies, no package manager, no tests, no linter. Code comments, UI strings and the README are in Spanish; keep new ones in Spanish.

Design-decision IDs like `D-03`, `D-04`, `D-07` and phases like `F3` refer to the external plan document (not in this repo); keep those references when touching related code.

## Running and deploying

- Run: open `index.html` directly in a browser, or serve the folder (e.g. `python3 -m http.server`) — test on desktop and on a phone in landscape.
- Debug: chunk shape is validated at load with `console.assert` ("chunk mal formado") — check the console after editing maps.
- Deploy: every push to `main` runs `.github/workflows/pages.yml`, which copies **only** `index.html`, `manifest.webmanifest` and `icon.svg` to GitHub Pages (https://alex-alas.github.io/multiplayuh/). Any new asset file must be added to the `cp` line in that workflow.

## Architecture of `index.html` (sections marked `// ---------- ... ----------`)

- **`CFG`** at the top of the script: all calibration knobs (gravity, launch power, charges, hover fade, kill speeds, etc.). Tune gameplay here rather than hardcoding values.
- **Chunks / map generation**: levels are hand-made 16×16 ASCII chunks (`START`, `MID[]`, `CH` = 16). Legend is in the comment above them (`#` solid, `B` bouncy, `^` spikes, `?` random enemy, `W/F/S/T` enemies, `o` orb, `*` orb that may carry a power-up, `N` possible core spot, `@` cannon start). Invariant (asserted): every chunk is 16×16, `START` has `@`, every `MID` chunk has exactly one `N`. `genLevel(seed, lvl)` lays chunks in a 2D grid that grows with the level (3×2 → 4×4), `START` somewhere on the bottom row, wrapped in a 1-tile solid border (`G.W`/`G.H` include it; `tileAt` treats out-of-bounds as solid). Entity chars are moved into `L.enemies` / `L.orbs`; `N` spots are shuffled and `min(6, 2 + lvl)` become `L.cores`. From level 2 a mini-boss (elite flyer, `boss: true`, `hp: 3`) guards and shields the first core. There is intentionally no reachability validator (see the `ponytail:` comment).
- **Movement bar**: the main resource. `launchVec` computes cost (`launchBase + launchPow × power`, scaled by passive mods) and clamps power to the remaining bar; while `G.cannon` is true the first launch is free and full power and `update` doesn't run. Hover drains bar over time up to `hoverMax`. Refills: orbs, cores, kills (fraction by style rank, `CFG.rankRefill`). Style (`G.style`, 100 per rank D–S) also boosts launch power and max speed (`boost()`). "Move or die": `P.cold` fills below `coldSpeed`; full = hurt. Levels end when every core is destroyed (`win()`).
- **Passives (`PASSIVES`)**: one optional slot (`inercia.passive`). Each is a partial override of `MODS`; `world()` merges them into the global `M`, and gameplay code reads multipliers from `M` rather than checking passive ids.
- **Cards (`CARDS`)**: card definition is kept separate from how cards are acquired (D-07). Each card has `n`, `d`, `cd`, optional `aim: 1` (receives a unit direction `ux, uy`), and `cast()`; returning `false` from `cast` means it failed and shouldn't go on cooldown. The player's 3-card build is persisted in `localStorage` (`inercia.build`, also `inercia.inv`) via the `load`/`save` helpers.
- **State**: globals `state` (`'menu'`/`'play'`/…), `G` (world: grid, enemies, shots, fx, splats, time-slow, shake…) and `P` (player). `world()` creates both; `startLevel()` also resets the hand, camera and input.
- **Physics**: tile-based circle-vs-grid collision. `move(e, dt, grav, onHit)` substeps by speed (≤6 px per step) and resolves X then Y via `hit()`; `onHit` callbacks (`playerHit`, `walkHit`, `flyHit`) handle bounces/ricochet. `tileAt` treats out-of-bounds horizontally as solid, vertically as empty.
- **Update**: fixed 60 Hz step (`STEP`) driven by an accumulator in `frame()`; "tiempo bala" (`G.slow`) scales the accumulator, not `dt`. Kill rule: colliding at ≥ `killSpeed` (tank and boss ≥ `tankSpeed`), or with parry/shield/stunned/marked enemies; otherwise the player takes damage. Lethal hits go through `strike(e)`, which removes 1 hp from multi-hp enemies (bosses) and only calls `kill(e)` on the last one.
- **Input**: Pointer Events for touch and mouse plus keyboard; slingshot on drag (left half on phone), hover while aiming in the air, cards 1–3/Q/right-click on desktop.
- **Render**: the world is drawn to a low-res offscreen buffer (`buf`, `ART` = world units per art pixel, so one tile = 16 art px at any screen size), then a WebGL post-process (`VS`/`FS` shaders, `post()`) adds chromatic aberration scaled by speed/hits/time-slow, damage glitch, dithering, scanlines and grain. Without WebGL the buffer is drawn scaled with no post-process. HUD is drawn separately at full resolution (`hud()`), respecting `SAFE` insets.
- **Look**: fixed "riso" ink palette in `C` (bone, sunflower, tomato, teal, cobalt on night) with Jersey 10 + IBM Plex Mono fonts; reuse `C` colors rather than introducing new ones.
- **Menu / fullscreen**: menu renders over a demo map (`G.demo`) that the camera pans across. The camera is clamped to the map bounds. Fullscreen via the Fullscreen API (auto on Android when tapping Play, `F` on desktop); iOS has no Fullscreen API, so it relies on `manifest.webmanifest` (fullscreen + landscape) via "Add to Home Screen".
