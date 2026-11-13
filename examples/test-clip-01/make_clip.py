#!/usr/bin/env python3
"""CMF test clip 01: a 5 s vertical explainer snippet that applies the rules in references/reports/.

Original content (placeholder fact, NOT fact-checked for publication). Deterministic: every random value is
seeded by frame/held-frame, no Math.random equivalent. Needs numpy, scipy, opencv, Pillow, ffmpeg.

Usage: python3 -I make_clip.py <outdir> [--stills 8,30,56]   (stills = save PNGs only, no video)
Timeline at 24 fps (120 frames): dark dip 0-5 | shot 1 6-53 | dark dip 54-57 | shot 2 58-119.
Rules applied (see references/reports): T3 graphics held at 12 fps, T4 24 fps, T6/T7 rough cutout edges + white border
+ soft shadow, T8 cycled paper variants, T9 warm paper, T10 grain last, T12 lens on one shot only, T13 shadows,
T15 chromatic aberration + edge blur, T16 compositing order, T18 highlighter draw-on, O1-O3 dip colour, watermark,
caption lag, S2/S3 two music sections with drop at the dip, S8-S10 few SFX landing 1-3 frames early, S4 -14 LUFS.
"""
import math, os, subprocess, sys, zlib
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from scipy import signal

W, H, FPS, N = 1080, 1920, 24, 120
DARK = 29.0                                   # O1: flat dark grey, not pure black
INK = np.array([38, 30, 28], np.float32)
RED = np.array([206, 64, 46], np.float32)
YEL = np.array([255, 226, 64], np.float32)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
if not os.path.exists(SANS):
    SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# timeline
DIP_A = (0, 5)
S1 = (6, 53)
DIP_B = (54, 57)
S2 = (58, 119)


def R(*k):
    return np.random.default_rng(zlib.crc32(repr(k).encode()))


