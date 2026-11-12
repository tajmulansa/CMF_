# Vox explainer video textures and surface treatments: vocabulary and how pros build them

STATUS: DRAFT v0 (early save). Being extended. Labels: "Cited" = stated by the linked source; "Inference" = my reading of how Vox-style videos look, not stated by any source.

## What texture types appear in Vox-style videos, and how are they built?

### Takeaway
Source coverage of Vox's own textures is thin: no Vox art director interview found that names textures directly. What exists is (a) tutorials that reproduce the "Vox look" in After Effects, and (b) general handmade-look techniques (Roughen Edges, Fractal Noise, Posterize Time, wiggle). Draft only; see sections below as they are filled.

### Cited Findings
- A PremiumBeat breakdown of replicating the Vox look says to render the graphics comp at 12 fps while the main edit stays 24 fps so graphics visibly stutter, which the author says adds character to plain elements. — [PremiumBeat (Lewis McGregor, 2021)](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)
- Same source: lower thirds use a rough, textured PNG with its jagged edges kept, revealed by a keyframed mask that grows unevenly and skips frames; text is revealed the same way a few frames later. — [PremiumBeat](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)
- Same source: a "motion background" is built from five or six distressed textures cycled so two or three appear each second, duplicated to about ten seconds and used behind static content; with only one texture, flip and rotate it for variety. — [PremiumBeat](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)
- Same source: lens look is Quick Chromatic Aberration (free plugin) on a top adjustment layer, kept subtle and rotated slightly, plus Gaussian Blur 3.5, restricted to the frame edges with an inverted circular mask feathered about 50. — [PremiumBeat](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)
- Same source does NOT cover grain, paper, drop shadows, halftone or palette. — [PremiumBeat](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)

### Inferences
- (pending)

### Gaps
- (pending)

---
## WORKING LOG (raw findings appended during research; will be folded into the sections above in the final rewrite)

