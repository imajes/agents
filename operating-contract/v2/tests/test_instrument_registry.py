from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import unittest


V2_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = V2_ROOT / "instruments" / "registry.json"
DIGEST_PATH = V2_ROOT / "instruments" / "registry.sha256"
MARKDOWN_PATH = V2_ROOT / "instruments" / "registry.md"
ATLAS_PATH = V2_ROOT / "instruments" / "atlas.png"
GENERATOR_PATH = V2_ROOT / "scripts" / "generate_instrument_registry.py"
CONTRACT_PATH = V2_ROOT / "OPERATING_CONTRACT.md"


def decode_scalars(scalars: list[str]) -> str:
    return "".join(chr(int(value.removeprefix("U+"), 16)) for value in scalars)


class InstrumentRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry_bytes = REGISTRY_PATH.read_bytes()
        self.registry = json.loads(self.registry_bytes)
        self.entries = self.registry["instruments"]

    def test_authoritative_registry_is_ascii_only(self) -> None:
        self.assertTrue(
            all(byte < 0x80 for byte in self.registry_bytes),
            "registry.json must contain ASCII bytes only",
        )

    def test_registry_has_required_schema_and_unique_ids(self) -> None:
        self.assertEqual(self.registry["schema"], "operating-instrument-registry/v1")
        self.assertRegex(self.registry["version"], r"^\d+\.\d+\.\d+$")
        self.assertGreater(len(self.entries), 20)

        ids = [entry["id"] for entry in self.entries]
        self.assertEqual(len(ids), len(set(ids)), "registry IDs must be unique")

        for entry in self.entries:
            with self.subTest(instrument=entry["id"]):
                self.assertRegex(entry["id"], r"^[A-Z][A-Z0-9_]+$")
                self.assertTrue(entry["label"])
                self.assertTrue(entry["role"])
                self.assertTrue(entry["unicode_scalars"])
                self.assertTrue(entry["utf8_hex"])
                self.assertIn("template", entry["render"])
                self.assertIn("spacing", entry["render"])
                self.assertIn("{glyph}", entry["render"]["template"])
                self.assertTrue(entry["ascii_fallback"])

    def test_scalar_sequences_match_utf8_hex(self) -> None:
        for entry in self.entries:
            with self.subTest(instrument=entry["id"]):
                rendered = decode_scalars(entry["unicode_scalars"])
                expected_hex = " ".join(f"{byte:02X}" for byte in rendered.encode("utf-8"))
                self.assertEqual(entry["utf8_hex"], expected_hex)

    def test_digest_file_and_contract_manifest_match_registry(self) -> None:
        digest = hashlib.sha256(self.registry_bytes).hexdigest()
        self.assertEqual(
            DIGEST_PATH.read_text(encoding="ascii"),
            f"{digest}  registry.json\n",
        )

        contract = CONTRACT_PATH.read_text(encoding="utf-8")
        self.assertIn(
            f"**Instrument Registry Version:** `{self.registry['version']}`",
            contract,
        )
        self.assertIn(
            "**Instrument Registry Path:** "
            "`operating-contract/v2/instruments/registry.json`",
            contract,
        )
        self.assertIn(f"**Instrument Registry SHA-256:** `{digest}`", contract)
        self.assertIn(
            "**Rendered Instrument Registry:** "
            "`operating-contract/v2/instruments/registry.md`",
            contract,
        )
        self.assertIn(
            "**Instrument Atlas:** "
            "`operating-contract/v2/instruments/atlas.png`",
            contract,
        )

    def test_generated_markdown_is_current_and_renders_every_instrument(self) -> None:
        markdown = MARKDOWN_PATH.read_text(encoding="utf-8")
        digest = hashlib.sha256(self.registry_bytes).hexdigest()

        self.assertIn("Generated from `registry.json`; do not edit.", markdown)
        self.assertIn(f"Registry version: `{self.registry['version']}`", markdown)
        self.assertIn(f"SHA-256: `{digest}`", markdown)

        for entry in self.entries:
            with self.subTest(instrument=entry["id"]):
                glyph = decode_scalars(entry["unicode_scalars"])
                intended = entry["render"]["template"].replace("{glyph}", glyph)
                self.assertIn(f"`{entry['id']}`", markdown)
                self.assertIn(glyph, markdown)
                self.assertIn(intended, markdown)

    def test_generated_atlas_has_png_metadata_for_registry(self) -> None:
        atlas = ATLAS_PATH.read_bytes()
        self.assertTrue(atlas.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertGreaterEqual(len(atlas), 24)
        width, height = struct.unpack(">II", atlas[16:24])
        self.assertGreaterEqual(width, 800)
        self.assertGreaterEqual(height, 600)

        digest = hashlib.sha256(self.registry_bytes).hexdigest().encode("ascii")
        self.assertIn(self.registry["version"].encode("ascii"), atlas)
        self.assertIn(digest, atlas)

    def test_generator_check_mode_accepts_checked_in_artifacts(self) -> None:
        result = subprocess.run(
            [sys.executable, str(GENERATOR_PATH), "--check"],
            cwd=V2_ROOT.parents[1],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
