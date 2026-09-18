---
title: I-Frog 업무현황판 중복 컨트롤러 정리 및 공정진행 조회 추가
date: 2026-09-18
type: 작업
project: I-Frog
status: 완료
priority: 보통
assignee:
  - 안재경
tags:
  - Groupware
  - WorkStatus
---

# I-Frog 업무현황판 중복 컨트롤러 정리 및 공정진행 조회 추가

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-09-18 |
| **대상 시스템** | F1Soft.Starmap.Service (`Controllers/Groupware/WorkStatus`) |
| **관련 화면·프로그램** | 업무현황판 |

> 레거시 경로(`Controllers/WorkStatus`)와 현재 경로(`Controllers/Groupware/WorkStatus`)에 업무현황판 컨트롤러가 중복 존재하던 것을 정리하고, 신규 조회 기능(공정진행 조회)을 추가.

## 🔍 현상 및 원인

`Controllers/WorkStatus/WorkStatusController.cs` (구 경로, `GetDomainRequest` 모델 사용)와 `Controllers/Groupware/WorkStatus/WorkStatusController.cs` (현 경로, `WorkStatusRequest` 모델 사용)가 동시에 남아 있었다. 구 경로 쪽은 더 이상 쓰이지 않는 상태였음.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 정리 | `Controllers/WorkStatus/*` | 구 경로 컨트롤러·모델(`GetDomainRequest.cs`) 삭제, `Groupware/WorkStatus`로 단일화 |
| 기능 추가 | `IWorkStatusService.GetWorkProgress`, `WorkProgressRequest` | 공정진행 조회 요청 모델 신설: `ProdDateFrom`/`ProdDateTo`(생산일자 범위, yyyyMMdd), `Search`(품목명 등 검색어), `CloseFlag`(0: 미완료건만 / 1: 전체, 기본값 "1") |
| 컨트롤러 | `WorkStatusController` | `POST /GetWorkProgress` 엔드포인트 추가 |
| 서비스 | `WorkStatusService` | MSSQL 커넥션 문자열(`_connectionString`)을 새로 주입받아 `SP_WPR307_01_LIST` 프로시저 호출(`SQLServerHelper` 사용, 기존 `GetDomain`은 PostgreSQL 사용). 응답은 `PART_NO`, `INSERT_COUNT`, `DIVISION_COUNT`, `INGRED_NAME`, `LAYER_CNT`, `INPUT_DNL`, `WORK_NAME`, `NEXT_NAME`, `HOLDING_TIME`, `LIMIT_FLAG` 컬럼만 필터링해 반환 |

> [!note] DB 이원화
> `WorkStatusService` 안에서 `GetDomain`(도메인/공장 목록, PostgreSQL)과 `GetWorkProgress`(공정진행, MSSQL SP)가 서로 다른 DB를 조회한다. 신규 메서드 추가 시 어느 커넥션을 써야 하는지 헷갈리지 않도록 주의.

## ✅ 검증 및 결과

- [ ] `SP_WPR307_01_LIST` 실제 응답 컬럼과 필터링 목록 일치 여부 확인 필요
- [ ] 구 경로(`Controllers/WorkStatus`) 참조하던 프론트/스케줄러가 없는지 확인 필요

## 🔗 참고

- 커밋: `a34c94f` Fix Ahn / 업무 현황판 수정, `08832d8` feat ahn / 업무현황 도메인 Selector 추가
