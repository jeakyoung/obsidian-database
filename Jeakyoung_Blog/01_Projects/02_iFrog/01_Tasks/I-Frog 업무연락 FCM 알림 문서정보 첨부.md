---
title: I-Frog 업무연락 FCM 알림 문서정보 첨부
date: 2026-08-14
type: 작업
project: I-Frog
status: 완료
priority: 보통
assignee:
  - 안재경
tags:
  - Notification
  - FCM
---

# I-Frog 업무연락 FCM 알림 문서정보 첨부

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-08-14 |
| **대상 시스템** | F1Soft.Starmap.Service (`Controllers/Notification/FcmController`) |
| **관련 화면·프로그램** | 업무연락 알림 (`notiGbn = 8`) |

> 업무연락 FCM을 탭했을 때 앱이 해당 결재/업무 문서로 바로 이동할 수 있도록, 알림 데이터(payload)에 문서 식별 정보를 함께 실어 보내는 기능 추가.

## 🔍 현상 및 원인

기존 FCM 발송(`FcmPassivityRequest`)은 `notiGbn`, `companyCode`, `empList`, `senderCode`, `title`, `body`만 가지고 있어 클라이언트가 알림을 눌러도 어떤 문서(결재 실행 ID 등)인지 알 수 없었다. 프론트에서 딥링크로 문서 상세화면까지 이동하려면 알림 데이터 안에 문서 키 값이 필요했다.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 모델 | `Models/FcmPassivityRequest.cs` | `division`(화면 구분, 예: `communication`)과 `payload`(`FcmPassivityPayload`: `eaExeId`, `eabusNo`, `employeeNo`, `gbnCode`, `exeSeq`) 필드 추가 |
| 컨트롤러 | `FcmController.cs` | XML 문서 Sample request에 `division`/`payload` 예시 추가. `notiGbn = 8`(업무연락)일 때만 사용하는 선택 필드로 문서화 |
| 인증 | `FcmController.cs` | 같은 커밋에서 API Key 검증 추가: `X-Api-Key` 헤더 값이 `ApiKeySettings:FcmInternalKey`와 일치하면 JWT 없이도(`User.Identity.IsAuthenticated == false`) 호출 허용 — 외부 서버(스케줄러 등)에서 JWT 없이 알림을 트리거하기 위함 |

## ✅ 검증 및 결과

- [ ] 클라이언트에서 알림 탭 → payload 파싱 → 문서 상세화면 딥링크 동작 확인 필요
- [ ] `ApiKeySettings:FcmInternalKey` 미설정 환경에서 401 처리 확인 필요

## 🔗 참고

- 커밋: `dea3a6d` Feat Ahn / 업무 알림시 FCM data내에 문서정보 첨부 기능
- [[I-Frog 결제함 문서 FCM기능 추가]] - 결재 흐름 내 FCM 발송 로직(별도 케이스)
