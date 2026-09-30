import pathlib, re, subprocess, os

p = pathlib.Path("C:/Users/mahad/yasin-tahlil/index.html")
c = p.read_text(encoding="utf-8")
orig_len = len(c)
print(f"orig len {orig_len}")

# 1) Foto lebih tinggi
if "min-height:520px" in c:
    c = c.replace("min-height:520px", "min-height:580px")
    print("patched cover min-height 520->580")

if "aspect-ratio:4/5" in c:
    c = c.replace("aspect-ratio:4/5", "aspect-ratio:3/4")
    print("patched aspect 4/5 -> 3/4 (desktop)")

if "aspect-ratio:4/3" in c:
    c = c.replace("aspect-ratio:4/3", "aspect-ratio:3/4")
    print("patched mobile 4/3->3/4")

if "aspect-ratio:3/4;border-radius:22px;" in c:
    c = c.replace("aspect-ratio:3/4;border-radius:22px;", "aspect-ratio:3/4;min-height:420px;border-radius:22px;")
    print("added min-height 420 to photo-frame")

if ".photo-frame{aspect-ratio:3/4}" in c:
    c = c.replace(".photo-frame{aspect-ratio:3/4}", ".photo-frame{aspect-ratio:3/4;min-height:320px}")
    print("added mobile min-height 320")

print("css photo check:", "min-height:420px" in c)

# 2) Font Arab - samakan
old_meta = '<div class="meta-value" style="font-family:\'Scheherazade New\',serif;font-size:15px">'
new_meta = '<div class="meta-value arab" style="font-size:15px">'
if old_meta in c:
    c = c.replace(old_meta, new_meta)
    print("patched meta arab to class")
else:
    print("meta old not found")

if ".ayah-body .arab{font-family:'Scheherazade New',serif;font-size:var(--arab);" in c:
    c = c.replace(".ayah-body .arab{font-family:'Scheherazade New',serif;font-size:var(--arab);", ".arab{font-family:'Scheherazade New',serif}\n.ayah-body .arab{font-family:'Scheherazade New',serif;font-size:var(--arab);")
    print("added .arab base rule")

# 3) Icon Latin/Terjemah/Arab saja di Yasin
old_latin_icon = '<path d="M4 7V5h16v2"/><path d="M9 20h6"/><path d="M12 5v15"/>'
new_latin_icon = '<path d="M7 20L12 4L17 20"/><path d="M9 15H15"/>'
if old_latin_icon in c:
    c = c.replace(old_latin_icon, new_latin_icon)
    print("patched Latin icon T->A")

old_terjemah_icon = '<path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20"/><path d="M12 2a15 15 0 0 0 0 20"/>'
new_terjemah_icon = '<path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20"/><path d="M12 2a15 15 0 0 0 0 20"/><path d="M16 8l2 2-2 2"/><path d="M8 16l-2-2 2-2"/>'
if old_terjemah_icon in c:
    c = c.replace(old_terjemah_icon, new_terjemah_icon, 1)
    print("patched Terjemah icon globe->with arrows")

old_arab_pill = '<button class="pill" id="pillArabOnly">Arab saja</button>'
new_arab_pill = '<button class="pill" id="pillArabOnly"><svg class="ico ico-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 20c1.5-2 2.5-4 2.5-7V8"/><path d="M12 13c0 2 1.2 3.5 3 4"/><path d="M14 8v5"/><circle cx="16" cy="6" r="1.2" fill="currentColor" stroke="none"/></svg> Arab saja</button>'
if old_arab_pill in c:
    c = c.replace(old_arab_pill, new_arab_pill)
    print("patched Arab pill add icon")

# 4) Tambah pills di tab Tahlil
old_tahlil = '<div class="panel" id="panel-tahlil"><div class="hero-mini"><svg class="ico ico-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"/><path d="M12 7V3M12 21v-4M7 12H3M21 12h-4"/></svg> <div><b>Tahlil untuk <span class="js-name">Lia Aris Tiarawati</span></b> <small> \u2022 24 bait \u2022 Urutan NU lengkap</small></div><button class="btn-sm" data-jump="cover" style="margin-left:auto"><svg class="ico ico-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg> Awal</button></div><div class="list" id="list-tahlil">'
new_tahlil = '<div class="panel" id="panel-tahlil"><div class="hero-mini"><svg class="ico ico-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"/><path d="M12 7V3M12 21v-4M7 12H3M21 12h-4"/></svg> <div><b>Tahlil untuk <span class="js-name">Lia Aris Tiarawati</span></b> <small> \u2022 27 bait *</small></div></div><div class="filterbar" style="justify-content:center"><div class="filter-pills"><button class="pill on" id="pillLatinT"><svg class="ico ico-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 20L12 4L17 20"/><path d="M9 15H15"/></svg> Latin</button><button class="pill on" id="pillTerjemahT"><svg class="ico ico-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20"/><path d="M12 2a15 15 0 0 0 0 20"/><path d="M16 8l2 2-2 2"/><path d="M8 16l-2-2 2-2"/></svg> Terjemah</button><button class="pill" id="pillArabOnlyT"><svg class="ico ico-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 20c1.5-2 2.5-4 2.5-7V8"/><path d="M12 13c0 2 1.2 3.5 3 4"/><path d="M14 8v5"/><circle cx="16" cy="6" r="1.2" fill="currentColor" stroke="none"/></svg> Arab saja</button></div></div><div class="list" id="list-tahlil">'
if old_tahlil in c:
    c = c.replace(old_tahlil, new_tahlil)
    print("added tahlil pills + removed Awal btn")
