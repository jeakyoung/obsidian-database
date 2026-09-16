# -*- coding: utf-8 -*-
"""Apply the per-directory common frontmatter schema (공통양식) to every note.

Directory type -> schema:
    01_Tasks        작업      : status, priority, assignee
    02_Docs         프로젝트문서 : status
    02/03_TechDocs  기술문서   : status, category, assignee
    03_Meetings     회의록    : status, attendees
    04_References   참고자료   : status, category

Body content is never touched. Run with --apply to write.
"""
import os, io, re, sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Jeakyoung_Blog")
DRY = "--apply" not in sys.argv

QT = chr(34)

DIR_TYPE = {
    "01_Tasks": "작업",
    "02_Docs": "프로젝트문서",
    "02_TechDocs": "기술문서",
    "03_TechDocs": "기술문서",
    "03_Meetings": "회의록",
    "04_References": "참고자료",
}

PROJECT = {
    "01_ShinJinSM": "신진SM",
    "02_IPACK": "IPACK",
    "03_iFrog": "I-Frog",
    "04_DongBang": "동방푸드",
    "05_SeHanMT": "세한MT",
    "06_ReelTrip": "ReelTrip",
    "07_DataBoucher": "데이터바우처",
    "08_NPP": "뉴파워프라즈마",
    "99_UNI": "대학프로젝트",
}

# NOTE: every *output* value must also be a key here, otherwise re-running the
# script would not recognise the status it wrote itself and would reset it.
STATUS = {
    "예정": "예정",
    "진행중": "진행중",
    "완료": "완료",
    "보류": "보류",
    "완료 \U0001f64c": "완료",
    "진행 중": "진행중",
    "작성중": "진행중",
    "시작 전": "예정",
    "할 일": "예정",
    "✅ 조회 가능": "완료",
}

PRIORITY = {"낮음": "낮음", "보통": "보통",
            "높음": "높음", "매우높음": "매우높음"}

CREATED_KEYS = ("created", "생성 일시", "생성일시", "생성일")
TAG_KEYS = ("tags", "태그")
OWNER_KEYS = ("assignee", "담당자")
CAT_KEYS = ("category", "카테고리")
PRIO_KEYS = ("priority", "우선순위")
STATUS_KEYS = ("status", "상태")
DROP = {"base"} | set(CREATED_KEYS[1:]) | set(TAG_KEYS[1:]) | set(OWNER_KEYS[1:]) \
       | set(CAT_KEYS[1:]) | set(PRIO_KEYS[1:]) | set(STATUS_KEYS[1:])

RE_KV = re.compile(r"^([^\s:#][^:]*):[ \t]?(.*)$")
RE_ITEM = re.compile(r"^[ \t]+-[ \t]*(.*)$")


