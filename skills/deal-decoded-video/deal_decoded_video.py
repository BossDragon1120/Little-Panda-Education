#!/usr/bin/env python3
"""Deal Decoded video renderer.
Usage:
  python3 deal_decoded_video.py spec.json stills 6 45 80   # preview frames (seconds)
  python3 deal_decoded_video.py spec.json render            # full video -> spec["output"]
Fonts: run `npm pack @fontsource/anton @fontsource/jetbrains-mono @fontsource/inter` in FONT_DIR
and untar each into FONT_DIR/fontsource-<name>/ (see SKILL.md).
"""
import sys, os, json, random, subprocess
from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FD = os.environ.get('FONT_DIR', os.path.expanduser('~/dd-fonts'))
X0, X1 = 64, 944          # content column, clear of TikTok's right rail
TOP, BOTTOM = 410, 1430   # content band, clear of search bar and caption

PALETTES = {
 'navy':     dict(BG=(14,27,51), ACC=(212,255,58), FG=(246,243,234), DIM=(150,162,184), LINE=(52,70,102), RED=(255,92,92), GREEN=(80,230,160),
                  ONACC=(14,27,51), PANEL=(22,38,68), APANEL=(36,52,40), RPANEL=(64,24,40), GRID=(26,42,70), TRACK=(36,54,86)),
 'terminal': dict(BG=(11,11,12), ACC=(255,176,0), FG=(242,242,238), DIM=(140,140,136), LINE=(52,52,54), RED=(255,69,58), GREEN=(48,219,110),
                  ONACC=(0,0,0), PANEL=(18,18,20), APANEL=(30,23,0), RPANEL=(42,10,10), GRID=(30,30,32), TRACK=(40,40,42)),
}
P = {}
SPEC = {}

@lru_cache(None)
def D(s): return ImageFont.truetype(f'{FD}/fontsource-anton/files/anton-latin-400-normal.woff', s)
@lru_cache(None)
def M(s, w=800): return ImageFont.truetype(f'{FD}/fontsource-jetbrains-mono/files/jetbrains-mono-latin-{w}-normal.woff', s)
@lru_cache(None)
def S(s, w=700): return ImageFont.truetype(f'{FD}/fontsource-inter/files/inter-latin-{w}-normal.woff', s)

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def prog(t, s, d=0.45): return ease((t - s) / d)
def mix(a, b, k): return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))
def tw(text, font): return font.getlength(text)
def fit(fn, text, maxw, size):
    while size > 20 and tw(text, fn(size)) > maxw: size -= 2
    return fn(size)
def wrap(text, font, maxw):
    out, cur = [], ''
    for w in text.split(' '):
        t = (cur + ' ' + w).strip()
        if tw(t, font) <= maxw: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

def T(d, xy, text, font, color, a=1, bg=None, anchor='la'):
    if a <= 0: return
    d.text(xy, text, font=font, fill=mix(bg or P['BG'], color, a), anchor=anchor)
def rise(d, t, s, xy, text, font, color, bg=None, anchor='la', dist=28):
    a = prog(t, s); T(d, (xy[0], xy[1] + (1 - a) * dist), text, font, color, a, bg, anchor)
def para(d, t, s, x, y, text, font, color, maxw, lh, stagger=0.08):
    lines = wrap(text, font, maxw)
    for i, ln in enumerate(lines): rise(d, t, s + i * stagger, (x, y + i * lh), ln, font, color)
    return y + len(lines) * lh
def pill(d, xr, y, text, color, solid=False, a=1):
    f = M(24); w = tw(text, f) + 28; box = (xr - w, y, xr, y + 44)
    if solid: d.rectangle(box, fill=mix(P['BG'], color, a)); T(d, (xr - w / 2, y + 22), text, f, P['ONACC'], a, bg=color, anchor='mm')
    else: d.rectangle(box, outline=mix(P['BG'], color, a), width=3); T(d, (xr - w / 2, y + 22), text, f, color, a, anchor='mm')

