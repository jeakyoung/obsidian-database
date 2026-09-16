---
title: ‘사원’ 항목에 대한 LIKE 검색 기능 구현
date: 2026-06-10
type: 작업
project: IPACK
status: 진행중
priority: 보통
assignee: []
tags: []
---

# ‘사원’ 항목에 대한 LIKE 검색 기능 구현

## 1. 개요

| 항목 | 내용 |
|------|------|
| 요청자 |  |
| 요청일 | 2026-06-10 |
| 대상 시스템 |  |
| 관련 화면·프로그램 |  |

## 2. 현상 및 원인

## 3. 조치 내용

---

### 수정사항

![[image 159.png]]

개선 전에는 다음과 같이 프로시저 내에서 정확히 같은것만 SELECT 하고 있기에 이름의 두글자를 입력해도 

검색이 불가합니다.

```sql
WHERE 1=1
	AND	(@WG_CODE   = '' OR (@WG_CODE <> '' AND T2.WG_CODE = @WG_CODE))
	AND	(@DEPT_NAME = '' OR (@DEPT_NAME <> '' AND T1.Department_Name  = @DEPT_NAME))
	AND	(@BASE_NAME = '' OR (@BASE_NAME <> '' AND T1.BASE_NAME LIKE '%'+@BASE_NAME+'%'))
	ORDER BY T1.DEPARTMENT_SEQ, T1.VIEW_SEQ, T1.BASE_NAME 
```

다음과 같이 WHERE 절에 LIKE ‘%’+@BASE_name+’%’ 절을 추가하여 부분일치 검색이 가능합니다.

---

### 결과화면

![[image 160.png]]

---

## 4. 검증 및 결과

## 5. 참고
