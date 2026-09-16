# -*- coding: utf-8 -*-
"""Document each directory's common format inside its index.md (above the AUTO-INDEX block)."""
import os, io, re, sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Jeakyoung_Blog")
APPLY = "--apply" in sys.argv
START = "<!-- AUTO-INDEX:START"
F_START = "<!-- FORMAT:START (do not edit - regenerate with tools/build_format_docs.py) -->"
F_END = "<!-- FORMAT:END -->"

SPEC = {
    "01_Tasks": ("작업", "작업 (01_Tasks)",
                 [("status", "예정 / 진행중 / 완료 / 보류"),
                  ("priority", "낮음 / 보통 / 높음 / 매우높음"),
                  ("assignee", "담당자 목록")],
                 ["1. 개요", "2. 현상 및 원인", "3. 조치 내용", "4. 검증 및 결과", "5. 참고"]),
    "02_TechDocs": ("기술문서", "기술문서 (02_TechDocs)",
                    [("status", "예정 / 진행중 / 완료 / 보류"),
                     ("category", "분류 (예: 근태관리, 알림시스템)"),
                     ("assignee", "담당자 목록")],
                    ["1. 개요", "2. 배경 및 요구사항", "3. 설계 및 구현", "4. 검증", "5. 참고"]),
    "03_TechDocs": ("기술문서", "기술문서 (02_TechDocs)",
                    [("status", "예정 / 진행중 / 완료 / 보류"),
                     ("category", "분류"),
                     ("assignee", "담당자 목록")],
                    ["1. 개요", "2. 배경 및 요구사항", "3. 설계 및 구현", "4. 검증", "5. 참고"]),
    "03_Meetings": ("회의록", "회의록 (03_Meetings)",
                    [("status", "예정 / 진행중 / 완료 / 보류"),
                     ("attendees", "참석자 목록")],
                    ["1. 개요", "2. 논의 내용", "3. 결정 사항", "4. 후속 조치", "5. 참고"]),
    "04_References": ("참고자료", "참고자료 (04_References)",
                      [("status", "예정 / 진행중 / 완료 / 보류"),
                       ("category", "분류 (예: SQL, 배포)")],
                      ["1. 개요", "2. 환경 및 전제", "3. 상세 내용", "4. 주의사항", "5. 참고"]),
}

done = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    folder = os.path.basename(dirpath)
    if folder not in SPEC:
        continue
    idx = os.path.join(dirpath, "index.md")
    if not os.path.exists(idx):
        continue
    dtype, tmpl, extra, sections = SPEC[folder]

    rows = [("title", "문서 제목 (파일명과 동일)"),
            ("date", "문서 기준일 (YYYY-MM-DD)"),
            ("type", "`%s` 고정" % dtype),
            ("project", "소속 프로젝트")] + extra + [("tags", "태그 목록")]

    lines = [F_START, "", "## 문서 양식", ""]
    if tmpl:
        lines.append("새 문서는 템플릿 `_templates/%s.md` 로 만듭니다." % tmpl)
        lines.append("")
    lines += ["### 속성", "", "| 속성 | 값 |", "|------|-----|"]
    lines += ["| `%s` | %s |" % (k, v) for k, v in rows]
    lines += ["", "### 본문 구성 (H2 고정)", ""]
    lines += ["%d. **%s**" % (i, s.split(". ", 1)[1]) for i, s in enumerate(sections, 1)]
    lines += ["", F_END]
    block = "\n".join(lines)

    txt = io.open(idx, encoding="utf-8").read()
    # strip any previously generated block (tolerant of older marker wording),
    # then insert exactly one fresh block above the AUTO-INDEX section
    stripped = re.sub(r"<!-- FORMAT:START.*?<!-- FORMAT:END -->\s*", "", txt, flags=re.S)
    pos = stripped.find(START)
    if pos < 0:
        continue
    new = stripped[:pos] + block + "\n\n" + stripped[pos:]
    if new != txt:
        done.append(os.path.relpath(idx, ROOT).replace(os.sep, "/"))
        if APPLY:
            io.open(idx, "w", encoding="utf-8", newline="\n").write(new)

print("문서 양식 삽입: %d (apply=%s)" % (len(done), APPLY))
for d in done:
    print("   ", d)
