---
title: 데이터 바우처 DB Helper 계층 분리 및 ApiResponse 통일화 06.25
date: 2026-06-25
type: 작업
project: 데이터바우처
status: 완료
priority: 높음
assignee:
  - 안재경
tags: []
---

# 데이터 바우처 DB Helper 계층 분리 및 ApiResponse 통일화 06.25

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-06-25 |
| **대상 시스템** | F1Soft.Starmap.Service — 전체 디렉토리 구조/응답 규약 |
| **관련 화면·프로그램** | `Common/Database/*Helper`, `Common/Models/ApiResponse.cs`, `Services/Auth/*` |

> 50개 파일, +1471/-1935 규모의 리팩터링. `IDatabaseHelper` 기반 SQLServer/Oracle/PostgreSQL 헬퍼 3종 분리, `ApiResponse<T>` 응답 봉투 도입, Auth를 `TokenService`/`UserService`로 재정리 — 현재 레이어링·응답 규약의 원형.

## 🔍 현상 및 원인

### 재현 조건

DB 접근 코드가 흩어져 있고 컨트롤러마다 응답 모양이 제각각이라, 클라이언트가 성공/실패를 판별하는 방식이 일관되지 않았다.

### 원인

초기 구조에는 공용 응답 모델이 없었고(`Services/TokenService.cs` 하나에 인증 로직이 몰려 있는 등) DB 헬퍼도 정리되지 않은 상태였다.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 신규 | `Common/Database/{SQLServerHelper,OracleHelper,PostgreSQLHelper}.cs` | `IDatabaseHelper` 구현체 3종으로 분리, 트랜잭션 오픈 → `DbProcedureRequest` 실행 → `DataTable` 변환 → 예외 시 롤백 패턴 통일 |
| 신규 | `Common/Models/ApiResponse.cs` | `ApiResponse<T>{ Result, ResultList, ErrorMessage }` + `ApiResultItem<T>` 도입, `Success()`/`Fail()` 정적 팩토리 |
| 분리 | `Services/TokenService.cs` → `Services/Auth/{TokenService,UserService}.cs` + `ITokenService`/`IUserService` | 인증 로직을 인터페이스+구현 분리 구조로 재정리 |
| 이동 | `Services/EnvService/*` → `Common/Env/*` | 이후 [[01_Projects/04_DataBoucher/01_Tasks/데이터 바우처 TickerMiddleware·EnvService 멀티테넌시 구조 최초 구현 06.30]]의 전신 구조 정리 |

## ✅ 검증 및 결과

- [x] 컨트롤러 응답이 `ApiResponse<T>.Success/Fail` 한 형태로 통일됐는지 확인
- [x] 세 종류 `*DatabaseHelper`가 동일한 `CallProcedureAsync` 시그니처를 갖는지 확인

## 🔗 참고

- 커밋 `a4c82b2` "Fix Ahn / 디렉토리 구조개선 및 Response Body 형식 통일화"
- [[01_Projects/04_DataBoucher/02_TechDocs/[기술] Controller-Service-DatabaseHelper 계층과 ApiResponse·인증 구조]]
