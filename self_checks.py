"""Student-facing self-checks for PS6 (same cases as the autograder)."""
from __future__ import annotations

import shutil
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


def _call_using_file_path(func, file_path="data/codons.txt"):
    """Call func with a copy at another path; hide the default file so hardcoding fails."""
    real = Path(file_path)
    with tempfile.TemporaryDirectory() as tmp:
        alt = Path(tmp) / "codon_table.tsv"
        shutil.copy(real, alt)
        hidden = real.with_name(real.name + ".bak_selfcheck")
        real.rename(hidden)
        try:
            return func(str(alt))
        finally:
            if not real.exists() and hidden.exists():
                hidden.rename(real)


def run_create_codon_dict_checks(func, file_path="data/codons.txt"):
    earned = total = 0
    path = Path(file_path)
    if not path.is_file():
        print(f"[FAIL] missing data file: {file_path}")
        return False

    try:
        d = _call_using_file_path(func, file_path)
    except FileNotFoundError as e:
        print(
            "[FAIL] create_codon_dict raised FileNotFoundError\n"
            "    Hint: open the path passed as file_path — do not hardcode "
            f"'data/codons.txt' ({e})"
        )
        return False
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
