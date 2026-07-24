from __future__ import annotations

from pathlib import Path
import unittest


V2_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = V2_ROOT / "OPERATING_CONTRACT.md"
STATE_TEMPLATE_PATH = V2_ROOT / "WORKSTREAM-STATE.md"
TRIAL_PROTOCOL_PATH = V2_ROOT / "TRIAL-PROTOCOL.md"

REQUIRED_HEADINGS = (
    "# Workstream checkpoint",
    "## Direction",
    "## Decisions",
    "## Constraints",
    "## Open assumptions",
    "## Open tangents",
)


class WorkstreamCheckpointTests(unittest.TestCase):
    def test_contract_defines_a_structured_markdown_checkpoint(self) -> None:
        contract = CONTRACT_PATH.read_text(encoding="utf-8")

        self.assertIn("**Version:** 2.1.12", contract)
        self.assertIn("```markdown\n# Workstream checkpoint", contract)
        for heading in REQUIRED_HEADINGS:
            self.assertIn(heading, contract)
        self.assertIn("| **Workstream** | `<workstream-id>` |", contract)
        self.assertIn("| **Revision** | `<revision>`", contract)
        self.assertIn("| **Persistence** | `<adapter>`", contract)
        self.assertIn("- **Objective:** <objective>", contract)
        self.assertIn("- **Control:** Focus Lock <ON/OFF>", contract)
        self.assertIn("Use `None` only when a section is genuinely empty", contract)
        self.assertNotIn("```text\nWorkstream: <workstream-id>", contract)

    def test_state_template_matches_the_portable_checkpoint_hierarchy(self) -> None:
        template = STATE_TEMPLATE_PATH.read_text(encoding="utf-8")

        for heading in REQUIRED_HEADINGS:
            self.assertIn(heading, template)
        self.assertIn("| **Workstream** |", template)
        self.assertIn("| **Revision** |", template)
        self.assertIn("| **Persistence** |", template)
        self.assertIn("**Objective:**", template)
        self.assertIn("**Next:**", template)
        self.assertIn("**Control:**", template)

    def test_trial_protocol_covers_checkpoint_structure_and_copy_safety(self) -> None:
        protocol = TRIAL_PROTOCOL_PATH.read_text(encoding="utf-8")

        self.assertIn("## 9. Structured workstream checkpoint", protocol)
        self.assertIn("stable Markdown hierarchy", protocol)
        self.assertIn("no claim tails or conversational commentary", protocol)


if __name__ == "__main__":
    unittest.main()
