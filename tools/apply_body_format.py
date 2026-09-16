# -*- coding: utf-8 -*-
"""Reshape every note body to the shared 5-step document format.

See `_templates/_문서 양식 명세.md`. Existing content is never deleted: its
headings are demoted so they nest under the step that owns legacy content.

Idempotent. Also migrates notes written against an earlier revision of the
spec (plain `## 1. 개요` headings) to the current one instead of re-wrapping.
"""
import os, io, re, sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Jeakyoung_Blog")
APPLY = "--apply" in sys.argv

DASH = "—"  # em dash, used for "not filled in yet"

SPEC = {
    "작업": {
        "steps": ["📋 개요", "🔍 현상 및 원인", "🔧 조치 내용", "✅ 검증 및 결과", "🔗 참고"],
        "plain": ["개요", "현상 및 원인", "조치 내용", "검증 및 결과", "참고"],
        "landing": 3,
        "meta": [("요청자", ""), ("요청일", "@date"),
                 ("대상 시스템", ""), ("관련 화면·프로그램", "")],
    },
    "기술문서": {
        "steps": ["📋 개요", "🎯 배경 및 요구사항", "🏗 설계 및 구현", "✅ 검증", "🔗 참고"],
        "plain": ["개요", "배경 및 요구사항", "설계 및 구현", "검증", "참고"],
        "landing": 3,
        "meta": [("대상 시스템", ""), ("적용 범위", "@category"), ("관련 모듈", "")],
    },
    "회의록": {
        "steps": ["📋 개요", "💬 논의 내용", "✅ 결정 사항", "🔜 후속 조치", "🔗 참고"],
        "plain": ["개요", "논의 내용", "결정 사항", "후속 조치", "참고"],
        "landing": 2,
        "meta": [("일시", "@date"), ("장소", ""), ("참석자", "@attendees"), ("안건", "")],
    },
    "참고자료": {
        "steps": ["📋 개요", "⚙️ 환경 및 전제", "📖 상세 내용", "⚠️ 주의사항", "🔗 참고"],
        "plain": ["개요", "환경 및 전제", "상세 내용", "주의사항", "참고"],
        "landing": 3,
        "meta": [("용도", ""), ("대상 시스템", ""), ("최종 확인일", "@date")],
    },
}

DIRT = {"01_Tasks": "작업", "02_TechDocs": "기술문서", "03_TechDocs": "기술문서",
        "03_Meetings": "회의록", "04_References": "참고자료"}

FENCE = re.compile(r"^(\s*)(```|~~~)")
HEADING = re.compile(r"^(#{1,6})(\s+)(.*)$")


def split_fm(text):
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", text, re.S)
    if m:
        return text[:m.end()], m.group(1), text[m.end():]
    return "", "", text


def fm_get(fm, key):
    m = re.search(r"^%s:[ \t]*(.*)$" % re.escape(key), fm, re.M)
    if not m:
        return ""
    v = m.group(1).strip()
    if v in ("[]", ""):
        blk = re.findall(r"^%s:[ \t]*\n((?:[ \t]+-[ \t]*.*\n?)+)" % re.escape(key), fm, re.M)
        if blk:
            return ", ".join(x.strip().lstrip("-").strip() for x in blk[0].splitlines() if x.strip())
        return ""
    if v.startswith("[") and v.endswith("]"):
        return v[1:-1].strip()
    return v.strip('"').strip("'")


def code_mask(lines):
    mask, fence = [], None
    for ln in lines:
        m = FENCE.match(ln)
        if fence is None and m:
            fence = m.group(2)
            mask.append(True)
            continue
        if fence is not None:
            mask.append(True)
            if ln.strip().startswith(fence):
                fence = None
            continue
        mask.append(False)
    return mask


def strip_leading_h1(body):
    lines = body.split("\n")
    for i, ln in enumerate(lines):
        if not ln.strip():
            continue
        if re.match(r"^#\s+\S", ln):
            return "\n".join(lines[i + 1:]).lstrip("\n")
        return body
    return body


def shift_headings(body):
    lines = body.split("\n")
    mask = code_mask(lines)
    levels = [len(HEADING.match(l).group(1))
              for l, inc in zip(lines, mask) if not inc and HEADING.match(l)]
    if not levels:
        return body
    shift = 3 - min(levels)
    if shift <= 0:
        return body
    out = []
    for l, inc in zip(lines, mask):
        m = HEADING.match(l)
        if inc or not m:
            out.append(l)
            continue
        out.append("#" * min(6, len(m.group(1)) + shift) + m.group(2) + m.group(3))
    return "\n".join(out)


