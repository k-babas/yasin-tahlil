import json, pathlib, urllib.request, ssl, sys
ssl._create_default_https_context = ssl._create_unverified_context

SRC = "https://api.alquran.cloud/v1/surah/36/editions/quran-uthmani,en.transliteration,id.indonesian"
OUT = pathlib.Path("C:/Users/mahad/yasin-tahlil/assets/data/yasin.json")
if not OUT.exists():
    OUT = pathlib.Path("assets/data/yasin.json")

print(f"fetch {SRC} ...")
try:
    data = json.loads(urllib.request.urlopen(SRC, timeout=20).read().decode())
except Exception as e:
    print(f"fetch gagal: {e}", file=sys.stderr)
    sys.exit(1)

# data['data'] is list of 3 editions
# 0: quran-uthmani, 1: en.transliteration, 2: id.indonesian
editions = data.get("data", [])
if len(editions) < 3:
    print(f"editions len {len(editions)} unexpected", file=sys.stderr)
    print(json.dumps(data)[:2000])
    sys.exit(1)

trans_ed = editions[1]
quran_ed = editions[0]
indo_ed = editions[2]
print(f"ed 0 {quran_ed.get('edition',{}).get('identifier')} ayahs {len(quran_ed.get('ayahs',[]))}")
print(f"ed 1 {trans_ed.get('edition',{}).get('identifier')} ayahs {len(trans_ed.get('ayahs',[]))}")
print(f"ed 2 {indo_ed.get('edition',{}).get('identifier')} ayahs {len(indo_ed.get('ayahs',[]))}")

trans_map = {a['numberInSurah']: a['text'] for a in trans_ed['ayahs']}
indo_map = {a['numberInSurah']: a['text'] for a in indo_ed['ayahs']}

j = json.loads(OUT.read_text(encoding="utf-8"))
filled = 0
for ax in j["ayat"]:
    n = ax["n"]
    t = trans_map.get(n, "")
    if t:
        ax["latin"] = t
        filled += 1
    # also ensure id from indo if empty (already filled, but keep)
    if not ax.get("id","").strip() and indo_map.get(n):
        ax["id"] = indo_map[n]

OUT.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"filled latin {filled}/83 -> {OUT}")
for ax in j["ayat"][:3]:
    print(f" n={ax['n']} latin={ax['latin'][:80]!r} id={ax['id'][:60]!r}")
