#!/usr/bin/env python3
"""Fail if aider did not fill a generated blog entry.

Checks the frontmatter description and the prose of "## What is this about?"
(the attribution HTML comment is allowed, but real sentences must follow it).
Usage: validate-blog-entry.py <blog-file>
"""
import re
import sys


def validate(text: str) -> list[str]:
    errors = []
    m = re.search(r'^description:\s*"(.*)"\s*$', text, re.MULTILINE)
    description = m.group(1).strip() if m else ""
    if not description:
        errors.append("frontmatter description is empty")
    elif len(description) > 160:
        errors.append(f"description has {len(description)} chars (max 160)")

    m = re.search(r"^## What is this about\?\s*$(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    section = m.group(1) if m else ""
    prose = re.sub(r"<!--.*?-->", "", section, flags=re.DOTALL).strip()
    if not prose:
        errors.append('"## What is this about?" section has no prose')
    return errors


if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        problems = validate(f.read())
    for p in problems:
        print(f"::error file={path}::{p}")
    sys.exit(1 if problems else 0)
