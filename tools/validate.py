#!/usr/bin/env python3
"""Checks that the kit's spec, templates, agents, skills and links agree with each other."""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

KNOWN_TOOLS = frozenset(
    {"Read", "Grep", "Glob", "Edit", "Write", "Bash", "Agent", "WebFetch", "WebSearch", "NotebookEdit", "TodoWrite"}
)
FRONT_MATTER_KEYS = frozenset({"id", "part-of", "title", "owner", "status"})
DELIVERABLE_ID = re.compile(r"^D(0[1-9]|1[0-9]|20)$")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
FENCED_CODE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
INLINE_CODE = re.compile(r"`[^`\n]*`")
MARKDOWN_LINK = re.compile(r"\]\(([^)\s]+)\)")


@dataclass
class Report:
    """Collects problems so one run lists all of them."""

    problems: list[str] = field(default_factory=list)

    def add(self, path: Path | str, message: str) -> None:
        self.problems.append(f"{path}: {message}")


def read_front_matter(text: str) -> dict[str, str | list[str]] | None:
    """Returns the front-matter at the top of a Markdown file, or None when there is none.

    The kit's front-matter uses only scalar values and lists of scalars, so this reads that subset of YAML.
    """
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    values: dict[str, str | list[str]] = {}
    current_list: list[str] | None = None
    for line in text[4:end].splitlines():
        if line.startswith("  - ") and current_list is not None:
            current_list.append(line[4:].strip())
            continue
        key, separator, value = line.partition(":")
        if not separator or line.startswith(" "):
            return None
        if value.strip():
            values[key.strip()] = value.strip().strip('"')
            current_list = None
        else:
            current_list = []
            values[key.strip()] = current_list
    return values


def scalar(front: dict[str, str | list[str]], key: str) -> str:
    value = front.get(key, "")

    return value if isinstance(value, str) else ""


def visible_text(markdown: str) -> str:
    """Strips HTML comments, fenced code blocks and code spans, where the spec says IDs are not read."""
    without_comments = HTML_COMMENT.sub("", markdown)
    without_fences = FENCED_CODE.sub("", without_comments)
    return INLINE_CODE.sub("", without_fences)


def markdown_files(root: Path) -> Iterator[Path]:
    yield from sorted(p for p in root.rglob("*.md") if not p.name.startswith("_"))


