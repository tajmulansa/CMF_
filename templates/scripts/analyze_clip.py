#!/usr/bin/env python3
"""Analyse a reference clip frame by frame.

Usage: python3 -I analyze_clip.py <video> <slug> <repo_root>
Needs: ffmpeg, ffprobe, python3 with opencv-python and numpy.

Writes:
  <repo>/references/frames/<slug>/u_<frame>_<time>.jpg   unique frames (holds collapsed), 960 px wide
  <repo>/references/sheets/<slug>/sheet_01.jpg            contact sheet of unique frames with timestamps
  <repo>/references/vox/<slug>/analysis.json              fps, hold pattern, dips, shots, audio levels
Prints a short summary.
"""
import json, os, re, subprocess, sys
import cv2
import numpy as np

HOLD_EPS = 0.05      # mean abs diff below this = duplicate frame (a hold)
DIP_LUM = 45         # mean luminance below this ...
DIP_STD = 8          # ... and low spatial std = a dip-to-dark frame


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stderr


def main(video, slug, root):
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames, small, diffs, lums, stds = [], [], [], [], []
    prev = None
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(cv2.resize(fr, (192, 108)), cv2.COLOR_BGR2GRAY).astype(float)
        lums.append(g.mean())
        stds.append(g[:, :130].std())   # left 2/3 only: ignores a corner watermark/logo
        diffs.append(0.0 if prev is None else float(np.abs(g - prev).mean()))
        prev = g
        frames.append(cv2.resize(fr, (960, int(960 * fr.shape[0] / fr.shape[1]))))
    n = len(frames)
    d = np.array(diffs)

    # hold pattern: gaps between changed frames (2,3,2,3 at 60 fps = 24 fps source)
    changed = [i for i in range(1, n) if d[i] >= HOLD_EPS]
    gaps = np.diff(changed).tolist() if len(changed) > 1 else []
    gap_hist = {}
    for g in gaps:
        gap_hist[g] = gap_hist.get(g, 0) + 1
    steady = [g for g in gaps if g in (2, 3)]
    if len(steady) >= 6:                      # 2,3,2,3 pulldown pattern -> source rate
        content_fps = round(fps / float(np.mean(steady)), 1)
    else:
        content_fps = round(fps / float(np.mean(gaps)), 1) if gaps else None

    # dips to dark
    dark = [lums[i] < DIP_LUM and stds[i] < DIP_STD for i in range(n)]
    dips, i = [], 0
    while i < n:
        if dark[i]:
            j = i
            while j + 1 < n and dark[j + 1]:
                j += 1
            dips.append({"start": i, "end": j, "frames": j - i + 1, "seconds": round((j - i + 1) / fps, 3),
                         "mean_gray": round(float(np.mean(lums[i:j + 1])), 1)})
            i = j + 1
        else:
            i += 1

    # hard cuts outside dips (big jump, neither frame dark)
    thr = max(12.0, float(d.mean() + 4 * d.std()))
    cuts = [i for i in range(1, n) if d[i] > thr and not dark[i] and not dark[i - 1]]

    # shots = runs of non-dark frames, split at hard cuts
    bounds = sorted(set(cuts))
    shots, start = [], None
    for i in range(n):
        if not dark[i] and start is None:
            start = i
        end_run = dark[i] or i == n - 1 or (i + 1) in bounds
        if start is not None and end_run:
            last = i if not dark[i] else i - 1
            shots.append({"start": start, "end": last, "seconds": round((last - start + 1) / fps, 3)})
            start = None

    # unique frames
    fdir = os.path.join(root, "references", "frames", slug)
    os.makedirs(fdir, exist_ok=True)
    uniq = [0] + changed
    for k in uniq:
        cv2.imwrite(os.path.join(fdir, f"u_{k:05d}_{k / fps:06.3f}s.jpg"), frames[k], [cv2.IMWRITE_JPEG_QUALITY, 88])

    # contact sheet
    cols, tw = 6, 320
    ims = []
    for k in uniq:
        im = cv2.resize(frames[k], (tw, int(tw * frames[k].shape[0] / frames[k].shape[1])))
        cv2.putText(im, f"{k} {k / fps:.2f}s", (6, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
        ims.append(im)
    while len(ims) % cols:
        ims.append(np.zeros_like(ims[0]))
    sheet = np.vstack([np.hstack(ims[r:r + cols]) for r in range(0, len(ims), cols)])
    sdir = os.path.join(root, "references", "sheets", slug)
    os.makedirs(sdir, exist_ok=True)
    cv2.imwrite(os.path.join(sdir, "sheet_01.jpg"), sheet, [cv2.IMWRITE_JPEG_QUALITY, 82])

    # audio
    out = sh(["ffmpeg", "-hide_banner", "-i", video, "-af", "ebur128=peak=true", "-f", "null", "-"])
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", out)
    wav = os.path.join(root, ".tmp_audio.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-ac", "1", "-ar", "16000", wav])
    rms100 = []
    try:
        import wave
        w = wave.open(wav)
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        rms100 = [round(20 * np.log10(np.sqrt(np.mean(x[i:i + 1600] ** 2)) + 1e-9)) for i in range(0, len(x), 1600)]
        os.remove(wav)
    except Exception:
        pass

    res = {"video": os.path.basename(video), "fps": fps, "frames": n, "duration_s": round(n / fps, 3),
           "hold_gap_histogram": gap_hist, "content_fps_estimate": content_fps,
           "dips": dips, "hard_cuts_frames": cuts, "shots": shots,
           "integrated_lufs": float(lufs[-1]) if lufs else None,
           "true_peak_dbfs": float(tp[-1]) if tp else None, "rms_db_per_100ms": rms100}
    adir = os.path.join(root, "references", "vox", slug)
    os.makedirs(adir, exist_ok=True)
    with open(os.path.join(adir, "analysis.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "rms_db_per_100ms"}, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
