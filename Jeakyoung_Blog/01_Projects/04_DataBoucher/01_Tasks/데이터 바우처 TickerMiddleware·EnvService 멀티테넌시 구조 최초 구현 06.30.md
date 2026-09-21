---
title: 데이터 바우처 TickerMiddleware·EnvService 멀티테넌시 구조 최초 구현 06.30
date: 2026-06-30
type: 작업
project: 데이터바우처
status: 완료
priority: 높음
assignee:
  - 안재경
tags: []
---

# 데이터 바우처 TickerMiddleware·EnvService 멀티테넌시 구조 최초 구현 06.30

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-06-30 |
| **대상 시스템** | F1Soft.Starmap.Service — 전체 API 파이프라인 |
| **관련 화면·프로그램** | `TickerMiddleware`, `SecurityCodeMapper`, `TickerContext`, `EnvService` |

> 회사별(`DevEnvService`/`StgEnvService`/`PrdEnvService`)로 나뉘어 있던 환경 서비스를 `SECURITY_CODE` 헤더 기반 `TickerMiddleware` + 단일 `EnvService`로 통합 — 이 구조가 이후 [[01_Projects/04_DataBoucher/02_TechDocs/[기술] SECURITY_CODE 기반 멀티테넌시 구조 (TickerMiddleware)]]의 원형.

## 🔍 현상 및 원인

### 재현 조건

여러 회사(거래처)·여러 환경(Dev/Stg/Prd)을 하나의 배포로 서빙해야 하는데, 기존에는 `Services/EnvService/{Dev,Stg,Prd}EnvService.cs`처럼 환경별로 클래스가 나뉘어 있었다.

### 원인

환경별 클래스 분리 방식은 회사가 늘어나거나 배포 대상이 바뀔 때마다 코드/DI 등록을 손봐야 해서 확장성이 떨어졌다. 요청 헤더 하나로 런타임에 회사·환경을 결정하는 구조가 필요했다.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 삭제 | `Common/Env/{Dev,Stg,Prd}EnvService.cs` | 환경별 개별 구현체 제거 |
| 신규 | `Common/Env/EnvService.cs` | `TickerContext`의 `CurrentTicker`/`CurrentEnv`로 `ConnSettings:{Ticker}:*` 키를 조합하는 단일 구현체 |
| 신규 | `Common/Env/SecurityCodeMapper.cs` | `SECURITY_CODE` 앞 2자리→Ticker, 뒤 2자리→Env 매핑 |
| 신규 | `Common/Env/TickerMiddleware.cs` | 요청 파이프라인에서 헤더를 읽어 `TickerContext`를 초기화하는 미들웨어 |
| 신규 | `Contexts/TickerContext.cs` | 요청 스코프 컨텍스트. `Initialize`/`EnvInitialize`는 각각 1회만 허용(재호출 시 `InvalidOperationException`) |

## ✅ 검증 및 결과

- [x] `SECURITY_CODE` 헤더로 DBG/SYN × Dev/Prd 조합이 올바른 커넥션 문자열로 분기되는지 확인
- [x] `TickerContext` 이중 초기화 시 예외 발생 확인

## 🔗 참고

- 커밋 `8533590` "Feat Ahn / 티커에"
- [[01_Projects/04_DataBoucher/02_TechDocs/[기술] SECURITY_CODE 기반 멀티테넌시 구조 (TickerMiddleware)]]
