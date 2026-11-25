"""Agentic AI (Andrew Ng, DeepLearning.AI), Module 5: patterns for highly autonomous agents.
Planning (text / Markdown / JSON / code plans, sandboxing) and multi-agent communication patterns.
Render: python3 ../course_explainer.py agentic-ai-m5-autonomous-agents.py render
"""
from course_explainer import *

META = {
    'series': 'COURSE EXPLAINER',
    'course_tag': 'AGENTIC AI \u00b7 M5',
    'output': 'agentic-ai-m5-autonomous-agents.mp4',
    'voice_trim': [1.55, 0, 0, 0, 0, 0, 0],   # the hook take had 1.7 s of silence before the first word
}
DUR = [8.5, 13.6, 12.8, 12.8, 15.8, 22.6, 27.2]   # fitted to Dana's voiceover takes (one clip per scene, starting 0.3 s in)

def s_hook(d, t):
    rise(d, t, 0.0, (X0, 440), 'MODULE 5 \u00b7 PATTERNS FOR AUTONOMOUS AGENTS', fit(lambda z: M(z, 800), 'MODULE 5 \u00b7 PATTERNS FOR AUTONOMOUS AGENTS', X1 - X0, 28), ACC, dist=12)
    for i, (ln, col) in enumerate([('WHAT IF YOUR AI', INK), ('WRITES ITS', INK), ('OWN PLAN?', ACC)]):
        rise(d, t, 0.25 + i * 0.3, (X0, 500 + i * 172), ln, fit(D, ln, X1 - X0, 168), col)
    a = prog(t, 2.0); x = X0
    for i, tag in enumerate(['PLANNING', 'CODE AS PLAN', 'MULTI-AGENT']):
        x = chip(d, x, 1085 + (1 - prog(t, 2.0 + i * 0.15)) * 16, tag, ACC, prog(t, 2.0 + i * 0.15)) + 14
    para(d, t, 3.0, X0, 1175, 'Who decides the steps: you, or the agent? And how should a team of agents talk?', S(44, 800), INK, X1 - X0, 56)
    rise(d, t, 4.2, (X0, 1360), 'NOTES FROM ANDREW NG’S AGENTIC AI COURSE, MODULE 5', fit(lambda z: M(z, 600), 'NOTES FROM ANDREW NG’S AGENTIC AI COURSE, MODULE 5', X1 - X0, 24), DIM, dist=10)

def s_plan(d, t):
    label(d, t, '01 / LET THE AGENT PLAN'); title(d, t, 'YOU ASK. IT PLANS.')
    a = prog(t, 0.7)
    box(d, (X0, 620 + (1 - a) * 20, X1, 720 + (1 - a) * 20), a, fill=(238, 238, 252), outline=ACC)
    T(d, (X0 + 26, 650 + (1 - a) * 20), 'PROMPT', M(22, 800), ACC, a)
    T(d, (X0 + 26, 680 + (1 - a) * 20), '"Create a step-by-step plan for this task."', fit(lambda z: S(z, 600), '"Create a step-by-step plan for this task."', X1 - X0 - 52, 32), INK, a)
    arrow(d, (X0 + X1) / 2, 728, (X0 + X1) / 2, 728 + 50 * prog(t, 1.4), ACC, prog(t, 1.4), 5)
    # plan steps appear; text revealed only at "run time"
    steps = ['Search for sources', 'Pull out key facts', 'Draft the summary', 'Check and finalize']
    for i, st in enumerate(steps):
        s = 1.8 + i * 0.5; a = prog(t, s); y = 800 + i * 82
        box(d, (X0, y, X1, y + 66), a)
        node(d, X0 + 40, y + 33, 20, str(i + 1), ACC, a, fill=ACC, f=M(22, 800))
        rev = t > 5.6 + i * 0.15
        if rev: T(d, (X0 + 80, y + 33), st, S(32, 600), INK, a, 'lm')
        else:
            T(d, (X0 + 80, y + 33), '? ? ?', M(30, 800), DIM, a * 0.8, 'lm')
    a = prog(t, 6.2)
    T(d, (X0, 1146 + (1 - a) * 10), "You don't see the plan until run time.", S(34, 700), DIM, a)
    # control vs range slider
    a = prog(t, 8.4); y = 1250
    if a > 0:
        T(d, (X0, y), 'CONTROL', M(26, 800), DIM, a, 'lm'); T(d, (X1, y), 'RANGE', M(26, 800), ACC, a, 'rm')
        sx0, sx1 = X0 + 150, X1 - 120
        d.rounded_rectangle((sx0, y - 6, sx1, y + 6), 6, fill=C(LINE, a))
        k = 0.2 + 0.65 * ease((t - 8.8) / 1.6); kx = sx0 + (sx1 - sx0) * k
        d.rounded_rectangle((sx0, y - 6, kx, y + 6), 6, fill=C(ACC, a))
        d.ellipse((kx - 22, y - 22, kx + 22, y + 22), fill=C(WHITE, a), outline=C(ACC, a), width=5)
    rise(d, t, 10.2, (X0, 1310), 'LESS CONTROL, MORE RANGE.', fit(D, 'LESS CONTROL, MORE RANGE.', X1 - X0, 80), INK)

