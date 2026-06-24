#!/usr/bin/env python3
"""Find duplicate surface forms in a tab-separated lexicon and write them with attributes."""

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

# allow larger fields in lexicon files
csv.field_size_limit(sys.maxsize)


def normalize(value: str) -> str:
    return (value or '').strip()


def parse_row(line: str):
    fields = line.split('\t')
    if len(fields) < 3:
        return None
    surface = normalize(fields[1])
    root = normalize(fields[2])
    primary_pos = normalize(fields[3]) if len(fields) > 3 else ''
    secondary_pos = normalize(fields[4]) if len(fields) > 4 else ''
    attributes = normalize(fields[8]) if len(fields) >= 9 else normalize(' '.join(fields[3:]))
    return {
        'surface': surface,
        'root': root,
        'primary_pos': primary_pos,
        'secondary_pos': secondary_pos,
        'attributes': attributes,
        'row': fields,
    }


def read_lexicon(path: str):
    text = Path(path).read_text(encoding='utf-8-sig')
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return []

    tab_counts = Counter(line.count('\t') for line in lines[:2000])
    expected_tabs = tab_counts.most_common(1)[0][0] if tab_counts else 8

    rows = []
    buffer = ''
    for line in lines:
        if buffer:
            buffer += '\n' + line
            if buffer.count('\t') >= expected_tabs:
                parsed = parse_row(buffer)
                if parsed:
                    rows.append(parsed)
                buffer = ''
            continue

        if line.count('\t') >= expected_tabs:
            parsed = parse_row(line)
            if parsed:
                rows.append(parsed)
        else:
            buffer = line

    if buffer:
        parsed = parse_row(buffer)
        if parsed:
            rows.append(parsed)

    return rows


def find_duplicates(rows):
    grouped = defaultdict(list)
    for item in rows:
        grouped[item['surface']].append(item)

    duplicates = []
    for surface, items in grouped.items():
        if len(items) < 2:
            continue
        unique_keys = {(item['root'], item['attributes']) for item in items}
        if len(unique_keys) < 2:
            continue
        duplicates.extend(items)
    return duplicates


def is_noun(item):
    return item['primary_pos'] == 'Noun' or item['secondary_pos'] == 'Noun'


def dedupe_rows(rows):
    grouped = defaultdict(list)
    for item in rows:
        grouped[item['surface']].append(item)

    result = []
    for surface, items in grouped.items():
        if len(items) == 1:
            result.extend(items)
            continue

        noun_items = [item for item in items if is_noun(item)]
        non_noun_items = [item for item in items if not is_noun(item)]

        if noun_items and non_noun_items:
            # If both noun and non-noun entries share the same surface, keep only noun entries.
            result.extend(noun_items)
        else:
            # Otherwise preserve all duplicates.
            result.extend(items)
    return result


def write_duplicates(duplicates, out_path):
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['surface', 'root', 'attributes', 'full_row_json'])
        for item in duplicates:
            writer.writerow([
                item['surface'],
                item['root'],
                item['attributes'],
                json.dumps(item['row'], ensure_ascii=False),
            ])


def write_deduped_lexicon(rows, out_path):
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        for item in rows:
            f.write('\t'.join(item['row']).rstrip('\n') + '\n')


def main():
    parser = argparse.ArgumentParser(description='Find lexicon entries with the same surface and different root/attributes.')
    parser.add_argument('--input', '-i', default='zemberek/resources/lexicon.csv', help='Path to lexicon file')
    parser.add_argument('--output', '-o', default='duplicates.csv', help='Output CSV file for duplicates')
    parser.add_argument('--dedup-output', '-d', default='zemberek/resources/lexicon.deduped.csv', help='Output path for deduped lexicon')
    args = parser.parse_args()

    rows = read_lexicon(args.input)
    duplicates = find_duplicates(rows)
    write_duplicates(duplicates, args.output)

    deduped_rows = dedupe_rows(rows)
    write_deduped_lexicon(deduped_rows, args.dedup_output)

    print(f'Wrote {len(duplicates)} duplicate rows for {len({item["surface"] for item in duplicates})} surfaces to {args.output}')
    print(f'Wrote {len(deduped_rows)} deduped lexicon rows to {args.dedup_output}')


if __name__ == '__main__':
    main()
