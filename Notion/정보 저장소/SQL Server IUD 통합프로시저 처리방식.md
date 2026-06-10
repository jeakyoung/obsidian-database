---
base: "[[정보 저장소.base]]"
상태: 시작 전
담당자: []
팀: []
---

```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_TEST4_01_IUD_AJK]    Script Date: 2025-08-01 오전 9:38:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_TEST4_01_IUD_AJK]
    @FACTORY_CODE     VARCHAR(10),
    @EMPLOYEE_NO      VARCHAR(10),
    @BASE_NAME        VARCHAR(10),
    @JOIN_DATE        VARCHAR(8),
    @DEPARTMENT_CODE  VARCHAR(10),
    @OPMAN_CODE       VARCHAR(10),
    @IUD              CHAR(2)
AS
BEGIN
    SET NOCOUNT ON;

    IF @IUD = 'IU'
    BEGIN
        UPDATE TIN114 

          SET   DEPARTMENT_CODE = @DEPARTMENT_CODE,
                BASE_NAME       = @BASE_NAME

        WHERE   EMPLOYEE_NO     = @EMPLOYEE_NO

        IF @@ROWCOUNT = 0

            BEGIN
                INSERT INTO TIN114 (
                    FACTORY_CODE,
                    EMPLOYEE_NO,
                    BASE_NAME,
                    JOIN_DATE,
                    DEPARTMENT_CODE,
                    OPMAN_CODE
                )
                VALUES (
                    @FACTORY_CODE,
                    NEXT VALUE FOR TEST_SEQ,
                    @BASE_NAME,
                    @JOIN_DATE,
                    @DEPARTMENT_CODE,
                    @OPMAN_CODE
                );

            END
    END
    ELSE IF @IUD = 'D'
    BEGIN
        DELETE FROM TIN114
        WHERE
            FACTORY_CODE = @FACTORY_CODE
            AND EMPLOYEE_NO = @EMPLOYEE_NO;
    END
END
```

→  Test4 IUD 프로시저

DEL은 기존방식 대로 개인 고유번호 두가지 매칭후 일치하는 행만 삭제하면 되지만

등록시 기본을 update로 지정하여 사용함


→ IU 동작방식

```sql
    IF @IUD = 'IU'
    BEGIN
        UPDATE TIN114 

          SET   DEPARTMENT_CODE = @DEPARTMENT_CODE,
                BASE_NAME       = @BASE_NAME

        WHERE   EMPLOYEE_NO     = @EMPLOYEE_NO

        IF @@ROWCOUNT = 0

            BEGIN
                INSERT INTO TIN114 (
                    쿼리명 1,
                    쿼리명 2
                )
                VALUES (
                    @value,
                    @value2
                );

            END
    END
```

기본 UPDATE 동작 변할수 있는 부서와 이름을 grid에서 넘겨받은대로 UPDATE 처리

조건은 중복되는 EMPLOYEE_NO (사원번호) 이 있을 경우에만 동작

만약 들어온 데이터 중에 중복되는 사원번호가 없을 경우(신규)

@@ROWCOUNT 는 false로 0값이됨

해당시 신규등록 실행 가져온 모든값을 담아 TIN 114에 등록

ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

→ D 작동 방식

```sql
    ELSE IF @IUD = 'D'
    BEGIN
        DELETE FROM TIN114
        WHERE
            FACTORY_CODE = @FACTORY_CODE
            AND EMPLOYEE_NO = @EMPLOYEE_NO;
```

삭제 동작시 FACTORY_CODE 와 EMPLOYEE_NO가 같을 경우 해당 항목을 TIN114에서 삭제

해당 로직 동작중 404 error 발생

```sql
SELECT A.FACTORY_CODE, A.DEPARTMENT_CODE, B.Department_Name, A.EMPLOYEE_NO, A.BASE_NAME, A.JOIN_DATE
	FROM	 TIN114 AS A
	LEFT JOIN	 TIN122 AS B
	ON A.DEPARTMENT_CODE = B.DEPARTMENT_CODE
```

→ Grid Select 과정에서 FACTORY_CODE을 빼먹은 것을 확인 추가
