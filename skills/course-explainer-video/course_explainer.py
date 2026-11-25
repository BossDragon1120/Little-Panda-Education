#!/usr/bin/env python3
"""Course Explainer video renderer (Little Panda Education house look).

Frosted text panel over a soft dusk-gradient background, 1080x1920, 30 fps, silent for voiceover.
This file holds the look and the drawing helpers. Each video is a small Python file that defines
META, DUR and SCENES (see examples/). Usage:

  python3 course_explainer.py examples/agentic-ai-m5-autonomous-agents.py stills 6 18 32
  python3 course_explainer.py examples/agentic-ai-m5-autonomous-agents.py render

Env: FONT_DIR (default ~/dd-fonts), BG=/path/photo.jpg to swap the generated background for a photo.
"""
import sys, os, math, random, subprocess, importlib.util
from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FD = os.environ.get('FONT_DIR', os.path.expanduser('~/dd-fonts'))
PX0, PY0, PX1, PY1 = 40, 395, 984, 1445      # frosted panel
X0, X1 = 84, 940                             # content column
INK = (18, 26, 44); DIM = (92, 102, 122); ACC = (79, 70, 229); ACC2 = (236, 120, 40)
GOOD = (16, 150, 105); RED = (214, 60, 60); LINE = (196, 202, 214); CARD = (255, 255, 255); WHITE = (255, 255, 255)

@lru_cache(None)
def D(s): return ImageFont.truetype(f'{FD}/fontsource-anton/files/anton-latin-400-normal.woff', s)
@lru_cache(None)
def M(s, w=700): return ImageFont.truetype(f'{FD}/fontsource-jetbrains-mono/files/jetbrains-mono-latin-{w}-normal.woff', s)
@lru_cache(None)
def S(s, w=700): return ImageFont.truetype(f'{FD}/fontsource-inter/files/inter-latin-{w}-normal.woff', s)

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def prog(t, s, d=0.45): return ease((t - s) / d)
def tw(text, f): return f.getlength(text)
def fit(fn, text, maxw, size):
    while size > 18 and tw(text, fn(size)) > maxw: size -= 2
    return fn(size)
def wrap(text, f, maxw):
    out, cur = [], ''
    for w in text.split(' '):
        tt = (cur + ' ' + w).strip()
        if tw(tt, f) <= maxw: cur = tt
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out
def C(col, a): return col + (int(255 * clamp(a)),)

# ---------- static layers ----------
def make_bg():
    p = os.environ.get('BG')
    if p and os.path.exists(p):
        im = Image.open(p).convert('RGB'); s = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1)); l = (im.width - W) // 2; tp = (im.height - H) // 2
        return im.crop((l, tp, l + W, tp + H))
    # placeholder "photo": warm dusk gradient + soft bokeh
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    top, bot = (40, 52, 98), (236, 140, 96)
    for y in range(H):
        k = y / H; d.line((0, y, W, y), fill=tuple(int(top[i] + (bot[i] - top[i]) * k ** 1.3) for i in range(3)))
    rnd = random.Random(7); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    for _ in range(38):
        r = rnd.randint(40, 170); x = rnd.randint(-50, W + 50); y = rnd.randint(0, H)
        col = rnd.choice([(255, 214, 150), (255, 170, 120), (150, 180, 255), (255, 240, 210)])
        ld.ellipse((x - r, y - r, x + r, y + r), fill=col + (rnd.randint(40, 95),))
    lay = lay.filter(ImageFilter.GaussianBlur(18)); im = Image.alpha_composite(im.convert('RGBA'), lay)
    return im.convert('RGB')

def build_static():
    global BASE
    bg = make_bg()
    # darken top band so chrome reads on any photo
    shade = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shade)
    for y in range(0, 400): sd.line((0, y, W, y), fill=(0, 0, 0, int(110 * (1 - y / 400))))
    base = Image.alpha_composite(bg.convert('RGBA'), shade)
    # frosted panel: blurred photo + white wash, rounded, soft shadow
    region = bg.crop((PX0, PY0, PX1, PY1)).filter(ImageFilter.GaussianBlur(28))
    wash = Image.new('RGBA', region.size, (250, 250, 253, 214))
    frost = Image.alpha_composite(region.convert('RGBA'), wash)
    mask = Image.new('L', region.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, region.width - 1, region.height - 1), 44, fill=255)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((PX0, PY0 + 14, PX1, PY1 + 14), 44, fill=(0, 0, 0, 70))
    base = Image.alpha_composite(base, sh.filter(ImageFilter.GaussianBlur(20)))
    base.paste(frost, (PX0, PY0), mask)
    ImageDraw.Draw(base).rounded_rectangle((PX0, PY0, PX1, PY1), 44, outline=(255, 255, 255, 255), width=3)
    BASE = base

# ---------- drawing helpers (all on an RGBA overlay; alpha = fade) ----------
def T(d, xy, text, f, col, a=1, anchor='la'):
    if a > 0: d.text(xy, text, font=f, fill=C(col, a), anchor=anchor)
def rise(d, t, s, xy, text, f, col, anchor='la', dist=26):
    a = prog(t, s); T(d, (xy[0], xy[1] + (1 - a) * dist), text, f, col, a, anchor)
