---
title: 옵시디언 문서 관리 체계 구축
date: 2026-09-17
type: 요구사항서
project: ReelTrip
status: 완료
assignee:
  - 안재경
tags: []
---

# 요구사항지시서

> 옵시디언 vault 서브모듈 연동 및 기술문서/태스크 문서 초안 작성

---

## 요구사항 정보

| 항목 | 내용 |
|------|------|
| **작성일** | 2026-09-17 |
| **대상 앱** | 공통 |
| **대상 페이지/화면** | N/A — 레포 구조(서브모듈) + 문서화 작업 |
| **작업 유형** | 기타 (레포 구조 변경 + 문서 자동 생성) |
| **우선순위** | 보통 |

---

## 현재 상태 (As-Is)

- 코드베이스 내 기술문서/작업 이력은 `docs/orders`, `docs/workOrders`, `docs/results` 마크다운으로만 관리되고 있으며, 옵시디언 vault와는 아무 연결점이 없음.
- 옵시디언 vault(`https://github.com/jeakyoung/obsidian-database.git`)는 별도 GitHub 저장소로 존재하며, 현재 이 레포(ReeL-Trip)에서 clone/참조할 방법이 없음.

---

## 원하는 상태 (To-Be)

- 옵시디언 vault가 이 레포의 `obsidian/` 경로에 git submodule로 편입되어, 하나의 로컬 워크스페이스에서 코드와 문서를 함께 다룰 수 있음.
- Web/Mobile/API 전체 코드베이스를 분석한 아키텍처·기술스택 문서와, 향후 진행할 만한 태스크 목록이 옵시디언 마크다운 컨벤션(YAML 프론트매터, `[[위키링크]]`)으로 `obsidian/` 하위에 1회성으로 작성됨.

---

## 상세 요구사항

### 기능 요구사항

1. `git submodule add https://github.com/jeakyoung/obsidian-database.git obsidian` 실행 (레포 루트 기준 `obsidian/` 경로).
2. 서브모듈 clone 직후 vault의 기존 폴더 구조/컨벤션(PARA, 태그 규칙 등)을 먼저 확인하고, 그 구조에 맞춰 신규 문서 배치 위치를 결정.
3. 기술문서 작성 — 모노레포 개요, 앱별(Web/Mobile/API) 아키텍처, 기술스택(Next.js 15 / Expo / Spring Boot 3 / PostgreSQL(Neon) / MyBatis / Flyway / pgvector 등), API 응답/도메인 구조 요약.
4. 태스크 문서 작성 — 현재 `docs/workOrders`에 남아있는 미완료/진행중 항목을 참고해 옵시디언 태스크 노트로 정리.
5. 문서는 옵시디언 컨벤션(YAML 프론트매터, `[[위키링크]]`, 태그)을 사용.

### 제약 조건

- 이번 작업 범위는 "1회성 초안 작성"까지이며, 자동화(git hook, CI, 반복 트리거)는 포함하지 않음 — 필요 시 추후 별도 요청.
- 서브모듈 추가로 인한 `.gitmodules` 변경 및 관련 커밋/푸시는 사용자 명시적 승인 후 진행 (git add/commit/push는 문서 작성과 별개로 확인받음).
- 기존 `docs/orders`, `docs/workOrders`, `docs/results` 체계는 그대로 유지 — 옵시디언 문서는 이를 대체하지 않고 보완하는 용도.

---

## 확인 필요 사항

- [ ] `obsidian-database` 레포가 private인 경우 인증 방식(SSH 키 / PAT) 확인 필요 — clone 시도 후 실패하면 보고.
- [ ] vault의 기존 폴더 구조를 clone 직후 실제로 확인해 문서 배치 위치를 재조정할 수 있음.
- [ ] 문서 작성 후 커밋/푸시 여부와 시점은 별도로 확인받음 (기본값: 작성만 하고 커밋은 보류).

---

## 참고 자료

- 옵시디언 vault: `https://github.com/jeakyoung/obsidian-database.git`
- 서브모듈 경로: `obsidian/`
- 기존 기술스택 정리: 본 대화 중 확인한 `apps/api-spring` 구성 (PostgreSQL/Neon, MyBatis, Flyway, pgvector, OpenAI 임베딩)
