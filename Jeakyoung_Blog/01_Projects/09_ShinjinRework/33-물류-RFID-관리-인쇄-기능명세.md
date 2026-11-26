---
title: 물류·RFID·관리·출력 폼별 이관 검토
date: 2026-11-26
draft: true
---

# 물류·RFID·관리·출력 폼별 이관 검토

원본 네 프로젝트의 폼 28개와 각 폼 내부 목록·편집·대화상자·보고서 분기를 실제 전환 working tree와 대조했다. POPLGS 12개, POPRFID 9개, POPMANAGEMENT 3개, POPPRINT 4개다. 프로젝트의 Properties 자동생성 파일과 일반 클래스는 폼 수에서 제외했다. 아래 링크의 줄 번호는 조사 시점 작업 트리 기준이다.

**우선 차이.** 발주입고의 날짜 일괄 반영, 간편이송의 사업장 간/동일 사업장 분기, RFID 매칭 해제와 실사진 적재, 작업지시서의 수주 선택·삭제·출력횟수 갱신, 사원번호 인쇄의 추가 권한 확인이 웹에 그대로 이관되지 않았다. 출하 완료/삭제처럼 이벤트가 남아 있어도 버튼이 숨겨진 경로는 별도로 표시했다.

**검증 범위.** 이번 격리 Chrome은 최신 메뉴에서 이송 의뢰→출고→입고와 간편이송 등록, 원문서 유형별 입고 조회 요청, RFID 타일별 입력·현황·사진 모드 및 출력 미리보기 요청을 확인했다. 그 밖의 메뉴 방문은 진입 검증이다. 기존 리뷰 링크는 각 리뷰 당시의 합성 데이터 범위다. 레거시 실행, 운영 DB 연결, SQL 실행, FTP, 카메라, 물리 출력은 이번 조사에서 사용하지 않았다. [Chrome 시나리오](../.menu-routing-review/browser.jsx)

**DB 인계 경계.** 현재는 연결 전이다. 조사 대상은 저장소에 있는 정의 파일과 C# 호출부다. 운영 설치 버전·권한·실제 데이터는 미확인이다. 기존 MSSQL 프로시저·트리거·함수 및 기타 로직의 생성·수정·삭제와 운영 쓰기 호출은 범위 밖이다. Spring 데모 메모리 저장 결과가 운영 SP 검증을 대신하지 않는다. 호출 위치별 계약과 정의 근거는 문서 뒤에 있다.

## POPLGS

### frmItemKind3 · 출하 품목유형 선택

**진입.** `POPLGS/frmLogistics6.cs:2892`. 출하 필터에서 유형 코드·명칭을 여러 개 체크한다. 저장은 호출 폼에 선택 목록 반환, 닫기·취소는 적용 중단이다.

**웹과 Spring.** 동일 단말의 품목유형 마스터를 여러 개 체크한다. 저장·취소·전체선택과 신규 유형의 기본 선택을 반영한다. 상세 기능·API는 Obsidian 18 「출하 전표와 업무 PDF」에 기록했다.

**운영 인수.** 운영 품목유형 마스터 결과 대사가 남았다.

**검증.** 2026-11-26 격리 Spring/Chrome과 동일 합성 값의 원본 폼 캡처. 분석 저장소 `.team/screen-review/web-parity/출하-화면대조.md` 참조.

**원본 이벤트.** `POPLGS/frmItemKind3.cs:42` · `POPLGS/frmItemKind3.cs:60` · `POPLGS/frmItemKind3.cs:36`

### frmLogistics1 · 공장이송의뢰

**진입.** `MainMenu/frmMenu.cs:692`. 출고·입고 사업장/창고, 의뢰일, 품목유형·재질·치수를 지정한다. 재고 조회→행 추가·적용→저장하며 기존 의뢰의 행/의뢰 삭제가 분리돼 있다.

**웹과 Spring.** 의뢰 ID·품목·수량으로 REQUEST, CANCEL_REQUEST. 단말별 출발·도착이 정해져 있다. `src/web/src/Transfer.tsx:73` · `src/api/src/main/java/com/shinjin/pop/transfer/TransferDemoController.java:29`

**남은 차이.** 복수 규격 재고를 조회해 서로 다른 위치의 여러 행으로 의뢰를 만드는 편집기와 행 단위 삭제가 없다.

**검증.** 이번 Chrome 의뢰 등록 및 후속 출고 확인. 레거시 다중행 편집은 미실행. `.rework-transfer-staging/transfer-integration-review.md:1`

**원본 이벤트.** `POPLGS/frmLogistics1.cs:1131` · `POPLGS/frmLogistics1.cs:1174` · `POPLGS/frmLogistics1.cs:1419` · `POPLGS/frmLogistics1.cs:1385` · `POPLGS/frmLogistics1.cs:1368` · `POPLGS/frmLogistics1.cs:1375` · `POPLGS/frmLogistics1.cs:1358` · `POPLGS/frmLogistics1.cs:1352` · `POPLGS/frmLogistics1.cs:605` · `POPLGS/frmLogistics1.cs:193` · `POPLGS/frmLogistics1.cs:912` · `POPLGS/frmLogistics1.cs:881` · `POPLGS/frmLogistics1.cs:660` · `POPLGS/frmLogistics1.cs:497` · `POPLGS/frmLogistics1.cs:654` · `POPLGS/frmLogistics1.cs:544` · `POPLGS/frmLogistics1.cs:273` · `POPLGS/frmLogistics1.cs:33`

**외부 선택창·보고서 호출.** `POPLGS/frmLogistics1.cs:886` · `POPLGS/frmLogistics1.cs:918` · `POPLGS/frmLogistics1.cs:1065` · `POPLGS/frmLogistics1.cs:1105` · `POPLGS/frmLogistics1.cs:1199` · `POPLGS/frmLogistics1.cs:1290` · `POPLGS/frmLogistics1.cs:1325`

### frmLogistics2 · 기존 공장이송출고

**진입.** `MainMenu/frmMenu.cs:707`. 의뢰·사업장·창고로 조회해 기출고/잔량을 보고 재고 위치를 적용, 출고량 저장 또는 삭제한다.

**웹과 Spring.** 새 출고 타일은 frmLogistics9 계열의 의뢰 상태 전이를 사용한다. `src/web/src/Transfer.tsx:73` · `src/api/src/main/java/com/shinjin/pop/transfer/TransferDemoController.java:29`

**남은 차이.** 구형 부모 타일이 숨김이다. 이 폼의 부분수량·출고위치 편집을 현역 출고와 합쳐 인수하지 않는다.

**검증.** Designer와 핸들러 정적 확인. 구형 화면 운영 사용 미확인. `.rework-transfer-staging/transfer-integration-review.md:1`

`MainMenu/frmMenu.Designer.cs:775`

**원본 이벤트.** `POPLGS/frmLogistics2.cs:280` · `POPLGS/frmLogistics2.cs:793` · `POPLGS/frmLogistics2.cs:761` · `POPLGS/frmLogistics2.cs:857` · `POPLGS/frmLogistics2.cs:604` · `POPLGS/frmLogistics2.cs:334` · `POPLGS/frmLogistics2.cs:306` · `POPLGS/frmLogistics2.cs:994` · `POPLGS/frmLogistics2.cs:1001` · `POPLGS/frmLogistics2.cs:1018` · `POPLGS/frmLogistics2.cs:1011` · `POPLGS/frmLogistics2.cs:1028` · `POPLGS/frmLogistics2.cs:29`

**외부 선택창·보고서 호출.** `POPLGS/frmLogistics2.cs:766` · `POPLGS/frmLogistics2.cs:799` · `POPLGS/frmLogistics2.cs:917` · `POPLGS/frmLogistics2.cs:955`

### frmLogistics3 · 공장이송입고

**진입.** `MainMenu/frmMenu.cs:722`. 미입고 출고 목록·출고품목과 기존 입고 목록·입고품목을 별도 조회한다. 선택 출고를 입고 저장하고 기존 입고 행의 삭제 버튼을 처리한다.

**웹과 Spring.** 출고 완료 의뢰를 조회하여 RECEIVE, 입고 완료 건에 UNDO_RECEIVE. `src/web/src/Transfer.tsx:73` · `src/api/src/main/java/com/shinjin/pop/transfer/TransferDemoController.java:29`

**남은 차이.** 사업장·창고·일자별 4개 그리드, 의뢰 내 원출고 행 선택 및 저장 행 삭제의 동등성 미확보.

**검증.** 이번 Chrome 실제 출고 뒤 입고 완료. 역순 취소·전표는 이전 이송 리뷰. `.rework-transfer-staging/transfer-integration-review.md:1`

**원본 이벤트.** `POPLGS/frmLogistics3.cs:1519` · `POPLGS/frmLogistics3.cs:105` · `POPLGS/frmLogistics3.cs:228` · `POPLGS/frmLogistics3.cs:1032` · `POPLGS/frmLogistics3.cs:1410` · `POPLGS/frmLogistics3.cs:1037` · `POPLGS/frmLogistics3.cs:1003` · `POPLGS/frmLogistics3.cs:36` · `POPLGS/frmLogistics3.cs:48`

### frmLogistics4 · ESCO 입고

**진입.** `MainMenu/frmMenu.cs:736`. 출하 문서 입력 후 Enter로 상세를 읽고 입고 창고·일자와 행을 확인한다. Clear는 입력 초기화, 저장은 ESCO 생성과 후속 반영을 트랜잭션으로 처리한다.

**웹과 Spring.** ESCO 출하번호 Enter로 조회하고 14자 전표 전체를 저장한다. 원본 사전·사후 행과 실패 조건은 분리한 합성 파일에 있다. `src/web/src/procurement/ProcurementReceiving.tsx:25` · `src/api/src/main/java/com/shinjin/pop/procurement/ProcurementDemoController.java:36`

**남은 차이.** 출하번호 불일치 정책, 현장 창고·LOT, 운영 월재고와 두 commit 사이 장애 처리 대사가 남아 있다.

**검증.** 2026-11-26 Chrome에서 정상 전표 전체·0행 조회·입력/행 Clear, 합성 ERP 및 월재고 오류, POP 빈 결과를 확인했다. 이전 부분입고 검증 기록을 보존한다. `.rework-procurement-staging/procurement-review.md:1`

**원본 이벤트.** `POPLGS/frmLogistics4.cs:415` · `POPLGS/frmLogistics4.cs:127` · `POPLGS/frmLogistics4.cs:122` · `POPLGS/frmLogistics4.cs:227` · `POPLGS/frmLogistics4.cs:28`

### frmLogistics5 · 재고이동

**진입.** `MainMenu/frmMenu.cs:750`. 기존 처리번호를 불러오거나 신규로 여러 행을 추가한다. 행별 출고·입고 창고/위치와 재고·이동량을 정한 뒤 저장·삭제한다.

**화면과 입력.** 물류 → 재고이동을 열면 입출일자는 오늘, 입고 사업장은 로그인 사업장이다. 창고와 목록은 빈 상태다. 사업장·창고 검색창에서 선택하고 적용을 확인한 다음 행 추가를 누른다. 작업자는 왼쪽 자재 목록에서 +를 눌러 오른쪽 적용 목록에 담는다. 같은 품목·LOT·창고·위치의 +는 수량을 1 늘리고 −는 1 줄인다. 재질·두께·폭으로 검색할 수 있다. LOT 스캔은 열 자리이며 여러 위치에서 발견된 LOT는 직접 터치한다. 별도 Location 스캔창은 입력창고의 바코드를 확인하고 위치명을 표시한다. 원본은 재고이동에서 위치스캔 결과를 재고 조회 조건으로 넘기지 않는다. 잔재 추가는 원본 허용 재질일 때 별도 재고 조회의 첫 행을 적용한다. 웹의 해당 후보는 합성 카탈로그에서 명시한다.

**전표와 삭제.** 적용하면 행마다 품목의 기본 입고 위치를 다시 설정한다. 기본값이 없으면 `000000/미적용`이다. 행의 입고 창고·Location은 선택창에서, 이동 수량은 신규 문서에서 숫자패드로 변경한다. 수량 0은 입력할 수 있고 재고 초과는 거부한다. 저장은 체크 여부와 관계없이 전 행을 하나의 처리번호에 담으며, 삭제는 체크한 행만 처리한다. 저장 전 삭제는 화면에만 반영된다. 저장 후 일부 삭제하면 같은 처리번호로 다시 조회하고, 마지막 상세가 없어지면 헤더도 제거한다. 기존 전표는 처리 번호 → 당일 출고 목록 → 체크 → 조회 → 예로 다시 연다. 기존 전표에서는 행 추가와 수량 변경을 제한한다. 웹은 `InventoryMoves.tsx`, `InventoryDialogs.tsx`, `InventoryStockDialog.tsx`에 구현했다.

**저장 근거와 확인할 운영 조건.** 원본은 출고요청·출고 헤더/상세(`TPR501/502`, `TMA502/503`)를 같은 트랜잭션에서 처리한다. 입고창고 인자는 헤더에서, 입고 위치는 상세 행에서 읽는다. 행의 창고를 바꿔도 이 바인딩을 유지했다. 원본의 기본 위치 조회는 `TCO102M`·`TCO102L`을 사용한다. 운영 상세/목록 SP 본문, 운영 창고와 위치의 제약 및 잔재 결과 산출식은 미확인이다. 합성 검증에서는 헤더가 BIN-B인 상태로 BIN-A 전용 위치 A-01을 넘기면 403이며, 전체 행·재고·번호가 보존된다. 운영 수용 여부, 상세 SP의 재고수량 산출 시점, LOT가 여러 건일 때 목록의 재질 표시 규칙은 운영 연결 시 확인한다.

**재현.** demo 프로파일의 별도 `demo/inventory-catalog.json`을 사용한다. DEMO-A에서 입고 창고를 현장창고로 지정한 뒤 자재창고의 LOT-X(A-01), LOT-X2(A-01)를 담아 한 행만 체크하고 저장한다. 처리 번호에서 두 행을 재조회하고 각각 삭제한다. 위치가 하나인 스캔값은 `0000000001`, 두 위치인 값은 `0000000002`다. 동일 번호 재시도와 두 작업자 버전 경합의 인수 기준은 [[30-Spring-API-명세]]의 InventoryDemoController를 따른다.

**원본 이벤트.** `POPLGS/frmLogistics5.cs:132` · `POPLGS/frmLogistics5.cs:1054` · `POPLGS/frmLogistics5.cs:176` · `POPLGS/frmLogistics5.cs:162` · `POPLGS/frmLogistics5.cs:831` · `POPLGS/frmLogistics5.cs:627` · `POPLGS/frmLogistics5.cs:187` · `POPLGS/frmLogistics5.cs:1136` · `POPLGS/frmLogistics5.cs:1143` · `POPLGS/frmLogistics5.cs:1153` · `POPLGS/frmLogistics5.cs:28`

