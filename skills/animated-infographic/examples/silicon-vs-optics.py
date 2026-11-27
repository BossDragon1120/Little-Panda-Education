"""Animated infographic: silicon vs. optics, for a layman.

Takeaway: chips do the math with electricity; more and more, they move data to each other with light.
Run: python3 ../animated_infographic.py silicon-vs-optics.py render
"""
from animated_infographic import *

META = {
    'title': 'Silicon vs. optics',
    'series': 'AI VOCAB',
    'topic_tag': 'SILICON VS. OPTICS',
    'bg': '~/photos/bg-bar.jpg',          # the bar photo; crop below hides the mouse on the table
    'bg_keep': 0.80, 'bg_dy': 70,
    'blur': 12, 'wash': 120,               # see-through frost (same as the ML toolbox post)
    'loop': 12.0,                          # seconds; motion periods below divide it, so the loop is seamless
    'output': '~/out/silicon-vs-optics.mp4',
    'caption': "Your AI chatbot thinks with electricity... but it's learning to talk with light 💡",
    'hashtags': ['#AIVocab', '#Photonics', '#Semiconductors', '#AIChips', '#DataCenters', '#Nvidia',
                 '#TechExplained', '#TechTok', '#LearnOnTikTok', '#ArtificialIntelligence'],
    'guesses': [
        'Series label: AI VOCAB (the Tech series has no name yet).',
        '"Thousands of chips" is a general figure; the biggest AI training runs use tens of thousands or more.',
        'Electricity vs. light trade-offs are simplified for a layman: both signals travel at similar speed; light wins on how much data it carries, how far, and how much heat it makes.',
    ],
}
PANEL_H = 1280

COPPER = (190, 105, 45); LIGHT = (40, 150, 230)

def lane(d, t, a, y, kind):
    """One link between two chips. Copper: a few pulses that fade with distance + heat squiggles.
    Fiber: a dense stream of bright pulses (more data, same distance, no heat)."""
    if a <= 0: return
    lx, rx = X0 + 110, X1 - 110
    for cx in (X0 + 60, X1 - 60):   # chips at each end
        d.rounded_rectangle((cx - 40, y - 34, cx + 40, y + 34), 10, fill=C(INK, a))
        for k in range(4):
            yy = y - 24 + k * 16
            d.line((cx - 50, yy, cx - 40, yy), fill=C(DIM, a), width=3); d.line((cx + 40, yy, cx + 50, yy), fill=C(DIM, a), width=3)
        d.rounded_rectangle((cx - 22, y - 16, cx + 22, y + 16), 6, outline=C((120, 128, 150), a), width=2)
    wire_end = lx + (rx - lx) * prog(t, 1.0 if kind == 'cu' else 1.3, 0.6)
    if kind == 'cu':
        d.line((lx, y, wire_end, y), fill=C(COPPER, a), width=10)
        for i in range(3):
            p = cyc(t, 3.0, i / 3); x = lx + (rx - lx) * p
            if x < wire_end: d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=C(ACC2, a * (1 - 0.8 * p)))   # signal weakens
        for k, hx in enumerate(range(lx + 80, rx - 40, 110)):   # heat
            if hx > wire_end: break
            ph = cyc(t, 1.5, k * 0.37); hy = y - 14 - ph * 14
            pts = [(hx + 6 * math.sin((j / 6 + ph) * 2 * math.pi), hy - j * 3) for j in range(11)]
            d.line(pts, fill=C(RED, a * (1 - ph) * 0.9), width=3)
    else:
        d.line((lx, y, wire_end, y), fill=C((200, 225, 245), a), width=12)
        d.line((lx, y, wire_end, y), fill=C(LIGHT, a * 0.5), width=4)
        for i in range(12):
            p = cyc(t, 3.0, i / 12); x = lx + (rx - lx) * p
            if x < wire_end:
                d.rounded_rectangle((x - 16, y - 5, x + 16, y + 5), 5, fill=C(LIGHT, a))
                d.ellipse((x + 8, y - 7, x + 22, y + 7), fill=C(WHITE, a))

def draw(d, t):
    y = top() + 34
    y = headline(d, t, y, 'SILICON THINKS.', 'LIGHT TALKS.',
                 "AI chips do their math with electricity. To talk to each other, they're switching to light.")
    # hero: two links, built in one after the other
    a1 = prog(t, 0.9); a2 = prog(t, 1.2)
    card(d, (X0, y + 4, X1, y + 266), a1, r=22)
    T(d, (X0 + 130, y + 18), 'ELECTRICITY · COPPER WIRE', M(22, 800), COPPER, a1)
    T(d, (X1 - 30, y + 18), 'fades + gets hot', S(22, 700), RED, a1, 'ra')
    lane(d, t, a1, y + 100, 'cu')
    T(d, (X0 + 130, y + 142), 'LIGHT · GLASS FIBER', M(22, 800), LIGHT, a2)
    T(d, (X1 - 30, y + 142), 'more data, farther, cooler', S(22, 700), GOOD, a2, 'ra')
    lane(d, t, a2, y + 222, 'fiber')
    y += 284
    y = versus(d, t, y, ('SILICON = ELECTRICITY', ACC2), ('OPTICS = LIGHT', LIGHT), [
        ('TRAVELS AS', 'Electric current in copper', 'Flashes of light in glass'),
        ('YOU USE IT', 'USB and HDMI cables', 'Fiber home internet'),
        ('BEST AT', 'The math inside a chip', 'Long trips between chips'),
        ('THE CATCH', 'Heat; fades with distance', 'Must turn back into electricity'),
    ], s=1.8, rh=80, stagger=0.3)
    # why AI cares
    a = prog(t, 3.3); y0 = y + 6 + (1 - a) * 24
    card(d, (X0, y0, X1, y0 + 128), a, fill=(238, 237, 253), outline=ACC, width=4, r=20, op=225)
    chip(d, X0 + 18, y0 + 16, 'WHY AI CARES', ACC, a, f=M(22, 800), h=40)
    f = S(25, 700)
    for k, ln in enumerate(wrap('One AI model trains on thousands of chips that swap results nonstop. The traffic jam is moving data, not doing math.', f, X1 - X0 - 40)[:2]):
        T(d, (X0 + 20, y0 + 64 + k * 32), ln, f, INK, a)
    y = y0 + 128 + 14
    punchline(d, t, y, 'SILICON DOES THE MATH. LIGHT MOVES THE DATA.', 4.0, ACC, 44)
