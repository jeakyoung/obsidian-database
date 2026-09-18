---
title: "[기술] FCM 토큰·메시지 이력 관리 구조"
date: 2026-01-06
type: 기술문서
project: I-Frog
status: 진행중
category: FCM
assignee:
  - 안재경
tags:
  - FCM
  - Firebase
---

# [기술] FCM 토큰·메시지 이력 관리 구조

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | `Services/FirebaseService/FirebaseMessagingService.cs`, `Controllers/Notification/FcmController.cs` |
| **적용 범위** | FCM 토큰 등록, 발송, 이력 조회 |
| **관련 모듈** | `tgi001`(토큰), `tgi002`(발송 이력) — 둘 다 Postgres |

> FCM 자체는 Firebase Admin SDK가 처리하고, 이 서비스가 하는 건 "누구 토큰에 뭘 보냈고 언제 읽었는지"를 DB에 남기는 부분. 토큰/이력 테이블은 Postgres에 있는데, 발송 로직(`SendMessageAsync`)은 **MSSQL과 Postgres를 동시에 열어서** 쓴다.

## 🎯 배경 및 요구사항

Firebase 초기화는 `Program.cs`에서 앱 시작 시 1회(`FirebaseApp.Create`, `Keys/firebase-admin.json` 서비스 계정 키 사용). FCM 자체 발송은 SDK가 하지만, "이 사람이 이 알림을 받았는지/읽었는지"는 별도로 관리해야 해서 `tgi001`(토큰 테이블), `tgi002`(발송 이력 테이블)을 둠.

## 🏗 설계 및 구현

### 토큰 등록/조회 — Postgres만 사용

| 메서드 | 프로시저 | 비고 |
|:--|:--|:--|
| `SaveTokenAsync` | `public.tgi001_01_iud` | 로그인 시(`AuthController.Authenticate`) 호출 |
| `GetNotificationAsync` | `public.tgi002_01_list` | 알림 목록 조회 |
| `FcmPassivity` | `public.tgi001_01_list` → `public.tgi002_01_iud` | 업무연락 알림 발송([[I-Frog 업무연락 FCM 알림 문서정보 첨부]]) |

### 발송(`SendMessageAsync`) — MSSQL + Postgres 동시 사용

```csharp
using var helper   = new SQLServerHelper(_connectionString, _logger);   // 결재/업무 상태 조회
using var pghelper = new PostgreSQLHelper(_postgreConnectionString, _logger); // 토큰/이력
```

먼저 MSSQL `SP_TGI001_01_PATH`로 결재/업무 상태에 따른 발송 대상·조건을 뽑고(결재 흐름에 따라 다음 수신자를 찾는 로직, [[I-Frog 결제함 문서 FCM기능 추가]] 참고), 그 결과로 Postgres 쪽 토큰/이력 테이블(`tgi001_01_list`, `tgi002_01_iud`)을 다룬다. 결재 워크플로 상태는 MSSQL(그룹웨어 원본 DB), FCM 토큰/이력은 Postgres(통합서버) — 두 DB를 한 메서드 안에서 넘나든다.

> [!warning] 읽음 처리(SetFcmRead)는 통째로 주석 처리돼 있음
> `SetFcmRead` 메서드와 `SP_TGI002_01_IUD` 호출부가 전부 주석 상태. 알림을 읽음 처리하는 기능 자체가 지금은 비활성화돼 있다는 뜻 — `GetNotificationAsync`가 반환하는 읽음 여부 필드가 있다면 항상 고정값일 가능성이 있다.

## ✅ 검증

- [ ] 읽음 처리 기능을 다시 켤 계획이 있는지, 있다면 `SP_TGI002_01_IUD` 주석 해제 + 프론트 연동 필요
- [ ] `SendMessageAsync`가 MSSQL 트랜잭션과 Postgres 트랜잭션을 각각 별도로 커밋하는데, 한쪽만 실패했을 때 정합성이 깨지지 않는지 확인

## 🔗 참고

- [[[기술] Ticker 전략 패턴(ITickerStrategy) 설계]] - `FcmDbg`/`FcmSyn`(업체별 FCM 제한, 현재 미적용)
- [[I-Frog 업무연락 FCM 알림 문서정보 첨부]]
- [[I-Frog Setting 서비스 신규 구현]] - 알림 on/off와의 연동
- 최초 도입: `bb23ee5`(2026-01-06)