def s_format(d, t):
    label(d, t, '02 / WHAT LANGUAGE IS THE PLAN IN?'); title(d, t, 'PICK A FORMAT')
    rows = [('PLAIN TEXT', ['First search the web for', 'sources, then summarize...'], 0.34, 'LESS CLEAR', DIM, 1.6),
            ('MARKDOWN', ['1. Search the web', '2. Summarize findings'], 0.67, 'CLEARER', ACC2, 4.4),
            ('JSON', ['{"step": 1, "tool": "search",', ' "query": "sources"}'], 1.0, 'MOST CLEAR', GOOD, 7.0)]
    for i, (name, code, clar, verdict, col, s) in enumerate(rows):
        a = prog(t, s); y = 630 + i * 212 + (1 - a) * 24
        box(d, (X0, y, X1, y + 196), a)
        T(d, (X0 + 26, y + 22), name, D(48), INK, a)
        T(d, (X1 - 26, y + 34), verdict, M(24, 800), col, a, 'ra')
        for j, ln in enumerate(code): T(d, (X0 + 26, y + 84 + j * 36), ln, M(27, 500), DIM if i == 0 else INK, a)
        bx0, bx1, by = X0 + 26, X1 - 26, y + 176
        d.rounded_rectangle((bx0, by - 5, bx1, by + 5), 5, fill=C(LINE, a))
        if a > 0: d.rounded_rectangle((bx0, by - 5, bx0 + max(10, (bx1 - bx0) * clar * prog(t, s + 0.4, 0.9)), by + 5), 5, fill=C(col, a))
    para(d, t, 9.2, X0, 1290, 'The more structured the plan, the more cleanly your code can parse out what to do next.', S(36, 700), INK, X1 - X0, 46)

CODE = ['import pandas as pd', 'df = pd.read_excel("sales.xlsx")', 'q4 = df[df.quarter == "Q4"]', 'answer = q4.revenue.sum()']
def s_code(d, t):
    label(d, t, '03 / EVEN BETTER: PLAN IN CODE'); title(d, t, 'LET IT WRITE PYTHON')
    a = prog(t, 0.6)
    T(d, (X0, 612 + (1 - a) * 10), 'ASK: "What were Q4 sales in this spreadsheet?"', fit(lambda z: S(z, 700), 'ASK: "What were Q4 sales in this spreadsheet?"', X1 - X0, 32), INK, a)
    a = prog(t, 1.0); y0 = 692
    sand = t > 8.8
    if a > 0:
        d.rounded_rectangle((X0, y0, X1, y0 + 290), 20, fill=C((24, 28, 44), a))
        for k, cc in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]): d.ellipse((X0 + 24 + k * 30, y0 + 20, X0 + 40 + k * 30, y0 + 36), fill=C(cc, a))
        T(d, (X1 - 24, y0 + 28), 'plan.py', M(22, 500), (150, 160, 190), a, 'rm')
        chars = int(max(0, t - 1.4) * 34); used = 0
        for j, ln in enumerate(CODE):
            show = ln[:max(0, chars - used)]; used += len(ln)
            col = (190, 180, 255) if ln.startswith('import') else (235, 238, 248)
            T(d, (X0 + 30, y0 + 72 + j * 50), show, M(29, 500), col, a)
            if 0 < len(show) < len(ln) and int(t * 4) % 2 == 0: d.rectangle((X0 + 32 + tw(show, M(29, 500)), y0 + 72 + j * 50, X0 + 46 + tw(show, M(29, 500)), y0 + 106 + j * 50), fill=C(ACC2, a))
    if sand:
        k = prog(t, 8.8, 0.5); pad = 18
        for x in range(int(X0 - pad), int(X1 + pad), 28):  # dashed sandbox border
            d.line((x, y0 - pad, min(x + 16, X1 + pad), y0 - pad), fill=C(GOOD, k), width=5); d.line((x, y0 + 290 + pad, min(x + 16, X1 + pad), y0 + 290 + pad), fill=C(GOOD, k), width=5)
        for y in range(int(y0 - pad), int(y0 + 290 + pad), 28):
            d.line((X0 - pad, y, X0 - pad, min(y + 16, y0 + 290 + pad)), fill=C(GOOD, k), width=5); d.line((X1 + pad, y, X1 + pad, min(y + 16, y0 + 290 + pad)), fill=C(GOOD, k), width=5)
        chip(d, X1 - 200, y0 + 290 + pad - 23, 'SANDBOX', GOOD, k, solid=True)
    pts = [('Taps huge libraries of functions it already knows', 5.0), ('Usually more effective than JSON or text plans', 6.8)]
    for i, (p_, s) in enumerate(pts):
        a = prog(t, s); y = 1036 + i * 106
        check(d, X0 + 4, y + 24, GOOD, a)
        for j, ln in enumerate(wrap(p_, S(36, 700), X1 - X0 - 70)[:2]): T(d, (X0 + 62, y + j * 44 + (1 - a) * 14), ln, S(36, 700), INK, a)
    rise(d, t, 9.2, (X0, 1262), 'BEST PRACTICE:', M(26, 800), GOOD)
    rise(d, t, 9.4, (X0, 1290), 'RUN IT IN A SANDBOX.', fit(D, 'RUN IT IN A SANDBOX.', X1 - X0, 88), INK)

