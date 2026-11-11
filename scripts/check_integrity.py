"""Integrity checks for the APCD-CDL source files and crosswalks.

Run from the repository root:

    python3 scripts/check_integrity.py

Checks:
  1. Spec structure: in each source/files/*.csv, element_id values are
     well formed, unique, and numbered 001..n without gaps, optionally
     followed by the Un-assigned row (XXX) and the 899 Record Type row; type
     and max_length are populated (the PV Un-assigned row is blank as published).
  2. Crosswalk references: every element_id in crosswalks/*/source/*.csv
     exists in source/files/. The spec's own Un-assigned rows
     (CDLMEXXX, CDLMCXXX, CDLPCXXX) are allowed.
  3. Crosswalk names: each crosswalk element_name matches the spec name for
     its element_id, with whitespace ignored. A mismatch is a warning only.

Exits non-zero if check 1 or 2 fails. Uses only the Python standard library.
"""
import argparse
import csv
import glob
import re
import sys
from pathlib import Path

ID = re.compile(r"^CDL([A-Z]{2})(\d{3}|XXX)$")
CROSSWALK_ALLOWED = {"CDLMEXXX", "CDLMCXXX", "CDLPCXXX"}


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_spec(elements_dir):
    errors, ids = [], {}
    files = sorted(Path(elements_dir).glob("*.csv"))
    if not files:
        return [f"no element files found in {elements_dir}"], ids
    for path in files:
        rows = read_rows(path)
        if not rows:
            errors.append(f"{path.name}: no element rows")
            continue
        codes, nums = set(), []
        for i, row in enumerate(rows, start=1):
            eid = (row.get("element_id") or "").strip()
            m = ID.match(eid)
            if not m:
                errors.append(f"{path.name} row {i}: malformed element_id {eid!r}")
                continue
            if eid in ids:
                errors.append(f"{path.name} row {i}: duplicate element_id {eid}")
            ids[eid] = row.get("element_name") or ""
            codes.add(m.group(1))
            nums.append(m.group(2))
            unassigned = m.group(2) == "XXX"
            for col in ("type", "max_length"):
                if not (row.get(col) or "").strip() and not unassigned:
                    errors.append(f"{path.name} row {i}: {eid} has no {col}")
        if len(codes) > 1:
            errors.append(f"{path.name}: mixes file codes {sorted(codes)}")
        seq = [int(n) for n in nums if n.isdigit() and int(n) < 800]
        if seq != list(range(1, len(seq) + 1)):
            errors.append(f"{path.name}: element numbers are not 001..{len(seq):03d} in order")
        tail = [n for n in nums if n == "XXX" or (n.isdigit() and int(n) >= 800)]
        if tail not in ([], ["899"], ["XXX", "899"]) or (tail and nums[-len(tail):] != tail):
            errors.append(f"{path.name}: trailing rows must be [XXX,] 899 at the end; found {tail}")
    return errors, ids


def squash(s):
    return re.sub(r"\s+", "", s or "")


def check_crosswalks(crosswalk_glob, spec_ids):
    errors, warnings = [], []
    files = sorted(Path(p) for p in glob.glob(crosswalk_glob))
    for path in files:
        for i, row in enumerate(read_rows(path), start=1):
            eid = (row.get("element_id") or "").strip()
            if eid in CROSSWALK_ALLOWED:
                continue
            if eid not in spec_ids:
                errors.append(f"{path} row {i}: element_id {eid!r} not found in the spec")
            elif "element_name" in row and squash(row["element_name"]) != squash(spec_ids[eid]):
                warnings.append(f"{path} row {i}: {eid} element_name {row['element_name']!r} "
                                f"differs from the spec name {spec_ids[eid]!r}")
    return errors, warnings, len(files)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--elements-dir", default="source/files")
    ap.add_argument("--crosswalks", default="crosswalks/*/source/*.csv")
    args = ap.parse_args()

    spec_errors, spec_ids = check_spec(args.elements_dir)
    xw_errors, xw_warnings, n_xw = check_crosswalks(args.crosswalks, spec_ids)

    for e in spec_errors + xw_errors:
        print("FAIL", e)
    for w in xw_warnings:
        print("WARN", w)
    print(f"spec: {len(spec_ids)} element ids, {len(spec_errors)} problem(s)")
    print(f"crosswalks: {n_xw} file(s) checked, {len(xw_errors)} problem(s), "
          f"{len(xw_warnings)} name warning(s)")
    return 1 if spec_errors or xw_errors else 0


if __name__ == "__main__":
    sys.exit(main())
