from __future__ import annotations

from pathlib import Path
import re
import unittest


V2_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = V2_ROOT / "OPERATING_CONTRACT.md"
CUSTOM_INSTRUCTIONS_PATH = V2_ROOT / "CUSTOM_INSTRUCTIONS.md"
PROJECT_INSTRUCTIONS_PATH = V2_ROOT / "PROJECT-INSTRUCTIONS-TEMPLATE.md"


class BootstrapDocumentTests(unittest.TestCase):
    def test_contract_requires_a_unique_cache_buster_and_complete_body(self) -> None:
        contract = CONTRACT_PATH.read_text(encoding="utf-8")

        version_match = re.search(r"\*\*Version:\*\* (\d+)\.(\d+)\.(\d+)", contract)
        self.assertIsNotNone(version_match)
        self.assertGreaterEqual(
            tuple(int(part) for part in version_match.groups()),
            (2, 1, 11),
        )
        self.assertIn("unique cache-busting", contract)
        self.assertIn("Do not request the bare canonical URL first", contract)
        self.assertIn("complete document body", contract)
        self.assertIn("is not a successful contract load", contract)
        self.assertIn("byte-preserving", contract)
        self.assertIn("independent unique cache-busting", contract)

    def test_custom_instructions_are_a_lean_bootstrap_loader(self) -> None:
        instructions = CUSTOM_INSTRUCTIONS_PATH.read_text(encoding="utf-8")

        self.assertLess(len(instructions), 2000)
        self.assertIn(
            "https://raw.githubusercontent.com/imajes/agents/main/"
            "operating-contract/v2/OPERATING_CONTRACT.md",
            instructions,
        )
        self.assertIn("?contract_cb=<unique timestamp or nonce>", instructions)
        self.assertIn("complete document body", instructions)
        self.assertIn("mandatory companion registry", instructions)
        self.assertIn("byte-preserving", instructions)
        self.assertIn("bootstrap pointer", instructions)
        self.assertNotIn("ADVANCE", instructions)
        self.assertNotIn("Directly evidenced", instructions)
        self.assertNotIn("Operating pillars:", instructions)

    def test_project_template_uses_the_same_fresh_loader_contract(self) -> None:
        instructions = PROJECT_INSTRUCTIONS_PATH.read_text(encoding="utf-8")

        self.assertIn("?contract_cb=<unique timestamp or nonce>", instructions)
        self.assertIn("complete document body", instructions)
        self.assertIn("mandatory companion registry", instructions)
        self.assertIn("byte-preserving", instructions)
        self.assertIn("project-specific state", instructions)
        self.assertNotIn("claim tails", instructions)


if __name__ == "__main__":
    unittest.main()