**외부 선택창·보고서 호출.** `POPLGS/frmLogistics5.cs:836` · `POPLGS/frmLogistics5.cs:879` · `POPLGS/frmLogistics5.cs:912` · `POPLGS/frmLogistics5.cs:968` · `POPLGS/frmLogistics5.cs:1059` · `POPLGS/frmLogistics5.cs:1099`

### frmLogistics6 · 출하

**진입.** `MainMenu/frmMenu.cs:765`. 포장일·거래처·수주·작업반·품목유형·재질·이월 조건으로 후보를 조회한다. 상단 후보 선택→적용→하단 출하 목록 저장·삭제, 인쇄와 자동인쇄가 있다. 완료/완료삭제 컨트롤은 Designer에서 숨김이다.

**웹과 Spring.** 상단 포장 후보, 하단 LOT 초안 및 완료내역, 수주 단위 적용, 전표 전체 저장·취소, 수동 다전표 PDF와 합성 프린터 2의 결과를 확인했다. 상세 기능·API는 Obsidian 18 「출하 전표와 업무 PDF」에 기록했다.

**운영 인수.** 01_LIST 이월 0/1의 운영 결과와 05_LIST 완료일의 비교 열, ERP 실제 수주·단가·세액·두 DB 커밋 간 실패는 운영 연결 전 인수 대상이다. 숨김 완료·완료삭제와 주석 처리된 ComShipplanSeq는 작업자에게 노출하지 않는다.

**검증.** 2026-11-26 격리 Spring/Chrome과 동일 합성 값의 원본 폼 캡처. 분석 저장소 `.team/screen-review/web-parity/출하-화면대조.md` 참조.

`POPLGS/frmLogistics6.Designer.cs:652` · `POPLGS/frmLogistics6.Designer.cs:3096`

**원본 이벤트.** `POPLGS/frmLogistics6.cs:4763` · `POPLGS/frmLogistics6.cs:2905` · `POPLGS/frmLogistics6.cs:2890` · `POPLGS/frmLogistics6.cs:2874` · `POPLGS/frmLogistics6.cs:2858` · `POPLGS/frmLogistics6.cs:4877` · `POPLGS/frmLogistics6.cs:1098` · `POPLGS/frmLogistics6.cs:2665` · `POPLGS/frmLogistics6.cs:111` · `POPLGS/frmLogistics6.cs:2719` · `POPLGS/frmLogistics6.cs:2737` · `POPLGS/frmLogistics6.cs:2849` · `POPLGS/frmLogistics6.cs:351` · `POPLGS/frmLogistics6.cs:3534` · `POPLGS/frmLogistics6.cs:3350` · `POPLGS/frmLogistics6.cs:3020` · `POPLGS/frmLogistics6.cs:1137` · `POPLGS/frmLogistics6.cs:2593` · `POPLGS/frmLogistics6.cs:1434` · `POPLGS/frmLogistics6.cs:69`

**외부 선택창·보고서 호출.** `POPLGS/frmLogistics6.cs:2690` · `POPLGS/frmLogistics6.cs:3550`

### frmLogistics7 · 발주입고

**진입.** `MainMenu/frmMenu.cs:779`. 지정일 발주입고 내역·반영 여부를 조회한다. 저장은 로그인 사업장을 ERP 사업장으로 매핑한 뒤 같은 시작·종료 날짜로 일괄 반영을 호출한다.

**웹과 Spring.** 날짜 변경 시 사업장 목록 자동 조회, 선택 날짜 일괄 저장 및 재조회를 수행한다. `src/web/src/procurement/ProcurementReceiving.tsx:25` · `src/api/src/main/java/com/shinjin/pop/procurement/ProcurementDemoController.java:36`

**남은 차이.** 합성 날짜·사업장 일괄은 구현했다. SP 결과셋과 실제 ERP 사업장별 수불 반영은 연결 전 검증 항목이다.

**검증.** Chrome에서 선행 날짜·빈 날짜, 동사업장 다른 단말 재조회, 다른 사업장 격리와 합성 실패 상태 보존을 확인했다. `.rework-procurement-staging/procurement-review.md:1`

**원본 이벤트.** `POPLGS/frmLogistics7.cs:229` · `POPLGS/frmLogistics7.cs:56` · `POPLGS/frmLogistics7.cs:61` · `POPLGS/frmLogistics7.cs:33`

일자 일괄의 호출 근거 `POPLGS/frmLogistics7.cs:105`

### frmLogistics8 · 간편공장이송

**진입.** `MainMenu/frmMenu.cs:793`. 자재 목록에서 규격·재고를 찾고 적용 목록에 수량을 추가·삭제한다. 출발/도착 사업장 조건에 따라 사업장 이동과 창고 이동 저장을 분기한다.

**웹과 Spring.** 간편 등록은 QUICK_TRANSFER로 의뢰·출고·입고를 묶는다. `src/web/src/Transfer.tsx:73` · `src/api/src/main/java/com/shinjin/pop/transfer/TransferDemoController.java:29`

**남은 차이.** 웹 의뢰 폼은 한 품목·한 수량이다. 다중 자재 목록과 같은 사업장 창고 이동 분기 대사 미완.

**검증.** 이번 Chrome 간편 등록 완료. ERP 선반영 재개는 합성 범위. `.rework-transfer-staging/transfer-integration-review.md:1`

**원본 이벤트.** `POPLGS/frmLogistics8.cs:907` · `POPLGS/frmLogistics8.cs:658` · `POPLGS/frmLogistics8.cs:485` · `POPLGS/frmLogistics8.cs:440` · `POPLGS/frmLogistics8.cs:455` · `POPLGS/frmLogistics8.cs:504` · `POPLGS/frmLogistics8.cs:470` · `POPLGS/frmLogistics8.cs:720` · `POPLGS/frmLogistics8.cs:825` · `POPLGS/frmLogistics8.cs:39`

사업장 이동/창고 이동 저장 분기 `POPLGS/frmLogistics8.cs:939` · `POPLGS/frmLogistics8.cs:2102`

**외부 선택창·보고서 호출.** `POPLGS/frmLogistics8.cs:510` · `POPLGS/frmLogistics8.cs:882`

### frmLogistics9 · 공장이송출고

**진입.** `MainMenu/frmMenu.cs:808`. 출고요청 목록/품목, 출고 목록/품목, 자동 입고 여부를 확인한다. 행 선택·저장·삭제와 출고목록 출력이 분리돼 있다.

**웹과 Spring.** 출고 타일은 SHIP/UNDO_SHIP 해당 상태를 표시한다. 출력 메뉴에 출고목록 PDF 양식이 있다. `src/web/src/Transfer.tsx:73` · `src/api/src/main/java/com/shinjin/pop/transfer/TransferDemoController.java:29`

**남은 차이.** 출고 행별 자동입고·사업장별 조회, 실제 선택 전표를 인자로 여는 출력과 부분 행 처리 미연결.

**검증.** 이번 Chrome 의뢰 선택→출고 확인. 선택 전표 인쇄 미검증. `.rework-transfer-staging/transfer-integration-review.md:1`

**원본 이벤트.** `POPLGS/frmLogistics9.cs:2102` · `POPLGS/frmLogistics9.cs:151` · `POPLGS/frmLogistics9.cs:270` · `POPLGS/frmLogistics9.cs:944` · `POPLGS/frmLogistics9.cs:868` · `POPLGS/frmLogistics9.cs:1959` · `POPLGS/frmLogistics9.cs:1951` · `POPLGS/frmLogistics9.cs:38` · `POPLGS/frmLogistics9.cs:47`

**외부 선택창·보고서 호출.** `POPLGS/frmLogistics9.cs:2145`

### frmWorkcenter · 출하 작업반 선택

**진입.** `POPLGS/frmLogistics6.cs:2907`. 작업반 코드·명칭 목록을 조회해 선택 결과를 출하 필터로 반환한다. 닫기·취소 시 적용하지 않는다.

**웹과 Spring.** 작업반 코드·명칭을 체크하고 저장하면 상단 조회에서 WORKCENTER_CODE 목록을 전송한다. 취소하면 이전 선택을 보존한다. 상세 기능·API는 Obsidian 18 「출하 전표와 업무 PDF」에 기록했다.

**운영 인수.** 실제 사업장 작업반 마스터 대사가 남았다.

**검증.** 2026-11-26 격리 Spring/Chrome과 동일 합성 값의 원본 폼 캡처. 분석 저장소 `.team/screen-review/web-parity/출하-화면대조.md` 참조.

**원본 이벤트.** `POPLGS/frmWorkcenter.cs:125` · `POPLGS/frmWorkcenter.cs:143` · `POPLGS/frmWorkcenter.cs:37`

### WaitForm1 · 물류 조회·저장 대기창

**진입.** `POPLGS/frmLogistics1.cs:1867` · `POPLGS/frmLogistics3.cs:605` · `POPLGS/frmLogistics6.cs:155` · `POPLGS/frmLogistics7.cs:69` · `POPLGS/frmLogistics8.cs:540` · `POPLGS/frmLogistics9.cs:474`. 호출 폼이 caption/description을 설정하고 작업 종료 시 닫는다. 독립 입력·업무 저장·인쇄 기능이 없다.

**웹과 Spring.** 각 물류 화면의 busy, 버튼 비활성 및 상태 통보가 일부 대응한다. `src/web/src/Transfer.tsx:73` · `src/api/src/main/java/com/shinjin/pop/transfer/TransferDemoController.java:29`

**남은 차이.** 부모 폼별 중복 터치 차단, 실패 시 닫힘/포커스 복구의 전수 UI 대조가 남았다.

**검증.** 이전 재전송 시험은 일부 부모만 검증. 대기창 자체 미실행. `.rework-transfer-staging/transfer-integration-review.md:1`

**원본 이벤트.** `POPLGS/WaitForm1.cs:12`

## POPRFID

### FrmNumericKeyPad · RFID 번호 입력

**진입.** `POPRFID/FrmPalletBox.cs:691` · `POPRFID/FrmPalletMatch.cs:647` · `POPRFID/FrmTagInOutReg.cs:398`. 숫자·한 글자 지움·전체 지움·적용·취소와 최대 자릿수를 가진 모달이다.

**웹과 Spring.** RFID 화면에서 TouchField로 번호/코드를 입력한다. `src/web/src/ScanInput.tsx:15` · `src/api/src/main/java/com/shinjin/pop/rfid/RfidDemoController.java:22`

**남은 차이.** 원본 8자리 제한, 거래처/파렛트 번호별 적용·취소 결과와 부모 포커스 동등성 미검증.

**검증.** 키패드 호출부 정적 비교. 다른 화면 키패드 시험을 전용 폼 합격으로 이월하지 않았다. `.rework-device-staging/scan-review.md:1`

**원본 이벤트.** `POPRFID/FrmNumericKeyPad.cs:93` · `POPRFID/FrmNumericKeyPad.cs:52` · `POPRFID/FrmNumericKeyPad.cs:76` · `POPRFID/FrmNumericKeyPad.cs:34` · `POPRFID/FrmNumericKeyPad.cs:118`

### FrmPalletBox · 파렛트 적재

**진입.** `MainMenu/frmMenu.cs:960`. 파렛트·태그·출고처·포장일을 입력한다. 촬영/카메라 전환/사진 확정과 적재 저장·전송 진행 표시가 별도다.

**웹과 Spring.** load로 품목을 적재한다. 이력 화면은 기존 첨부를 읽고 검증 모드에서만 샘플 첨부를 허용한다. `src/web/src/RfidDemo.tsx:50` · `src/api/src/main/java/com/shinjin/pop/rfid/RfidDemoController.java:22`

**남은 차이.** 실제 카메라·촬영본 채택 및 FTP 업로드, 거래처와 포장일을 포함한 적재 원본 저장 미구현.

**검증.** 이번 API 적재·일반/검증 사진 UI 구분. 장비/FTP 미실행. `.rework-scan-rfid-staging/scan-rfid-integration-review.md:1`

**원본 이벤트.** `POPRFID/FrmPalletBox.cs:171` · `POPRFID/FrmPalletBox.cs:689` · `POPRFID/FrmPalletBox.cs:94` · `POPRFID/FrmPalletBox.cs:202` · `POPRFID/FrmPalletBox.cs:485` · `POPRFID/FrmPalletBox.cs:554` · `POPRFID/FrmPalletBox.cs:181` · `POPRFID/FrmPalletBox.cs:76`

### FrmPalletMatch · 파렛트 매칭

**진입.** `MainMenu/frmMenu.cs:942`. 사업장·유형·상태 목록, RFID로 찾기, 선택행 태그·파렛트 저장. 삭제 이벤트는 기존 파렛트의 태그 코드를 해제한다.

**웹과 Spring.** match로 태그와 파렛트를 연결하고 충돌을 차단한다. `src/web/src/RfidDemo.tsx:50` · `src/api/src/main/java/com/shinjin/pop/rfid/RfidDemoController.java:22`

**남은 차이.** 태그로 파렛트 역조회, 파렛트 마스터 필터·목록, 저장된 매칭 해제 명령이 없다.

**검증.** 이번 타일과 API 매칭 확인. 해제 미구현. `.rework-scan-rfid-staging/scan-rfid-integration-review.md:1`

**원본 이벤트.** `POPRFID/FrmPalletMatch.cs:645` · `POPRFID/FrmPalletMatch.cs:583` · `POPRFID/FrmPalletMatch.cs:635` · `POPRFID/FrmPalletMatch.cs:363` · `POPRFID/FrmPalletMatch.cs:625` · `POPRFID/FrmPalletMatch.cs:315` · `POPRFID/FrmPalletMatch.cs:444` · `POPRFID/FrmPalletMatch.cs:58`

### FrmPhoto · RFID 사진 보기

**진입.** `POPRFID/FrmRfidNoScan.cs:591` · `POPRFID/FrmTagInOutList.cs:280`. 스캔 창 또는 입출고 이력에서 사진을 열고 읽은 이미지에 입/출 도장을 그린다. 닫기는 부모로 복귀한다.

**웹과 Spring.** 기존 첨부 미리보기·확대가 있고 원본 촬영 명령은 없다. `src/web/src/RfidPhotos.tsx:20` · `src/api/src/main/java/com/shinjin/pop/rfid/RfidDemoController.java:22`