ROLES = [('RESEARCHER', 'R'), ('ANALYST', 'A'), ('DESIGNER', 'D'), ('EXECUTIVE', 'E')]
def s_team(d, t):
    label(d, t, '04 / MULTI-AGENT'); title(d, t, 'HIRE A TEAM OF AGENTS')
    a = prog(t, 0.7); cx = (X0 + X1) / 2
    box(d, (cx - 250, 640 + (1 - a) * 20, cx + 250, 740 + (1 - a) * 20), a, fill=ACC, outline=ACC)
    T(d, (cx, 690 + (1 - a) * 20), 'RESEARCH REPORT', D(56), WHITE, a, 'mm')
    cw = (X1 - X0 - 3 * 20) / 4
    for i, (role, ic) in enumerate(ROLES):
        s = 7.2 + i * 0.6; a = prog(t, s); x = X0 + i * (cw + 20); y = 860 + (1 - a) * 24
        arrow(d, cx, 744, x + cw / 2, 852, LINE, prog(t, s - 0.3), 3, 12)
        box(d, (x, y, x + cw, y + 230), a)
        node(d, x + cw / 2, y + 85, 50, ic, ACC, a)
        T(d, (x + cw / 2, y + 185), role, fit(lambda z: M(z, 800), role, cw - 20, 22), INK, a, 'mm')
        if t > 12.2 + i * 0.3: check(d, x + cw - 50, y + 30, GOOD, prog(t, 12.2 + i * 0.3, 0.3), 0.7)
    para(d, t, 1.0, X0, 1140, 'Break a complex task into roles, just like hiring people for the different pieces.', S(38, 700), INK, X1 - X0, 48)
    rise(d, t, 12.0, (X0, 1290), 'BUILD ONE SUBTASK AT A TIME.', fit(D, 'BUILD ONE SUBTASK AT A TIME.', X1 - X0, 76), ACC)

def pat_linear(d, t, y, a, cx0, cx1):
    xs = [cx0 + k * (cx1 - cx0) / 3 for k in range(4)]
    for k in range(3): arrow(d, xs[k] + 30, y, xs[k + 1] - 34, y, INK, a, 4, 12)
    for k, x in enumerate(xs): node(d, x, y, 28, 'RADE'[k], ACC, a, f=D(30))
    ph = (t * 0.5) % 1; px = xs[0] + (xs[3] - xs[0]) * ph
    if a > 0: d.rounded_rectangle((px - 9, y - 45, px + 9, y - 27), 4, fill=C(ACC2, a))
def pat_hier(d, t, y, a, cx0, cx1):
    mx = (cx0 + cx1) / 2; xs = [cx0 + 40, mx, cx1 - 40]
    for x in xs: d.line((mx, y - 38, x, y + 38), fill=C(INK, a), width=4) if a > 0 else None
    node(d, mx, y - 48, 32, 'M', WHITE, a, fill=ACC, f=D(34))
    for k, x in enumerate(xs): node(d, x, y + 50, 26, 'RAD'[k], ACC, a, f=D(28))
    k = int(t * 0.8) % 3; ph = (t * 0.8) % 1; px = mx + (xs[k] - mx) * ph; py = y - 30 + 70 * ph
    if a > 0: d.rounded_rectangle((px - 9, py - 9, px + 9, py + 9), 4, fill=C(ACC2, a))
