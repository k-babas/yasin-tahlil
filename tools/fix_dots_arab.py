import pathlib, re, subprocess, os

p = pathlib.Path("C:/Users/mahad/yasin-tahlil/index.html")
c = p.read_text(encoding="utf-8")
orig = len(c)

# --- 1) CSS: arab-inline + arab-quote, samakan dgn Scheherazade New ---
old_istirja = ".istirja{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);text-align:center;border:1px solid var(--line);background:var(--card-2);border-radius:999px;padding:7px 10px;width:fit-content;margin:0 auto}"
new_istirja = ".istirja{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);text-align:center;border:1px solid var(--line);background:var(--card-2);border-radius:999px;padding:7px 10px;width:fit-content;margin:0 auto}\n.arab-inline{font-family:'Scheherazade New',serif;font-size:16px;letter-spacing:0;text-transform:none;line-height:1.6}\n.arab-quote{font-family:'Scheherazade New',serif;font-size:17px;line-height:1.9}"
assert old_istirja in c, "istirja css not found"
c = c.replace(old_istirja, new_istirja)
print("patched css arab-inline/arab-quote")

# --- 2) HTML: wrap arab di istirja + quote ---
old_ist = '<div class="istirja">'
assert old_ist in c
c = c.replace(
  '<div class="istirja">',
  '<div class="istirja"><span class="arab-inline">',
  1,
)
# close span before latin dash: the line is:
# <div class="istirja"><span class="arab-inline">إِنَّا ... رَاجِعُونَ — Inna lillahi ...
# need </span> before " — Inna"
old_line = "رَاجِعُونَ — Inna lillahi"
assert old_line in c, "istirja line not found"
c = c.replace(old_line, "رَاجِعُونَ</span> — Inna lillahi", 1)
print("patched istirja html wrap")

old_q = '<div class="quote" id="vQuote">'
assert old_q in c
c = c.replace(
  '<div class="quote" id="vQuote">',
  '<div class="quote" id="vQuote"><span class="arab-quote">',
  1,
)
# close span before <small>
old_qend = "بِفَضْلِكَ.”<small>"
assert old_qend in c, "quote end not found"
c = c.replace(old_qend, "بِفَضْلِكَ.”</span><small>", 1)
print("patched quote html wrap")

# applyCover sets q.firstChild.textContent — firstChild now <span>, still works (element textContent)
# verify: q.firstChild is span element, textContent assignment keeps span. OK.

# --- 3) JS: jangan buat card khusus titik-titik ---
# index.html has one flatMap with "if(tail)"
n_tail = c.count("if(tail)")
print("if(tail) count:", n_tail)
c = c.replace(
  "if(tail)",
  "if(tail && tail.replace(/[.\\u2026\\s]/g,''))",
)
print("patched tail guard x", n_tail)

# node check
m = re.search(r'<script>(.*?)</script>', c, re.S)
js = m.group(1)
tmp = pathlib.Path(os.environ["TEMP"]) / "_fixdots.js"
tmp.write_text(js, encoding="utf-8")
r = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True)
print("node", r.returncode, r.stderr[:400] if r.stderr else "OK")
assert r.returncode == 0

p.write_text(c, encoding="utf-8")
print(f"written index len {len(c)} diff {len(c)-orig}")
