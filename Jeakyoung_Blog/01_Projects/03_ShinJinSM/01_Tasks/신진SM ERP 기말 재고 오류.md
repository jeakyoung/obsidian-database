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

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 신진SM 현장(재고 담당) |
| **요청일** | 2026-08-31 |
| **대상 시스템** | 더존 ERP (MSSQL) |
| **관련 화면·프로그램** | `MM_OHSLINVM`(월별 집계), `MM_OHSLINVD`(일별 상세) |

> 이 문서는 2026-08-31에 처음 발견된 개별 사례(품목 `11-38*150*155W`, 2026-07)를 다룬다. 같은 종류의 불일치를 매번 찾고 고치는 표준 절차는 09-10에 [[신진SM ERP 기말 재고 오류 ( 입 출고 내역에 이상이 없을경우 )]]로 정리됐다 — 신규 사례 대응 시 그 문서를 먼저 참고할 것.

## 🔍 현상 및 원인

더존 ERP의 월별 집계 테이블 `MM_OHSLINVM`이 일별 상세 테이블 `MM_OHSLINVD`(2026-07, `YM_IO='202607'`)의 실제 합계와 어긋나는 품목이 다수 발견됨. 최초 사례는 `11-38*150*155W`(창고 `1210`, 사업장 `2000`, 회사 `1000`, 수불형태 `983`)로, 첨부 스크린샷(`Pasted image 20260820162722.png`) 기준 규격에 `W`가 붙는 품목군에서 지속 발생 중임이 확인됨. 근본 원인은 별도로 규명되지 않았고(더존 배치 집계 로직의 이슈로 추정), MES 쪽 원인이 아니라 더존 ERP 내부 집계 문제로 파악하고 있음 — [[신진SM 개발 이력]]에서 정리한 "포장 중복→더존 재고 어긋남"(5월)과는 다른, 더존 집계 레이어의 별개 문제.

## 🔧 조치 내용

### 검증 로직 — 202607 불일치 품목 탐지

```sql

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
```

### 긴급 조치 — 해당 건만 즉시 덮어쓰기

당시 급한 건 하나만 수동으로 확정값(`3.0000`)으로 덮어쓴 임시 조치. 이 값은 별도 대사 결과로 확인된 정상값이며 임의값이 아님.

```sql
UPDATE MM_OHSLINVM
  SET QT_GOOD_GI = 3.0000
  WHERE CD_ITEM     = '11-38*150*155W'
    AND YM_IO       = '202607'
    AND CD_QTIOTP   = '983'
    AND CD_SL       = '1210'
    AND CD_PLANT    = '2000'
    AND CD_COMPANY  = '1000'
```

### 2단계 — 다음 달(8월) 기초재고 확인

7월 값을 고치면 8월 기초재고에도 영향이 있을 수 있어, 8월 행 존재 여부를 먼저 확인.

```sql
SELECT * FROM MM_OHSLINVM
  WHERE CD_ITEM    = '11-38*150*155W'
    AND YM_IO      = '202608'
    AND CD_SL      = '1210'
    AND CD_PLANT   = '2000'
```











### 확산 확인 — 단일 건이 아님

이 건 하나만 어긋난 게 아니라, 규격에 `W`가 붙는 품목군 전반에서 같은 유형의 불일치가 계속 발생하는 것을 스크린샷(`Pasted image 20260820162722.png`)으로 확인.

### 전체 일괄 정정 (스케줄링 고려 필요)

```sql
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
```

## ✅ 검증 및 결과

- [x] `11-38*150*155W` 건은 확정값으로 수동 정정 완료
- [ ] 규격에 `W`가 붙는 품목군 전체 일괄 정정 — 위 UPDATE는 준비됐으나 실행/스케줄링 여부는 이 문서 기준으로 확인 안 됨
- [ ] 더존 배치 집계 로직 자체의 근본 원인 규명 — 미착수. 발생할 때마다 정정 쿼리로 대응하는 상태가 지속되고 있음

## 🔗 참고

- [[신진SM ERP 기말 재고 오류 ( 입 출고 내역에 이상이 없을경우 )]] — 이 사례를 바탕으로 만든 표준 탐지·정정 절차
- [[신진SM 개발 이력]]
