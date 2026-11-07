#!/usr/bin/env python3
"""Checks that the kit's spec, templates, agents, skills and links agree.

Usage: `python3 tools/validate.py [kit-root]`. Every problem found is printed,
and the exit code is 1 when there is one.
"""

from __future__ import annotations

from collections.abc import Iterator
import dataclasses
import json
import pathlib
import re
import sys
from typing import Any

type JsonObject = dict[str, Any]
type FrontMatter = dict[str, str | list[str]]

KNOWN_TOOLS = frozenset({
    "Read",
    "Grep",
    "Glob",
    "Edit",
    "Write",
    "Bash",
    "Agent",
    "WebFetch",
    "WebSearch",
    "NotebookEdit",
    "TodoWrite",
})
FRONT_MATTER_KEYS = frozenset({"id", "part-of", "title", "owner", "status"})
DELIVERABLE_ID = re.compile(r"^D(0[1-9]|1[0-9]|20)$")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
FENCED_CODE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
INLINE_CODE = re.compile(r"`[^`\n]*`")
MARKDOWN_LINK = re.compile(r"\]\(([^)\s]+)\)")
# Tool and dependency folders a local run leaves; their Markdown is not the
# kit's.
SKIPPED_FOLDERS = frozenset(
    {".git", ".venv", ".mypy_cache", ".pytest_cache", "node_modules"}
)


@dataclasses.dataclass
class Report:
    """Collects problems, so that one run lists all of them.

    Attributes:
        problems: Each problem, as `<path>: <message>`.
    """

    problems: list[str] = dataclasses.field(default_factory=list[str])

    def add(self, path: pathlib.Path | str, message: str) -> None:
        """Records a problem found in `path`."""
        self.problems.append(f"{path}: {message}")


def read_front_matter(text: str) -> FrontMatter | None:
    """Reads the front matter at the top of a Markdown file.

    The kit's front matter holds only scalars and lists of scalars, so this
    reads that subset of YAML.

    Args:
        text: The whole file.

    Returns:
        The keys and their values, or None when the file has no front matter
        or it is not that subset.
    """
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    values: FrontMatter = {}
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


def scalar(front: FrontMatter, key: str) -> str:
    """Returns the value of `key`, or "" when it is missing or a list."""
    value = front.get(key, "")
    return value if isinstance(value, str) else ""


def visible_text(markdown: str) -> str:
    """Strips what the spec says IDs are not read from.

    Args:
        markdown: A Markdown document.

    Returns:
        The document without HTML comments, fenced code blocks and code spans.
    """
    without_comments = HTML_COMMENT.sub("", markdown)
    without_fences = FENCED_CODE.sub("", without_comments)
    return INLINE_CODE.sub("", without_fences)


def markdown_files(root: pathlib.Path) -> Iterator[pathlib.Path]:
    """Yields the Markdown files under `root` in order, skipping partials."""
    yield from sorted(
        path
        for path in root.rglob("*.md")
        if not path.name.startswith("_")
        and not SKIPPED_FOLDERS.intersection(path.relative_to(root).parts)
    )


@dataclasses.dataclass(frozen=True)
class _IdPatterns:
    """The regular expressions the ID spec defines.

    Attributes:
        record: A record ID between the spec's delimiters.
        candidate: Text that looks like an ID, valid or not (TR013).
        whole: A whole string that is a valid ID.
    """

    record: re.Pattern[str]
    candidate: re.Pattern[str]
    whole: re.Pattern[str]


