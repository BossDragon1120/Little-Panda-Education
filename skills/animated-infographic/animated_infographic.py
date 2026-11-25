#!/usr/bin/env python3
"""Animated infographic renderer (Little Panda Education house look).

One vertical 1080x1920 infographic: a see-through frosted panel, centered top to bottom over a photo,
whose content builds in, holds, and loops. Output is a short silent MP4 loop (TikTok post), a PNG of
the fully built frame (cover or photo post), and caption.md with the title and hashtags.

Each infographic is one small Python file that defines META, PANEL_H and draw(d, t).
See examples/silicon-vs-optics.py. Usage:

  python3 animated_infographic.py examples/<file>.py stills 1 3 6      # frames at those seconds
  python3 animated_infographic.py examples/<file>.py safe              # built frame with TikTok no-go zones drawn on
  python3 animated_infographic.py examples/<file>.py render            # MP4 loop + PNG + caption.md

Env: FONT_DIR (default ~/dd-fonts), BG=photo and OUT=file.mp4 override META. META sets the photo and how it is cropped (see SKILL.md).
"""
import sys, os, math, subprocess, importlib.util
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FD = os.environ.get('FONT_DIR', os.path.expanduser('~/dd-fonts'))
X0, X1 = 84, 940                      # content column: clear of TikTok's right button rail
PX0, PX1 = 40, 984                    # frosted panel left/right
CAPTION_Y = 1550                      # TikTok caption + username start around here
RAIL_X = 960                          # TikTok like/comment/share rail starts around here (y 900-1650)
INK = (18, 26, 44); DIM = (92, 102, 122); ACC = (79, 70, 229); ACC2 = (236, 120, 40)
GOOD = (16, 150, 105); RED = (214, 60, 60); LINE = (196, 202, 214); WHITE = (255, 255, 255)

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

# ---------- layout: the panel is always centered top to bottom ----------
SPEC = None
def panel():
    h = SPEC.PANEL_H; top = (H - h) // 2
    return PX0, top, PX1, top + h
def top(): return panel()[1]      # use as the y origin when laying out a spec

# ---------- static layer: photo (cropped to hide clutter) + frosted see-through panel ----------
def make_bg():
    m = SPEC.META; im = Image.open(os.path.expanduser(os.environ.get('BG', m['bg']))).convert('RGB')
    keep = m.get('bg_keep', 1.0)                    # keep the top fraction of the photo (crops clutter at the bottom)
    if keep < 1: im = im.crop((0, 0, im.width, int(im.height * keep)))
    zoom = m.get('bg_zoom', 1.0)                    # >1 zooms in around the center (crops clutter at the edges)
    s = max(W / im.width, H / im.height) * zoom
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1))
    l = (im.width - W) // 2 + m.get('bg_dx', 0); tp = (im.height - H) // 2 - m.get('bg_dy', 0)
    l = clamp(l, 0, im.width - W); tp = clamp(tp, 0, im.height - H)
    return im.crop((int(l), int(tp), int(l) + W, int(tp) + H))

def build_static():
    global BASE
    m = SPEC.META; bg = make_bg(); P = panel()
    shade = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shade)
    for y in range(0, P[1]): sd.line((0, y, W, y), fill=(0, 0, 0, int(120 * (1 - y / P[1]))))   # chrome reads on any photo
    base = Image.alpha_composite(bg.convert('RGBA'), shade)
    region = bg.crop(P).filter(ImageFilter.GaussianBlur(m.get('blur', 12)))
    frost = Image.alpha_composite(region.convert('RGBA'), Image.new('RGBA', region.size, (250, 250, 253, m.get('wash', 120))))
    mask = Image.new('L', region.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, region.width - 1, region.height - 1), 44, fill=255)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((P[0], P[1] + 14, P[2], P[3] + 14), 44, fill=(0, 0, 0, 70))
    base = Image.alpha_composite(base, sh.filter(ImageFilter.GaussianBlur(20)))
    base.paste(frost, P[:2], mask)
    ImageDraw.Draw(base).rounded_rectangle(P, 44, outline=WHITE, width=3)
    BASE = base

# ---------- drawing helpers (on an RGBA overlay; a = fade) ----------
CA = 200   # card opacity: cards stay a little see-through like the panel
def T(d, xy, text, f, col, a=1, anchor='la'):
    if a > 0: d.text(xy, text, font=f, fill=C(col, a), anchor=anchor)