**남은 차이.** 날짜·태그별 원본 파일 매핑, 원본 이미지·도장 및 다운로드 실패 동작 미대응.

**검증.** 합성 첨부 이력 진입 확인. FTP·카메라·원본 사진 미사용. `.rework-rfid-photo-staging/release-2b54fc3/d2-review.md:1`

**원본 이벤트.** `POPRFID/FrmPhoto.cs:185` · `POPRFID/FrmPhoto.cs:110`

이미지 읽기 및 도장 근거 `POPRFID/FrmPhoto.cs:148` · `POPRFID/FrmPhoto.cs:216`

### FrmProgress · 사진 전송 진행창

**진입.** `POPRFID/FrmPalletBox.cs:593`. 파렛트 적재 저장 과정에서 전송 진행률을 전달받는 WaitForm이다. 독립 저장·삭제·출력 없음.

**웹과 Spring.** 사진 요청 busy·상태 메시지가 대응한다. `src/web/src/RfidPhotos.tsx:20` · `src/api/src/main/java/com/shinjin/pop/rfid/RfidDemoController.java:22`

**남은 차이.** 바이트 진행률, FTP 실패 후 닫힘과 부모 저장 상태 복구는 장비/전송 통합 범위다.

**검증.** 코드 확인. 전송 시험 없음. `.rework-rfid-photo-staging/release-2b54fc3/d2-review.md:1`

**원본 이벤트.** `POPRFID/FrmProgress.cs:12`

### FrmRfidNoScan · RFID 스캔 대화상자

**진입.** `POPRFID/FrmPalletBox.cs:175` · `POPRFID/FrmPalletMatch.cs:629` · `POPRFID/FrmTagInOutReg.cs:68` · `POPRFID/FrmTagReg.cs:175`. 호출 유형별 태그번호·ID와 바코드를 수집하고 중복/존재 여부를 검사한다. 닫을 때 결과에 따라 OK/Cancel, 사진창 호출도 있다.

**웹과 Spring.** ScanInput과 태그 등록 필드는 스캔 문자열을 전달한다. `src/web/src/ScanInput.tsx:15` · `src/api/src/main/java/com/shinjin/pop/rfid/RfidDemoController.java:22`

**남은 차이.** 파렛트 매칭·수동이동의 호출 유형별 반환값, 스캐너/사진 왕복과 다건 목록 반환 미대응.

**검증.** 기존 scan-rfid-integration-review는 전달·세션 시험. 실물 스캔 미실행. `.rework-device-staging/scan-review.md:1`

**원본 이벤트.** `POPRFID/FrmRfidNoScan.cs:149` · `POPRFID/FrmRfidNoScan.cs:175` · `POPRFID/FrmRfidNoScan.cs:589` · `POPRFID/FrmRfidNoScan.cs:83` · `POPRFID/FrmRfidNoScan.cs:88`

### FrmTagInOutList · 입출고 현황

**진입.** `MainMenu/frmMenu.cs:996`. 사업장·기간·자동 새로고침, 목록 더블클릭 사진, 수동등록 화면 호출이 있다.

**웹과 Spring.** 현재 세션의 이동 행·증감, 사진 이벤트/기존 첨부 확대. `src/web/src/RfidDemo.tsx:50` · `src/api/src/main/java/com/shinjin/pop/rfid/RfidDemoController.java:22`

**남은 차이.** 사업장·기간 필터와 주기 갱신, 목록 행에서 해당 이미지/수동등록으로 넘어가는 동선 미대응.

**검증.** 이번 Chrome 실제 생성한 파렛트 이력 조회. 다사업장 목록 미검증. `.rework-scan-rfid-staging/scan-rfid-integration-review.md:1`

**원본 이벤트.** `POPRFID/FrmTagInOutList.cs:255` · `POPRFID/FrmTagInOutList.cs:169` · `POPRFID/FrmTagInOutList.cs:186` · `POPRFID/FrmTagInOutList.cs:250` · `POPRFID/FrmTagInOutList.cs:103`

### FrmTagInOutReg · 입출고 수동등록

**진입.** `MainMenu/frmMenu.cs:978`. 태그 또는 파렛트 조회 후 입출처·일시를 확인하고 입고·출고 버튼을 구분한다.

**웹과 Spring.** in/out 이벤트를 작업자·단말 범위에서 기록하고 재생·입출고 순서를 확인한다. `src/web/src/RfidDemo.tsx:50` · `src/api/src/main/java/com/shinjin/pop/rfid/RfidDemoController.java:22`

**남은 차이.** 원 태그번호 조회와 거래처·사용자 지정 일시, 사진 파일 연계가 남았다. 반대 방향 이동을 원 이벤트 취소로 해석하지 않았다.

**검증.** 이번 타일 및 수동 입고 API. 기존 RFID 리뷰의 순서·중복 범위. `.rework-scan-rfid-staging/scan-rfid-integration-review.md:1`

**원본 이벤트.** `POPRFID/FrmTagInOutReg.cs:185` · `POPRFID/FrmTagInOutReg.cs:254` · `POPRFID/FrmTagInOutReg.cs:180` · `POPRFID/FrmTagInOutReg.cs:170` · `POPRFID/FrmTagInOutReg.cs:64` · `POPRFID/FrmTagInOutReg.cs:396` · `POPRFID/FrmTagInOutReg.cs:387`

### FrmTagReg · TAG 등록

**진입.** `MainMenu/frmMenu.cs:924`. 사업장·등록기간으로 관리번호/태그 ID/사용여부를 조회하고 스캔 후 저장한다.

**웹과 Spring.** TAG 등록 타일, 태그 입력 및 register 명령, 작업자별 이벤트 키. `src/web/src/RfidDemo.tsx:50` · `src/api/src/main/java/com/shinjin/pop/rfid/RfidDemoController.java:22`

**남은 차이.** 관리번호와 리더 ID의 별도 관리, 기간별 등록 목록·사용여부 편집의 대응이 없다.

**검증.** 이번 타일 진입 및 API 등록. 기존 RFID 합성 중복 시험. `.rework-scan-rfid-staging/scan-rfid-integration-review.md:1`

**원본 이벤트.** `POPRFID/FrmTagReg.cs:181` · `POPRFID/FrmTagReg.cs:293` · `POPRFID/FrmTagReg.cs:171` · `POPRFID/FrmTagReg.cs:69`

## POPMANAGEMENT

### frmExpendables · 소모품 목록·신청재고·최근 1개월 신청내역

**진입.** `MainMenu/frmMenu.cs:824`. Designer 604–608행에서 탭을 page1, page3, page2 순으로 추가한다. gc1/gv1은 선택 출고, gc3/gv3는 작업장 신청재고의 행별 반납, gc2/gv2는 최근 1개월 신청내역에서 선택 재출고를 처리한다.

**웹과 Spring.** Expendables의 두 요청 원천·출고 확인·신청 이력, ExpendableReturns의 원출고별 부분 반납. `src/web/src/management/Expendables.tsx:32` · `src/api/src/main/java/com/shinjin/pop/management/ManagementDemoController.java:37`

**남은 차이.** 3탭과 분류 마스터 조회, 수량 키패드, 체크 출고 및 행 반납은 데모에 구현했다. 운영 최근 1개월 경계, 분류 마스터와 수불·품목·창고명은 실제 프로시저 결과셋 대조 대상이다.

**검증.** 이번 두 타일 진입. M1 합성 HTTP/Chrome에서 원출고·초과·재시도 검증. `.rework-m1-return-staging/release-44c751a/m1-return-review.md:1`

**원본 이벤트.** `POPMANAGEMENT/frmExpendables.cs:1661` · `POPMANAGEMENT/frmExpendables.cs:1655` · `POPMANAGEMENT/frmExpendables.cs:1650` · `POPMANAGEMENT/frmExpendables.cs:1221` · `POPMANAGEMENT/frmExpendables.cs:1666` · `POPMANAGEMENT/frmExpendables.cs:1226` · `POPMANAGEMENT/frmExpendables.cs:1330` · `POPMANAGEMENT/frmExpendables.cs:1278` · `POPMANAGEMENT/frmExpendables.cs:44`

| 하위 탭 | 입력·적용 및 웹 대응 |
|---|---|
| 소모품 목록 | 품목분류·대분류·중분류 재조회→현재고와 출고량 선택→출고 확인. 웹의 일반재고 원천과 수량 제한 대조 대상. `POPMANAGEMENT/frmExpendables.cs:415` |
| 소모품 신청재고 | 현재 작업장의 신청 잔량을 확인하고 행별 반납량을 편집한 뒤 반납한다. gc3 조회 470행, gv3 행 이벤트 1330행. `POPMANAGEMENT/frmExpendables.cs:470` |
| 최근 1개월 신청내역 | gc2 조회 521행, gv2 행 이벤트 1278행. 최근 신청 품목을 선택하고 현재고 범위에서 출고수량을 입력한 뒤 상단 소모품 출고로 재신청한다. `POPMANAGEMENT/frmExpendables.cs:521` · `POPMANAGEMENT/frmExpendables.cs:1278` |

**외부 선택창·보고서 호출.** `POPMANAGEMENT/frmExpendables.cs:253`


### frmProduction · 최종생산조회

**진입.** `MainMenu/frmMenu.cs:860`. 작업지시번호를 Enter로 누적 조회하고 Clear와 All Clear를 구분한다. 작업 한 건을 2행으로 묶은 표시 그리드를 선택 경로에 XLSX로 저장한다. 원본 내보내기는 합계 행을 생성하지 않는다.

**웹과 Spring.** FinalProductionReport와 FinalProductionReportController, 브라우저 XLSX 내보내기. `src/web/src/FinalProductionReport.tsx:18` · `src/api/src/main/java/com/shinjin/pop/drawing/FinalProductionReportController.java:24`

**남은 차이.** 원본 DevExpress와 웹 XLSX의 열·머리글·병합·행 높이 및 셀 스타일 ID를 합성 2행으로 대조했다. 현장 작업지시와 프로시저 결과 순서 대사가 남아 있다.

**검증.** Spring 데모·Chrome을 통해 조회 누적, 삭제, 저장 취소 및 저장 파일의 ZIP·XML을 검증했다. 과거 PACK2 샘플 검증 기록도 보관한다. `.rework-production-report-staging/production-report-review.md:1`

**원본 이벤트.** `POPMANAGEMENT/frmProduction.cs:196` · `POPMANAGEMENT/frmProduction.cs:203` · `POPMANAGEMENT/frmProduction.cs:104` · `POPMANAGEMENT/frmProduction.cs:209` · `POPMANAGEMENT/frmProduction.cs:35`

### frmRepair · 설비 수리내역

**진입.** `MainMenu/frmMenu.cs:842`. 기간과 완료조건으로 설비·이슈·발생/해결자·시간·결과를 조회한다. 이 메뉴의 폼에는 수리 요청 작성·저장 버튼이 없다.

**웹과 Spring.** RepairHistory의 날짜·상태 조회와 ManagementDemoController의 합성 행. `src/web/src/management/RepairHistory.tsx:8` · `src/api/src/main/java/com/shinjin/pop/management/ManagementDemoController.java:37`

**남은 차이.** 레거시 발생자·해결자 코드, 경과시간 등 열별 대사와 실제 사유/완료코드 매핑 미완.

**검증.** 격리 Spring 데모와 Chrome 터치로 기본 한 달, 세 완료여부, 날짜 역전 취소, 10개 열, 미완료 경과시간 색, 행 정렬·선택, 작업자 세션과 사업장 격리를 확인했다. 실제 이슈 행은 연결 시 대조한다. `.rework-m1-staging/m1-review.md:1`

**원본 이벤트.** `POPMANAGEMENT/frmRepair.cs:186` · `POPMANAGEMENT/frmRepair.cs:37`

## POPPRINT

### frmMaterialOption · 재질 선택

**진입.** `POPLGS/frmLogistics6.cs:2876` · `POPPRINT/frmWorkPrint.cs:3460`. 작업지시서와 출하 양쪽에서 기존 선택을 넘겨 열고 사용/재질코드·명을 체크한다. OK일 때만 목록과 코드를 호출자에 반환한다.

**웹과 Spring.** 출하에서 재질별 사용 체크·순번·재질코드·재질명, 저장·취소와 다음 조회 조건을 반영했다. 상세 기능·API는 Obsidian 18 「출하 전표와 업무 PDF」에 기록했다.

**운영 인수.** 작업지시 출력 폼의 독립 구현 여부는 그 폼의 검증 기록을 따른다.

**검증.** 2026-11-26 격리 Spring/Chrome과 동일 합성 값의 원본 폼 캡처. 분석 저장소 `.team/screen-review/web-parity/출하-화면대조.md` 참조.

**원본 이벤트.** `POPPRINT/frmMaterialOption.cs:45` · `POPPRINT/frmMaterialOption.cs:63` · `POPPRINT/frmMaterialOption.cs:38`

### frmOpmanBarCode · 사원번호 인쇄

**진입.** `MainMenu/frmMenu.cs:906`. 메뉴에서 비밀번호 확인 후 진입한다. 사업장/부서/사원을 조회·선택해 바코드 또는 QR 리포트 미리보기를 연다.

**웹과 Spring.** 작업자 바코드·QR 양식이 인증된 출력 목록에 있다. `src/web/src/output/OutputPreview.tsx:13` · `src/api/src/main/java/com/shinjin/pop/output/SyntheticOutputController.java:22`

**남은 차이.** 레거시 진입 비밀번호 또는 동등한 업무 권한, 실사원 다중 선택·매수·부서별 발행 미연결. 화면 로그인만으로 민감한 실사원 출력을 허용할 근거가 없다.

**검증.** 기존 합성 출력 인증·PDF 시험. 직원 마스터·실물 라벨 미검증. `.rework-device-staging/output-review.md:1`

**원본 이벤트.** `POPPRINT/frmOpmanBarCode.cs:300` · `POPPRINT/frmOpmanBarCode.cs:173` · `POPPRINT/frmOpmanBarCode.cs:132` · `POPPRINT/frmOpmanBarCode.cs:126` · `POPPRINT/frmOpmanBarCode.cs:271` · `POPPRINT/frmOpmanBarCode.cs:35`

사원번호 폼의 비밀번호 통과 후 호출과 두 미리보기 분기는 각각 `MainMenu/frmMenu.cs:896` · `POPPRINT/frmOpmanBarCode.cs:173` · `POPPRINT/frmOpmanBarCode.cs:300`

**외부 선택창·보고서 호출.** `POPPRINT/frmOpmanBarCode.cs:195` · `POPPRINT/frmOpmanBarCode.cs:322`

### frmProductOption · 계정구분

