# -*- coding: utf-8 -*-
"""Normalize Obsidian note frontmatter so the Quartz blog listing matches the vault."""
import os, io, re, sys, subprocess, datetime

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Jeakyoung_Blog")
REPO = os.path.dirname(ROOT)
DRY = "--apply" not in sys.argv

BS = chr(92)
QT = chr(34)

K_CREATED = ("created", "\uc0dd\uc131 \uc77c\uc2dc", "\uc0dd\uc131\uc77c\uc2dc", "\uc0dd\uc131\uc77c")

RE_FULL = re.compile(r"(?<!\d)(20\d{2})[-._](\d{1,2})[-._](\d{1,2})(?!\d)")
RE_YY = re.compile(r"(?<!\d)(\d{2})[-._](\d{1,2})[-._](\d{1,2})(?!\d)")
RE_MD = re.compile(r"(?<!\d)(\d{1,2})[-.](\d{1,2})(?!\d)")
RE_PATHYEAR = re.compile(r"(?<!\d)(20[0-3]\d)(?!\d)")

_gitcache = {}


def git_first_date(relpath):
    if relpath in _gitcache:
        return _gitcache[relpath]
    val = None
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%aI", "--", relpath],
            cwd=REPO, capture_output=True, text=True, encoding="utf-8")
        lines = [l for l in out.stdout.strip().splitlines() if l.strip()]
        if lines:
            val = lines[-1][:10]
    except Exception:
        pass
    _gitcache[relpath] = val
    return val


def valid(y, m, d):
    try:
        return datetime.date(y, m, d)
    except ValueError:
        return None


def date_from_name(stem, base, path_year):
    """base = datetime.date fallback context, path_year = year hint from folder names"""
    m = RE_FULL.search(stem)
    if m:
        dt = valid(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if dt:
            return dt
    m = RE_YY.search(stem)
    if m:
        yy = int(m.group(1))
        if 20 <= yy <= 35:
            dt = valid(2000 + yy, int(m.group(2)), int(m.group(3)))
            if dt:
                return dt
    m = RE_MD.search(stem)
    if m:
        mo, dy = int(m.group(1)), int(m.group(2))
        if path_year:
            return valid(path_year, mo, dy)
        if base:
            dt = valid(base.year, mo, dy)
            if dt and (dt - base).days > 45:
                dt = valid(base.year - 1, mo, dy)
            return dt
    return None


def split_fm(text):
    if not text.startswith("---"):
        return [], text, False
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", text, re.S)
    if m:
        return m.group(1).splitlines(), text[m.end():], True
    m2 = re.match(r"^---[ \t]*\r?\n---[ \t]*\r?\n?", text)
    if m2:
        return [], text[m2.end():], True
    return [], text, False


def yaml_escape(v):
    if re.search(r"[:#\[\]{}&*!|>%@`" + QT + r"']", v) or v.strip() != v:
        return QT + v.replace(BS, BS + BS).replace(QT, BS + QT) + QT
    return v


def parse_date_value(v):
    v = v.strip().strip(QT).strip("'")
    m = re.match(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", v)
    if m:
        return valid(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


changed = []
report = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in (".obsidian", ".git")]
    for fn in sorted(filenames):
        if not fn.endswith(".md"):
            continue
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, REPO).replace(os.sep, "/")
        raw = io.open(full, encoding="utf-8").read()
        fm, body, had = split_fm(raw)

        keys = {}
        for line in fm:
            mm = re.match(r"^([^\s:#][^:]*):(.*)$", line)
            if mm:
                keys.setdefault(mm.group(1).strip(), mm.group(2).strip())

        add = []
        stem = fn[:-3]
        if "title" not in keys:
            add.append("title: " + yaml_escape(stem))

        src = None
        if "date" not in keys:
            base = None
            for k in K_CREATED:
                if keys.get(k):
                    base = parse_date_value(keys[k])
                    if base:
                        break
            if not base:
                g = git_first_date(rel)
                if g:
                    base = parse_date_value(g)
            if not base:
                base = datetime.date.fromtimestamp(os.path.getmtime(full))

            relin = os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
            py = RE_PATHYEAR.search(relin)
            path_year = int(py.group(1)) if py else None

            dt = None
            if stem != "index":
                dt = date_from_name(stem, base, path_year)
                src = "filename" if dt else None
            if not dt:
                dt = base
                src = src or "metadata/git"
            add.append("date: " + dt.isoformat())

        if not add:
            continue

        new_fm = add + [l for l in fm if l.strip() != ""]
        new = "---\n" + "\n".join(new_fm) + "\n---\n\n" + body.lstrip("\n")
        changed.append(rel)
        report.append((rel, add, src))
        if not DRY:
            io.open(full, "w", encoding="utf-8", newline="\n").write(new)

print("files changed: %d (dry-run=%s)" % (len(changed), DRY))
if "--show" in sys.argv:
    for rel, add, src in report:
        print("  %-95s %s  [%s]" % (rel[7:], add, src))