- School of Motion hand-drawn look: Roughen Edges Scale ~100 -> ~10, Border ~3 for outlines; brush-style shadow = circle + Roughen Edges (Border 400, Scale ~10) + Gaussian Blur + Multiply; flicker texture = Fractal Noise Contrast ~6000, Multiply, hold keyframes on Evolution every few frames (4-5 keys) + loopOut(); Posterize Time 12 fps typical hand-drawn. — https://www.schoolofmotion.com/blog/tricks-for-creating-a-hand-drawn-look-in-after-effects
- Inspired Animator (Medium): line boil via Turbulent Displace Amount 10 Size 20, second pass Size 4 Amount 30; Evolution expression posterizeTime(8); time*1000; suggests 6/8/12 fps; colour boil via Turbulent Noise (Terrain, Contrast 24, Hue blend 15%). — https://medium.com/the-inspired-animator/how-to-apply-a-hand-crafted-look-to-your-animations-in-after-effects-2da1c5dbd282
- PremiumBeat line boil: adjustment layer + Turbulent Displace Amount 5-10, Size 20-60, Random Seed expression posterizeTime(4);random(100) (or 12 for faster). — https://www.premiumbeat.com/blog/wiggle-text-line-boil
- PremiumBeat free animated textures: scanned paper/fabric scanned facing different directions, animated "on twos"; Multiply on top, Overlay/Hard Light alternatives; Tint to recolour; keep simple; ~50% of end-tag animations might benefit from a little texture. — https://www.premiumbeat.com/blog/free-animated-textures/
- Envato Tuts+ collage animation: loose Pen masks for handcrafted edges; Drop Shadow on cutouts; animate Scale+Shadow Distance together to mimic paper lifting; Posterize Time 12 fps. — https://photography.tutsplus.com/articles/collage-animation-in-after-effects--cms-93666
- Miles of Roses (Medium) paper cutout: Roughen Edges per layer (Border 12-45, Scale 76-193); crumpled paper/cardboard/brown paper textures per element; shadows from duplicated black layer + Gaussian Blur 45 (leaves) / 120 (trunk); 3D camera depth Z values. — https://medium.com/@MilesOfRoses/create-a-paper-cut-out-animation-with-after-effects-e4891f6aba95
- Boris FX halftone: CC Ball Action ball size ~18-20 spacing ~5 + Camera Lens Blur w/ blur map to vary dot size; BCC Halftone dot shapes, CMY/CMYK w/ light paper colour for print look, RGB w/ dark paper for screen look. — https://borisfx.com/blog/create-after-effects-halftone-plugin-2-methods
- PremiumBeat film grain: ~15-20% opacity for light blend, fine grain for cohesion across layers. — https://www.premiumbeat.com/blog/using-film-grain-digital-video/
- Video Milkshake grain rules: match grain size to footage format; Linear Light preferred over Overlay for mid-grey grain; sprocket holes should be voids not transparent overlays. — https://www.videomilkshake.com/blogs/news/film-grain-overlays-in-video-editing
- Envato Tuts+ riso texture (Photoshop): paper texture on Multiply; two-tone via Gradient Map (e.g. 2f3450->56d5ff, dd0000->ffc8c8); overprint via Multiply; Camera Raw grain 36; Color Lookup at 30%. — https://design.tutsplus.com/tutorials/how-to-make-a-risograph-texture-effect--cms-38557
- Jonathan Stephens riso reference (CSS): misregistration 0.5-2 px nudges; overprint = multiply; riso ink hexes #0078BF, #FF5C5C, #FFE800, #00A95C. — https://jonathanstephens.us/play/riso/
- aescripts Johnny Harris maps page: no texture details; uses GEOlayers. — https://aescripts.com/learn/how-johnny-harris-makes-maps
- CORRECTION to v0: PremiumBeat Vox article actually has FIVE breakdowns. The one the v0 pass missed is "Tracking Transitions": two pre-edited sequences placed as 3D layers + 3D camera; camera keyframed to pull back over the edit point with Easy Ease peaking on the cut; adjustment-layer blur keyframed up at the cut and down a few frames later, shorter than the camera move. Also: author points to a free Shutterstock set of 50 distressed textures for the motion background; describes Vox look as fluid/professional with small elements giving rhythm; says chromatic aberration gives 2D images a "real life" feel. — https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/
- Enchanted Media torn paper transition (AE): tear matte = solid + Linear Wipe 50% angle 0 + Roughen Edges Border 40, Edge Sharpness 10, Scale 200; scale layer 105%; paper layer on Multiply; Alpha / Alpha Inverted track mattes for the two sides; white rip seam = duplicate matte at 48%/180deg with different Offset Turbulence, white Fill on side 2; optional Noise; Posterize Time 8 fps adjustment layer for stepped look. — https://enchanted.media/?p=393617
- Adobe torn paper edge (Photoshop): lasso jagged selection, white "paper edge" layer slightly larger beneath subject, Warp to make less uniform, Drop Shadow, paper texture as clipping mask. No values. — https://www.adobe.com/learn/photoshop/web/torn-paper-edge
- Tuts+ noise/grain AE: Add Grain intensity ~0.3-0.5 on adjustment layer (Final Output view); pre-rendered grain = 50% grey solid + Add Grain, loop via time remap loopOut("cycle"), blend Overlay or Linear Light; Noise effect to break banding (1-2% steps); 8->16 bpc. — https://photography.tutsplus.com/tutorials/how-to-add-noise-and-grain-in-after-effects--cms-41486
- ProVideo Coalition banding: Add Grain ~1-5% often removes banding; 16/32 bpc; AE dithers on 8-bpc render; avoid pure solid backgrounds since lighting turns them into gradients; low-detail backgrounds. — https://www.provideocoalition.com/remove-banding-in-after-effects/amp/
- Photofocus textures: match texture to existing light colour/intensity/direction; even out lighting with curves/dodge-burn; do not add texture just because you can; avoid straight lines across curved surfaces. — https://photofocus.com/2018/10/03/five-tips-for-adding-textures-to-your-photos/
- autoae newspaper animation (vendor blog): warm off-white/cream paper, "pure white never looks like paper", subtle halftone as realism cue, slightly reduced ink contrast (grey on off-white), highlight sweep ~0.5 s, slow push-in with slight rotation, stop camera when highlight finishes. — https://autoae.online/blog/how-to-make-newspaper-animation-effect
- autoae highlighter (vendor blog): marker sweep via shape + matte, 0.3-0.6 s reveal, Easy Ease (linear looks stiff), slight roughen on bar for marker look, classic yellow. — https://autoae.online/blog/how-to-make-highlight-text-animation-video
- Superhive "Boil" Blender asset pack: single clock node group, "Frames per Drawing" 1/2/3 (twos default), 8 seamless 2048x2048 paper/grain textures, View Transform Standard (AgX mutes saturation). — https://superhivemarket.com/products/boil-hand-drawn-toon-shaders/docs
- Goodspeed via roblog (opinion): authentic imperfection comes from real materials/process; added-on imperfection as signal = "strategic mimicry"; polish now suspected as AI so handmade cues = trust signal. — https://roblog.co.uk/2026/02/faking-realness/
- Caswell on School of Motion podcast (Vox): holds on single image for several seconds, rarely uses transitions, archival images/articles/charts chosen to back facts, no mention of grain/paper. — https://www.schoolofmotion.com/podcast/estelle-caswell-vox-interview