**진입.** `POPPRINT/frmWorkPrint.cs:4042`. 작업지시서의 계정구분에서 기존 목록을 열어 코드 다중선택→저장/취소로 부모 필터를 갱신한다.

**웹과 Spring.** OutputPreview에는 양식 선택만 있다. `src/web/src/output/OutputPreview.tsx:13` · `src/api/src/main/java/com/shinjin/pop/output/SyntheticOutputController.java:22`

**남은 차이.** 계정구분 목록·선택 코드와 실제 수주 조회 연계가 없다. 이 대화상자의 저장은 마스터 갱신이 아니다.

**검증.** 소스 대조. 브라우저 대응 시험 없음. `.rework-device-staging/output-review.md:1`

**원본 이벤트.** `POPPRINT/frmProductOption.cs:40` · `POPPRINT/frmProductOption.cs:58` · `POPPRINT/frmProductOption.cs:33`

### frmWorkPrint · 작업지시서 조회·양식 선택·출력

**진입.** `MainMenu/frmMenu.cs:878`. 수주일·작업반·재질·계정·출력/완료 여부로 조회하고 거래처 행으로 필터링한다. 선택/취소 뒤 Single·Multiple·Multiple1·Multiple2·Multiple3로 분기한다. 수주삭제와 출력 횟수 반영도 별도 이벤트다.

**웹과 Spring.** OutputPreview, SyntheticOutputController의 양식 선택·미리보기·PDF. 계획/출하 화면의 문서도 별도 존재한다. `src/web/src/output/OutputPreview.tsx:13` · `src/api/src/main/java/com/shinjin/pop/output/SyntheticOutputController.java:22`

**남은 차이.** 선택한 실제 수주 묶음에서 양식을 생성하는 계약, 원 수주 삭제 권한·처리와 출력 횟수 갱신, 거래처·재질·규격별 분할 및 물리 출력은 미대응.

**검증.** 이번 Chrome 양식 선택과 미리보기 요청. 기존 output-review는 글꼴·권한·PDF 합성 시험이며 원본 행 대사는 미실행. `.rework-device-staging/output-review.md:1`

**원본 이벤트.** `POPPRINT/frmWorkPrint.cs:4147` · `POPPRINT/frmWorkPrint.cs:4040` · `POPPRINT/frmWorkPrint.cs:3473` · `POPPRINT/frmWorkPrint.cs:3458` · `POPPRINT/frmWorkPrint.cs:587` · `POPPRINT/frmWorkPrint.cs:467` · `POPPRINT/frmWorkPrint.cs:541` · `POPPRINT/frmWorkPrint.cs:533` · `POPPRINT/frmWorkPrint.cs:549` · `POPPRINT/frmWorkPrint.cs:67`

| 선택 양식/별도 동선 | 레거시 분기와 웹의 검증 한계 |
|---|---|
| Single | 선택 수주 단건 리포트와 작업지시 번호. 웹의 양식 PDF 또는 정적 예제와 실제 선택 행 대사는 미검증. `POPPRINT/frmWorkPrint.cs:641` |
| Multiple | 선택 수주 묶음, 원본 실제 분기·그룹별 페이지. 웹의 양식 PDF 또는 정적 예제와 실제 선택 행 대사는 미검증. `POPPRINT/frmWorkPrint.cs:641` |
| Multiple1 | PLATE 품목별 바코드와 거래처 묶음. 웹의 양식 PDF 또는 정적 예제와 실제 선택 행 대사는 미검증. `POPPRINT/frmWorkPrint.cs:1163` |
| Multiple2 | 물류반 거래처별 장수. 웹의 양식 PDF 또는 정적 예제와 실제 선택 행 대사는 미검증. `POPPRINT/frmWorkPrint.cs:1725` |
| Multiple3 | 거래처·재질·규격별 분리. 웹의 양식 PDF 또는 정적 예제와 실제 선택 행 대사는 미검증. `POPPRINT/frmWorkPrint.cs:2862` |
| 수주삭제 | 수주 스캔·확인 이후 원 주문 상태 반영. 웹의 양식 PDF 또는 정적 예제와 실제 선택 행 대사는 미검증. `POPPRINT/frmWorkPrint.cs:3473` |

cPrint3 구현도 남아 있다. 현재 출력 선택 이벤트의 Multiple3 호출 대상은 cPrint4다. `POPPRINT/frmWorkPrint.cs:621`

**외부 선택창·보고서 호출.** `POPPRINT/frmWorkPrint.cs:598` · `POPPRINT/frmWorkPrint.cs:1041` · `POPPRINT/frmWorkPrint.cs:1240` · `POPPRINT/frmWorkPrint.cs:1803` · `POPPRINT/frmWorkPrint.cs:2352` · `POPPRINT/frmWorkPrint.cs:2939` · `POPPRINT/frmWorkPrint.cs:3493`

## 메뉴에서 숨긴 경로와 프로젝트 밖의 보조 경계

물류 구형 출고, 관리 불량내역·설비 수리의뢰, 인쇄 재고 라벨은 원본 부모 타일이 숨김이다. 웹의 포장 라벨 PDF를 원본 재고 라벨 메뉴 완료로 집계하지 않았다. `MainMenu/frmMenu.Designer.cs:775` · `MainMenu/frmMenu.Designer.cs:1293` · `MainMenu/frmMenu.Designer.cs:1325` · `MainMenu/frmMenu.Designer.cs:1436`

COMMON의 수주 스캔·양식 선택·사업장/창고/위치/의뢰번호/재질 선택창, REPORT 양식은 위 호출 폼 아래에 연결했다. POPRFID의 UploadFTP는 폼 외부 파일 전송 클래스다. 전송/삭제·실물 촬영을 이번 검증에서 호출하지 않았다. POPRFID와 POPPRINT의 Program.cs 안에 주석으로 남은 독립 실행 예시는 메뉴 진입 근거에서 제외했다.

## 기존 MSSQL 호출 계약 · 연결 전 인계

Spring의 향후 연결 단위는 호출 이름, 호출 컨텍스트(POP/ERP), 순서와 방향이 있는 인수, 결과셋/OUT, 트랜잭션 경계와 재시도 규칙이다. 아래 목록은 C#에 남은 실행 문자열과 CommandType.StoredProcedure를 정적으로 추적했다. 정의는 원본 SQL 폴더의 스크립트만 대조했다. 여러 정의·롤백본이 있어도 운영 버전을 지정하지 않았다. 표의 호출부 인수는 코드에서 식별한 이름이며 SQL Server의 정식 타입·길이·기본값을 보증하지 않는다. 동적 문자열·분기·공통 helper 안의 호출은 링크 원문에서 재확인이 필요하다.

| 호출군 | 확인된 결과·오류·부작용과 연결 조건 |
|---|---|
| 공장이송 채번·저장·삭제 | 의뢰 저장의 NEOE.CP_GETNO는 회사·모듈(PU)·문서분류(08)·연월 입력, P_NO NVARCHAR(20) OUTPUT을 후속 헤더/라인에 사용한다. false면 POP/ERP 양쪽 트랜잭션 rollback을 시도하고 오류를 표시한다. 연결 사이의 커밋을 하나의 원자적 성공으로 가정할 수 없다. 채번/전표가 이미 반영되었는지 확인할 방법 없이 자동 재실행하면 안 된다. `POPLGS/frmLogistics1.cs:1971` |
| ESCO·발주입고 | ESCO는 스캔 조회 후 생성·월재고 후처리·POP 반영으로 이어진다. 발주 자동 반영은 회사 1000, ERP 사업장(원본 000001이면 2000, 그 외 해당 코드 경로는 1000), 선택일 yyyyMMdd를 시작일·종료일로 전달한다. 반환 bool은 C# 실행 helper의 성공 여부다. 실제 처리 행 수나 SP RETURN 코드로 간주할 수 없다. 실패 시 rollback 및 화면 오류, 성공 후 조회. `POPLGS/frmLogistics4.cs:284` · `POPLGS/frmLogistics7.cs:105` |
| 출하 | 현재시간/월말, 헤더번호, 항번, LOT순번 조회와 TSA402·403·403L 및 ERP 의뢰/상세 생성은 서로 다른 호출이다. 완료삭제 호출과 일반 삭제를 분리해야 한다. 재실행 시 원전표·재고·ERP 대응 전표를 함께 확인할 식별자가 필요하다. 저장소 정의는 아래 링크에 표시했다. |
| RFID | 스칼라 count로 존재 여부를 확인하는 호출과 등록·매칭·입출고 저장이 분리된다. 매칭 해제는 SP가 아닌 원본 인라인 UPDATE이며, 사진은 별도 파일 전송이 수반된다. DB 성공이 파일 저장 성공을 보장하지 않는다. `POPRFID/FrmTagInOutReg.cs:93` · `POPRFID/FrmPalletMatch.cs:593` |
| 관리 | 수리조회 SP_POP_CALL_01_LIST는 DIVISION=REPAIR_LIST, PLANT_CODE, EQUIP_SYS_CD, SDATE, EDATE, CLEAR를 받고 DataTable을 그리드에 연결한다. 소모품 목록·잔량 조회와 출고·반납용 저장 호출은 별개다. 실적조회는 조회 행을 엑셀 파일로 내보낸다. 엑셀 저장이 생산 원장을 갱신한다는 근거는 없다. `POPMANAGEMENT/frmRepair.cs:207` |
| 출력 | 수주 선택 결과와 여러 리포트 데이터셋을 구성하는 읽기, 출력 횟수 반영 SP_POP_PRINT_CNT_IUD, 수주 삭제/상태 변경을 분리한다. 미리보기 요청을 반복할 때 레거시 횟수 증가를 자동 재현하지 않는다. 재출력·미리보기·물리 제출의 확정 시점은 설치본/운영 확인 대상이다. `POPPRINT/frmWorkPrint.cs:1105` |

**아래 정의 링크의 의미.** 저장소 SQL 스크립트에 CREATE/ALTER 본문이 있는 위치다. DROP/CREATE·롤백·진단 스크립트는 모두 읽기만 했다. 호출 뒤의 행셋/스칼라/실행 표시는 클라이언트가 소비하는 방식이다. 정의 미확인 호출의 RETURN 값, 업무 오류 코드, 트리거 연쇄 효과와 격리 수준은 미확정으로 둔다.

### frmItemKind3의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPLGS/frmItemKind3.cs:156` | @FACTORY_CODE | `POPLGS/frmItemKind3.cs:165` | 이 조사에서 본문 미확인 |

### frmLogistics1의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPLGS/frmLogistics1.cs:113` | @factory_code, @plant_code, @search_date, @output_req_no | 분기·공통 실행부 참조 | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics1.cs:130` | 호출부 참조 | `POPLGS/frmLogistics1.cs:136` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics1.cs:351` | @FACTORY_CODE, @OUTPUT_REQ_NO, @MAT_SEQ | `POPLGS/frmLogistics1.cs:363` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics1.cs:396` | @P_NO_GIREQ, @P_NO_LINE, @P_CD_COMPANY, @P_ID_DELETE_EMP, @P_ID_DELETE | `POPLGS/frmLogistics1.cs:415` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics1.cs:431` | @P_NO_GIREQ, @P_CD_COMPANY, @P_ID_DELETE_EMP, @P_ID_DELETE | `POPLGS/frmLogistics1.cs:447` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics1.cs:803` | @P_NO_GIREQ, @P_CD_COMPANY, @P_ID_DELETE_EMP, @P_ID_DELETE | `POPLGS/frmLogistics1.cs:819` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics1.cs:1512` | @factory_code, @material_quality, @thickness, @spec_x, @spec_y, @item_kind1, @item_kind2, @item_kind3, @OUT_PLANT_CODE | `POPLGS/frmLogistics1.cs:1536` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics1.cs:1686` | @factory_code, @material_quality, @thickness, @spec_x, @spec_y, @item_kind1, @item_kind2, @item_kind3, @PLANT_CODE, @IN_PLANT_CODE, @OUT_PLANT_CODE, @WAREHOUSE_CODE_IN | `POPLGS/frmLogistics1.cs:1718` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics1.cs:1971` | @P_CD_COMPANY, @P_CD_MODULE, @P_CD_CLASS, @P_DOCU_YM, @P_NO | `POPLGS/frmLogistics1.cs:1987` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics1.cs:2002` | @P_NO_GIREQ, @P_CD_PLANT, @P_CD_GIPLANT, @P_CD_COMPANY, @P_DT_GIREQ, @P_FG_GIREQ, @P_FG_GI, @P_CD_DEPT, @P_NO_EMP, @P_DC50_PO, @P_CD_PARTNER, @P_DC_RMK2, @P_GI_PARTNER, @P_YN_APP, @P_CD_USERDEF1, @P_TXT_USERDEF1 | `POPLGS/frmLogistics1.cs:2042` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics1.cs:2131` | @P_NO_GIREQ, @P_NO_LINE, @P_CD_PLANT, @P_CD_COMPANY, @P_CD_ITEM, @P_DT_DELIVERY, @P_QT_GIREQ, @P_QT_GI, @P_CD_SL, @P_CD_GRSL, @P_NM_CUST_DLV, @P_CD_ZIP, @P_ADDR1, @P_ADDR2, @P_NO_TEL_D1, @P_NO_TEL_D2, @P_TP_DLV, @P_DC_REQ, @P_FG_TRACK_L, @P_CD_WC, @P_CD_WCOP, @P_QT_PO_MM, @P_ID_INSERT_EMP, @P_ID_INSERT, @P_CD_WORKITEM, @P_QT_WORK, @P_CD_PJT, @P_SEQ_PROJECT, @P_QT_WEIGHT, @P_UNIT_WEIGHT, @P_TP_DLV_DUE, @P_CD_EXCH, @P_RT_EXCH, @P_UM, @P_UM_EX, @P_UM_EX_PSO, @P_AM, @P_AM_EX, @P_DT_REC, @P_DC_RMK, @P_NO_SO, @P_SEQ_SO, @P_SEQ_MGMT, @P_NO_WBS, @P_NO_CBS, @P_NO_LOT_DISP, @P_NO_MREQ, @P_NO_MREQLINE, @P_NO_LINE_PJTBOM, @P_QT_MGREQ, @P_FG_POST, @P_GI_PARTNER, @P_CD_ITEM_REF, @P_YN_PICKING, @P_FG_GUBUN, @P_NO_ORDER, @P_NM_CUST, @P_NO_TEL1, @P_NO_TEL2, @P_DLV_TXT_USERDEF1, @P_DLV_CD_USERDEF1, @P_CD_USERDEF3, @P_NO_LINK, @P_NO_LINE_LINK, @P_CD_CC, @P_NM_USERDEF1, @P_NM_USERDEF2, @P_DATE_USERDEF1, @P_CD_GRPLANT, @P_TXT_USERDEF1, @P_NUM_USERDEF1, @P_NUM_USERDEF2, @P_NO_WO, @P_TXT_USERDEF2, @P_NUM_USERDEF3, @P_CD_USERDEF4, @P_TXT_USERDEF3, @P_TXT_USERDEF4 | `POPLGS/frmLogistics1.cs:2295` | 이 조사에서 본문 미확인 |

