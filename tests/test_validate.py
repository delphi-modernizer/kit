"""The validator: the kit passes, and each kind of problem is reported."""

from __future__ import annotations

import json
import pathlib
import shutil

import pytest

import validate

KIT = pathlib.Path(__file__).resolve().parent.parent
_COPY_SKIPS = (
    ".git",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    "target",
    "bin",
    "obj",
)
_D03 = (
    "workspace/docs/02-functional-requirements/D03-functional-requirements.md"
)


@pytest.fixture(name="kit")
def fixture_kit(tmp_path: pathlib.Path) -> pathlib.Path:
    """A throwaway copy of the kit that a test may break."""
    root = tmp_path / "kit"
    shutil.copytree(KIT, root, ignore=shutil.ignore_patterns(*_COPY_SKIPS))
    return root


def _problems(root: pathlib.Path) -> list[str]:
    return validate.KitValidator(root).run().problems


def _append(path: pathlib.Path, text: str) -> None:
    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")


def _replace(path: pathlib.Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def _edit_gates(kit: pathlib.Path, index: int, name: str | None) -> None:
    gates = kit / "spec/gates.json"
    spec = json.loads(gates.read_text(encoding="utf-8"))
    if name is None:
        del spec["gates"][index]["name"]
    else:
        spec["gates"][index]["name"] = name
    gates.write_text(json.dumps(spec), encoding="utf-8")


def _reported(kit: pathlib.Path, text: str) -> bool:
    return any(text in problem for problem in _problems(kit))


def test_the_kit_is_consistent() -> None:
    assert _problems(KIT) == []


def test_a_template_that_mentions_a_record_is_reported(
    kit: pathlib.Path,
) -> None:
    _append(kit / _D03, "\nSee FR-001.\n")

    assert _reported(kit, "FR-001")


def test_a_record_inside_an_html_comment_is_not_reported(
    kit: pathlib.Path,
) -> None:
    _append(kit / _D03, "\n<!-- e.g. FR-001 -->\n")

    assert _problems(kit) == []


def test_a_malformed_id_in_a_target_pack_is_reported(kit: pathlib.Path) -> None:
    pack = "targets/jvm/workspace/docs/05-target-architecture"
    _append(kit / pack / "stack-candidates.md", "\nOnly where NFR-PERF says.\n")

    assert _reported(kit, "NFR-PERF")


def test_a_write_permission_rule_is_reported(kit: pathlib.Path) -> None:
    settings = kit / "workspace/.claude/settings.json"
    _replace(settings, '"Edit(/docs/**)"', '"Write(/docs/**)"')

    assert _reported(kit, "Write rules match nothing")


def test_a_hook_that_fails_open_is_reported(kit: pathlib.Path) -> None:
    _replace(kit / "workspace/.claude/settings.json", " || exit 2", "")

    assert _reported(kit, "fail closed")


def test_an_owner_that_disagrees_with_the_spec_is_reported(
    kit: pathlib.Path,
) -> None:
    inventory = kit / "workspace/docs/01-discovery/D02-system-inventory.md"
    _replace(inventory, "owner: WS01", "owner: WS02")

    assert _reported(kit, "title or owner differs")


def test_a_gate_without_a_name_is_reported(kit: pathlib.Path) -> None:
    _edit_gates(kit, 1, None)

    assert _reported(kit, "G1 has no name")


def test_two_gates_with_one_name_are_reported(kit: pathlib.Path) -> None:
    _edit_gates(kit, 2, "Discovery")

    assert _reported(kit, "G2 shares its name")


def test_a_missing_deliverable_file_is_reported(kit: pathlib.Path) -> None:
    (kit / "workspace/docs/13-project-roadmap/D18-estimates.md").unlink()

    assert _reported(kit, "D18 file")


def test_an_agent_that_preloads_an_unknown_skill_is_reported(
    kit: pathlib.Path,
) -> None:
    agent = kit / "workspace/.claude/agents/ws02-requirements.md"
    _replace(agent, "  - write-nfr", "  - write-poetry")

    assert _reported(kit, "unknown skill write-poetry")


def test_a_recipe_naming_an_unknown_skill_is_reported(
    kit: pathlib.Path,
) -> None:
    recipes = kit / "spec/recipes.json"
    _replace(recipes, '"skill": "write-frs"', '"skill": "write-sonnets"')

    assert _reported(kit, "unknown skill write-sonnets")


def test_a_broken_relative_link_is_reported(kit: pathlib.Path) -> None:
    _append(kit / "README.md", "\n[gone](missing.md)\n")

    assert _reported(kit, "missing.md")


def test_markdown_in_a_virtual_environment_is_not_the_kits(
    kit: pathlib.Path,
) -> None:
    (kit / ".venv").mkdir()
    (kit / ".venv/README.md").write_text("[x](nowhere.md)\n", encoding="utf-8")

    assert _problems(kit) == []


def test_front_matter_reads_scalars_and_lists() -> None:
    text = (
        "---\nname: pa\ntools: Read, Grep\nskills:\n  - a\n  - b\n---\n\nbody\n"
    )

    front = validate.read_front_matter(text)

    assert front == {"name": "pa", "tools": "Read, Grep", "skills": ["a", "b"]}


def test_text_without_front_matter_has_none() -> None:
    assert validate.read_front_matter("# Title\n") is None


def test_visible_text_drops_comments_fences_and_code_spans() -> None:
    markdown = "keep <!-- FR-001 --> `FR-002`\n```\nFR-003\n```\nend"

    assert validate.visible_text(markdown).split() == ["keep", "end"]
