---
title: 신진SM ERP 기말 재고 오류 ( 입 출고 내역에 이상이 없을경우 )
date: 2026-09-10
type: 작업
project: 신진SM
status: 진행중
priority: 보통
assignee: []
tags: []
---

# 신진SM ERP 기말 재고 오류 ( 입 출고 내역에 이상이 없을경우 )

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-09-10 |
| **대상 시스템** | — |
| **관련 화면·프로그램** | — |

## 🔍 현상 및 원인

## 🔧 조치 내용

MM_OHSLINVM 월별집계 불일치 수정 가이드                                                          
                                                                                          
  전제 조건                                                                                        
                                                                                                   
  - MM_OHSLINVD (일별 상세) = 정상                                                                 
  - MM_PINVN (연간 집계) = 정상                                                                    
  - MM_OHSLINVM (월별 집계) = 틀어진 상태

  ---
  Step 1. 불일치 품목 전체 탐지

  SELECT p.CD_ITEM,
         p.QT_GOOD_OPEN + p.QT_GOOD_GR - p.QT_GOOD_GI AS 기말재고_PINVN,
         p.QT_GOOD_GR - m.SUM_GR AS GR_차이,
         p.QT_GOOD_GI - m.SUM_GI AS GI_차이
  FROM MM_PINVN p
  JOIN (
      SELECT CD_SL, CD_PLANT, CD_COMPANY, CD_ITEM, CD_PJT, SEQ_PROJECT,
             SUM(QT_GOOD_GR) AS SUM_GR,
             SUM(QT_GOOD_GI) AS SUM_GI
      FROM MM_OHSLINVM
      WHERE YY_INV = '[년도]'
      GROUP BY CD_SL, CD_PLANT, CD_COMPANY, CD_ITEM, CD_PJT, SEQ_PROJECT
  ) m ON p.CD_SL=m.CD_SL AND p.CD_PLANT=m.CD_PLANT
     AND p.CD_COMPANY=m.CD_COMPANY AND p.CD_ITEM=m.CD_ITEM
     AND p.CD_PJT=m.CD_PJT AND p.SEQ_PROJECT=m.SEQ_PROJECT
  WHERE p.P_YR = '[년도]'
    AND p.CD_SL = '[창고]' AND p.CD_PLANT = '[공장]' AND p.CD_COMPANY = '[회사]'
    AND (ABS(p.QT_GOOD_GR - m.SUM_GR) > 0 OR ABS(p.QT_GOOD_GI - m.SUM_GI) > 0)

  ---
  Step 2. 특정 품목의 틀어진 월/QTIOTP 확인

  SELECT d.YM_IO, d.CD_QTIOTP,
         d.SUM_GR AS D_GR, ISNULL(m.QT_GOOD_GR,0) AS M_GR, d.SUM_GR - ISNULL(m.QT_GOOD_GR,0) AS
  GR_차이,
         d.SUM_GI AS D_GI, ISNULL(m.QT_GOOD_GI,0) AS M_GI, d.SUM_GI - ISNULL(m.QT_GOOD_GI,0) AS
  GI_차이
  FROM (
      SELECT CD_SL, CD_PLANT, CD_COMPANY, CD_ITEM, YY_INV,
             LEFT(DT_IO,6) AS YM_IO, CD_QTIOTP, CD_PJT, SEQ_PROJECT,
             SUM(QT_GOOD_GR) AS SUM_GR,
             SUM(QT_GOOD_GI) AS SUM_GI
      FROM MM_OHSLINVD
      WHERE CD_ITEM    = '[품목코드]'
        AND YY_INV     = '[년도]'
        AND CD_SL      = '[창고]'
        AND CD_PLANT   = '[공장]'
        AND CD_COMPANY = '[회사]'
      GROUP BY CD_SL, CD_PLANT, CD_COMPANY, CD_ITEM, YY_INV,
               LEFT(DT_IO,6), CD_QTIOTP, CD_PJT, SEQ_PROJECT
  ) d
  LEFT JOIN MM_OHSLINVM m
    ON m.CD_SL=d.CD_SL AND m.CD_PLANT=d.CD_PLANT AND m.CD_COMPANY=d.CD_COMPANY
   AND m.CD_ITEM=d.CD_ITEM AND m.YY_INV=d.YY_INV AND m.YM_IO=d.YM_IO
   AND m.CD_QTIOTP=d.CD_QTIOTP AND m.CD_PJT=d.CD_PJT AND m.SEQ_PROJECT=d.SEQ_PROJECT
  WHERE ABS(d.SUM_GR - ISNULL(m.QT_GOOD_GR,0)) > 0
     OR ABS(d.SUM_GI - ISNULL(m.QT_GOOD_GI,0)) > 0

  ---
  Step 3. MM_OHSLINVM 수정

  단일 품목 수정 (Step 2 결과 보고 수동 지정):
  UPDATE MM_OHSLINVM
  SET QT_GOOD_GR = [D_GR값],
      QT_GOOD_GI = [D_GI값]
  WHERE CD_ITEM    = '[품목코드]'
    AND YM_IO      = '[년월]'
    AND CD_QTIOTP  = '[수불형태]'
    AND CD_SL      = '[창고]'
    AND CD_PLANT   = '[공장]'
    AND CD_COMPANY = '[회사]'

  불일치 전체 일괄 수정 (DD→M 동기화):
  UPDATE m
  SET m.QT_GOOD_GR = d.SUM_GR,
      m.QT_GOOD_GI = d.SUM_GI
  FROM MM_OHSLINVM m
  JOIN (
      SELECT CD_SL, CD_PLANT, CD_COMPANY, CD_ITEM, YY_INV,
             LEFT(DT_IO,6) AS YM_IO, CD_QTIOTP, CD_PJT, SEQ_PROJECT,
             SUM(QT_GOOD_GR) AS SUM_GR,
             SUM(QT_GOOD_GI) AS SUM_GI
      FROM MM_OHSLINVD
      WHERE YY_INV     = '[년도]'
        AND CD_SL      = '[창고]'
        AND CD_PLANT   = '[공장]'
        AND CD_COMPANY = '[회사]'
      GROUP BY CD_SL, CD_PLANT, CD_COMPANY, CD_ITEM, YY_INV,
               LEFT(DT_IO,6), CD_QTIOTP, CD_PJT, SEQ_PROJECT
  ) d ON m.CD_SL=d.CD_SL AND m.CD_PLANT=d.CD_PLANT AND m.CD_COMPANY=d.CD_COMPANY
     AND m.CD_ITEM=d.CD_ITEM AND m.YY_INV=d.YY_INV AND m.YM_IO=d.YM_IO
     AND m.CD_QTIOTP=d.CD_QTIOTP AND m.CD_PJT=d.CD_PJT AND m.SEQ_PROJECT=d.SEQ_PROJECT
  WHERE ABS(m.QT_GOOD_GR - d.SUM_GR) > 0
     OR ABS(m.QT_GOOD_GI - d.SUM_GI) > 0

  ---
  주의사항

  ┌──────────────────────┬────────────────────────────────────────────────┐
  │         상황         │                      방법                      │
  ├──────────────────────┼────────────────────────────────────────────────┤
  │ MM_OHSLINVM만 틀어짐 │ Step 3 UPDATE (PINVN 건드리지 않음)            │
  ├──────────────────────┼────────────────────────────────────────────────┤
  │ MM_PINVN도 틀어짐    │ MM_PINVN 별도 확인 후 추가 조치                │
  ├──────────────────────┼────────────────────────────────────────────────┤
  │ 프로시저 호출로 수정 │ 금지 — 누적가산(+=) 방식이라 PINVN 이중 반영됨 │
  └──────────────────────┴────────────────────────────────────────────────┘

  ---

## ✅ 검증 및 결과

## 🔗 참고
