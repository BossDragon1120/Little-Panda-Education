# 🐼 Little Panda Education

A set of Claude agents and skills that turn **AI and M&A topics into short educational videos**. Each stage of the pipeline is its own skill or agent: finding stories, writing scripts, building slides, assembling video and, later, posting and tracking engagement. I stay in the loop where it matters: reviewing scripts and recording my own voice.

## Pipeline

```
  ① SCOUT          ② SCRIPT          ③ SLIDES            ④ ASSEMBLE           ⑤ PUBLISH & LEARN
  (agents)         (skills)          (skills)            (agent)              (agents)
 ┌──────────┐    ┌────────────┐    ┌──────────────┐    ┌────────────────┐    ┌──────────────────┐
 │ find the │ →  │ write the  │ →  │ build slides │ →  │ slides + my    │ →  │ post, then track │
 │ story    │    │ talk track │    │ per series   │    │ audio → video  │    │ engagement       │
 └──────────┘    └────────────┘    └──────────────┘    └────────────────┘    └──────────────────┘
                        │                                     ▲
                        └──────── 🎙️ I review & record ───────┘
```

**Why split it up this way:** **agents** handle stages that run on their own, make decisions or call other pieces (scouting, assembling, posting). **Skills** hold the house formats: how a Deal Decoded script is shaped, how a vocab slide looks. Formats change often and agents change rarely, so keeping them apart means a format change never touches an agent.

## Series

| Series | What it is | Look |
|---|---|---|
| [**Deal Decoded**](series/deal-decoded.md) | $1B+ M&A announcements explained for non-bankers | Navy + green |
| [**AI Vocab**](series/ai-vocab.md) | One AI term per video, in plain language | Golden Gate Bridge photography backgrounds |
| [**Course Explainers**](series/course-explainers.md) | Module-by-module summaries of AI courses | Its own style |

## Components

| Stage | Component | Type | Series | Status |
|---|---|---|---|---|
| ① Scout | [`deal-decoded-scout`](agents/deal-decoded-scout.md) | Agent | Deal Decoded | ✅ Running daily |
| ② Script | [`deal-decoded-script`](skills/deal-decoded-script) | Skill | Deal Decoded | ✅ Built |
| ② Script | `ai-vocab-script` | Skill | AI Vocab | 🛠️ Planned |
| ② Script | `course-explainer-script` | Skill | Course Explainers | 🛠️ Planned |
| ③ Slides | `deal-decoded-slides` | Skill | Deal Decoded | 🛠️ Planned |
| ③ Slides | `ai-vocab-slides` | Skill | AI Vocab | 🛠️ Planned |
| ③ Slides | `course-explainer-slides` | Skill | Course Explainers | 🛠️ Planned |
| ④ Assemble | `video-assembler` | Agent | All | 🛠️ Planned |
| ⑤ Publish | `tiktok-poster` | Agent | All | 💡 Idea |
| ⑤ Learn | `engagement-tracker` | Agent | All | 💡 Idea |

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
agents/            stages that run on their own (scout, assembler, poster, tracker)
skills/            house formats (scripts and slides for each series)
series/            premise, look and status for each series
templates/         starting points for new skills and agents
.claude-plugin/    plugin and marketplace manifests
scripts/validate.py   checks every skill and agent's frontmatter (runs in CI)
```

## Principles
- **A human is in the loop on purpose.** Agents draft; I review and record every voiceover. Nothing posts without me.
- **Primary sources only.** Figures come from filings and press releases. If a number wasn't disclosed, it isn't shown.
- **One format per series, kept in a skill**, so each series stays consistent and is easy to change in one place.

## About

Built by a strategy and M&A integration professional who works on AI adoption. Little Panda Education is my working lab for designing agentic workflows that keep a human in the loop.

MIT licensed.
