---
title: IPACK BioStar 근태기 코드 정보
date: 2026-06-10
type: 작업
project: IPACK
status: 완료
priority: 보통
assignee:
  - 안재경
tags: []
created: 2026-06-10T14:28:00
---

# IPACK BioStar 근태기 코드 정보

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-06-10 |
| **대상 시스템** | 근태관리 (BioStar 생체인식 근태기 연동) |
| **관련 화면·프로그램** | TIN334 (출입기록 테이블) |

## 🔍 현상 및 원인

## 🔧 조치 내용

544354658
546839166
546839168
546839434
546839480
546839481
546839595
546839597
546839598
546839602
546839603

TIN334 → 조회가능

## ✅ 검증 및 결과

> [!note]
> 코드 목록 중 `546839166`/`546839596`은 입실, `546839433`/`546839434`는 퇴실 판별에 실제로 쓰이는 값이다 — `SP_WHR314_01_LIST`, `SP_WHR328_02_LIST`(둘 다 이 vault의 [[01_Projects/02_IPACK/01_Tasks/근태현황 list 아쉬운거 백업|근태현황 list 아쉬운거 백업]], [[01_Projects/02_IPACK/01_Tasks/iPack월근태 종합집계|iPack월근태 종합집계]]에 원문 있음)의 `NREADERIDN IN (...)` 조건과 `CASE WHEN NREADERIDN IN (546839596, 546839166) THEN '입실' WHEN NREADERIDN IN (546839433, 546839434) THEN '퇴실'` 분기에서 확인됨. 나머지 코드(544354658, 546839168, 546839480/481/595/597/598/602/603)의 의미는 소스에서 확인 안 됨 — 미확인.
> TIN334 자체는 iPlusERP 여러 SP에서 실제로 조회되는 테이블이 맞다(`FROM TIN334`, `WHERE ... NREADERIDN IN (...)`).

## 🔗 참고

- [[01_Projects/02_IPACK/02_TechDocs/근태_1기본개념/[참고] BioStar 근태기 코드정보|[참고] BioStar 근태기 코드정보]]
- [[01_Projects/02_IPACK/01_Tasks/근태현황 list 아쉬운거 백업|근태현황 list 아쉬운거 백업]]