### frmLogistics2의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPLGS/frmLogistics2.cs:90` | @factory_code, @date_from, @date_to, @output_req_no, @plant_code_in, @warehouse_code_in, @plant_code_out, @warehouse_code_out | 분기·공통 실행부 참조 | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics2.cs:100` | @factory_code, @date_from, @date_to, @output_req_no, @plant_code_in, @warehouse_code_in, @plant_code_out, @warehouse_code_out | `POPLGS/frmLogistics2.cs:117` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics2.cs:163` | 호출부 참조 | `POPLGS/frmLogistics2.cs:170` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics2.cs:176` | @factory_code, @output_no, @output_req_no, @mat_seq, @material_code | 분기·공통 실행부 참조 | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics2.cs:183` | @factory_code, @output_no, @output_req_no, @mat_seq, @material_code | `POPLGS/frmLogistics2.cs:197` | 이 조사에서 본문 미확인 |

### frmLogistics3의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPLGS/frmLogistics3.cs:487` | @DT_FROM, @DT_TO, @CD_COMPANY, @NO_EMP, @CD_QTIOTP, @CD_PLANT, @CD_SL, @P_FG_LANG | `POPLGS/frmLogistics3.cs:510` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics3.cs:514` | @DT_FROM, @DT_TO, @CD_PLANT_RCV, @CD_SL_REF, @CD_COMPANY, @NO_EMP, @CD_QTIOTP, @CD_PLANT, @CD_SL, @FG_TYPE, @P_FG_LANG | `POPLGS/frmLogistics3.cs:545` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics3.cs:634` | @P_NO_IO, @P_CD_COMPANY, @P_FG_LANG | `POPLGS/frmLogistics3.cs:653` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics3.cs:778` | @DT_FROM, @DT_TO, @CD_PLANT_RCV, @CD_SL_REF, @CD_COMPANY, @NO_EMP, @CD_QTIOTP, @CD_PLANT, @CD_SL, @FG_TYPE, @P_FG_LANG | `POPLGS/frmLogistics3.cs:809` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics3.cs:876` | @CD_COMPANY, @NO_IO, @P_FG_LANG | `POPLGS/frmLogistics3.cs:889` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics3.cs:1167` | @FACTORY_CODE, @OLD_OUTPUT_REQ_NO, @OLD_OUTPUT_REQ_SEQNO, @OLD_OUTPUT_NO, @OLD_OUTPUT_SEQNO, @PLANT_CODE, @OUT_PLANT_CODE_ETC, @OUT_WAREHOUSE_CODE_ETC, @IN_PLANT_CODE_ETC, @IN_WAREHOUSE_CODE_ETC, @PART_NO, @ORDER_QTY, @OPMAN_CODE, @OPMAN_DEPT | `POPLGS/frmLogistics3.cs:1201` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics3.cs:1215` | @P_CD_COMPANY, @P_CD_MODULE, @P_CD_CLASS, @P_DOCU_YM, @P_NO | `POPLGS/frmLogistics3.cs:1231` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics3.cs:1246` | @P_NO_IO, @P_CD_COMPANY, @P_CD_PLANT, @P_CD_PARTNER, @P_FG_TRANS, @P_YN_RETURN, @P_DT_IO, @P_GI_PARTNER, @P_CD_DEPT, @P_NO_EMP, @P_DC_RMK, @P_ID_INSERT, @P_CD_QTIOTP | `POPLGS/frmLogistics3.cs:1278` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics3.cs:1315` | @P_YN_RETURN, @P_NO_IO, @P_NO_IOLINE, @P_CD_COMPANY, @P_CD_PLANT, @P_CD_SL, @P_DT_IO, @P_CD_QTIOTP, @P_CD_PARTNER, @P_CD_ITEM, @P_QT_GOOD_INV, @P_QT_REJECT_INV, @P_AM, @P_NO_IO_MGMT, @P_NO_IOLINE_MGMT, @P_CD_PLANT_RCV, @P_CD_SL_REF, @P_NO_EMP, @P_ID_INSERT, @P_CD_PJT | `POPLGS/frmLogistics3.cs:1361` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics3.cs:1450` | @FACTORY_CODE, @NO_IO | `POPLGS/frmLogistics3.cs:1460` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics3.cs:1472` | @P_NO_IO, @P_CD_COMPANY | `POPLGS/frmLogistics3.cs:1483` | 이 조사에서 본문 미확인 |

### frmLogistics4의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPLGS/frmLogistics4.cs:84` | @factory_code, @date_from, @date_to, @shipplan_seq, @matquality | 분기·공통 실행부 참조 | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics4.cs:91` | @factory_code, @date_from, @date_to, @shipplan_seq, @matquality | `POPLGS/frmLogistics4.cs:103` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics4.cs:172` | @P_CD_COMPANY, @P_DT_FR, @P_DT_TO, @P_NO_GI_E | `POPLGS/frmLogistics4.cs:186` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics4.cs:284` | @P_CD_COMPANY, @P_DT_FR, @P_DT_TO, @P_NO_GIR | `POPLGS/frmLogistics4.cs:298` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics4.cs:316` | @P_CD_SL, @P_CD_PLANT, @P_CD_COMPANY, @P_CD_ITEM, @P_DT_FR, @P_DT_TO | `POPLGS/frmLogistics4.cs:334` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics4.cs:369` | @P_CD_COMPANY, @P_NO_GI_E, @OPMAN_CODE, @OPMAN_DEPT, @OPTIME | `POPLGS/frmLogistics4.cs:385` | `SQL/FIX_SP_POP_ESCO_AUTO_20261120.sql:28` · `SQL/ROLLBACK_SP_POP_ESCO_AUTO_20261120.sql:10` / 복수 스크립트, 설치본 미확정 |

### frmLogistics5의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPLGS/frmLogistics5.cs:66` | @factory_code, @output_no | `POPLGS/frmLogistics5.cs:77` | 이 조사에서 본문 미확인 |

### frmLogistics6의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPLGS/frmLogistics6.cs:133` | 호출부 참조 | 분기·공통 실행부 참조 | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:192` | @factory_code, @plant_code, @date_from, @date_to, @customer_code, @matquality, @item_kind3, @WORKCENTER_CODE, @OPMAN_NAME, @CARRY_OVER_FLAG | `POPLGS/frmLogistics6.cs:230` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:239` | @P_CD_COMPANY, @P_DT_SO_FROM, @P_DT_SO_TO, @P_CD_PLANT, @P_TP_BUSI, @P_CD_PARTNER, @P_CD_SALEGRP, @P_CD_SL, @P_NO_PROJECT, @P_NO_EMP, @P_CD_ITEM, @P_DT_GUBUN, @P_YN_RETURN, @P_TP_VAT, @P_CD_EXCH, @P_FG_TAXP, @P_TP_PRICE, @P_GI_PARTNER, @P_TP_GI, @P_NO_PO_PARTNER, @P_RE_CALE, @P_DC_RMK, @P_DC_RMK1, @P_MULTI_GRP_MFG, @P_TABNAME, @P_NO_EMP_LOGIN, @P_NO_SO, @P_TP_SO, @P_FG_LANG | `POPLGS/frmLogistics6.cs:304` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:401` | @SHIPPLAN_SEQ, @ORDER_NO, @ORDER_SEQNO | `POPLGS/frmLogistics6.cs:413` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:502` | @factory_code, @plant_code, @date_from, @date_to, @customer_code, @matquality, @item_kind3, @WORKCENTER_CODE, @OPMAN_NAME, @CARRY_OVER_FLAG | `POPLGS/frmLogistics6.cs:534` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:543` | @P_CD_COMPANY, @P_DT_SO_FROM, @P_DT_SO_TO, @P_CD_PLANT, @P_TP_BUSI, @P_CD_PARTNER, @P_CD_SALEGRP, @P_CD_SL, @P_NO_PROJECT, @P_NO_EMP, @P_CD_ITEM, @P_DT_GUBUN, @P_YN_RETURN, @P_TP_VAT, @P_CD_EXCH, @P_FG_TAXP, @P_TP_PRICE, @P_GI_PARTNER, @P_TP_GI, @P_NO_PO_PARTNER, @P_RE_CALE, @P_DC_RMK, @P_DC_RMK1, @P_MULTI_GRP_MFG, @P_TABNAME, @P_NO_EMP_LOGIN, @P_NO_SO, @P_TP_SO, @P_FG_LANG | `POPLGS/frmLogistics6.cs:608` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:744` | @PLANT_CODE, @OPTIME, @CUSTOMER_CODE | `POPLGS/frmLogistics6.cs:757` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:862` | @division, @factory_code, @plant_code | `POPLGS/frmLogistics6.cs:876` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:922` | @FACTORY_CODE | `POPLGS/frmLogistics6.cs:931` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:1008` | @FACTORY_CODE, @PLANT_CODE | `POPLGS/frmLogistics6.cs:1019` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:1281` | @factory_code, @plant_code, @shipplan_seq | 분기·공통 실행부 참조 | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:1286` | @factory_code, @plant_code, @shipplan_seq | `POPLGS/frmLogistics6.cs:1299` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:1665` | 호출부 참조 | `POPLGS/frmLogistics6.cs:1669` | `SQL/SP_POP_LGS_LOGISTICS6_PROCEDURES.sql:18` |
| `POPLGS/frmLogistics6.cs:1823` | @P_CD_COMPANY, @P_NO_SO, @P_CD_PLANT, @P_TP_BUSI, @P_CD_SL, @P_NO_PROJECT, @P_CD_ITEM, @P_DT_SO_FROM, @P_DT_SO_TO, @P_DT_GUBUN, @P_RE_CALE, @P_NO_PO_PARTNER, @P_GI_PARTNER, @P_MULTI_GRP_MFG, @P_FG_LANG | `POPLGS/frmLogistics6.cs:1860` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:1942` | @factory_code, @today | `POPLGS/frmLogistics6.cs:1951` | `SQL/SP_POP_LGS_LOGISTICS6_PROCEDURES.sql:38` / 선언 @factory_code VARCHAR(6), @today VARCHAR(8) |
| `POPLGS/frmLogistics6.cs:1962` | @P_CD_COMPANY, @P_CD_MODULE, @P_CD_CLASS, @P_DOCU_YM, @P_NO | `POPLGS/frmLogistics6.cs:1979` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:1995` | @P_CD_COMPANY, @P_CD_MODULE, @P_CD_CLASS, @P_DOCU_YM, @P_NO | `POPLGS/frmLogistics6.cs:2012` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:2029` | @factory_code, @shipping_no, @shipping_date, @shipping_time, @delivery_customer, @customer_code, @charge_code, @opman_code, @optime | `POPLGS/frmLogistics6.cs:2048` | `SQL/SP_POP_LGS_LOGISTICS6_PROCEDURES.sql:105` / 선언 @factory_code VARCHAR(6), @shipping_no VARCHAR(12), @shipping_date VARCHAR(8), @shipping_time VARCHAR(4), @delivery_customer VARCHAR(10), @customer_code VARCHAR(10), @charge_code VARCHAR(10), @opman_code VARCHAR(10), @optime VARCHAR(14) / 본문 INSERT INTO TSA402 |
| `POPLGS/frmLogistics6.cs:2062` | @P_CD_COMPANY, @P_NO_GIR, @P_NO_SO, @P_NO_IO, @P_CD_DEPT, @P_TP_BUSI, @P_DT_GI, @P_DC_RMK, @P_DC_RMK1, @P_DC_RMK2, @P_NO_EMP, @P_YN_RETURN, @P_ID_INSERT | `POPLGS/frmLogistics6.cs:2096` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:2291` | @factory_code, @shipping_no | `POPLGS/frmLogistics6.cs:2300` | `SQL/SP_POP_LGS_LOGISTICS6_PROCEDURES.sql:60` / 선언 @factory_code VARCHAR(6), @shipping_no VARCHAR(12) |
| `POPLGS/frmLogistics6.cs:2307` | @factory_code, @shipping_no, @shipping_seqno, @order_no, @order_histno, @order_seqno, @item_code, @shipplan_seq, @shipplan_gbn, @shipping_qty, @opman_code, @optime, @old_shipping_reqno, @old_shipping_no, @old_shipping_seqno | `POPLGS/frmLogistics6.cs:2334` | `SQL/SP_POP_LGS_LOGISTICS6_PROCEDURES.sql:137` / 선언 @factory_code VARCHAR(6), @shipping_no VARCHAR(12), @shipping_seqno INT, @order_no VARCHAR(12), @order_histno INT, @order_seqno INT, @item_code VARCHAR(20), @shipplan_seq VARCHAR(20), @shipplan_gbn VARCHAR(6), @shipping_qty DECIMAL(18,4), @opman_code VARCHAR(10), @optime VARCHAR(14), @old_shipping_reqno VARCHAR(20), @old_shipping_no VARCHAR(20), @old_shipping_seqno INT / 본문 INSERT INTO TSA403 |
| `POPLGS/frmLogistics6.cs:2350` | @P_CD_COMPANY, @P_NO_GIR, @P_NO_SO, @P_SEQ_SO, @P_NO_IO, @P_NO_IOLINE, @P_CD_SL, @P_NO_EMP, @P_QT_GI, @P_UM, @P_AM_GIR, @P_AM_GIRAMT, @P_AM_VAT, @P_UNIT, @P_QT_GIR_IM, @P_DC_RMK3, @P_DC_RMK4, @P_RT_EXCH, @P_NO_LC, @P_SEQ_LC, @P_SEQ_PROJECT, @P_YN_RETURN, @P_ID_INSERT, @P_TXT_USERDEF1, @P_TXT_USERDEF2, @P_NUM_USERDEF1, @P_NUM_USERDEF2, @P_NM_USERDEF1 | `POPLGS/frmLogistics6.cs:2416` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:2432` | @factory_code, @shipping_no, @shipping_seqno | `POPLGS/frmLogistics6.cs:2442` | `SQL/SP_POP_LGS_LOGISTICS6_PROCEDURES.sql:83` / 선언 @factory_code VARCHAR(6), @shipping_no VARCHAR(12), @shipping_seqno INT |
| `POPLGS/frmLogistics6.cs:2449` | @factory_code, @shipping_no, @shipping_seqno, @lot_seq, @lot_no, @out_warehouse_code, @out_location_code, @output_date, @output_qty, @opman_code, @optime | `POPLGS/frmLogistics6.cs:2471` | `SQL/SP_POP_LGS_LOGISTICS6_PROCEDURES.sql:179` / 선언 @factory_code VARCHAR(6), @shipping_no VARCHAR(12), @shipping_seqno INT, @lot_seq INT, @lot_no VARCHAR(20), @out_warehouse_code VARCHAR(6), @out_location_code VARCHAR(6), @output_date VARCHAR(20), @output_qty DECIMAL(18,4), @opman_code VARCHAR(10), @optime VARCHAR(14) / 본문 INSERT INTO TSA403L |
| `POPLGS/frmLogistics6.cs:3174` | @FACTORY_CODE, @SHIPPING_NO, @SHIPPING_SEQNO, @LOT_SEQ, @LOT_NO, @WAREHOUSE_CODE, @LOCATION_CODE | `POPLGS/frmLogistics6.cs:3190` | `SQL/SP_POP_LGS_LOGISTICS6_PROCEDURES.sql:213` / 선언 @factory_code VARCHAR(6), @shipping_no VARCHAR(12), @shipping_seqno INT, @lot_seq INT, @lot_no VARCHAR(20), @warehouse_code VARCHAR(6), @location_code VARCHAR(6) |
| `POPLGS/frmLogistics6.cs:3204` | @FACTORY_CODE, @SHIPPING_NO, @SHIPPING_SEQNO, @ITEM_CODE, @ORDER_NO, @ORDER_HISTNO, @ORDER_SEQNO | `POPLGS/frmLogistics6.cs:3220` | `SQL/SP_POP_LGS_LOGISTICS6_PROCEDURES.sql:242` / 선언 @factory_code VARCHAR(6), @shipping_no VARCHAR(12), @shipping_seqno INT, @item_code VARCHAR(20), @order_no VARCHAR(12), @order_histno INT, @order_seqno INT |
| `POPLGS/frmLogistics6.cs:3235` | @SHIPPING_NO | `POPLGS/frmLogistics6.cs:3243` | `SQL/SP_POP_LGS_LOGISTICS6_PROCEDURES.sql:272` / 선언 @shipping_no VARCHAR(12) |
| `POPLGS/frmLogistics6.cs:3251` | @SHIPPING_NO | `POPLGS/frmLogistics6.cs:3259` | `SQL/SP_POP_LGS_LOGISTICS6_PROCEDURES.sql:290` / 선언 @shipping_no VARCHAR(12) |
| `POPLGS/frmLogistics6.cs:3277` | @P_CD_COMPANY, @P_NO_IO, @P_NO_IOLINE, @P_NO_GIR, @P_SEQ_GIR, @P_NO_SO | `POPLGS/frmLogistics6.cs:3296` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:3425` | @factory_code, @plant_code, @shipplan_seq | 분기·공통 실행부 참조 | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:3430` | @factory_code, @plant_code, @shipplan_seq | `POPLGS/frmLogistics6.cs:3442` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:3690` | @CUSTOMER_CODE, @SA_CUSTOMER_CODE | `POPLGS/frmLogistics6.cs:3700` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:3963` | @PLANT_CODE, @SHIPPING_NO | `POPLGS/frmLogistics6.cs:3976` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:4045` | @CUSTOMER_CODE, @SA_CUSTOMER_CODE | `POPLGS/frmLogistics6.cs:4056` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:4450` | @PLANT_CODE, @SHIPPING_NO | `POPLGS/frmLogistics6.cs:4463` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics6.cs:4532` | @CUSTOMER_CODE, @SA_CUSTOMER_CODE | `POPLGS/frmLogistics6.cs:4543` | 이 조사에서 본문 미확인 |

