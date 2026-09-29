#!/usr/bin/env python3
"""Fetch Surah Yasin (36) from alquran.cloud API and save as JSON."""

import json
import urllib.request
import sys
from pathlib import Path

API_BASE = "https://api.alquran.cloud/v1/surah/36"
ARABIC_EDITION = "quran-uthmani"
INDONESIAN_EDITION = "id.indonesian"

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "data"
OUTPUT_FILE = OUTPUT_DIR / "yasin.json"

EXPECTED_COUNT = 83


def fetch_edition(edition: str) -> list[dict]:
    url = f"{API_BASE}/{edition}"
    print(f"Fetching {url} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "yasin-builder/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("code") != 200:
        print(f"  API returned code {data.get('code')}: {data.get('data')}")
        sys.exit(1)
    ayat = data["data"]["ayahs"]
    print(f"  Got {len(ayat)} ayat")
    return ayat


def main():
    arabic = fetch_edition(ARABIC_EDITION)
    indonesian = fetch_edition(INDONESIAN_EDITION)

    if len(arabic) != EXPECTED_COUNT or len(indonesian) != EXPECTED_COUNT:
        print(f"ERROR: expected {EXPECTED_COUNT} ayat, got Arabic={len(arabic)}, Indonesian={len(indonesian)}")
        sys.exit(1)

    combined = []
    for a, i in zip(arabic, indonesian):
        combined.append({
            "n": a["numberInSurah"],
            "ar": a["text"],
            "id": i["text"],
            "latin": "",
        })

    output = {
        "surah": "Yasin",
        "number": 36,
        "count": EXPECTED_COUNT,
        "ayat": combined,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved {len(combined)} ayat to {OUTPUT_FILE}")
    assert len(combined) == EXPECTED_COUNT, f"Count mismatch: {len(combined)}"


if __name__ == "__main__":
    main()