def para(d, t, s, x, y, text, f, col, maxw, lh, stagger=0.08):
    ls = wrap(text, f, maxw)
    for i, ln in enumerate(ls): rise(d, t, s + i * stagger, (x, y + i * lh), ln, f, col)
    return y + len(ls) * lh
def box(d, xy, a, fill=CARD, outline=LINE, width=3, r=18):
    if a > 0: d.rounded_rectangle(xy, r, fill=C(fill, a * 0.92) if fill else None, outline=C(outline, a) if outline else None, width=width)
def chip(d, x, y, text, col, a=1, solid=False, f=None):
    f = f or M(24); w = tw(text, f) + 30
    if a > 0:
        d.rounded_rectangle((x, y, x + w, y + 46), 23, fill=C(col, a) if solid else C(WHITE, a * 0.9), outline=C(col, a), width=3)
        T(d, (x + w / 2, y + 23), text, f, WHITE if solid else col, a, 'mm')
    return x + w
def label(d, t, text): rise(d, t, 0.05, (X0, 440), text, M(28, 800), ACC, dist=12)
def title(d, t, text, y=486, size=96, col=INK): rise(d, t, 0.15, (X0, y), text, fit(D, text, X1 - X0, size), col)
def check(d, x, y, col, a, s=1.0):
    if a > 0: d.line((x, y, x + 12 * s, y + 13 * s, x + 34 * s, y - 14 * s), fill=C(col, a), width=int(7 * s), joint='curve')
def arrow(d, x1, y1, x2, y2, col, a, w=4, head=14):
    if a <= 0: return
    d.line((x1, y1, x2, y2), fill=C(col, a), width=w); ang = math.atan2(y2 - y1, x2 - x1)
    pts = [(x2, y2), (x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45)), (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))]
    d.polygon(pts, fill=C(col, a))
def node(d, cx, cy, r, text, col, a, fill=CARD, f=None):
    if a <= 0: return
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=C(fill, a), outline=C(col, a), width=4)
    T(d, (cx, cy), text, f or D(int(r * 0.9)), col if fill == CARD else WHITE, a, 'mm')


# ---------- fixed chrome: series name, course + module, progress bar ----------
VIDEO = None  # the loaded video module
def chrome(d, gt, si, lt):
    meta, dur = VIDEO.META, VIDEO.DUR
    T(d, (X0 - 20, 238), meta.get('series', 'COURSE EXPLAINER'), M(30, 800), WHITE, 1, 'lm')
    T(d, (X1 + 20, 238), meta['course_tag'], M(26, 700), (225, 228, 240), 1, 'rm')
    n = len(dur); gap = 8; sw = (X1 - X0 + 40 - gap * (n - 1)) / n
    for i in range(n):
        x = X0 - 20 + i * (sw + gap); d.rounded_rectangle((x, 292, x + sw, 299), 3, fill=(255, 255, 255, 90))
        f = 1 if i < si else (clamp(lt / dur[si]) if i == si else 0)
        if f > 0: d.rounded_rectangle((x, 292, x + max(sw * f, 7), 299), 3, fill=(255, 255, 255, 255))

# ---------- render loop ----------
def bounds():
    out, s = [], 0
    for dd in VIDEO.DUR: out.append((s, s + dd)); s += dd
    return out

def frame(gt):
    B = bounds()
    for si, (a, b) in enumerate(B):
        if a <= gt < b or si == len(B) - 1: break
    lt = gt - B[si][0]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    chrome(d, gt, si, lt); VIDEO.SCENES[si](d, lt)
    img = Image.alpha_composite(BASE, lay)
    if si > 0 and lt < 0.2: img = Image.blend(img, BASE, 1 - lt / 0.2)  # short fade between scenes
    return img.convert('RGB')

def load(path):
    global VIDEO
    sys.modules.setdefault('course_explainer', sys.modules[__name__])
    spec = importlib.util.spec_from_file_location('ce_video', path); VIDEO = importlib.util.module_from_spec(spec); spec.loader.exec_module(VIDEO)
    assert len(VIDEO.DUR) == len(VIDEO.SCENES), 'DUR and SCENES must have the same length'
    build_static()

def render_scene(args):
    si, outdir = args; a, b = bounds()[si]; out = f'{outdir}/scene{si}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(int(round((b - a) * FPS))): p.stdin.write(frame(a + i / FPS).tobytes())
    p.stdin.close(); assert p.wait() == 0, f'scene {si} failed'; return out

if __name__ == '__main__':
    load(sys.argv[1]); mode = sys.argv[2]
    out = os.path.abspath(VIDEO.META.get('output', 'course-explainer.mp4')); outdir = os.path.join(os.path.dirname(out), 'ce_scenes')
    os.makedirs(outdir, exist_ok=True)
    if mode == 'stills':
        for ts in sys.argv[3:]:
            p = f'{outdir}/still_{ts}.png'; frame(float(ts)).save(p); print(p)
    else:
        with ProcessPoolExecutor() as ex: files = list(ex.map(render_scene, [(i, outdir) for i in range(len(VIDEO.SCENES))]))
        lst = f'{outdir}/list.txt'; open(lst, 'w').write(''.join(f"file '{f}'\n" for f in files))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], check=True); print(out)