def rise(d, t, s, xy, text, f, col, anchor='la', dist=24):
    a = prog(t, s); T(d, (xy[0], xy[1] + (1 - a) * dist), text, f, col, a, anchor); return a
def para(d, t, s, x, y, text, f, col, maxw, lh, stagger=0.08):
    ls = wrap(text, f, maxw)
    for i, ln in enumerate(ls): rise(d, t, s + i * stagger, (x, y + i * lh), ln, f, col)
    return y + len(ls) * lh
def card(d, xy, a, fill=WHITE, outline=LINE, width=3, r=20, op=None):
    if a > 0: d.rounded_rectangle(xy, r, fill=fill + (int((op or CA) * clamp(a)),) if fill else None, outline=C(outline, a) if outline else None, width=width)
def chip(d, x, y, text, col, a=1, solid=True, f=None, h=44):
    f = f or M(24, 800); w = tw(text, f) + 36
    if a > 0:
        d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=C(col, a) if solid else C(WHITE, a * 0.85), outline=C(col, a), width=3)
        T(d, (x + w / 2, y + h / 2), text, f, WHITE if solid else col, a, 'mm')
    return x + w
def arrow(d, x1, y1, x2, y2, col, a, w=4, head=14):
    if a <= 0: return
    d.line((x1, y1, x2, y2), fill=C(col, a), width=w); ang = math.atan2(y2 - y1, x2 - x1)
    d.polygon([(x2, y2), (x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45)),
               (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))], fill=C(col, a))
def check(d, x, y, col, a, s=1.0):
    if a > 0: d.line((x, y, x + 12 * s, y + 13 * s, x + 34 * s, y - 14 * s), fill=C(col, a), width=int(7 * s), joint='curve')
def cyc(t, period, phase=0.0):
    """0..1 sawtooth for continuous motion. Pick periods that divide META['loop'] so the loop is seamless."""
    return ((t / period) + phase) % 1.0

# ---------- reusable blocks ----------
def headline(d, t, y, line1, line2, sub=None, s=0.1):
    """Two-line Anton takeaway (second line in accent) and one plain sentence. Returns the y below it."""
    rise(d, t, s, (X0, y), line1, fit(D, line1, X1 - X0, 104), INK)
    rise(d, t, s + 0.25, (X0, y + 108), line2, fit(D, line2, X1 - X0, 104), ACC)
    y += 244
    if sub: y = para(d, t, s + 0.55, X0, y, sub, S(28, 700), INK, X1 - X0, 38) + 6
    return y
def rows(d, t, y, items, s=1.0, h=124, gap=10, stagger=0.35):
    """Toolbox-style rows: (name, tag, plain line, seen-in, icon_fn(d, t, a, cx, cy, col), col). Returns y below."""
    for i, (name, tag, good, seen, icon, col) in enumerate(items):
        a = prog(t, s + i * stagger); dy = (1 - a) * 30; y0 = y + dy
        card(d, (X0, y0, X1, y0 + h), a)
        if a > 0: d.ellipse((X0 + 16, y0 + 17, X0 + 106, y0 + 107), fill=(243, 244, 248, int(235 * a)))
        icon(d, t, a, X0 + 61, y0 + 62, col)
        tx = X0 + 126
        T(d, (tx, y0 + 10), name, D(40), INK, a); T(d, (tx + tw(name, D(40)) + 16, y0 + 26), tag, M(18, 700), DIM, a)
        T(d, (tx, y0 + 56), good, S(26, 600), INK, a)
        T(d, (tx, y0 + 90), 'SEEN IN', M(20, 800), col, a); T(d, (tx + 100, y0 + 87), seen, S(26, 700), INK, a)
        y += h + gap
    return y
def versus(d, t, y, left, right, items, s=1.0, rh=96, stagger=0.3):
    """Two-column comparison. left/right = (header, color). items = (label, left text, right text). Returns y below."""
    cx = (X0 + X1) // 2 + 70; lw = 150
    a = prog(t, s)
    for (hdr, col), x0, x1 in ((left, X0 + lw, cx - 6), (right, cx + 6, X1)):
        card(d, (x0, y, x1, y + 52), a, fill=col, outline=None, r=16, op=235)
        T(d, ((x0 + x1) / 2, y + 26), hdr, fit(lambda z: M(z, 800), hdr, x1 - x0 - 20, 24), WHITE, a, 'mm')
    y += 64
    for i, (lab, lt, rt) in enumerate(items):
        a = prog(t, s + 0.3 + i * stagger); y0 = y + (1 - a) * 24
        card(d, (X0, y0, X1, y0 + rh - 10), a, r=16)
        T(d, (X0 + 16, y0 + (rh - 10) / 2), lab, fit(lambda z: M(z, 800), lab, lw - 24, 20), DIM, a, 'lm')
        for txt, x0, x1, col in ((lt, X0 + lw, cx - 6, left[1]), (rt, cx + 6, X1, right[1])):
            f = S(25, 700); ls = wrap(txt, f, x1 - x0 - 28)[:2]; lh = 32; ty = y0 + (rh - 10) / 2 - (len(ls) * lh) / 2
            for k, ln in enumerate(ls): T(d, (x0 + 14, ty + k * lh), ln, f, INK, a)
        if a > 0: d.line((cx, y0 + 12, cx, y0 + rh - 22), fill=C(LINE, a), width=3)
        y += rh
    return y