### frmLogistics7의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPLGS/frmLogistics7.cs:105` | @CD_COMPANY, @CD_PLANT, @DT_FROM, @DT_TO | `POPLGS/frmLogistics7.cs:119` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics7.cs:192` | @CD_COMPANY, @CD_PLANT, @DT_FROM, @DT_TO | `POPLGS/frmLogistics7.cs:207` | 이 조사에서 본문 미확인 |

### frmLogistics8의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPLGS/frmLogistics8.cs:563` | @division, @factory_code, @plant_code, @warehouse_code, @material_quality, @thicknes, @spec_x, @work_status2, @spec_y, @location_code | `POPLGS/frmLogistics8.cs:592` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:1120` | @P_CD_COMPANY, @P_CD_MODULE, @P_CD_CLASS, @P_DOCU_YM, @P_NO | `POPLGS/frmLogistics8.cs:1136` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:1151` | @P_NO_GIREQ, @P_CD_PLANT, @P_CD_GIPLANT, @P_CD_COMPANY, @P_DT_GIREQ, @P_FG_GIREQ, @P_FG_GI, @P_CD_DEPT, @P_NO_EMP, @P_DC50_PO, @P_CD_PARTNER, @P_DC_RMK2, @P_GI_PARTNER, @P_YN_APP, @P_CD_USERDEF1, @P_TXT_USERDEF1 | `POPLGS/frmLogistics8.cs:1189` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:1278` | @P_NO_GIREQ, @P_NO_LINE, @P_CD_PLANT, @P_CD_COMPANY, @P_CD_ITEM, @P_DT_DELIVERY, @P_QT_GIREQ, @P_QT_GI, @P_CD_SL, @P_CD_GRSL, @P_NM_CUST_DLV, @P_CD_ZIP, @P_ADDR1, @P_ADDR2, @P_NO_TEL_D1, @P_NO_TEL_D2, @P_TP_DLV, @P_DC_REQ, @P_FG_TRACK_L, @P_CD_WC, @P_CD_WCOP, @P_QT_PO_MM, @P_ID_INSERT_EMP, @P_ID_INSERT, @P_CD_WORKITEM, @P_QT_WORK, @P_CD_PJT, @P_SEQ_PROJECT, @P_QT_WEIGHT, @P_UNIT_WEIGHT, @P_TP_DLV_DUE, @P_CD_EXCH, @P_RT_EXCH, @P_UM, @P_UM_EX, @P_UM_EX_PSO, @P_AM, @P_AM_EX, @P_DT_REC, @P_DC_RMK, @P_NO_SO, @P_SEQ_SO, @P_SEQ_MGMT, @P_NO_WBS, @P_NO_CBS, @P_NO_LOT_DISP, @P_NO_MREQ, @P_NO_MREQLINE, @P_NO_LINE_PJTBOM, @P_QT_MGREQ, @P_FG_POST, @P_GI_PARTNER, @P_CD_ITEM_REF, @P_YN_PICKING, @P_FG_GUBUN, @P_NO_ORDER, @P_NM_CUST, @P_NO_TEL1, @P_NO_TEL2, @P_DLV_TXT_USERDEF1, @P_DLV_CD_USERDEF1, @P_CD_USERDEF3, @P_NO_LINK, @P_NO_LINE_LINK, @P_CD_CC, @P_NM_USERDEF1, @P_NM_USERDEF2, @P_DATE_USERDEF1, @P_CD_GRPLANT, @P_TXT_USERDEF1, @P_NUM_USERDEF1, @P_NUM_USERDEF2, @P_NO_WO, @P_TXT_USERDEF2, @P_NUM_USERDEF3, @P_CD_USERDEF4, @P_TXT_USERDEF3, @P_TXT_USERDEF4 | `POPLGS/frmLogistics8.cs:1440` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:1520` | @P_CD_COMPANY, @P_CD_MODULE, @P_CD_CLASS, @P_DOCU_YM, @P_NO | `POPLGS/frmLogistics8.cs:1536` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:1551` | @P_NO_IO, @P_CD_COMPANY, @P_CD_PLANT, @P_CD_PARTNER, @P_FG_TRANS, @P_YN_RETURN, @P_DT_IO, @P_GI_PARTNER, @P_CD_DEPT, @P_NO_EMP, @P_DC_RMK, @P_ID_INSERT, @P_CD_QTIOTP | `POPLGS/frmLogistics8.cs:1583` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:1678` | @YN_RETURN, @NO_IO, @NO_IOLINE, @CD_COMPANY, @CD_PLANT, @CD_SL, @DT_IO, @NO_ISURCV, @NO_ISURCVLINE, @CD_QTIOTP, @CD_PARTNER, @CD_ITEM, @QT_GOOD_INV, @QT_REJECT_INV, @CD_PJT, @NO_EMP, @CD_PLANT_RCV, @CD_SL_REF, @FG_TRANS, @YN_AM, @UM, @AM, @CD_USERDEF1 | `POPLGS/frmLogistics8.cs:1730` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:1907` | @P_CD_COMPANY, @P_CD_MODULE, @P_CD_CLASS, @P_DOCU_YM, @P_NO | `POPLGS/frmLogistics8.cs:1923` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:1938` | @P_NO_IO, @P_CD_COMPANY, @P_CD_PLANT, @P_CD_PARTNER, @P_FG_TRANS, @P_YN_RETURN, @P_DT_IO, @P_GI_PARTNER, @P_CD_DEPT, @P_NO_EMP, @P_DC_RMK, @P_ID_INSERT, @P_CD_QTIOTP | `POPLGS/frmLogistics8.cs:1970` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:2007` | @P_YN_RETURN, @P_NO_IO, @P_NO_IOLINE, @P_CD_COMPANY, @P_CD_PLANT, @P_CD_SL, @P_DT_IO, @P_CD_QTIOTP, @P_CD_PARTNER, @P_CD_ITEM, @P_QT_GOOD_INV, @P_QT_REJECT_INV, @P_AM, @P_NO_IO_MGMT, @P_NO_IOLINE_MGMT, @P_CD_PLANT_RCV, @P_CD_SL_REF, @P_NO_EMP, @P_ID_INSERT, @P_CD_PJT | `POPLGS/frmLogistics8.cs:2053` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:2380` | @P_CD_COMPANY, @P_CD_MODULE, @P_CD_CLASS, @P_DOCU_YM, @P_NO | `POPLGS/frmLogistics8.cs:2396` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:2411` | @P_NO_IO, @P_CD_COMPANY, @P_CD_PLANT, @P_CD_PARTNER, @P_FG_TRANS, @P_YN_RETURN, @P_DT_IO, @P_GI_PARTNER, @P_CD_DEPT, @P_NO_EMP, @P_DC_RMK, @P_ID_INSERT, @P_CD_QTIOTP | `POPLGS/frmLogistics8.cs:2443` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics8.cs:2559` | @YN_RETURN, @NO_IO, @NO_IOLINE, @CD_COMPANY, @CD_PLANT, @CD_SL, @DT_IO, @CD_QTIOTP, @CD_ITEM, @QT_GOOD_INV, @QT_REJECT_INV, @NO_EMP, @CD_SL_REF, @YN_AM, @NO_ISURCV, @NO_ISURCVLINE, @NO_PSO_MGMT, @NO_PSOLINE_MGMT, @FLAG, @NO_GIREQ, @NO_LINE, @QT_UNIT_PO, @P_NO_POP, @P_NO_POP_LINE, @P_CD_PARTNER, @P_DC_RMK, @P_CD_PROJECT, @P_SEQ_PROJECT, @P_DC_RMK1, @P_NO_WBS, @P_NO_CBS, @P_NO_IO_MGMT, @P_NO_IOLINE_MGMT, @P_NO_MREQ, @P_NO_MREQLINE, @P_GI_PARTNER, @P_CD_ITEM_REF, @P_NO_TRACK, @P_NO_TRACKLINE, @P_CD_USERDEF1, @P_CD_USERDEF2, @P_NM_USERDEF1, @P_NM_USERDEF2, @P_DATE_USERDEF1, @P_NUM_USERDEF1, @P_DT_DELIVERY, @P_FG_TRACK, @P_CD_USERDEF3, @P_CD_USERDEF4, @P_CD_USERDEF5, @P_ID_INSERT, @P_NUM_USERDEF2, @P_TXT_USERDEF1, @P_TXT_USERDEF2 | `POPLGS/frmLogistics8.cs:2673` | 이 조사에서 본문 미확인 |

