# -*- coding: utf-8 -*-
"""Document each directory's common format inside its index.md (above the AUTO-INDEX block)."""
import os, io, re, sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Jeakyoung_Blog")
APPLY = "--apply" in sys.argv
START = "<!-- AUTO-INDEX:START"
F_START = "<!-- FORMAT:START (do not edit - regenerate with tools/build_format_docs.py) -->"
F_END = "<!-- FORMAT:END -->"

# 단계 이름은 tools/apply_body_format.py 의 SPEC 과 글자 하나까지 같아야 한다.
SPEC = {
    "01_Tasks": ("작업", "작업 (01_Tasks)",
                 [("status", "예정 / 진행중 / 완료 / 보류"),
                  ("priority", "낮음 / 보통 / 높음 / 매우높음"),
                  ("assignee", "담당자 목록")],
                 ["📋 개요", "🔍 현상 및 원인", "🔧 조치 내용", "✅ 검증 및 결과", "🔗 참고"]),
    "02_TechDocs": ("기술문서", "기술문서 (02_TechDocs)",
                    [("status", "예정 / 진행중 / 완료 / 보류"),
                     ("category", "분류 (예: 근태관리, 알림시스템)"),
                     ("assignee", "담당자 목록")],
                    ["📋 개요", "🎯 배경 및 요구사항", "🏗 설계 및 구현", "✅ 검증", "🔗 참고"]),
    "03_TechDocs": ("기술문서", "기술문서 (02_TechDocs)",
                    [("status", "예정 / 진행중 / 완료 / 보류"),
                     ("category", "분류"),
                     ("assignee", "담당자 목록")],
                    ["📋 개요", "🎯 배경 및 요구사항", "🏗 설계 및 구현", "✅ 검증", "🔗 참고"]),
    "03_Meetings": ("회의록", "회의록 (03_Meetings)",
                    [("status", "예정 / 진행중 / 완료 / 보류"),
                     ("attendees", "참석자 목록")],
                    ["📋 개요", "💬 논의 내용", "✅ 결정 사항", "🔜 후속 조치", "🔗 참고"]),
    "04_References": ("참고자료", "참고자료 (04_References)",
                      [("status", "예정 / 진행중 / 완료 / 보류"),
                       ("category", "분류 (예: SQL, 배포)")],
                      ["📋 개요", "⚙️ 환경 및 전제", "📖 상세 내용", "⚠️ 주의사항", "🔗 참고"]),
    # 아래 3종은 유형 전용 폴더가 아니라 frontmatter 의 type 으로 갈린다.
    # 템플릿은 따로 두지 않는다(기존 문서 정리용).
    "03_Learning": ("학습자료", "",
                    [("status", "예정 / 진행중 / 완료 / 보류"),
                     ("category", "분류 (예: Backend, DevOps)")],
                    ["📋 개요", "🧩 핵심 개념", "📖 상세 내용", "💡 정리 및 활용", "🔗 참고"]),
    "02_Career": ("경력문서", "",
                  [("status", "예정 / 진행중 / 완료 / 보류")],
                  ["📋 개요", "🧭 경력 요약", "🛠 주요 수행 내용", "🏆 성과 및 역량", "🔗 참고"]),
    "99_UNI": ("프로젝트문서", "",
               [("status", "예정 / 진행중 / 완료 / 보류")],
               ["📋 개요", "🎯 목표 및 범위", "🏗 진행 내용", "✅ 결과 및 회고", "🔗 참고"]),
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
    lines += ["### 속성", "", "| 속성 | 값 |", "|:--|:--|"]
    lines += ["| `%s` | %s |" % (k, v) for k, v in rows]
    lines += ["", "### 본문 구성 (H2 고정)", "", "| 단계 | 제목 |", "|:--:|:--|"]
    lines += ["| %d | %s |" % (i, s) for i, s in enumerate(sections, 1)]
    lines += ["", F_END]
    block = "\n".join(lines)

    txt = io.open(idx, encoding="utf-8").read()
    # strip any previously generated block (tolerant of older marker wording),
    # then insert exactly one fresh block above the AUTO-INDEX section
    stripped = re.sub(r"<!-- FORMAT:START.*?<!-- FORMAT:END -->\s*", "", txt, flags=re.S)
    pos = stripped.find(START)
    if pos < 0:
        # 손으로 꾸민 index (AUTO-INDEX 블록이 없는 페이지) 는 맨 끝에 붙인다
        new = stripped.rstrip("\n") + "\n\n" + block + "\n"
    else:
        new = stripped[:pos] + block + "\n\n" + stripped[pos:]
    if new != txt:
        done.append(os.path.relpath(idx, ROOT).replace(os.sep, "/"))
        if APPLY:
            io.open(idx, "w", encoding="utf-8", newline="\n").write(new)

print("문서 양식 삽입: %d (apply=%s)" % (len(done), APPLY))
for d in done:
    print("   ", d)
