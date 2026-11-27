---
name: animated-infographic
description: Use when the creator wants one animated TikTok infographic (not a video with voiceover) explaining a term or comparison in plain language. Renders a 1080x1920 frosted-panel loop (MP4), a still PNG, and one catchy title with a hashtag set.
---

# Animated infographic

One vertical infographic that explains one idea, with light animation: the content builds in over about 4 seconds, holds, fades and loops (12 s by default). It is the low-effort sibling of [`course-explainer-video`](../course-explainer-video): no script, no voiceover, no scene timing. The creator only needs to give a topic (and, if they like, a photo). You do the rest and hand back three files.

- [`animated_infographic.py`](animated_infographic.py) holds the look, the layout rules, reusable blocks and the render loop.
- Each infographic is one Python file that sets `META`, `PANEL_H` and `draw(d, t)`. Start from [`examples/silicon-vs-optics.py`](examples/silicon-vs-optics.py).

## Output
| File | What it's for |
|---|---|
| `<slug>.mp4` | The post: a silent 12 s loop, 1080x1920, 30 fps (about 2 MB). The creator adds a trending sound in TikTok if they want one. |
| `<slug>.png` | The fully built frame: the cover image, or a photo post. |
| `<slug>-caption.md` | One catchy title/caption, one hashtag set (8–10 tags), and a "check before posting" list of anything you guessed. |

## Photo carousel (teaser + answer)
When the creator wants stills instead of a loop, make a two-slide TikTok photo carousel from the same look. Example: [`examples/silicon-vs-optics-carousel/`](examples/silicon-vs-optics-carousel/).
- **Slide 1 is a short teaser only:** a four-line Anton question hook and a "Swipe for the answer" chip. No diagram, no table, nothing else. Size the panel to the content (about 650 tall) and keep it centered.
- **Slide 2 is the answer** in plain words: headline takeaway, one sentence, a `versus` table tied to things people use, a "why it matters" box, and the punchline.
- Add `· 1/2` and `· 2/2` to `topic_tag`. Set `chrome_pills: True` when the top of the photo is bright (sky), so the labels stay readable.
- Render each slide with `png` mode (built frame only). No MP4 is needed.
- **Accuracy over hype:** say "starting to", "often" and "more of" where the change is partial. Fact-check every line before calling it final, and list the softened claims in the caption file.

## Look (shared with course-explainer-video)
- **Photo background** the creator supplied (default: their bar photo). Crop it to hide clutter (a mouse, a cable, a stranger) with `bg_keep` (keep the top fraction), `bg_zoom`, `bg_dx`/`bg_dy`. Never move the panel to dodge clutter.
- **Frosted panel, see-through:** blur 12, white wash 120, cards at about 80% opacity, so the photo shows through. Panel x 40–984.
- **Panel centered top to bottom:** top = (1920 − `PANEL_H`) / 2, so equal photo shows above and below. The engine does this for you; don't hard-code y values, lay out from `top()`. 1280 is the usual height (y 320–1600).
- **Chrome** above the panel: series at left (e.g. `AI VOCAB`), topic at right, white mono on a soft top shade.
- **Colors:** ink `#121A2C`, indigo `#4F46E5` accent, orange `#EC7828`, green `#10966A` good, red `#D63C3C` risk, gray `#5C667A` secondary. **Type:** Anton headlines, Inter body, JetBrains Mono labels.
- No panda, no logos, no photos of real people.

## TikTok safe area
- Keep all content inside x 84–940: TikTok's like/comment/share rail covers x > ~960 from y 900 to 1650.
- TikTok's caption and username start around y 1550. With a centered 1280 panel the last line sits near y 1510–1560: keep it a short punchline, not information someone needs. The engine prints a note when the panel reaches that zone; centering still wins.
- Run `safe` mode: it shades those zones in red on the built frame so you can see what they would hide.

## Content rules (plain language, for a layman)
1. **Lead with one clear takeaway** as a two-line Anton headline (second line in accent), e.g. `SILICON THINKS. / LIGHT TALKS.`, then one plain sentence.
2. **One animated diagram that shows the idea** (things flowing, building, filling), not decoration.
3. **Tie every item to something people already use** ("seen in" / "you use it": a phone charger, Face ID, fiber internet).
4. **Say why it matters** in one short box, then a one-line punchline that restates the takeaway.
5. No jargon without a plain translation beside it. At most ~90 words on the panel.
6. Mark anything you're not sure of, any simplification, and any number not from a source in `META['guesses']`; it lands in the caption file's checklist.

## Blocks you build with
`headline(d, t, y, line1, line2, sub)`, `rows(d, t, y, items)` (toolbox list: name, tag, plain line, seen-in, icon, color), `versus(d, t, y, left, right, items)` (two-column comparison), `punchline(d, t, y, text, start)`, plus `card`, `chip`, `arrow`, `check`, `rise`, `para`, `fit`, `prog(t, start, dur)` (eased 0→1 for build-in) and `cyc(t, period)` (0→1 sawtooth for continuous motion). Pick periods that divide `META['loop']` so the loop has no jump. Pass the fade `a` to every draw call. The engine fades all content out in the last 0.6 s so the loop restarts cleanly.

## Steps
1. **Pick the takeaway.** From the topic (or a note in Upskilling-and-Subject-Matter-Expertise), write the one sentence a layman should remember. Choose the layout: `versus` for "X vs. Y", `rows` for "kinds of X".
2. **Install fonts** once per machine (same as the other skills):
   ```bash
   mkdir -p ~/dd-fonts && cd ~/dd-fonts
   for p in anton jetbrains-mono inter; do npm pack @fontsource/$p >/dev/null 2>&1; mkdir -p x && tar xzf fontsource-$p-*.tgz -C x && rm -rf fontsource-$p && mv x/package fontsource-$p && rmdir x; done
   ```
   Needs Python 3 with Pillow, and ffmpeg.
3. **Write the spec** `examples/<slug>.py`: copy the example, set `META` (title, topic tag, photo and crop, caption, hashtags, guesses) and write `draw`. Stagger build-in starts between about 0.1 s and 4 s.
4. **Preview.** `BG=photo.jpg OUT=out/<slug>.mp4 python3 animated_infographic.py examples/<slug>.py safe`, then `stills 1.5 3 11.7` for mid-build and fade frames. Look for overlaps, text in red zones, clutter showing in the photo, and empty space. Fix and look again.
5. **Render.** `... render` writes the MP4, PNG and caption file (about 15 s).
6. **Hand off** the three files with the caption and hashtags in the message, and list the guesses. Save the caption file next to the spec as `examples/<slug>.md`.

## Caption and hashtags
- One caption, under ~100 characters, that teases the takeaway in everyday words, with at most one emoji. A curiosity gap works: "Your AI chatbot thinks with electricity... but it's learning to talk with light 💡".
- 8–10 hashtags: the series tag (`#AIVocab`), 3–4 topic tags, 2–3 broad reach tags (`#TechTok`, `#LearnOnTikTok`, `#TechExplained`).

## Guardrails
- Nothing on screen you can't stand behind; simplifications are flagged in `guesses`.
- Don't commit rendered MP4s or PNGs (except the small `preview.png`) to this repo.
