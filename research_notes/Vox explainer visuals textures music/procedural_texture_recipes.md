# Procedural paper, grain, halftone, collage and cutout textures in code (Remotion 4.x, no image assets)

STATUS: DRAFT v0 (skeleton saved before research; sections get filled/appended as sources are read). Compiled 2026-11-12. Labels: "Cited" = stated by the linked source; "Snippet (mine)" = code I wrote from understanding of the primitives, not copied from a source; "UNVERIFIED headless" = I have not run it in Remotion's headless Chromium in this session.

## 1. SVG filters (feTurbulence, feDisplacementMap, feColorMatrix, feComposite, feMorphology) in Remotion

### Takeaway
(pending)

### Cited Findings
- (pending)

### Inferences
- (pending)

### Gaps
- (pending)

## 2. Canvas 2D and GLSL: noise, film grain, halftone, vignette, chromatic aberration, bloom

### Takeaway
(pending)

### Cited Findings
- (pending)

### Inferences
- (pending)

### Gaps
- (pending)

## 3. CSS: mix-blend-mode, mask-image, filter drop-shadow, reliability in Remotion's renderer

### Takeaway
(pending)

### Cited Findings
- (pending)

### Inferences
- (pending)

### Gaps
- (pending)

## 4. Remotion specifics: random(), @remotion/noise, @remotion/paths, shapes, three, skia, --gl, CSS animation pitfalls, performance

### Takeaway
Use `random(seed)` and `@remotion/noise` for anything stochastic, and drive every animation from `useCurrentFrame()` (never CSS `transition`/`@keyframes`). NEW and most important: since Remotion 4.0.464 (2026) there is an `@remotion/effects` package of GPU (WebGL2/WebGPU) shader effects applied through an `effects={[...]}` prop on canvas-based components. It already contains `paper()`, `halftone()`, `whiteNoise()`, `roughenEdges()` and `lightLeak()`, which cover much of this brief natively. Remotion 5.0 was still "not yet released" on its migration page when read (2026-11-12), so everything here targets 4.0.x.