# ---------- icons (generic library) ----------
def icon(d, kind, cx, cy, col):
    k = kind.lower()
    if k == 'laptop':
        d.rounded_rectangle((cx-44, cy-32, cx+44, cy+22), 5, outline=col, width=4); d.rectangle((cx-58, cy+26, cx+58, cy+32), fill=col)
    elif k == 'server':
        for i in range(3):
            y = cy - 34 + i * 24; d.rounded_rectangle((cx-46, y, cx+46, y+18), 3, outline=col, width=4); d.ellipse((cx+28, y+6, cx+34, y+12), fill=col)
    elif k == 'phone':
        d.rounded_rectangle((cx-22, cy-38, cx+22, cy+36), 8, outline=col, width=4); d.rectangle((cx-8, cy+26, cx+8, cy+29), fill=col)
    elif k == 'cloud':
        d.ellipse((cx-46, cy-6, cx-6, cy+30), outline=col, width=4); d.ellipse((cx-22, cy-30, cx+26, cy+18), outline=col, width=4); d.ellipse((cx+6, cy-8, cx+46, cy+30), outline=col, width=4)
    elif k in ('identity', 'person', 'user'):
        d.rounded_rectangle((cx-40, cy-34, cx+40, cy+34), 6, outline=col, width=4); d.ellipse((cx-12, cy-22, cx+12, cy+2), outline=col, width=4); d.arc((cx-24, cy+4, cx+24, cy+44), 200, 340, fill=col, width=4)
    elif k in ('data', 'database'):
        d.ellipse((cx-36, cy-36, cx+36, cy-16), outline=col, width=4)
        d.line((cx-36, cy-26, cx-36, cy+26), fill=col, width=4); d.line((cx+36, cy-26, cx+36, cy+26), fill=col, width=4)
        d.arc((cx-36, cy-10, cx+36, cy+10), 0, 180, fill=col, width=4); d.arc((cx-36, cy+16, cx+36, cy+36), 0, 180, fill=col, width=4)
    elif k == 'factory':
        d.polygon([(cx-50, cy+30), (cx-50, cy-10), (cx-20, cy+5), (cx-20, cy-10), (cx+10, cy+5), (cx+10, cy-34), (cx+30, cy-34), (cx+30, cy+30)], outline=col, width=4)
        d.line((cx-50, cy+30, cx+50, cy+30), fill=col, width=4)
    elif k in ('pill', 'drug', 'medicine'):
        d.rounded_rectangle((cx-46, cy-18, cx+46, cy+18), 18, outline=col, width=4); d.line((cx, cy-18, cx, cy+18), fill=col, width=4)
    elif k in ('lab', 'flask'):
        d.polygon([(cx-12, cy-36), (cx+12, cy-36), (cx+12, cy-6), (cx+38, cy+32), (cx-38, cy+32), (cx-12, cy-6)], outline=col, width=4)
    elif k in ('car', 'vehicle'):
        d.rounded_rectangle((cx-50, cy-6, cx+50, cy+20), 6, outline=col, width=4); d.polygon([(cx-28, cy-6), (cx-16, cy-28), (cx+18, cy-28), (cx+30, cy-6)], outline=col, width=4)
        d.ellipse((cx-36, cy+12, cx-18, cy+30), outline=col, width=4); d.ellipse((cx+18, cy+12, cx+36, cy+30), outline=col, width=4)
    elif k in ('chart', 'growth'):
        d.line((cx-46, cy+30, cx+46, cy+30), fill=col, width=4)
        for i, h in enumerate([20, 36, 52]): d.rectangle((cx-38 + i*28, cy+30-h, cx-22 + i*28, cy+30), outline=col, width=4)
    elif k == 'globe':
        d.ellipse((cx-36, cy-36, cx+36, cy+36), outline=col, width=4); d.ellipse((cx-14, cy-36, cx+14, cy+36), outline=col, width=3); d.line((cx-36, cy, cx+36, cy), fill=col, width=3)
    elif k in ('store', 'shop', 'retail'):
        d.rectangle((cx-42, cy-8, cx+42, cy+30), outline=col, width=4); d.polygon([(cx-48, cy-8), (cx-38, cy-30), (cx+38, cy-30), (cx+48, cy-8)], outline=col, width=4)
    elif k in ('gear', 'machine', 'equipment'):
        d.ellipse((cx-30, cy-30, cx+30, cy+30), outline=col, width=6); d.ellipse((cx-10, cy-10, cx+10, cy+10), outline=col, width=4)
        for ax, ay in [(0,-38),(0,38),(-38,0),(38,0)]: d.rectangle((cx+ax-6, cy+ay-6, cx+ax+6, cy+ay+6), fill=col)
    elif k in ('money', 'bank', 'payment'):
        d.rounded_rectangle((cx-48, cy-26, cx+48, cy+26), 6, outline=col, width=4); d.ellipse((cx-14, cy-14, cx+14, cy+14), outline=col, width=4)
    elif k in ('chip', 'semiconductor'):
        d.rectangle((cx-28, cy-28, cx+28, cy+28), outline=col, width=4)
        for i in range(-2, 3):
            d.line((cx+i*10, cy-40, cx+i*10, cy-28), fill=col, width=3); d.line((cx+i*10, cy+28, cx+i*10, cy+40), fill=col, width=3)
    elif k in ('lift', 'scissor-lift'):
        d.rectangle((cx-48, cy-34, cx+48, cy-24), outline=col, width=4)
        d.line((cx-48, cy-34, cx-48, cy-46), fill=col, width=3); d.line((cx+48, cy-34, cx+48, cy-46), fill=col, width=3); d.line((cx-48, cy-46, cx+48, cy-46), fill=col, width=3)
        d.line((cx-34, cy-24, cx+34, cy+12), fill=col, width=4); d.line((cx+34, cy-24, cx-34, cy+12), fill=col, width=4)
        d.rectangle((cx-48, cy+12, cx+48, cy+24), outline=col, width=4)
        d.ellipse((cx-42, cy+22, cx-26, cy+38), outline=col, width=4); d.ellipse((cx+26, cy+22, cx+42, cy+38), outline=col, width=4)
    elif k in ('boom', 'boom-lift'):
        d.rectangle((cx-46, cy+12, cx+10, cy+26), outline=col, width=4)
        d.ellipse((cx-42, cy+24, cx-28, cy+38), outline=col, width=4); d.ellipse((cx-8, cy+24, cx+6, cy+38), outline=col, width=4)
        d.line((cx-20, cy+12, cx+30, cy-30), fill=col, width=5)
        d.rectangle((cx+24, cy-46, cx+50, cy-30), outline=col, width=4)
    else:  # fallback: initial in a box
        d.rectangle((cx-36, cy-36, cx+36, cy+36), outline=col, width=4); d.text((cx, cy), kind[:1].upper(), font=D(48), fill=col, anchor='mm')

