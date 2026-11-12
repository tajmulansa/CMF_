# Texture report (Vox-style tactile look)

Evidence: NO Vox staff source describes grain, paper or boil. Every number below comes from third-party tutorials (mainly PremiumBeat's "replicating the Vox look") or general handmade-look guides, or is marked Inference. Full citations: `reports/Vox explainer visuals textures music.md`.

Core idea: the look is plain, legible graphics plus a few cheap imperfection cues, used with restraint. Uniform texture on everything is the tell of automation.

## Rules (C = cited from a tutorial/doc, I = inference)

| # | Rule | Tag |
|---|------|-----|
| T1 | Drive all motion from `useCurrentFrame()` + `interpolate()`. Never CSS transition/keyframes or setTimeout (they do not render deterministically). | C (Remotion docs) |
| T2 | All randomness via `random("seed")` or `@remotion/noise`. Never `Math.random()`. Per-element seeds: `random("x-" + i)`. | C (Remotion docs) |
| T3 | Graphics layer steps at 12 fps inside a 24 fps edit (the stutter adds character). | C (PremiumBeat) |
| T4 | Compose at 24 fps so stepped looks are whole-frame holds: hold 2 = 12 fps, hold 3 = 8 fps, hold 4 = 6 fps. (At 30 fps: hold 3 = 10 fps, hold 5 = 6 fps.) 55-70 s = 1,320-1,680 frames at 24 fps. Confirm the target platform accepts 24 fps. | I |
| T5 | Boil/wobble seed refresh 4-12 fps. Default 12; go slower (8, 6, 4) for a visible boil. | C |
| T6 | Cutouts and lower thirds keep rough, jagged alpha edges. Reveal with a mask that grows unevenly and skips frames; reveal text a few frames later. | C (PremiumBeat) |
| T7 | Roughen edges with Remotion `roughenEdges` defaults (amount 1, border 26.5, scale 0.07) and re-seed on each held drawing. Do NOT copy After Effects Roughen Edges numbers. | C (defaults) / I (use) |
| T8 | Motion background: 5-6 distressed textures, 2-3 visible per second, ~10 s loop, behind static content. With one texture only: flip/rotate it for variety. | C |
| T9 | Paper colour is warm off-white or cream, never pure white. Paper layer on Multiply (Overlay/Hard Light as alternatives). Reduce ink contrast slightly. | C |
| T10 | Grain is the LAST texture step: fine grain at about 15-20% opacity. Linear Light blend is preferred over Overlay for mid-grey grain. | C |
| T11 | Fight banding with 1-5% grain/noise. Avoid pure solid backgrounds. | C |
| T12 | Restraint: texture a subset of scenes (a vendor suggests about half of end-tag animations), match light direction, never add texture just because you can. | C |
| T13 | Shadows under cutouts: soft blurred duplicate; animate scale and shadow distance together for a paper-lift feel. Precompute shadow images if CPU rendering is slow (CSS blur/drop-shadow/box-shadow are slow without a GPU). | C |
| T14 | Print-style colour layers: misregistration 0.5-2 px, overprint = multiply. | C |
| T15 | Lens look: subtle, slightly rotated chromatic aberration; edge-only blur (AE Gaussian blur 3.5, mask feather about 50, inverted circular mask). | C (PremiumBeat) |
| T16 | Compositing order: flat art -> roughen/offset -> stepped seed -> paper (Multiply) -> precomputed shadow -> lens -> grain LAST. | I |
| T17 | Remotion native effects package: pin identical `remotion` and `@remotion/effects` versions (docs: paper 4.0.486+, roughenEdges 4.0.487+, lightLeak 4.0.500+). Effects do not animate themselves. Smoke-test one still per machine first. `--gl=angle` with a GPU, `swangle` without (slow). | C (versions, flags) / I (smoke test) |
| T18 | Highlighter/underline draw-on 0.3-0.6 s, ease-in-out (not linear), classic yellow, slight roughen. | C (vendor) |
| T19 | Slow push-in/drift on stills at 1-5% scale with randomised direction and speed; vary animation durations 0.25-0.6 s. | I |

## Texture vocabulary to build (priority order)
1. Paper under everything (cream, Multiply) + last-step grain.
2. Rough-edged cutouts with white border and soft shadow, on held (stepped) drawings.
3. Highlighter / underline / circle draw-on annotations on documents.
4. Cycled distressed texture background (5-6 variants).
5. Subtle lens (chromatic aberration + edge blur) on selected scenes only.
6. Optional: halftone and riso misregistration on photos, light leak at section changes.

## Engineering first tasks (not yet done)
- Render one still each of `paper()`, `roughenEdges()`, `halftone()` on the real target machine under each `--gl` mode (nothing was run headless in this research).
- Build and smoke-test the dependency-light fallback: seeded SVG `feTurbulence` grain/paper, `feDisplacementMap` rough edges, `@remotion/paths` `evolvePath` draw-ons.
- Code recipes (composed from cited APIs, NOT run): see the "Short code recipes" section of the full report.
