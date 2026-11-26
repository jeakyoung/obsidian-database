---
title: Spring API 명세 및 원본 업무 연결
date: 2026-11-26
draft: true
---

# Spring API 명세 및 원본 업무 연결

### 003·103 완료와 동시 자재 명령

`POST /api/pop/work-baskets/commands`의 FINISH_BASKET은 그룹 전체 지시의 실적을 확정한다. 이후 오래된 버전의 편집은 409 STALE_REVISION이다. 같은 단말의 두 사원이 서로 다른 세션을 사용해, 완료 뒤 현재 버전으로 개별·일괄삭제, 자재 추가·행 삭제·탭 초기화, 반납수량·전체 반납행 저장 및 재완료를 시도했을 때 모두 409이고 그룹의 실원장은 그대로임을 확인했다. 성공한 완료 명령을 원래 사원이 같은 요청 ID로 재전송하면 기존 응답을 반환하며 다른 사원이 ID를 재사용하면 403이다. 앱은 재조회한 실원장의 최종 반납 건수와 수량을 표시한다. 작업자에게 노출되는 다음 스캔은 잔량 0일 때 ORDER_FINISHED를 반환한다. [인수표와 재현 명령](file:///E:/ajk/devgit/shinjin/.team/screen-review/basket-completed/인수.md)

### 003·103 중첩 위치 스캔과 기존 반납행의 프리셋 취소

`POST /api/pop/work-baskets/stock-picker/{date}/{sequence}/location`의 위치 응답은 수동창의 위치 코드·이름에 적용한다. 성공 또는 닫기 후 같은 창의 `/stock`을 다시 조회하며 003·103은 원본대로 위치 필터를 전달하지 않는다. 인라인 LOT의 미완성 바코드, 오른쪽 선택수량과 입력 포커스는 클라이언트가 보존한다. 003·103용 별도 ComMaterialNoScan 요청은 없다.

기존 양수 길이 셀에서 ComNumericKeyPad3을 취소하면 `/return-lookup`에 기존 길이와 현재 반납행의 규격을 보낸다. 구 데이터셋에서 `line.material`이 비어 있어도 현재 작업 원장 `productionReturns[].material`을 같은 순번·LOT로 찾아 사용한다. 원본 품목 재조회는 품목코드만 다시 결정하므로 기존 LOT·창고/위치 이름·표시 재질·치수는 보존한다. 그룹 저장 및 재조회 시점은 `SAVE_RETURN_GRID` 계약과 같다.

### 003·103 그룹 해제 후 부모 수주목록

`GET /api/pop/work-baskets/parent?order=<수주번호>&detail=<고객규격>`은 그룹 양쪽 자재가 모두 비었을 때 호출한다. 세션과 선택한 슬롯·공정의 동일 시점 스냅샷 `view`와 원본 순서의 `keys`를 반환한다. 네 자리 고객규격이 빈 값이면 같은 수주 전체를 대상으로 한다. 서버는 배정된 계획키로 범위를 제한하고 클라이언트는 현재 부모 화면에서 이미 삭제한 계획키를 제외한다.

합성 응답은 `basket-scans.json`의 수주·고객규격·계획키에 정의한 `remainingWork`를 사용한다. 원본 SELECT2_GV1의 최종 미완료 수량 조건에 해당하며 0인 행은 제외한다. 수량이 없는 구형 스캐너 전용 데이터셋은 `keys: null`을 반환해 기존 부모 목록을 유지한다. 명시적인 빈 결과는 `keys: []`이다. 접속한 단말의 003/103 공정 헤더 없이 호출하면 403이다. 단순 닫기·실패·한 탭에 자재가 남은 경우에는 이 부모 조회를 호출하지 않는다.

### 003·103 반납행 추가·길이 입력

`POST /api/pop/work-baskets/return-lookup/{date}/{sequence}`는 선택한 슬롯·공정 헤더와 로그인 세션으로 포커스 수주를 찾는다. `firstPlan`, `firstIssue`, `focusedIssue`에 각각 첫 수주 키와 첫 투입·포커스 투입 LOT의 네 키를 보낸다. 길이를 생략한 요청은 원본 GV3_SELECT2에 해당한다. 응답은 창고·위치·재질명·재질코드·두께·폭·길이 0과 빈 품목/LOT를 담은 배열이다. 길이 적용은 같은 경로에 `length`, `position`, 기존 `row`를 보내는 GV3_SELECT1이다. 최초 등록 후 포커스를 다른 투입행으로 바꿔도 기존 반납행의 두께와 폭으로 품목을 조회한다.

응답 데이터는 `shinjin.demo.basket-return-lookup`에서 지정할 수 있다. 기본 파일은 `demo/basket-return-lookup.json`이다. 단말·반납창고·입출품목·수주/투입 작업상태·재질·규격·품목 구분과 합성 입력에 맞춘 창고/위치·품목 응답을 지정한다. API가 조회한 반납 규격은 같은 로그인 세션과 단말·작업자·슬롯·공정·수주에 묶는다. 선택 수주나 투입 근거가 없으면 404/422, 적용된 반납창고가 비면 409다.

`POST /api/pop/work-baskets/commands`의 `SAVE_RETURN_GRID`는 `visible=[포커스 수주 키]`, `groupId`, `expectedRevision`, `requestId`, `returns` 배열을 받는다. 각 반납행에는 LOT 키, 수량, 길이, 조회한 규격과 `sequence`가 있다. 그룹의 기존 행 또는 세션에서 확보한 규격을 재검증하고, 행 순서대로 순번 0에 새 순번을 부여한 뒤 전체 실반납 목록을 한 번에 갱신한다. 이미 사용한 순번과 충돌하거나 버전이 바뀌면 409이며, 단일 요청 재시도는 처음의 결과를 반환한다. 조회에 사용한 숫자 키패드는 [[22-003-103-장바구니와-미완료-작업-삭제]]에 기록했다.

### 003·103 부모 그리드의 선택 자재 삭제

`POST /api/pop/work-baskets/commands`는 `REMOVE_ISSUE_ROWS`와 `REMOVE_RETURN_ROWS`를 받는다. 로그인 세션, 현재 공정 슬롯·코드 헤더, `groupId`, 수주목록의 `visible`, `requestId`, `expectedRevision`을 검증한다. `removal.rows`는 화면 행 순서대로 보낸 MAT_SEQ이고 `removal.checked`는 그중 선택한 0부터 시작하는 행 인덱스다. 예를 들어 `{"rows":[2,4,5],"checked":[0,2]}`는 2·5번을 지우고 4번의 순번과 수량을 보존한다. 서버는 화면이 보낸 창고·LOT를 삭제 키로 사용하지 않는다.

저장 전 그룹의 `issueSequences`·`returnSequences`는 임시 자재 목록에 대응한다. 작업 중 목록은 `productionIssues[].sequence`·`productionReturns[].sequence`로 복원한다. 부모 GRID에 새로 붙은 순번 0은 원본 DELETE에서 원장 일치행이 없어 화면만 제거한다. 시작 전 수동 추가가 별도로 작성한 작업 원장과 임시 원장을 구분한다. 수주목록에 완료가 섞이거나 버전 충돌·마지막 투입 전체 선택이면 409, 013 반납창고 선택은 422, 공정 불일치는 403이다. 같은 작업자의 같은 요청 ID·본문에는 첫 결과가 반환된다. 동작 근거는 [[22-003-103-장바구니와-미완료-작업-삭제]]에 있다.


[[29-운영-POP-기능명세]]와 함께 사용한다. 아래 경로는 로컬 소스의 Spring MVC 매핑이다. demo 프로필의 상태 변경은 검증용이며 운영 DB 반영을 뜻하지 않는다. 요청 필드·검증값은 연결된 컨트롤러의 DTO가 기준이다.

## 주요 계약

| 업무 | 요청·응답 및 오류 | 기존 업무와의 연결 |
| --- | --- | --- |
| 작업자 세션 | POST /api/pop/session은 단말·입력 방식·작업자 식별값을 검증한다. 세션 복원은 GET, 로그아웃은 별도 POST다. 보호된 업무는 만료 시 401을 반환한다. | frmLogin과 frmMain의 로그인·로그아웃 |
| 작업지시 | 계획일과 순번으로 상세 조회. 변경은 action별 유효 상태·권한·수량을 확인한 뒤 결과와 이력을 조회한다. | frmProcess1의 작업지시 선택, 실적, 투입·반납 |
| 단말 설정 | 경로의 terminalId와 세션 단말을 대조한다. GET은 저장값과 적용값을 제공한다. PUT은 수정 가능한 사용자와 버전을 확인한다. POST refresh는 현재 세션에 설정을 반영한다. | frmSetting 및 하위 설정 창 |
| 그룹·008 | 단말/작업자 범위에서 명령을 처리한다. 008의 불확정 응답은 저장된 요청 키·본문으로 재시도한다. 확정 거절과 응답 유실의 처리 경로가 다르다. | frmProcess5·frmProcess7·frmProcess6 |
| 계획 출력 | 미리보기는 출력 횟수를 바꾸지 않는다. 실행은 선택 계획·버전·요청 키에 따라 횟수와 PDF를 반환한다. | 계획 단일·복수 인쇄 및 재출력 |

## 컨트롤러별 경로

### TerminalSettingsDemoController

소스 `src/api/src/main/java/com/shinjin/pop/admin/TerminalSettingsDemoController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/admin/terminal-settings/{terminalId}` | `read` |
| PUT | `/api/pop/admin/terminal-settings/{terminalId}` | `save` |
| PUT | `/api/pop/admin/terminal-settings/{terminalId}/printers` | `savePrinters` |
| POST | `/api/pop/admin/terminal-settings/{terminalId}/refresh` | `refresh` |

프린터 저장은 `expectedVersion`과 `outputs` 객체를 받는다. `document`, `shipment`, `label` 세 역할에 단말 등록 장치를 지정한다. 한 장치가 여러 역할을 담당할 수 있다. 저장 응답은 `code`와 `view`에 저장·세션 적용 버전을 반환한다. 미등록 장치는 400, 편집 권한과 타 단말 접근은 403, 버전 충돌은 409다.

### BasketDemoController

소스 `src/api/src/main/java/com/shinjin/pop/basket/BasketDemoController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/work-baskets` | `view` |
| GET | `/api/pop/work-baskets/groups/{groupId}` | `group` |
| POST | `/api/pop/work-baskets/commands` | `command` |

그룹 상세 조회는 로그인 세션에 배정된 작업센터와 단말의 미시작 그룹만 반환한다. 응답에는 revision, group의 투입·반납 행, 예약 반영 재고 materials, 표시명과 규격 displayLots가 있다. 팝업을 열거나 탭을 전환할 때 조회한다.

탭 초기화는 기존 명령 API에 `CLEAR_BASKET_ISSUES` 또는 `CLEAR_BASKET_RETURNS`, requestId, expectedRevision, groupId와 visible에 클릭한 지시 키 1개를 보낸다. selected·issues·returns는 빈 배열이다. 다른 탭에 행이 남으면 응답 groupId가 유지되며 affected가 빈 배열이다. 마지막 행이 제거되면 groupId가 null이 되고 affected에 그룹이 해제된 지시 키가 담긴다. 동일 요청 재전송은 첫 결과를 반환한다. 변경된 버전·작업 시작·그룹 불일치·빈 탭이면 409, 범위 밖 작업은 403 또는 404, 잘못된 명령은 422이다.

작업 중 반납수량 편집은 같은 POST 경로에 `action=SET_RETURN_QUANTITY`, requestId, 셀을 열었을 때의 expectedRevision, groupId, 전체 조회 목록의 visible 지시 키와 `returnEdit={sequence,quantity}`를 보낸다. selected·issues·returns는 빈 배열이다. 해당 단말의 시작된 그룹과 자재순번이 대상이다. 그룹과 임시 투입·반납 목록을 유지하며 작업 중 반납 목록 전체의 수정 이력을 원자적으로 갱신한다. 성공은 200과 새 revision이다. GET으로 다시 읽은 `groups[].productionReturns`에 수량·규격·순번·반납일·등록자·수정자·시각이 있다. 등록 전/완료 포함과 버전 충돌은 409, 누락된 행은 404, 입력 범위 초과·규격 미확인은 422이다. 원본 조회 분기는 `SP_POP_REG_PROCESS3_01_LIST`의 SELECT_GV3이다.

### DrawingController

소스 `src/api/src/main/java/com/shinjin/pop/drawing/DrawingController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/drawing-008/plans` | `plans` |
| GET | `/api/drawing-008/groups` | `groups` |
| GET | `/api/drawing-008/groups/{id}` | `group` |
| POST | `/api/drawing-008/groups/{id}/commands` | `groupCommand` |
| GET | `/api/drawing-008/active` | `active` |
| GET | `/api/drawing-008/plans/{*path}` | `get` |
| POST | `/api/drawing-008/plans/{key}/scan` | `scan` |
| POST | `/api/drawing-008/plans/{key}/commands` | `execute` |

스캔과 명령은 `{factory}/{site}/{date}/{seq}` 형태의 복합 키 경로도 받는다. 스캔은 `decision`에 따라 `accepted`, `scanToken`, 투입 후보 `materials`를 반환한다. 화면에서 작업일과 순번을 인증된 지시 목록에 대조하고 선택 계획의 키를 전송한다. 단건 명령은 `action`, `expectedVersion`, `requestId`와 동작별 LOT·수량·투입 행을 사용한다. 그룹 명령은 계획별 버전과 수량을 `members`로 전송한다. 재시도는 최초 요청 키와 본문을 유지한다. 원본 스캔·완료 조건과 남은 항목은 [[34-생산-보고서-기능명세]]에 있다.

### FinalProductionReportController

소스 `src/api/src/main/java/com/shinjin/pop/drawing/FinalProductionReportController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/production-report` | `find` |

### HealthController

소스 `src/api/src/main/java/com/shinjin/pop/health/HealthController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/health/live` | `live` |

### DemoSessionController

소스 `src/api/src/main/java/com/shinjin/pop/history/DemoSessionController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| POST | `/api/pop/session` | `login` |
| GET | `/api/pop/session` | `session` |
| POST | `/api/pop/session/logout` | `logout` |

### WorkHistoryController

소스 `src/api/src/main/java/com/shinjin/pop/history/WorkHistoryController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/context` | `context` |
| GET | `/api/pop/work-history` | `workHistory` |

### InventoryDemoController

소스 `src/api/src/main/java/com/shinjin/pop/inventory/InventoryDemoController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/inventory-moves` | `list` |
| POST | `/api/pop/inventory-moves/commands` | `command` |
| POST | `/api/pop/inventory-moves/documents` | `document` |

`GET`은 로그인한 작업자·단말의 범위에서 버전, 이동 가능 여부, 위치, 현재 잔량, 이동 이력, 전표 헤더/상세 ID, 서버의 오늘 날짜와 표시용 카탈로그를 반환한다. `catalog.inputWarehouses`와 `auxiliaryWarehouses`는 단말별 투입창고와 보조창고다. 선택한 헤더로 상세를 열 때 다시 조회한다. 기존 단건 MOVE/CANCEL과 미결 재시도는 `/commands`로 복구하며 단건 이동도 웹 전표 목록에 나타난다.

합성 전표 저장 요청 예시다. 버전은 직전 GET의 값으로, requestId는 새 요청마다 고유한 값으로 바꾼다. 작업자·단말·공장은 세션에서 구한다.

```json
{"action":"SAVE","requestId":"move-example-001","expectedVersion":0,"destinationSite":"SITE-NORTH","warehouse":"BIN-B","lines":[{"lot":{"item":"ITEM-X","lot":"LOT-X"},"source":{"warehouse":"BIN-A","position":"A-01"},"rowDestination":{"warehouse":"BIN-B","position":"B-02"},"quantity":"2"}]}
```

- 저장은 각 행의 출발잔량과 확정 위치를 검증하고 전표번호·요청번호·상세·잔량을 함께 확정한다. 전표번호와 요청번호는 각각 공장과 날짜 단위의 `yyyyMMdd+4자리`다. 응답은 `{version,documentNo}`다. 수량은 0 이상의 정수이며 같은 창고는 422, 부족 재고는 409다. 원본 헤더 창고와 행 위치 바인딩에 따라 최종 조합이 합성 단말의 등록 위치에서 벗어나면 403 `LOCATION_OUT_OF_SCOPE`다.
- 삭제 요청은 `{action:"DELETE_LINES",requestId,expectedVersion,documentNo,selectedIds:[이동ID]}`다. 체크한 상세 전체를 처리할 수 있을 때만 재고를 되돌린다. 일부 삭제 시 기존 documentNo를 반환하고 전부 삭제하면 null이다. 상세의 취소 감사이력은 남는다.
- 같은 작업자와 단말이 같은 요청을 다시 보내면 최초 버전과 결과를 그대로 반환한다. 같은 ID로 내용을 바꾸면 409 `REQUEST_ID_REUSED`, 다른 작업자가 해당 영수증을 사용하면 403이다. 다른 요청 두 건의 버전이 같으면 하나만 커밋하고 나머지는 409 `STALE_VERSION`이다. 실패한 일괄 요청은 잔량·상세·번호를 소비하지 않는다.
- 원본 근거는 `POPLGS/frmLogistics5.cs`의 `btnApply_Click`·`btnDelete_Click`·`FnStockCall`·`FnOutputCall`이다. `SP_POP_LGS_LOGISTICS5_01_LIST`와 `_02_LIST` 결과에 대한 합성 투영을 사용한다. 배포 SP의 JOIN·제약 및 운영 검증 범위는 [[33-물류-RFID-관리-인쇄-기능명세]]의 frmLogistics5 절에 기록했다. 운영 MSSQL 연결 없이 `shinjin.demo.inventory-catalog`로 조회용 데이터셋을 교체한다.

### ManagementDemoController

소스 `src/api/src/main/java/com/shinjin/pop/management/ManagementDemoController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/management/expendables/catalog` | `catalog` |
| GET | `/api/pop/management/expendables/recent` | `recent` |
| GET | `/api/pop/management/expendables/history` | `history` |
| POST | `/api/pop/management/expendables/issues` | `issue` |
| GET | `/api/pop/management/expendables/returns` | `returns` |
| POST | `/api/pop/management/expendables/returns` | `returnStock` |
| GET | `/api/pop/management/repairs` | `repairs` |

### SyntheticOutputController

소스 `src/api/src/main/java/com/shinjin/pop/output/SyntheticOutputController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/demo/output` | `examples` |
| GET | `/api/demo/output/{id}/{step}` | `preview` |
| GET | `/api/demo/output/{id}/{step}/pdf` | `download` |

### PlanningDemoController

소스 `src/api/src/main/java/com/shinjin/pop/planning/PlanningDemoController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/planning` | `list` |
| POST | `/api/pop/planning/commands` | `command` |
| GET | `/api/pop/planning/followups` | `followups` |
| POST | `/api/pop/planning/management` | `management` |
| POST | `/api/pop/planning/batch` | `batch` |

### PlanningOutputController

소스 `src/api/src/main/java/com/shinjin/pop/planning/PlanningOutputController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| POST | `/api/pop/planning/output/preview` | `preview` |
| POST | `/api/pop/planning/output/execute` | `execute` |

### ProcessGroupController

소스 `src/api/src/main/java/com/shinjin/pop/processgroup/ProcessGroupController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/process-group-demo` | `find` |
| POST | `/api/pop/process-group-demo` | `apply` |

두 메서드는 단말에 배정된 프로필을 경로 마지막에 지정할 수도 있다. GET은 설정, revision, 대기·시작 목록, 실적을 반환한다. POST는 `revision`, `action`(START 또는 FINISH), 선택 계획별 `lines`를 받는다. 타 단말·프로필 접근은 403, 오래된 revision은 409, 중복 선택·수량 오류는 422다.

### ProcurementDemoController

소스 `src/api/src/main/java/com/shinjin/pop/procurement/ProcurementDemoController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/procurement/sources` | `list` |
| GET | `/api/pop/procurement/sources/{type}/{number}` | `get` |
| GET | `/api/pop/procurement/balances` | `balances` |
| POST | `/api/pop/procurement/sources/{type}/{number}/receipts` | `receive` |

### RfidDemoController

소스 `src/api/src/main/java/com/shinjin/pop/rfid/RfidDemoController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/rfid/photos` | `photoEvents` |
| POST | `/api/pop/rfid/photos/events/{eventId}` | `attachPhoto` |
| GET | `/api/pop/rfid/photos/samples/{sampleId}` | `photoSample` |
| GET | `/api/pop/rfid` | `view` |
| POST | `/api/pop/rfid/commands` | `apply` |

### ShippingDemoController

소스 `src/api/src/main/java/com/shinjin/pop/shipping/ShippingDemoController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/shipping` | `list` |
| POST | `/api/pop/shipping/commands` | `command` |
| GET | `/api/pop/shipping/{number}/print-jobs` | `jobs` |
| GET | `/api/pop/shipping/{number}/document` | `preview` |
| GET | `/api/pop/shipping/{number}/document/pdf` | `download` |

### TransferDemoController

소스 `src/api/src/main/java/com/shinjin/pop/transfer/TransferDemoController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/transfers` | `get` |
| POST | `/api/pop/transfers/commands` | `command` |

### WorkOrderController

소스 `src/api/src/main/java/com/shinjin/pop/workorders/WorkOrderController.java`

| 메서드 | 경로 | Java 핸들러 |
| --- | --- | --- |
| GET | `/api/pop/work-orders` | `list` |
| GET | `/api/pop/work-orders/{planDate}/{planSequence}` | `detail` |
| POST | `/api/pop/work-orders/{planDate}/{planSequence}/actions` | `apply` |

데모 관리자 스캔 로그인은 POST /api/pop/session에 현재 단말 ID, method=scan, identifier=0000을 보낸다. 서버는 해당 단말에 배정된 관리자 샘플 계정으로 세션을 생성한다. 단말 또는 배정 계정이 없으면 401을 반환한다.

### DrawingOrderScanController

POST `/api/drawing-008/order-scan`은 `barcode`와 현재 그리드에 표시한 계획 키 목록 `listed`를 받는다. 인증 범위는 서버가 세션에서 가져온다. 성공 응답은 새 계획의 `key`, `material` 목록이며 모두 중복이면 빈 배열이다. 형식 오류 400, 세션 만료 401, 알 수 없는 수주·품목재질 또는 일반 수주 404, 단말 등록 재질·현재 그리드 재질 불일치 422를 반환한다. 조회는 생산 상태를 변경하지 않는다. 각 계획의 시작용 스캔 토큰은 기존 계획별 scan 요청을 통해 발급한다. 데모 리소스를 바꾸려면 `shinjin.demo.drawing-orders`에 Spring 파일 리소스를 지정한다.

출하 명령 CONFIRM의 `printChecked`는 커밋 뒤 거래처 발송 구분에 따라 Printer2 출력을 결정한다. 수동 REPRINT는 미리보기 응답 헤더 `X-Preview-Printer`의 장치를 `previewPrinter`로 전달한다. 같은 요청 키·본문의 재시도는 중복 제출을 억제한다. GET print-jobs의 `calls`와 `results`는 인증된 해당 전표의 합성 호출 및 출력 결과다.

## 합성 사원번호 바코드·QR

demo 프로필의 기본 경로는 `/api/demo/employee-print`이다. 모든 응답에 no-store를 적용한다. 모든 API는 로그인 세션이 필요하고, 입장 성공 뒤에는 같은 세션의 `X-Employee-Entry` 헤더도 필요하다. 추가 승인값은 화면 메모리에만 있고 메뉴 복귀 시 폐기한다. 새 승인은 이전 승인을 대체한다.

| 메서드와 경로 | 입력과 의미 |
|---|---|
| POST /entry | JSON password를 검증한다. 성공 시 entry와 사업장 목록, 미설정·불일치 시 403. 인증 전 401. |
| DELETE /entry | 해당 승인을 폐기한다. |
| GET /employees | plant, department 쿼리. 선택 사업장의 departments와 employees를 반환한다. 부서 생략 또는 전체 코드면 전체 사원이다. |
| POST /preview | plant, department, ids, form(QR 또는 BARCODE). 현재 명단의 중복 없는 선택을 서버에서 검사한다. 문서 id, pages, printer, printKey를 반환한다. 미리보기 시 출력은 0회다. |
| GET /preview/{id}/{page} | 1부터 시작하는 서버 생성 A4 페이지 SVG. 현재 승인·문서 소유 확인 후 전달한다. |
| POST /preview/{id}/print | key와 선택적 copies를 받는다. 응답은 key, printer, pages, copies, nextKey다. Quick Print는 원본처럼 copies 인수를 생략한다. 같은 키·본문 재전송은 직전 접수 결과를 반환한다. 같은 키로 부수를 바꾸거나 이전 키를 재사용하면 409다. |
| DELETE /preview/{id} | 미리보기 문서와 현재 출력 키를 닫는다. 화면 체크 선택에는 영향을 주지 않는다. |

잘못된 선택/매수는 400, 만료된 로그인은 401, 추가 승인 누락·불일치는 403, 다른 문서나 페이지는 404, Printer1 미등록·빈 값 또는 미리보기 이후 적용 장치 변경 시 출력은 422(접수 없음), Code128로 인코딩할 수 없는 사번은 422다. 부서·사원·Printer1은 서버 자료를 사용한다. 사원 조회 원본 SP_POP_OPMAN_BARCODE의 입력은 @DIVISION, @PLANT_CODE, @Department_Code다. 데모는 별도 JSON을 사용한다. 원본 SP_POP_PASSWORD는 첫 행을 비교하는 호출부만 조사했다. 이 API는 두 SP 모두 호출하지 않는다.


## 일반 포장과 설비·그룹의 합성 계약

* GET /api/pop/packing은 서버 세션의 공정·사업장 범위와 적용 재질로 수주를 조회한다. GET /api/pop/packing/stock?key=…는 해당 지시의 LOT·창고·위치별 후보를 반환한다. 같은 LOT가 여러 위치에 존재할 수 있다.
* POST /api/pop/packing/commands는 requestId, operatorId, action, members 및 autoLabel을 받는다. 각 member는 지시 key, version과 pieces를 가진다. 완료 pieces에는 lot, qty, warehouse, location, item이 있다. 전체 대상의 버전·재고 검사를 마친 후 일괄 반영한다. 중복 키에 동일한 본문은 기존 rows·labels 결과를 반환한다. 401 세션 만료, 403 범위 밖과 422 위치 불명·누적 과량은 데모에서 확인했다.
* GET /api/pop/admin/terminal-settings/{terminalId}/equipment는 scope에 맞는 설비·공정·창고, saved 및 로그인 당시 applied를 반환한다. PUT 하위 경로 /machines, /add, /remove, /processes, /assign은 expectedVersion을 검사한다. 일반 작업자는 읽기 가능, 변경은 해당 단말 관리자 권한이 필요하다. 공장·사업장별 공유 버전 경합은 409이며 신규 로그인 시 단말 사본을 적용한다. 공정 순번/창고와 역할은 현재 진행 작업에 소급하지 않는다.
* 사원번호 출력 API는 합본 Spring에 반영했다. 추가 사번으로 조합한 두 양식, 미등록 Printer1 거절은 검증했다. 검색·그리드·도구막대 UI는 담당자의 별도 검토본이며 공용 화면 승인을 기다린다.


## 생산 작업지시와 두 PLAN 진입점

| 경로 | 입력과 결과 |
| --- | --- |
| GET /api/pop/work-orders/production | 단말 지시의 계획 일자·순번, 실적량·작업그룹·버전·시작 시각을 반환한다. 원본 표시 열은 /api/pop/work-orders의 display로 읽는다. |
| POST /api/pop/work-orders/production | requestId, action, selected의 행별 date·sequence·revision·good, 선택적 autoPrint. 전체 행을 검증해 START·PAUSE·RESUME·COMPLETE를 적용한다. 완료 응답은 printStatus와 device를 포함한다. 동일 명령의 재전송은 이전 결과를 돌려준다. |
| POST /api/pop/work-orders/remove | requestId, visible, selected로 보이는 목록과 제거 대상을 검증한다. 제거된 미완료 지시는 다시 스캔할 수 있다. |
| POST /api/pop/work-orders/{planDate}/{planSequence}/scan | 기존 지시 또는 보관된 지시의 계획 키로 조회·복귀한다. 없는 키는 404다. |
| POST /api/pop/work-orders/{planDate}/{planSequence}/materials/remove | revision, action과 selected 기록번호로 투입·반납 내역을 검증 후 취소한다. |
| GET /api/pop/process1/planning | 세션의 계획 원장, 필터 선택지, 원주문·자재 키, 발행 수주별 인쇄횟수와 부모 재질을 반환한다. 운영 _01_LIST·_02_LIST 결과는 별도 합성 자료로 재현한다. |
| POST /api/pop/process1/planning/publish | requestId·expectedRevision·rows. 원주문 또는 대상 계획과 원자재 LOT·창고·위치를 검증해 역발행·규격 변경을 일괄 저장한다. 003·103은 parentPlans에 실제 보이는 부모 지시의 일자·순번을 보내며 서버가 자기 단말에서 재질 코드를 다시 읽는다. 미등록 부모 키는 404, 다른 재질은 409다. |
| POST /api/pop/process1/planning/administrator 및 /management | 관리자 암호 확인은 현재 세션의 단말·작업자에게만 유효하다. 이후 규격·창고·수량으로 관리계획을 확정한다. |
| POST /api/pop/process1/planning/attach | requestId·expectedRevision·plans. 실제 반영한 키와 건너뛴 사유를 반환한다. 완료 건 재발행은 원주문 잔량으로 새 키를 생성한다. 동일 요청 재시도는 기존 영수 결과를 돌려준다. |
| POST /api/pop/process1/planning/output | requestId·expectedRevision·selection(site, mode, plans). 단일 양식은 체크한 모든 행, 다중 양식은 같은 발행 수주만 허용한다. 적용된 문서 프린터·생성 PDF·출력 행을 돌려주며 동일 재시도는 출력횟수를 늘리지 않는다. |

003·103의 /api/pop/work-baskets/commands는 PAUSE_BASKET, RESUME_BASKET, FINISH_BASKET, DELETE_ROW도 처리한다. 완료량은 amounts에 계획 키와 수량을 묶어 보내며 그룹·작업 단계와 버전을 재검사한다. 위 경로는 demo 프로필에서 합성 원장을 사용한다. 운영 프로시저·실제 프린터·ERP 후속 기록은 연결 전 대사 대상이다.

## 공용 헤더 서버 시계

GET /api/pop/workplace/time은 POP 세션을 요구하고 date1 문자열 하나와 Cache-Control: no-store를 반환한다. 원본 frmMain.cs 651–670의 SP_POP_MAIN_GETDATE_LIST 결과를 그대로 표시하는 계약이다. demo 서버는 한국시간 예시 yyyy-MM-dd HH:mm:ss를 공급한다. 운영 SP 형식은 미확인이다. 401 및 서로 다른 브라우저 시간대/날짜 형식의 원문 전달을 검증했다.

## 008 일반 반납과 중단

`POST /api/drawing-008/plans/{key}/commands`의 DRAW_PAUSE·DRAW_RESUME는 현재 단말·예상 버전·요청 식별자를 검사하며 중단 상태에서 DRAW_FINISH는 409다. DRAW_FINISH의 returns는 창고·로케이션·재질과 두께·폭·길이·수량을 받는다. 반납 규격은 양수이며 설정과 다른 창고·재질은 422, 취소와 검증 실패 시 기존 투입·작업기록은 유지된다. 일반 반납은 완료 때 1회 저장되며 `GET /api/drawing-008/plans/{key}/audit`에 returns로 반환한다. 그룹 반납, 실 ERP 재고·라벨 연동은 후속이다. 근거 POPREG/frmProcess7.cs 2449, 2664, 4571, 9490. 15177에서 메뉴·초 갱신 및 작업 진입, 같은 빌드의 격리 Chrome에서 단건 완료·취소·중단 검증.

### 008 체크 작업 명령

`POST /api/drawing-008/work-grid/commands`는 명령 식별자와 각 계획 키·예상 버전을 받는다. 첫 DRAW_START에서는 행별 스캔 토큰과 투입 수량을 검증해 그룹을 생성한다. 이후 같은 그룹의 DRAW_PAUSE, DRAW_RESUME, DRAW_FINISH는 모든 선택행의 버전을 검사해 함께 반영한다. 완료 응답 유실 뒤 같은 요청을 다시 전송해 각 행에 한 번만 기록되는지 확인했다. `POST /api/drawing-008/delete-listed`와 `/api/drawing-008/planning` 하위의 발행·선택은 008 전용이며 001 계획에는 영향을 주지 않는다. 최신 C: 격리 Chrome까지 검증했다.

## frmProcess1 작업상태, 자재 및 불량 원장

경로 접두사는 /api/pop/work-orders이며 아래 API는 demo 프로필에서 동작한다. 단말·작업자는 로그인 세션에 귀속된다.

| 경로 | 요청 및 응답 |
| --- | --- |
| GET /production | 지시 날짜·순번, 버전, 양품·불량·배치·합성 생산잔량 및 그룹과 시작시각 |
| GET /production/roles | 세션에 적용된 투입·반납·양품·불량창고. 명시적으로 비운 역할은 비어 있는 채 유지 |
| POST /production | requestId, action, selected, visible, focus, autoPrint. 행에 날짜·순번·revision과 선택적인 양품/배치수. START의 materialDrafts는 기존 자재 셀 변경이며 scannedIssues는 새 스캔 투입행. 마지막 포커스가 진행행인 병합은 기존 원장에 지시만 추가 |
| GET /{date}/{sequence}/production-materials | 포커스가 속한 그룹의 투입/반납표. 소유 지시의 날짜·순번과 revision, 행의 영속 이벤트 번호, LOT·창고·위치·규격·수량을 반환 |
| POST /{date}/{sequence}/production-materials | requestId, action, remove, visible, lines. 소유행 revision과 기존 이벤트 번호를 확인한다. 반납 수정은 전체 반납표를 함께 보내고 투입 수량은 해당 행만 보낸다. |
| GET /{date}/{sequence}/rejections | 등록 가능한 상태·창고를 확인한 후 행 버전, 설정 불량창고·위치, 사유, 기존 합계·수량·사원을 반환 |
| POST /{date}/{sequence}/rejections | requestId, revision, warehouse, location, lines[{code,quantity}]. 사유 코드는 중복될 수 없고 수량은 0 이상 정수다. 0이면 사유 원장을 제거하고 부모 불량합계를 다시 계산 |

최초 START의 스캔행은 부모 포커스와 날짜/순번, 실재하는 창고·위치·LOT·품목, 현재 수량 및 공정 후보를 다시 확인한다. 동일 요청은 재시도해도 한 번만 차감한다. 후반 행 검증 실패 시 선행행의 자재와 그룹 저장도 취소한다. 서명을 바꿔 requestId를 재사용하거나 이전 버전으로 다시 쓰면 409다. 자료 입력 형식 오류는 422, 다른 단말 소유 지시나 없는 지시는 404다. 대표 사유 코드는 FOCUS_STARTED_ORDER, WORK_CHANGED, INPUT_MATERIAL_REQUIRED, BAD_WAREHOUSE_REQUIRED, PRODUCTION_QUANTITY_REQUIRED, LAST_MATERIAL이다.

Spring Boot jar와 Java 17 이상으로 다음과 같이 합성 원장 시험을 재현할 수 있다.

```console
python tools/process1-production/verify.py <spring-boot-jar>
```

### 008 그룹 반납 행 저장

`POST /api/drawing-008/returns`에 선택 지시 key, expectedVersion, requestId, returns 전 행을 전송한다. 단건과 다건 모두 시작 시 productionGroupNo를 갖는다. 작업중·중단중 해당 단말이 저장할 수 있고 같은 묶음 전체에서 같은 반납 행을 다시 읽는다. 서버가 사업장·허용 목적지·버전·치수와 수량을 검증한다. 동일 식별자 재전송은 같은 성공을 돌려주고 새 버전을 만들지 않는다. 최종 완료의 양품 수량, 실적 기록과 반납 중간저장은 별개 명령이다. `POST /api/drawing-008/plans/{key}/scan`과 audit 응답의 stockDetails는 LOT·창고·품목·사업장별 규격과 현재 잔고를 담는다. 확인용 규격은 별도 drawing-stock.json에서 온다.

## 작업지시서 전용 PDF

`/api/pop/work-print`는 frmWorkPrint의 기간·작업반·재질·계정·출력 상태 조회, 폼 선택 및 출력 원장을 제공한다. `POST /search`가 제공한 수주행 키와 양식으로 `POST /preview`를 호출한다. 등록된 문서 프린터, 선택행·사업장·역할, 종결 여부를 검사하고 문서 ID, 장수, 장치 및 해당 양식의 그룹번호를 돌려준다. 선택행이 없으면 400, 원본 단일 양식 보류 분기·장치 누락은 422, 글꼴이나 렌더 실패는 503이다.

`GET /preview/{id}/{page}`는 현재 세션의 페이지 PNG, `GET /preview/{id}/pdf`는 실제 전체 A4 PDF를 application/pdf 인라인으로 반환한다. `POST /preview/{id}/close`는 원장 갱신 없이 문서를 닫는다. `POST /preview/{id}/submit`은 진단 설정과 동일 요청키를 검증해 합성 출력을 한 번만 반영한다. 다른 세션 문서는 404다. 데이터·양식 레이아웃과 소스 대응은 전환 레포 docs/work-print.md, 보고서 경계 및 바코드 회귀는 tools/work-print-verify에 있다.

PDF 기본 글꼴 설정 shinjin.demo.work-print-font는 shinjin.demo.output-font를 기본값으로 사용한다. 원본 조판 비교 시 로컬 배포 권한이 있는 글꼴로 work-print-latin-font, work-print-bold-font, work-print-latin-bold-font도 설정한다. 확인한 조합은 맑은 고딕·맑은 고딕 굵게·Arial·Arial Bold다.

## frmProcess1 수동 자재 위치 선택과 저장

수동 추가와 스캔은 현재 생산 슬롯을 전달한다. 수동 조회에서 반환한 실제 창고·위치·LOT·품목을 해당 세션·단말·지시·슬롯에서 다시 검증한다. 시작 전 선택은 최초 START 때 저장한다. 이미 생산 그룹이 있을 때 `POST /api/pop/work-orders/{date}/{sequence}/production-materials/manual`은 수동 창에서 확인한 부모 포커스 행을 저장한다. 검색만 했거나 취소했거나, 조회 목록에만 있고 합성 재고 원장에 없는 키는 재고를 차감하지 않는다. 재전송은 요청 ID로 구분한다.

합성 인수 파일 tools/demo-dataset/process1-manual-stock.json을 shinjin.demo.process1-material-stock으로 지정하면 키가 같은 명시적 창고·위치·품목 재고로 일반/보조/잔재 저장을 재현한다. 운영 재고와의 위치 또는 품목 추정 매핑은 사용하지 않았다.

### 003·103 메뉴에서의 장바구니 API 범위

`GET /api/pop/work-baskets`, `GET /api/pop/work-baskets/groups/{groupId}`, `POST /api/pop/work-baskets/commands`는 메뉴가 선택한 `X-Pop-Process-Slot`, `X-Pop-Work-Code`를 받는다. 서버는 현재 로그인 단말의 활성 슬롯과 저장된 공정코드를 검증한다. 다른 공정의 행을 명령에 포함하면 403, 현재 공정 목록에 없는 그룹 조회는 404다. 기존 헤더 없는 독립 합성 호출은 기존 계약을 유지한다. 공정별 합성 지시 연결은 `shinjin.demo.basket-processes`로 교체 가능하다. 동일 날짜·다른 순번의 실제 두 타일 조작은 [[22-003-103-장바구니와-미완료-작업-삭제]]에서 확인한다.

### 로그인 전 상세 설정 및 현재 작업장 메뉴 (15179)

`GET /api/pop/prelogin-settings/terminals`로 이 데모가 제공하는 단말을 확인한다. `GET /api/pop/prelogin-details/{terminal}/{process|material}`는 현재 사업장·작업장, 버전, 후보와 현재 선택을 반환한다. 같은 경로의 PUT은 조회한 plant, center, expectedVersion과 slots 또는 materials를 받는다. 사업장이 바뀌거나 버전이 오래되면 409, 설정 가능한 범위를 벗어나면 저장이 거절된다. 창고는 같은 단말의 warehouse/entry → selection → priority 순서로 별도 확인을 거친다.

브라우저별 선택은 운영 DB 대신 별도 원자적 파일에 저장한다. 범위는 브라우저의 서명 권한 없는 난수 쿠키, 단말, 사업장, 작업장이다. 인증된 세션의 GET /api/pop/session에서 processSlots와 슬롯별 실제 workCodes를 확인한다. 같은 단말 관리자 PUT /api/pop/admin/terminal-settings/{terminal}/section/process 성공 뒤 현재 사용자 세션만 갱신하고, 로그인 전 브라우저의 슬롯 선택도 후행 편집에 보존한다. 공장 그룹의 단계/창고 배열과 일반 슬롯 효과는 독립적이다. 재시작 시험은 브라우저가 같은 쿠키를 보유한 경우에 수행했다. 검증용 암호 및 외부 스냅샷 전체 목록은 API 응답·문서로 반환하지 않는다.
 
### 사원번호 인쇄 미리보기의 제출 조건

`POST /api/demo/employee-print/entry`는 현재 로그인에 추가 비밀번호를 확인한다. 서버 시작 시 `shinjin.demo.employee-print-password`가 비어 있으면 진입을 거절한다. 사업장·부서별 사원조회와 QR/Code128 미리보기는 그 세션의 `X-Employee-Entry`를 요구한다. 보고서 정보의 `diagnostic`이 false이면 Quick Print가 비활성이고 `POST /api/demo/employee-print/preview/{id}/print`는 403이다. 독립 검증에서만 `shinjin.demo.employee-print-submit=true`로 합성 제출을 활성화한다. 등록 Printer1, 요청 키·부수·동일 본문 재시도 규칙은 그 다음에 적용한다.

### 003·103의 수주 바코드 스캔

`GET /api/pop/work-baskets/scan`은 선택한 실제 공정 슬롯 및 단말의 양품창고 설정 여부를 반환한다. `POST /api/pop/work-baskets/scan`은 JSON `{"barcode":"…"}`와 같은 슬롯·공정 헤더를 받는다. 원본 `ComOrderNoScan.cs` 177–288·380–446행에서 12자 수주번호 또는 수주번호+4자 고객 규격을 읽고, 로그인 단말의 공장·사업장·작업반, 선택 공정, 첫 양품창고, 수주번호·규격을 `SP_POP_COM_ORDERNOSCAN_01_LIST`에 전달한다. 결과에 등록 재질이 하나라도 있는지 확인한 뒤 완료 시각이 있고 잔량이 0인 행을 건너뛴다. 웹의 격리 fixture는 이 입력과 결과를 `basket-scans.json`에 명시한다. 잘못된 길이 400, 조건에 맞는 수주 없음 404, 양품창고 미설정/완료 409, 재질 미등록 422이다. 데이터가 이미 그리드에 있으면 원본과 같이 확인창에서 재스캔을 막는다. 12자는 복수 행/규격, 16자는 지정한 규격만 포함한다. 반환값은 `keys,orderNo,detailCode`이고 운영 프로시저는 호출하지 않는다.


## 003·103 투입자재 위치 선택과 포커스 행 저장

| 요청 | 003·103 투입 위치 선택 |
| --- | --- |
| `GET /api/pop/work-baskets/stock-picker/{date}/{sequence}?checked={date}/{seq}` | 반복 가능한 checked와 실제 공정 슬롯·코드를 검사한다. 포커스 지시, 체크된 지시, 두께·폭, 재질명, 투입·보조창고, 마지막 고정 창고를 반환한다. |
| 같은 경로 아래 `PUT /fixed`, `POST /stock` | 고정 창고를 변경하거나 선택 창고·창고 역할·두께·폭으로 조회한다. 해당 지시가 반환받은 창고·위치·LOT·자재 복합키를 로그인 세션별로 기억한다. |
| `POST /location`, `POST /remnants` | 위치 바코드 결과 또는 잔재 허용 여부와 후보 목록을 반환한다. 원본의 재질 014·015 확대와 잔재 사업장·공정 분기를 적용한다. |
| `POST /api/pop/work-baskets/commands`의 `ADD_MANUAL_ISSUE` | 단건 포커스 지시·그룹·자재행·수량·부모의 실제 `manualSequence`를 받는다. 0이면 다음 그룹 투입 순번을 채번하고, 이미 표시된 순번이면 원본 INSERT의 키를 유지한다. 미조회 후보·다른 로그인/슬롯 403, 오래된 버전 또는 기존 PK 충돌 409, 지시에 없는 순번 422다. 같은 요청 ID·동일 로그인 주체·동일 내용으로 재전송하면 첫 응답을 돌려준다. |

합성 SP 응답은 `demo/basket-stock-picker.json`의 입력·결과 쌍에서 읽는다. `shinjin.demo.basket-stock-picker`로 독립 테스트 파일을 지정할 수 있다. 운영 SP 호출이나 운영 DB 변경을 수행하지 않는다. 재현 도구는 `tools/basket-stock-picker/verify.py`이며 웹 빌드와 demo Spring JAR, Python Playwright 및 Chrome이 필요하다. 부모 표와 원본 SQL의 순번 처리 근거는 [[22-003-103-장바구니와-미완료-작업-삭제]]에서 확인할 수 있다.

## 001 양품위치 조회와 작업 배치

GET `/api/pop/work-orders/{date}/{sequence}/good-locations?slot={slot}`는 활성 공정 슬롯·단말 지시를 검사하여 양품창고와 종속 위치, 기존 선택을 반환한다. POST `/api/pop/work-orders/production`의 START·COMPLETE는 선택 행의 선택적 `goodPlace:{warehouse,location,slot}`를 검증한 뒤 생산 전이와 함께 저장한다. 상태 및 ETC는 서버의 행/창고 기준으로 결정한다. 오류와 반영 범위는 [[32-공통팝업-기능명세#001 작업지시의 양품창고·로케이션]]에서 확인할 수 있다.

팝업 적용의 POST `/api/pop/work-orders/{date}/{sequence}/good-locations?slot={slot}`는 확인된 세션 내 선택을 기억한다. 새 창고에 없는 기존 위치코드는 동일 지시의 선택 이력이 확인될 때 작업 배치에 전달할 수 있다. 수불 원장은 작업 배치 성공 때 반영한다.

## 로그인 전 프린터 및 연결 프로필

두 구획은 브라우저의 POP_LOCAL_SETTINGS 쿠키와 terminalId에 귀속되며 plant·center는 사용하지 않는다. 로그인 전 읽기·쓰기는 사원/관리자 로그인 권한을 생성하지 않는다.

| 요청 | 계약 |
| --- | --- |
| GET /api/pop/prelogin-details/{terminalId}/printer | revision, 등록된 합성 devices, outputs의 document·shipment·label 역할값을 반환한다. 미선택은 NONE이다. |
| PUT /api/pop/prelogin-details/{terminalId}/printer | expectedVersion, outputs 세 역할을 받는다. 모든 역할이 해당 단말 장치 목록에 있어야 한다. 같은 장치 반복 사용이 가능하다. |
| GET /api/pop/prelogin-details/{terminalId}/info | revision, profile을 반환한다. profile은 ftpHost·ftpPort·imagePath·updatePath·version·dbHost·dbPort·database 여덟 문자열이다. |
| PUT /api/pop/prelogin-details/{terminalId}/info | expectedVersion, 같은 여덟 키의 profile을 원자적으로 저장한다. 각 키는 원본 버퍼 크기를 따라 63자까지 담는다. 주소에 자격정보를 섞은 형태와 제어 문자는 거부한다. |

구버전 요청은 409, 지원하지 않는 장치·잘못된 프로필은 422다. 두 구획이 같은 단말 설정 버전을 사용하므로 다른 창에서 먼저 저장하면 기존 창은 다시 조회한다. 로그인 세션의 applied.values.outputs는 다음 로그인 또는 명시적 관리자 새로고침 때 갱신된다. 별도 도구 tools/prelogin/verify_print_info.py는 임시 저장 경로와 로컬 포트에서 실행한다. 합성 출력 경로와 실제 장치 연동 범위는 [[31-시스템-설정-기능명세#로그인 전 프린터와 정보 확인]]에서 확인할 수 있다.

## 로그인 전 사업장·POP ID·설비 설정 API

기본 주소는 `/api/pop/prelogin-site-equipment/{terminalId}/{kind}`이며 kind는 plant, popId, machine이다. GET 기본 주소는 현재 버전·공정 설정 여부, GET `/equipment`는 해당 단말 후보 및 로컬 저장 상태를 반환한다. POP ID·설비의 전제 조건이 비어 있으면 409를 돌려준다. 로그인 세션은 요구하지 않는다.

| 저장 경로 | 요청·효과 |
| --- | --- |
| PUT `plant/plant` (단말 다음부터) | expectedVersion·equipmentVersion·plant·center. 서버 후보와 일치할 때 사업장과 종속 설정 초기화를 함께 기록한다. |
| PUT `popId/equipment/pop-id` | expectedVersion·siteRevision·scopePlant·scopeCenter, 단일 설비 코드 number. 해당 단말/사업장의 POP 후보를 검증한다. |
| PUT `machine/equipment/machines` | 같은 버전·범위와 machines 배열. 중복, 미등록 코드, 7개 이상 또는 NONE 혼합을 422로 거절한다. |

등록 상태가 바뀐 뒤에 오래된 편집창에서 저장해도 이전 설정이 복원되지 않도록 사이트 버전과 업무 버전을 확인한다. 최신 상태는 `GET /api/pop/prelogin-settings?terminalId=…`에서 읽는다. 정상 로그인 후 적용값은 해당 세션의 작업장과 설비 도크에서 확인한다. 업무 명세는 [[31-시스템-설정-기능명세#로그인 전 공장·작업장, POP ID, 설비 배정]]에 있다.

## 2026-11-26 로그인 전 설정과 세션 적용

선택 단말의 준비 상태는 `GET /api/pop/prelogin-settings?terminalId=...`, 등록 단말 목록은 `GET /api/pop/prelogin-settings/terminals`로 확인한다. 준비되지 않은 신규 단말도 설정 화면을 열 수 있다. 프린터 3역할과 연결 정보 8값은 `/api/pop/prelogin-details/{terminalId}/{printer|info}`, 공정·재질은 같은 경로의 `process|material`에서 GET·PUT 한다. 창고는 `warehouse/entry`에서 별도 암호 확인 후 `warehouse/selection`, `warehouse/priority` 순으로 저장한다. POP 그룹은 `group` 조회와 `group/{add|remove|processes|assign}` PUT, 사업장·설비·POP ID는 `/api/pop/prelogin-site-equipment/{terminalId}/{plant|machine|popId}` 하위를 사용한다.

서버는 브라우저 프로필과 선택 단말, 업무별 사업장·작업장을 구분해 로컬 파일에 기록한다. 온라인 사용자가 동시에 같은 로컬 구역을 저장하면 버전 충돌을 알린다. 다음 정상 로그인에 공정코드·슬롯, 설비 도크·POP ID, 그룹 단계·창고, 프린터 역할을 반영한다. [공개 검증 기록](file:///E:/ajk/devgit/shinjin/.team/menu-screen/README.md).

008의 `GET /api/drawing-008/return-places` 및 `POST /api/drawing-008/return-material`은 반납 위치 선택과 규격에 맞는 자재를 판정한다. `POST /api/drawing-008/good-place`는 작업자가 실제 연 지시·세션·저장 버전에 양품 위치 선택을 연결한다. START/END가 선택한 창고·위치·상태/ETC를 기록하며 완료 수불의 고정 017/000000을 별도로 검증했다. 호출 권한과 원장 데이터는 로그인 전 설정에서 생성되지 않는다.

## 006/106 포장 15·16자리 스캔

`POST /api/pop/packing/scan`은 단말·근무자·바코드와 화면의 기존 지시 키를 받아 인증된 단말 범위의 지시와 기존 투입 위치를 조회한다. 15자리 목록과 16자리 수주번호/규격을 구분한다. 같은 수주의 서로 다른 행을 유지하고 완료·중복·미배정 행의 사유를 반환한다. 기존 투입 LOT는 창고·위치·LOT가 함께 일치해야 한다. 이 호출은 지시와 재고를 저장하지 않는다. 401·403·404·409·422, 지연 응답 폐기와 503 후 재시도 결과는 [스캔 인계 명세](file:///E:/ajk/devgit/shinjin/.rework-process6-integrated-scan/release/006-106-통합스캔-인계.md)에서 확인한다.

### 005 그룹 계획의 불량 이력

현재 그룹에서 시작한 계획에 대해 `GET /api/pop/process-group-demo/groups/{group}/plans/{plan}/rejections`는 해당 단말의 불량창고·위치·사유·저장 내역과 부모 revision을 돌려준다. 같은 URI의 POST는 요청 식별자·revision·창고·위치·사유별 수량을 받는다. 저장 당시 그룹과 활성 계획을 다시 확인하고 부모의 불량합계 및 revision을 함께 갱신한다. 작업 전 또는 종료 뒤에는 409, 불량창고가 없을 때도 409이며 사용자에게 사유를 알린다. 현재 16:14 공개판 뒤의 C: 통합본에서 001·005의 저장·취소·재진입 및 창고 없음 사례를 확인했다. [원본과 검사](file:///E:/ajk/devgit/shinjin/.rework-parent-state-qa/handoff.md)

### 005·105와 008 투입 자재 조회

005·105 로봇의 `GET /api/pop/process-group-demo/input-material`은 세션에 설정된 투입창고와 규격을 제공한다. 같은 주소에 `POST {"raw":"LOT 번호"}`를 보내면 해당 단말·사업장·작업장·투입창고·공정 상태·재질·규격에서 사용 가능한 합성 재고 위치가 반환된다. 이 조회는 그룹 revision과 저장 수량을 유지한다. 부모 화면 안에서 모은 위치·수량은 START 또는 END 명령으로 확정한다. [그룹 저장 경계와 두 세션 시험](file:///E:/ajk/devgit/shinjin/.rework-group-material005/handoff.md)

008은 `GET /api/drawing-008/material-scan?plan=…`에서 계획과 단말의 투입창고를 확인한다. `lot`을 함께 보내면 재고가 남은 위치별 수량을 반환한다. 신규 단건은 1, 같은 LOT 재스캔은 재고 한도까지 1씩 더한다. 복수 위치는 선택창 적용 전까지 부모에 반영되지 않는다. [008 원본 호출·START 원장·재조회](file:///E:/ajk/devgit/shinjin/.rework-008-material-scan/handoff.md)

### 008 작업 시작 전 수동 투입

`GET /api/drawing-008/manual-material?plan=…`은 해당 계획의 수동 창고·규격 초기값을 제공한다. 하위 `stock`, `remnants`, `location`의 POST는 일반/잔재 후보와 위치를 조회하고 `PUT …/fixed`는 단말의 수동 선택창에 쓸 고정창고를 저장한다. 선택창 적용·체크삭제는 부모의 초안에서 처리하며 START가 확정될 때 수량을 반영한다. 시험한 고정창고 범위는 같은 데모 서버 프로세스에서의 재개방이다. [원본·후보·잔재·START 시험](file:///E:/ajk/devgit/shinjin/.rework-008-manual-material/handoff.md)

008의 완료 응답·감사 조회에서 automaticReturns는 013 자동 행, returnBalances는 일반 반납의 합성 잔량, productReceipts는 양품 입고다. 비정상 위치는 422로 원장을 보존한다. 수정 시 이전 위치의 수량을 차감한 뒤 새 위치에 더한다. 체크행 리비전 변경은 409로 거절하며 같은 완료 요청의 재전송은 두 번째 입고를 만들지 않는다. [실행 결과와 반납 산식](file:///E:/ajk/devgit/shinjin/.rework-008-checked-accounting/integration-handoff.md)
