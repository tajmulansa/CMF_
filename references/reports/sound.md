# Sound report (music, SFX, mix)

Evidence: Vox staff sources (2016-2022) document music practice for ONE video; levels and SFX numbers come from third-party/vendor guides or are Inference. Citations: `reports/Vox explainer visuals textures music.md`.

## What is documented about Vox
- Producers choose and edit music themselves. Music is licensed from APM (library), looking for minimal, energetic tones. Black-hole video: tracks switched about every 20 s, cut into sections, beats aligned, bass/kick layered from another track, endings extended or pasted.
- Track starts/ends used as attention cues; a track ended right after a key statement for emphasis; music kept sparse/low under narration; busy instruments that compete with the narrator's pitch range avoided; fast music to open, a reflective track at the delayed reveal.
- A reverb trick can make a track sound as if it has ended when it has not.
- Effects: paid library (Soundsnap) and library risers (one former producer). No Vox SFX recipe is published.

## Rules (C = cited, I = inference)
| # | Rule | Tag |
|---|------|-----|
| S1 | Music minimal, energetic, not busy; sparse/low under voice; avoid melody in the narrator's pitch range. | C |
| S2 | Change music section about every 20 s. For 55-70 s that is 2-3 sections (hook, body, close). | C (20 s) / I (scaling) |
| S3 | End a track or leave silence right after the key claim; 0.5-1.5 s of silence before a reveal. | C (track end) / I (numbers) |
| S4 | Final mix about -14 LUFS integrated (window -16 to -13), true peak -1 to -2 dBTP. Do not chase louder. (Sources conflict on -1 vs -2.) | C (third-party) |
| S5 | Duck music -14 to -18 dB with a 300-450 ms fade (Premiere preset) or -10 to -16 dB with a 400 ms hold (Resolve). Sources conflict (a "20-25 dB below voice" claim, an unsourced 12-20 dB working range). Verify with a LUFS meter AND a low-volume listen. | C (presets) / I (range) |
| S6 | Music EQ carve at 1.5-3.5 kHz, -2.5 to -4 dB, Q 1.0-1.4; avoid pad build-up at 250-500 Hz. | C (vendor) |
| S7 | Voice chain: gate 6-8 dB range, HPF up to ~80 Hz, bell cuts 300-800 Hz, 1-2 dB cut at 5-10 kHz, de-ess under ~4 dB, compress 2:1-4:1 under ~6 dB, limiter last under ~6 dB. | C (third-party) |
| S8 | SFX: one family; starter kit whoosh + hit + tick (+ optional riser); 3-5 accents total; own track, below voice. | C (generic) |
| S9 | Sync: align the transient (not the file start) to the landing frame. Whoosh 1-3 frames (about 40-100 ms) early; impact on the landing frame or 1 frame early. Test by ear. | C (principle) / I (numbers) |
| S10 | Layer SFX offset 1-3 frames across different frequency ranges so they fuse. | C |
| S11 | SFX vocabulary: swish = slide/camera move, tick/pop = highlight/text, paper rustle = document/photo, pencil scribble = hand-drawn underline, key taps = typed text, shutter = photo snap, low hit = reveal, riser into reveal. Shift a cue so its peak avoids an important word. | I |
| S12 | Music style guide (vendor, low reliability): marimba/pizzicato 95-110 BPM, light tech pulse 110-124, subtle cinematic underscore 70-90, ambient pads 60-75, playful plucks 115-128. | C (vendor) |

## Original audio plan
Use original or properly licensed music only (the pipeline's `templates/audio/` synthesizer is the base). Humanize synthesized music: timing and velocity jitter, swing, layer variation. Synthesised whoosh = band-passed noise with an envelope, plus a short tonal tick, through one shared reverb bus (Inference). Tooling, theory and free-library licences (Q7, Q8) were NOT researched to completion: see the gaps list.
