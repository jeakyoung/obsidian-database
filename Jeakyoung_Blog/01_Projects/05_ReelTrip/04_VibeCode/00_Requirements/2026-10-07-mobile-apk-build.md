---
title: 모바일 APK 빌드 문서 완성 및 빌드 실행
date: 2026-10-07
type: 요구사항서
project: ReelTrip
status: 컨펌대기
assignee: []
tags: []
---

## 요구사항 정보

| 항목 | 내용 |
|------|------|
| **작성일** | 2026-10-07 |
| **대상 앱** | Mobile |
| **대상 페이지/화면** | — (빌드/배포 작업, 화면 변경 없음) |
| **작업 유형** | 기타 (문서화 + 빌드 실행) |
| **우선순위** | 보통 |

---

## 현재 상태 (As-Is)

- `apps/mobile/eas.json`에 빌드 프로필 3종이 정의되어 있음: `development`(internal, dev client), `preview`(internal, `android.buildType: apk` 명시, staging API), `production`(autoIncrement, buildType 미지정 → EAS 기본값인 app-bundle/AAB).
- `obsidian/.../01_Tasks/RT 모바일 apk 빌드방식.md` 문서가 이미 존재하지만 `status: 진행중`이며, "현상 및 원인", "검증 및 결과", "참고" 섹션이 비어 있고 로컬 빌드 명령어 가이드만 채워진 미완성 상태.
- EAS CLI는 설치되어 있고 `dwahn1213`(dwahn4823@gmail.com) 계정으로 로그인되어 있음 — 빌드 실행 자체는 가능한 상태.

---

## 원하는 상태 (To-Be)

- 기존 작업 문서(`RT 모바일 apk 빌드방식.md`)의 빈 섹션을 채워 완성하고, 실제로 EAS에서 APK 빌드를 1회 실행해 그 결과(빌드 링크, 성공 여부 등)를 문서에 기록한다.

---

## 상세 요구사항

### 기능 요구사항
1. 기존 작업 문서의 "현상 및 원인", "조치 내용", "검증 및 결과", "참고" 섹션을 실제 내용으로 완성하고 `status`를 `완료`로 변경한다.
2. EAS Build로 Android APK를 실제로 1회 빌드하고, 빌드 결과(성공/실패, 빌드 상세 페이지 링크)를 문서의 "검증 및 결과" 섹션에 기록한다.

### 제약 조건
- 범위를 벗어나는 추가 기능 구현, 리팩토링은 하지 않는다.
- 기존 `production` 프로필(스토어 제출용 AAB 흐름)의 동작은 변경하지 않는다.

### 확인 필요 사항 [?]
- [?] 어떤 프로필로 빌드할지: `preview`(staging API, 이미 APK로 명시됨 — 추가 설정 없이 바로 실행 가능) vs `development`(dev client, internal 배포 시 기본값이 APK) vs `production`을 APK로 받고 싶다면 별도 프로필 신설 필요.
- [?] 빌드 방식: EAS 클라우드 빌드(권장, 서명/credentials를 EAS가 관리) vs 로컬 빌드(`expo run:android --variant release`, release keystore가 로컬에 없어 추가 설정 필요).

---

## 참고 자료

- `apps/mobile/eas.json`
- `apps/mobile/app.config.js`
- `obsidian/Jeakyoung_Blog/01_Projects/05_ReelTrip/01_Tasks/RT 모바일 apk 빌드방식.md`
