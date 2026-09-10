
화면 1. WPR559 – 생산실적등록                                                                                                                                         
  ---
  WebContent/app/store/PR/WPR550/WPR559_ST.js

  작업: 스토어 필드 및 콤보 데이터 추가

  ┌──────────────────────────┬──────────────────────────────────────────────────────────────────────────────┐
  │           항목           │                                     내용                                     │
  ├──────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ gridStore_01 fields 추가 │ { name: 'ITEM_KIND2', type: 'string' } — 행 색상 CSS 처리용 히든 컬럼 데이터 │
  ├──────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ gridStore_01 fields 추가 │ { name: 'SHIPPING_QTY', type: 'float' } — 출하량 컬럼 데이터                 │
  ├──────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ cboStore_itemKind2 추가  │ 도면가공 구분 로컬 콤보 스토어 (전체='', 도면가공='1', 도면가공 제외='0')    │
  └──────────────────────────┴──────────────────────────────────────────────────────────────────────────────┘

  ---
  WebContent/app/view/PR/WPR550/WPR559_VW.js

  작업: 조회조건 콤보 추가 / 그리드 컬럼 추가 / 행 색상 로직 추가

  ① 조회조건 콤보 추가
  - 수주종결 콤보 우측에 cbo_itemKind2 콤보박스 추가
  - 바인딩: cboStore_itemKind2 로컬 스토어 (전체/도면가공/도면가공 제외)

  ② grid_01 컬럼 추가
  - SHIPPING_QTY numbercolumn — 공정진척현황 그룹 내 '출하' 컬럼
  - ITEM_KIND2 gridcolumn — hidden: true (CSS 처리용, 화면 미표시)

  ③ viewConfig.getRowClass 추가
  getRowClass: function (record) {
    var packQty   = parseFloat(record.get('PROD_QTY_WORK_005')) || 0;
    var orderQty  = parseFloat(record.get('ORDER_UNIT_QTY'))    || 0;
    var itemKind2 = record.get('ITEM_KIND2');

    if (packQty > orderQty)   return 'row-over-packed';   // 연분홍 (최우선)
    if (itemKind2 === 'A70')  return 'row-drawing-work';  // 연노랑
    return '';
  }
  - 포장수량 > 수주수량이면 연분홍 우선 적용, 도면가공이면 연노랑

  ---
  WebContent/app/controller/PR/WPR550/WPR559_CT.js

  작업: CSS 주입 / 조회 파라미터 추가

  ① init 함수에 CSS 동적 주입
  Ext.util.CSS.createStyleSheet(
    '.x-grid-row.row-drawing-work .x-grid-cell { background-color: #FFFACD !important; }' +
    '.x-grid-row.row-drawing-work:hover .x-grid-cell { background-color: #FFF5A0 !important; }' +
    '.x-grid-row.row-over-packed .x-grid-cell { background-color: #FFD1DC !important; }' +
    '.x-grid-row.row-over-packed:hover .x-grid-cell { background-color: #FFB3C6 !important; }',
    'WPR559_drawing_row_style'
  );
  - ExtJS 내부 스타일 특이도(specificity) 문제로 외부 CSS 적용 불가 → createStyleSheet + !important 로 해결

  ② onView_grid01 함수에 파라미터 추가
  itemKind2Flag = me.getView().down('#cbo_itemKind2').getValue()
  // store.load params 에 추가:
  ITEM_KIND2_FLAG: itemKind2Flag,

  ---
  src/com/PR/WPR550/jvWPR559_01_LIST.java

  작업: 파라미터 파싱 및 SP 호출 인자 추가

  String ITEM_KIND2_FLAG = "";
  if (request.getParameter("ITEM_KIND2_FLAG") != null) {
      ITEM_KIND2_FLAG = request.getParameter("ITEM_KIND2_FLAG").trim().replace("'", "''");
  }

  String sql = "EXEC SP_WPR559_01_LIST ... ,'" + ITEM_KIND2_FLAG + "'";

  ---
  SP_WPR559_01_LIST (DB Stored Procedure)

  작업: 파라미터 추가 / SELECT 컬럼 추가 / WHERE 조건 추가 / TSA403 LEFT JOIN 추가

  ① 파라미터 선언
  @ITEM_KIND2_FLAG VARCHAR(1) = ''

  ② SELECT에 컬럼 추가
  ISNULL(MAT.ITEM_KIND2, '') AS ITEM_KIND2,
  ISNULL(SHIP_DATA.SHIPPING_QTY, 0) AS SHIPPING_QTY

  ③ WHERE 조건 추가
  AND (
      @ITEM_KIND2_FLAG = ''
      OR (@ITEM_KIND2_FLAG = '1' AND ISNULL(MAT.ITEM_KIND2,'') = 'A70')
      OR (@ITEM_KIND2_FLAG = '0' AND ISNULL(MAT.ITEM_KIND2,'') <> 'A70')
  )

  ④ TSA403 LEFT JOIN 추가 (출하량 집계)
  LEFT JOIN (
      SELECT FACTORY_CODE, ORDER_NO, ORDER_HISTNO, ORDER_SEQNO,
             SUM(ISNULL(SHIPPING_QTY, 0)) AS SHIPPING_QTY
      FROM TSA403 WITH (NOLOCK)
      GROUP BY FACTORY_CODE, ORDER_NO, ORDER_HISTNO, ORDER_SEQNO
  ) SHIP_DATA
  ON ORDER_DETAIL.FACTORY_CODE = SHIP_DATA.FACTORY_CODE
  AND ORDER_DETAIL.ORDER_NO     = SHIP_DATA.ORDER_NO
  AND ORDER_DETAIL.ORDER_HISTNO = SHIP_DATA.ORDER_HISTNO
  AND ORDER_DETAIL.ORDER_SEQNO  = SHIP_DATA.ORDER_SEQNO
  - TSA406(데이터 없음) → TSA308(데이터 없음) → TSA403(데이터 확인) 순서로 테이블 조사 후 최종 결정
  - 기존 OUTER APPLY 방식에서 LEFT JOIN 방식으로 변경 (사용자 요청)

  ---
  ---
  화면 2. WMA624 – 재고조정 엑셀 업로드

  ---
  src/com/MA/WMA620/jvWMA624_02_EXCEL_UPLOAD.java

  작업: 엑셀 파싱 시 DB 일괄 조회로 품목 정보 채움 (기존: 엑셀 값 그대로 사용)

  ① bulkFetchMaterialByPartNo 메서드 신규 추가
  private Map<String, String[]> bulkFetchMaterialByPartNo(
          Connection conn, String factoryCode, Set<String> partNoSet) {
      // TCO403 WHERE PART_NO IN (?, ?, ...) 일괄 조회
      // 반환: { PART_NO → [MATERIAL_CODE, MATERIAL_NAME, MATERIAL_SPEC, MATERIAL_FLAG] }
  }

  ② Pass 1 (고유값 수집) 확장
  - 기존: 창고명만 수집 → 추가: PART_NO도 함께 수집
  String partNo = cellValue(row, COL_PART_NO, fmt);
  if (!partNo.isEmpty()) partNoSet.add(partNo);

  ③ Pass 2 (JSON 빌드) 수정
  - 기존: 엑셀 col 2(품목코드), col 3(규격) 값을 그대로 사용
  - 변경: materialMap.getOrDefault(partNo, ...) 로 DB 조회값 사용
  String[] mInfo = materialMap.getOrDefault(partNo, new String[]{"", "", "", ""});
  item.put("MATERIAL_CODE", mInfo[0]);  // DB 조회값 (TCO403)
  item.put("MATERIAL_NAME", mInfo[1]);  // DB 조회값
  item.put("MATERIAL_SPEC", mInfo[2]);  // DB 조회값
  item.put("MATERIAL_FLAG", mInfo[3]);  // DB 조회값
  - LOT_NO(col 6), TARGET_QTY(col 7)는 엑셀 값 그대로 유지 (다운로드 시 이미 DB 값으로 채워진 값)

  ---
  src/com/MA/WMA620/jvWMA624_03_BATCH_FETCH.java ← 신규 생성

  작업: 붙여넣기 N건 배치 처리용 엔드포인트

  - URL: /com/MA/WMA620/jvWMA624_03_BATCH_FETCH
  - 파라미터: PART_NOS(쉼표 구분), FACTORY_CODE, PLANT_CODE, WAREHOUSE_CODE, TYPE_FLAG, ZERO_FLAG

  처리 흐름:
  Step 1: TCO403 WHERE PART_NO IN (?,?,?) → 품목 정보 일괄 조회 (PreparedStatement)
  Step 2: 찾은 MATERIAL_CODE별로 SP_WEB_STORE_FUNCTION_GET_LOT_LIST 순차 호출
          (동일 DB 커넥션, HTTP 왕복 없음)

  응답 구조:
  {
    "success": "true",
    "data": {
      "materials": { "PART_NO_A": { "MATERIAL_CODE": "...", "MATERIAL_NAME": "...", ... } },
      "lots":      { "MAT_CODE_X": [ { "LOT_NO": "...", "STOCK_QTY": "...", ... } ] }
    }
  }

  ---
  WebContent/app/controller/MA/WMA600/WMA624_CT.js

  작업: 붙여넣기 처리를 개별 병렬 → 1회 배치 요청으로 변경

  ① onPastePartNos 수정
  // 변경 전
  me.onProcessPasteParallel(items);
  // 변경 후
  me.onProcessPasteBatch(items);

  ② onProcessPasteBatch 신규 추가
  - PART_NO 배열을 쉼표로 조인 → jvWMA624_03_BATCH_FETCH 1회 Ajax 호출
  - 응답의 materialsMap, lotsMap을 순회하여 각 레코드에 세팅
  - _materialCache에도 결과 저장 → 이후 단건 엔터 조회 시 캐시 히트
  - LOT 0건: SYSTEM_LOT_NO = '', LOT 1건: 자동 세팅, LOT 다건: 팝업 순차 처리(lotQueue)

  ③ onProcessPasteParallel 유지 — 폴백용으로 삭제하지 않고 코멘트만 변경

  ---
  성능 개선 요약

  ┌───────────────────────┬──────────────────────────┬──────────────────────────────┐
  │         구분          │         변경 전          │           변경 후            │
  ├───────────────────────┼──────────────────────────┼──────────────────────────────┤
  │ 붙여넣기 N건          │ HTTP 2N회 (품목N + LOTN) │ HTTP 1회                     │
  ├───────────────────────┼──────────────────────────┼──────────────────────────────┤
  │ 엑셀 업로드 품목 조회 │ 엑셀 값 그대로           │ TCO403 IN쿼리 1회 배치       │
  ├───────────────────────┼──────────────────────────┼──────────────────────────────┤
  │ 붙여넣기 LOT 조회     │ N개 개별 Ajax            │ 서버 내부 순차 (동일 커넥션) │
  └───────────────────────┴──────────────────────────┴──────────────────────────────┘