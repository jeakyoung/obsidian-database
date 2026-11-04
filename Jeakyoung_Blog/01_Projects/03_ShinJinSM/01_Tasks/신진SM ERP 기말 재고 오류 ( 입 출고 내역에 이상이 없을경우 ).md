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
| **요청자** | 신진SM 현장(재고 담당) |
| **요청일** | 2026-09-10 |
| **대상 시스템** | 더존 ERP (MSSQL) |
| **관련 화면·프로그램** | `MM_OHSLINVM`(월별 집계), `MM_OHSLINVD`(일별 상세), `MM_PINVN`(연간 집계) |

> 제목의 "입·출고 내역에 이상이 없을 경우"는 `MM_OHSLINVD`(일별 상세)와 `MM_PINVN`(연간 집계)은 정상인데 `MM_OHSLINVM`(월별 집계)만 틀어진 케이스를 가리킨다. [[신진SM ERP 기말 재고 오류]](08-31, `11-38*150*155W` 사례)에서 처음 발견한 문제를 겪고 나서, 같은 유형이 반복될 걸 대비해 09-10에 일반화한 표준 탐지·정정 절차 문서.

## 🔍 현상 및 원인

더존 ERP의 3단 재고 집계 구조(일별 `MM_OHSLINVD` → 월별 `MM_OHSLINVM` → 연간 `MM_PINVN`)에서 중간 단계인 월별 집계만 하위 집계와 어긋나는 경우가 반복적으로 발생. 정확한 근본 원인(더존 배치 집계 타이밍 문제로 추정)은 규명되지 않았고, 이 문서는 "왜 틀어지는가"가 아니라 "틀어졌을 때 안전하게 찾고 고치는 방법"을 표준화한 것이다.

## 🔧 조치 내용

### 전제 조건

- `MM_OHSLINVD` (일별 상세) = 정상
- `MM_PINVN` (연간 집계) = 정상
- `MM_OHSLINVM` (월별 집계) = 틀어진 상태

### Step 1. 불일치 품목 전체 탐지

`MM_PINVN`(연간, 신뢰 기준)과 `MM_OHSLINVM`(월별, 검증 대상)을 대사해서 차이가 있는 품목을 먼저 찾는다.

```sql
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
```

### Step 2. 특정 품목의 틀어진 월/QTIOTP 확인

Step 1에서 나온 품목에 대해, `MM_OHSLINVD`(일별, 신뢰 기준)를 월/수불형태(`CD_QTIOTP`) 단위로 집계해서 `MM_OHSLINVM`과 정확히 어느 월·어느 수불형태에서 차이가 나는지 좁힌다.

```sql
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
```

### Step 3. MM_OHSLINVM 수정

**단일 품목 수정** (Step 2 결과 보고 수동 지정):

```sql
UPDATE MM_OHSLINVM
  SET QT_GOOD_GR = [D_GR값],
      QT_GOOD_GI = [D_GI값]
  WHERE CD_ITEM    = '[품목코드]'
    AND YM_IO      = '[년월]'
    AND CD_QTIOTP  = '[수불형태]'
    AND CD_SL      = '[창고]'
    AND CD_PLANT   = '[공장]'
    AND CD_COMPANY = '[회사]'
```

**불일치 전체 일괄 수정** (일별→월별 동기화):

```sql
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
```

### 주의사항

| 상황 | 방법 |
|:--|:--|
| `MM_OHSLINVM`만 틀어짐 | Step 3 UPDATE (`MM_PINVN`은 건드리지 않음) |
| `MM_PINVN`도 틀어짐 | `MM_PINVN` 별도 확인 후 추가 조치 |
| 프로시저 재실행으로 수정 | **금지** — 더존 수불 프로시저는 누적가산(`+=`) 방식이라, 이미 반영된 데이터에 다시 실행하면 `MM_PINVN`이 이중 반영됨 |

## ✅ 검증 및 결과

이 절차 자체는 09-10 시점 정리된 가이드이며, 이후 실제로 몇 건에 적용됐는지·자동화(스케줄러화) 여부는 이 문서 기준으로는 확인되지 않음. 신규 사례 발생 시 이 문서의 Step 1~3을 그대로 따라가면 됨.

## 🔗 참고

- [[신진SM ERP 기말 재고 오류]] — 이 절차의 계기가 된 최초 사례(08-31, `11-38*150*155W`)
- [[신진SM 개발 이력]]
