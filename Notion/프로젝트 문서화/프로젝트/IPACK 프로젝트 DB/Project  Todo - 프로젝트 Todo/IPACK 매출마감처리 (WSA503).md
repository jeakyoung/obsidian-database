---
base: "[[Notion/프로젝트 문서화/프로젝트/IPACK 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:28:00
담당자: []
---

[SP_WSA503_01_LIST] → 반영예정

```sql
SELECT	A.FACTORY_CODE
		,	ISNULL(A1.CUSTOMER_CODE, '')                                                                AS CUSTOMER_CODE			-- 수주처
		,	ISNULL(A1.CUSTOMER_NAME, '')                                                                AS CUSTOMER_NAME			-- 수주처명
		,	ISNULL(A1.OUT_CUSTOMER_NAME, '')                                                            AS OUT_CUSTOMER_NAME		-- 발주처명
		,	ISNULL(A1.OUT_CUSTOMER_CODE, '')                                                            AS OUT_CUSTOMER_CODE		-- 발주처 코드
	    ,   ISNULL(A1.DELIVERY_CUST_NAME, '')                                                           AS DELIVERY_CUST_NAME		-- 납품처
		,	ISNULL(A1.DELIVER_CUST_CODE , '')                                                           AS DELIVERY_CUST_CODE		-- 납품처 코드
		,   ISNULL(A1.DELIVERY_CUST_SEQ, '')                                                            AS DELIVERY_CUST_SEQ		-- 납품처 시퀀스
		,   ISNULL(A3.INPUT_CUST_CD, ISNULL(A1.DELIVER_CUST_CODE,''))                                   AS INPUT_CUST_CD            -- 계산서 발행처
		,   ISNULL(A3.INPUT_CUST_NM, ISNULL(A1.DELIVERY_CUST_NAME,''))                                  AS INPUT_CUST_NM            -- 계산서 발행처
        
		,	ISNULL(A3.INPUT_CUST_SEQ, '')                                                               AS INPUT_CUST_SEQ
		,	A.ORDER_NO														                            AS ORDER_NO		            -- 수주번호 													  
		,	A.SHIPPING_NO														                        AS SHIPPING_NO	            -- 출하번호
		,	A.SHIPPING_SEQNO                                                                            AS SHIPPING_SEQNO           -- 출하SEQ
        ,	ISNULL(dbo.FN_FORMAT_DATE(A2.SHIPPING_DATE,'1'), '') 	                                    AS SHIPPING_DATE            -- 출하일
		,	ISNULL(A.SHIP_UNIT_QTY, 0) 								                                    AS SHIP_UNIT_QTY            -- 출하량
        ,   ISNULL(A1.SALE_CHARGE,'')                                                                   AS SALE_CHARGE              -- 영업담당자코드
		,	ISNULL(A1.BASE_NAME, '')                                                                    AS SALE_CHARGE_NAME         -- 영업담당자
		,	ISNULL(A4.MATERIAL_NAME,'')                                                                 AS MATERIAL_NAME			-- 품목명
		,	ISNULL(A5.PRESS_PIE,'')                                                                     AS MATERIAL_SPEC			-- 규격		
		--,	A4.MATERIAL_SPEC                                                                            AS MATERIAL_SPEC			-- 규격		
		--,	A4.MATERIAL_CODE                                                                            AS MATERIAL_CODE	        -- 품목코드
		,	ISNULL(A.ITEM_CODE, '')                                                                     AS ITEM_CODE				-- 품목코드
		,	ISNULL(A4.SEARCH_ITEM_NAME, '')                                                             AS SEARCH_ITEM_NAME			-- 검색품목명
		,	ISNULL(A5.MATERIAL_CODE,'')                                                                 AS MATERIAL_CODE	        -- 품목코드
		,	ISNULL(A14.PRESS_FOLD, '')                                                                  AS PRESS_FOLD				-- 층(겹)						       
		,	ISNULL(A14.PRESS_SIZE, '')                                                                  AS PRESS_SIZE				-- 기장
		,	ISNULL(A3.SALES_SUP_AMOUNT,0)                                                               AS SALES_SUP_AMOUNT		    -- 금액
		,	ISNULL(A3.SALES_VAT_AMOUNT, A.SHIP_VAT_AMOUNT)                                              AS SALES_VAT_AMOUNT			-- 출하(부가세)
		,	ISNULL(A8.UPRICE_UNIT, A.SHIP_UPRICE_UNIT)                                                  AS SALES_UNIT				--  단위
		,	ISNULL(A3.SALES_MEMO, '')                                                                   AS SALES_MEMO				-- 비고			
		,	ISNULL(A3.SALES_SEQ, '')                                                                    AS SALES_SEQ				-- 마감순번
		,	ISNULL(A3.SALES_QTY, 0)                                                                     AS SALES_QTY				-- 마감수량
		,	ISNULL(A3.LOSS_QTY, 0)                                                                      AS LOSS_QTY                 -- LOSS수량
		,	ISNULL(A3.BAD_QTY, 0)                                                                       AS BAD_QTY                  -- 반품수량
		,	ISNULL(A3.IWOL_QTY, 0)                                                                      AS IWOL_QTY                 -- 이월수량
		,   CASE WHEN ISNULL(A1.ORDER_GUBUN1,'001') = '001' THEN '1' 
                 WHEN ISNULL(A1.ORDER_GUBUN1,'001') ='002' THEN '2' END                                 AS VAT_GBN
		,	'1'                 																        AS VAT_FLAG                 -- 부가세포함여부 (미포함 고정)
        ,   A1.ORDER_GUBUN1                                                                             AS ORDER_GUBUN1
        --,	A.VAT_GBN																                    AS VAT_GBN                  -- 부가세 구분 
		--,	A.VAT_FLAG																                    AS VAT_FLAG                 -- 부가세포함여부
		,	ISNULL(A1.ORDER_QTY, 0)                                                                     AS ORDER_QTY				-- 수주수량
		--,	ISNULL(A11.CUSTOMER_NAME, '')                                                               AS CAP_COATING_CUST			-- 증착후가공사
		--,	ISNULL(A10.CAP_COATING_COLOR , '')                                                          AS CAP_COATING_COLOR        -- 증착색상
		,	ISNULL(A12.MATERIAL_NAME, '')                                                               AS CAP_NAME                 -- 캡구분
		,	ISNULL(K.CAP_CUSTOMER_NAME, '')                                                             AS CAP_CUSTOMER_NAME        -- 캡 외주처 || 캡 수급처
		,	ISNULL(K.CAP_SPEC1, '')                                                                     AS CAP_SPEC                 -- 캡외경
		,	ISNULL(K.CAP_COLOR1, '')                                                                    AS CAP_COLOR                -- 캡색깔
		
		,	ISNULL(K.CAP_COATING_CUST1, '')																AS CAP_COATING_CUST			--증착후가공사
		,	ISNULL(K.CAP_COATING_COLOR1, '')															AS CAP_COATING_COLOR		--증착색상
		,	ISNULL(A5.PRINT_LABELCUST, '')																AS PRINT_LABELCUST			--라벨공급처
		,	ISNULL(K.CAP_COATING_PROC_NAME1, '')														AS CAP_COATING_PROC_NAME    --증착

		,	CASE WHEN K.AFTER_PROCESS_CUSNAME IS NOT NULL  THEN K.AFTER_PROCESS_CUSNAME ELSE '없음' END AS AFTER_PROCESS_CUSNAME    -- 후가공업체
		,	ISNULL(A10.PRINT_DOSU, '') AS PRINT_DOSU --인쇄 || 옵셋 도수
		--,	ISNULL(A11.CUSTOMER_NAME, '') AS PRINT_LABELCUST --라벨 공급처
		--,	CASE WHEN S.PUMP_CUSTOMER_NAME IS NOT NULL THEN S.PUMP_CUSTOMER_NAME ELSE '없음' END AS PUMP_CUSTOMER_NAME --펌프공급처
		,	CASE WHEN A10.PRINT_DOSU IS NOT NULL THEN CAST(A10.PRINT_DOSU AS VARCHAR) ELSE '없음' END AS PRINT_DOSU         --인쇄도수
		,	CASE WHEN A13.CODE_NAME_FULL IS NOT NULL THEN CAST(A13.CODE_NAME_FULL AS VARCHAR) ELSE '없음' END AS PRINT_SILK_DOSU    --실크도수
		,	CASE WHEN A15.CODE_NAME_FULL IS NOT NULL THEN CAST(A15.CODE_NAME_FULL AS VARCHAR) ELSE '없음' END AS PRINTSTAMP --PRINTSTAMP
		,	CASE WHEN K2.CODE_NAME_FULL IS NOT NULL THEN K2.CODE_NAME_FULL ELSE '없음' END AS AIRLESS_ASSEMBLY --에어리스 조립
		,	CASE WHEN K2.CODE_NAME_FULL IS NOT NULL THEN F4.CODE_NAME_FULL ELSE '없음' END AS PUMP_TYPE --펌프 타입
		,   ISNULL(A7.ORDER_AMOUNT, '')  AS ORDER_AMOUNT   --기계산서 발행액
        
		,	CASE WHEN ISNULL(A3.SALES_UNIT_UPRICE, 0) = 0 THEN ISNULL(A4.STANDARD_PRICE, 0) ELSE ISNULL(A3.SALES_UNIT_UPRICE, 0) END AS SALES_UNIT_UPRICE	-- 단가
		,	CASE WHEN ISNULL(A3.SALES_TOTAL_AMOUNT, 0) = 0 THEN ISNULL(A.SHIP_TOTAL_AMOUNT, 0) ELSE ISNULL(A3.SALES_TOTAL_AMOUNT, 0) END AS SALES_TOTAL_AMOUNT
		,	ISNULL(dbo.FN_FORMAT_DATE(A3.SALES_DATE,'1'), dbo.FN_FORMAT_DATE(CONVERT(VARCHAR(8), GETDATE(), 112),'1')) AS SALES_DATE			--마감일

		,	A3.SALES_DATE
        ,   A3.OPMAN_CODE
        ,   A3.OPTIME
        ,   A3.OPMAN_CODE2
        ,   A3.OPTIME2

        ,	CASE WHEN ISNULL(A.SHIPPING_NO, '') <> '' AND ISNULL(A.SHIPPING_SEQNO, '') <> '' THEN '0'
			WHEN ISNULL(A.SHIPPING_NO, '') = '' OR ISNULL(A.SHIPPING_SEQNO, '') = '' THEN '1'
			ELSE '0' END AS STATE_GBN   --상태여부

		,	CASE WHEN ISNULL(A3.SALES_SEQ, 0) = 0 THEN 0 ELSE 1 END AS END_CHECK	-- 마감
        ,   SA501A.SHIPPING_SEQNO
		,	CASE WHEN ISNULL(A7.SHIPPING_NO, '') = '' THEN 0 ELSE 1 END AS TAX_FLAG	-- 계산서발행여부 및 삭제가능여부 체크플래그
        ,   CASE WHEN ISNULL(A3.SALES_SEQ, 0) > 1 THEN 1 ELSE 0 END SALES_SEQ_FLAG -- 분할마감한것
	

		, LTRIM(RTRIM(
          CASE WHEN ISNULL(K.CAP_NIUM_CUST, '') <> '' THEN K.CAP_NIUM_CUST ELSE '' END
          + CASE WHEN ISNULL(K.CAP_COATING_CUST, '') <> ''
			THEN CASE WHEN ISNULL(K.CAP_NIUM_CUST, '') <> ''
                        THEN ' / ' + K.CAP_COATING_CUST
                        ELSE K.CAP_COATING_CUST
                   END
             ELSE ''
      END
    + CASE
        WHEN ISNULL(K.CAP_BAND_CUST, '') <> ''
             THEN CASE
                    WHEN ISNULL(K.CAP_NIUM_CUST, '') <> '' OR ISNULL(K.CAP_COATING_CUST, '') <> ''
                    THEN ' / ' + K.CAP_BAND_CUST
                    ELSE K.CAP_BAND_CUST
                  END
             ELSE ''
      END
)) AS CAP_LASTCUST_NAME  --후가공업체
	, CASE WHEN S.PUMP_CUSTOMER_NAME IS NOT NULL 
       THEN '(주)아이팩'
       ELSE '없음' 
	END AS PUMP_CUSTOMER_NAME

    FROM TSA403 A
		LEFT JOIN (
			SELECT	A.FACTORY_CODE
				,	A.ORDER_NO
				,	A.ORDER_HISTNO
                ,   A.ORDER_GUBUN1                                          --TSA307 수주구분 (내수/수출)
				,	B.SEARCH_ITEM_NAME 
				,	C.CUSTOMER_CODE                                         --TSA307 수주처코드 
				,	C.CUSTOMER_NAME                                         --TSA307 수주처명
				,   C2.CUSTOMER_NAME AS OUT_CUSTOMER_NAME                   --TSA307 발주처명
				,   C2.CUSTOMER_CODE AS OUT_CUSTOMER_CODE                   --TSA307 발주처 코드
				,   D.DELIVERY_CUST_NAME		                            --TSA308/TCO612 납품처 
				,   ISNULL(D.CUSTOMER_CODE, '') AS DELIVER_CUST_CODE        --납품처 코드 
				,	D.DELIVERY_CUST_SEQ		                                --납품처 시퀀스
                ,   A.SALE_CHARGE                                           --영업담당자
				,   F.BASE_NAME                                             --영업담당자
                ,	E.ITEM_CODE
				,	E.ORDER_UNIT_QTY AS ORDER_QTY
				,	ISNULL(E.DELETE_FLAG, '0') AS DELETE_FLAG
				--,   ISNULL(D.CUSTOMER_CODE, '') AS SALES_CUSTOMER_CODE      --납품처 코드
			FROM	TSA307 A
							
                LEFT JOIN TCO601 B
			    ON A.CUSTOMER_CODE = B.CUSTOMER_CODE
			    AND B.DELETE_FLAG <> '1'
							
                LEFT JOIN TSA308 E
			    ON A.FACTORY_CODE = E.FACTORY_CODE
			    AND A.ORDER_HISTNO = E.ORDER_HISTNO
			    AND	A.ORDER_NO	=	E.ORDER_NO
							
                LEFT JOIN TCO601 C    --수주처 
			    ON A.CUSTOMER_CODE = C.CUSTOMER_CODE  
			    AND C.DELETE_FLAG <> '1'	
							
       --         LEFT JOIN  TCO601 C1  --납품처
			    --ON E.SALES_CUSTOMER_CODE = C1.CUSTOMER_CODE 
							
                LEFT JOIN  TCO601 C2  --발주처
			    ON  A.OUT_CUST= C2.CUSTOMER_CODE 
							
                LEFT JOIN TCO612 D  -- 납품처
			    ON E.SALES_CUSTOMER_CODE = D.CUSTOMER_CODE 
                AND E.DELIVERY_CUSTOMER = D.DELIVERY_CUST_SEQ 
							
                LEFT JOIN TIN114 F --영업담당자
			    ON F.EMPLOYEE_NO = A.SALE_CHARGE
			) A1
			ON  A.FACTORY_CODE = A1.FACTORY_CODE
			AND A.ORDER_NO = A1.ORDER_NO
			AND A.ORDER_HISTNO = A1.ORDER_HISTNO

			LEFT JOIN TSA402 A2
			ON A.FACTORY_CODE = A2.FACTORY_CODE
			AND A.SHIPPING_NO = A2.SHIPPING_NO

			LEFT JOIN TSA408 A3					--단가구성 단가금액 조인인데 이거 아님
			ON A.FACTORY_CODE = A3.FACTORY_CODE
			AND A.SHIPPING_NO = A3.SHIPPING_NO
			AND A.SHIPPING_SEQNO = A3.SHIPPING_SEQNO

            LEFT JOIN TCO601 F3
            ON A3.INPUT_CUST_CD = F3.CUSTOMER_CODE

			INNER JOIN TCO403 A4					
			ON A.ITEM_CODE = A4.MATERIAL_CODE

            INNER JOIN TCO453 A5					
			ON A.ITEM_CODE = A5.MATERIAL_CODE
			 
			LEFT JOIN TSA101 A8
			ON A1.CUSTOMER_CODE = A8.CUSTOMER_CODE
			AND A1.ITEM_CODE = A8.ITEM_CODE

			LEFT JOIN
			(
				SELECT	FACTORY_CODE
					,	SHIPPING_NO
					,	SHIPPING_SEQNO
					,	SALES_SEQ 
					,	SUM(ORDER_QTY) TAX_QTY
					,   ORDER_AMOUNT  -- 기계산 발행액
				FROM	TSA501A 
				GROUP BY FACTORY_CODE, SHIPPING_NO, SHIPPING_SEQNO, SALES_SEQ, ORDER_AMOUNT
			) A7
			ON  A3.FACTORY_CODE = A7.FACTORY_CODE
			AND A3.SHIPPING_NO = A7.SHIPPING_NO
			AND A3.SHIPPING_SEQNO = A7.SHIPPING_SEQNO
			AND A3.SALES_SEQ = A7.SALES_SEQ

            LEFT JOIN
			(
				SELECT	A.FACTORY_CODE
					,	A.SHIPPING_NO
					,	A.SHIPPING_SEQNO
					,	A.SALES_SEQ 
					,	COUNT(TAXBILL_NO) TAX_FLAG
				FROM	TSA501A A
                GROUP BY A.FACTORY_CODE, A.SHIPPING_NO, A.SHIPPING_SEQNO, A.SALES_SEQ
			) SA501A
			ON  A3.FACTORY_CODE     = SA501A.FACTORY_CODE
			AND A3.SHIPPING_NO      = SA501A.SHIPPING_NO
			AND A3.SHIPPING_SEQNO   = SA501A.SHIPPING_SEQNO
			AND A3.SALES_SEQ        = SA501A.SALES_SEQ


			INNER JOIN TCO453  A10						  --A4 : TCO403
			ON A4.MATERIAL_CODE = A10.MATERIAL_CODE

			LEFT JOIN TCO601 A11						  --캡(증착후가공사) 조인
			ON A10. CAP_COATING_CUST = A11.CUSTOMER_CODE 
			AND A10.PRINT_LABELCUST = A11.CUSTOMER_CODE   --라벨 공급처 조인

			LEFT JOIN TCO403 A12						  --캡구분조인
			ON A10.CAP_CODE = A12.MATERIAL_CODE 

			LEFT JOIN TCO101 A13
			ON A10.PRINT_SILK_DOSU = A13.CODE_ID2
			AND A13.CODE_ID1= '136'

			LEFT JOIN TCO453  A14						 --PRESS_FOLD, PRESS_PIE 조인
			ON  A.ITEM_CODE =  A14.MATERIAL_CODE 

			LEFT JOIN TCO101 A15						 --스템핑 조인
			ON  A10.PRINT_STAMP = A15.CODE_ID2
			AND A15.CODE_ID1 = '135'

			LEFT JOIN 	(
					SELECT	 A.FACTORY_CODE
						,	A.MATERIAL_CODE
						,	A.MATERIAL_NAME 
						,	D.CUSTOMER_NAME AS PUMP_CUSTOMER_NAME
						,	F2.CODE_NAME_FULL  AS PUMP_TYPE 
					FROM	TCO403 A
							LEFT JOIN TCO501 B
							ON A.MATERIAL_CODE = B.ITEM_CODE
							LEFT JOIN TCO403 C
							ON B.CHILD_CODE = C.MATERIAL_CODE
							LEFT JOIN TCO453 C1
							ON C1.FACTORY_CODE = C.FACTORY_CODE
							AND C1.MATERIAL_CODE = C.MATERIAL_CODE
							LEFT JOIN TCO601 D  --거래처 조인
							ON A.CUSTOMER_CODE = D.CUSTOMER_CODE 
							LEFT JOIN TCO101 F2
							ON C.MATERIAL_TYPE = F2.CODE_ID2
							AND F2.CODE_ID1 = '191'

					WHERE	C.MATERIAL_BODY_GBN = '003'
					AND		C.MATERIAL_TYPE3 = '001'
				) S --펌프정보
			ON  A1.ITEM_CODE = S.MATERIAL_CODE  --여기 조인 여부 검토해보기
			AND A1.FACTORY_CODE = S.FACTORY_CODE

			LEFT JOIN (
					SELECT	A.FACTORY_CODE
						,	A.MATERIAL_CODE		AS MATERIAL_CODE
						,	A.MATERIAL_NAME		AS MATERIAL_NAME
						,	C.MATERIAL_CODE		AS CAP_CODE
						,	C.MATERIAL_NAME		AS CAP_NAME				--캡타입
						,	C.MATERIAL_COLOR	AS CAP_COLOR1			--캡색상
						,	D.CODE_NAME_FULL    AS	CAP_COATING_PROC_NAME1 --증착
						,	C5.CUSTOMER_NAME	 AS CAP_COATING_CUST1	--증착후가공사
						,	C1.CAP_COATING_COLOR AS CAP_COATING_COLOR1  --증착색상
						--,	C1.PRINT_LABELCUST	 AS PRINT_LABELCUST1    --라벨공급처
						,	C.CUST_CODE
						,	C1.CAP_CUST
						,	C1.PRINT_DOSU
						,	C1.PRINT_SILK_DOSU
						,	C2.CUSTOMER_NAME	AS CAP_CUSTOMER_NAME	--캡수급처
						,	C.MATERIAL_SPEC		AS CAP_SPEC1			--캡 외경  
						,	C3.CUSTOMER_NAME	 AS AFTER_PROCESS_CUSNAME			-- 후가공업체
						,	ISNULL(C4.CUSTOMER_NAME, '')	 AS CAP_NIUM_CUST		-- 늄 후가공업체
						,	ISNULL(C5.CUSTOMER_NAME, '')	 AS CAP_COATING_CUST	-- 증착 후가공업체
						,	ISNULL(C6.CUSTOMER_NAME, '')	 AS CAP_BAND_CUST		-- 박 후가공업체
						,	ISNULL(C7.CUSTOMER_NAME, '')	 AS CAP_LASTCUST
					FROM TCO403 A

					LEFT JOIN TCO501 B
					ON A.MATERIAL_CODE = B.ITEM_CODE

					LEFT JOIN TCO403 C
					ON B.CHILD_CODE = C.MATERIAL_CODE

					LEFT JOIN TCO453 C1
					ON C1.FACTORY_CODE = C.FACTORY_CODE
					AND C1.MATERIAL_CODE = C.MATERIAL_CODE

					LEFT JOIN TCO601 C2 -- 캡 수급처
					ON C.CUSTOMER_CODE = C2.CUSTOMER_CODE

					LEFT JOIN TCO601 C3
					ON C.AFTER_PROCESS_CUST = C3.CUSTOMER_CODE

					LEFT JOIN TCO601 C4 --늄 후가공업체
					ON C1.CAP_NIUM_CUST = C4.CUSTOMER_CODE

					LEFT JOIN TCO601 C5 --증착 후가공업체
					ON C1.CAP_COATING_CUST = C5.CUSTOMER_CODE

					LEFT JOIN TCO601 C6 --박 후가공업체
					ON C1.CAP_BAND_CUST = C6.CUSTOMER_CODE 

					LEFT JOIN TCO601 C7	--마지막 후가공업체
					ON C1.CAP_LASTCUST = C7.CUSTOMER_CODE 

					LEFT JOIN TCO101 D -- 증착 종류
					ON D.CODE_ID1 = '307'
					AND C1.CAP_COATING_PROC = D.CODE_ID2

					WHERE A.MAT_CATA_GBN = 'A'
					AND C.MATERIAL_BODY_GBN = '004'
					) K  --캡정보
			ON  A1.ITEM_CODE = K.MATERIAL_CODE  --여기 조인 여부 검토해보기
			AND A1.FACTORY_CODE = K.FACTORY_CODE

			LEFT JOIN TCO101 K2  --에어리스타입(조립으로 가져오기)
			ON A4.PUMP_AIRLESS_TYPE  = A15.CODE_ID2
			AND A15.CODE_ID1 = '152'

			LEFT JOIN TCO601 F1
			ON A4.AFTER_PROCESS_CUST = F1.CUSTOMER_CODE

			LEFT JOIN TCO101 F4      
			ON A4.MATERIAL_TYPE2 = F4.CODE_ID2
			AND F4.CODE_ID1 = '191' 
			--납품번호, 출하번호로 정렬

WHERE A.FACTORY_CODE = @FACTORY_CODE -- 회사명
	AND (
		(@ORDER_NO <> '' AND A.ORDER_NO LIKE '%' + @ORDER_NO + '%') -- 수주번호
		OR	(
			@ORDER_NO = '' 

            AND 
        (   
            -- 이월포함(@IWOL_FLAG=1) --
            (
                @IWOL_FLAG = '1' 
                AND 
                (
                    (ISNULL(A3.IWOL_QTY, 0) <> 0) 
                    OR 
                    (
                        ISNULL(A3.IWOL_QTY, 0) = 0  
                        AND (
                            (@SHIPPING_DATE_FLAG = '0' OR A2.SHIPPING_DATE BETWEEN @SHIPPING_DATE_FROM AND @SHIPPING_DATE_TO)
                            AND 
                            (@SALES_DATE_FLAG = '0' OR A3.SALES_DATE BETWEEN @SALES_DATE_FROM AND @SALES_DATE_TO)
                        )
                    )
                )
            )
            OR 
            -- 이월미포함(@IWOL_FLAG=0) --
            (
                @IWOL_FLAG = '0' 
                AND ISNULL(A3.IWOL_QTY, 0) = 0  -- 이월수량=0
                AND (
                    (@SHIPPING_DATE_FLAG = '0' OR A2.SHIPPING_DATE BETWEEN @SHIPPING_DATE_FROM AND @SHIPPING_DATE_TO)
                    AND 
                    (@SALES_DATE_FLAG = '0' OR A3.SALES_DATE BETWEEN @SALES_DATE_FROM AND @SALES_DATE_TO)
                )
            )
        )

			AND (
				@REG_GBN = '0' 
				OR (@REG_GBN = '1' AND ISNULL(A3.SALES_SEQ, '') <> '') 
				OR (@REG_GBN = '2' AND ISNULL(A3.SALES_SEQ, '') = '')
				) 
			AND (
				@ITEM_NAME = '' 
				OR (@ITEM_NAME <> '' AND A4.MATERIAL_NAME LIKE '%' + @ITEM_NAME + '%')
                 AND (
                        (@IWOL_FLAG = '0' AND ISNULL(A3.IWOL_QTY, 0) = 0)
                        OR (@IWOL_FLAG = '1' )
                    )
				) 
			AND (
				@OUT_CUSTOMER = '' 
				OR (@OUT_CUSTOMER <> '' AND A1.OUT_CUSTOMER_NAME LIKE '%' + @OUT_CUSTOMER + '%')
				) 
                 AND (
                        (@IWOL_FLAG = '0' AND ISNULL(A3.IWOL_QTY, 0) = 0)
                        OR (@IWOL_FLAG = '1')
                    )
			AND (
				@ORDER_CUSTOMER = '' 
				OR (@ORDER_CUSTOMER <> '' AND A1.CUSTOMER_NAME LIKE '%' + @ORDER_CUSTOMER + '%')
				)
                 AND (
                        (@IWOL_FLAG = '0' AND ISNULL(A3.IWOL_QTY, 0) = 0)
                        OR (@IWOL_FLAG = '1' )
                    )
			AND (
				@DELIVERY_CUSTOMER = '' 
				OR (@DELIVERY_CUSTOMER <> '' AND A1.DELIVERY_CUST_NAME LIKE '%' + @DELIVERY_CUSTOMER + '%')
				)
                 AND (
                        (@IWOL_FLAG = '0' AND ISNULL(A3.IWOL_QTY, 0) = 0)
                        OR (@IWOL_FLAG = '1' )
                    )
            AND (@INPUT_CUST_NM = '' 
                OR (@INPUT_CUST_NM <> ''  AND ((ISNULL(A3.INPUT_CUST_NM,A1.CUSTOMER_NAME) LIKE '%' + @INPUT_CUST_NM + '%')
				)
                 AND (
                        (@IWOL_FLAG = '0' AND ISNULL(A3.IWOL_QTY, 0) = 0)
                        OR (@IWOL_FLAG = '1' )
                    )
			)   
		)
	)
)


	ORDER BY  A.SHIPPING_NO, A.ORDER_NO, A3.SALES_SEQ ASC

    --ORDER BY A3.SALES_DATE, A.ORDER_NO

```
