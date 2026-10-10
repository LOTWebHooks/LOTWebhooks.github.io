#!/usr/bin/env python3

import csv
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = ROOT / "index.html"
CSV_OUT = ROOT / "data" / "webhooks.csv"
BADGE_OUT = ROOT / "data" / "badge.json"


def normalize_text(value):
    return re.sub(r"\s+", " ", value).strip()


class WebhookTableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found_table = False
        self.in_table = False
        self.row = None
        self.cell_text = None
        self.code_text = None
        self.code_depth = 0
        self.rows = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "table" and attributes.get("id") == "hooks":
            self.found_table = True
            self.in_table = True
        elif self.in_table:
            if tag == "tr":
                self.row = []
            elif tag == "td" and self.row is not None:
                self.cell_text = []
                self.code_text = []
            elif tag == "code" and self.cell_text is not None:
                self.code_depth += 1

    def handle_endtag(self, tag):
        if not self.in_table:
            return

        if tag == "code" and self.code_depth:
            self.code_depth -= 1
        elif tag == "td" and self.cell_text is not None:
            self.row.append(
                {
                    "text": normalize_text("".join(self.cell_text)),
                    "code": normalize_text("".join(self.code_text)),
                }
            )
            self.cell_text = None
            self.code_text = None
        elif tag == "tr" and self.row is not None:
            if len(self.row) == 4:
                self.rows.append(self.row)
            self.row = None
        elif tag == "table":
            self.in_table = False

    def handle_data(self, data):
        if self.cell_text is not None:
            self.cell_text.append(data)
            if self.code_depth:
                self.code_text.append(data)


def parse_rows(markup):
    parser = WebhookTableParser()
    parser.feed(markup)
    if not parser.found_table:
        raise ValueError('Could not find <table id="hooks"> in index.html')

    return [
        {
            "name": row[0]["text"],
            "endpoint": row[1]["code"] or row[1]["text"],
            "type": row[2]["text"],
            "reference": row[3]["text"],
        }
        for row in parser.rows
    ]


def write_csv(rows):
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(
            output, fieldnames=["name", "endpoint", "type", "reference"]
        )
        writer.writeheader()
        writer.writerows(rows)


def write_badge(count):
    badge = {
        "schemaVersion": 1,
        "label": "entries",
        "message": str(count),
        "color": "56e795",
    }
    BADGE_OUT.parent.mkdir(parents=True, exist_ok=True)
    with BADGE_OUT.open("w", encoding="utf-8") as output:
        json.dump(badge, output, indent=2)
        output.write("\n")


def main():
    markup = INDEX_HTML.read_text(encoding="utf-8")
    rows = parse_rows(markup)
    write_csv(rows)
    write_badge(len(rows))
    print(f"Wrote {len(rows)} rows to {CSV_OUT.relative_to(ROOT)}")
    print(f"Wrote entry-count badge to {BADGE_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
