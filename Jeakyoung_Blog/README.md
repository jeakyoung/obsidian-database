---
title: 블로그 문서 저장소 - 구조 가이드
type: 안내
date: 2026-09-16
---

# 📚 블로그 문서 저장소 구조 가이드

> 이 폴더(`Jeakyoung_Blog/`)가 **Quartz 블로그의 content 루트**입니다.
> 여기에 있는 문서가 곧 [Jeakyoung's Notes](https://jeakyoung.github.io/obsidian-database) 에 그대로 게시됩니다.

---

## 🗂️ 전체 구조

```
Jeakyoung_Blog/                     📁 블로그 content 루트
├── index.md                        🏠 블로그 홈
├── README.md                       📄 이 파일
│
├── 01_Projects/                    📁 프로젝트 문서
│   ├── index.md
│   ├── 01_IPACK/                   📂 IPACK 근태 시스템
│   │   ├── 01_Tasks/ 02_TechDocs/ 03_Meetings/
│   ├── 02_iFrog/                   📂 I-Frog
│   │   ├── 01_Tasks/ 02_TechDocs/ 03_Meetings/ 04_References/
│   ├── 03_ShinJinSM/                📂 신진SM ERP/MES
│   │   ├── 01_Tasks/               작업 목록
│   │   ├── 02_TechDocs/            기술 문서
│   │   ├── 03_Meetings/            회의록
│   │   └── 04_References/          참고 자료
│   ├── 04_DataBoucher/             📂 데이터 바우처
│   │   ├── 01_Tasks/ 02_TechDocs/ 03_Meetings/ 04_References/ 05_Docs/
│   ├── 05_ReelTrip/                📂 ReelTrip (개인)
│   │   ├── 01_Tasks/ 02_Docs/ 03_TechDocs/
│   ├── 06_DongBang/                📂 동방푸드 ERP
│   │   └── 01_Tasks/ 02_TechDocs/ 04_References/
│   ├── 07_UNI/                     📂 대학 프로젝트
│   │   ├── 2023_OpenSoop/
│   │   └── 2024_PaekTaekApp/
│   └── 98_ETC/                     📂 기타 (단기 기술지원, 포트폴리오 비노출)
│       ├── 05_SeHanMT/             📂 세한MT POP
│       └── 08_NPP/                 📂 뉴파워 프라즈마
│
├── 02_Career/                      📁 경력 서류 (4개)
│   ├── 01_Resume.md                이력서
│   ├── 02_CareerDescription.md     경력기술서
│   ├── 03_CoverLetter.md           자기소개서
│   └── 04_Portfolio.md             포트폴리오
│
└── 03_Learning/                    📁 학습 & 기술 자료 (37개)
    ├── Backend/                    📂 백엔드 개발                (34)
    │   ├── Database/               DB 아키텍처, 인덱싱, N+1, 트랜잭션
    │   └── 개발정보 저장소/          Spring Boot, Servlet, Tomcat, MyBatis
    ├── DevOps/                     📂 DevOps & 배포              (3)
    │   └── 기술참고/                NginX, PostgreSQL, vi/vim 명령어
    ├── Tools/                      📂 개발 도구 (준비 중)
    └── References/                 📂 참고 자료 (준비 중)
```

---

## 📖 폴더별 역할

### 01_Projects - 프로젝트 문서
회사/개인 프로젝트의 작업 기록, 기술 문서, 회의록을 관리합니다.

**프로젝트 하위 폴더 규칙 (번호는 고정, 없는 분류는 생략):**

| 폴더 | 용도 |
|------|------|
| `01_Tasks/` | 이슈 대응·기능 개발 등 작업 기록 |
| `02_Docs/` | 프로젝트 일반 문서 |
| `02_TechDocs/` · `03_TechDocs/` | 기술 명세·분석 문서 |
| `03_Meetings/` | 회의록 |
| `04_References/` | SQL·배포·연동 등 참고 자료 |

### 02_Career - 경력 서류
Spring Boot 백엔드 지원용 경력 서류.

### 03_Learning - 학습 & 기술 자료
프로젝트에 종속되지 않는 일반 기술 학습 자료.

---

## 📝 문서 작성 규칙

블로그 목록과 Obsidian 문서 목록을 **동일하게** 유지하기 위한 규칙입니다.

### 1. 디렉토리별 공통양식

새 문서는 **템플릿에서 생성**합니다. Obsidian: `Ctrl+P` → `템플릿 삽입`.

| 디렉토리 | `type` | 템플릿 | 전용 속성 |
|----------|--------|--------|-----------|
| `01_Tasks/` | `작업` | `_templates/작업 (01_Tasks).md` | `priority`, `assignee` |
| `02_TechDocs/` · `03_TechDocs/` | `기술문서` | `_templates/기술문서 (02_TechDocs).md` | `category`, `assignee` |
| `03_Meetings/` | `회의록` | `_templates/회의록 (03_Meetings).md` | `attendees` |
| `04_References/` | `참고자료` | `_templates/참고자료 (04_References).md` | `category` |

**모든 문서 공통 속성**

```yaml
---
title: 신진SM 09.15 업무 미팅   # Obsidian 파일명과 동일하게
date: 2026-09-15                # 문서 기준일 (YYYY-MM-DD)
type: 회의록                    # 디렉토리에 따라 고정
project: 신진SM                 # 소속 프로젝트
status: 완료                    # 예정 / 진행중 / 완료 / 보류
tags: []
---
```

- `title` 이 없으면 블로그 목록 표기가 파일명과 어긋납니다.
- `date` 가 없으면 Quartz 가 **빌드 시각**을 쓰므로 목록 정렬이 매번 뒤섞입니다.
- `status` 는 위 4개 값만 사용합니다. 다른 값을 쓰면 필터가 깨집니다.
- 각 디렉토리의 `index.md` 상단에도 해당 양식이 정리돼 있습니다.

### 2. 본문 공통 골격

모든 문서가 **5단계 H2 하나**를 공유합니다. 상세 명세는 `_templates/_문서 양식 명세.md`.

| 단계 | 작업 | 기술문서 | 회의록 | 참고자료 |
|:--:|---|---|---|---|
| 1 | 개요 | 개요 | 개요 | 개요 |
| 2 | 현상 및 원인 | 배경 및 요구사항 | 논의 내용 | 환경 및 전제 |
| 3 | 조치 내용 | 설계 및 구현 | 결정 사항 | 상세 내용 |
| 4 | 검증 및 결과 | 검증 | 후속 조치 | 주의사항 |
| 5 | 참고 | 참고 | 참고 | 참고 |

- **H2 는 이 5개만** 씁니다. 세부 구분은 H3 이하로 내려씁니다.
- 빈 단계도 지우지 않습니다. 문서 간 비교가 가능해야 합니다.
- **코드·쿼리는 반드시 코드 펜스(` ```sql `)에 넣습니다.** 펜스가 없으면
  `#FFFACD` 같은 값이 블로그에서 태그로 잘못 인식됩니다.

### 3. 파일명에 날짜를 넣을 때

`09.15`, `25.11.03`, `(2025-10-15)` 형식을 사용하면 자동 생성 도구가 `date` 를 채워줍니다.

### 4. 폴더 목록 페이지 (`index.md`)

각 폴더의 `index.md` 안에 있는 아래 블록은 **자동 생성 영역**입니다. 직접 수정하지 마세요.

```
<!-- AUTO-INDEX:START ... -->
...
<!-- AUTO-INDEX:END -->
```

문서를 추가/삭제/이동한 뒤에는 저장소 루트에서 아래를 실행합니다.

```bash
python tools/normalize_frontmatter.py --apply  # 누락된 title/date 채우기
python tools/apply_schema.py --apply           # 프론트매터 공통양식 적용
python tools/apply_body_format.py --apply      # 본문 5단계 골격 적용
python tools/build_format_docs.py --apply      # index.md 의 "문서 양식" 갱신
python tools/build_index.py --apply            # index.md 의 문서 목록 갱신
```

모든 도구는 인자 없이 실행하면 **dry-run**(미리보기)이고, 여러 번 실행해도 결과가 같습니다.

마커 바깥의 설명 문구는 자유롭게 손으로 작성해도 유지됩니다.

### 5. 이미지

첨부 이미지는 **`Jeakyoung_Blog/resources/` 안에** 넣어주세요.
Vault 루트에 붙여넣은 이미지는 블로그 빌드에 포함되지 않아 깨져 보입니다.
(Obsidian 설정: `설정 → 파일 및 링크 → 첨부 파일 기본 저장 위치`)

---

## 🚀 배포

| 항목 | 내용 |
|------|------|
| **정적 사이트 생성기** | Quartz v4.4.0 |
| **배포** | GitHub Actions → GitHub Pages |
| **트리거** | `main` 브랜치의 `Jeakyoung_Blog/**`, `quartz.config.ts`, 워크플로 변경 |
| **워크플로** | `.github/workflows/deploy.yml` |
| **설정** | `quartz.config.ts` (저장소 루트) |

---

**구조 정리일:** 2026-06-30
**Quartz 배포 시작:** 2026-07-29
**목록 동기화 정비:** 2026-09-16
