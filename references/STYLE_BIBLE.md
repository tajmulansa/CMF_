# CMF Style Bible (v0.2, research-based, not yet visually validated)

Target: a 55-70 s vertical explainer that feels hand-edited by a person. Built from our own scripts, images and voice.

## The one-paragraph recipe
Plain, legible graphics on warm paper. Graphics step at 12 fps inside a 24 fps edit. Cutouts have rough edges, a white border and a soft shadow. Annotations (highlighter, underline, circle) draw on by hand. Grain goes on last, fine and light. Texture is used on some scenes, not all. Cuts are hard, shot lengths are skewed (many 2-4 s, a few long holds for evidence and charts). Music is minimal, changes 2-3 times, and drops out on the key claim. SFX are few and land a few frames early. Voice about 150 wpm with deliberate pauses after the big ideas.

## Graphics (what Vox staff say)
- After Effects-style builds: masks, shape layers, parenting, templates. These map to Remotion components, SVG paths and clips. No 3D needed to look Vox-like.
- Recurring formats seen in sources: animated maps (hand-drawn lines, arrows, labels over a base map), highlighted text on documents, corner-pinned clips on screens, cutout archival photos, simple charts, kinetic text.
- Per-format build recipes were NOT completed in the research: to be derived from our own reference frames.

## Texture, sound, pacing
See `reports/texture.md`, `reports/sound.md`, `reports/pacing.md` for numbered rules (T1-T19, S1-S12, P1-P10) with Cited/Inference tags.

## Evidence quality (read before trusting a number)
- Vox's own people document process, not textures or metrics. Texture numbers are from third-party tutorials; shot-length stats are from a vendor sample of AI-built long-form videos; loudness and ducking numbers are from third-party guides and partly conflict.
- Treat every number as a starting point. The refinement loop (compare renders to our own reference frames, adjust) is what makes the skill good.

## Open gaps (to fill with our own references)
- Palette, typography and drop-shadow style at Vox: no source found.
- Graphic-format build recipes (maps, charts, lower thirds).
- Procedural recipes verified in headless Chromium (SVG filters, canvas/GLSL, CSS blend reliability, cutout stroke, torn edges).
- Open-source music/SFX tooling, free-library licences, music theory for explainer scoring.
- 9:16 adaptation evidence from Vox and peers; Vox shot-length and cuts-per-minute figures.
