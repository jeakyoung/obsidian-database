---
title: 모바일 APK 빌드 문서 완성 및 빌드 실행
date: 2026-10-07
type: 작업지시서
project: ReelTrip
status: 진행중
assignee: []
tags: []
---

## 작업 개요

| 항목 | 내용 |
|------|------|
| **작성일** | 2026-10-07 |
| **요구사항 참조** | [[Jeakyoung_Blog/01_Projects/05_ReelTrip/04_VibeCode/00_Requirements/2026-10-07-mobile-apk-build]] |
| **대상 앱** | Mobile |
| **대상 페이지/화면** | — (빌드/배포 작업) |
| **작업 유형** | 기타 (문서화 + 빌드 실행) |
| **예상 영향 범위** | `obsidian/.../01_Tasks/RT 모바일 apk 빌드방식.md` (수정), EAS 클라우드 빌드 1건 생성 |

---

## 요구사항 분석 요약

- `eas.json`의 `preview` 프로필이 이미 `android.buildType: apk`로 명시되어 있어, 별도 설정 변경 없이 바로 APK 빌드가 가능한 유일한 프로필임.
- `development`도 internal 배포라 EAS 기본값상 APK로 나오지만 dev client가 포함되어 별도 실행 환경이 필요함.
- `production`은 buildType 미지정 → 기본 AAB. 운영 데이터 기준 APK가 필요하면 기존 `production`을 건드리지 않고 새 프로필을 추가하는 편이 안전.
- [?] 사용자가 어떤 데이터(운영/스테이징/개발)를 바라보는 APK를 원하는지에 따라 선택할 프로필이 달라짐 — 채팅으로 확인 후 진행.

---

## 작업 계획

### 1단계: 분석 및 준비
- [x] `eas.json`/`app.config.js` 구조 확인
- [x] EAS CLI 설치 및 로그인 상태 확인 (`dwahn1213`, dwahn4823@gmail.com)
- [x] 사용자에게 빌드 프로필 확인 → `preview` 선택

### 2단계: 구현
- [ ] `eas build --platform android --profile preview` 실행 (클라우드 빌드)
- [ ] 빌드 진행/완료 상태 확인

### 3단계: 검증
- [ ] 빌드 성공 여부 및 산출물(APK) 다운로드 링크 확보
- [ ] `RT 모바일 apk 빌드방식.md`의 "현상 및 원인"/"조치 내용"/"검증 및 결과"/"참고" 섹션 작성, `status: 완료`로 변경

---

## 변경 대상 파일

| 파일 경로 | 변경 유형 | 변경 내용 요약 |
|-----------|-----------|----------------|
| `obsidian/Jeakyoung_Blog/01_Projects/05_ReelTrip/01_Tasks/RT 모바일 apk 빌드방식.md` | 수정 | 빈 섹션 완성, status 완료 처리 |

---

## 사이드 이펙트 검토

- 영향 없음 — 앱 코드/설정은 변경하지 않고(프로필 신설이 필요한 경우만 `eas.json`에 새 블록 추가), 기존 `eas.json`의 `production`/`preview`/`development` 프로필 동작은 그대로 유지한다.

---

## 확인 필요 사항

- [x] 빌드할 프로필: `preview` 선택 완료
- [x] EAS 클라우드 빌드로 진행 (로컬 release 서명키 없음)

---

## 컨펌

- [x] 위 계획대로 진행 승인
- [ ] 수정 후 재검토 필요