def punchline(d, t, y, text, s, col=INK, size=46):
    rise(d, t, s, (X0, y), text, fit(D, text, X1 - X0, size), col); return y + size + 14

# ---------- fixed chrome above the panel ----------
def chrome(d):
    m = SPEC.META; y = top() - 52
    T(d, (X0 - 20, y), m.get('series', 'AI VOCAB'), M(30, 800), WHITE, 1, 'lm')
    T(d, (X1 + 20, y), m['topic_tag'], fit(lambda z: M(z, 700), m['topic_tag'], 520, 26), (225, 228, 240), 1, 'rm')

# ---------- frames ----------
def frame(t):
    loop = SPEC.META.get('loop', 12.0); out_fade = SPEC.META.get('fade_out', 0.6)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    SPEC.draw(d, t)
    k = clamp((loop - t) / out_fade) if t > loop - out_fade else 1.0   # content fades out, then builds in again
    if k < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * k)))
    chr_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); chrome(ImageDraw.Draw(chr_))
    return Image.alpha_composite(Image.alpha_composite(BASE, chr_), lay).convert('RGB')

def safe_overlay(img):
    """Shade the zones TikTok covers so you can see what they hide."""
    o = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    d.rectangle((0, CAPTION_Y, W, H), fill=(255, 0, 0, 70)); d.rectangle((RAIL_X, 900, W, 1650), fill=(255, 0, 0, 70))
    d.rectangle((0, 0, W, 150), fill=(255, 0, 0, 50))
    return Image.alpha_composite(img.convert('RGBA'), o).convert('RGB')

def load(path):
    global SPEC
    sys.modules.setdefault('animated_infographic', sys.modules[__name__])
    spec = importlib.util.spec_from_file_location('ai_spec', path); SPEC = importlib.util.module_from_spec(spec); spec.loader.exec_module(SPEC)
    P = panel()
    if P[3] > CAPTION_Y: print(f'note: panel bottom y={P[3]} reaches into TikTok caption area (starts ~{CAPTION_Y}); keep the last line short or check in the app preview')
    build_static()

def caption_md(png, mp4):
    m = SPEC.META
    return (f"# {m['title']}\n\n**Caption:** {m['caption']}\n\n**Hashtags:** {' '.join(m['hashtags'])}\n\n"
            f"**Files:** `{os.path.basename(mp4)}` (loop, post as video) · `{os.path.basename(png)}` (built frame: cover or photo post)\n\n"
            + (f"**Check before posting:**\n" + ''.join(f"- {g}\n" for g in m.get('guesses', [])) if m.get('guesses') else ''))

if __name__ == '__main__':
    load(sys.argv[1]); mode = sys.argv[2]
    out = os.path.abspath(os.path.expanduser(os.environ.get('OUT', SPEC.META.get('output', 'infographic.mp4')))); os.makedirs(os.path.dirname(out), exist_ok=True)
    stem = out[:-4]; built = SPEC.META.get('built_at', SPEC.META.get('loop', 12.0) - 1.0)
    if mode == 'stills':
        for ts in sys.argv[3:]: p = f'{stem}-t{ts}.png'; frame(float(ts)).save(p); print(p)
    elif mode == 'safe':
        p = f'{stem}-safe.png'; safe_overlay(frame(built)).save(p); print(p)
    else:
        loop = SPEC.META.get('loop', 12.0)
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
        for i in range(int(round(loop * FPS))): p.stdin.write(frame(i / FPS).tobytes())
        p.stdin.close(); assert p.wait() == 0
        png = f'{stem}.png'; frame(built).save(png)
        open(f'{stem}-caption.md', 'w').write(caption_md(png, out))
        print(out); print(png); print(f'{stem}-caption.md')
