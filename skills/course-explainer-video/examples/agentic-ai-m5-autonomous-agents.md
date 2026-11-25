# Agentic AI, Module 5: Patterns for autonomous agents

Final video (kept outside the repo): `agentic-ai-m5-voiced.mp4` (1:53, 1080x1920, your voiceover, Presidio photo background).
Rendered with the `course-explainer-video` skill: `skills/course-explainer-video/examples/agentic-ai-m5-autonomous-agents.py`.

## Voiceover as recorded
| Start | Scene | Your take |
|---|---|---|
| 0:00 | Hook | What if your AI wrote its own plan? Here are the patterns for autonomous agents, from my notes on Module 5 of Andrew Ng's Agentic AI course. |
| 0:08 | 01 Let the agent plan | Instead of hard-coding every step, you prompt the agent to create a step-by-step plan. The catch is that you don't know what it will plan until run time. There's less control but more range. |
| 0:22 | 02 Pick a format | How it writes the plan matters. Plain text is the least clear, Markdown more clear, and JSON is the clearest, because your tools can parse exactly what needs to be done. |
| 0:35 | 03 Plan in code | Even better, let the model write code. It can pull from huge libraries of functions it already knows, so this usually beats JSON or text. The best practice is to run it in a sandbox. |
| 0:48 | 04 Multi-agent | Multi-agent means breaking a complex job into pieces, like hiring a team. A research report might require a researcher, an analyst and a designer. Build each subtask one at a time. |
| 1:03 | 05 How agents talk | Then the key design decision: how do they communicate? One, linear: each hands off to the next. Two, hierarchy: a manager agent coordinates. Three, all-to-all: everyone talks to everyone. That's the least predictable. Just like org design for people, it gets complex fast. |
| 1:26 | Sum it up | So, to sum it up: let the agent write the plan, but you trade some control for range. Have it write the plan in JSON, or better yet in code, and always run the code in a sandbox. For big jobs, split the work across a team of agents, then decide how they talk: linear, hierarchy, or all-to-all. That wraps up all five modules of Andrew Ng's Agentic AI course. |

## Caption (paste into TikTok)
Your AI agent can write its own plan. But should it plan in text, Markdown, JSON or code? And when you have a team of agents, how should they talk? 🧠 Notes from Module 5 of Andrew Ng's Agentic AI course. That wraps up all five modules, with a quick sum-up at the end.

#AgenticAI #AIAgents #LearnAI #MultiAgent #TechTok #AIexplained #LittlePandaEducation

## Illustrative (not from the notes)
- The four plan steps, the spreadsheet code (`sales.xlsx`, Q4) and the role letters on screen are made-up examples.
