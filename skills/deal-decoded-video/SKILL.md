---
name: deal-decoded-video
description: Use when turning a fact-checked Deal Decoded script into its TikTok video. Renders an 86-second, 1080x1920, silent MP4 in the series' navy and lime market-terminal style, timed to the script so the creator can record the voiceover.
---

# Deal Decoded: video renderer

Turns one Deal Decoded talk track (made by the [`deal-decoded-script`](../deal-decoded-script) skill) into a vertical video. The video has no audio: the creator records the voiceover to the script's timestamps.

The renderer is [`deal_decoded_video.py`](deal_decoded_video.py) in this folder. It reads a short JSON spec describing what goes on screen. Examples are in [`examples/`](examples).

## Look
- Navy `#0E1B33` background with a faint dot grid, electric lime `#D4FF3A` accent, cream text, coral red for risk, mint for checks.
- Anton headlines, JetBrains Mono labels, Inter body text.
- Fixed elements: blinking "DEAL DECODED" header with the episode number, a lime ticker scrolling real deal numbers (never stock prices), a seven-segment progress bar, and a lime wipe between sections.
- Content stays between y≈410 and y≈1430 and x 64–944, clear of TikTok's search bar, right-side buttons and caption.

## Scenes and timing (default)
| Start | Scene | Spec key |
|---|---|---|
| 0:00 | Hook: buyer, target, counting price, structure tags | `hook` |
| 0:07 | 01 / The buyer: headline, icon tiles or flow diagram, analogy, optional red callout | `buyer` |
| 0:20 | 02 / The target: same layout, optional big stat | `target` |
| 0:30 | 03 / My hypothesis: three cards that light up in turn | `hypothesis` |
| 0:50 | 04 / Why you care: a token travels through three steps, optional threat that gets blocked | `you` |
| 1:00 | 05 / What I'm watching: two rows plus a big red line | `watching` |
| 1:10 | 06 / The deal card: full-screen card, "SCREENSHOT THIS", follow line | `card` |

Change lengths with `durations` (seven values) and keep the script's timestamps in sync.

## Steps
1. **Get the facts.** Start from the deal's fact-checked talk track. Only put numbers on screen that appear in it. If there's no script yet, run `deal-decoded-script` first.
2. **Install fonts** (once per machine):
   ```bash
   mkdir -p ~/dd-fonts && cd ~/dd-fonts
   for p in anton jetbrains-mono inter; do npm pack @fontsource/$p >/dev/null 2>&1; mkdir -p x && tar xzf fontsource-$p-*.tgz -C x && rm -rf fontsource-$p && mv x/package fontsource-$p && rmdir x; done
   ```
   Set `FONT_DIR` to use another folder. Requires Python 3 with Pillow, and ffmpeg.
3. **Write the spec** `<buyer>-<target>.json`, starting from [`examples/crwd-zs.json`](examples/crwd-zs.json):
   - `episode`: next number in the series. `tickers`: stock tickers only if the sources confirm them, otherwise short names.
   - `ticker_items`: 4–6 facts from the deal card.
   - `hook.value` and `decimals`: the headline value. `tags`: 2–3 short structure facts.
   - `buyer` / `target`: `verb` + `what` form the second headline (`what` is lime); `sub` is an optional lime line. `visual` is `tiles` (3 or 6 items with `label`, `icon`, optional `alert: true` to flash red during the callout) or `flow` (people → `hub` → up to 4 `right` boxes, optional `blocked_label`). Add either a `callout` or a `stat`, not both.
   - Icons: laptop, server, phone, cloud, identity/person, data/database, factory, pill, lab, car, chart, globe, store, gear, money/bank, chip. Anything else draws its first letter in a box.
   - `hypothesis.cards`: three cards at 0.6 / 6.5 / 12.0 s, body about 110 characters or less.
   - `you`: two title lines, a 1–3 letter `token`, three `nodes` (the last one `final: true`), optional `threat`.
   - `watching.rows`: two rows (`pill` such as PENDING, `risk: true` for a red title), `big`: two punchy lines, `foot`: a small footnote.
   - `card.rows`: the deal card as `[LABEL, [line, line]]`, at most 2 lines each and 8 rows. `caveat` says which figures are projections and names the sources.
   - Keep `line` text under about 90 characters. Long text shrinks to fit, but short reads better.
4. **Preview.** `python3 deal_decoded_video.py spec.json stills 6 15 27 45 55 66 80`, put the frames side by side and look at them. Check for overlaps, text below y≈1430, and empty middles. Fix the spec and check again.
5. **Render.** `python3 deal_decoded_video.py spec.json render`. Scenes render in parallel and are joined without re-encoding (about 25 seconds).
6. **Check and hand off.** Look at a few frames from the finished MP4. Give the creator the scene start times, and flag anything on screen that's illustrative rather than factual.

## Guardrails
- Every figure on screen comes from the fact-checked script. Undisclosed fields are left off.
- Company projections (synergies, accretion) are labeled as projections on the card.
- No stock prices, logos or photos of real people.