class KitValidator:
    """Validates one checkout of the kit.

    Attributes:
        root: The kit's root folder.
        report: The problems found so far.
        spec: The spec's JSON files by name, empty when one cannot be read.
    """

    def __init__(self, root: pathlib.Path) -> None:
        self.root = root
        self.report = Report()
        self.spec = {
            name: self._load_json(f"spec/{name}.json")
            for name in (
                "ids",
                "deliverables",
                "gates",
                "trace-rules",
                "recipes",
            )
        }

    def run(self) -> Report:
        """Runs every check.

        Returns:
            The report; the spec checks are skipped when a spec file cannot be
            read.
        """
        if all(self.spec.values()):
            self._check_deliverables()
            self._check_gates()
            self._check_patterns()
            patterns = self._id_patterns()
            self._check_docs(
                self.root / "workspace", patterns, is_template=True
            )
            for pack in sorted((self.root / "targets").glob("*/workspace")):
                self._check_docs(pack, patterns, is_template=False)
            self._check_skills()
            self._check_agents()
            self._check_recipes()
            self._check_settings()
        self._check_links()
        return self.report

    def _load_json(self, relative: str) -> JsonObject:
        path = self.root / relative
        try:
            loaded: JsonObject = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            self.report.add(relative, f"cannot be read as JSON: {error}")
            return {}
        return loaded

    def _check_deliverables(self) -> None:
        """Checks D01 to D20: their order, owners, contributors and files."""
        deliverables = self.spec["deliverables"]["deliverables"]
        owners = self.spec["deliverables"]["owners"]
        shown = "spec/deliverables.json"
        if [d["id"] for d in deliverables] != [
            f"D{n:02d}" for n in range(1, 21)
        ]:
            self.report.add(shown, "must list D01 to D20 once each, in order")
        for deliverable in deliverables:
            identifier = deliverable["id"]
            if deliverable["owner"] not in owners:
                self.report.add(
                    shown,
                    f"{identifier} has unknown owner {deliverable['owner']}",
                )
            for contributor in deliverable["contributors"]:
                if contributor not in owners:
                    self.report.add(
                        shown,
                        f"{identifier} has unknown contributor {contributor}",
                    )
            if not (self.root / "workspace" / deliverable["file"]).is_file():
                self.report.add(
                    shown,
                    f"{identifier} file {deliverable['file']} does not exist",
                )

    def _check_gates(self) -> None:
        """Checks G0 to G4: their order, names, requirements and conditions."""
        gates = self.spec["gates"]
        deliverables = self.spec["deliverables"]["deliverables"]
        known = {d["id"] for d in deliverables}
        gate_ids = [gate["id"] for gate in gates["gates"]]
        if gate_ids != [f"G{n}" for n in range(5)]:
            self.report.add("spec/gates.json", "must list G0 to G4 in order")
        names = [str(gate.get("name", "")).strip() for gate in gates["gates"]]
        for gate, name in zip(gates["gates"], names, strict=True):
            if not name:
                self.report.add("spec/gates.json", f"{gate['id']} has no name")
            elif names.count(name) > 1:
                self.report.add(
                    "spec/gates.json",
                    f"{gate['id']} shares its name {name} with another gate",
                )
            for requirement in gate["requires"]["deliverables"]:
                if requirement["id"] not in known:
                    self.report.add(
                        "spec/gates.json",
                        f"{gate['id']} requires unknown {requirement['id']}",
                    )
            for condition in gate["requires"]["conditions"]:
                if condition not in gates["conditions"]:
                    self.report.add(
                        "spec/gates.json",
                        f"{gate['id']} uses undefined condition {condition}",
                    )
        for deliverable in deliverables:
            if deliverable["gate"] not in gate_ids:
                self.report.add(
                    "spec/deliverables.json",
                    f"{deliverable['id']} names unknown gate"
                    f" {deliverable['gate']}",
                )

    def _check_patterns(self) -> None:
        """Checks that every pattern in the spec compiles."""
        for kind in self.spec["ids"]["kinds"]:
            try:
                re.compile(kind["pattern"])
            except re.error as error:
                self.report.add(
                    "spec/ids.json",
                    f"{kind['prefix']} pattern does not compile: {error}",
                )
        try:
            re.compile(self.spec["trace-rules"]["malformedCandidate"])
            re.compile(self.spec["ids"]["evidence"]["pattern"])
        except re.error as error:
            self.report.add("spec", f"a pattern does not compile: {error}")

    def _id_patterns(self) -> _IdPatterns:
        ids = self.spec["ids"]
        kinds = "|".join(f"(?:{kind['pattern']})" for kind in ids["kinds"])
        delimiters = ids["delimiters"]
        return _IdPatterns(
            record=re.compile(
                delimiters["before"] + f"(?:{kinds})" + delimiters["after"]
            ),
            candidate=re.compile(
                self.spec["trace-rules"]["malformedCandidate"]
            ),
            whole=re.compile(f"^(?:{kinds})$"),
        )

    def _check_docs(
        self,
        workspace: pathlib.Path,
        patterns: _IdPatterns,
        *,
        is_template: bool,
    ) -> None:
        """Checks every document under a workspace's `docs/`.

        Args:
            workspace: The workspace template, or a target pack's workspace.
            patterns: The spec's ID patterns.
            is_template: Whether the documents are the empty templates, which
                must not define or reference records.
        """
        for path in markdown_files(workspace / "docs"):
            shown = path.relative_to(self.root)
            text = path.read_text(encoding="utf-8")
            front = read_front_matter(text)
            if front is None:
                self.report.add(shown, "has no front-matter")
                continue
            self._check_front_matter(shown, front)
            self._check_placement(
                shown, path.relative_to(workspace).as_posix(), front
            )
            self._check_ids(shown, text, patterns)
            if is_template:
                self._check_template(shown, text, front, patterns)

    def _check_front_matter(
        self, shown: pathlib.Path, front: FrontMatter
    ) -> None:
        """Checks a document's front matter keys and values."""
        owners = self.spec["deliverables"]["owners"]
        statuses = set(self.spec["deliverables"]["statuses"])
        unknown_keys = set(front) - FRONT_MATTER_KEYS
        if unknown_keys:
            self.report.add(
                shown, f"front-matter has unknown keys {sorted(unknown_keys)}"
            )
        if ("id" in front) == ("part-of" in front):
            self.report.add(
                shown, "front-matter needs exactly one of id and part-of"
            )
        parent = scalar(front, "id") or scalar(front, "part-of")
        if not DELIVERABLE_ID.match(parent):
            self.report.add(
                shown, f"front-matter names invalid deliverable {parent!r}"
            )
        if scalar(front, "owner") not in owners:
            self.report.add(
                shown,
                f"front-matter owner {front.get('owner')!r} is not a known"
                " role",
            )
        if scalar(front, "status") not in statuses:
            self.report.add(
                shown,
                f"front-matter status {front.get('status')!r} is not one of"
                f" {sorted(statuses)}",
            )
        if not scalar(front, "title"):
            self.report.add(shown, "front-matter has no title")

    def _check_placement(
        self, shown: pathlib.Path, relative: str, front: FrontMatter
    ) -> None:
        """Checks a document against the deliverable deliverables.json puts at
        its path."""
        by_file = {
            d["file"]: d for d in self.spec["deliverables"]["deliverables"]
        }
        expected = by_file.get(relative)
        if "id" not in front:
            if expected is not None:
                self.report.add(
                    shown,
                    f"is the file of {expected['id']} but declares part-of"
                    " instead of id",
                )
            return
        if expected is None or expected["id"] != front["id"]:
            self.report.add(
                shown,
                f"declares {front['id']} but deliverables.json does not place"
                " it here",
            )
        elif expected["title"] != scalar(front, "title") or expected[
            "owner"
        ] != scalar(front, "owner"):
            self.report.add(
                shown,
                "title or owner differs from deliverables.json for"
                f" {front['id']}",
            )

    def _check_ids(
        self, shown: pathlib.Path, text: str, patterns: _IdPatterns
    ) -> None:
        """Reports text that looks like an ID but is not one (TR013)."""
        bad = sorted({
            match.group(0)
            for match in patterns.candidate.finditer(visible_text(text))
            if not patterns.whole.match(match.group(0))
        })
        if bad:
            self.report.add(
                shown,
                "text that looks like an ID but is not one would fail TR013:"
                f" {bad}",
            )

    def _check_template(
        self,
        shown: pathlib.Path,
        text: str,
        front: FrontMatter,
        patterns: _IdPatterns,
    ) -> None:
        """Checks that a workspace template is a template, empty of records."""
        if scalar(front, "status") != "template":
            self.report.add(
                shown, "a workspace template must have status template"
            )
        found = sorted(set(patterns.record.findall(visible_text(text))))
        if found:
            self.report.add(
                shown,
                "a template must not define or reference records, found"
                f" {found}",
            )

    def _skills(self) -> list[str]:
        skills = self.root / "workspace" / ".claude" / "skills"
        return sorted(path.name for path in skills.iterdir() if path.is_dir())

    def _check_skills(self) -> None:
        """Checks each skill's front matter and that CLAUDE.md lists it."""
        claude = self.root / "workspace" / ".claude"
        claude_md = (self.root / "workspace" / "CLAUDE.md").read_text(
            encoding="utf-8"
        )
        for skill in self._skills():
            skill_md = claude / "skills" / skill / "SKILL.md"
            front = read_front_matter(skill_md.read_text(encoding="utf-8"))
            if (
                front is None
                or scalar(front, "name") != skill
                or not scalar(front, "description")
            ):
                self.report.add(
                    skill_md.relative_to(self.root),
                    "needs name equal to its folder and a description",
                )
            if f"/{skill}`" not in claude_md:
                self.report.add(
                    "workspace/CLAUDE.md", f"does not list the skill /{skill}"
                )

    def _check_agents(self) -> None:
        """Checks each agent's front matter, tools and preloaded skills."""
        skills = set(self._skills())
        agents = self.root / "workspace" / ".claude" / "agents"
        for path in sorted(agents.glob("*.md")):
            shown = path.relative_to(self.root)
            front = read_front_matter(path.read_text(encoding="utf-8"))
            if (
                front is None
                or scalar(front, "name") != path.stem
                or not scalar(front, "description")
            ):
                self.report.add(
                    shown, "needs name equal to its file name and a description"
                )
                continue
            tools = {
                tool.strip()
                for tool in scalar(front, "tools").split(",")
                if tool.strip()
            }
            if not tools or not tools <= KNOWN_TOOLS:
                unknown = sorted(tools - KNOWN_TOOLS) or "missing"
                self.report.add(
                    shown, f"tools {unknown} are not known tool names"
                )
            preloaded = front.get("skills", [])
            for skill in preloaded if isinstance(preloaded, list) else []:
                if skill not in skills:
                    self.report.add(shown, f"preloads unknown skill {skill}")

    def _check_recipes(self) -> None:
        """Checks that each recipe names a known agent, skill and
        deliverable."""
        claude = self.root / "workspace" / ".claude"
        recipes = self.spec["recipes"]["recipes"]
        deliverables = {
            d["id"] for d in self.spec["deliverables"]["deliverables"]
        }
        ids = [recipe["id"] for recipe in recipes]
        if len(ids) != len(set(ids)):
            self.report.add("spec/recipes.json", "recipe ids must be unique")
        for recipe in recipes:
            agent = claude / "agents" / f"{recipe['agent']}.md"
            if not agent.is_file():
                self.report.add(
                    "spec/recipes.json",
                    f"{recipe['id']} names unknown agent {recipe['agent']}",
                )
            if not (claude / "skills" / recipe["skill"] / "SKILL.md").is_file():
                self.report.add(
                    "spec/recipes.json",
                    f"{recipe['id']} names unknown skill {recipe['skill']}",
                )
            for written in recipe["writes"]:
                if written not in deliverables:
                    self.report.add(
                        "spec/recipes.json",
                        f"{recipe['id']} writes unknown deliverable {written}",
                    )

    def _check_settings(self) -> None:
        """Checks the agents' permissions and the guard hook."""
        shown = "workspace/.claude/settings.json"
        settings = self._load_json(shown)
        if not settings:
            return
        permissions = settings.get("permissions", {})
        for rule in permissions.get("allow", []) + permissions.get("deny", []):
            if rule.startswith("Write("):
                self.report.add(
                    shown,
                    f"{rule}: Edit rules govern writes; Write rules"
                    " match nothing",
                )
        if "Edit(/legacy/**)" not in permissions.get("deny", []):
            self.report.add(shown, "must deny Edit(/legacy/**)")
        commands = [
            hook.get("command", "")
            for entry in settings.get("hooks", {}).get("PreToolUse", [])
            for hook in entry.get("hooks", [])
        ]
        if not any(
            command.startswith("dmz guard pre-tool-use")
            and command.endswith("|| exit 2")
            for command in commands
        ):
            self.report.add(
                shown, "the PreToolUse hook must run dmz guard and fail closed"
            )

    def _check_links(self) -> None:
        """Checks that every relative link in the kit's Markdown resolves."""
        for path in markdown_files(self.root):
            text = visible_text(path.read_text(encoding="utf-8"))
            for target in MARKDOWN_LINK.findall(text):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                if not resolved.exists():
                    self.report.add(
                        path.relative_to(self.root),
                        f"links to missing {target}",
                    )


def main(argv: list[str]) -> int:
    """Validates the kit at `argv[1]`, or the one this file is in.

    Args:
        argv: The command line, the program name first.

    Returns:
        The exit code: 1 when there is a problem, else 0.
    """
    if len(argv) > 1:
        root = pathlib.Path(argv[1])
    else:
        root = pathlib.Path(__file__).resolve().parent.parent
    report = KitValidator(root).run()
    for problem in report.problems:
        print(problem)
    print(f"{len(report.problems)} problem(s)")
    return 1 if report.problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