def pat_all(d, t, y, a, cx0, cx1):
    mx = (cx0 + cx1) / 2; pts = [(mx, y - 62), (cx1 - 30, y), (mx, y + 62), (cx0 + 30, y)]
    for i in range(4):
        for j in range(i + 1, 4):
            if a > 0: d.line((*pts[i], *pts[j]), fill=C(INK, a * 0.7), width=3)
    for k, (x, yy) in enumerate(pts): node(d, x, yy, 26, 'RADE'[k], ACC, a, f=D(28))
    rnd = random.Random(int(t * 2.2))
    for m in range(3):
        i, j = rnd.sample(range(4), 2); ph = (t * 2.2) % 1
        px = pts[i][0] + (pts[j][0] - pts[i][0]) * ph; py = pts[i][1] + (pts[j][1] - pts[i][1]) * ph
        if a > 0: d.rounded_rectangle((px - 8, py - 8, px + 8, py + 8), 4, fill=C(RED, a))

def s_patterns(d, t):
    label(d, t, '05 / THE KEY DESIGN DECISION'); title(d, t, 'HOW DO AGENTS TALK?')
    rows = [('1  LINEAR', 'One hands off to the next.', 'PREDICTABLE', GOOD, 4.2, pat_linear),
            ('2  HIERARCHY', 'A manager agent coordinates (or a deep hierarchy).', 'BALANCED', ACC2, 8.4, pat_hier),
            ('3  ALL-TO-ALL', 'Everyone talks to everyone.', 'LESS PREDICTABLE', RED, 11.8, pat_all)]
    for i, (nm, desc, verdict, col, s, fn) in enumerate(rows):
        a = prog(t, s); y = 620 + i * 228 + (1 - a) * 20
        nxt = rows[i + 1][4] if i < 2 else 99
        act = s <= t < nxt
        box(d, (X0, y, X1, y + 212), a, fill=(242, 241, 255) if act else CARD, outline=ACC if act else LINE, width=4 if act else 3)
        T(d, (X0 + 26, y + 22), nm, D(50), INK, a)
        for j, ln in enumerate(wrap(desc, S(26, 600), 410)[:2]): T(d, (X0 + 26, y + 90 + j * 32), ln, S(26, 600), DIM, a)
        T(d, (X0 + 26, y + 186), verdict, M(22, 800), col, a, 'lm')
        fn(d, t, y + 106, a, X0 + 470, X1 - 40)
    para(d, t, 17.6, X0, 1312, 'Like org design: people or agents, communication gets complex fast.', S(34, 700), INK, X1 - X0, 44)

SHEET = [('PLAN', 'Agent writes the steps. Less control, more range.'),
         ('FORMAT', 'Text < Markdown < JSON. Code is usually best.'),
         ('CODE', 'Huge function libraries. Always use a sandbox.'),
         ('TEAM', 'Split work into roles. Build one subtask at a time.'),
         ('TALK', 'Linear · Hierarchy · All-to-all')]
SHEET_CUES = [2.6, 7.0, 10.4, 13.0, 16.4, 20.7]   # when each row is spoken in the sum-up take (last = end of rows)
def s_sheet(d, t):
    label(d, t, 'SUM IT UP')
    title(d, t, 'AUTONOMOUS AGENT PATTERNS', size=74)
    y = 600
    for i, (k, v) in enumerate(SHEET):
        a = prog(t, 0.7 + i * 0.25)
        act = SHEET_CUES[i] <= t < SHEET_CUES[i + 1]; done = t >= SHEET_CUES[i + 1]
        box(d, (X0, y, X1, y + 112), a, fill=(242, 241, 255) if act else CARD, outline=ACC if act else LINE, width=4 if act else 3)
        T(d, (X0 + 24, y + 56), k, M(26, 800), ACC, a, 'lm')
        ls = wrap(v, S(32, 600), X1 - X0 - 270)
        col = INK if (act or done or t < SHEET_CUES[0]) else DIM
        for j, ln in enumerate(ls[:2]): T(d, (X0 + 190, y + 56 + (j - (len(ls[:2]) - 1) / 2) * 40), ln, S(32, 600), col, a, 'lm')
        if done: check(d, X1 - 50, y + 56, GOOD, prog(t, SHEET_CUES[i + 1], 0.3), 0.7)
        y += 126
    a = prog(t, 20.7)
    T(d, (X0, 1250 + (1 - a) * 20), 'THAT\u2019S ALL 5 MODULES.', D(64), INK, a)
    T(d, (X0, 1322 + (1 - a) * 20), 'FOLLOW FOR MORE.', D(64), ACC, a)
    T(d, (X0, 1404), 'Source: my notes, Agentic AI Module 5 (DeepLearning.AI)', S(20, 500), DIM, prog(t, 2.0))

SCENES = [s_hook, s_plan, s_format, s_code, s_team, s_patterns, s_sheet]
