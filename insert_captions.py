#!/usr/bin/env python3
"""Insert captions/tags from captions.csv into index.html's gallery photos.

Usage: python3 insert_captions.py

Reads captions.csv (columns: filename, caption, tag). For each gallery photo
in index.html whose filename has a non-empty caption/tag in the CSV, fills
in its (currently empty, contenteditable) figcaption and/or stamps a
data-tag="..." attribute onto its <img> (for a future category-filter
feature -- birthdays, weddings, holidays, etc.).

Blank cells in the CSV are left alone (existing caption/tag, if any, is kept
as-is), so you can fill in captions.csv incrementally and re-run this
script safely as many times as you like.
"""
import csv
import re

INDEX = "index.html"
CSV_PATH = "captions.csv"


def escape(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    s = s.replace("\r", "").replace("\n", "\\n")
    return s


def main():
    rows = {}
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)  # header
        for row in reader:
            if not row:
                continue
            fn = row[0].strip()
            cap = row[1].strip() if len(row) > 1 else ""
            tag = row[2].strip() if len(row) > 2 else ""
            if fn:
                rows[fn] = (cap, tag)

    with open(INDEX, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        r'(?P<prefix><img src=\\"img/webp/(?P<fn>[A-Za-z0-9_]+\.webp)\\" '
        r'alt=\\"Decorated sugar cookies by Sprinkle Kindness\\" )'
        r'(?:data-tag=\\"(?P<existing_tag>.*?)\\" )?'
        r'(?P<mid>style=\\".*?\\">\\n\s*<figcaption class=\\"ck-cap\\" '
        r'data-ph=\\"Add a caption…\\" '
        r'style=\\".*?\\">)(?P<existing_cap>.*?)(?P<close><\\u002Ffigcaption>)'
    )

    caps_updated = tags_updated = unknown_count = 0
    unknown = []

    def replace(m):
        nonlocal caps_updated, tags_updated, unknown_count
        fn = m.group("fn")
        entry = rows.get(fn)
        if entry is None:
            unknown.append(fn)
            return m.group(0)
        cap, tag = entry

        final_tag = tag or m.group("existing_tag") or ""
        if tag:
            tags_updated += 1
        tag_attr = f'data-tag=\\"{escape(final_tag)}\\" ' if final_tag else ""

        if cap:
            caps_updated += 1
            final_cap = escape(cap)
        else:
            final_cap = m.group("existing_cap")

        return (
            m.group("prefix") + tag_attr + m.group("mid") + final_cap + m.group("close")
        )

    new_content, count = pattern.subn(replace, content)

    print(f"Matched {count} gallery slots in {INDEX}")
    print(f"Captions inserted/updated: {caps_updated}")
    print(f"Tags inserted/updated: {tags_updated}")
    if unknown:
        print(f"WARNING: filenames in {INDEX} not found in {CSV_PATH}: {unknown}")
    if count != 66:
        print(f"WARNING: expected 66 gallery slots, matched {count}")

    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    main()
