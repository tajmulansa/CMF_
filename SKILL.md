---
name: cmf-explainer-short
description: Make a CuriousMindsFeed vertical explainer short (55-70 s) in a Vox-style editorial look - tight narration, motion graphics, maps, typography, archive-style imagery, designed sound - rendered with Remotion. Use when the user asks for a CMF video, an explainer short, or says "use the CMF skill".
---

# CMF explainer short (Remotion)

Goal: videos that feel hand-edited by a person, not generated. The target is the pacing, structure and polish of Vox-style explainers, built from our own scripts, visuals and voice.

## Status
Version 0.1 - scaffold. `templates/` is copied from the open-source (MIT) `mromidev/claude-animated-shorts` skill and still contains its 3D cartoon pipeline. It is the engine to learn from and rewrite, not the final look. See `NOTICE`.

## Ground rules
- References are STUDY MATERIAL. Learn pacing, structure, shot rhythm and sound design. Never copy scripts, footage, graphics or voice. Story, visuals and voice are always our own.
- Never name the reference channel in a voice-over, title or description.
- Keep this repo private while it holds reference frames, audio or transcripts.
- Save after every step. Commit often.

## How the references work
Each reference video gets its own folder: `references/vox/<slug>/` (start from `references/vox/_TEMPLATE/`).
- `frames/`: frame-by-frame stills (e.g. 2 fps) plus contact sheets.
- `audio/`: separated stems if available (voice, music, sfx).
- `transcript.md`: word-timed transcript.
- `notes.md`: shot-by-shot breakdown (see template).

Measured findings from all references are distilled into `references/STYLE_BIBLE.md` and `references/reports/` (pacing, shot length, motion, typography, colour, sound). The skill follows those reports, so improving them improves every video.

## Pipeline
1. **Topic and facts.** One surprising true story with a clear cause and effect. Sources at the top of `SCRIPT.md`.
2. **Script.** ~2.5-3.2 words/s, 55-70 s. Hook, stakes, explanation in steps, twist, payoff. Conversational, specific, no filler. Every line either moves the story or sharpens the idea.
3. **Voice.** Record or generate `voice.wav`, then word timings in `words.json`. Hand-fix them. Everything is timed to the words.
4. **Shot plan.** One row per shot: start/end frame, what is on screen, motion, transition, sound. Visual reactions land 0-3 frames before their word.
5. **Build visuals** in Remotion: maps, charts, typography, cut-out imagery, simple 3D where it helps. Use motion with intent (ease curves, parallax, camera moves), never static slides.
6. **Sound.** Voice first, then music bed ducked under it, then synthesized or sourced effects timed to the picture (`templates/audio/`). Lock picture timing before making sound.
7. **Look checks.** Render stills, build side-by-sides against reference frames (`templates/scripts/sbs_sheet.py`), fix differences.
8. **Final render and QA.** 1080x1920 at 30 fps, then run `templates/scripts/short_qa.py` for black, white, frozen and pop frames and loudness.
9. **Deliver** the mp4 and update notes.

## Refinement loop (the point of this repo)
After each video: compare against the references, write what felt "generated" instead of "human-made" into `references/reports/`, and change the skill so the next video avoids it.

## TODO (next sessions)
- Fill the first reference folders and write the reports.
- Rewrite the shot and camera system for motion-graphics layouts (templates currently target a 3D cartoon world).
- Add a text and typography module, a map module and a chart module.
- Add a GitHub Actions workflow to render in CI.