def ease_io(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = np.clip(x, 0, 1)
    return 1 - (1 - x) ** 3


def smooth_noise(shape, sigma, key):
    n = R(*key).standard_normal(shape).astype(np.float32)
    n = cv2.GaussianBlur(n, (0, 0), sigma)
    return n / (n.std() + 1e-6)


def warp(img, dx, dy):
    h, w = img.shape[:2]
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    return cv2.remap(img, gx + dx, gy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


# ---------------------------------------------------------------- paper
def make_paper(seed):
    r = R("paper", seed)
    base = np.zeros((H, W), np.float32)
    for sc, amp in [(6, .35), (24, .35), (96, .30)]:
        small = r.standard_normal((H // sc + 3, W // sc + 3)).astype(np.float32)
        base += amp * cv2.resize(small, (W, H), interpolation=cv2.INTER_CUBIC)
    base /= base.std()
    fib = np.zeros((H, W), np.float32)
    for _ in range(1800):
        x, y = int(r.integers(0, W)), int(r.integers(0, H))
        a, l = r.uniform(0, 6.283), r.uniform(8, 34)
        cv2.line(fib, (x, y), (int(x + l * math.cos(a)), int(y + l * math.sin(a))), float(r.uniform(.25, .9)), 1, cv2.LINE_AA)
    fib = cv2.GaussianBlur(fib, (0, 0), 0.7)
    tone = 1 + 0.018 * base - 0.035 * np.clip(fib, 0, 1)
    return (np.array([241, 233, 215], np.float32)[None, None, :] * tone[..., None]).astype(np.float32)   # T9 warm cream


# ---------------------------------------------------------------- cutout sprites (T6, T7, T13)
def make_sprites(rgb_p, a, border_px, K, key, shadow=(16, 26), rough=2.5, rough_b=4.0, sh_sigma=16, sh_alpha=.34):
    P = 100
    rgb_p = np.pad(rgb_p, ((P, P), (P, P), (0, 0)))
    a = np.pad(a, P)
    out = []
    for k in range(K):
        sx, sy = smooth_noise(a.shape, 5, (key, k, "x")), smooth_noise(a.shape, 5, (key, k, "y"))
        ins = (a > .5).astype(np.uint8)
        dist = np.where(ins > 0, cv2.distanceTransform(ins, cv2.DIST_L2, 3), cv2.distanceTransform(1 - ins, cv2.DIST_L2, 3))
        wgt = np.exp(-dist / 6).astype(np.float32)                  # edge-only roughening: interior art stays clean
        aw, rw = warp(a, rough * sx * wgt, rough * sy * wgt), warp(rgb_p, rough * sx * wgt, rough * sy * wgt)
        straight = rw / np.maximum(aw, 1e-3)[..., None]
        a1 = np.clip((aw - .5) * 3 + .5, 0, 1)
        obj = straight * a1[..., None]
        if border_px:
            bm = cv2.dilate((a > .5).astype(np.float32), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * border_px + 1,) * 2))
            bx, by = smooth_noise(a.shape, 10, (key, k, "bx")), smooth_noise(a.shape, 10, (key, k, "by"))
            b1 = np.clip((warp(bm, rough_b * bx, rough_b * by) - .5) * 3 + .5, 0, 1)
        else:
            b1 = a1
        sh = cv2.GaussianBlur(b1, (0, 0), sh_sigma)
        sh = cv2.warpAffine(sh, np.float32([[1, 0, shadow[0]], [0, 1, shadow[1]]]), (a.shape[1], a.shape[0]))
        S_rgb, S_a = np.zeros_like(rgb_p), sh * sh_alpha
        if border_px:
            A_rgb, A_a = np.array([250, 247, 240], np.float32) * b1[..., None], b1
            S_rgb, S_a = A_rgb + S_rgb * (1 - A_a[..., None]), A_a + S_a * (1 - A_a)
        S_rgb, S_a = obj + S_rgb * (1 - a1[..., None]), a1 + S_a * (1 - a1)
        out.append(np.concatenate([S_rgb, S_a[..., None]], axis=2).astype(np.float32))
    return out


def build_jar():
    S = 2
    w, h = 760 * S, 980 * S
    ink = (52, 34, 44, 255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    e = 7 * S
    for box, rad in [((80, 230, 680, 900), 90), ((170, 150, 590, 260), 30), ((130, 70, 630, 170), 22)]:
        d.rounded_rectangle([box[0] * S - e, box[1] * S - e, box[2] * S + e, box[3] * S + e], radius=rad * S + e, fill=ink)
    ys = np.linspace(0, 1, h)[:, None, None]
    col = np.array([232, 160, 38]) * (1 - ys) + np.array([176, 98, 14]) * ys
    grad = np.zeros((h, w, 4), np.uint8)
    grad[..., :3] = np.broadcast_to(col, (h, w, 3)).astype(np.uint8)
    grad[..., 3] = 255
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([80 * S, 230 * S, 680 * S, 900 * S], radius=90 * S, fill=255)
    md.rounded_rectangle([170 * S, 150 * S, 590 * S, 260 * S], radius=30 * S, fill=255)
    jar = Image.fromarray(grad)
    jar.putalpha(mask)
    im.alpha_composite(jar)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([130 * S, 70 * S, 630 * S, 170 * S], radius=22 * S, fill=(128, 78, 42, 255))
    for x in range(160, 620, 34):
        d.line([x * S, 84 * S, x * S, 156 * S], fill=(104, 62, 34, 255), width=5 * S)
    d.rounded_rectangle([190 * S, 470 * S, 570 * S, 760 * S], radius=20 * S, fill=(247, 238, 214, 255), outline=ink, width=5 * S)
    f1 = ImageFont.truetype(SERIF, 78 * S)
    f2 = ImageFont.truetype(SANS, 34 * S)
    for txt, fnt, y in [("HONEY", f1, 528), ("PURE & SEALED", f2, 662)]:
        tw = d.textlength(txt, font=fnt)
        d.text((380 * S - tw / 2, y * S), txt, font=fnt, fill=(86, 52, 30, 255))
    for cx, cy in [(300, 500), (380, 500), (460, 500)]:      # tiny honeycomb cells
        pts = [(cx * S + 22 * S * math.cos(math.pi / 3 * i), cy * S + 22 * S * math.sin(math.pi / 3 * i)) for i in range(6)]
        d.polygon(pts, outline=(214, 138, 24, 255), width=3 * S)
    d.rounded_rectangle([118 * S, 300 * S, 158 * S, 840 * S], radius=20 * S, fill=(255, 255, 255, 70))
    d.ellipse([112 * S, 262 * S, 160 * S, 292 * S], fill=(255, 255, 255, 90))
    im = im.resize((760, 980), Image.LANCZOS)
    arr = np.asarray(im).astype(np.float32)
    a = arr[..., 3] / 255
    return arr[..., :3] * a[..., None], a


def build_backing():
    w, h = 880, 1040
    a = np.ones((h, w), np.float32)
    rgb = np.zeros((h, w, 3), np.float32)
    rgb[:] = np.array([217, 196, 160], np.float32)
    n = smooth_noise((h, w), 3, ("kraft",))
    rgb *= (1 + 0.03 * n)[..., None]
    return rgb * a[..., None], a


# ---------------------------------------------------------------- text
def fit_font(path, lines, maxw, start):
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    size = start
    while size > 20:
        f = ImageFont.truetype(path, size)
        if max(d.textlength(t, font=f) for t in lines) <= maxw:
            return f
        size -= 2
    return ImageFont.truetype(path, 20)


def layer_lines(lines, font, cx, y0, line_h, tracking=0):
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    boxes = []
    for i, t in enumerate(lines):
        if tracking:
            widths = [d.textlength(c, font=font) + tracking for c in t]
            w = sum(widths) - tracking
            x = cx - w / 2
            xx = x
            for c, cw in zip(t, widths):
                d.text((xx, y0 + i * line_h), c, font=font, fill=255)
                xx += cw
        else:
            w = d.textlength(t, font=font)
            x = cx - w / 2
            d.text((x, y0 + i * line_h), t, font=font, fill=255)
        boxes.append((x, y0 + i * line_h, w))
    return np.asarray(img, np.float32) / 255, boxes


def word_span(font, line, sub, x_line):
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    pre = line[: line.index(sub)]
    x0 = x_line + d.textlength(pre, font=font)
    return x0, x0 + d.textlength(sub, font=font)


INKTEX = None


def ink_alpha(mask):
    return mask * (1 - 0.10 * np.abs(INKTEX))


def highlight_mask(x0, x1, y0, y1, prog, key, hf):
    m = np.zeros((H, W), np.float32)
    if prog <= 0:
        return m
    xe = x0 + (x1 - x0) * prog
    xs = np.linspace(x0, xe, 28)
    j = R("hlj", key, hf // 2).normal(0, 1.1, (2, 28))
    top = y0 + 3 * np.sin(xs * .02 + key) + j[0]
    bot = y1 + 3 * np.sin(xs * .017 + key * 2) + j[1]
    pts = np.concatenate([np.stack([xs, top], 1), np.stack([xs[::-1] + 4, bot[::-1]], 1)]).astype(np.int32)
    cv2.fillPoly(m, [pts], 1.0)
    return cv2.GaussianBlur(m, (0, 0), .8)


def marker_ellipse(cx, cy, rx, ry, prog, hf, seed):
    m = np.zeros((H, W), np.float32)
    n = 150
    k = int(n * min(prog, 1))
    if k < 3:
        return m
    th = np.linspace(-0.6, -0.6 + 2 * math.pi * 1.08, n)
    wob = np.convolve(R("ell", seed).standard_normal(n + 24), np.ones(12) / 12, "same")[12:n + 12] * 5
    rad = 1 + 0.04 * (th - th[0]) / (2 * math.pi)
    ang = math.radians(-4)
    x = rx * rad * np.cos(th) + wob
    y = ry * rad * np.sin(th) + wob
    px = cx + x * math.cos(ang) - y * math.sin(ang)
    py = cy + x * math.sin(ang) + y * math.cos(ang)
    jit = R("ellj", seed, hf // 2).normal(0, 1.1, (n, 2))                # boil: refreshed at 12 fps (T3/T5)
    pts = np.stack([px + jit[:, 0], py + jit[:, 1]], 1)[:k].astype(np.int32)
    cv2.polylines(m, [pts], False, 1.0, 15, cv2.LINE_AA)
    cv2.polylines(m, [(pts + np.int32([2, 3]))], False, 1.0, 8, cv2.LINE_AA)
    return cv2.GaussianBlur(m, (0, 0), .7)


def marker_line(x0, x1, y, prog, hf, seed):
    m = np.zeros((H, W), np.float32)
    if prog <= 0:
        return m
    xs = np.linspace(x0, x0 + (x1 - x0) * prog, 40)
    wob = np.convolve(R("ul", seed).standard_normal(64), np.ones(8) / 8, "same")[:40] * 6
    jit = R("ulj", seed, hf // 2).normal(0, 1.0, (40, 2))
    pts = np.stack([xs + jit[:, 0], y + wob + jit[:, 1] + (xs - x0) * 0.012], 1).astype(np.int32)
    cv2.polylines(m, [pts], False, 1.0, 13, cv2.LINE_AA)
    return cv2.GaussianBlur(m, (0, 0), .7)


def multiply(img, m, color, strength=1.0):
    k = (m * strength)[..., None]
    return img * (1 - k + k * color / 255.0)


def over_ink(img, mask, color=INK):
    a = ink_alpha(mask)[..., None]
    return img * (1 - a) + color * a


# ---------------------------------------------------------------- setup
print("building assets...", flush=True)
PAPERS = [make_paper(i) for i in range(3)]                          # T8: cycle distressed variants
INKTEX = smooth_noise((H, W), 1.2, ("ink",)).astype(np.float32)
_jar_rgb, _jar_a = build_jar()
JAR = make_sprites(_jar_rgb, _jar_a, 20, 4, "jar")
_bk_rgb, _bk_a = build_backing()
BACK = make_sprites(_bk_rgb, _bk_a, 0, 4, "back", rough=3.0, sh_alpha=.30)

SUB1 = ["Honey jars were found", "in ancient Egyptian tombs."]
SUB2 = ["That is older than", "the Roman Empire."]
SUBFONT = fit_font(SANS, SUB1 + SUB2, 860, 58)
SUBY, SUBLH = 1340, 84
sub1_mask, sub1_boxes = layer_lines(SUB1, SUBFONT, W / 2, SUBY, SUBLH)
sub2_mask, sub2_boxes = layer_lines(SUB2, SUBFONT, W / 2, SUBY, SUBLH)
asc, desc = SUBFONT.getmetrics()
HL1 = (*word_span(SUBFONT, SUB1[1], "ancient Egyptian tombs.", sub1_boxes[1][0]), SUBY + SUBLH + 6, SUBY + SUBLH + asc + desc - 4)
HL2 = (*word_span(SUBFONT, SUB2[1], "Roman Empire.", sub2_boxes[1][0]), SUBY + SUBLH + 6, SUBY + SUBLH + asc + desc - 4)

STATFONT = fit_font(SERIF, ["3,000+"], 800, 300)
STAT_Y, YR_Y = 640, 970
stat_mask, stat_boxes = layer_lines(["3,000+"], STATFONT, W / 2, STAT_Y, 0)
YRFONT = fit_font(SANS, ["YEARS OLD"], 700, 120)
yr_mask, yr_boxes = layer_lines(["YEARS OLD"], YRFONT, W / 2, YR_Y, 0, tracking=16)
sa, sd = STATFONT.getmetrics()
ELL = (W / 2, STAT_Y + sa * .62, stat_boxes[0][2] / 2 + 70, sa * .5 + 60)
yr_asc, yr_desc = YRFONT.getmetrics()
UL = (yr_boxes[0][0] - 6, yr_boxes[0][0] + yr_boxes[0][2] + 6, YR_Y + yr_asc + yr_desc + 4)

WMFONT = ImageFont.truetype(SERIF, 34)
_wm = Image.new("L", (W, H), 0)
_d = ImageDraw.Draw(_wm)
_d.text((W - 110 - _d.textlength("CuriousMindsFeed", font=WMFONT), 300), "CuriousMindsFeed", font=WMFONT, fill=255)  # O2 watermark
WM = np.asarray(_wm, np.float32) / 255

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
RN = np.sqrt((xx - W / 2) ** 2 + (yy - H / 2) ** 2) / (0.5 * math.hypot(W, H))
VIG = (1 - 0.12 * RN ** 2)[..., None]
EDGE = ease_io((RN - 0.6) / 0.4)[..., None]
CA = {}
for ch, s in [(0, 1.0035), (2, .9965)]:
    CA[ch] = ((xx - W / 2) / s + W / 2, (yy - H / 2) / s + H / 2)


def place(sprite, cx, cy, scale, rot):
    h, w = sprite.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, scale)
    M[0, 2] += cx - w / 2
    M[1, 2] += cy - h / 2
    return cv2.warpAffine(sprite, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def comp_sprite(img, sp):
    return img * (1 - sp[..., 3:4]) + sp[..., :3]


def scale_layer(layer, s, cx, cy):
    M = cv2.getRotationMatrix2D((cx, cy), 0, s)
    return cv2.warpAffine(layer, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


# ---------------------------------------------------------------- frame
def dark_frame(f):
    img = np.full((H, W, 3), DARK, np.float32)
    r = R("dust", f // 2)                                           # specks refresh at 12 fps
    for _ in range(int(r.integers(5, 13))):
        x, y = int(r.integers(0, W)), int(r.integers(0, H))
        cv2.circle(img, (x, y), int(r.integers(1, 3)), float(r.choice([20, 40])), -1, cv2.LINE_AA)
    wm_a = float(ease_io((f - 2) / 4)) if f < 6 else 1.0            # watermark fades in out of the dip
    img = img * (1 - WM[..., None] * .85 * wm_a) + 235 * WM[..., None] * .85 * wm_a
    n = R("grain", f).standard_normal((H, W)).astype(np.float32)
    return img + n[..., None] * 1.5


def paper_frame(f):
    hf = f // 2 * 2
    in1 = S1[0] <= f <= S1[1]
    t0 = S1[0] if in1 else S2[0]
    t1 = S1[1] if in1 else S2[1]
    img = PAPERS[(f // 10) % 3].copy()                              # T8
    if in1:
        bk = BACK[int(R("bk", hf // 2).integers(0, 4))]
        img = comp_sprite(img, place(bk, 540, 840, 1.0, 2.5))
        e = ease_out((hf - S1[0]) / 8)
        t = (hf - S1[0]) / (S1[1] - S1[0])
        jar = JAR[int(R("jv", hf // 2).integers(0, 4))]             # re-seeded each held drawing (T7)
        img = comp_sprite(img, place(jar, 540, 840 + 120 * (1 - e), (0.88 + 0.12 * e) * (1 + .04 * t), -3 + 1.6 * t))
    else:
        pop = ease_out((hf - S2[0]) / 6)
        s = .92 + .08 * pop
        a = scale_layer(stat_mask, s, W / 2, STAT_Y + 150)
        ref = np.roll(a, (-1, 2), (0, 1))                           # T14: ~2 px misregistration
        img = multiply(img, ref, RED, .45)
        img = over_ink(img, a)
        img = over_ink(img, scale_layer(yr_mask, s, W / 2, YR_Y + 60))
        img = multiply(img, marker_ellipse(*ELL, ease_io((hf - 66) / 10), hf, 1), RED, .92)
        img = multiply(img, marker_line(UL[0], UL[1], UL[2], ease_io((hf - 78) / 6), hf, 2), RED, .92)
    # camera drift (continuous, per shot)
    tt = (f - t0) / max(1, t1 - t0)
    M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, 1 + .022 * tt)
    M[0, 2] += 7 * tt
    img = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    # caption: lags the picture (O3), highlighter draw-on (T18), ink text
    if in1 and f >= 10:
        img = multiply(img, highlight_mask(*HL1, ease_io((hf - 22) / 8), 1, hf), YEL, .95)
        img = over_ink(img, sub1_mask)
    if (not in1) and f >= 64:
        img = multiply(img, highlight_mask(*HL2, ease_io((hf - 92) / 8), 2, hf), YEL, .95)
        img = over_ink(img, sub2_mask)
    # lens on shot 2 only (T12/T15)
    if not in1:
        for ch in (0, 2):
            img[..., ch] = cv2.remap(img[..., ch], CA[ch][0], CA[ch][1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        img = img * (1 - EDGE * .8) + cv2.GaussianBlur(img, (0, 0), 3.5) * (EDGE * .8)
    img = img * VIG
    img = img * (1 - WM[..., None] * .55) + INK * WM[..., None] * .55   # dark watermark on paper
    n = R("grain", f).standard_normal((H, W)).astype(np.float32)        # T10: grain last, fresh every frame
    n = cv2.GaussianBlur(n, (0, 0), .6)
    n /= n.std()
    return img + n[..., None] * 6.0


def render(f):
    if DIP_A[0] <= f <= DIP_A[1] or DIP_B[0] <= f <= DIP_B[1]:
        img = dark_frame(f)
    else:
        img = paper_frame(f)
    return np.clip(img, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- audio
SR = 48000


def build_audio(path):
    n = int(SR * N / FPS)
    L, Rt = np.zeros(n, np.float32), np.zeros(n, np.float32)

    def add(sig, t0, gain=1.0, pan=0.0):
        i = max(0, int(t0 * SR))
        sig = sig[: max(0, n - i)] * gain
        L[i:i + len(sig)] += sig * (1 - max(pan, 0))
        Rt[i:i + len(sig)] += sig * (1 + min(pan, 0))

    def bp(x, lo, hi):
        return signal.sosfilt(signal.butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)

    rng = R("audio")
    t = lambda d: np.arange(int(d * SR)) / SR

    def pluck(freq, dur=.55):
        tt = t(dur)
        s = sum(a * np.sin(2 * np.pi * freq * h * tt) for h, a in [(1, 1), (2, .4), (3.01, .2), (4.2, .08)])
        return (s * np.exp(-tt / .16) * (1 - np.exp(-tt / .004))).astype(np.float32)

    def pad(freqs, dur):
        tt = t(dur)
        s = sum(np.sin(2 * np.pi * f_ * tt + i) for i, f_ in enumerate(freqs)) / len(freqs)
        env = np.minimum(1, tt / .4) * np.minimum(1, (dur - tt) / .3)
        return (s * env * (1 + .08 * np.sin(2 * np.pi * .5 * tt))).astype(np.float32)

    music_L, music_R = L.copy(), Rt.copy()
    L[:], Rt[:] = 0, 0
    # section A (C pentatonic) until the dip, drops out after the claim (S3); section B (F pentatonic) after the hit
    notesA = [523.25, 659.25, 783.99, 880.0, 783.99, 659.25]
    notesB = [698.46, 880.0, 1046.5, 1174.7, 1046.5, 880.0]
    step = .3
    for i, tm in enumerate(np.arange(.25, 2.1, step)):
        add(pluck(notesA[i % 6]), tm + rng.normal(0, .008), .55 * rng.uniform(.7, 1), pan=(-.3 if i % 2 else .3))
    add(pad([130.8, 196.0, 329.6], 2.3), 0, .35)
    for i, tm in enumerate(np.arange(2.45, 4.95, step)):
        add(pluck(notesB[i % 6]), tm + rng.normal(0, .008), .6 * rng.uniform(.7, 1), pan=(-.3 if i % 2 else .3))
    for tm in np.arange(2.42, 4.9, .6):
        tt = t(.35)
        add((np.sin(2 * np.pi * 87.3 * tt) * np.exp(-tt / .18)).astype(np.float32), tm, .55)
    add(pad([174.6, 261.6, 440.0], 2.6), 2.42, .35)
    m = L + 0
    mL, mR = L.copy(), Rt.copy()
    # reverb on the music bus
    ir = (rng.standard_normal(int(.8 * SR)) * np.exp(-t(.8) / .22)).astype(np.float32)
    wetL = signal.fftconvolve(mL, ir)[:n] * .05
    wetR = signal.fftconvolve(mR, ir)[:n] * .05
    mL, mR = mL * .9 + wetL, mR * .9 + wetR
    L[:], Rt[:] = 0, 0

    # SFX (S8-S10): few, one family, landing 1-3 frames early
    f = lambda fr: fr / FPS
    nz = lambda d: rng.standard_normal(int(d * SR)).astype(np.float32)
    # paper rustle at jar enter (f6, 2 frames early)
    d = .3
    r_ = bp(nz(d), 1500, 7000) * np.abs(signal.sosfilt(signal.butter(2, 60, "low", fs=SR, output="sos"), nz(d))) * 40
    add((r_ * np.exp(-t(d) / .12)).astype(np.float32), f(6 - 2), .16)
    # tick at highlighter 1 (f22, 1 frame early) and 2 (f92)
    for fr in (22, 92):
        tt = t(.05)
        add((np.sin(2 * np.pi * 2100 * tt) * np.exp(-tt / .008)).astype(np.float32), f(fr - 1), .22)
    # whoosh into the dip (lands f54, starts 3 frames early) + low hit with shot 2 (f58, 1 frame early)
    d = .3
    tt = t(d)
    lo = bp(nz(d), 300, 1200) * np.exp(-((tt - .35 * d) / (.22 * d)) ** 2)
    hi = bp(nz(d), 1500, 5500) * np.exp(-((tt - .78 * d) / (.18 * d)) ** 2)
    add(((lo + hi) * 1.0).astype(np.float32), f(54 - 3), .28)
    tt = t(.4)
    hit = np.sin(2 * np.pi * np.cumsum(np.linspace(95, 45, len(tt))) / SR) * np.exp(-tt / .16)
    add(hit.astype(np.float32), f(58 - 1), .55)
    # marker scribble over the circle draw-on (f66..76) and a swish for the underline (f78)
    d = .42
    sc = bp(nz(d), 2500, 7000) * (np.abs(bp(nz(d), 20, 60)) * 25 + .2)
    add((sc * np.minimum(1, t(d) / .03) * np.minimum(1, (d - t(d)) / .05)).astype(np.float32), f(66 - 1), .09)
    d = .15
    sw = bp(nz(d), 2000, 6000) * np.sin(np.pi * t(d) / d)
    add(sw.astype(np.float32), f(78 - 1), .1)

    sL, sR = L.copy(), Rt.copy()
    out = np.stack([mL * .5 + sL, mR * .5 + sR], 1)
    out *= np.minimum(1, (n - np.arange(n)) / (.15 * SR))[:, None]
    out = np.clip(out, -1, 1)
    import wave
    w = wave.open(path, "wb")
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
    w.close()


def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    if "--stills" in sys.argv:
        for s in sys.argv[sys.argv.index("--stills") + 1].split(","):
            cv2.imwrite(os.path.join(outdir, f"still_{int(s):03d}.png"), cv2.cvtColor(render(int(s)), cv2.COLOR_RGB2BGR))
        return
    wav = os.path.join(outdir, "audio.wav")
    build_audio(wav)
    out = os.path.join(outdir, "cmf_test_clip_01.mp4")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
                          "-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{N / FPS}",
                          "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for f in range(N):
        p.stdin.write(render(f).tobytes())
        if f % 20 == 0:
            print("frame", f, flush=True)
    p.stdin.close()
    p.wait()
    print("wrote", out)


if __name__ == "__main__":
    main()
