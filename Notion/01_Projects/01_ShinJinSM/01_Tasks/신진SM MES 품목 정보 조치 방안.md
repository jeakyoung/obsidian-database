
 -- ============================================================                                                                                                  
  -- SP_WMA624_01_LIST 수정 이력                                                          
  -- 수정일: 2026-09-04                                                                                                                                            
  -- 수정사유: TCO403.PLANT_CODE와 TMA922.PLANT_CODE 불일치로                                                                                                      
  --           인해 품목이 조회되지 않는 문제 해결                                                                                                                 
  --           (동일 품목이 다른 사업장 창고에 재고가 있을 경우                                                                                                    
  --            조회가 안 되던 구조적 문제)
  -- 수정내용:
  --   1. WHERE절 A.PLANT_CODE = @PLANT_CODE 제거
  --      → TCO403는 품목정보 조회 용도로만 사용,
  --        사업장 필터는 TMA922 서브쿼리에서 처리
  --   2. WHERE절 A.PLANT_CODE = B.PLANT_CODE 제거
  --      → TCO403 등록 사업장과 TMA922 재고 사업장이
  --        다르더라도 조회 가능하도록 변경
  --   3. SELECT A.PLANT_CODE → B.PLANT_CODE 변경
  --      → 실제 재고 사업장(TMA922 기준) 표시
  --   4. TCO101 JOIN 조건 A.PLANT_CODE → @PLANT_CODE 변경
  --      → 조회 사업장명 정상 표시
  -- ============================================================


  -- ============================================================
  -- [롤백용] 원본 SP
  -- ============================================================
  /*
  ALTER PROC [dbo].[SP_WMA624_01_LIST]
  (
      @FACTORY_CODE        VARCHAR(6),
      @DATE                VARCHAR(8),
      @SEARCH_NAME         VARCHAR(100),
      @WAREHOUSE_CODE      VARCHAR(100),
      @OPMAN_CODE          VARCHAR(10) = '0000',
      @PLANT_CODE          VARCHAR(20) = '001',
      @MATERIAL_QUALITY    VARCHAR(20) = ''
  )
  AS
  BEGIN

      SELECT
            A.MATERIAL_CODE                    AS MATERIAL_CODE
          , A.MATERIAL_NAME                    AS MATERIAL_NAME
          , A.PART_NO                          AS PART_NO
          , A.MATERIAL_SPEC                    AS MATERIAL_SPEC
          , A.PLANT_CODE                       AS PLANT_CODE
          , D.CODE_NAME_FULL                   AS PLANT_NAME
          , B.WAREHOUSE_CODE                   AS WAREHOUSE_CODE
          , C.ETC                              AS WAREHOUSE_CODE_ETC
          , C.WAREHOUSE_NAME                   AS WAREHOUSE_NAME
          , A.UNIT                             AS MATERIAL_UNIT
          , ISNULL(B.SYSTEM_LOT_NO ,'')        AS SYSTEM_LOT_NO
          , 0                                  AS STOCK_QTY
          , 0                                  AS IN_QTY
          , 0                                  AS OUT_QTY
          , ISNULL(B2.IN_QTY - B2.OUT_QTY, 0) AS CUR_QTY
          , ISNULL(B.IN_QTY  - B.OUT_QTY,  0) AS TARGET_QTY
          , 0   AS NOW_QTY
          , 0   AS NOW_QTY2
          , ''  AS IO_NO
          , '1' AS GUBUN

      FROM TCO403 AS A WITH(NOLOCK)

          LEFT JOIN TCO101 D WITH(NOLOCK)
          ON  D.CODE_ID1 = '132'
          AND A.PLANT_CODE = D.CODE_ID2        -- 원본: A.PLANT_CODE 기준

          , TMA922M AS B2 WITH(NOLOCK)
          , (
              SELECT  A.FACTORY_CODE
                  ,   A.PLANT_CODE
                  ,   A.WAREHOUSE_CODE
                  ,   A.SYSTEM_LOT_NO
                  ,   A.MATERIAL_CODE
                  ,   SUM(ISNULL(A.IN_QTY, 0))  IN_QTY
                  ,   SUM(ISNULL(A.OUT_QTY, 0)) OUT_QTY
              FROM    TMA922 A WITH(NOLOCK)
              WHERE   A.PLANT_CODE = @PLANT_CODE
              AND     (@WAREHOUSE_CODE = '' OR A.WAREHOUSE_CODE = @WAREHOUSE_CODE)
              AND     A.IO_DATE <= @DATE
              GROUP BY A.FACTORY_CODE, A.PLANT_CODE, A.WAREHOUSE_CODE,
                       A.SYSTEM_LOT_NO, A.MATERIAL_CODE
          ) B
          LEFT JOIN TCO102 C WITH(NOLOCK)
          ON  B.FACTORY_CODE   = C.FACTORY_CODE
          AND B.PLANT_CODE     = C.PLANT_CODE
          AND B.WAREHOUSE_CODE = C.WAREHOUSE_CODE

      WHERE A.MATERIAL_CODE   = B.MATERIAL_CODE
      AND A.PLANT_CODE        = @PLANT_CODE    -- 원본: TCO403 사업장 필터
      AND A.PLANT_CODE        = B.PLANT_CODE   -- 원본: TCO403↔TMA922 사업장 일치 조건
      AND B.FACTORY_CODE      = B2.FACTORY_CODE
      AND B.PLANT_CODE        = B2.PLANT_CODE
      AND B.WAREHOUSE_CODE    = B2.WAREHOUSE_CODE
      AND B.MATERIAL_CODE     = B2.MATERIAL_CODE
      AND B.SYSTEM_LOT_NO     = B2.SYSTEM_LOT_NO
      AND ISNULL(A.DELETE_FLAG, '0') <> '1'
      AND (@WAREHOUSE_CODE = '' OR B.WAREHOUSE_CODE = @WAREHOUSE_CODE)
      AND (@MATERIAL_QUALITY = '' OR A.MATERIAL_QUALITY = @MATERIAL_QUALITY)
      AND (@SEARCH_NAME = '' OR (
              A.MATERIAL_CODE  LIKE '%' + @SEARCH_NAME + '%'
           OR A.MATERIAL_NAME  LIKE '%' + @SEARCH_NAME + '%'
           OR A.PART_NO        LIKE '%' + @SEARCH_NAME + '%'
           OR B2.SYSTEM_LOT_NO LIKE '%' + @SEARCH_NAME + '%'
      ))
      ORDER BY A.PART_NO, B.SYSTEM_LOT_NO
  END
  */


  -- ============================================================
  -- [적용본] 수정된 SP
  -- ============================================================
  ALTER PROC [dbo].[SP_WMA624_01_LIST]
  (
      @FACTORY_CODE        VARCHAR(6),
      @DATE                VARCHAR(8),
      @SEARCH_NAME         VARCHAR(100),
      @WAREHOUSE_CODE      VARCHAR(100),
      @OPMAN_CODE          VARCHAR(10) = '0000',
      @PLANT_CODE          VARCHAR(20) = '001',
      @MATERIAL_QUALITY    VARCHAR(20) = ''
  )
  AS
  BEGIN

      SELECT
            A.MATERIAL_CODE                    AS MATERIAL_CODE
          , A.MATERIAL_NAME                    AS MATERIAL_NAME
          , A.PART_NO                          AS PART_NO
          , A.MATERIAL_SPEC                    AS MATERIAL_SPEC
          , B.PLANT_CODE                       AS PLANT_CODE      -- 수정: A→B (실제 재고 사업장)
          , D.CODE_NAME_FULL                   AS PLANT_NAME
          , B.WAREHOUSE_CODE                   AS WAREHOUSE_CODE
          , C.ETC                              AS WAREHOUSE_CODE_ETC
          , C.WAREHOUSE_NAME                   AS WAREHOUSE_NAME
          , A.UNIT                             AS MATERIAL_UNIT
          , ISNULL(B.SYSTEM_LOT_NO ,'')        AS SYSTEM_LOT_NO
          , 0                                  AS STOCK_QTY
          , 0                                  AS IN_QTY
          , 0                                  AS OUT_QTY
          , ISNULL(B2.IN_QTY - B2.OUT_QTY, 0) AS CUR_QTY
          , ISNULL(B.IN_QTY  - B.OUT_QTY,  0) AS TARGET_QTY
          , 0   AS NOW_QTY
          , 0   AS NOW_QTY2
          , ''  AS IO_NO
          , '1' AS GUBUN

      FROM TCO403 AS A WITH(NOLOCK)

          LEFT JOIN TCO101 D WITH(NOLOCK)
          ON  D.CODE_ID1 = '132'
          AND D.CODE_ID2 = @PLANT_CODE         -- 수정: A.PLANT_CODE→@PLANT_CODE (조회 사업장명 표시)

          , TMA922M AS B2 WITH(NOLOCK)
          , (
              SELECT  A.FACTORY_CODE
                  ,   A.PLANT_CODE
                  ,   A.WAREHOUSE_CODE
                  ,   A.SYSTEM_LOT_NO
                  ,   A.MATERIAL_CODE
                  ,   SUM(ISNULL(A.IN_QTY, 0))  IN_QTY
                  ,   SUM(ISNULL(A.OUT_QTY, 0)) OUT_QTY
              FROM    TMA922 A WITH(NOLOCK)
              WHERE   A.PLANT_CODE = @PLANT_CODE
              AND     (@WAREHOUSE_CODE = '' OR A.WAREHOUSE_CODE = @WAREHOUSE_CODE)
              AND     A.IO_DATE <= @DATE
              GROUP BY A.FACTORY_CODE, A.PLANT_CODE, A.WAREHOUSE_CODE,
                       A.SYSTEM_LOT_NO, A.MATERIAL_CODE
          ) B
          LEFT JOIN TCO102 C WITH(NOLOCK)
          ON  B.FACTORY_CODE   = C.FACTORY_CODE
          AND B.PLANT_CODE     = C.PLANT_CODE
          AND B.WAREHOUSE_CODE = C.WAREHOUSE_CODE

      WHERE A.MATERIAL_CODE   = B.MATERIAL_CODE
      -- 제거: AND A.PLANT_CODE = @PLANT_CODE   (사업장 필터는 TMA922 서브쿼리에서 처리)
      -- 제거: AND A.PLANT_CODE = B.PLANT_CODE  (TCO403↔TMA922 사업장 불일치 허용)
      AND B.FACTORY_CODE      = B2.FACTORY_CODE
      AND B.PLANT_CODE        = B2.PLANT_CODE
      AND B.WAREHOUSE_CODE    = B2.WAREHOUSE_CODE
      AND B.MATERIAL_CODE     = B2.MATERIAL_CODE
      AND B.SYSTEM_LOT_NO     = B2.SYSTEM_LOT_NO
      AND ISNULL(A.DELETE_FLAG, '0') <> '1'
      AND (@WAREHOUSE_CODE = '' OR B.WAREHOUSE_CODE = @WAREHOUSE_CODE)
      AND (@MATERIAL_QUALITY = '' OR A.MATERIAL_QUALITY = @MATERIAL_QUALITY)
      AND (@SEARCH_NAME = '' OR (
              A.MATERIAL_CODE  LIKE '%' + @SEARCH_NAME + '%'
           OR A.MATERIAL_NAME  LIKE '%' + @SEARCH_NAME + '%'
           OR A.PART_NO        LIKE '%' + @SEARCH_NAME + '%'
           OR B2.SYSTEM_LOT_NO LIKE '%' + @SEARCH_NAME + '%'
      ))
      ORDER BY A.PART_NO, B.SYSTEM_LOT_NO
  END