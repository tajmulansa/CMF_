# Pacing, narration and process report

Evidence: Vox sources describe process and craft, not metrics. Numbers come from a vendor sample of AI-built long-form timelines (not Vox, not Shorts) or are Inference. Citations: `reports/Vox explainer visuals textures music.md`.

## Process (Cited, Vox staff)
- One producer owns a video end to end (research, script, edit, graphics). After Effects is the main graphics tool; Premiere for edit and mix. Every video gets a script editor who flags confusing parts.
- Inferred order: research and assets -> script written around the available visuals -> edit with placeholder graphics -> motion graphics -> audio. Animation is a fast, late step after research and writing.
- Narration: plainer than print, not too clever, pauses after big ideas, signpost where to look. Open on the thing the audience can picture before the abstract reveal. Start from what the audience does not yet understand.
- Vox short-form guidance (2022): "transient, organic, native" rather than polished.

## Rules (C = cited, I = inference)
| # | Rule | Tag |
|---|------|-----|
| P1 | Voice about 150 wpm (2.5 words/s). 60 s script = 140-150 words; 55-70 s = about 137-175 words before pauses. | C (vendor) |
| P2 | Add 0.4-0.9 s of extra silence after the claim-bearing sentence; vary sentence length; avoid a metronomic cadence. Each second of pause removes about 2.5 words. | C (pauses) / I (numbers) |
| P3 | Shot lengths are right-skewed, not uniform: median about 3.5-4 s; P10 about 1.5 s, P25 about 2.3 s, P75 about 5.3 s, P90 about 7.5 s; first 30 s slightly faster (about 3.2 s). | C (vendor long-form sample) / I (Shorts) |
| P4 | Hold by content: hook 2-4 s, standard 3-5 s, evidence photo 6-10+ s, chart 5-12+ s. Text reading floor = words / 3 + 1 s. | C (vendor opinion) / I (floor) |
| P5 | A 55-70 s short is roughly 13-18 scenes at the vendor's long-form density; Shorts are probably faster (unmeasured). | I |
| P6 | Hard cuts by default; transitions only at section changes. | I |
| P7 | Vertical safe area at 1080x1920: keep key content in the centred ~984x1500 px (top 120-290, bottom 300-670, right 96-190, left 48). Captions 60-75 px, 1-3 words (karaoke) or 3-8 words per card, width under ~850 px. | C (vendor estimate) |
| P8 | One idea per frame; design vertical-first, not shrunken 16:9. | I |
| P9 | Human tells to add: on-screen source lines, a 1-5% push on stills with randomised direction, hand-drawn annotations, intentional silence before a reveal. | I |
| P10 | Automation tells to avoid: identical shot length, the same transition on every cut, one music bed throughout, text animating on every line, charts held 2 s, no on-screen sources. | I |

## Sourcing and legal (Cited)
- Lock the asset list (photo/footage/document/graphic per beat) before the final script.
- Keep an asset ledger per item: URL, author, licence, date, caveats. Flag logos, identifiable people and third-party music; credit sources in the description and on screen.
- NASA: generally not copyrighted, but logos, third-party material and identifiable people have limits. Library of Congress: rights are per item. Internet Archive: no copyright guarantee; Prelinger films are not blanket public domain. Wikimedia Commons, Smithsonian, Unsplash and Pexels terms were NOT verified.

## QA gate (to build)
Measure and fail on: shot-length variation, repeated transition count, music-change count, text words vs hold time, LUFS and true peak, fraction of scenes with texture.