### frmLogistics9의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPLGS/frmLogistics9.cs:516` | @P_CD_COMPANY, @P_DT_FROM, @P_DT_TO, @P_CD_QTIOTP, @P_CD_PLANT, @P_CD_GRPLANT, @P_CD_SL, @P_CD_GRSL, @P_FG_LANG | `POPLGS/frmLogistics9.cs:541` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:601` | @P_CD_COMPANY, @P_NO_GIREQ, @P_FG_LANG | `POPLGS/frmLogistics9.cs:614` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:697` | @DT_FROM, @DT_TO, @CD_COMPANY, @NO_EMP, @CD_QTIOTP, @CD_PLANT, @CD_SL, @P_FG_LANG | `POPLGS/frmLogistics9.cs:720` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:784` | @P_NO_IO, @P_CD_COMPANY, @P_FG_LANG | `POPLGS/frmLogistics9.cs:803` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:1123` | @FACTORY_CODE, @OLD_OUTPUT_REQ_NO, @OLD_OUTPUT_REQ_SEQNO, @OPMAN_CODE | `POPLGS/frmLogistics9.cs:1137` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:1294` | @FACTORY_CODE, @OLD_OUTPUT_REQ_NO, @OLD_OUTPUT_REQ_SEQNO, @OPMAN_CODE | `POPLGS/frmLogistics9.cs:1308` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:1326` | @P_CD_COMPANY, @P_CD_MODULE, @P_CD_CLASS, @P_DOCU_YM, @P_NO | `POPLGS/frmLogistics9.cs:1342` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:1357` | @P_NO_IO, @P_CD_COMPANY, @P_CD_PLANT, @P_CD_PARTNER, @P_FG_TRANS, @P_YN_RETURN, @P_DT_IO, @P_GI_PARTNER, @P_CD_DEPT, @P_NO_EMP, @P_DC_RMK, @P_ID_INSERT, @P_CD_QTIOTP | `POPLGS/frmLogistics9.cs:1389` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:1479` | @YN_RETURN, @NO_IO, @NO_IOLINE, @CD_COMPANY, @CD_PLANT, @CD_SL, @DT_IO, @NO_ISURCV, @NO_ISURCVLINE, @CD_QTIOTP, @CD_PARTNER, @CD_ITEM, @QT_GOOD_INV, @QT_REJECT_INV, @CD_PJT, @NO_EMP, @CD_PLANT_RCV, @CD_SL_REF, @FG_TRANS, @YN_AM, @UM, @AM, @CD_USERDEF1 | `POPLGS/frmLogistics9.cs:1531` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:1709` | @P_CD_COMPANY, @P_CD_MODULE, @P_CD_CLASS, @P_DOCU_YM, @P_NO | `POPLGS/frmLogistics9.cs:1725` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:1740` | @P_NO_IO, @P_CD_COMPANY, @P_CD_PLANT, @P_CD_PARTNER, @P_FG_TRANS, @P_YN_RETURN, @P_DT_IO, @P_GI_PARTNER, @P_CD_DEPT, @P_NO_EMP, @P_DC_RMK, @P_ID_INSERT, @P_CD_QTIOTP | `POPLGS/frmLogistics9.cs:1772` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:1809` | @P_YN_RETURN, @P_NO_IO, @P_NO_IOLINE, @P_CD_COMPANY, @P_CD_PLANT, @P_CD_SL, @P_DT_IO, @P_CD_QTIOTP, @P_CD_PARTNER, @P_CD_ITEM, @P_QT_GOOD_INV, @P_QT_REJECT_INV, @P_AM, @P_NO_IO_MGMT, @P_NO_IOLINE_MGMT, @P_CD_PLANT_RCV, @P_CD_SL_REF, @P_NO_EMP, @P_ID_INSERT, @P_CD_PJT | `POPLGS/frmLogistics9.cs:1855` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:2007` | @FACTORY_CODE, @NO_IO | `POPLGS/frmLogistics9.cs:2017` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:2029` | @P_NO_IO, @P_CD_COMPANY, @P_ID_DELETE | `POPLGS/frmLogistics9.cs:2043` | 이 조사에서 본문 미확인 |
| `POPLGS/frmLogistics9.cs:2168` | @P_CD_COMPANY, @P_DT_START, @P_DT_END, @P_CD_PLANT, @P_처리여부, @P_NO_EMP, @P_FG_GIREQ, @P_FG_GI, @P_CD_GISL, @P_CD_GRPLANT, @P_CDGRSL, @P_SEARCH_FILTER, @P_DT_SEL, @P_TAB_INDEX, @P_CD_BGACCT, @P_SEARCH_FILTER_1, @P_SEARCH_FILTER_2, @P_CD_PARTNER, @P_GRP_MFG, @P_GI_PARTNER, @P_확정여부, @P_FG_LANG, @P_CD_ITEM, @P_CD_PJT | `POPLGS/frmLogistics9.cs:2203` | 이 조사에서 본문 미확인 |

### frmWorkcenter의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPLGS/frmWorkcenter.cs:83` | @FACTORY_CODE, @PLANT_CODE | `POPLGS/frmWorkcenter.cs:94` | 이 조사에서 본문 미확인 |

### FrmPalletBox의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPRFID/FrmPalletBox.cs:408` | @TODAY | `POPRFID/FrmPalletBox.cs:410` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmPalletBox.cs:707` | @PALLET_CODE | `POPRFID/FrmPalletBox.cs:709` | 이 조사에서 본문 미확인 |

### FrmPalletMatch의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPRFID/FrmPalletMatch.cs:162` | 호출부 참조 | `POPRFID/FrmPalletMatch.cs:164` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmPalletMatch.cs:206` | 호출부 참조 | `POPRFID/FrmPalletMatch.cs:208` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmPalletMatch.cs:250` | 호출부 참조 | `POPRFID/FrmPalletMatch.cs:251` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmPalletMatch.cs:326` | @PLANT_CODE, @PALLET_STATE, @PALLET_TYPE, @RFID_TAG_CODE | `POPRFID/FrmPalletMatch.cs:334` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmPalletMatch.cs:401` | @RFID_TAG_CODE | `POPRFID/FrmPalletMatch.cs:404` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmPalletMatch.cs:461` | @RFID_TAG_CODE | `POPRFID/FrmPalletMatch.cs:464` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmPalletMatch.cs:486` | @RFID_TAG_ID | `POPRFID/FrmPalletMatch.cs:491` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmPalletMatch.cs:663` | @PALLET_CODE | `POPRFID/FrmPalletMatch.cs:668` | 이 조사에서 본문 미확인 |

### FrmPhoto의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPRFID/FrmPhoto.cs:162` | @IO_NO | `POPRFID/FrmPhoto.cs:164` | 이 조사에서 본문 미확인 |

### FrmRfidNoScan의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPRFID/FrmRfidNoScan.cs:249` | @RFID_TAG_ID | `POPRFID/FrmRfidNoScan.cs:254` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmRfidNoScan.cs:287` | @RFID_TAG_ID | `POPRFID/FrmRfidNoScan.cs:289` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmRfidNoScan.cs:333` | @RFID_TAG_ID | `POPRFID/FrmRfidNoScan.cs:335` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmRfidNoScan.cs:383` | @PRODPLAN_SEQ | `POPRFID/FrmRfidNoScan.cs:385` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmRfidNoScan.cs:431` | @RFID_TAG_ID | `POPRFID/FrmRfidNoScan.cs:433` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmRfidNoScan.cs:508` | @TODAY | `POPRFID/FrmRfidNoScan.cs:510` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmRfidNoScan.cs:536` | @RFID_TAG_ID | `POPRFID/FrmRfidNoScan.cs:538` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmRfidNoScan.cs:567` | @RFID_TAG_ID | `POPRFID/FrmRfidNoScan.cs:569` | 이 조사에서 본문 미확인 |

### FrmTagInOutList의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPRFID/FrmTagInOutList.cs:135` | 호출부 참조 | `POPRFID/FrmTagInOutList.cs:137` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmTagInOutList.cs:207` | @SDATE, @EDATE, @PLANT_CODE | `POPRFID/FrmTagInOutList.cs:214` | 이 조사에서 본문 미확인 |

### FrmTagInOutReg의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPRFID/FrmTagInOutReg.cs:90` | PALLET_CODE | `POPRFID/FrmTagInOutReg.cs:93` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmTagInOutReg.cs:127` | @BOX_NO | `POPRFID/FrmTagInOutReg.cs:129` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmTagInOutReg.cs:368` | @TODAY | `POPRFID/FrmTagInOutReg.cs:370` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmTagInOutReg.cs:414` | @PALLET_CODE | `POPRFID/FrmTagInOutReg.cs:416` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmTagInOutReg.cs:451` | PALLET_CODE | `POPRFID/FrmTagInOutReg.cs:454` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmTagInOutReg.cs:488` | @BOX_NO | `POPRFID/FrmTagInOutReg.cs:490` | 이 조사에서 본문 미확인 |

### FrmTagReg의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPRFID/FrmTagReg.cs:86` | 호출부 참조 | `POPRFID/FrmTagReg.cs:88` | 이 조사에서 본문 미확인 |
| `POPRFID/FrmTagReg.cs:314` | @SDATE, @EDATE, @PLANT_CODE | `POPRFID/FrmTagReg.cs:321` | 이 조사에서 본문 미확인 |

### frmExpendables의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPMANAGEMENT/frmExpendables.cs:287` | @DIVISION | `POPMANAGEMENT/frmExpendables.cs:290` | 이 조사에서 본문 미확인 |
| `POPMANAGEMENT/frmExpendables.cs:332` | @DIVISION | `POPMANAGEMENT/frmExpendables.cs:335` | 이 조사에서 본문 미확인 |
| `POPMANAGEMENT/frmExpendables.cs:377` | @DIVISION, @ITEM_KIND1 | `POPMANAGEMENT/frmExpendables.cs:381` | 이 조사에서 본문 미확인 |
| `POPMANAGEMENT/frmExpendables.cs:424` | @FACTORY_CODE, @PLANT_CODE, @MATERIAL_FLAG, @ITEM_KIND1, @ITEM_KIND2, @WAREHOUSE_CODE, @SYSTEM_LOT_NO, @MATERIAL_CODE, @LOCATION_CODE | `POPMANAGEMENT/frmExpendables.cs:451` | 이 조사에서 본문 미확인 |
| `POPMANAGEMENT/frmExpendables.cs:479` | @DIVISION, @FACTORY_CODE, @PLANT_CODE, @WORKCENTER_CODE, @VIEW_SEQ, @SYS_LOT_NO, @REQ_DATE | `POPMANAGEMENT/frmExpendables.cs:502` | 이 조사에서 본문 미확인 |
| `POPMANAGEMENT/frmExpendables.cs:530` | @DIVISION, @FACTORY_CODE, @PLANT_CODE, @WORKCENTER_CODE, @VIEW_SEQ, @SYS_LOT_NO, @REQ_DATE | `POPMANAGEMENT/frmExpendables.cs:553` | 이 조사에서 본문 미확인 |
| `POPMANAGEMENT/frmExpendables.cs:628` | @FACTORY_CODE, @PLANT_CODE, @MATERIAL_FLAG, @ITEM_KIND1, @ITEM_KIND2, @WAREHOUSE_CODE, @SYSTEM_LOT_NO, @MATERIAL_CODE, @LOCATION_CODE | `POPMANAGEMENT/frmExpendables.cs:643` | 이 조사에서 본문 미확인 |
| `POPMANAGEMENT/frmExpendables.cs:913` | @FACTORY_CODE, @PLANT_CODE, @MATERIAL_FLAG, @ITEM_KIND1, @ITEM_KIND2, @WAREHOUSE_CODE, @SYSTEM_LOT_NO, @MATERIAL_CODE, @LOCATION_CODE | `POPMANAGEMENT/frmExpendables.cs:928` | 이 조사에서 본문 미확인 |
| `POPMANAGEMENT/frmExpendables.cs:1392` | @DIVISION, @FACTORY_CODE, @PLANT_CODE, @WORKCENTER_CODE, @SYS_LOT_NO, @VIEW_SEQ, @REQ_DATE | `POPMANAGEMENT/frmExpendables.cs:1405` | 이 조사에서 본문 미확인 |

### frmProduction의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPMANAGEMENT/frmProduction.cs:152` | @PRODPLAN_DATE, @PRODPLAN_SEQ | `POPMANAGEMENT/frmProduction.cs:163` | 이 조사에서 본문 미확인 |

### frmRepair의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPMANAGEMENT/frmRepair.cs:206` | @DIVISION, @PLANT_CODE, @EQUIP_SYS_CD, @SDATE, @EDATE, @CLEAR | `POPMANAGEMENT/frmRepair.cs:217` | 이 조사에서 본문 미확인 |

### frmMaterialOption의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPPRINT/frmMaterialOption.cs:159` | @division, @factory_code, @plant_code | `POPPRINT/frmMaterialOption.cs:173` | 이 조사에서 본문 미확인 |

### frmOpmanBarCode의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPPRINT/frmOpmanBarCode.cs:95` | @DIVISION, @PLANT_CODE, @Department_Code | `POPPRINT/frmOpmanBarCode.cs:101` | 이 조사에서 본문 미확인 |
| `POPPRINT/frmOpmanBarCode.cs:154` | @DIVISION, @PLANT_CODE, @Department_Code | `POPPRINT/frmOpmanBarCode.cs:160` | 이 조사에서 본문 미확인 |

### frmWorkPrint의 명시적 SP 호출

| 호출 위치 | 호출부 인수 단서 | 결과 소비 지점 | 저장소 정의·기록된 변경 대상 |
|---|---|---|
| `POPPRINT/frmWorkPrint.cs:278` | @division, @factory_code, @plant_code | `POPPRINT/frmWorkPrint.cs:292` | 이 조사에서 본문 미확인 |
| `POPPRINT/frmWorkPrint.cs:352` | @DIVISION, @FACTORY_CODE, @PLANT_CODE | `POPPRINT/frmWorkPrint.cs:357` | 이 조사에서 본문 미확인 |
| `POPPRINT/frmWorkPrint.cs:398` | @FACTORY_CODE, @PLANT_CODE, @S_DATE, @E_DATE, @COMPLETE, @PRINT_STATE, @WORKCENTER_CODE, @MATERIAL_CODE, @FG_USE, @CD_SL, @OPMAN, @DRAW_ONLY | `POPPRINT/frmWorkPrint.cs:433` | `SQL/FIX_SP_POP_ORDER_01_LIST_20261002.sql:9` · `SQL/FIX_SP_POP_ORDER_01_LIST_20261124.sql:28` · `SQL/ROLLBACK_SP_POP_ORDER_01_LIST_20261002.sql:4` · `SQL/ROLLBACK_SP_POP_ORDER_01_LIST_20261124.sql:5` / 복수 스크립트, 설치본 미확정 |
| `POPPRINT/frmWorkPrint.cs:942` | @division, @factory_code, @plant_code, @workcenter_code, @order_no, @order_histno, @order_seqno, @prodplan_date, @prodplan_seq, @prodplan_dateseq, @order_noseqno | `POPPRINT/frmWorkPrint.cs:1000` | 이 조사에서 본문 미확인 |
| `POPPRINT/frmWorkPrint.cs:1105` | @FACTORY_CODE, @ORDER_NO, @ORDER_HISTNO, @ORDER_SEQNO, @OPMAN_CODE | `POPPRINT/frmWorkPrint.cs:1121` | `SQL/FIX_SP_POP_PRINT_CNT_IUD_20260930.sql:34` · `SQL/ROLLBACK_SP_POP_PRINT_CNT_IUD_20260930.sql:6` / 복수 스크립트, 설치본 미확정 |
| `POPPRINT/frmWorkPrint.cs:1339` | @division, @factory_code, @plant_code, @order_no, @order_seqno, @prodplan_dateseq | `POPPRINT/frmWorkPrint.cs:1372` | `SQL/FIX_SP_POP_COM_REPORT_03_LIST_20261007.sql:1` · `SQL/ROLLBACK_SP_POP_COM_REPORT_03_LIST_20261007.sql:1` / 복수 스크립트, 설치본 미확정 |
| `POPPRINT/frmWorkPrint.cs:1634` | @FACTORY_CODE, @ORDER_NO, @ORDER_HISTNO, @ORDER_SEQNO, @OPMAN_CODE | `POPPRINT/frmWorkPrint.cs:1652` | `SQL/FIX_SP_POP_PRINT_CNT_IUD_20260930.sql:34` · `SQL/ROLLBACK_SP_POP_PRINT_CNT_IUD_20260930.sql:6` / 복수 스크립트, 설치본 미확정 |
| `POPPRINT/frmWorkPrint.cs:1905` | @division, @factory_code, @plant_code, @order_no, @order_seqno, @prodplan_dateseq | `POPPRINT/frmWorkPrint.cs:1938` | `SQL/FIX_SP_POP_COM_REPORT_03_LIST_20261007.sql:1` · `SQL/ROLLBACK_SP_POP_COM_REPORT_03_LIST_20261007.sql:1` / 복수 스크립트, 설치본 미확정 |
| `POPPRINT/frmWorkPrint.cs:2218` | @FACTORY_CODE, @ORDER_NO, @ORDER_HISTNO, @ORDER_SEQNO, @OPMAN_CODE | `POPPRINT/frmWorkPrint.cs:2236` | `SQL/FIX_SP_POP_PRINT_CNT_IUD_20260930.sql:34` · `SQL/ROLLBACK_SP_POP_PRINT_CNT_IUD_20260930.sql:6` / 복수 스크립트, 설치본 미확정 |
| `POPPRINT/frmWorkPrint.cs:2446` | @division, @factory_code, @plant_code, @order_no, @order_seqno, @prodplan_dateseq | `POPPRINT/frmWorkPrint.cs:2479` | `SQL/FIX_SP_POP_COM_REPORT_03_LIST_20261007.sql:1` · `SQL/ROLLBACK_SP_POP_COM_REPORT_03_LIST_20261007.sql:1` / 복수 스크립트, 설치본 미확정 |
| `POPPRINT/frmWorkPrint.cs:2770` | @FACTORY_CODE, @ORDER_NO, @ORDER_HISTNO, @ORDER_SEQNO, @OPMAN_CODE | `POPPRINT/frmWorkPrint.cs:2788` | `SQL/FIX_SP_POP_PRINT_CNT_IUD_20260930.sql:34` · `SQL/ROLLBACK_SP_POP_PRINT_CNT_IUD_20260930.sql:6` / 복수 스크립트, 설치본 미확정 |
| `POPPRINT/frmWorkPrint.cs:3040` | @division, @factory_code, @plant_code, @order_no, @order_seqno, @prodplan_dateseq | `POPPRINT/frmWorkPrint.cs:3073` | `SQL/FIX_SP_POP_COM_REPORT_03_LIST_20261007.sql:1` · `SQL/ROLLBACK_SP_POP_COM_REPORT_03_LIST_20261007.sql:1` / 복수 스크립트, 설치본 미확정 |
| `POPPRINT/frmWorkPrint.cs:3367` | @FACTORY_CODE, @ORDER_NO, @ORDER_HISTNO, @ORDER_SEQNO, @OPMAN_CODE | `POPPRINT/frmWorkPrint.cs:3385` | `SQL/FIX_SP_POP_PRINT_CNT_IUD_20260930.sql:34` · `SQL/ROLLBACK_SP_POP_PRINT_CNT_IUD_20260930.sql:6` / 복수 스크립트, 설치본 미확정 |

