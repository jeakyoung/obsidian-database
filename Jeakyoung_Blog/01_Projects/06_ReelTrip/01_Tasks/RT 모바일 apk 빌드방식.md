---
title: RT 모바일 apk 빌드방식
date: 2026-06-10
type: 작업
project: ReelTrip
status: 진행중
priority: 보통
assignee: []
tags: []
created: 2026-06-10T14:29:00
---

# RT 모바일 apk 빌드방식

## 1. 개요

| 항목 | 내용 |
|------|------|
| 요청자 |  |
| 요청일 | 2026-06-10 |
| 대상 시스템 |  |
| 관련 화면·프로그램 |  |

## 2. 현상 및 원인

## 3. 조치 내용

---

### 📱 React Native / Expo 빌드 명령어 가이드

| 상황 | 명령어 | 비고 |
| --- | --- | --- |
| **로컬 개발 빌드** | `$env:APP_VARIANT="development"; npx expo run:android` | PowerShell 환경 기준 (Windows) |
| **로컬 운영 빌드** | `npx expo prebuild --clean && npx expo run:android --variant release` | 네이티브 폴더 클린 후 Release 빌드 |
| **EAS 개발 빌드** | `eas build --profile development --platform android` | Expo Cloud 개발용 빌드 |
| **EAS 운영 빌드** | `eas build --profile production --platform android` | 스토어 배포용 최종 빌드 |

---

##### 💻 명령어 상세 설명

##### 1. 로컬 개발 빌드 (Local Development Build)

> 로컬 머신에서 에뮬레이터나 실기기를 연결하여 개발 모드로 네이티브 빌드를 진행할 때 사용합니다.

```powershell
$env:APP_VARIANT="development"; npx expo run:android
```

## 4. 검증 및 결과

## 5. 참고
