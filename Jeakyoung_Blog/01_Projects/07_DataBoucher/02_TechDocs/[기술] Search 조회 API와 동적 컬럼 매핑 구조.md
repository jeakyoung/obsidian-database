---
title: Search 조회 API와 동적 컬럼 매핑 구조
date: 2026-09-18
type: 기술문서
project: 데이터바우처
status: 완료
category: 조회 API
assignee:
  - 안재경
tags: []
---

# Search 조회 API와 동적 컬럼 매핑 구조

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | F1Soft.Starmap.Service — Search |
| **적용 범위** | 거래처/원료/창고/용도 등 모바일 콤보·목록 조회 전반 |
| **관련 모듈** | `SearchListController`, `SearchListService` |

> 7개 조회 엔드포인트 모두 `SP_*` 실행 결과 `DataTable`을 고정 DTO 없이 `Dictionary<string, object?>`로 그대로(또는 일부만 골라서) 응답한다 — 타입 안전성보다 SP 변경에 즉시 대응하는 걸 택한 구조.

## 🎯 배경 및 요구사항

모바일 앱의 콤보박스/검색 화면(거래처, 원료, 창고, 창고 로케이션, 용도, 입고 대상·완료 거래처)에서 쓰는 조회 API들은 화면마다 필요한 컬럼 구성이 조금씩 다르고 SP 쪽 컬럼도 자주 바뀔 수 있어서, 매번 Response DTO를 새로 만들고 배포하는 대신 SP 결과를 거의 그대로 흘려보내는 방식을 택한 것으로 보인다.

## 🏗 설계 및 구현

### 엔드포인트 ↔ SP 매핑

| 엔드포인트 | SP | 비고 |
|:--|:--|:--|
| `POST CustomerList` | `SP_APP_CUSTOMER_LIST` | `CustKind`, `CustomerName` — [[01_Projects/07_DataBoucher/01_Tasks/데이터 바우처 거래처 검색 파라미터 정리 08.07]]에서 파라미터 정리됨 |
| `POST MaterialList` | `SP_APP_MATERIAL_LIST` | `ItemGbn`, `SearchItemName`, `CustomerCode` |
| `GET WarehouseList` | `SP_WCO103_01_LIST` | `FACTORY_CODE` 고정값 `"000001"` 하드코딩 |
| `POST WarehouseLocateList` | `SP_WMA662_WIN01_LIST` | `WarehouseCode` |
| `GET UsePurposeList` | `SP_WEB_STORE_COMBO_TCO101` | `CODE_ID1` 고정값 `"426"` 하드코딩 (공통 코드 콤보) |
| `POST TargetCustomerList` | `SP_APP_INPUT_TARGET_CUSTOMER_LIST` | 입고 대상(아직 등록 안 된) 거래처 |
| `POST SavedCustomerList` | `SP_APP_INPUT_SAVED_CUSTOMER_LIST` | 입고 완료 거래처 |

### 두 가지 응답 매핑 방식이 섞여 있음

```csharp
// 1) 대부분: SP DataTable 컬럼을 전부 그대로 Dictionary화 (예: GetCustomerListAsync, GetMaterialListAsync 등)
dataTable.AsEnumerable().Select(row => dataTable.Columns.Cast<DataColumn>()
    .ToDictionary(col => col.ColumnName, col => row[col] == DBNull.Value ? null : row[col]))

// 2) 일부(WarehouseList, UsePurposeList): 화이트리스트/컬럼명 리네이밍
var allowedColumns = new HashSet<string> { "WAREHOUSE_CODE", "WAREHOUSE_NAME" };
// ... allowedColumns.Contains(col.ColumnName) 로 필터링

var columnMap = new Dictionary<string, string> { { "CODE_ID2", "USE_CODE" }, { "CODE_NAME_FULL", "USE_NAME" } };
// ... columnMap[col.ColumnName] 로 리네이밍해서 응답
```

> [!warning] SP 컬럼이 그대로 API 응답에 노출되는 엔드포인트가 대부분
> `CustomerList`/`MaterialList`/`TargetCustomerList`/`SavedCustomerList`/`WarehouseLocateList`는 SP가 반환하는 컬럼을 필터링 없이 그대로 `Dictionary`에 담아 응답한다. SP를 고칠 때 컬럼을 추가/삭제하면 **API 배포 없이 응답 스펙이 바뀐다** — 클라이언트가 이 암묵적 계약에 의존하고 있다면 SP 변경 시 프론트/모바일과 반드시 컬럼 단위로 소통해야 한다. `WarehouseList`/`UsePurposeList`만 화이트리스트·리네이밍으로 응답을 고정해뒀는데, 왜 이 둘만 그렇게 했는지는 코드에 남아있지 않다.

### 하드코딩된 값

- `GetWarehouseListAsync`: `FACTORY_CODE = "000001"` 하드코딩 — 다른 엔드포인트는 요청에서 `FactoryCode`를 받는데 이것만 고정값. 멀티 공장 지원 시 누락 포인트가 될 수 있음.
- `GetUsePurposeListAsync`: `CODE_ID1 = "426"` 하드코딩 — 공통 코드 테이블에서 "용도" 그룹 코드로 보이는 매직 넘버. 어떤 코드 체계인지 주석이 없음.

## ✅ 검증

- [x] `CustomerList`/`MaterialList` 등 주요 조회가 `Dictionary<string, object?>` 형태로 정상 응답하는지 확인
- [ ] `FACTORY_CODE`/`CODE_ID1` 하드코딩이 실제로 공장 1개·용도코드 1그룹만 쓰는 현재 운영 범위에서 문제 없는지 재확인 필요 (멀티 공장 확장 시 영향)
- [ ] SP 컬럼 변경 시 클라이언트 영향 범위를 추적할 방법이 없음 — 계약 테스트나 스키마 고정이 필요한지 검토 필요

## 🔗 참고

- `Controllers/Search/SearchListController.cs`, `Services/Search/SearchListService.cs`
- [[01_Projects/07_DataBoucher/01_Tasks/데이터 바우처 거래처 검색 파라미터 정리 08.07]]
- [[01_Projects/07_DataBoucher/02_TechDocs/[기술] 입고(Input) 등록과 임베디드 이미지 동시 저장 (InputSaveService)]] — 같은 `Dictionary` 동적 응답 패턴을 `InputListController`에서도 사용
