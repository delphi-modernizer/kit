"""Tests for validate.py: the kit itself passes, and each kind of inconsistency is reported."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate import KitValidator, read_front_matter, visible_text

KIT = Path(__file__).resolve().parent.parent
IGNORED = shutil.ignore_patterns(".git", "target", "bin", "obj", "__pycache__", ".ruff_cache")


class KitCopy:
    """A throwaway copy of the kit that a test may break."""

    def __enter__(self) -> Path:
        self._directory = tempfile.TemporaryDirectory()
        root = Path(self._directory.name) / "kit"
        shutil.copytree(KIT, root, ignore=IGNORED)

        return root

    def __exit__(self, *_: object) -> None:
        self._directory.cleanup()


def problems_in(root: Path) -> list[str]:
    return KitValidator(root).run().problems


class ValidateTests(unittest.TestCase):
    def test_the_kit_is_consistent(self) -> None:
        self.assertEqual(problems_in(KIT), [])

    def test_a_template_that_mentions_a_record_is_reported(self) -> None:
        with KitCopy() as root:
            template = root / "workspace/docs/02-functional-requirements/D03-functional-requirements.md"
            template.write_text(template.read_text(encoding="utf-8") + "\nSee FR-001.\n", encoding="utf-8")

            self.assertTrue(any("FR-001" in p for p in problems_in(root)))

    def test_a_record_inside_an_html_comment_is_not_reported(self) -> None:
        with KitCopy() as root:
            template = root / "workspace/docs/02-functional-requirements/D03-functional-requirements.md"
            template.write_text(template.read_text(encoding="utf-8") + "\n<!-- e.g. FR-001 -->\n", encoding="utf-8")

            self.assertEqual(problems_in(root), [])

    def test_a_malformed_id_in_a_target_pack_is_reported(self) -> None:
        with KitCopy() as root:
            pack = root / "targets/jvm/workspace/docs/05-target-architecture/stack-candidates.md"
            pack.write_text(pack.read_text(encoding="utf-8") + "\nOnly where NFR-PERF says so.\n", encoding="utf-8")

            self.assertTrue(any("NFR-PERF" in p for p in problems_in(root)))

    def test_a_write_permission_rule_is_reported(self) -> None:
        with KitCopy() as root:
            settings = root / "workspace/.claude/settings.json"
            settings.write_text(
                settings.read_text(encoding="utf-8").replace('"Edit(/docs/**)"', '"Write(/docs/**)"'), encoding="utf-8"
            )

            self.assertTrue(any("Write rules match nothing" in p for p in problems_in(root)))

    def test_a_hook_that_fails_open_is_reported(self) -> None:
        with KitCopy() as root:
            settings = root / "workspace/.claude/settings.json"
            settings.write_text(settings.read_text(encoding="utf-8").replace(" || exit 2", ""), encoding="utf-8")

            self.assertTrue(any("fail closed" in p for p in problems_in(root)))

    def test_an_owner_that_disagrees_with_the_spec_is_reported(self) -> None:
        with KitCopy() as root:
            template = root / "workspace/docs/01-discovery/D02-system-inventory.md"
            template.write_text(
                template.read_text(encoding="utf-8").replace("owner: WS01", "owner: WS02", 1), encoding="utf-8"
            )

            self.assertTrue(any("title or owner differs" in p for p in problems_in(root)))

    def test_a_gate_without_a_name_is_reported(self) -> None:
        with KitCopy() as root:
            gates = root / "spec/gates.json"
            spec = json.loads(gates.read_text(encoding="utf-8"))
            del spec["gates"][1]["name"]
            gates.write_text(json.dumps(spec), encoding="utf-8")

            self.assertTrue(any("G1 has no name" in p for p in problems_in(root)))

    def test_two_gates_with_one_name_are_reported(self) -> None:
        with KitCopy() as root:
            gates = root / "spec/gates.json"
            spec = json.loads(gates.read_text(encoding="utf-8"))
            spec["gates"][2]["name"] = spec["gates"][1]["name"]
            gates.write_text(json.dumps(spec), encoding="utf-8")

            self.assertTrue(any("G2 shares its name" in p for p in problems_in(root)))

    def test_a_missing_deliverable_file_is_reported(self) -> None:
        with KitCopy() as root:
            (root / "workspace/docs/13-project-roadmap/D18-estimates.md").unlink()

            self.assertTrue(any("D18 file" in p for p in problems_in(root)))

    def test_an_agent_that_preloads_an_unknown_skill_is_reported(self) -> None:
        with KitCopy() as root:
            agent = root / "workspace/.claude/agents/ws02-requirements.md"
            agent.write_text(
                agent.read_text(encoding="utf-8").replace("  - write-nfr", "  - write-poetry"), encoding="utf-8"
            )

            self.assertTrue(any("unknown skill write-poetry" in p for p in problems_in(root)))

    def test_a_recipe_naming_an_unknown_skill_is_reported(self) -> None:
        with KitCopy() as root:
            recipes = root / "spec/recipes.json"
            recipes.write_text(
                recipes.read_text(encoding="utf-8").replace('"skill": "write-frs"', '"skill": "write-sonnets"'),
                encoding="utf-8",
            )

            self.assertTrue(any("unknown skill write-sonnets" in p for p in problems_in(root)))

    def test_a_broken_relative_link_is_reported(self) -> None:
        with KitCopy() as root:
            readme = root / "README.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "\n[gone](missing.md)\n", encoding="utf-8")

            self.assertTrue(any("missing.md" in p for p in problems_in(root)))


class FrontMatterTests(unittest.TestCase):
    def test_reads_scalars_and_lists(self) -> None:
        front = read_front_matter("---\nname: pa\ntools: Read, Grep\nskills:\n  - a\n  - b\n---\n\nbody\n")

        self.assertEqual(front, {"name": "pa", "tools": "Read, Grep", "skills": ["a", "b"]})

    def test_text_without_front_matter_has_none(self) -> None:
        self.assertIsNone(read_front_matter("# Title\n"))

    def test_visible_text_drops_comments_fences_and_code_spans(self) -> None:
        markdown = "keep <!-- FR-001 --> `FR-002`\n```\nFR-003\n```\nend"

        self.assertEqual(visible_text(markdown).split(), ["keep", "end"])


if __name__ == "__main__":
    unittest.main()