else:
    print("tahlil panel not matched")

# 5) Hapus tombol Kembali ke awal di Yasin
old_yasin_btn = '<button class="btn-sm" data-jump="cover" style="margin-left:auto"><svg class="ico ico-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg> Kembali ke awal</button>'
if old_yasin_btn in c:
    c = c.replace(old_yasin_btn, '')
    print("removed Yasin Kembali")

old_doa = '<button class="btn-sm" data-jump="cover" style="margin-left:auto">Kembali</button>'
if old_doa in c:
    c = c.replace(old_doa, '')
    print("removed Doa Kembali")

# 6) Hapus kalimat tidak diperlukan
old_hint = '<div class="hint">Foto <code>assets/img/portrait.jpg</code> \u2014 ganti file di repo untuk update permanen.</div>'
if old_hint in c:
    c = c.replace(old_hint, '')
    print("removed hint foto")

old_cta_note = '<div class="cta-note">Halaman awal tampil pertama. Edit data di <code>index.html \u2192 let cover</code> & foto <code>assets/img/portrait.jpg</code>.</div>'
if old_cta_note in c:
    c = c.replace(old_cta_note, '')
    print("removed cta-note")

old_hero_data = '      <div class="hero-mini" style="margin-top:12px"><svg class="ico ico-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg> <div><b>Data real:</b> Lia Aris Tiarawati (19 Juli 1989 \u2013 22 September 2026) \u2022 <span class="js-name">Lia Aris Tiarawati</span>. <small style="color:var(--muted)">Foto assets/img/portrait.jpg \u2022 Yasin 83 ayat \u2022 Tahlil 24 bait.</small></div></div>\n'
if old_hero_data in c:
    c = c.replace(old_hero_data, '')
    print("removed hero-mini Data real")

old_info_foto = 'Foto <code>assets/img/portrait.jpg</code>. '
if old_info_foto in c:
    c = c.replace(old_info_foto, '')
    print("removed info foto mention")

old_source = '<div class="hero-mini" style="margin:12px 20px"><svg class="ico ico-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg> <div><b>Sumber data:</b> <code>assets/data/yasin.json</code> (Kemenag) & <code>tahlil.json</code> (quran.nu.or.id). Latin kosong pada Yasin (ditampilkan hanya jika ada).</div></div>'
new_source = '<div class="hero-mini" style="margin:12px 20px"><svg class="ico ico-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg> <div><b>Sumber data:</b> Kemenag & quran.nu.or.id \u2022 83 ayat \u2022 27 bait Tahlil</div></div>'
if old_source in c:
    c = c.replace(old_source, new_source)
    print("patched source hero minimal")

old_doa_small = " \u2022 Filter section mengandung 'Doa' (4 bait)"
new_doa_small = " \u2022 4 doa penutup"
if old_doa_small in c:
    c = c.replace(old_doa_small, new_doa_small)
    print("patched doa small")

# JS listeners for new Tahlil pills
old_listeners = "document.getElementById('pillArabOnly')?.addEventListener('click', ()=>{prefs.arabOnly=!prefs.arabOnly; if(prefs.arabOnly){prefs.showLatin=false;prefs.showTerjemah=false} refresh()});"
new_listeners = "document.getElementById('pillArabOnly')?.addEventListener('click', ()=>{prefs.arabOnly=!prefs.arabOnly; if(prefs.arabOnly){prefs.showLatin=false;prefs.showTerjemah=false} refresh()});\n// Tahlil pills sync same prefs\ndocument.getElementById('pillLatinT')?.addEventListener('click', ()=>{prefs.showLatin=!prefs.showLatin; if(prefs.showLatin)prefs.arabOnly=false; refresh()});\ndocument.getElementById('pillTerjemahT')?.addEventListener('click', ()=>{prefs.showTerjemah=!prefs.showTerjemah; if(prefs.showTerjemah)prefs.arabOnly=false; refresh()});\ndocument.getElementById('pillArabOnlyT')?.addEventListener('click', ()=>{prefs.arabOnly=!prefs.arabOnly; if(prefs.arabOnly){prefs.showLatin=false;prefs.showTerjemah=false} refresh()});"
if old_listeners in c:
    c = c.replace(old_listeners, new_listeners)
    print("added T pill listeners")

old_sync = "  document.getElementById('pillArabOnly')?.classList.toggle('on',prefs.arabOnly);"
new_sync = "  document.getElementById('pillArabOnly')?.classList.toggle('on',prefs.arabOnly);\n  document.getElementById('pillLatinT')?.classList.toggle('on',prefs.showLatin);\n  document.getElementById('pillTerjemahT')?.classList.toggle('on',prefs.showTerjemah);\n  document.getElementById('pillArabOnlyT')?.classList.toggle('on',prefs.arabOnly);"
if old_sync in c:
    c = c.replace(old_sync, new_sync)
    print("added T sync")

# Node check
m=re.search(r'<script>(.*?)</script>', c, re.S)
js=m.group(1)
tmp=pathlib.Path(os.environ["TEMP"])/"_batch.js"
tmp.write_text(js, encoding="utf-8")
r=subprocess.run(["node","--check",str(tmp)], capture_output=True, text=True)
print("node", r.returncode, r.stderr[:600] if r.stderr else "OK")
print(f"new len {len(c)} diff {len(c)-orig_len}")
p.write_text(c, encoding="utf-8")
print("written")
