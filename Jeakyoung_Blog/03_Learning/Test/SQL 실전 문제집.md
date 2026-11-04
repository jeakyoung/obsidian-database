---
title: SQL 실전 문제집
date: 2026-10-14
type: 학습자료
status: 완료
tags: []
---

# SQL 실전 문제집

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **분류** | 면접준비 |
| **관련 기술** | Oracle, MS SQL, SQL |
| **정리일** | 2026-10-14 |

> Oracle/MS SQL 문법 차이, 서브쿼리, 윈도우 함수, 페이징, 계층형 쿼리까지 면접 코딩테스트 SQL형 문제 대비. 정답/해설 포함.

## 🧩 핵심 개념

- Oracle과 MS SQL은 **같은 개념, 다른 문법**인 경우가 대부분 — 대응표로 묶어서 기억
- 실무형 SQL 문제는 대부분 JOIN + GROUP BY + 서브쿼리/윈도우 함수 조합으로 풀림
- PLM(BOM) 도메인에서는 계층형(트리) 쿼리가 특히 중요

## 📖 상세 내용

### 0. Oracle vs MS SQL 문법 대응표

| 용도 | Oracle | MS SQL |
|:--|:--|:--|
| 상위 N건 | `WHERE ROWNUM <= N` | `SELECT TOP N` |
| 페이징 | `OFFSET n ROWS FETCH NEXT m ROWS ONLY` (12c+) | `OFFSET n ROWS FETCH NEXT m ROWS ONLY` (2012+, `ORDER BY` 필수) |
| NULL 대체 | `NVL(a, b)` | `ISNULL(a, b)` |
| NULL 대체 (공통) | `COALESCE(a, b, ...)` | `COALESCE(a, b, ...)` |
| 문자열 연결 | `a \|\| b` | `a + b` 또는 `CONCAT(a, b)` |
| 현재 일시 | `SYSDATE` | `GETDATE()` |
| 문자열 자르기 | `SUBSTR(s, 시작, 길이)` | `SUBSTRING(s, 시작, 길이)` |
| 조건 분기 | `DECODE(...)` 또는 `CASE` | `CASE` |
| 자동 증가 키 | `SEQUENCE` + `.NEXTVAL` (12c+는 IDENTITY도 가능) | `IDENTITY(1,1)` |
| 계층형 조회 | `START WITH ... CONNECT BY PRIOR` | 재귀 CTE (`WITH ... UNION ALL`) |

> 공통 문법(`CASE`, `COALESCE`, ANSI JOIN)을 우선 쓰면 DB가 바뀌어도 수정할 곳이 줄어든다.

### 문제 1 — 급여 상위 3명 (ROWNUM 함정)

Q. Oracle에서 아래 쿼리는 왜 "급여 상위 3명"이 아닐까요?

```sql
SELECT * FROM EMP WHERE ROWNUM <= 3 ORDER BY SAL DESC;
```

A. `ROWNUM`은 `ORDER BY`보다 **먼저** 매겨진다. 즉 아무 행 3개를 먼저 뽑은 뒤 그 3개만 정렬한 결과. 정렬을 서브쿼리 안에서 먼저 해야 한다.

```sql
-- Oracle
SELECT * FROM (SELECT * FROM EMP ORDER BY SAL DESC) WHERE ROWNUM <= 3;

-- MS SQL
SELECT TOP 3 * FROM EMP ORDER BY SAL DESC;
```

### 문제 2 — 평균보다 급여가 높은 직원 (서브쿼리)

```sql
SELECT EMP_ID, NAME, SAL
FROM EMP
WHERE SAL > (SELECT AVG(SAL) FROM EMP);
```

- 집계 함수(`AVG`)는 `WHERE`에 바로 쓸 수 없으므로 서브쿼리로 값을 먼저 구한다

### 문제 3 — 부서별 최고 급여 직원 (윈도우 함수)

```sql
SELECT DEPT_ID, EMP_ID, NAME, SAL
FROM (
    SELECT E.*,
           ROW_NUMBER() OVER (PARTITION BY DEPT_ID ORDER BY SAL DESC) AS RN
    FROM EMP E
) T
WHERE RN = 1;
```

- `PARTITION BY`는 "그룹별로 나눠서", `ORDER BY`는 "그 안에서 순번 매기기" — `GROUP BY`와 달리 원래 행이 그대로 남는다
- Oracle/MS SQL 모두 동일한 문법으로 동작

**꼬리질문: `ROW_NUMBER` / `RANK` / `DENSE_RANK` 차이** (급여 300, 300, 200 기준)

