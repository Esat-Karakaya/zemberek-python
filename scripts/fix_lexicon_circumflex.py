#!/usr/bin/env python3
"""
Fix lexicon.csv: if lemma contains circumflex (â,î,û) and root equals lemma with
circumflexes removed (â->a, î->i, û->u), replace root with lemma.
If lemma contains circumflex but root is not the normalized lemma, print it and
leave unchanged.

Usage: python scripts/fix_lexicon_circumflex.py [--dry-run] [path/to/lexicon.csv]
"""
import argparse
import csv
import shutil
from pathlib import Path

CIRC_MAP = {
    'â': 'a', 'î': 'i', 'û': 'u',
    'Â': 'A', 'Î': 'I', 'Û': 'U'
}
CIRCUMFLEX_CHARS = set('âîûÂÎÛ')


def normalize_remove_circ(lemma: str) -> str:
    return ''.join(CIRC_MAP.get(c, c) for c in lemma)


def process(lex_path: Path, dry_run: bool = False):
    if not lex_path.exists():
        raise FileNotFoundError(f"File not found: {lex_path}")

    backup = lex_path.with_suffix(lex_path.suffix + '.bak')
    if not dry_run:
        shutil.copy2(lex_path, backup)
        print(f"Backup written to {backup}")
    else:
        print("Dry-run: no backup written")

    updated_lines = []
    exceptions = []
    changed_count = 0
    total = 0

    with lex_path.open('r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in reader:
            total += 1
            # ensure row has at least 9 columns by padding
            if len(row) < 9:
                row += [''] * (9 - len(row))

            lemma = row[1]
            root = row[2]

            # Only consider lemmas that contain circumflex characters
            if any(c in CIRCUMFLEX_CHARS for c in lemma):
                normalized = normalize_remove_circ(lemma)
                # If root equals normalized lemma (exact) OR differs only by case,
                # replace root with the lemma in lowercase form.
                if normalized == root:
                    row[2] = lemma
                    changed_count += 1
                elif normalized.lower() == root.lower():
                    row[2] = lemma.lower()
                    changed_count += 1
                else:
                    exceptions.append((total, row))
            updated_lines.append(row)

    # Write back
    if not dry_run:
        tmp_path = lex_path.with_suffix(lex_path.suffix + '.tmp')
        with tmp_path.open('w', encoding='utf-8', newline='') as outf:
            writer = csv.writer(outf, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar='\\')
            for row in updated_lines:
                writer.writerow(row)
        # Replace original
        shutil.move(str(tmp_path), str(lex_path))
        print(f"Wrote {changed_count} changes to {lex_path}")
    else:
        print(f"Dry-run: would change {changed_count} rows")

    if exceptions:
        print('\nExceptions (lemma contains circumflex but root differs from normalized lemma):')
        for idx, row in exceptions:
            print(idx, '\t'.join(row))
    else:
        print('\nNo exceptions found')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('lexicon', nargs='?', default='zemberek/resources/lexicon.csv')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    process(Path(args.lexicon), dry_run=args.dry_run)
