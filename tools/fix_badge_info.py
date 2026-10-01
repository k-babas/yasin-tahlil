import pathlib, re, subprocess, os

p = pathlib.Path("C:/Users/mahad/yasin-tahlil/index.html")
c = p.read_text(encoding="utf-8")
orig = len(c)

# 1) Hapus badge Ayat/Utsmani + Kemenag di ayahCard, sisakan qari
old_badges = '<span class="tag">Ayat ${a.no} \\u2022 Utsmani</span><span class="tag" style="background:var(--gold-soft)">Kemenag</span>'
assert old_badges in c, "badges not found"
c = c.replace(old_badges, "")
print("removed yasin badges")

# 2) Info: pindah kalimat data dari card Tentang ke card Sumber data
old_tentang = " untuk almarhumah. Data Yasin 83 ayat & Tahlil 35 bait di-fetch dari JSON.</p>"
assert old_tentang in c, "tentang sentence not found"
c = c.replace(old_tentang, " untuk almarhumah.</p>")
print("removed tentang data sentence")

old_sumber = "Kemenag & quran.nu.or.id \u2022 83 ayat \u2022 <span id=\"infoTahlilCount\">35</span> bait Tahlil</div>"
assert old_sumber in c, "sumber line not found"
new_sumber = "Kemenag & quran.nu.or.id \u2022 Data Yasin 83 ayat & Tahlil <span id=\"infoTahlilCount\">35</span> bait di-fetch dari JSON.</div>"
c = c.replace(old_sumber, new_sumber)
print("patched sumber data card")

# node check
m = re.search(r"<script>(.*?)</script>", c, re.S)
tmp = pathlib.Path(os.environ["TEMP"]) / "_badge_info.js"
tmp.write_text(m.group(1), encoding="utf-8")
r = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True)
print("node", r.returncode, r.stderr[:400] if r.stderr else "OK")
assert r.returncode == 0

p.write_text(c, encoding="utf-8")
print(f"written len {len(c)} diff {len(c) - orig}")
