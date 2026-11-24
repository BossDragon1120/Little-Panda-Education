# Deal Decoded: Script Writer

**What it does:** turns a $1B+ M&A press release into a 90-second TikTok that a non-finance viewer can follow. It explains what each company does through everyday analogies, gives a synergy hypothesis, shows why the deal touches the viewer's life, names the risk to watch, and ends with a deal card worth screenshotting.

**Why I built it:** I spend my working days on M&A integration. Most deal coverage is written for bankers. I wanted a repeatable format that makes deals understandable for everyone else, without dumbing down the numbers.

**Design choices**
- **Fixed six-part structure.** Every episode has the same shape, so viewers know what's coming and the script is fast to write.
- **Analogies come in pairs from the same world**, so the buyer and target make sense together.
- **The synergy section is labeled a hypothesis.** Company synergy targets are projections, and the deal card says so.
- **Every figure comes from the primary source** (8-K or press release). Fields that weren't disclosed are dropped, not guessed.

**Used by:** the [`deal-decoded-scout`](../../agents/deal-decoded-scout.md) agent, which finds deals and hands each one to this skill.
