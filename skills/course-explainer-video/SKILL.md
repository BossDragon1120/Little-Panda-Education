---
name: course-explainer-video
description: Use when turning course or learning notes into a Course Explainer (or AI Vocab) TikTok. Renders a 60-90 second, 1080x1920, silent MP4 in the house frosted-panel look, with animated diagrams, timed for the creator's voiceover.
---

# Course Explainer: video renderer

The go-forward standard for Little Panda Education explainers made from notes (Course Explainers, and AI Vocab until it has its own skill). It turns one module's notes into a vertical video with no audio: the creator records the voiceover to the scene start times.

- [`course_explainer.py`](course_explainer.py) holds the look, the drawing helpers and the render loop. Change it only to change the look for every video.
- Each video is one small Python file that defines `META`, `DUR` and `SCENES`. Start from [`examples/agentic-ai-m5-autonomous-agents.py`](examples/agentic-ai-m5-autonomous-agents.py).

## Look
- **Background:** a soft dusk gradient (navy to warm orange) with blurred bokeh circles, generated in code. A photo can replace it with `BG=/path/photo.jpg`, but the gradient is the default.
- **Frosted panel:** a blurred, white-washed rounded panel (x 40–984, y 395–1445) holds all content. Text inside runs x 84–940, clear of TikTok's right-side buttons and caption.
- **Colors:** ink `#121A2C` text, indigo `#4F46E5` accent, orange `#EC7828` for movement and the middle option, green `#10966A` for good or safe, red `#D63C3C` for risk, gray `#5C667A` for secondary text.
- **Type:** Anton headlines, JetBrains Mono labels and code, Inter body.
- **Fixed chrome** on the photo above the panel: `COURSE EXPLAINER` at left, course and module (e.g. `AGENTIC AI · M5`) at right, and a segmented progress bar with one segment per scene. Scenes fade in over 0.2 s.
- No panda, no logos, no photos of real people.

## Video shape (default, 7 scenes, about 88 s)
| Scene | What it does |
|---|---|
| Hook (≈7 s) | Kicker with module number, a three-line question headline (last line in accent), 2–3 topic chips, one plain sentence, source line |
| 3–5 idea scenes (12–16 s each) | Label `0N / ...`, one Anton title, then **one animated diagram** that shows the idea (steps appearing, bars filling, code typing, nodes passing packets), then a short takeaway line or a big Anton punchline |
| Cheat sheet (≈13 s) | `SCREENSHOT THIS` chip, 4–6 rows of `LABEL · one line`, `FOLLOW FOR THE / NEXT MODULE.` and a source line naming the course and module |

One idea per scene. Show it, don't list it: each scene needs a moving diagram, not just bullets.

## Helpers you write scenes with
`label(d, t, text)`, `title(d, t, text)`, `rise(...)` (fade-and-rise text), `para(...)` (wrapped text), `box(...)` (white card), `chip(...)`, `node(...)` (circle with a letter), `arrow(...)`, `check(...)`, `fit(font, text, maxw, size)` (shrinks to fit), `prog(t, start, dur)` (eased 0→1). Every scene is `def s_name(d, t)` where `t` is seconds into the scene and `d` draws on a transparent layer; pass the fade value `a` as the alpha to every draw call.

## Steps
1. **Get the ideas.** Read the module note (in Upskilling-and-Subject-Matter-Expertise, or notes the creator pastes). Pick the 3–5 ideas that teach best. Put only claims from the notes on screen; mark any example you invent (sample code, sample steps, role names) as illustrative when you hand off.
2. **Install fonts** (once per machine), same as `deal-decoded-video`:
   ```bash
   mkdir -p ~/dd-fonts && cd ~/dd-fonts
   for p in anton jetbrains-mono inter; do npm pack @fontsource/$p >/dev/null 2>&1; mkdir -p x && tar xzf fontsource-$p-*.tgz -C x && rm -rf fontsource-$p && mv x/package fontsource-$p && rmdir x; done
   ```
   Needs Python 3 with Pillow, and ffmpeg.
3. **Write the video file** `examples/<course>-m<N>-<slug>.py`: copy the example, set `META` (`course_tag`, `output`), `DUR`, and rewrite the scenes. Keep the hook and cheat sheet shapes.
4. **Preview.** `python3 course_explainer.py examples/<file>.py stills <one time near the end of each scene>`, put the frames side by side and look. Check for overlapping text, anything below y≈1430, and empty panels. Fix and check again.
5. **Render.** `python3 course_explainer.py examples/<file>.py render` (scenes render in parallel, about 40 s).
6. **Hand off.** Spot-check a few frames from the MP4. Give the creator the scene start times, a suggested voiceover line per scene, and a TikTok caption with hashtags. Flag anything illustrative.

## Guardrails
- Nothing on screen that isn't in the notes, except clearly illustrative examples, which you flag.
- Name the course and module on screen (hook and source line).
- Don't commit rendered MP4s to this repo.
