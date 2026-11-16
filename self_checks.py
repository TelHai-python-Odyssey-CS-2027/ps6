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


def _with_hidden_default(real: Path, alt: Path, func):
    """Call func(alt) while the default data file is temporarily renamed away."""
    hidden = real.with_name(real.name + ".bak_selfcheck")
    real.rename(hidden)
    try:
        return func(str(alt))
    finally:
        if not real.exists() and hidden.exists():
            hidden.rename(real)


def _plant_aaa(text: str, letter: str) -> str:
    out = []
    for line in text.splitlines(True):
        if line.startswith("AAA\t"):
            parts = line.rstrip("\n\r").split("\t")
            if len(parts) >= 3:
                parts[2] = letter
            nl = "\n" if line.endswith("\n") else ""
            line = "\t".join(parts) + nl
        out.append(line)
    return "".join(out)


def run_create_codon_dict_checks(func, file_path="data/codons.txt"):
    earned = total = 0
    path = Path(file_path)
    if not path.is_file():
        print(f"[FAIL] missing data file: {file_path}")
        return False

    original = path.read_text()

    try:
        with tempfile.TemporaryDirectory() as tmp:
            # Canary: altered AAA must be returned → proves the given path was read.
            alt_canary = Path(tmp) / "canary.tsv"
            alt_canary.write_text(_plant_aaa(original, "Z"))
            d_canary = _with_hidden_default(path, alt_canary, func)

            if not isinstance(d_canary, dict):
                print(f"[FAIL] return type should be dict, got {type(d_canary).__name__}")
                return False
            if d_canary.get("AAA") != "Z":
                print(
                    "[FAIL] create_codon_dict did not use file_path\n"
                    "    Hint: open and read the path passed in (do not hardcode "
                    "'data/codons.txt' or a fixed dictionary)"
                )
                return False

            # Normal table for the scored checks.
            alt = Path(tmp) / "codon_table.tsv"
            alt.write_text(original)
            d = _with_hidden_default(path, alt, func)
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
