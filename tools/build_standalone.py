import pathlib, json, base64, re, subprocess, os

src = pathlib.Path("C:/Users/mahad/yasin-tahlil/index.html")
jy_path = pathlib.Path("C:/Users/mahad/yasin-tahlil/assets/data/yasin.json")
jt_path = pathlib.Path("C:/Users/mahad/yasin-tahlil/assets/data/tahlil.json")
img_path = pathlib.Path("C:/Users/mahad/yasin-tahlil/assets/img/portrait.jpg")
dst = pathlib.Path("C:/Users/mahad/yasin-tahlil/yasin-tahlil-Lia-Aris-Tiarawati-standalone.html")

c = src.read_text(encoding="utf-8")
jy = json.loads(jy_path.read_text(encoding="utf-8"))
jt = json.loads(jt_path.read_text(encoding="utf-8"))
print(f"yasin {len(jy['ayat'])} latin {sum(1 for x in jy['ayat'] if x.get('latin','').strip())}")
print(f"tahlil {len(jt['bait'])}")

data_uri = ""
if img_path.exists():
    b64 = base64.b64encode(img_path.read_bytes()).decode()
    data_uri = f"data:image/jpeg;base64,{b64}"
    print(f"portrait {len(b64)} b64")

c = c.replace('photo:"assets/img/portrait.jpg"', f'photo:"{data_uri}"')
c = c.replace('if(!cover.photo) cover.photo="assets/img/portrait.jpg";', f'if(!cover.photo) cover.photo="{data_uri}";')
c = c.replace('<title>Yasin & Tahlil \u2014 Lia Aris Tiarawati</title>', '<title>Yasin & Tahlil \u2014 Lia Aris Tiarawati (Standalone)</title>')

jy_json = json.dumps(jy, ensure_ascii=False)
jt_json = json.dumps(jt, ensure_ascii=False)

old_init = src.read_text(encoding="utf-8")[src.read_text(encoding="utf-8").index("// init"):src.read_text(encoding="utf-8").index("init();")+7]
# simpler: replace fetch block pattern
# find fetch line
# Instead construct: replace the whole init function text by searching known snippet
needle = "const [ry, rt] = await Promise.all([fetch('assets/data/yasin.json')"
if needle in c:
    print("found fetch needle")
else:
    print("needle missing")
    raise SystemExit(1)

# Replace from "// init" to "init();" inclusive
start = c.index("// init")
end = c.index("init();", start) + len("init();")
old_block = c[start:end]
print(f"old_block len {len(old_block)}")