def migrate_headings(body, spec):
    """Rewrite step headings written against older spec revisions."""
    for i, (plain, new) in enumerate(zip(spec["plain"], spec["steps"]), start=1):
        body = re.sub(r"^##[ \t]+%d\.[ \t]+%s[ \t]*$" % (i, re.escape(plain)),
                      "## " + new, body, flags=re.M)
        body = re.sub(r"^##[ \t]+%s[ \t]*$" % re.escape(plain),
                      "## " + new, body, flags=re.M)
    return body


def is_formatted(body, spec):
    return all(re.search(r"^##[ \t]+%s[ \t]*$" % re.escape(s), body, re.M)
               for s in spec["steps"])


def meta_table(spec, fm, existing=None):
    rows = []
    for label, src in spec["meta"]:
        val = fm_get(fm, src[1:]) if src.startswith("@") else ""
        if existing and existing.get(label):
            val = existing[label]
        rows.append("| **%s** | %s |" % (label, val if val else DASH))
    return "\n".join(["| 항목 | 내용 |", "|:--|:--|"] + rows)


def read_meta(body, spec):
    """Pull already-filled values out of the 개요 table so a rewrite keeps them."""
    m = re.search(r"^##[ \t]+%s[ \t]*$" % re.escape(spec["steps"][0]), body, re.M)
    if not m:
        return {}
    chunk = body[m.end():]
    nxt = re.search(r"^##[ \t]", chunk, re.M)
    if nxt:
        chunk = chunk[:nxt.start()]
    out = {}
    for row in re.findall(r"^\|(.+?)\|(.*?)\|[ \t]*$", chunk, re.M):
        label = row[0].strip().strip("*").strip()
        val = row[1].strip()
        if label in ("항목", "") or set(label) <= set("-: "):
            continue
        if val and val != DASH:
            out[label] = val
    return out


def rebuild_meta(body, spec, fm):
    """Replace the 개요 table in an already-formatted note with the current style."""
    existing = read_meta(body, spec)
    m = re.search(r"^##[ \t]+%s[ \t]*$" % re.escape(spec["steps"][0]), body, re.M)
    if not m:
        return body
    start = m.end()
    chunk = body[start:]
    nxt = re.search(r"^##[ \t]", chunk, re.M)
    end = start + (nxt.start() if nxt else len(chunk))
    section = body[start:end]
    tbl = re.search(r"^\|.*\|[ \t]*\n\|[-: |]+\|[ \t]*\n(?:\|.*\|[ \t]*\n?)*", section, re.M)
    new_tbl = meta_table(spec, fm, existing)
    if tbl:
        section = section[:tbl.start()] + new_tbl + "\n" + section[tbl.end():]
    else:
        section = "\n" + new_tbl + "\n" + section.lstrip("\n")
    return body[:start] + section + body[end:]


def build(title, spec, fm, legacy):
    parts = ["# %s" % title, ""]
    for i, name in enumerate(spec["steps"], start=1):
        parts += ["## %s" % name, ""]
        if i == 1:
            parts += [meta_table(spec, fm), ""]
        if i == spec["landing"] and legacy.strip():
            parts += [legacy.strip(), ""]
    return "\n".join(parts).rstrip() + "\n"


changed, migrated = [], 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in (".obsidian", "resources")]
    parts = os.path.relpath(dirpath, ROOT).replace(os.sep, "/").split("/")
    dtype = next((DIRT[p] for p in parts if p in DIRT), None)
    if not dtype:
        continue
    spec = SPEC[dtype]
    for fn in sorted(filenames):
        if not fn.endswith(".md") or fn in ("index.md", "README.md"):
            continue
        full = os.path.join(dirpath, fn)
        raw = io.open(full, encoding="utf-8").read()
        fmblock, fm, body = split_fm(raw)
        title = fm_get(fm, "title") or fn[:-3]

        body2 = migrate_headings(body, spec)
        if is_formatted(body2, spec):
            new_body = rebuild_meta(body2, spec, fm).strip() + "\n"
            migrated += 1
        else:
            legacy = shift_headings(strip_leading_h1(body.strip()).strip())
            new_body = build(title, spec, fm, legacy)

        new = fmblock.rstrip("\n") + "\n\n" + new_body
        if new != raw:
            changed.append(os.path.relpath(full, ROOT).replace(os.sep, "/"))
            if APPLY:
                io.open(full, "w", encoding="utf-8", newline="\n").write(new)

print("본문 양식 적용: %d건 변경 (기존 양식 인식 %d건, apply=%s)" % (len(changed), migrated, APPLY))
if "--show" in sys.argv:
    for c in changed:
        print("   ", c)