# ---------- chrome ----------
def build_static():
    global BGIMG, TICKIMG, TLEN
    BGIMG = Image.new('RGB', (W, H), P['BG']); bd = ImageDraw.Draw(BGIMG)
    for gx in range(0, W, 40):
        for gy in range(0, H, 40): bd.point((gx, gy), fill=P['GRID'])
    text = '   ' + '  ///  '.join(['DEAL DECODED'] + SPEC['ticker_items']) + '  ///'
    f = M(26); TLEN = int(tw(text, f))
    TICKIMG = Image.new('RGB', (TLEN * 2 + W, 46), P['ACC']); td = ImageDraw.Draw(TICKIMG)
    for k in range(3): td.text((k * TLEN, 23), text, font=f, fill=P['ONACC'], anchor='lm')

def chrome(img, d, gt, si, lt, dur, n):
    if int(gt * 2) % 2 == 0: d.ellipse((X0, 232, X0 + 16, 248), fill=P['RED'])
    T(d, (X0 + 28, 240), 'DEAL DECODED', M(30), P['ACC'], anchor='lm')
    T(d, (X1, 240), f"{SPEC['episode']} · {SPEC['tickers']}", M(24, 700), P['DIM'], anchor='rm')
    off = int(gt * 110) % TLEN
    img.paste(TICKIMG.crop((off, 0, off + W, 46)), (0, 290))
    gap = 8; sw = (X1 - X0 - gap * (n - 1)) / n
    for i in range(n):
        x = X0 + i * (sw + gap); d.rectangle((x, 362, x + sw, 367), fill=P['TRACK'])
        f = 1 if i < si else (clamp(lt / dur) if i == si else 0)
        if f > 0: d.rectangle((x, 362, x + sw * f, 367), fill=P['ACC'])

def wipe(d, lt):
    if lt < 0.3:
        x = -W + 2 * W * ease(lt / 0.3); d.rectangle((x, TOP - 15, x + W, BOTTOM), fill=P['ACC'])

def label(d, t, text): rise(d, t, 0.05, (X0, 420), text, M(30), P['ACC'], dist=14)

