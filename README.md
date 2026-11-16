# PS6 — Codon → amino-acid dictionary

Read a tab-separated codon table from a text file and build a dictionary.

**Due (Odyssey):** 25/11/2026 at 08:00 (Asia/Jerusalem).

## What to change

### `codons.py`

Implement:

```python
def create_codon_dict(file_path):
    ...
```

- The caller passes `file_path` — open **that** path (do not hardcode a filename), read its lines, then close it.
- An example valid file is provided: `data/codons.txt`. Each line looks like: `AAA\tLys\tK\tLysine\n`
- Return a dict mapping **column 1 → column 3** (for the example file: codon → one-letter amino acid).
- Example from `data/codons.txt`: `"AAA" → "K"`, `"ATG" → "M"`, stop codons map to `"O"`.

Keep the provided `data/codons.txt` in the repo (do not rename it).

## Practice in Colab (optional)

**From GitHub:** use **Ctrl+click** / **⌘+click** (or middle-click) so Colab opens in a new tab.

- <a href="https://colab.research.google.com/github/TelHai-python-Odyssey-CS-2027/ps6/blob/main/codons.ipynb" target="_blank" rel="noopener noreferrer"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> `codons.ipynb`

The notebook is not graded — only `codons.py` counts. It loads `self_checks.py` with the **same cases** as the autograder.

## Submit

1. Accept the Classroom 50 assignment.
2. Edit `codons.py`, then **Commit changes**.
3. Check the latest autograding run for your score.

## Grading — 10 points

| Check | Points |
| --- | ---: |
| `AAA` → `K` | 1 |
| `AAC` → `N` | 1 |
| `ATG` → `M` | 1 |
| `TTT` → `F` | 1 |
| `TGG` → `W` | 1 |
| `TAA` → `O` (stop) | 1 |
| `TAG` → `O` (stop) | 1 |
| `TGA` → `O` (stop) | 1 |
| Dictionary has 64 keys | 1 |
| Values are single-letter strings | 1 |

## Optional: keep Colab work in Drive

In Colab: **File → Save a copy in Drive**.
