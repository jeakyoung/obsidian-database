---

---

---

## 기존방식

```sql
ALTER PROCEDURE [dbo].[SP_HHR101_LIST]
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
          A.FACTORY_CODE
        , A.WORK_CODE
        , A.WORK_NAME
        , B.BASE_NAME
        , A.OPTIME
    --  , A.PROD_LIMIT_QTY
        , A.LINE_COUNT
        , A.OUTORDER_FLAG
        , A.VIEW_SEQ
        , A.DELETE_FLAG
        , ISNULL(A.PROD_LIMIT_QTY, SUM(D.PROD_LIMIT_QTY)) AS PROD_LIMIT_QTY
    FROM HHR101 AS A

    LEFT JOIN TIN114 AS B
    ON A.OPMAN_CODE = B.EMPLOYEE_NO
    LEFT JOIN HHR102 AS D --호기정보 
    ON A.FACTORY_CODE = D.FACTORY_CODE
    AND A.WORK_CODE = D.WORK_CODE

    WHERE ISNULL(A.DELETE_FLAG, '0') <> '1'
    GROUP BY
         A.FACTORY_CODE
       , A.WORK_CODE
       , A.WORK_NAME
       , B.BASE_NAME
       , A.OPTIME
       , A.PROD_LIMIT_QTY
       , A.LINE_COUNT
       , A.OUTORDER_FLAG
       , A.VIEW_SEQ
       , A.DELETE_FLAG

    ORDER BY TRY_CAST(A.VIEW_SEQ AS INT) ASC;
END
```

기존 방식은 다음과 같이 GROUP BY를 활용하여 PROD_LIMIT_QTY 값을 SELECT 절에서 직접 연산하고 

있습니다. 해당 부가 많아질수록 유지보수와 데이터 처리 효율이 떨어질 수 있다고 합니다.

---

## 코드 수정

```sql
ALTER PROCEDURE [dbo].[SP_HHR101_LIST]
AS
BEGIN
    SET NOCOUNT ON;

    WITH TEMPSUM AS (
        SELECT
              FACTORY_CODE
            , WORK_CODE
            , SUM(PROD_LIMIT_QTY) AS TEMP

        FROM HHR102
        WHERE ISNULL(DELETE_FLAG, '0') <> '1'
        GROUP BY FACTORY_CODE, WORK_CODE
    )
    SELECT
          A.FACTORY_CODE
        , A.WORK_CODE
        , A.WORK_NAME
        , B.BASE_NAME
        , A.OPTIME
        , A.LINE_COUNT
        , A.OUTORDER_FLAG
        , A.VIEW_SEQ
        , A.DELETE_FLAG
        , CASE
          WHEN A.PROD_LIMIT_QTY != 0 THEN A.PROD_LIMIT_QTY
          ELSE C.TEMP
          END AS PROD_LIMIT_QTY

    FROM HHR101 AS A
    LEFT JOIN TIN114 AS B
    ON A.OPMAN_CODE = B.EMPLOYEE_NO

    LEFT JOIN TEMPSUM AS C
    ON C.FACTORY_CODE = A.FACTORY_CODE
    AND C.WORK_CODE    = A.WORK_CODE

    WHERE ISNULL(A.DELETE_FLAG, '0') <> '1'
    ORDER BY TRY_CAST(A.VIEW_SEQ AS INT) ASC;
END

```

다음과 같이 WITH절을 사용하여 TEMPSUM이라는 임시테이블을 만들어 준뒤에 SUM계산을 시행, 저장

SELECT할때 CASE를 사용하여 PROD_LIMIT에 변경된 값이 존재해 DEFAULT값이 0이 아닐때  변경값으로

조회 그것이 아닌 상황이라면 아래에서 JOIN시켜 사전에 계산을 완료한 TEMP값을 가져옴으로서

공정그리드내 강제변경한 생산수량 값이 없을경우 호기 그리드내 값을 자동으로 더해주는 로직으로

구현했습니다.

