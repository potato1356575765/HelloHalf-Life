#!/usr/bin/env python3
"""Preflight: overlay every design sheet and list what is unfinished.

Every row x column cell is a checkbox. A cell fails when it is empty
("" or null), when its row is not verified, or when it names a row in
another sheet that does not exist. Exit code 0 only when all pass.
"""
import json
import sys
from pathlib import Path

DESIGN = Path(__file__).resolve().parent.parent / "design"


def load_sheets():
    sheets = {}
    for path in sorted(DESIGN.glob("*.json")):
        data = json.loads(path.read_text())
        sheets[data["sheet"]] = data
    return sheets


def check(sheets):
    empty, unverified, broken = [], [], []
    ids = {name: {row["id"] for row in s["rows"]} for name, s in sheets.items()}
    for name, sheet in sheets.items():
        for row in sheet["rows"]:
            where = f"{name}.{row['id']}"
            for col in sheet["columns"]:
                value = row.get(col)
                if value is None or value == "":
                    empty.append(f"{where}.{col}")
            if row.get("verified") is not True:
                unverified.append(where)
            for col, target in sheet.get("refs", {}).items():
                values = row.get(col)
                for ref in values if isinstance(values, list) else [values]:
                    if ref in (None, ""):
                        continue
                    if target not in ids:
                        broken.append(f"{where}.{col} -> missing sheet '{target}'")
                    elif ref not in ids[target]:
                        broken.append(f"{where}.{col} -> '{ref}' not in {target}")
    return empty, unverified, broken


def main():
    sheets = load_sheets()
    empty, unverified, broken = check(sheets)
    total = sum(len(s["rows"]) * len(s["columns"]) for s in sheets.values())
    print(f"{len(sheets)} sheets, {sum(len(s['rows']) for s in sheets.values())} rows, {total} cells")
    for title, items in (("Broken references", broken), ("Empty cells", empty), ("Unverified rows", unverified)):
        print(f"\n{title}: {len(items)}")
        for item in items:
            print(f"  - {item}")
    clean = not (empty or unverified or broken)
    print("\nPREFLIGHT", "CLEAN" if clean else "NOT CLEAN: fix the above before building")
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
