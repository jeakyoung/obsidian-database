---
title: 신진SM - 더존 중복 문서처리 방어
date: 2026-09-14
type: 작업
project: 신진SM
status: 진행중
priority: 보통
assignee: []
tags: []
---

# 신진SM - 더존 중복 문서처리 방어

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-09-14 |
| **대상 시스템** | — |
| **관련 화면·프로그램** | — |

## 🔍 현상 및 원인

## 🔧 조치 내용

ProdReportService.java
- processProdReport() — IRU='I' 분기에서 ISEXISTS_OUT 확인 후 더존 문서 생성 생략 여부 판단
- createPreparedStatement() — CallableStatement로 전환, 38번 파라미터(ISEXISTS_OUT) OUTPUT 등록

ProdSLService.java
- processSLCrossMove() — 아래 두 지점에서 ISEXISTS_OUT 확인 후 더존 문서 생성 생략 여부 판단
  - "자체생산"(SL_ETC == null) 분기: prodReport() 호출 직후 / prodPacking() 호출 직후
  - "일반 포장"(else) 분기: prodPacking() 호출 직후
- prodReport() — CallableStatement로 전환, 38번 파라미터 OUTPUT 등록
- prodPacking() — CallableStatement로 전환, 38번 파라미터 OUTPUT 등록

SP
- SP_WPR559_02_IUD_TEST — @ISEXISTS_OUT INT = 0 OUTPUT 파라미터 추가 (양쪽 클래스가 공유하는 하나의 SP)

미적용(참고용, 손 안 댄 곳)
- ProdReportService IRU='U'/'D' 분기
- ProdSLService 삭제(IRU='D') 경로의 prodPacking() 호출 2곳

## ✅ 검증 및 결과

## 🔗 참고
