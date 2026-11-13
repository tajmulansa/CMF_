# test-clip-01 (5 s, 1080x1920, 24 fps)

Original test clip made from our own rules (not a Vox copy). Placeholder topic: honey found in ancient Egyptian tombs, "3,000+ years old", "older than the Roman Empire". NOT fact-checked for publishing.

Render: `python3 -I make_clip.py <outdir>` (needs numpy, scipy, opencv, Pillow, ffmpeg). Stills only: add `--stills 8,30,56`.
Self-check: `python3 -I ../../templates/scripts/analyze_clip.py <mp4> test-clip-01 <repo>`.
The mp4 is not committed (large, ignored by .gitignore); re-render it.

## Timeline (24 fps)
| Frames | What |
| ------ | ---- |
| 0-5 (0.25 s) | Flat dark grey #1d1d1d with dust specks, watermark fades in (O1, O2) |
| 6-53 (2.0 s) | Shot 1: kraft backing paper + honey-jar cutout (rough white border, soft shadow), caption from f10, highlighter on f22-30 |
| 54-57 (0.167 s) | Dark-grey dip, watermark stays (O1) |
| 58-119 (2.58 s) | Shot 2: "3,000+" circled by hand-drawn marker, "YEARS OLD" underlined, caption from f64 (lags the cut by about 0.25 s, O3), highlighter f92-100 |

## Rules applied
T3/T5 graphics boil refreshed at 12 fps, T4 24 fps, T6/T7 edge-only roughening, T8 three paper variants cycled every 10 frames, T9 warm cream paper, T10 grain last, T12 lens on shot 2 only, T13 soft shadow, T14 ~2 px misregistration on the stat, T15 chromatic aberration + edge blur, T16 compositing order, T18 highlighter 0.33 s ease-in-out, P7 content inside the safe core. Audio: two music sections with a drop at the dip (S2/S3), SFX landing 1-3 frames early (S9), 5 SFX (S8), loudnorm to -14 LUFS (S4).

## Known weaknesses (to refine)
- No voice-over (no speech tool here). Captions only.
- Audio was synthesised and checked by measurement only, not listened to. Measured -12.6 LUFS / -6.5 dBFS peak (a 5 s clip makes loudnorm imprecise), target -14.
- Typography is DejaVu (placeholder). Jar is a simple vector drawing. Shot 2 is text only (no cutout).
- Rendered in Python, not Remotion (not installed here). Port to Remotion components later.
- Rules are from research plus a 5 s Vox sample; nothing here is validated against a full Vox video.
