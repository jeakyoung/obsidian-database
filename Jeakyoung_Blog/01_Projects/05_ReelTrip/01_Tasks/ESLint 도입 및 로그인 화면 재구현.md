---
title: ESLint 도입 및 로그인 화면 재구현
date: 2026-06-17
type: 작업
project: ReelTrip
status: 완료
priority: 보통
assignee:
  - 류채현
tags: []
---

# ESLint 도입 및 로그인 화면 재구현

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-06-17 |
| **대상 시스템** | Web |
| **관련 화면·프로그램** | `apps/web/eslint.config.mjs`, `domains/auth/*`, `app/test-ui` |

> 기능 붙이기 바쁘던 시기 이후 한 번 정리하고 간 커밋. Web에 처음으로 ESLint 설정이 생긴 게 이때

## 🔍 현상 및 원인

Web에 그동안 ESLint 설정 자체가 없어서 (`next lint`가 기본값으로만 동작) 스타일이 들쭉날쭉했고, 실험용으로 만들어둔 `app/test-ui/page.tsx`(149줄) 같은 죽은 라우트가 그대로 남아있었다. 로그인 화면도 초기 버전 그대로라 브랜드 아이덴티티 없이 폼만 덩그러니 있는 상태였음.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 설정 | `eslint.config.mjs` | 신규 생성 — `next/core-web-vitals` + `next/typescript` 기반 |
| 삭제 | `app/test-ui/page.tsx` | 죽은 라우트 제거 (149줄) |
| 화면 | `AuthLoginScreen.tsx` / `LoginForm.tsx` | 로직 정리 |
| 화면 | `OrbitBrandPanel.tsx` | 신규 — 로그인 화면 좌측 브랜드 패널 |
| 도메인 | `UrlParserModal.tsx` | `place` 도메인으로 이동·재구성 (273줄) |
| 정리 | `domains/auth/session.ts` | 중복 로직 제거 |

ESLint 규칙 중 특기할 것 두 가지:

```javascript
// _ 접두사 변수/인자는 "의도적 미사용"으로 간주
"@typescript-eslint/no-unused-vars": [
  "error",
  { argsIgnorePattern: "^_", varsIgnorePattern: "^_", caughtErrorsIgnorePattern: "^_" },
],
// 영상 썸네일 등 동적 외부 URL 이미지가 핵심 기능이라 <img>를 구조적으로 사용.
// next/image는 임의 외부 도메인에 부적합하므로 규칙을 끈다.
"@next/next/no-img-element": "off",
```

`no-img-element`를 끈 건 임의로 넘긴 게 아니라, URL 파서로 받아오는 유튜브/인스타 썸네일이 도메인이 매번 달라서 `next/image`의 화이트리스트 방식이랑 구조적으로 안 맞기 때문 — 이 서비스 특성 때문에 생긴 예외.

## ✅ 검증 및 결과

- [x] `next lint` 통과
- [x] 죽은 라우트(`test-ui`) 접근 시 404 확인
- [x] 로그인 화면 브랜드 패널 정상 렌더링

## 🔗 참고

- 커밋 `636aef8` (Rchaehyeon)
- [\[기술\] 모노레포 기반 설정](<../03_TechDocs/[기술] 모노레포 기반 설정.md>) — ESLint 규칙 배경 설명
