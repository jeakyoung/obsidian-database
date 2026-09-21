---
title: I-Frog Setting 서비스 신규 구현
date: 2026-01-14
type: 작업
project: I-Frog
status: 완료
priority: 보통
assignee:
  - 안재경
tags:
  - Setting
  - FCM
---

# I-Frog Setting 서비스 신규 구현

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-01-14 |
| **대상 시스템** | `Controllers/Setting` (신규), `Controllers/Notification/FcmController` |
| **관련 화면·프로그램** | 알림 설정 화면 |

> 사용자별로 결재/게시판/공지/일정 알림을 개별적으로 켜고 끌 수 있게 `Setting` 도메인을 새로 만들고, FCM 발송 시 이 설정을 확인하도록 연결.

## 🔍 현상 및 원인

FCM은 이미 있었지만(`Notification/FcmController`), 사용자가 "결재 알림은 받고 공지 알림은 끄고 싶다" 같은 개인화가 불가능했음 — 껐다 켰다 할 설정 자체가 없었음.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 신규 도메인 | `Controllers/Setting/{ISettingService,SettingController,SettingService}.cs` | `GetSetting`(`SP tgi003_01_list`), `SetSetting`(`SP tgi003_01_iud`) 엔드포인트 신설 |
| 모델 | `Models/SetSettingRequest.cs` | `employeeNo` + 알림 종류별 플래그(`approvalChkFlag`, `boardChkFlag`, `notiChkFlag`, `scheduleChkFlag`) |
| FCM 연동 | `FcmController.cs` | 발송 전 조회 조건에 사용자별 알림 허용 여부 판별 로직 추가 |
| 정리 | `GetAlarmRequest.cs` → `GetNotificationRequest.cs` | 엔드포인트/모델명을 `GetAlarmList` → `GetNotificationList`로 정리 |

## ✅ 검증 및 결과

- [x] TGI003 등록/수정/조회 프로시저 연동 확인 (커밋 메시지 기준 "완료")
- [ ] 알림 종류가 늘어날 때(`*ChkFlag` 필드 추가) 마이그레이션 방식 정리 필요

## 🔗 참고

- 커밋: `cf364cb` feat ahn / Setting 서비스 추가 및 FCM 기능 수정
- [[I-Frog 결제함 문서 FCM기능 추가]]
