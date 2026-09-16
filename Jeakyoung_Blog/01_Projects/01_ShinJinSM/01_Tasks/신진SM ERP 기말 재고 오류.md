---
title: 신진SM ERP 기말 재고 오류
date: 2026-08-31
type: 작업
project: 신진SM
status: 진행중
priority: 보통
assignee: []
tags: []
---

# 신진SM ERP 기말 재고 오류

## 1. 개요

| 항목 | 내용 |
|------|------|
| 요청자 |  |
| 요청일 | 2026-08-31 |
| 대상 시스템 |  |
| 관련 화면·프로그램 |  |

## 2. 현상 및 원인

## 3. 조치 내용

-> 검증로직

SELECT m.CD_ITEM, m.CD_QTIOTP, m.YM_IO,
         m.QT_GOOD_GR AS 현재_입고, d.QT_GOOD_GR AS 정상_입고,
         m.QT_GOOD_GI AS 현재_출고, d.QT_GOOD_GI AS 정상_출고
  FROM MM_OHSLINVM m
  JOIN (
      SELECT CD_SL, CD_PLANT, CD_COMPANY, CD_ITEM, YY_INV,
             LEFT(DT_IO,6) AS YM_IO, CD_QTIOTP, CD_PJT, SEQ_PROJECT,
             SUM(QT_GOOD_GR)   AS QT_GOOD_GR,
             SUM(QT_REJECT_GR) AS QT_REJECT_GR,
             SUM(QT_INSP_GR)   AS QT_INSP_GR,
             SUM(QT_TRANS_GR)  AS QT_TRANS_GR,
             SUM(QT_GOOD_GI)   AS QT_GOOD_GI,
             SUM(QT_REJECT_GI) AS QT_REJECT_GI,
             SUM(QT_INSP_GI)   AS QT_INSP_GI,
             SUM(QT_TRANS_GI)  AS QT_TRANS_GI
      FROM MM_OHSLINVD
      WHERE LEFT(DT_IO,6) = '202607'
      GROUP BY CD_SL, CD_PLANT, CD_COMPANY, CD_ITEM, YY_INV,
               LEFT(DT_IO,6), CD_QTIOTP, CD_PJT, SEQ_PROJECT
  ) d ON  m.CD_SL       = d.CD_SL
      AND m.CD_PLANT    = d.CD_PLANT
      AND m.CD_COMPANY  = d.CD_COMPANY
      AND m.CD_ITEM     = d.CD_ITEM
      AND m.YY_INV      = d.YY_INV
      AND m.YM_IO       = d.YM_IO
      AND m.CD_QTIOTP   = d.CD_QTIOTP
      AND m.CD_PJT      = d.CD_PJT
      AND m.SEQ_PROJECT = d.SEQ_PROJECT
  WHERE m.YM_IO = '202607'
    AND ABS(m.QT_GOOD_GI - d.QT_GOOD_GI) > 0



-> 급해서 해당건만 당장덮어놔야할때

UPDATE MM_OHSLINVM
  SET QT_GOOD_GI = 3.0000
  WHERE CD_ITEM     = '11-38*150*155W'
    AND YM_IO       = '202607'
    AND CD_QTIOTP   = '983'
    AND CD_SL       = '1210'
    AND CD_PLANT    = '2000'
    AND CD_COMPANY  = '1000'

  ---
  2단계. 8월 MM_OHSLINVM 기초재고 확인 후 처리

  -- 8월 행이 있는지 확인
  SELECT * FROM MM_OHSLINVM
  WHERE CD_ITEM    = '11-38*150*155W'
    AND YM_IO      = '202608'
    AND CD_SL      = '1210'
    AND CD_PLANT   = '2000'












-> 그것만 안맞고 있는게아님 규격 + W 로되어있는것들에서 지속발생중

![[Pasted image 20260820162722.png]]


-> 전체 맞추기 ( 스케쥴링 고려 )

UPDATE m
  SET
      m.QT_GOOD_GR   = ISNULL(d.QT_GOOD_GR, 0),
      m.QT_REJECT_GR = ISNULL(d.QT_REJECT_GR, 0),
      m.QT_INSP_GR   = ISNULL(d.QT_INSP_GR, 0),
      m.QT_TRANS_GR  = ISNULL(d.QT_TRANS_GR, 0),
      m.QT_GOOD_GI   = ISNULL(d.QT_GOOD_GI, 0),
      m.QT_REJECT_GI = ISNULL(d.QT_REJECT_GI, 0),
      m.QT_INSP_GI   = ISNULL(d.QT_INSP_GI, 0),
      m.QT_TRANS_GI  = ISNULL(d.QT_TRANS_GI, 0)
  FROM MM_OHSLINVM m
  JOIN (
      SELECT CD_SL, CD_PLANT, CD_COMPANY, CD_ITEM, YY_INV,
             LEFT(DT_IO,6)    AS YM_IO, CD_QTIOTP, CD_PJT, SEQ_PROJECT,
             SUM(QT_GOOD_GR)   AS QT_GOOD_GR,
             SUM(QT_REJECT_GR) AS QT_REJECT_GR,
             SUM(QT_INSP_GR)   AS QT_INSP_GR,
             SUM(QT_TRANS_GR)  AS QT_TRANS_GR,
             SUM(QT_GOOD_GI)   AS QT_GOOD_GI,
             SUM(QT_REJECT_GI) AS QT_REJECT_GI,
             SUM(QT_INSP_GI)   AS QT_INSP_GI,
             SUM(QT_TRANS_GI)  AS QT_TRANS_GI
      FROM MM_OHSLINVD
      WHERE LEFT(DT_IO,6) = '202607'
      GROUP BY CD_SL, CD_PLANT, CD_COMPANY, CD_ITEM, YY_INV,
               LEFT(DT_IO,6), CD_QTIOTP, CD_PJT, SEQ_PROJECT
  ) d
      ON  m.CD_SL       = d.CD_SL
      AND m.CD_PLANT    = d.CD_PLANT
      AND m.CD_COMPANY  = d.CD_COMPANY
      AND m.CD_ITEM     = d.CD_ITEM
      AND m.YY_INV      = d.YY_INV
      AND m.YM_IO       = d.YM_IO
      AND m.CD_QTIOTP   = d.CD_QTIOTP
      AND m.CD_PJT      = d.CD_PJT
      AND m.SEQ_PROJECT = d.SEQ_PROJECT
  WHERE m.YM_IO = '202607'
    AND ABS(m.QT_GOOD_GI - d.QT_GOOD_GI) > 0

## 4. 검증 및 결과

## 5. 참고