| 함수 | 결과 | 특징 |
|:--|:--|:--|
| `ROW_NUMBER()` | 1, 2, 3 | 동점이어도 무조건 다른 번호 |
| `RANK()` | 1, 1, 3 | 동점은 같은 순위, 다음 순위는 건너뜀 |
| `DENSE_RANK()` | 1, 1, 2 | 동점은 같은 순위, 건너뛰지 않음 |

### 문제 4 — 중복 데이터 찾기

Q. 같은 이메일로 가입한 회원이 여러 명인 경우를 찾으세요.

```sql
SELECT EMAIL, COUNT(*) AS CNT
FROM MEMBER
GROUP BY EMAIL
HAVING COUNT(*) > 1;
```

- 그룹화 후 조건이므로 `WHERE`가 아니라 `HAVING`

### 문제 5 — 페이징 (10건씩, 2페이지 = 11~20번째)

```sql
-- 공통 (Oracle 12c+ / MS SQL 2012+)
SELECT * FROM BOARD
ORDER BY CREATED_AT DESC
OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY;

-- Oracle 구버전 (ROWNUM 2중 서브쿼리)
SELECT * FROM (
    SELECT A.*, ROWNUM AS RN
    FROM (SELECT * FROM BOARD ORDER BY CREATED_AT DESC) A
    WHERE ROWNUM <= 20
)
WHERE RN > 10;
```

- 레거시 시스템(ENOVIA 고객사 포함)에서는 구버전 ROWNUM 패턴을 자주 보게 되므로 읽을 줄은 알아야 함

### 문제 6 — NOT IN과 NULL 함정

Q. 주문이 없는 고객을 찾으려고 아래처럼 썼는데 결과가 0건입니다. 왜일까요?

```sql
SELECT * FROM CUSTOMER
WHERE CUST_ID NOT IN (SELECT CUST_ID FROM ORDERS);
```

A. `ORDERS.CUST_ID`에 NULL이 하나라도 있으면 `NOT IN` 비교 결과가 전부 UNKNOWN이 되어 0건이 된다. `NOT EXISTS`로 바꾸면 안전하다.

```sql
SELECT * FROM CUSTOMER C
WHERE NOT EXISTS (SELECT 1 FROM ORDERS O WHERE O.CUST_ID = C.CUST_ID);
```

### 문제 7 — BOM 계층 조회 (Oracle CONNECT BY)

부품 테이블 `PART(PART_ID, PARENT_PART_ID, PART_NAME)`에서 최상위 부품부터 트리 형태로 조회.

```sql
SELECT LEVEL,
       LPAD(' ', (LEVEL - 1) * 2) || PART_NAME AS TREE,
       PART_ID, PARENT_PART_ID
FROM PART
START WITH PARENT_PART_ID IS NULL
CONNECT BY PRIOR PART_ID = PARENT_PART_ID;
```

- `START WITH`: 시작점(루트), `CONNECT BY PRIOR 부모쪽컬럼 = 자식쪽컬럼`: 연결 조건, `LEVEL`: 깊이
- MS SQL 버전(재귀 CTE)은 [[03_Learning/Test/기술스택 종합 문제]] 9번 참고

### 문제 8 — 있으면 수정, 없으면 입력 (MERGE)

```sql
MERGE INTO PART_STOCK T
USING (SELECT 'P001' AS PART_ID, 50 AS QTY FROM DUAL) S  -- MS SQL은 FROM DUAL 생략
ON (T.PART_ID = S.PART_ID)
WHEN MATCHED THEN
    UPDATE SET T.QTY = T.QTY + S.QTY
WHEN NOT MATCHED THEN
    INSERT (PART_ID, QTY) VALUES (S.PART_ID, S.QTY);
```

- MS SQL은 문장 끝에 세미콜론이 필수이고 `ON` 괄호는 생략 가능
- "UPSERT를 어떻게 하나요?"라는 질문이 나오면 `MERGE`를 언급하면 충분

## 💡 정리 및 활용

- 1번(ROWNUM 정렬 순서)과 6번(NOT IN + NULL)은 "왜 틀렸는지" 설명형으로 자주 나오는 함정 문제
- 윈도우 함수(3번)는 "그룹별 1등" 유형의 정석 풀이 — `GROUP BY`로 못 푸는 이유(다른 컬럼을 같이 못 가져옴)까지 말할 수 있으면 좋음
- 대응표(0번)는 면접 전 한 번 훑어보기만 해도 Oracle/MS SQL 질문 대부분 커버 가능

## 🔗 참고

- [[03_Learning/Test/기술스택 종합 문제]]
- [[03_Learning/Test/코딩테스트 종합 문제집]]
- [[03_Learning/Test/코딩테스트 기본 개념 문제]]