def parse_fm(lines):
    data, order, i = {}, [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = RE_KV.match(line)
        if not m:
            i += 1
            continue
        k, v = m.group(1).strip(), m.group(2).strip()
        if v == "":
            items, j = [], i + 1
            while j < len(lines) and RE_ITEM.match(lines[j]):
                items.append(unquote(RE_ITEM.match(lines[j]).group(1).strip()))
                j += 1
            data[k] = items if items else ""
            i = j if items else i + 1
        else:
            if v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                data[k] = [unquote(x.strip()) for x in inner.split(",")] if inner else []
            else:
                data[k] = unquote(v)
            i += 1
        if k not in order:
            order.append(k)
    return data, order


def unquote(v):
    if len(v) >= 2 and ((v[0] == QT and v[-1] == QT) or (v[0] == "'" and v[-1] == "'")):
        return v[1:-1]
    return v


def quote(v):
    v = str(v)
    if v == "":
        return QT + QT
    if re.search(r"^[\s\-?:,\[\]{}#&*!|>'" + QT + r"%@`]", v) or ": " in v or v.endswith(":") \
            or v.strip() != v or "#" in v:
        return QT + v.replace("\\", "\\\\").replace(QT, "\\" + QT) + QT
    return v


def emit(k, v):
    if isinstance(v, list):
        if not v:
            return ["%s: []" % k]
        return ["%s:" % k] + ["  - %s" % quote(x) for x in v]
    return ["%s: %s" % (k, quote(v))]


def first(data, keys):
    for k in keys:
        if k in data and data[k] not in ("", [], None):
            return data[k]
    return None


def aslist(v):
    if v is None:
        return []
    if isinstance(v, list):
        return [x for x in v if x not in ("", None)]
    return [v] if v else []


def split_fm(text):
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", text, re.S)
    if m:
        return m.group(1).splitlines(), text[m.end():]
    m2 = re.match(r"^---[ \t]*\r?\n---[ \t]*\r?\n?", text)
    if m2:
        return [], text[m2.end():]
    return None, text


changed, stats = [], {}
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in (".obsidian", ".git", "resources")]
    rel = os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
    parts = [] if rel == "." else rel.split("/")

    dtype = next((DIR_TYPE[p] for p in parts if p in DIR_TYPE), None)
    proj = next((PROJECT[p] for p in parts if p in PROJECT), None)
    if dtype is None:
        if parts and parts[0] == "02_Career":
            dtype = "경력문서"
        elif parts and parts[0] == "03_Learning":
            dtype = "학습자료"
        elif proj:
            dtype = "프로젝트문서"

    for fn in sorted(filenames):
        if not fn.endswith(".md") or fn == "index.md" or fn == "README.md":
            continue
        if dtype is None:
            continue
        full = os.path.join(dirpath, fn)
        raw = io.open(full, encoding="utf-8").read()
        fmlines, body = split_fm(raw)
        if fmlines is None:
            continue
        data, order = parse_fm(fmlines)

        out = []
        out += emit("title", data.get("title", fn[:-3]))
        out += emit("date", data.get("date", ""))
        out += emit("type", dtype)
        if proj:
            out += emit("project", proj)

        raw_status = first(data, STATUS_KEYS)
        status = STATUS.get(str(raw_status).strip(), None) if raw_status else None
        if status is None:
            status = "완료" if dtype in ("회의록", "참고자료") else "진행중"
        out += emit("status", status)

        if dtype == "작업":
            p = first(data, PRIO_KEYS)
            out += emit("priority", PRIORITY.get(str(p).strip(), "보통") if p else "보통")
            out += emit("assignee", aslist(first(data, OWNER_KEYS)))
        elif dtype == "기술문서":
            cat = first(data, CAT_KEYS)
            if not cat and data.get("type") and data.get("type") != dtype:
                cat = data["type"]
            out += emit("category", cat or "")
            out += emit("assignee", aslist(first(data, OWNER_KEYS)))
        elif dtype == "회의록":
            out += emit("attendees", aslist(first(data, OWNER_KEYS)))
        elif dtype == "참고자료":
            cat = first(data, CAT_KEYS)
            if not cat and data.get("type") and data.get("type") != dtype:
                cat = data["type"]
            out += emit("category", cat or "")

        out += emit("tags", aslist(first(data, TAG_KEYS)))

        created = first(data, CREATED_KEYS)
        if created:
            out += emit("created", created)

        known = {"title", "date", "type", "project", "status", "priority",
                 "assignee", "attendees", "category", "tags", "created"} | DROP
        for k in order:
            if k not in known:
                out += emit(k, data[k])

        new = "---\n" + "\n".join(out) + "\n---\n\n" + body.lstrip("\n")
        if new != raw:
            changed.append(os.path.relpath(full, ROOT).replace(os.sep, "/"))
            stats[dtype] = stats.get(dtype, 0) + 1
            if not DRY:
                io.open(full, "w", encoding="utf-8", newline="\n").write(new)

print("files changed: %d (dry-run=%s)" % (len(changed), DRY))
for k, v in sorted(stats.items()):
    print("   %-10s %d" % (k, v))
if "--show" in sys.argv:
    for c in changed:
        print("   ", c)
