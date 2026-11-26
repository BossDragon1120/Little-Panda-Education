# 🐼 Little Panda Education

**Little Panda Education** is a TikTok account that teaches **Business, Tech and AI** in short videos. This repo holds the Claude agents and skills that produce it: finding the story, writing the script, building vertical slides, assembling video with my own voiceover, and (later) posting and learning from engagement.

## Inputs

| Input | Where it comes from | What it becomes |
|---|---|---|
| 📰 **What's happening** | News and filings, watched by scout agents (e.g. new $1B+ M&A deals) | Timely explainers such as Deal Decoded |
| 📚 **What I'm learning** | My notes repo, [Upskilling & Subject Matter Expertise](https://github.com/BossDragon1120/Upskilling-and-Subject-Matter-Expertise), with notes from courses and deep dives | Evergreen explainers: if I learned it, I teach it |
| 📖🎧 **What I'm reading & hearing** | [Book & Podcast Whispers](https://github.com/BossDragon1120/Book-and-Podcast-Whispers): monthly book reflections and daily M&A Science notes | Ideas from books and practitioners, through my own lens |

The learning inputs are the flywheel: every course I take and every book I read produces notes, and those notes become videos.

## Pipeline

```
 ① INPUTS                     ② SCRIPT        ③ SLIDES          ④ ASSEMBLE         ⑤ PUBLISH & LEARN
 ┌──────────────────────┐
 │ 📰 news scouts       │──┐
 │   (agents)           │  │   ┌──────────┐   ┌────────────┐   ┌──────────────┐   ┌────────────────┐
 └──────────────────────┘  ├─▶ │ talk     │ ▶ │ 9:16 TikTok│ ▶ │ slides + my  │ ▶ │ post, then     │
 ┌──────────────────────┐  │   │ track    │   │ slides     │   │ audio → MP4  │   │ track what     │
 │ 📚📖 learning-notes  │──┘   │ (skills) │   │ (skills)   │   │ (agent)      │   │ works (agents) │
 │   intake (agent)     │      └────┬─────┘   └────────────┘   └──────▲───────┘   └───────┬────────┘
 └──────────────────────┘           └──── 🎙️ I review & record ───────┘                   │
            ▲                                                                              │
            └────────────────── engagement data shapes what gets made next ◀──────────────┘
```

**Why split it up this way:** **agents** handle stages that run on their own, make decisions or call other pieces (scouting, intake, assembling, posting). **Skills** hold the house formats: how a Deal Decoded script is shaped, how a Course Explainer looks. Formats change often and agents change rarely, so keeping them apart means a format change never touches an agent.

## Built for TikTok first
Every format is designed for TikTok before any other platform:
- **Vertical 9:16**, so slides and video are built for a phone screen.
- **Hook in the first seconds**, with an on-screen line, because people decide within a couple of seconds whether to keep watching.
- **On-screen text throughout**, because many people watch with the sound off.
- **Key content kept clear of TikTok's on-screen buttons and caption area.**

These layout rules live inside every slide and video skill (see the `TikTok layout` section of the [skill template](templates/skill/SKILL.md)), not in a separate shared skill, so each builder works on its own.
- **60–90 seconds**: one idea per video, ending with something worth saving or screenshotting.

## Subjects and series

| Subject | Series | Input | What it is | Look |
|---|---|---|---|---|
| **Business** | [**Deal Decoded**](series/deal-decoded.md) | 📰 News | $1B+ M&A announcements explained for people who don't work in finance | Navy + lime |
| **AI · Tech · Business** | [**Course Explainers**](series/course-explainers.md) | 📚 Notes | The key ideas from a course module I just took | Frosted text panel over a dusk gradient, one animated diagram per idea |
| **Any** | _Book series (name TBD)_ | 📖 Books | One idea from this month's book and what it changed in my thinking | |
| **Tech** | _coming_ | 📰 / 📚 | _To be defined_ | |

## Components

| Stage | Component | Type | Feeds | Status |
|---|---|---|---|---|
| ① Input | [`deal-decoded-scout`](agents/deal-decoded-scout.md) | Agent | Deal Decoded | ✅ Running daily |
| ① Input | [`learning-notes-intake`](agents/learning-notes-intake.md) | Agent | Course Explainers, Books | ✅ Built (waiting on notes) |
| ② Script | [`deal-decoded-script`](skills/deal-decoded-script) | Skill | Deal Decoded | ✅ Built |
| ② Script | `course-explainer-script` | Skill | Course Explainers | 🛠️ Planned |
| ③ Slides + ④ Video | [`deal-decoded-video`](skills/deal-decoded-video) | Skill | Deal Decoded | ✅ Built (silent video; voiceover added by me) |
| ③ Slides + ④ Video | [`course-explainer-video`](skills/course-explainer-video) | Skill | Course Explainers | ✅ Built (silent video; voiceover added by me) |
| ④ Assemble | `video-assembler` | Agent | All | 🛠️ Planned |
| ⑤ Publish | `tiktok-poster` | Agent | All | 💡 Idea |
| ⑤ Learn | `engagement-tracker` | Agent | All, plus inputs | 💡 Idea |

**How the notes become videos:** in the notes repo, each `## Teachable moments` bullet and each glossary term in a note marked `status: done` is a candidate video. `learning-notes-intake` picks the best ones, sends each to the matching script skill, and sets the note's `video` field so nothing gets made twice. See the [notes repo README](https://github.com/BossDragon1120/Upskilling-and-Subject-Matter-Expertise#from-notes-to-videos) for the full set of rules.

## Install

**Claude Code (whole pipeline as a plugin):**
```
/plugin marketplace add BossDragon1120/Little-Panda-Education
/plugin install little-panda-education@little-panda-education
```

**Claude Code (one piece at a time):** copy `skills/<name>/` to `~/.claude/skills/`, or copy `agents/<name>.md` to `~/.claude/agents/`.

**Claude.ai / Claude desktop:** zip a skill folder and upload it under *Settings → Capabilities → Skills*.

## Repo layout

```
agents/            stages that run on their own (scouts, notes intake, assembler, poster, tracker)
skills/            house formats (scripts and slides for each series)
series/            premise, look and status for each series
templates/         starting points for new skills and agents
.claude-plugin/    plugin and marketplace manifests
scripts/validate.py   checks every skill and agent's frontmatter (runs in CI)
```

## Principles
- **A human is in the loop on purpose.** Agents draft; I review and record every voiceover. Nothing posts without me.
- **TikTok first.** Vertical, hook up front, readable with the sound off.
- **Teach what I learn.** My course notes become videos, so learning and making content reinforce each other.
- **Primary sources only.** Figures come from filings and press releases. If a number wasn't disclosed, it isn't shown.
- **No panda on slides.** The name stays; the mascot doesn't appear on screen in any series.
- **One format per series, kept in a skill**, so each series stays consistent and is easy to change in one place.

## About

Built by a strategy and M&A integration professional who works on AI adoption. Little Panda Education is my working lab for designing agentic workflows that keep a human in the loop.

MIT licensed.
