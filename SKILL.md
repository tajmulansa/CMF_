---
name: cmf-explainer-short
description: Make a CuriousMindsFeed vertical explainer short (55-70 s) in a Vox-style editorial look - tight narration, motion graphics, maps, typography, archive-style imagery, designed sound - rendered with Remotion. Use when the user asks for a CMF video, an explainer short, or says "use the CMF skill".
---

# CMF explainer short (Remotion)

Goal: videos that feel hand-edited by a person, not generated. The target is the pacing, structure and polish of Vox-style explainers, built from our own scripts, visuals and voice.

## Status
Version 0.2 - research-trained (rules from web research, not yet validated against our own reference frames). `templates/` is copied from the open-source (MIT) `mromidev/claude-animated-shorts` skill and still contains its 3D cartoon pipeline. It is the engine to learn from and rewrite, not the final look. See `NOTICE`.

## Ground rules
- References are STUDY MATERIAL. Learn pacing, structure, shot rhythm and sound design. Never copy scripts, footage, graphics or voice. Story, visuals and voice are always our own.
- Never name the reference channel in a voice-over, title or description.
- Keep this repo private while it holds reference frames, audio or transcripts.
- Save after every step. Commit often.

## How the references work
Reference material lives in `references/`, split by type. Use the same `<video-slug>` everywhere.
- `references/vox/<slug>/`: per-video folder (start from `_TEMPLATE/`) with `audio/` (separated stems), `transcript.md` (word-timed) and `notes.md` (shot-by-shot breakdown).
- `references/frames/<slug>/`: frame-by-frame stills (e.g. 2 fps).
- `references/sheets/<slug>/`: contact sheets with timestamps.
- `references/random-frames/`: single standout frames (maps, titles, charts, grades), indexed in `INDEX.md`.
- `references/tutorial/`: tutorial videos about how to make this style: `frames/<slug>/`, `transcripts/<slug>.md`, and `<slug>.notes.md` with extracted techniques.
Each folder has a README with naming rules.

Measured findings from all references are distilled into `references/STYLE_BIBLE.md` and `references/reports/` (pacing, shot length, motion, typography, colour, sound). The skill follows those reports, so improving them improves every video.

## Pipeline
1. **Topic and facts.** One surprising true story with a clear cause and effect. Sources at the top of `SCRIPT.md`.
2. **Script.** ~2.5-3.2 words/s, 55-70 s. Hook, stakes, explanation in steps, twist, payoff. Conversational, specific, no filler. Every line either moves the story or sharpens the idea.
3. **Voice.** Record or generate `voice.wav`, then word timings in `words.json`. Hand-fix them. Everything is timed to the words.
4. **Shot plan.** One row per shot: start/end frame, what is on screen, motion, transition, sound. Visual reactions land 0-3 frames before their word.
5. **Build visuals** in Remotion: maps, charts, typography, cut-out imagery, simple 3D where it helps. Use motion with intent (ease curves, parallax, camera moves), never static slides.
6. **Sound.** Voice first, then music bed ducked under it, then synthesized or sourced effects timed to the picture (`templates/audio/`). Lock picture timing before making sound.
7. **Look checks.** Render stills, build side-by-sides against reference frames (`templates/scripts/sbs_sheet.py`), fix differences.
8. **Final render and QA.** 1080x1920 at 24 fps (rule T4; confirm the platform accepts it), then run `templates/scripts/short_qa.py` for black, white, frozen and pop frames and loudness.
9. **Deliver** the mp4 and update notes.

## Look rules (start here)
Numbered rules with Cited/Inference tags live in `references/reports/`: `texture.md` (T1-T19), `sound.md` (S1-S12), `pacing.md` (P1-P10). Style summary: `references/STYLE_BIBLE.md`. Full research: `reports/Vox explainer visuals textures music.md` and the raw notes in `research_notes/`.
The ten that matter most:
1. Deterministic Remotion only: `useCurrentFrame()` + `interpolate()`, seeded `random()`; no CSS animations, no `Math.random()`.
2. Compose at 24 fps; graphics step at 12 fps (hold 2 frames); boil seeds refresh at 4-12 fps.
3. Cutouts: rough alpha edge, white border, soft shadow that moves with scale.
4. Warm off-white paper layer on Multiply; never pure white.
5. Grain LAST, fine, about 15-20% opacity. Texture only on a subset of scenes.
6. Compositing order: flat art, roughen/offset, stepped seed, paper, shadow, lens, grain.
7. Shot lengths right-skewed (median about 3.5-4 s, a few 6-10 s holds). Hard cuts; transitions only at section changes.
8. Voice about 150 wpm plus 0.4-0.9 s pause after the key claim.
9. Music 2-3 sections for a short, minimal, ducked 14-18 dB, dropped on the claim; SFX 3-5 accents, whoosh 1-3 frames early.
10. Final mix about -14 LUFS, true peak -1 to -2 dBTP; keep key content inside the 984x1500 px safe core.
Sources of imagery must be logged in an asset ledger (URL, author, licence, date).
First measurements from real Vox clips (`references/reports/observed.md`): content is 24 fps; shot changes in an archival montage were a 4-frame (at 24 fps) dip to flat dark grey (#1d1d1d) with the corner watermark kept on screen, not plain hard cuts; subtitles lag the picture cut by about 0.25 s; archival shots drift a few percent over 1.5-2 s. Tiny sample (5 s, one episode), so verify on more clips.
Analyse any new clip with `python3 -I templates/scripts/analyze_clip.py <video> <slug> <repo>` (writes frames, a contact sheet and analysis.json).

## Refinement loop (the point of this repo)
After each video: compare against the references, write what felt "generated" instead of "human-made" into `references/reports/`, and change the skill so the next video avoids it.

## TODO (next sessions)
- Fill the first reference folders and validate the rules in `references/reports/` against our own frames and audio.
- Smoke-test `@remotion/effects` (paper, roughenEdges, halftone) headless on the target machine, and build the SVG-filter fallback.
- Finish the unresearched areas listed in `references/STYLE_BIBLE.md` (open gaps).
- Rewrite the shot and camera system for motion-graphics layouts (templates currently target a 3D cartoon world).
- Add a text and typography module, a map module and a chart module.
- Add a GitHub Actions workflow to render in CI.
