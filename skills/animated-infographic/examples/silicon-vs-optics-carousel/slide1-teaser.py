"""Photo carousel, slide 1 of 2: short teaser: hook + swipe, nothing else.

Run: python3 ../../animated_infographic.py slide1-teaser.py png
"""
from animated_infographic import *

META = {
    'title': 'Silicon vs. optics',
    'series': 'AI CONCEPTS', 'chrome_pills': True,   # pills keep the labels readable on the bright sky
    'topic_tag': 'SILICON VS. OPTICS · 1/2',
    'bg': '~/photos/bg-alhambra.jpg',          # Alhambra theater street, SF: sky on top, nothing to crop
    'bg_keep': 1.0, 'bg_dy': 0,
    'blur': 12, 'wash': 120,               # see-through frost (same as the ML toolbox post)
    'output': '~/out/silicon-vs-optics-slide1-teaser.mp4',  # png mode writes the .png next to it
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
PANEL_H = 650


def draw(d, t):
    y = top() + 44
    for i, (ln, col) in enumerate((('AI RUNS ON', INK), ('ELECTRICITY.', INK), ('SO WHY IS IT', ACC), ('STARTING TO USE LIGHT?', ACC))):
        rise(d, t, 0.2 + i * 0.2, (X0, y + i * 112), ln, fit(D, ln, X1 - X0, 108), col)
    y += 4 * 112 + 50
    a = prog(t, 1.2); xe = chip(d, X0, y, 'SWIPE FOR THE ANSWER', INK, a, f=M(26, 800), h=56)
    arrow(d, xe + 16, y + 28, xe + 80, y + 28, INK, a, w=6, head=18)
