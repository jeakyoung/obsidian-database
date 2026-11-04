---
title: 신진SM 포장 단독 생산 시 창고코드 오류 (미해결)
date: 2026-07-28
type: 작업
project: 신진SM
status: 보류
priority: 보통
assignee: []
tags: []
---

# 신진SM 포장 단독 생산 시 창고코드 오류 (미해결)

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 신진SM 현장 |
| **요청일** | 2026-07-28 |
| **대상 시스템** | MES |
| **관련 화면·프로그램** | WPR559(생산실적등록), `ProdSLService.java` |

> 이 문서는 07-28 회의록에서 보고된 버그를 정리한 것이다. 코드베이스를 확인한 결과(2026-09-18 기준) **아직 근본 수정이 반영되지 않았다** — 09-14 도면가공 작업([[신진SM 도면가공 체계 MES 동기화 작업]])에서 창고코드 결정 로직을 `resolvePackingWarehouseCode()`로 리팩터링했지만, 이 버그가 지적한 "이전 실적 없는 포장 단독 생성" 케이스에 대한 분기는 그 리팩터링에도 포함되지 않았다.

## 🔍 현상 및 원인

일반수주 포장(WORK_CODE=005) 저장 시 포장입고가 항상 출하창고로 생성되는 버그. 이전 공정 실적 없이 포장 단독으로 생산일보를 생성하는 경우에는 원래 제품창고로 입고되어야 하는데, 실제로는 이전 실적 유무와 무관하게 무조건 출하창고로 들어간다.

**흐름 정리**
1. 프론트(`WPR559_CT.js`)에서 WORK_CODE=005 선택 후 저장 시 `packing=1` 파라미터를 `jvWPR559_01_IUD` 서블릿으로 전송
2. `jvWPR559_01_IUD.java`에서 `packing=1`이면 `ProdSLService.processSLCrossMove()` 호출
3. 호출 전 `jvPROD_DATA_FETCH.fetchProductionPlanSecure()`가 실행되어, 해당 생산계획(PRODPLAN_DATE + PRODPLAN_SEQ)에 WORK_CODE != '005'인 이전 실적이 있으면 `SL_ETC`에 `TCO102.ETC` 값을 세팅, 없으면 null
4. `ProdSLService.java`에서 `SL_ETC == null` 여부로 분기해야 함:
   - `SL_ETC == null` → 이전 실적 없음(포장 단독) → 생산일보 + 창고이동 전체 생성 → **제품창고**로 가야 함
   - `SL_ETC != null` → 이전 실적 있음 → 포장만 처리 → 출하창고
5. **버그**: 이 분기와 무관하게 창고코드가 `plantCode` 기준으로 무조건 출하창고(`000001`→`016`, `000002`→`225`)로 하드코딩되어 있었음

## 🔧 조치 내용 (미착수)

07-28 회의에서 제시된 수정 방향:

```java
// 수정 전
String warehouseCode = "";
if("000001".equals(plantCode)) {
    warehouseCode = "016";
} else if("000002".equals(plantCode)){
    warehouseCode = "225";
}

// 수정 방향 — SL_ETC 유무로 분기
String slEtc = sanitizeInput(String.valueOf(jsonObject.get("SL_ETC")));
boolean hasPrevRecord = slEtc != null && !slEtc.isEmpty() && !"null".equals(slEtc);

if (hasPrevRecord) {
    // 이전 실적 있음 → 출하창고
    if("000001".equals(plantCode)) { warehouseCode = "016"; }
    else if("000002".equals(plantCode)) { warehouseCode = "225"; }
} else {
    // 포장 단독 → 제품창고 (TCO102 조회로 코드 확정 필요)
    if("000001".equals(plantCode)) { warehouseCode = "확인필요"; }
    else if("000002".equals(plantCode)) { warehouseCode = "확인필요"; }
}
```

선행 확인 필요(제품창고 코드 특정):

```sql
SELECT WAREHOUSE_CODE, WAREHOUSE_NAME, WORK_STATUS, ETC
FROM TCO102
WHERE FACTORY_CODE = '000001'
ORDER BY WAREHOUSE_CODE
```

### 현재 코드 상태 (2026-09-18 확인)

`ProdSLService.java`의 `resolvePackingWarehouseCode()`는 여전히 `WAREHOUSE_CODE_OVERRIDE`가 없으면 plantCode 기준 고정값(`016`/`225`)을 반환한다 — 즉 07-28에 보고된 "포장 단독 시 제품창고로 가야 한다"는 분기는 구현되지 않았고, `SL_ETC` 유무를 창고코드 결정에 반영하는 코드도 없다. 09-14 도면가공 작업은 `WAREHOUSE_CODE_OVERRIDE`라는 별도 우회 경로를 얹었을 뿐, 이 버그 자체를 고치지는 않았다.

## ✅ 검증 및 결과

미해결. 제품창고 코드 확정(TCO102 조회)도, `SL_ETC` 기준 분기 반영도 코드에 없음 — 재현 시 여전히 같은 증상(포장 단독 생성 건이 출하창고로 잘못 입고)이 발생할 것으로 예상됨.

## 🔗 참고

- [[신진SM 도면가공 체계 MES 동기화 작업]] — 같은 `resolvePackingWarehouseCode()`를 다루지만 이 버그는 고치지 않은 후속 작업
- [[신진SM 개발 이력]]
