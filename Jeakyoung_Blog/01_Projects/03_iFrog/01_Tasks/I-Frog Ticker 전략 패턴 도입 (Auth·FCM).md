---
title: I-Frog Ticker 전략 패턴 도입 (Auth·FCM)
date: 2026-03-05
type: 작업
project: I-Frog
status: 완료
priority: 보통
assignee:
  - 안재경
tags:
  - Strategy Pattern
  - Auth
  - FCM
---

# I-Frog Ticker 전략 패턴 도입 (Auth·FCM)

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-03-05 |
| **대상 시스템** | `Controllers/Auth`, `Services/FirebaseService` |
| **관련 화면·프로그램** | 로그인, FCM 토큰 등록 |

> 회사별로 갈라지는 로그인/FCM 로직을 `if (ticker == ...)` 대신 `ITickerStrategy<T>` 구현체로 분리.

## 🔍 현상 및 원인

멀티테넌시 커넥션은 정리됐는데([[I-Frog 보안코드 기반 멀티테넌시 DB 커넥션 구현]]), 로그인 시 ATC만 FCM 토큰을 같이 받아야 하는 것처럼 회사별 예외 로직이 컨트롤러/서비스 코드에 조건문으로 박히기 시작함.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 인터페이스 | `Strategies/ITickerStrategy.cs` | `f02d066`에서 최초 도입 (원래는 `Groupware/Notice`에 적용해봄) |
| 로그인 | `Controllers/Auth/Strategy/LoginAtc.cs`, `LoginSyn.cs` | `4e22bbc`에서 추가. `LoginAtc`는 ATC 로그인 시 FCM 토큰을 파라미터에 실어 보냄 |
| FCM | `Services/FirebaseService/Strategy/FcmDbg.cs`, `FcmSyn.cs` | 같은 커밋에서 추가, 회사별 FCM 등록 처리 분리 |
| 등록 | `Program.cs` | `AddScoped<ITickerStrategy<AuthRequest>, LoginAtc>()` 등으로 DI 등록 |
| 롤백 | `Groupware/Notice` | `bc683d3`에서 Notice 쪽 전략(`GetNoticeAtc`/`GetNoticeSgy`)은 제거 — 분기가 그 정도로 복잡하지 않았던 걸로 보임 |

## ✅ 검증 및 결과

- [x] ATC 로그인 시 FCM 토큰 파라미터 반영 확인
- [ ] `LoginAtc`/`LoginSyn`이 서로 다른 제네릭 타입(`AuthRequest`/`AuthResponse`)으로 등록된 부분 정리할지 결정 필요

## 🔗 참고

- [[[기술] Ticker 전략 패턴(ITickerStrategy) 설계]]
- 커밋: `f02d066`, `4e22bbc`, `bc683d3`(Notice 전략 제거)