new_block = f"""// init \u2014 standalone: data inline (offline file://), no fetch required
const _JY = {jy_json};
const _JT = {jt_json};
function buildFromEmbedded(){{
  YASIN = (_JY.ayat||[]).map(x=>({{no:x.n, arab:x.ar, latin:x.latin||'', terjemah:x.id}}));
  TAHLIL = (_JT.bait||[]).flatMap(b=>{{
    const m=((b.latin||'')+' '+(b.section||'')).match(/\\(\\s*(\\d+)\\s*x\\s*\\)/i) || (b.ar||'').match(/[×x]\\s*(\\d+)/) || (b.ar||'').match(/([٠-٩]+)\\s*$/);
    let counter = null;
    if(m){{
      const raw=m[1];
      if(/[٠-٩]/.test(raw)) counter = parseInt(raw.replace(/[٠-٩]/g, d=> String(d.charCodeAt(0)-0x0660)),10);
      else counter = parseInt(raw,10);
    }}
    const base = {{judul:b.section, arab:b.ar, latin:b.latin, terjemah:b.id, counter}};
    if(!b.ar.includes('\u0627\u0644\u0652\u0641\u064e\u0627\u062a\u0650\u062d\u064e\u0629\u064f') || b.ar.includes('\u0627\u0644\u0652\u0641\u064e\u0627\u062a\u0650\u062d\u064e\u0629\u064f ......')) return [base];
    const parts = b.ar.split('\u0627\u0644\u0652\u0641\u064e\u0627\u062a\u0650\u062d\u064e\u0629\u064f');
    const out=[];
    for(let i=0;i<parts.length-1;i++){{
      const seg = parts[i].trim();
      const arab = (seg ? seg + ' ' : '') + '\u0627\u0644\u0652\u0641\u064e\u0627\u062a\u0650\u062d\u064e\u0629\u064f ......';
      out.push({{judul:b.section + (parts.length>3 ? ' '+(i+1) : ''), arab, latin:'', terjemah:'', counter}});
    }}
    const tail = parts[parts.length-1].trim();
    if(tail && tail.replace(/[.\u2026\s]/g,'')) out.push({{judul:b.section, arab:tail, latin:'', terjemah:'', counter}});
    return out.length ? out : [base];
  }});
  DOA = TAHLIL.filter(t=> t.judul.includes('Doa'));
}}
async function init(){{
  applyTheme(); applyCover();
  render();
  try{{
    if(location.protocol !== 'file:'){{
      try{{
        const [ry, rt] = await Promise.all([fetch('assets/data/yasin.json'), fetch('assets/data/tahlil.json')]);
        if(ry.ok && rt.ok){{
          const jy = await ry.json(); const jt = await rt.json();
          YASIN = (jy.ayat||[]).map(x=>({{no:x.n, arab:x.ar, latin:x.latin||'', terjemah:x.id}}));
          TAHLIL = (jt.bait||[]).flatMap(b=>{{
            const m=((b.latin||'')+' '+(b.section||'')).match(/\\(\\s*(\\d+)\\s*x\\s*\\)/i) || (b.ar||'').match(/[×x]\\s*(\\d+)/) || (b.ar||'').match(/([٠-٩]+)\\s*$/);
            let counter = null;
            if(m){{
              const raw=m[1];
              if(/[٠-٩]/.test(raw)) counter = parseInt(raw.replace(/[٠-٩]/g, d=> String(d.charCodeAt(0)-0x0660)),10);
              else counter = parseInt(raw,10);
            }}
            const base = {{judul:b.section, arab:b.ar, latin:b.latin, terjemah:b.id, counter}};
            if(!b.ar.includes('\u0627\u0644\u0652\u0641\u064e\u0627\u062a\u0650\u062d\u064e\u0629\u064f') || b.ar.includes('\u0627\u0644\u0652\u0641\u064e\u0627\u062a\u0650\u062d\u064e\u0629\u064f ......')) return [base];
            const parts = b.ar.split('\u0627\u0644\u0652\u0641\u064e\u0627\u062a\u0650\u062d\u064e\u0629\u064f'); const out=[];
            for(let i=0;i<parts.length-1;i++){{
              const seg = parts[i].trim(); const arab = (seg ? seg + ' ' : '') + '\u0627\u0644\u0652\u0641\u064e\u0627\u062a\u0650\u062d\u064e\u0629\u064f ......';
              out.push({{judul:b.section + (parts.length>3 ? ' '+(i+1) : ''), arab, latin:'', terjemah:'', counter}});
            }}
            if(tail && tail.replace(/[.\u2026\s]/g,'')) out.push({{judul:b.section, arab:tail, latin:'', terjemah:'', counter}});
            return out.length ? out : [base];
          }});
          DOA = TAHLIL.filter(t=> t.judul.includes('Doa'));
        }} else throw new Error('fetch not ok');
      }} catch(_e){{ buildFromEmbedded(); }}
    }} else {{ buildFromEmbedded(); }}
  }}catch(e){{
    try{{ buildFromEmbedded(); }}catch(_e2){{}}
  }}
  refresh();
  activate('cover');
}}
init();"""

c = c[:start] + new_block + c[end:]
print(f"replaced, new len {len(c)}")

m=re.search(r'<script>(.*?)</script>', c, re.S)
js=m.group(1)
tmp=pathlib.Path(os.environ["TEMP"])/"_standalone_check.js"
tmp.write_text(js, encoding="utf-8")
r=subprocess.run(["node","--check",str(tmp)], capture_output=True, text=True)
print("node", r.returncode, r.stderr[:800] if r.stderr else "OK")

dst.write_text(c, encoding="utf-8")
print(f"written {dst} {dst.stat().st_size} bytes")

dl = pathlib.Path("C:/Users/mahad/Downloads/yasin-tahlil-Lia-Aris-Tiarawati-standalone.html")
dl.write_text(c, encoding="utf-8")
print(f"copied to {dl} {dl.stat().st_size}")