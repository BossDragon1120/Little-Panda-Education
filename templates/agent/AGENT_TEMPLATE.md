---
name: agent-name-in-kebab-case
description: One or two sentences on WHEN Claude should hand work to this agent. Be specific; this text decides when the agent is used.
tools: Read, Grep, Glob, WebSearch, WebFetch
model: sonnet
---

You are a <role>. Your job is to <outcome>.

## Inputs you'll receive
- …

## How to work
1. …
2. …

## Output format
Return:
- **Summary:** 2–3 sentences
- **Findings:** …
- **Open questions:** …

## Guardrails
- Don't …
