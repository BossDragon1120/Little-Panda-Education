"""Photo carousel, slide 2 of 2: the answer in plain words.

Run: python3 ../../animated_infographic.py slide2-info.py png
"""
from animated_infographic import *

META = {
    'title': 'Silicon vs. optics',
    'series': 'AI CONCEPTS', 'chrome_pills': True,   # pills keep the labels readable on the bright sky
    'topic_tag': 'SILICON VS. OPTICS · 2/2',
    'bg': '~/photos/bg-alhambra.jpg',          # Alhambra theater street, SF: sky on top, nothing to crop
    'bg_keep': 1.0, 'bg_dy': 0,
    'blur': 12, 'wash': 120,               # see-through frost (same as the ML toolbox post)
    'output': '~/out/silicon-vs-optics-slide2-info.mp4',  # png mode writes the .png next to it
    'caption': "Your AI chatbot thinks with electricity... but it's learning to talk with light 💡",
    'hashtags': ['#AIConcepts', '#Photonics', '#Semiconductors', '#AIChips', '#DataCenters', '#Nvidia',
                 '#TechExplained', '#TechTok', '#LearnOnTikTok', '#ArtificialIntelligence'],
    'guesses': [
        'Series label: AI CONCEPTS (Dana, 2026-11-27).',
        '"Thousands of chips" is a lower bound; the biggest AI training runs use tens of thousands or more.',
        '"Starting to use light", not "switching": light already links server racks; inside a rack, chips still mostly use copper.',
        '"Often the slowdown is the traffic": a major bottleneck, not the only one. "Silicon" = shorthand for electronic chips (silicon photonics left out).',
        'Simplified for a layman: both signals travel at similar speed; light wins on how much data it carries, how far, and how much heat it makes.',
    ],
}
PANEL_H = 1060
LIGHT = (40, 150, 230)


def draw(d, t):
    y = top() + 34
    y = headline(d, t, y, 'CHIPS THINK.', 'LIGHT TALKS.',
                 "The chips that run AI do their math with electricity. To pass results to each other, they're starting to use light.")
    y += 8
    y = versus(d, t, y, ('ELECTRICITY (SILICON)', ACC2), ('LIGHT (OPTICS)', LIGHT), [
        ('MOVES IN', 'Metal wires', 'Thin glass cables'),
        ("YOU'VE USED", 'Phone chargers', 'Fiber home internet'),
        ('GREAT FOR', 'The math inside a chip', 'Sending lots of data far'),
        ('DOWNSIDE', 'Gets hot, weakens over distance', 'Must switch back to electricity'),
    ], s=0.9, rh=84, stagger=0.3)
    a = prog(t, 2.6); y0 = y + 8 + (1 - a) * 24
    f = S(25, 700); ls = wrap("Training one big AI takes thousands of chips passing data back and forth. Often the slowdown isn't the math. It's the traffic between chips.", f, X1 - X0 - 40)
    hh = 66 + len(ls) * 32 + 12
    card(d, (X0, y0, X1, y0 + hh), a, fill=(238, 237, 253), outline=ACC, width=4, r=20, op=225)
    chip(d, X0 + 18, y0 + 16, 'WHY IT MATTERS', ACC, a, f=M(22, 800), h=40)
    for k, ln in enumerate(ls): T(d, (X0 + 20, y0 + 66 + k * 32), ln, f, INK, a)
    y = y0 + hh + 18
    punchline(d, t, y, 'ELECTRICITY DOES THE MATH. LIGHT MOVES MORE OF THE DATA.', 3.2, ACC, 44)
