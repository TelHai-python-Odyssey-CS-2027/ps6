"""Student-facing self-checks for PS6 (same cases as the autograder)."""
from __future__ import annotations

import tempfile
from pathlib import Path


def _check(title, points, ok, detail=""):
    if ok:
        print(f"[PASS] {title}  ({points}/{points} pt)")
        return points
    print(f"[FAIL] {title}  (0/{points} pt)")
    if detail:
        print(detail)
    return 0


def _must_use_file_path(func) -> bool:
    """Call with a tiny dummy TSV; hardcoded data/codons.txt or a fixed dict will fail."""
    dummy = (
        "XX1\tIgn\tA\tIgnore\n"
        "XX2\tIgn\tB\tIgnore\n"
        "XX3\tIgn\tC\tIgnore\n"
    )
    expected = {"XX1": "A", "XX2": "B", "XX3": "C"}
    with tempfile.TemporaryDirectory() as tmp:
        alt = Path(tmp) / "dummy_table.tsv"
        alt.write_text(dummy)
        try:
            got = func(str(alt))
        except Exception as e:
            print(
                f"[FAIL] create_codon_dict raised {type(e).__name__} on a dummy file_path: {e}\n"
                "    Hint: open the path passed as file_path (not a hardcoded filename)"
            )
            return False
    if not isinstance(got, dict):
        print(f"[FAIL] return type should be dict, got {type(got).__name__}")
        return False
    if got != expected:
        print(
            "[FAIL] create_codon_dict did not use file_path\n"
            f"    Hint: expected {expected} from a dummy TSV, got {got!r}\n"
            "    Open and parse the given path; do not hardcode 'data/codons.txt' or answers"
        )
        return False
    print("[PASS] create_codon_dict uses file_path (dummy file)")
    return True


def run_create_codon_dict_checks(func, file_path="data/codons.txt"):
    earned = total = 0
    path = Path(file_path)
    if not path.is_file():
        print(f"[FAIL] missing data file: {file_path}")
        return False

    if not _must_use_file_path(func):
        return False

    try:
        d = func(file_path)
    except Exception as e:
        print(f"[FAIL] create_codon_dict raised {type(e).__name__}: {e}")
        return False

    if not isinstance(d, dict):
        print(f"[FAIL] return type should be dict, got {type(d).__name__}")
        return False

    cases = [
        ("create_codon_dict: AAA → K", 1, d.get("AAA") == "K", "expected 'K' for codon AAA"),
        ("create_codon_dict: AAC → N", 1, d.get("AAC") == "N", "expected 'N' for codon AAC"),
        ("create_codon_dict: ATG → M (start)", 1, d.get("ATG") == "M", "expected 'M' for ATG"),
        ("create_codon_dict: TTT → F", 1, d.get("TTT") == "F", "expected 'F' for TTT"),
        ("create_codon_dict: TGG → W", 1, d.get("TGG") == "W", "expected 'W' for TGG"),
        ("create_codon_dict: TAA stop → O", 1, d.get("TAA") == "O", "this table uses 'O' for stop"),
        ("create_codon_dict: TAG stop → O", 1, d.get("TAG") == "O", "this table uses 'O' for stop"),
        ("create_codon_dict: TGA stop → O", 1, d.get("TGA") == "O", "this table uses 'O' for stop"),
        ("create_codon_dict: 64 codons", 1, len(d) == 64, f"expected 64 keys, got {len(d)}"),
        (
            "create_codon_dict: one-letter values",
            1,
            all(isinstance(v, str) and len(v) == 1 for v in d.values()),
            "use column 3 (1-letter code), not the 3-letter name",
        ),
    ]
    for title, points, ok, detail in cases:
        total += points
        earned += _check(title, points, ok, f"    Hint: {detail}")

    print(f"\nSelf-check score: {earned}/{total}")
    return earned == total