class KitValidator:
    """Validates one checkout of the kit."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.report = Report()
        self.spec = {name: self._load_json(f"spec/{name}.json") for name in ("ids", "deliverables", "gates")}
        self.spec["trace-rules"] = self._load_json("spec/trace-rules.json")

    def run(self) -> Report:
        if all(self.spec.values()):
            self._check_spec()
            self._check_docs(self.root / "workspace", is_template=True)
            for pack in sorted((self.root / "targets").glob("*/workspace")):
                self._check_docs(pack, is_template=False)
            self._check_agents_and_skills()
            self._check_settings()
        self._check_links()

        return self.report

    def _load_json(self, relative: str) -> dict:
        path = self.root / relative
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            self.report.add(relative, f"cannot be read as JSON: {error}")

            return {}

    def _check_spec(self) -> None:
        deliverables = self.spec["deliverables"]["deliverables"]
        owners = self.spec["deliverables"]["owners"]
        ids = [d["id"] for d in deliverables]
        if ids != [f"D{n:02d}" for n in range(1, 21)]:
            self.report.add("spec/deliverables.json", "must list D01 to D20 once each, in order")
        for deliverable in deliverables:
            if deliverable["owner"] not in owners:
                self.report.add(
                    "spec/deliverables.json", f"{deliverable['id']} has unknown owner {deliverable['owner']}"
                )
            for contributor in deliverable["contributors"]:
                if contributor not in owners:
                    self.report.add(
                        "spec/deliverables.json", f"{deliverable['id']} has unknown contributor {contributor}"
                    )
            if not (self.root / "workspace" / deliverable["file"]).is_file():
                self.report.add(
                    "spec/deliverables.json", f"{deliverable['id']} file {deliverable['file']} does not exist"
                )

        gates = self.spec["gates"]
        known = set(ids)
        gate_ids = [g["id"] for g in gates["gates"]]
        if gate_ids != [f"G{n}" for n in range(5)]:
            self.report.add("spec/gates.json", "must list G0 to G4 in order")
        for gate in gates["gates"]:
            for requirement in gate["requires"]["deliverables"]:
                if requirement["id"] not in known:
                    self.report.add("spec/gates.json", f"{gate['id']} requires unknown {requirement['id']}")
            for condition in gate["requires"]["conditions"]:
                if condition not in gates["conditions"]:
                    self.report.add("spec/gates.json", f"{gate['id']} uses undefined condition {condition}")
        for deliverable in deliverables:
            if deliverable["gate"] not in gate_ids:
                self.report.add(
                    "spec/deliverables.json", f"{deliverable['id']} names unknown gate {deliverable['gate']}"
                )

        for kind in self.spec["ids"]["kinds"]:
            try:
                re.compile(kind["pattern"])
            except re.error as error:
                self.report.add("spec/ids.json", f"{kind['prefix']} pattern does not compile: {error}")
        try:
            re.compile(self.spec["trace-rules"]["malformedCandidate"])
            re.compile(self.spec["ids"]["evidence"]["pattern"])
        except re.error as error:
            self.report.add("spec", f"a pattern does not compile: {error}")

    def _id_pattern(self) -> re.Pattern[str]:
        ids = self.spec["ids"]
        alternatives = "|".join(f"(?:{kind['pattern']})" for kind in ids["kinds"])

        return re.compile(ids["delimiters"]["before"] + f"(?:{alternatives})" + ids["delimiters"]["after"])

    def _check_docs(self, workspace: Path, *, is_template: bool) -> None:
        docs = workspace / "docs"
        by_file = {d["file"]: d for d in self.spec["deliverables"]["deliverables"]}
        owners = self.spec["deliverables"]["owners"]
        statuses = set(self.spec["deliverables"]["statuses"])
        id_pattern = self._id_pattern()

        for path in markdown_files(docs):
            relative = path.relative_to(workspace).as_posix()
            shown = path.relative_to(self.root)
            text = path.read_text(encoding="utf-8")
            front = read_front_matter(text)
            if front is None:
                self.report.add(shown, "has no front-matter")
                continue

            unknown_keys = set(front) - FRONT_MATTER_KEYS
            if unknown_keys:
                self.report.add(shown, f"front-matter has unknown keys {sorted(unknown_keys)}")
            if ("id" in front) == ("part-of" in front):
                self.report.add(shown, "front-matter needs exactly one of id and part-of")
            parent = scalar(front, "id") or scalar(front, "part-of")
            if not DELIVERABLE_ID.match(parent):
                self.report.add(shown, f"front-matter names invalid deliverable {parent!r}")
            if scalar(front, "owner") not in owners:
                self.report.add(shown, f"front-matter owner {front.get('owner')!r} is not a known role")
            if scalar(front, "status") not in statuses:
                self.report.add(shown, f"front-matter status {front.get('status')!r} is not one of {sorted(statuses)}")
            if not scalar(front, "title"):
                self.report.add(shown, "front-matter has no title")

            expected = by_file.get(relative)
            if "id" in front:
                if expected is None or expected["id"] != front["id"]:
                    self.report.add(shown, f"declares {front['id']} but deliverables.json does not place it here")
                elif expected["title"] != scalar(front, "title") or expected["owner"] != scalar(front, "owner"):
                    self.report.add(shown, f"title or owner differs from deliverables.json for {front['id']}")
            elif expected is not None:
                self.report.add(shown, f"is the file of {expected['id']} but declares part-of instead of id")

            if is_template:
                if scalar(front, "status") != "template":
                    self.report.add(shown, "a workspace template must have status template")
                found = sorted(set(id_pattern.findall(visible_text(text))))
                if found:
                    self.report.add(shown, f"a template must not define or reference records, found {found}")

    def _check_agents_and_skills(self) -> None:
        claude = self.root / "workspace" / ".claude"
        skills = {p.name for p in (claude / "skills").iterdir() if p.is_dir()}
        for skill in sorted(skills):
            front = read_front_matter((claude / "skills" / skill / "SKILL.md").read_text(encoding="utf-8"))
            if front is None or scalar(front, "name") != skill or not scalar(front, "description"):
                self.report.add(
                    f"workspace/.claude/skills/{skill}/SKILL.md", "needs name equal to its folder and a description"
                )

        for path in sorted((claude / "agents").glob("*.md")):
            shown = path.relative_to(self.root)
            front = read_front_matter(path.read_text(encoding="utf-8"))
            if front is None or scalar(front, "name") != path.stem or not scalar(front, "description"):
                self.report.add(shown, "needs name equal to its file name and a description")
                continue
            tools = {t.strip() for t in scalar(front, "tools").split(",") if t.strip()}
            if not tools or not tools <= KNOWN_TOOLS:
                self.report.add(shown, f"tools {sorted(tools - KNOWN_TOOLS) or 'missing'} are not known tool names")
            preloaded = front.get("skills", [])
            for skill in preloaded if isinstance(preloaded, list) else []:
                if skill not in skills:
                    self.report.add(shown, f"preloads unknown skill {skill}")

        claude_md = (self.root / "workspace" / "CLAUDE.md").read_text(encoding="utf-8")
        for skill in sorted(skills):
            if f"/{skill}`" not in claude_md:
                self.report.add("workspace/CLAUDE.md", f"does not list the skill /{skill}")

    def _check_settings(self) -> None:
        settings = self._load_json("workspace/.claude/settings.json")
        if not settings:
            return
        permissions = settings.get("permissions", {})
        for rule in permissions.get("allow", []) + permissions.get("deny", []):
            if rule.startswith("Write("):
                self.report.add(
                    "workspace/.claude/settings.json", f"{rule}: Edit rules govern writes; Write rules match nothing"
                )
        if "Edit(/legacy/**)" not in permissions.get("deny", []):
            self.report.add("workspace/.claude/settings.json", "must deny Edit(/legacy/**)")
        commands = [
            hook.get("command", "")
            for entry in settings.get("hooks", {}).get("PreToolUse", [])
            for hook in entry.get("hooks", [])
        ]
        if not any(c.startswith("dmz guard pre-tool-use") and c.endswith("|| exit 2") for c in commands):
            self.report.add("workspace/.claude/settings.json", "the PreToolUse hook must run dmz guard and fail closed")

    def _check_links(self) -> None:
        for path in markdown_files(self.root):
            if ".git" in path.parts:
                continue
            text = visible_text(path.read_text(encoding="utf-8"))
            for target in MARKDOWN_LINK.findall(text):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                if not resolved.exists():
                    self.report.add(path.relative_to(self.root), f"links to missing {target}")


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    report = KitValidator(root).run()
    for problem in report.problems:
        print(problem)
    print(f"{len(report.problems)} problem(s)")

    return 1 if report.problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