# ---------- scenes ----------
def s_hook(img, d, t, c):
    rise(d, t, 0.0, (X0, 420), c['kicker'], M(30), P['ACC'], dist=14)
    rise(d, t, 0.15, (X0, 468), c['buyer'], fit(D, c['buyer'], X1 - X0, 170), P['FG'])
    a = prog(t, 0.5); vf = M(40)
    T(d, (X0, 690), c.get('verb', 'IS BUYING'), vf, P['ACC'], a)
    if a > 0:
        xs = X0 + tw(c.get('verb', 'IS BUYING'), vf) + 30; x2 = xs + (X1 - 40 - xs) * a
        d.rectangle((xs, 686, x2, 694), fill=P['ACC']); d.polygon([(x2, 674), (x2 + 26, 690), (x2, 706)], fill=P['ACC'])
    rise(d, t, 0.8, (X0, 735), c['target'], fit(D, c['target'], X1 - X0, 170), P['FG'])
    a = prog(t, 1.3, 0.3)
    if a > 0:
        v = c['value'] * ease((t - 1.3) / 1.3)
        txt = c.get('value_prefix', '$') + f"{v:.{c.get('decimals', 1)}f}" + c.get('value_suffix', 'B')
        T(d, (X0 - 6, 1195), txt, fit(D, c.get('value_prefix', '$') + f"{c['value']:.{c.get('decimals', 1)}f}" + c.get('value_suffix', 'B'), X1 - X0, 230), P['ACC'], a, anchor='ls')
    a = prog(t, 2.6)
    if a > 0:
        x = X0
        for txt in c.get('tags', []):
            f = M(28); w = tw(txt, f) + 28
            if x + w > X1: break
            d.rectangle((x, 1222, x + w, 1272), outline=mix(P['BG'], P['FG'], a), width=3)
            T(d, (x + w / 2, 1247), txt, f, P['FG'], a, anchor='mm'); x += w + 14
    f, lh = fit_para(c['line'], X1 - X0, sizes=((50, 60), (44, 54), (38, 47)))
    para(d, t, 3.6, X0, 1300, c['line'], f, P['FG'], X1 - X0, lh)

def headline(d, t, c):
    rise(d, t, 0.15, (X0, 462), c['name'], fit(D, c['name'], X1 - X0, 150), P['FG'])
    a = prog(t, 0.5); full = c['verb'] + ' ' + c['what']; f = fit(D, full, X1 - X0, 92)
    T(d, (X0, 630 + (1 - a) * 20), c['verb'], f, P['FG'], a)
    T(d, (X0 + tw(c['verb'] + ' ', f), 630 + (1 - a) * 20), c['what'], f, P['ACC'], a)
    if c.get('sub'): rise(d, t, 0.9, (X0, 752), c['sub'], fit(M, c['sub'], X1 - X0, 30), P['ACC'], dist=14)

