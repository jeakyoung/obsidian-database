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

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-06-10 |
| **대상 시스템** | iPlusERP |
| **관련 화면·프로그램** | [[01_Projects/02_IPACK/02_TechDocs/근태_2기능스펙/[기술] WHR316 주차별 근무조 등록\|WHR316 주차별 근무조 등록]] |

## 🔍 현상 및 원인

`SP_WHR316_01_LIST`가 `T1.BASE_NAME = @BASE_NAME`로 정확히 일치하는 값만 조회해서, 사원명 두 글자만 입력해도 검색이 되지 않음.

## 🔧 조치 내용

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

## ✅ 검증 및 결과

- [ ] `SP_WHR316_01_LIST`는 DB 저장 프로시저라 레포에 원문이 없어, 이 LIKE 수정이 실제로 반영된 현재 SP 본문인지는 미확인. `jvWHR316_LIST.java`는 `BASE_NAME` 파라미터를 그대로 SP에 넘기기만 해서 LIKE 처리 자체는 SP 내부에 있음.

## 🔗 참고

- [[01_Projects/02_IPACK/02_TechDocs/근태_2기능스펙/[기술] WHR316 주차별 근무조 등록|WHR316 주차별 근무조 등록 스펙]]
- [[01_Projects/02_IPACK/01_Tasks/MSSQL 특수문자 LIKE 검색|MSSQL 특수문자 LIKE 검색]] — 같은 LIKE 패턴의 일반 원칙 정리
