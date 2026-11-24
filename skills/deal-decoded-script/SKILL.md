---
name: deal-decoded-script
description: Use when writing a Deal Decoded TikTok script about an M&A announcement. Produces a 75–90 second talk track, an on-screen deal card, a caption, hashtags and sources.
---

# Deal Decoded: script writer

Turns one M&A announcement into a short-form video script that explains the deal to a general audience. Viewers should finish knowing what both companies do, why the deal might make sense, and why it touches their life.

## Inputs
- Buyer, target, and the primary source: the press release, 8-K or merger agreement. If no primary source is given, find it before writing.

## 1. Gather the facts (primary sources first)
Pull from the press release or 8-K, never from memory:
- value and structure (cash/stock mix), price per share and premium
- ownership after close, expected close date and required approvals
- synergy targets (cost/revenue, timeframe), scale (combined revenue, customers, employees)
- leadership after close, and any customer overlap the companies disclose

**Never invent a figure.** If a field wasn't disclosed, leave it out.

## 2. Talk track (75–90 s at ~150 words/min, about 190–225 words)
Use these timestamped sections, in this order:

| # | Section | What it does |
|---|---|---|
| 0 | **Hook** (0–5 s) | A surprising angle on the deal, plus a short **on-screen line** |
| 1 | **Who's buying** | What the buyer does, through an everyday analogy |
| 2 | **Who's being bought** | What the target does, through an analogy from the same world as #1 |
| 3 | **My synergy hypothesis** | Why 1 + 1 > 2, framed as *my* hypothesis, not fact |
| 4 | **Why this touches your life** | A concrete everyday scene (your bank login, your kid's school laptop…) |
| 5 | **What I'm watching** | The biggest integration or regulatory risk |
| 6 | **The deal card** | "Here's the deal card. Screenshot it." → voice over 3–4 headline numbers → "Follow for the next deal, decoded." |

Style: second person, short sentences, no jargon left unexplained, one idea per sentence.

## 3. Deal card (blockquote shown on screen at the end)
Fields, in this order, skipping any that weren't disclosed: **Value & structure · Terms & premium · Ownership after · Customer overlap · Synergy targets · Scale · Leadership · Expected close & approvals**. End with: *Synergy targets are company projections.*

## 4. Caption and hashtags
- Caption under ~300 characters, ending with `Deal card at the end 📌`.
- 6–9 hashtags, always including `#DealDecoded`, `#MergersAndAcquisitions` and both company names.

## 5. Output
One markdown file named `ma-<buyer>-<target>-talk-track.md` (lowercase, hyphens), with sections in this order: Talk track → Deal card → Caption → Hashtags → Sources (links to the primary filings or press releases).

## Check before delivering
- Every number in the talk track and deal card matches the primary source.
- Read-aloud length is 75–90 seconds.
- The synergy section is framed as a hypothesis, and the deal card ends with the caveat.
