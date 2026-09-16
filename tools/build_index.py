# -*- coding: utf-8 -*-
"""Generate folder index.md pages so the Quartz blog navigation mirrors the Obsidian vault tree."""
import os, io, re, sys, datetime

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Jeakyoung_Blog")
DRY = "--apply" not in sys.argv

START = "<!-- AUTO-INDEX:START (do not edit below - regenerate with tools/build_index.py) -->"
END = "<!-- AUTO-INDEX:END -->"

FOLDER_NAMES = {
    "01_Tasks": "\uc791\uc5c5 \ubaa9\ub85d",
    "02_Docs": "\ud504\ub85c\uc81d\ud2b8 \ubb38\uc11c",
    "02_TechDocs": "\uae30\uc220 \ubb38\uc11c",
    "03_TechDocs": "\uae30\uc220 \ubb38\uc11c",
    "03_Meetings": "\ud68c\uc758\ub85d",
    "04_References": "\ucc38\uace0 \uc790\ub8cc",
    "01_Projects": "\ud504\ub85c\uc81d\ud2b8",
    "02_Career": "\uacbd\ub825 \ubb38\uc11c",
    "03_Learning": "\ud559\uc2b5 \uc790\ub8cc",
    "99_UNI": "\ub300\ud559 \ud504\ub85c\uc81d\ud2b8",
    "2023_OpenSoop": "2023 Open Soop",
    "2024_PaekTaekApp": "2024 \ud3c9\ud0dd\ub300\ud559\uad50\uc571 \ub9ac\uc6cc\ud06c",
    "Backend": "\ubc31\uc5d4\ub4dc \uac1c\ubc1c",
    "DevOps": "DevOps & \ubc30\ud3ec",
    "Tools": "\uac1c\ubc1c \ub3c4\uad6c",
    "References": "\ucc38\uace0 \uc790\ub8cc",
    "Database": "\ub370\uc774\ud130\ubca0\uc774\uc2a4",
}

# folders whose index.md is hand-curated: only the AUTO-INDEX block is refreshed
CURATED = set()


def has_md(path):
    for d, ds, fs in os.walk(path):
        ds[:] = [x for x in ds if x != ".obsidian"]
        if any(f.endswith(".md") and f != "index.md" for f in fs):
            return True
    return False


def read_title(index_path):
    if not os.path.exists(index_path):
        return None
    txt = io.open(index_path, encoding="utf-8").read()
    m = re.search(r"^title:\s*(.+)$", txt, re.M)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None


def display(folder, full):
    t = read_title(os.path.join(full, "index.md"))
    if t:
        return t
    return FOLDER_NAMES.get(folder, folder)


def page_title(rel, folder, full):
    t = read_title(os.path.join(full, "index.md"))
    if t:
        return t
    base = FOLDER_NAMES.get(folder, folder)
    if folder in FOLDER_NAMES and re.match(r"^0\d_", folder):
        parent = os.path.dirname(full)
        ptitle = read_title(os.path.join(parent, "index.md"))
        if ptitle and os.path.basename(parent) not in ("Jeakyoung_Blog",):
            return "%s - %s" % (ptitle, base)
    return base


def sortkey(name):
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r"(\d+)", name)]


def doc_link(filename):
    """Wikilinks cannot carry '[', ']', '#' or '|' in Quartz's Obsidian-flavored markdown
    parser, so fall back to a plain markdown link with an angle-bracket destination
    (understood by both Obsidian and Quartz)."""
    stem = filename[:-3]
    if not re.search(r"[\[\]#|]", stem):
        return "- [[%s]]" % stem
    text = re.sub(r"([\[\]])", r"\\\1", stem)
    return "- [%s](<%s>)" % (text, filename)


created, updated = [], []

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = sorted([d for d in dirnames if d not in (".obsidian", ".git")], key=sortkey)
    rel = os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
    rel = "" if rel == "." else rel

    subs = [d for d in dirnames if has_md(os.path.join(dirpath, d))]
    docs = sorted([f for f in filenames if f.endswith(".md") and f != "index.md"], key=sortkey)
    if not subs and not docs:
        continue

    lines = [START, ""]
    if subs:
        lines.append("## \ud558\uc704 \ubd84\ub958")
        lines.append("")
        for d in subs:
            full = os.path.join(dirpath, d)
            p = (rel + "/" + d) if rel else d
            lines.append("- [[%s|%s]]" % (p, display(d, full)))
        lines.append("")
    if docs:
        lines.append("## \ubb38\uc11c \ubaa9\ub85d (%d)" % len(docs))
        lines.append("")
        for f in docs:
            lines.append(doc_link(f))
        lines.append("")
    lines.append(END)
    block = "\n".join(lines)

    idx = os.path.join(dirpath, "index.md")
    if os.path.exists(idx):
        txt = io.open(idx, encoding="utf-8").read()
        if START in txt and END in txt:
            new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, txt, flags=re.S)
        else:
            # hand-curated index page without markers: leave it alone
            continue
        if new != txt:
            updated.append(rel or "(root)")
            if not DRY:
                io.open(idx, "w", encoding="utf-8", newline="\n").write(new)
    else:
        folder = os.path.basename(dirpath)
        title = page_title(rel, folder, dirpath)
        today = datetime.date.today().isoformat()
        new = "---\ntitle: %s\ndate: %s\n---\n\n# %s\n\n%s\n" % (title, today, title, block)
        created.append((rel, title))
        if not DRY:
            io.open(idx, "w", encoding="utf-8", newline="\n").write(new)

print("created: %d, updated: %d (dry-run=%s)" % (len(created), len(updated), DRY))
for rel, title in created:
    print("  + %-70s %s" % (rel, title))
for rel in updated:
    print("  ~ %s" % rel)
