#!/usr/bin/env python3
"""校验每个 skill 的 SKILL.md frontmatter：name 与目录一致、description 非空。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "skills"
REQUIRED = ("name", "description")


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    block = text[4:end]
    fields = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields


def main():
    errors = []
    skills = sorted(p for p in ROOT.iterdir() if p.is_dir())
    if not skills:
        print("没有找到 skills/ 下的目录", file=sys.stderr)
        return 1
    for d in skills:
        md = d / "SKILL.md"
        if not md.exists():
            errors.append(f"{d.name}: 缺 SKILL.md")
            continue
        fm = frontmatter(md.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{d.name}: 没有 frontmatter")
            continue
        for key in REQUIRED:
            if not fm.get(key):
                errors.append(f"{d.name}: frontmatter 缺 {key}")
        if fm.get("name") and fm["name"] != d.name:
            errors.append(f"{d.name}: name 是 {fm['name']}，与目录不一致")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"ok: {len(skills)} 个 skill")
    return 0


if __name__ == "__main__":
    sys.exit(main())
