---

---
---

## 피드백 정리

- OPMAN_CODE, CODE2를 파라미터로 받을 필요가 없음

- 사용자 아이디 4자리 → TIN114 테이블 확인하고 수정하기

- OPMAN_CODE, CODE2 가 분리되었으면 조회 쿼리가 어떻게 이루어 지는지

---

## OPMAN_CODE, CODE2 의 조회쿼리

```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_HHR102_LIST]    Script Date: 2025-09-04 오후 5:23:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[SP_HHR102_LIST]
    @FACTORY_CODE  VARCHAR(6),
    @WORK_CODE     VARCHAR(6),
	--@LINE_CODE              VARCHAR(3),
    --@LINE_NAME              VARCHAR(8),
    --@PROD_LIMIT_QTY         VARCHAR(20),
    --@BASE_NAME              VARCHAR(5),
    --@LINE_INSP_DATE         VARCHAR(24),
    --@OPMAN_TIME             VARCHAR(20),
    --@IMPORTANT_LINE_FLAG    VARCHAR(1),
    --@VIEW_SEQ               VARCHAR(10),
    @DELETE_FLAG   VARCHAR(1)
AS
BEGIN
    SET NOCOUNT ON;
	--WITH BASE_NAME2 AS (
	--	SELECT
	--	A.FACTORY_CODE
	--	,A.WORK_CODE
	--	,A.OPMAN_CODE2
	--	,B.BASE_NAME AS BASE_NAME2
	--FROM HHR102 AS A
	--LEFT JOIN TIN114 AS B
	--ON A.OPMAN_CODE = B.EMPLOYEE_NO
	--WHERE ISNULL(A.DELETE_FLAG, '0') <> '1'
 --   GROUP BY A.FACTORY_CODE, A.WORK_CODE
	--)

    SELECT
          B.FACTORY_CODE
        , B.WORK_CODE
        , A.LINE_CODE
        , A.LINE_NAME
        , A.PROD_LIMIT_QTY
        , C1.BASE_NAME
		    , C2.BASE_NAME AS BASE_NAME2
        , A.LINE_INSP_DATE
        , A.OPMAN_TIME
        , A.OPTIME2
        , A.IMPORTANT_LINE_FLAG
        , A.VIEW_SEQ
        , A.DELETE_FLAG

    FROM  HHR102 AS A
    LEFT JOIN HHR101 AS B
    ON A.WORK_CODE = B.WORK_CODE
    LEFT JOIN TIN114 AS C1
    ON A.OPMAN_CODE  = C1.EMPLOYEE_NO
    LEFT JOIN TIN114 AS C2
    ON A.OPMAN_CODE2 = C2.EMPLOYEE_NO
    WHERE
          B.FACTORY_CODE = @FACTORY_CODE
      AND A.WORK_CODE    = @WORK_CODE
      AND (
            @DELETE_FLAG = '1'                             
            OR ISNULL(A.DELETE_FLAG,'0') <> '1'
          )
    ORDER BY TRY_CAST(A.VIEW_SEQ AS INT) ASC;
END
GO
```

다음과 같은 방식으로 C1과 C2로 나누어 C1조회시 OPMAN_CODE를 사용하여 비교한뒤 BASENAME으로

출력해주고 C2조회시 OPMAN_CODE2를 사용하여 BASENAME을 가져온뒤 BASE_NAME2라는 이름을

붙여 출력해줍니다.

```javascript

                            text: replaceLocale('최초등록자'),
                            width: 80,
                            dataIndex: 'BASE_NAME',
                            align: 'center',
                            editor: null,
                        },
                        {
                            text: replaceLocale('최종수정자'),
                            dataIndex: 'BASE_NAME2',
                            align: 'center',
                            editor: null,
                            width: 80,
                        },
```

이후 다음과 같은 방식으로 BASE_NAME과 BASE_NAME2를 별개 출력하도록 만들었습니다.

---

## 사용자 아이디 4자리 → TIN114 확인하기

<!-- Column 1 -->
![[image 47.png]]

<!-- Column 2 -->
![[image 48.png]]

- TIN114 내부에서 EMPLOYEE_NO를 OPMAN_CODE로 비교해서 가져오는데 둘의 데이터 형식은

같으나 길이가 맞지 않습니다.

![[image 49.png]]

- 따라서 다음과 같이 OPMAN_CODE의 데이터 형식을 VARCHAR(20)으로 수정했습니다.

---

## OPMAN_CODE, CODE2를 파라미터로 받을 필요가 없음

```sql
ALTER PROCEDURE [dbo].[SP_HHR102_LIST]
    @FACTORY_CODE  VARCHAR(6),
    @WORK_CODE     VARCHAR(6),
	--@LINE_CODE              VARCHAR(3),
    --@LINE_NAME              VARCHAR(8),
    --@PROD_LIMIT_QTY         VARCHAR(20),
    --@BASE_NAME              VARCHAR(5),
    --@LINE_INSP_DATE         VARCHAR(24),
    --@OPMAN_TIME             VARCHAR(20),
    --@IMPORTANT_LINE_FLAG    VARCHAR(1),
    --@VIEW_SEQ               VARCHAR(10),
    @DELETE_FLAG   VARCHAR(1)
AS
BEGIN
```

조회기능에서는 테이블에 저장된 OPMAN_CODE를 찾아와서 조회에만 사용하기 때문에 파라미터를 받을

필요가 없습니다. 따라서 조회 구분에만 필요한 공장, 공정, 삭제정보 코드만 받아옵니다.

---

## 결과화면

![[image 50.png]]

다음과 같이 수정시 최종수정자, 최종 변경일시가 변경될수 있게 구현했습니다.