### Cited Findings
- `random(seed)` accepts a number or string, returns a deterministic value in [0,1); Remotion renders on multiple threads/tabs so `Math.random()` would differ per thread; `random(null)` is the explicit non-deterministic escape hatch; no-arg call throws. Example uses per-index string seeds like `random(\`random-x-${i}\`)`. — [Remotion random()](https://www.remotion.dev/docs/random)
- `@remotion/noise` (since v3.2.32) exports `noise2D`, `noise3D`, `noise4D`; `noise3D(seed, x, y, z)` takes a string or number seed and returns a smooth value in [-1, 1]. — [noise](https://www.remotion.dev/docs/noise/), [noise3D](https://www.remotion.dev/docs/noise/noise-3d)
- `evolvePath(progress, path)` from `@remotion/paths` returns `{strokeDasharray, strokeDashoffset}`; progress 0 = invisible, 1 = fully drawn; progress >1 devolves the start of the path, <0 evolves from the end. Example in docs: `evolvePath(0.5, "M 0 0 L 100 0")` -> `{strokeDasharray:'100 100', strokeDashoffset:50}`. — [evolvePath](https://www.remotion.dev/docs/paths/evolve-path)
- `@remotion/shapes` `makeRect({width,height})` returns `{path, width, height, transformOrigin}` (rect path `M 0 0 l 100 0 l 0 100 l -100 0 Z`); shapes are SVG path generators usable inside `<svg>`. — [makeRect](https://www.remotion.dev/docs/shapes/make-rect)
- CSS-driven animation is called wrong in Remotion: "`transition`, `@keyframes`, or JavaScript-based timers like `setTimeout`" will flicker or give wrong progress because "CSS animations don't know which frame Remotion is currently rendering"; drive everything from `useCurrentFrame()` + `interpolate()`. — [Troubleshooting: CSS animations](https://www.remotion.dev/docs/troubleshooting/css-animations)
- `--gl` options: `null` = Remotion 4.0 default (Chrome decides); `angle` = recommended for WebGL/three.js on desktop (default in Remotion 5.0, falls back to SwiftShader); `angle-egl` (>=4.0.52) for Linux cloud GPU instances; `swangle` default on Lambda/Cloud Run and recommended with no GPU (slow); `vulkan` (>=4.0.41). `angle` has known memory leaks (split long renders); in 4.0 GitHub Actions runners fail with `angle` (no GPU). Page does not mention SVG filters. — [--gl option](https://www.remotion.dev/docs/gl-options)
- Remotion 5.0 migration page says 5.0 is "not yet released", lists planned changes (GL default -> `angle`; path functions return `null` past path end; `@remotion/light-leaks` and `@remotion/starburst` stop being published after 4.x). — [v5.0 migration](https://remotion.dev/docs/5-0-migration)
- Performance page: `--concurrency` tunable (`npx remotion benchmark`); GPU-heavy things listed as potentially slow on cloud machines without a GPU: WebGL (three.js, Skia, P5.js), 2D canvas, and CSS `box-shadow`, `text-shadow`, `linear-gradient()`, `radial-gradient()`, `filter: blur()`, `filter: drop-shadow()`; suggested fix is to replace them with a precomputed image; PNG slower than JPEG; `--scale` reduces output size. SVG filters are NOT mentioned. — [Performance](https://www.remotion.dev/docs/performance)
- `@remotion/three`: `<ThreeCanvas>` lets `useCurrentFrame()` drive scene (not R3F `useFrame()`); use `<Sequence layout="none">` inside it; needs a non-default GL renderer, docs recommend `angle` (`Config.setChromiumOpenGlRenderer('angle')`, or `chromiumOptions: {gl: 'angle'}` for SSR/Lambda APIs). Also `<ThreeWebGPUCanvas>` (TSL materials). — [@remotion/three](https://www.remotion.dev/docs/three)
- `@remotion/skia`: wraps React Native Skia; install pinned (exact versions, page example 4.0.236), `enableSkia()` webpack override, `await LoadSkia()` before `registerRoot()`; CPU-rendered by default, "some Skia effects rely on GPU features and can be very slow"; `--gl=angle` is the suggested fix. Page does not document shader/filter support. — [@remotion/skia](https://www.remotion.dev/docs/skia)

#### @remotion/effects (the new native route)
- Effects feature available from 4.0.464; `effectsOutputSize` from 4.0.474. Pass an array to `effects` on `<Solid>`, `<HtmlInCanvas>`, `<Video>`, `<Img>`, `<CanvasImage>`, `<AnimatedImage>`, `<Gif>`, `<RemotionRiveCanvas>` and `@remotion/shapes` components; applied in listed order; `createEffect()` for custom effects (2D canvas, WebGL2 or WebGPU). Example: `effects={[blur({radius: 40})]}`. — [Effects](https://remotion.dev/docs/effects)
- Effects do NOT animate on their own: "Effects do not animate on their own", drive props from `useCurrentFrame()` / `interpolate()`. — [lightLeak](https://remotion.dev/docs/effects/light-leak), [whiteNoise](https://www.remotion.dev/docs/effects/white-noise)
- `paper()` (`@remotion/effects/paper`, added 4.0.486, WebGPU backend 4.0.540, WebGL2 also supported): procedural grain, fibres, crumples, folds, speckles; preserves source alpha; based on the open-source Paper Shaders paper texture. Props (defaults): amount 1, colorFront #9fadbc, colorBack #ffffff, contrast .3, roughness .4, fiber .3, fiberSize .2, crumples .3, crumpleSize .35, folds .65, foldCount 5, drops .2, fade 0, seed 6 (0-1000), scale .6. — [paper()](https://www.remotion.dev/docs/effects/paper)
- `halftone()` (`@remotion/effects/halftone`, added 4.0.467; compatible with `<Video>`, `<HtmlInCanvas>`, `<Solid>`): `shape` circle|square|line, `dotSize` (20), `dotSpacing`, `rotation` (deg), `offsetX/Y`, `sampling` bilinear|nearest, `colorMode` solid|source, `dotColor` (default 'red'), `invert`. Single-colour per pass; page does not mention CMYK (so a CMYK look needs 3-4 stacked passes or a custom shader). — [halftone()](https://remotion.dev/docs/effects/halftone)
- `whiteNoise()` (4.0.470): replaces/blends toward grayscale random noise, props `amount`, `seed`; animate by passing a seed derived from the frame. Docs contrast it with `noise()`, which "adds centered noise to existing pixels, which suits subtle film grain". — [whiteNoise()](https://www.remotion.dev/docs/effects/white-noise)
- `roughenEdges()` (4.0.487; WebGL2, WebGPU 4.0.540): roughens the alpha boundary into an "irregular paper-like edge"; props `amount` 1, `border` 26.5 px (0-200), `scale` .07, `seed` 231.2 (0-1000; pass a frame-derived value to animate). — [roughenEdges()](https://convert.remotion.dev/docs/effects/roughen-edges)
- `lightLeak()` (`@remotion/effects/light-leak`, 4.0.500): WebGL2/WebGPU overlay; props `seed`, `hueShift` (0 = yellow-orange, 120 green, 240 blue), `progress` (reveals first half, retracts second half), `disabled`; usable on `<Solid>`, `<Video>`, `<CanvasImage>`, and as a `TransitionSeries.Overlay`. The older `@remotion/light-leaks` package is listed as not published after 4.x. — [lightLeak()](https://remotion.dev/docs/effects/light-leak)
- Search listing also shows docs pages for `blur`, `halftone-linear-gradient` and others (about 50 effects advertised by a third-party news summary), but I only read paper, halftone, white-noise, roughen-edges, light-leak, blur. — [search result: alphasignal summary](https://alphasignal.ai/news/remotion-ships-50-video-effects-react-developers-can-control-with-ai.md) (secondary, not read)

### Inferences
- Because `paper()` and `roughenEdges()` are GPU shaders applied to a canvas, they likely need a working WebGL2 context in the renderer; on a laptop render that is probably fine, on CI/cloud without GPU use `--gl=swangle` (slow) or `angle-egl` with a GPU. I did not find the effects docs stating a `--gl` requirement, so this is inference.
- The effects package is new (4.0.464 onward), so pin one exact `remotion` + `@remotion/effects` version across all packages, as Remotion requires versions to match.
- The `random()`-seeded + `useCurrentFrame()` pattern means stepped/boiling effects (section 5) are done by quantising the frame number before using it as seed.

### Gaps
- Full list of effects in `@remotion/effects` (docs table of contents did not render in the fetch; only paper, halftone, white-noise, roughen-edges, light-leak, blur, halftone-linear-gradient confirmed to exist). Check `https://remotion.dev/docs/effects/api` in a browser.
- Whether `@remotion/effects` works with `--gl=null`/default on a headless Linux box: not stated; test with a one-frame `npx remotion still`.
- Install command for `@remotion/effects` not shown on pages read (assume `npm i @remotion/effects@<same version as remotion>`).

## 5. Stepped (boiling, 8-12 fps) animation and wobble

### Takeaway
(pending)

### Cited Findings
- (pending)

### Inferences
- (pending)

### Gaps
- (pending)

## 6. Cutout look: white stroke + soft shadow around arbitrary alpha shape, rotation, paper thickness, torn edges

### Takeaway
(pending)

### Cited Findings
- (pending)

### Inferences
- (pending)

### Gaps
- (pending)

## 7. Draw-on in SVG: highlighter, underline, circle annotation, handwriting, rough paths

### Takeaway
(pending)

### Cited Findings
- (pending)

### Inferences
- (pending)

### Gaps
- (pending)

## 8. Open-source libraries and CC0 texture sources (with licences)

### Takeaway
(pending)

### Cited Findings
- (pending)

### Inferences
- (pending)

### Gaps
- (pending)

## 9. Whole-look compositing recipe (misregistration, dust/scratches, light leaks, duotone, DOF)

### Takeaway
(pending)

### Cited Findings
- (pending)

### Inferences
- (pending)

### Gaps
- (pending)