def vis_tiles(d, t, c, vis, alert_on):
    items = vis['items'][:6]; cols = 3; g = 22
    tw_ = (X1 - X0 - (cols - 1) * g) / cols; th = 140 if len(items) > 3 else 190
    for i, it in enumerate(items):
        a = prog(t, 1.0 + i * 0.12, 0.35)
        if a <= 0: continue
        x = X0 + (i % cols) * (tw_ + g); y = 812 + (i // cols) * (th + g) + (1 - a) * 20
        al = alert_on and it.get('alert')
        fc = P['RPANEL'] if al else P['PANEL']; col = P['RED'] if al else P['FG']
        d.rounded_rectangle((x, y, x + tw_, y + th), 10, fill=mix(P['BG'], fc, a), outline=mix(P['BG'], P['RED'] if al else P['LINE'], a), width=3)
        icon(d, it.get('icon', it['label']), x + tw_ / 2, y + th / 2 - 10, mix(P['BG'], col, a))
        T(d, (x + 14, y + th - 14), it['label'], fit(M, it['label'], tw_ - 28, 20), P['DIM'], a, bg=fc, anchor='lb')
        if al: T(d, (x + tw_ - 18, y + 14), '!', D(44), P['RED'], a, bg=fc, anchor='ra')
        else:
            gx, gy = x + tw_ - 26, y + 26; ph = (t * 0.9 + i * 0.17) % 1; r = 8 + ph * 20
            d.ellipse((gx - r, gy - r, gx + r, gy + r), outline=mix(fc, P['ACC'], (1 - ph) * a), width=2)
            d.ellipse((gx - 7, gy - 7, gx + 7, gy + 7), fill=mix(fc, P['ACC'], a))
            sy = y + 12 + ((t * 0.6 + i * 0.23) % 1) * (th - 24)
            d.line((x + 8, sy, x + tw_ - 8, sy), fill=mix(fc, P['ACC'], 0.35 * a), width=2)

def vis_flow(d, t, c, vis):
    va = prog(t, 1.0, 0.6)
    if va <= 0: return
    right = vis['right'][:4]; nl = len(right); ys = [810 + i * 75 for i in range(nl)]; cy = (ys[0] + ys[-1]) / 2
    ux, gx, ax = X0 + 30, 500, 790
    left = vis.get('left', [])
    for y in ys:
        d.line((ux + 24, y, gx - 34, cy), fill=mix(P['BG'], P['LINE'], va), width=2); d.line((gx + 34, cy, ax, y), fill=mix(P['BG'], P['LINE'], va), width=2)
    for i, y in enumerate(ys):
        d.ellipse((ux - 22, y - 22, ux + 22, y + 22), outline=mix(P['BG'], P['FG'], va), width=4)
        if i < len(left) and left[i]: T(d, (ux, y), left[i][:2], M(18), P['FG'], va, anchor='mm')
        else: d.ellipse((ux - 7, y - 12, ux + 7, y + 2), fill=mix(P['BG'], P['FG'], va))
        d.rectangle((ax, y - 26, ax + 150, y + 26), outline=mix(P['BG'], P['FG'], va), width=3)
        T(d, (ax + 75, y), right[i], fit(M, right[i], 136, 22), P['FG'], va, anchor='mm')
    d.rectangle((gx - 34, ys[0] - 40, gx + 34, ys[-1] + 40), fill=mix(P['BG'], P['APANEL'], va), outline=mix(P['BG'], P['ACC'], va), width=4)
    T(d, (gx, cy), vis.get('hub', '*')[:2], D(54), P['ACC'], va, bg=P['APANEL'], anchor='mm')
    T(d, (gx, ys[-1] + 63), vis.get('hub_label', 'HUB'), M(22), P['ACC'], va, anchor='mm')
    for k in range(8):
        ph = (t * 0.45 + k / 8) % 1; src, dst = k % nl, (k * 3 + 1) % nl
        bad = k == 5 and vis.get('blocked_label')
        if bad and ph > 0.8: continue
        if ph < 0.5 or bad:
            p = min(ph, 0.5) / 0.5; px = ux + 24 + (gx - 58 - ux) * p; py = ys[src] + (cy - ys[src]) * p
        else:
            p = (ph - 0.5) / 0.5; px = gx + 34 + (ax - gx - 34) * p; py = cy + (ys[dst] - cy) * p
        col = P['RED'] if bad else P['ACC']
        d.rectangle((px - 8, py - 8, px + 8, py + 8), fill=mix(P['BG'], col, va))
        if bad and ph >= 0.5: T(d, (px - 30, py - 40), vis['blocked_label'], M(20), P['RED'], va, anchor='rm')

def fit_para(text, maxw, sizes=((46, 56), (40, 50), (36, 45), (32, 40)), maxlines=2):
    for fs, lh in sizes:
        f = S(fs, 800)
        if len(wrap(text, f, maxw)) <= maxlines: return f, lh
    return f, lh

def visual_bottom(vis):
    if vis.get('type') == 'tiles':
        n = len(vis['items'][:6]); rows = (n + 2) // 3; th = 140 if n > 3 else 190
        return 812 + rows * th + (rows - 1) * 22
    if vis.get('type') == 'flow':
        return 810 + (len(vis['right'][:4]) - 1) * 75 + 80
    return 760

def s_company(img, d, t, c):
    label(d, t, c['label']); headline(d, t, c)
    co = c.get('callout'); alert_on = bool(co) and co['at'] <= t < co['at'] + 1.4
    vis = c.get('visual', {})
    if vis.get('type') == 'flow': vis_flow(d, t, c, vis)
    elif vis.get('type') == 'tiles': vis_tiles(d, t, c, vis, alert_on)
    extra = 150 if (co or c.get('stat')) else 0
    y = visual_bottom(vis) + 40
    f, lh = fit_para(c['line'], X1 - X0)
    nlines = len(wrap(c['line'], f, X1 - X0))
    # keep the whole stack inside the content band
    y = min(y, BOTTOM - extra - 25 - nlines * lh)
    y = para(d, t, 3.0, X0, y, c['line'], f, P['FG'], X1 - X0, lh) + 25
    if co:
        a = prog(t, co['at'], 0.3)
        if a > 0:
            yy = y + (1 - a) * 20; rp = P['RPANEL']
            d.rectangle((X0, yy, X1, yy + 135), fill=mix(P['BG'], rp, a), outline=mix(P['BG'], P['RED'], a), width=3)
            T(d, (X0 + 22, yy + 20), co['kicker'], M(26), P['RED'], a, bg=rp)
            for j, ln in enumerate(co['text'][:2]): T(d, (X0 + 22, yy + 58 + j * 38), ln, fit(S, ln, X1 - X0 - 44, 31), P['FG'], a, bg=rp)
    st = c.get('stat')
    if st:
        a = prog(t, st['at'])
        if a > 0:
            y0 = y - 20
            bf = fit(D, st['big'], 420, 130); T(d, (X0 - 4, y0 + (1 - a) * 20), st['big'], bf, P['ACC'], a)
            x = X0 + tw(st['big'], bf) + 26
            T(d, (x, y0 + 38 + (1 - a) * 20), st['l1'], fit(S, st['l1'], X1 - x, 40), P['FG'], a)
            T(d, (x, y0 + 88 + (1 - a) * 20), st.get('l2', ''), fit(lambda z: S(z, 500), st.get('l2', ''), X1 - x, 40), P['DIM'], a)

def s_hypothesis(img, d, t, c):
    label(d, t, c.get('label', '03 / MY HYPOTHESIS'))
    rise(d, t, 0.15, (X0, 462), c.get('title', 'WHY 1 + 1 > 2'), fit(D, c.get('title', 'WHY 1 + 1 > 2'), X1 - X0, 120), P['FG'])
    cards = c['cards'][:3]; y = 640
    for i, cd in enumerate(cards):
        s = cd['at']; a = prog(t, s); nxt = cards[i + 1]['at'] if i + 1 < len(cards) else 1e9
        active = s <= t < nxt
        if a > 0:
            yy = y + (1 - a) * 30; fc = P['APANEL'] if active else P['PANEL']
            d.rectangle((X0, yy, X1, yy + 240), fill=mix(P['BG'], fc, a), outline=mix(P['BG'], P['ACC'] if active else P['LINE'], a), width=3)
            T(d, (X0 + 30, yy + 18), str(i + 1), D(150), P['ACC'] if active else P['DIM'], a, bg=fc)
            T(d, (X0 + 150, yy + 26), cd['head'], fit(D, cd['head'], X1 - X0 - 180, 64), P['FG'], a, bg=fc)
            bf, blh = S(34, 600), 44
            if len(wrap(cd['body'], bf, X1 - X0 - 180)) > 2: bf, blh = S(29, 600), 36
            for j, ln in enumerate(wrap(cd['body'], bf, X1 - X0 - 180)[:3]):
                T(d, (X0 + 150, yy + 112 + j * blh), ln, bf, P['FG'] if active else P['DIM'], a, bg=fc)
        y += 262

def s_you(img, d, t, c):
    label(d, t, c.get('label', '04 / WHY YOU CARE'))
    for i, ln in enumerate(c['title'][:2]):
        rise(d, t, 0.15 + i * 0.12, (X0, 462 + i * 112), ln, fit(D, ln, X1 - X0, 104), P['ACC'] if i else P['FG'])
    ys = [740, 880, 1020]; nodes = c['nodes'][:3]; tok = clamp((t - 1.6) / 5.0) * 2
    for i, nd in enumerate(nodes):
        a = prog(t, 0.8 + i * 0.15)
        if a <= 0: continue
        done = tok >= i and t > 1.6 + (0.4 if i == 0 else 0); fc = P['PANEL']; y = ys[i]
        d.rectangle((X0, y, X1, y + 100), fill=mix(P['BG'], fc, a), outline=mix(P['BG'], P['GREEN'] if done else P['LINE'], a), width=3)
        T(d, (X0 + 150, y + 50), nd['title'], fit(D, nd['title'], 430, 52), P['FG'], a, bg=fc, anchor='lm')
        if done: d.line((X1 - 62, y + 50, X1 - 50, y + 63, X1 - 28, y + 36), fill=P['GREEN'], width=7)
        T(d, (X1 - 90, y + 50), nd.get('tag', ''), M(22), P['GREEN'] if nd.get('final') else P['ACC'], a, bg=fc, anchor='rm')
    a = prog(t, 0.8)
    if a > 0:
        d.line((X0 + 70, ys[0] + 50, X0 + 70, ys[2] + 50), fill=mix(P['BG'], P['LINE'], a), width=4)
        seg = min(int(tok), 1); fr = tok - seg
        if tok >= 2: seg, fr = 1, 1
        ty = ys[seg] + 50 + (ys[seg + 1] - ys[seg]) * ease(fr)
        d.ellipse((X0 + 34, ty - 36, X0 + 106, ty + 36), fill=mix(P['BG'], P['ACC'], a))
        T(d, (X0 + 70, ty), c.get('token', 'YOU')[:3], fit(M, c.get('token', 'YOU')[:3], 60, 28), P['ONACC'], a, bg=P['ACC'], anchor='mm')
    if c.get('threat') and 3.2 <= t < 5.6:
        p = ease((t - 3.2) / 0.8); x = X1 + 200 - 330 * p; y = ys[1] - 40
        f = M(22); w = tw(c['threat'], f) + 24; rp = P['RPANEL']
        d.rectangle((x - w, y, x, y + 36), fill=rp, outline=P['RED'], width=3)
        T(d, (x - w / 2, y + 18), c['threat'], f, P['RED'], bg=rp, anchor='mm')
        if t > 4.0:
            cx = x - w / 2; d.line((cx - 40, y - 10, cx + 40, y + 46), fill=P['RED'], width=7); d.line((cx - 40, y + 46, cx + 40, y - 10), fill=P['RED'], width=7)
    f, lh = fit_para(c['line'], X1 - X0, maxlines=3)
    para(d, t, 6.2, X0, 1160, c['line'], f, P['FG'], X1 - X0, lh)

def s_watching(img, d, t, c):
    label(d, t, c.get('label', "05 / WHAT I'M WATCHING"))
    y = 478
    for i, r in enumerate(c['rows'][:2]):
        s = 0.3 + i * 1.5; a = prog(t, s)
        if a > 0:
            col = P['RED'] if r.get('risk') else P['FG']
            T(d, (X0, y + (1 - a) * 20), r['title'], fit(D, r['title'], X1 - X0 - (230 if r.get('pill') else 0), 72), col, a)
            if r.get('pill'): pill(d, X1, y + 22, r['pill'], P['ACC'], solid=int(t * 2) % 2 == 0, a=a)
            yb = para(d, t, s + 0.3, X0, y + 97, r['body'], S(38, 600), P['DIM'], X1 - X0, 48)
        else: yb = y + 97 + 96
        y = yb + 25
        if i == 0: d.line((X0, y - 12, X1, y - 12), fill=P['LINE'], width=2)
    big = c.get('big', [])
    for i, ln in enumerate(big[:2]):
        s = 4.2 + i * 0.25
        if t >= s:
            jit = (t - s) < 0.35; rnd = random.Random(int(t * 30) + i); dx = rnd.randint(-14, 14) if jit else 0
            f = fit(D, ln, X1 - X0, 190)
            if jit: T(d, (X0 + dx + 8, 930 + i * 175), ln, f, (0, 200, 255), 0.6)
            T(d, (X0 + dx, 930 + i * 175), ln, f, P['RED'])
    if c.get('foot'): rise(d, t, 6.0, (X0, 1345), c['foot'], fit(M, c['foot'], X1 - X0, 28), P['DIM'])

def s_card(img, d, t, c):
    label(d, t, c.get('label', '06 / THE DEAL CARD'))
    if t > 0.6: pill(d, X1, 412, 'SCREENSHOT THIS', P['ACC'], solid=int(t * 2) % 2 == 0)
    a = prog(t, 0.3); fc = P['PANEL']; top, bot = 480, 1262
    if a > 0: d.rectangle((X0, top, X1, top + (bot - top) * a), fill=fc, outline=P['ACC'], width=4)
    if a < 1: return
    rise(d, t, 0.6, (X0 + 30, 500), c['header'], fit(D, c['header'], X1 - X0 - 60, 68), P['FG'])
    d.line((X0 + 30, 596, X1 - 30, 596), fill=P['ACC'], width=2)
    rows = c['rows']; vx = X0 + 250; vw = X1 - 30 - vx
    for vs, lh, gap in [(30, 38, 14), (28, 35, 12), (26, 32, 10), (24, 29, 8)]:
        vf = S(vs, 600); total = sum(len(v) * lh + gap for _, v in rows)
        if 616 + total <= bot - 50 and all(tw(x, vf) <= vw for _, v in rows for x in v): break
    y = 616
    for i, (k, vals) in enumerate(rows):
        s = 0.8 + i * 0.12
        T(d, (X0 + 30, y + 6), k, fit(M, k, 200, 22), P['ACC'], prog(t, s), bg=fc)
        for j, v in enumerate(vals): T(d, (vx, y + j * lh), v, fit(lambda z: S(z, 600), v, vw, vs), P['FG'], prog(t, s), bg=fc)
        y += len(vals) * lh + gap
    cf = S(21, 500)
    for j, ln in enumerate(wrap(c.get('caveat', ''), cf, X1 - X0 - 60)[:2]):
        T(d, (X0 + 30, y + 4 + j * 27), ln, cf, P['DIM'], prog(t, 2.0), bg=fc)
    a = prog(t, 6.0)
    if a > 0:
        cta = c.get('cta', ['FOLLOW FOR THE NEXT DEAL,', 'DECODED.'])
        T(d, (X0, 1290 + (1 - a) * 20), cta[0], fit(D, cta[0], X1 - X0, 60), P['FG'], a)
        T(d, (X0, 1360 + (1 - a) * 20), cta[1], fit(D, cta[1], X1 - X0, 60), P['ACC'], a)

ORDER = [('hook', s_hook), ('buyer', s_company), ('target', s_company), ('hypothesis', s_hypothesis),
         ('you', s_you), ('watching', s_watching), ('card', s_card)]

def setup(spec_path):
    global SPEC, P, BOUNDS
    SPEC = json.load(open(spec_path)); P = PALETTES[SPEC.get('palette', 'navy')]
    durs = SPEC.get('durations', [7, 13, 10, 20, 10, 10, 16]); BOUNDS = []; s = 0
    for dd in durs: BOUNDS.append((s, s + dd)); s += dd
    build_static()

def frame(gt):
    n = len(ORDER)
    for si, (a, b) in enumerate(BOUNDS):
        if a <= gt < b or si == n - 1: break
    lt = gt - BOUNDS[si][0]
    img = BGIMG.copy(); d = ImageDraw.Draw(img)
    chrome(img, d, gt, si, lt, BOUNDS[si][1] - BOUNDS[si][0], n)
    key, fn = ORDER[si]; fn(img, d, lt, SPEC['scenes'][key])
    if si > 0: wipe(d, lt)
    return img

def render_scene(args):
    spec_path, si, outdir = args
    setup(spec_path); a, b = BOUNDS[si]
    tmp, final = f'{outdir}/scene{si}.tmp.mp4', f'{outdir}/scene{si}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for i in range(int(round((b - a) * FPS))): p.stdin.write(frame(a + i / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit(f'scene {si} failed')
    os.replace(tmp, final); return final

if __name__ == '__main__':
    spec_path, mode = sys.argv[1], sys.argv[2]
    setup(spec_path)
    out = SPEC.get('output', 'deal-decoded.mp4'); outdir = os.path.join(os.path.dirname(os.path.abspath(out)), 'dd_scenes')
    os.makedirs(outdir, exist_ok=True)
    if mode == 'stills':
        for ts in sys.argv[3:]:
            p = os.path.join(outdir, f'still_{ts}.png'); frame(float(ts)).save(p); print(p)
    else:
        with ProcessPoolExecutor() as ex: files = list(ex.map(render_scene, [(spec_path, i, outdir) for i in range(len(ORDER))]))
        lst = os.path.join(outdir, 'list.txt'); open(lst, 'w').write(''.join(f"file '{f}'\n" for f in files))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], check=True)
        print(out)
