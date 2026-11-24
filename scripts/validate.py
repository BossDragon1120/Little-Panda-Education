#!/usr/bin/env python3
"""Check that every skill and agent has valid frontmatter (name + description)."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip().strip('"')
    return fields


targets = [(p, p.parent.name) for p in ROOT.glob("**/skills/*/SKILL.md") if "templates" not in p.parts]
targets += [(p, p.stem) for p in ROOT.glob("**/agents/*.md") if p.name != "README.md" and "templates" not in p.parts]

for path, expected in targets:
    rel = path.relative_to(ROOT)
    fm = frontmatter(path)
    if fm is None:
        errors.append(f"{rel}: missing --- frontmatter ---")
        continue
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        errors.append(f"{rel}: name '{name}' must be kebab-case")
    if name != expected:
        errors.append(f"{rel}: name '{name}' should match '{expected}'")
    if not desc:
        errors.append(f"{rel}: description is empty")
    elif len(desc) > 1024:
        errors.append(f"{rel}: description over 1024 chars")

for d in ROOT.glob("**/skills/*/"):
    if "templates" in d.parts:
        continue
    if not (d / "README.md").exists():
        errors.append(f"{d.relative_to(ROOT)}: add a README.md for portfolio readers")

print("\n".join(errors) or f"OK: {len(targets)} file(s) valid")
sys.exit(1 if errors else 0)
