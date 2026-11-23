"""Bounded retrieval and style discovery against a read-only catalog."""

import difflib
import json
import re

from .common import ROOT, connect, read_json

STOP = set(
    "a an and are as at be can could for from give help i icon icons in is it me my need of on or please represent show some suitable that the this to use want with would".split()
)


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


class Catalog:
    def __init__(self, library):
        self.library = library
        self.db = connect(library)
        self.style_data = {r["directory"]: dict(r) for r in self.db.execute("SELECT * FROM styles")}

    def close(self):
        self.db.close()

    def canonical(self, name):
        name = name.lower().strip()
        if name.startswith("fa-"):
            name = name[3:]
        row = self.db.execute("SELECT name FROM icons WHERE name=?", (name,)).fetchone()
        if not row:
            row = self.db.execute("SELECT name FROM aliases WHERE alias=?", (name,)).fetchone()
        if not row:
            raise ValueError(f"Unknown icon: {name}. Use search to find a related icon.")
        return row[0]

    def variants(self, name, family=None, weight=None):
        if family == "brands":
            family, weight = "classic", "brands"
        if family and family not in {s["family"] for s in self.style_data.values()}:
            raise ValueError(f"Unknown family: {family}; use styles to list families.")
        if weight and weight not in {"solid", "semibold", "regular", "light", "thin", "brands"}:
            raise ValueError(f"Unknown weight: {weight}")
        rows = [
            dict(r)
            for r in self.db.execute("SELECT * FROM variants WHERE name=? ORDER BY family,weight", (name,))
        ]
        for row in rows:
            style = self.style_data[row["directory"]]
            row.update(prefix=style["prefix"], fresh=bool(style["fresh"]), description=style["description"])
        return [
            r for r in rows if (not family or r["family"] == family) and (not weight or r["weight"] == weight)
        ]

    def recommendations(self, rows):
        fresh = sorted(
            (r for r in rows if r["fresh"]),
            key=lambda r: ("duo" not in r["family"], r["family"], r["weight"]),
        )
        house = [r for r in rows if r["family"] == "duotone" and r["weight"] == "light"]
        fallback = sorted(
            rows, key=lambda r: (r["family"] != "classic", r["weight"] != "light", r["directory"])
        )
        result = []
        for row in fresh[:3] + house + fallback[:1]:
            if row not in result:
                result.append(row)
        return result

    def inspect(self, name, family=None, weight=None, all_variants=True):
        canonical = self.canonical(name)
        icon = dict(self.db.execute("SELECT * FROM icons WHERE name=?", (canonical,)).fetchone())
        for key in ("aliases", "terms", "categories"):
            icon[key] = json.loads(icon[key])
        rows = self.variants(canonical, family, weight)
        icon.update(
            requested_name=name,
            available_variants=len(rows),
            style_available=bool(rows),
            recommendations=self.recommendations(rows),
        )
        if all_variants:
            icon["variants"] = rows
        return icon

    def styles(self, name=None):
        if name:
            return self.inspect(name)["variants"]
        rows = self.db.execute("""SELECT s.*, count(v.name) AS icons FROM styles s
            JOIN variants v ON s.directory=v.directory GROUP BY s.directory ORDER BY s.family,s.weight""")
        return [dict(r) for r in rows]

    def search(self, query, limit=5, family=None, weight=None):
        normalized = " ".join(words(query))
        tokens = set(words(query)) - STOP
        if not tokens:
            # Some canonical icons are letters or stop words, such as a, i, and at.
            try:
                self.canonical(query)
                tokens = set(words(query))
            except ValueError as error:
                raise ValueError("Provide an icon name or a descriptive concept.") from error
        # Validate constraints even when retrieval returns no candidates.
        self.variants("", family, weight)
        candidates = {}

        def add(name, score, kind, evidence):
            try:
                name = self.canonical(name)
            except ValueError:
                return
            if name not in candidates or score > candidates[name][0]:
                candidates[name] = (score, kind, evidence)

        slug = "-".join(words(query))
        for value in (query.strip().lower(), slug):
            try:
                name = self.canonical(value)
            except ValueError:
                continue
            add(name, 1000, "exact", [f"Canonical name or alias: {value}"])
        fts = " OR ".join('"' + t + '"' for t in sorted(tokens))
        rows = self.db.execute(
            """SELECT rowid, bm25(search,10,8,8,4,1) AS rank
            FROM search WHERE search MATCH ? ORDER BY rank LIMIT 180""",
            (fts,),
        ).fetchall()
        for row in rows:
            icon = self.db.execute("SELECT * FROM icons WHERE rowid=?", (row["rowid"],)).fetchone()
            terms = json.loads(icon["terms"])
            text = " ".join([icon["name"], icon["label"], *terms, *json.loads(icon["categories"])])
            overlap = tokens & set(words(text))
            exact_term = any(normalized == " ".join(words(t)) for t in terms)
            score = 30 + 15 * len(overlap) / len(tokens) + min(25, -row["rank"]) + 30 * exact_term
            evidence = (
                "Metadata terms: " + ", ".join(sorted(overlap))
                if overlap
                else "Stemmed metadata match: " + normalized
            )
            add(icon["name"], score, "related", [evidence])
        concepts = read_json(ROOT / "data/concepts.json")["concepts"]
        for concept in concepts:
            matched = [
                t for t in concept["terms"] if " " + " ".join(words(t)) + " " in " " + normalized + " "
            ]
            if not matched:
                continue
            for kind in ("related", "broader"):
                for i, name in enumerate(concept[kind]):
                    add(
                        name,
                        (300 if kind == "related" else 200) - i,
                        kind,
                        [f"Concept: {matched[0]}", concept["reason"]],
                    )
        if not any(score >= 200 for score, _, _ in candidates.values()):
            names = [r[0] for r in self.db.execute("SELECT name FROM icons UNION SELECT alias FROM aliases")]
            for close in difflib.get_close_matches(slug, names, n=5, cutoff=0.78):
                canonical = self.canonical(close)
                add(
                    canonical,
                    150 * difflib.SequenceMatcher(None, slug, close).ratio(),
                    "related",
                    [f"Possible spelling match: {close}"],
                )
        results = []
        unavailable = []
        for name, (score, kind, evidence) in sorted(
            candidates.items(), key=lambda item: (-item[1][0], item[0])
        ):
            icon = self.inspect(name, family, weight, all_variants=False)
            icon.update(match_kind=kind, evidence=evidence)
            if icon["style_available"]:
                results.append(icon)
            elif score >= 1000:
                icon["available_styles"] = sorted({r["directory"] for r in self.variants(name)})
                unavailable.append(icon)
            if len(results) >= limit:
                break
        return {
            "query": query,
            "requested_style": {"family": family, "weight": weight},
            "results": results,
            "unavailable_exact_matches": unavailable,
            "judgment": "Metadata retrieves candidates; use artifact context to judge semantic and visual fit.",
        }