## 남은 인수 질문

1. 사업장별 발주입고 일괄과 ESCO 후처리에 사용하는 기존 SP 버전, 실행 계정/권한, 재실행 판단에 사용하는 전표키와 실패 결과셋을 담은 비운영 계약 자료가 있는가?
2. 과거 공장이송출고 및 출하의 숨김 완료·완료삭제를 현재 여는 다른 메뉴가 있는가? 있다면 작업장과 진입 순서는 무엇인가?
3. 사원번호 출력의 추가 인증, 작업지시서 출력횟수·삭제가 확정되는 시점 및 RFID 사진 확정/매칭 해제의 허용 역할은 무엇인가?

폼 수는 Designer와 구현 파일의 짝을 기준으로 검산했다. 명시적 SP 호출 위치 158개를 위 표에 기록했다. C#에서 직접 만든 질의·갱신, 트리거·함수 등 서버 내부 효과는 이 수에 포함하지 않는다. 원문 없는 경로의 Spring 구현이나 운영 배포는 수행하지 않았다.

[[29-운영-POP-기능명세]] · [[30-Spring-API-명세]]

## 2026-11-26 통합 검증

관리 메뉴의 원본 소모품 타일은 ‘소모품 요청’이며 이미지·라벨·배경 모두 같은 frmExpendables를 연다. 전환 화면도 같은 타일에서 소모품 목록, 신청재고, 최근 1개월 신청내역 탭으로 이동한다. 반납은 신청재고의 행에서 처리한다. 원본 근거는 MainMenu/frmMenu.Designer.cs 1223–1246행, frmMenu.cs 446–452·820–824행이다.

출하의 종이 발행은 인증된 세션에 적용된 Printer2를 쓴다. 확정된 전표의 수동 미리보기 닫기, PDF 저장, 실제 제출을 분리했다. 저장 이후의 자동 출력 실패는 이미 확정한 출하를 되돌리지 않는다. 합성 Spring·Chrome에서 종이/이메일 발송 구분, 미리보기 취소, 장치 미설정, 수동 제출 응답 유실 후 재시도, 동일·상이 본문 동시 요청과 출하 취소를 검증했다. 실장치 출력과 운영 기록 대사는 남았다. 상세 호출 계약은 전환 레포 docs/shipping-statement-print.md에 있다.

## 사원번호 출력과 추가 인증

인쇄 두 번째 타일의 사원번호 출력은 폼 진입 때마다 사용제한 대화상자를 연다. 원본 MainMenu/frmMenu.cs 891–906, POPSYS/frmPassWord.cs 77–114, 190–230에 근거한다. 비밀번호 불일치 시 입력을 지우고 다시 입력한다. 단말 역할이나 로그인 암호로 추가 인증을 자동 통과시키지 않는다.

최초 화면에는 사업장 목록만 있다. 사업장을 선택하면 사원과 부서 목록을 조회하고, 부서를 바꾸면 선택을 다시 조회한다. 행을 누르면 개별 선택, 선택 헤더는 전체 토글이다. 선택 없이 두 출력 버튼을 누르면 원본 안내를 표시한다. 원본 POPPRINT/frmOpmanBarCode.cs 35–115, 126–169, 173–207, 211–287, 300–334.

Spring은 선택 행에 맞춰 원본 Designer 기준 A4 페이지를 생성한다. 원본 REPORT.dll의 출력물은 독립 대조에만 사용한다. 같은 사원의 Code128 두 장이 한 행에 배치되고 QR은 다른 사원을 가로 두 열로 채운다. 보고서의 Printer1은 인증 단말에 적용된 작업지시서 프린터 설정에 대응한다. 미리보기와 명시적 Quick Print 접수를 구분하며 닫을 때 선택은 유지한다. 합성 접수는 실물 출력 완료를 뜻하지 않는다.

원본 Preview 창에서는 Print...와 Quick Print가 별도이며 Save, Page Setup, 내보내기, 메일 명령도 존재한다. 웹에서 확인한 동선은 실제 합성 제출, 확대/축소, 페이지 이동, 닫기이다. 원본 PRNX의 메모리 저장·재열기는 확인했다. 일반 인쇄 대화상자·저장 위치·페이지 변경·메일 연결 및 미연결 명령 표시 방식은 현장 결정 대기다. 스풀러와 운영 DB를 호출하지 않는다.

### 2026-11-26 폼 화면 증빙

[원본·웹 좌우 대조와 실측 좌표](</E:/ajk/devgit/shinjin/.team/screen-review/web-parity/RFID-관리-화면대조.md>)를 참조한다. 원본 관리 3폼과 RFID 9폼, 최종조회 2행 같은 상태를 비교했다.

출고처 필드를 누르면 원본과 같이 작업지시번호를 스캔한다. 별도 데이터셋 `src/api/src/main/resources/demo/rfid-forms.json`의 DEMO-A/DEMO-W01, 파렛트 26000001·26000002, 출고처 스캔 20261125201로 검증했다. 원본 `SP_POP_RFID_PALLETBOX_01_CUSTOMER(@PRODPLAN_SEQ)`에 전달하는 스캔 문자열을 데모에서 매핑한다. 카메라 모드에서는 같은 ZXing 계열 디코더를 브라우저에서 동적으로 읽어 원본처럼 단말 내에서 해독한다. Spring으로 사진이 전송되는 시점은 촬영본 확정 후 적재 저장이다. 포장/입출고 번호는 발행일 기준 각각 yyyyMMdd0001부터 할당하고 동일 requestId를 재전송하면 재발번하지 않는다. 실장비의 카메라 목록 순서와 USB 스캐너의 키 종결자는 현장 인수 대상이다.

2026-11-26 15179 공개판. 원본 frmMenu.Designer.cs 1413의 타일명은 사원번호 인쇄, frmMenu.cs 906의 자식 제목은 사원번호 출력이다. 정상 로그인 뒤 추가 암호를 확인하고 사업장·부서·사원을 선택해 QR/Code128 미리보기를 열었다. 작업지시서는 작업반 전체 → 조회 → 행 선택 → 출력 양식 → 실제 PDF 응답까지 양쪽 화면 크기에서 검증했다. 1024×768·1584×1024의 실제 캡처는 원본 분석 저장소 .team/menu-screen/15179-current 아래에 있다. 물리·합성 제출은 꺼진 공개 설정이며, 사원 추가암호는 로그인용 0000을 거절한다.
 
### 작업지시서와 사원번호 조회 화면의 표시·터치

기존 POP의 인쇄 메뉴에서 작업지시서는 `frmWorkPrint`, 사원번호 인쇄는 비밀번호 확인 뒤 `frmOpmanBarCode`를 연다. 재고 라벨 패널은 Designer에서 숨김이다. 인쇄 메뉴에는 위 두 활성 화면만 제공한다. 테스트 자료는 Spring 프로파일에서만 공급한다.

원본 1280×800 인쇄 조회의 MDI 영역은 (3,88), 1274×639이다. 날짜 필드는 175×50, 조회·출력은 110×140, 거래처 열은 230, 주문 데이터 행은 100이다. 원본은 고정된 계정구분 필드와 오른쪽에 붙은 조회 버튼이 75px 겹친다. 사원번호 화면의 QR·바코드 버튼은 1024에서 오른쪽 경계 밖이다. 사용자 결정에 따라 웹 조회 폼은 사용 가능한 MDI 공간을 채우고, 좁은 폭에서는 검색 조건을 여러 줄로 배치한다. 고정 비율로 화면 전체를 축소하지 않는다. 조회, 선택, 출력 순서와 필터 의미, 보고서 A4 및 라벨 용지는 원본을 따른다.

| 화면 | 실메뉴에서 확인한 동작 | 확인 크기 |
|---|---|---|
| 작업지시서 | 재질/계정 설정과 취소, 12행→결과 없음→12행, 체크와 양식 선택, PDF 열기 후 별도 탭에서 진짜 PDF 수신 | 1024×768, 1280×800, 1366×768, 1920×1080 |
| 사원번호 인쇄 | 비밀번호, 사업장 선택, 체크, QR·바코드 동적 보고서 열기/닫기 | 같은 네 크기 |
| 원본 비교 | 1600×1024 기준과 1024/1280/1366에서 원본 폼, WinForms MDI 위치·컨트롤 바운드·글꼴 크기 수집 | 원본 DB 이벤트와 실물 프린터 제외 |

사원 미리보기에는 원본 툴바의 메뉴·아이콘을 보존한다. 문서 열기/저장·Print...·장치 설정·외부 내보내기/메일은 웹에서 연결 대기이며, 연결된 명령은 문서 확대/축소·쪽 이동·닫기·창 확대이다. Quick Print는 합성 제출을 명시한 독립 검증에서만 사용할 수 있다. 기본 미리보기는 물리 장치나 합성 인쇄 원장에 제출하지 않는다.

## 11월 26일 RFID 숫자 입력 및 조건별 인쇄 검수

공개 POP A에서 팔레트 매칭 시 숫자 키보드의 8자리 제한, 한 자리/전체 삭제, 취소와 부모 복귀를 검증했다. 사진과 전송 결과는 가상 카메라가 연결된 격리 합성 데이터 기준이다. 작업지시서 네 양식은 7·8행 및 혼합 그룹 등 12가지 입력, 총 18쪽의 쪽 나뉨·지시번호·바코드를 원본과 비교했다. [RFID 검수](file:///E:/ajk/devgit/shinjin/.rework-visual-qa/rfid-wait-followup/handoff.md) · [PDF 비교](file:///E:/ajk/devgit/shinjin/.rework-visual-qa/conditional-reports/page-check.log).

### 재고이동 위치 재스캔

물류 → 재고이동 → 입고 창고 → 행 추가의 재고 선택창에서 미등록 위치를 스캔해 안내를 닫으면 위치 입력란으로 포커스가 돌아간다. 1280×800, 1366×768, 1024×768에서 재터치 없이 다음 위치를 스캔했다. 격리 장부에서 저장 취소 시 전후 상태 일치, 승인 시 이동 1건 및 잔량 −1/+1, 다시 열어 수량·위치 일치를 확인했다. [위치 포커스와 저장 검수](file:///E:/ajk/devgit/shinjin/.rework-visual-qa/logistics-stock-parent/handoff.md)

### 공장이송출고 수동 미리보기 합계 위치

원본 rptOutputList에서 마지막 쪽에 예약하는 합계 표 높이 30.20835를 적용했다. 한 줄 품목 24행은 합계가 같은 쪽에, 25행은 합계가 다음 쪽에 표시된다. 원본 PDF 15개 전표의 23쪽과 쪽별 행·합계 유무를 대조했다. 출하 거래명세서도 문서별 분할은 확인했으나 원본의 공급자·공급받는자 보관용 두 부, 등록번호·공급가·세액 필드는 추가 이관 대상이다. [출고목록·출하 보고서 비교](file:///E:/ajk/devgit/shinjin/.rework-output-list-compare/handoff.md)

#### 출하 거래명세서의 두 보관용

별도 합성 데이터셋 `shipping-statement-example.json`을 지정하면 출하 완료 조회에서 선택한 각 문서에 공급받는자 보관용과 인수증이 나온다. 거래처 원본 두 행, 전표 일련번호, 발주량·출하량·단가·공급가액·세액을 필드 그대로 바인딩한다. 세액과 공급가액은 제공된 값이다. 15행마다 두 부에 각각 페이지 소계를 쓰고 문서 총계를 반복한다. 17행·2문서 3쪽을 원본 PDF와 비교해 양쪽 상세행·필드·합계를 확인했다. 지정된 자료가 불완전한 전표는 PDF 422이며 상태와 출력 이력은 유지한다. 인영, 실물 여백, 긴 문구의 줄바꿈과 운영 SP 내부 산식은 별도 검수 대상이다. [원본 양식과 PDF 대조](file:///E:/ajk/devgit/shinjin/.rework-shipping-statement-increment/handoff.md)
