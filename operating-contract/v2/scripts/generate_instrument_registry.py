#!/usr/bin/env python3
"""Validate the ASCII instrument registry and generate its human artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from typing import Any


V2_ROOT = Path(__file__).resolve().parents[1]
INSTRUMENTS_ROOT = V2_ROOT / "instruments"
REGISTRY_PATH = INSTRUMENTS_ROOT / "registry.json"
DIGEST_PATH = INSTRUMENTS_ROOT / "registry.sha256"
MARKDOWN_PATH = INSTRUMENTS_ROOT / "registry.md"
ATLAS_PATH = INSTRUMENTS_ROOT / "atlas.png"

REQUIRED_ENTRY_FIELDS = {
    "id",
    "label",
    "role",
    "unicode_scalars",
    "utf8_hex",
    "ascii_fallback",
    "render",
}
VALID_SPACING = {
    "none",
    "one-after-glyph",
    "one-after-token",
    "one-around-token",
}


class RegistryError(ValueError):
    """Raised when the authoritative registry violates its schema."""


def decode_scalars(scalars: list[str]) -> str:
    characters: list[str] = []
    for scalar in scalars:
        if not re.fullmatch(r"U\+[0-9A-F]{4,6}", scalar):
            raise RegistryError(f"invalid Unicode scalar: {scalar}")
        value = int(scalar[2:], 16)
        if value > 0x10FFFF or 0xD800 <= value <= 0xDFFF:
            raise RegistryError(f"invalid Unicode scalar value: {scalar}")
        characters.append(chr(value))
    return "".join(characters)


def expected_utf8_hex(text: str) -> str:
    return " ".join(f"{byte:02X}" for byte in text.encode("utf-8"))


def load_registry(path: Path = REGISTRY_PATH) -> tuple[bytes, dict[str, Any]]:
    raw = path.read_bytes()
    non_ascii = [index for index, byte in enumerate(raw) if byte >= 0x80]
    if non_ascii:
        first = non_ascii[0]
        raise RegistryError(
            f"{path} must be ASCII-only; byte 0x{raw[first]:02X} at offset {first}"
        )

    registry = json.loads(raw.decode("ascii"))
    validate_registry(registry)
    return raw, registry


def validate_registry(registry: dict[str, Any]) -> None:
    if registry.get("schema") != "operating-instrument-registry/v1":
        raise RegistryError("unsupported or missing registry schema")
    if not re.fullmatch(r"\d+\.\d+\.\d+", registry.get("version", "")):
        raise RegistryError("registry version must use semantic versioning")

    entries = registry.get("instruments")
    if not isinstance(entries, list) or not entries:
        raise RegistryError("registry must contain a non-empty instruments list")

    seen_ids: set[str] = set()
    for entry in entries:
        missing = REQUIRED_ENTRY_FIELDS.difference(entry)
        if missing:
            raise RegistryError(
                f"{entry.get('id', '<unknown>')} missing fields: {sorted(missing)}"
            )

        instrument_id = entry["id"]
        if not re.fullmatch(r"[A-Z][A-Z0-9_]+", instrument_id):
            raise RegistryError(f"invalid instrument ID: {instrument_id}")
        if instrument_id in seen_ids:
            raise RegistryError(f"duplicate instrument ID: {instrument_id}")
        seen_ids.add(instrument_id)

        for field in ("label", "role", "ascii_fallback"):
            value = entry[field]
            if not isinstance(value, str) or not value:
                raise RegistryError(f"{instrument_id}.{field} must be non-empty")
            try:
                value.encode("ascii")
            except UnicodeEncodeError as error:
                raise RegistryError(
                    f"{instrument_id}.{field} must be ASCII-only"
                ) from error

        scalars = entry["unicode_scalars"]
        if not isinstance(scalars, list) or not scalars:
            raise RegistryError(
                f"{instrument_id}.unicode_scalars must be a non-empty list"
            )
        glyph = decode_scalars(scalars)
        if entry["utf8_hex"] != expected_utf8_hex(glyph):
            raise RegistryError(
                f"{instrument_id}.utf8_hex does not match unicode_scalars"
            )

        render = entry["render"]
        if not isinstance(render, dict):
            raise RegistryError(f"{instrument_id}.render must be an object")
        template = render.get("template")
        if not isinstance(template, str) or template.count("{glyph}") != 1:
            raise RegistryError(
                f"{instrument_id}.render.template must contain one {{glyph}}"
            )
        try:
            template.encode("ascii")
        except UnicodeEncodeError as error:
            raise RegistryError(
                f"{instrument_id}.render.template must be ASCII-only"
            ) from error
        if render.get("spacing") not in VALID_SPACING:
            raise RegistryError(
                f"{instrument_id}.render.spacing must be one of {sorted(VALID_SPACING)}"
            )


def registry_digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def markdown_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def markdown_inline_code(value: str) -> str:
    return f"`{markdown_table_cell(value)}`"


def render_markdown(registry: dict[str, Any], digest: str) -> str:
    lines = [
        "# Operating Instrument Registry",
        "",
        "> Generated from `registry.json`; do not edit.",
        "",
        f"- Registry version: `{registry['version']}`",
        f"- SHA-256: `{digest}`",
        "- Authority: the ASCII JSON registry; this document is a rendered view.",
        "",
        "| ID | Glyph | Intended rendering | Unicode scalars | UTF-8 hex | ASCII fallback | Role |",
        "| --- | :---: | --- | --- | --- | --- | --- |",
    ]

    for entry in registry["instruments"]:
        glyph = decode_scalars(entry["unicode_scalars"])
        intended = entry["render"]["template"].replace("{glyph}", glyph)
        scalars = " ".join(entry["unicode_scalars"])
        lines.append(
            "| "
            f"{markdown_inline_code(entry['id'])} | "
            f"{markdown_table_cell(glyph)} | "
            f"{markdown_table_cell(intended)} | "
            f"{markdown_inline_code(scalars)} | "
            f"{markdown_inline_code(entry['utf8_hex'])} | "
            f"{markdown_inline_code(entry['ascii_fallback'])} | "
            f"{markdown_inline_code(entry['role'])} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Unicode scalar sequences are the authoritative instrument identities.",
            "- UTF-8 hex is a transport-integrity cross-check.",
            "- Intended rendering is generated from the registry template.",
            "- ASCII fallbacks are degraded-mode semantics, not alternate styling.",
            "",
        ]
    )
    return "\n".join(lines)


def _font_from_candidates(candidates: list[str], size: int):
    from PIL import ImageFont

    for candidate in candidates:
        path = Path(candidate)
        if not path.exists():
            continue
        try:
            return ImageFont.truetype(str(path), size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _draw_instrument(
    draw,
    position,
    scalars: list[str],
    emoji_font,
    symbol_font,
    text_font,
) -> None:
    glyph = decode_scalars(scalars)
    first = glyph[0]
    remainder_start = 1
    if len(glyph) > 1 and ord(glyph[1]) == 0xFE0F:
        first += glyph[1]
        remainder_start = 2

    first_is_emoji = ord(first[0]) >= 0x1F000 or ord(first[0]) in {
        0x23F1,
        0x2705,
        0x27A1,
    }
    x, y = position

    if first_is_emoji:
        try:
            draw.text(
                (x, y),
                first,
                font=emoji_font,
                embedded_color=True,
                fill=(20, 25, 35, 255),
            )
        except (OSError, ValueError):
            draw.text((x, y), first, font=text_font, fill=(20, 25, 35, 255))
        bbox = draw.textbbox((x, y), first, font=emoji_font)
        x = max(x + 42, bbox[2] + 8)

    remainder = glyph[remainder_start:] if first_is_emoji else glyph
    if remainder:
        remainder_font = (
            text_font
            if ord(remainder[0]) in {0x3014, 0x3015}
            else symbol_font
        )
        draw.text(
            (x, y + 4),
            remainder,
            font=remainder_font,
            fill=(20, 25, 35, 255),
        )


def render_atlas(registry: dict[str, Any], digest: str, output: Path) -> None:
    try:
        from PIL import Image, ImageDraw, PngImagePlugin
    except ImportError as error:
        raise RegistryError(
            "Pillow is required to regenerate atlas.png; "
            "run with --skip-atlas to update text artifacts only"
        ) from error

    text_font = _font_from_candidates(
        [
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/Library/Fonts/Arial Unicode.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        18,
    )
    title_font = _font_from_candidates(
        [
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/Library/Fonts/Arial Unicode.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        28,
    )
    emoji_font = _font_from_candidates(
        [
            "/System/Library/Fonts/Apple Color Emoji.ttc",
            "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
            "/usr/share/fonts/truetype/noto/NotoEmoji-Regular.ttf",
        ],
        32,
    )
    symbol_font = _font_from_candidates(
        [
            "/System/Library/Fonts/Supplemental/STIXTwoMath.otf",
            "/System/Library/Fonts/Symbol.ttf",
            "/System/Library/Fonts/SFNS.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        ],
        24,
    )

    entries = registry["instruments"]
    width = 1500
    header_height = 110
    row_height = 58
    height = header_height + row_height * len(entries) + 30
    image = Image.new("RGBA", (width, height), (247, 249, 252, 255))
    draw = ImageDraw.Draw(image)

    draw.text(
        (30, 24),
        "Operating Instrument Atlas",
        font=title_font,
        fill=(13, 20, 33, 255),
    )
    draw.text(
        (30, 66),
        f"Registry {registry['version']}  |  SHA-256 {digest}",
        font=text_font,
        fill=(70, 79, 92, 255),
    )

    for index, entry in enumerate(entries):
        top = header_height + index * row_height
        if index % 2 == 0:
            draw.rectangle(
                (20, top, width - 20, top + row_height),
                fill=(238, 242, 247, 255),
            )
        draw.line(
            (20, top + row_height, width - 20, top + row_height),
            fill=(215, 220, 228, 255),
            width=1,
        )
        _draw_instrument(
            draw,
            (35, top + 8),
            entry["unicode_scalars"],
            emoji_font,
            symbol_font,
            text_font,
        )
        draw.text(
            (130, top + 17),
            entry["id"],
            font=text_font,
            fill=(13, 20, 33, 255),
        )
        draw.text(
            (500, top + 17),
            entry["label"],
            font=text_font,
            fill=(13, 20, 33, 255),
        )
        draw.text(
            (930, top + 17),
            " ".join(entry["unicode_scalars"]),
            font=text_font,
            fill=(70, 79, 92, 255),
        )
        draw.text(
            (1215, top + 17),
            entry["ascii_fallback"],
            font=text_font,
            fill=(70, 79, 92, 255),
        )

    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("registry_version", registry["version"])
    metadata.add_text("registry_sha256", digest)
    metadata.add_text("generated_from", "operating-contract/v2/instruments/registry.json")
    image.convert("RGB").save(output, format="PNG", pnginfo=metadata, optimize=True)


def png_metadata(path: Path) -> tuple[int, int, dict[str, str]]:
    raw = path.read_bytes()
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RegistryError(f"{path} is not a PNG")

    width, height = struct.unpack(">II", raw[16:24])
    metadata: dict[str, str] = {}
    offset = 8
    while offset < len(raw):
        length = struct.unpack(">I", raw[offset : offset + 4])[0]
        chunk_type = raw[offset + 4 : offset + 8]
        payload = raw[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if chunk_type == b"tEXt":
            key, value = payload.split(b"\0", 1)
            metadata[key.decode("latin-1")] = value.decode("latin-1")
        if chunk_type == b"IEND":
            break
    return width, height, metadata


def expected_digest_file(digest: str) -> str:
    return f"{digest}  registry.json\n"


def check_artifacts(
    registry: dict[str, Any], raw: bytes, *, require_atlas: bool = True
) -> list[str]:
    digest = registry_digest(raw)
    mismatches: list[str] = []

    expected_files = {
        DIGEST_PATH: expected_digest_file(digest),
        MARKDOWN_PATH: render_markdown(registry, digest),
    }
    for path, expected in expected_files.items():
        if not path.exists():
            mismatches.append(f"missing generated artifact: {path}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            mismatches.append(f"stale generated artifact: {path}")

    if require_atlas:
        if not ATLAS_PATH.exists():
            mismatches.append(f"missing generated artifact: {ATLAS_PATH}")
        else:
            width, height, metadata = png_metadata(ATLAS_PATH)
            if width < 800 or height < 600:
                mismatches.append(
                    f"atlas dimensions are unexpectedly small: {width}x{height}"
                )
            if metadata.get("registry_version") != registry["version"]:
                mismatches.append("atlas registry_version metadata is stale")
            if metadata.get("registry_sha256") != digest:
                mismatches.append("atlas registry_sha256 metadata is stale")

    return mismatches


def write_artifacts(
    registry: dict[str, Any], raw: bytes, *, skip_atlas: bool = False
) -> None:
    digest = registry_digest(raw)
    DIGEST_PATH.write_text(expected_digest_file(digest), encoding="ascii")
    MARKDOWN_PATH.write_text(render_markdown(registry, digest), encoding="utf-8")
    if not skip_atlas:
        render_atlas(registry, digest, ATLAS_PATH)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate checked-in artifacts without rewriting them",
    )
    parser.add_argument(
        "--skip-atlas",
        action="store_true",
        help="skip PNG generation or validation",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        raw, registry = load_registry()
        if args.check:
            mismatches = check_artifacts(
                registry,
                raw,
                require_atlas=not args.skip_atlas,
            )
            if mismatches:
                for mismatch in mismatches:
                    print(mismatch, file=sys.stderr)
                return 1
            print(
                f"instrument registry {registry['version']} is valid; "
                f"SHA-256 {registry_digest(raw)}"
            )
            return 0

        write_artifacts(registry, raw, skip_atlas=args.skip_atlas)
        print(
            f"generated instrument registry {registry['version']}; "
            f"SHA-256 {registry_digest(raw)}"
        )
        return 0
    except (OSError, RegistryError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
