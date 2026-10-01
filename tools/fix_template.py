import pathlib, re, subprocess, os

# Fix corrupted tail-guard lines in build_standalone.py template
p = pathlib.Path("C:/Users/mahad/yasin-tahlil/tools/build_standalone.py")
lines = p.read_text(encoding="utf-8").splitlines()
fixed = 0
for i, l in enumerate(lines):
    s = l.strip()
    if "tail.replace" in s or (s.startswith("if(tail") and "out.push" in s):
        indent = l[: len(l) - len(l.lstrip())]
        body = "if(tail && tail.replace(/[." + chr(92) + "u2026" + chr(92) + "s]/g,'')) out.push({{judul:b.section, arab:tail, latin:'', terjemah:'', counter}});"
        if "const tail" in s and s.strip().startswith("const tail"):
            lines[i] = indent + "const tail = parts[parts.length-1].trim(); " + body
        else:
            lines[i] = indent + body
        fixed += 1
        print("fixed line", i + 1, repr(lines[i][:100]))
print("fixed", fixed)
assert "\\\\&" not in p.read_text(encoding="utf-8") or True
p.write_text("\n".join(lines), encoding="utf-8")
# verify no corrupted \&\& left
t = p.read_text(encoding="utf-8")
print("has corrupted &&:", "\\&\\&" in t)
print("tail guard count:", t.count("tail.replace"))
