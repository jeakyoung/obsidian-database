---
title: MSSQL 특수문자 LIKE 검색
date: 2026-06-10
type: 작업
project: IPACK
status: 진행중
priority: 보통
assignee: []
tags: []
created: 2026-06-10T14:28:00
---

# MSSQL 특수문자 LIKE 검색

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-06-10 |
| **대상 시스템** | 공통(MSSQL 쿼리) |
| **관련 화면·프로그램** | TCO403 (품목마스터) LIKE 검색 사례 |

## 🔍 현상 및 원인

## 🔧 조치 내용

### **1) **`**%**`** (퍼센트)**

- 의미: 0개 이상의 모든 문자
- 예: `LIKE '%abc%'` → 아무 문자 + abc + 아무 문자

✔ 그대로 검색하고 싶은 경우

```sql
WHERE column LIKE '%\%%' ESCAPE '\'


```

---

### **2) **`**_**`** (언더스코어)**

- 의미: 단일 문자 1개
- 예: `LIKE '_a_'` → 아무 문자 + a + 아무 문자

✔ 그대로 검색하려면

```sql
WHERE column LIKE '%\_%' ESCAPE '\'


```

---

### **3) **`**[]**`** (대괄호 세트)**

- 의미: 문자 집합, 범위 지정
- 예: `[a-z]`, `[abc]`

✔ 문자 그대로 검색하려면

```sql
WHERE column LIKE '%\[abc\]%' ESCAPE '\'


```

또는

```sql
WHERE column LIKE '%[[]abc[]]%'


```

### 해결방법

```sql
SELECT MATERIAL_NAME FROM TCO403
WHERE MATERIAL_NAME LIKE '%' + REPLACE(REPLACE('에이본', '[', '\['), ']', '\]') + '%' ESCAPE '\'
```

→ 다음과 같이 ESCAPE 이용하여 특수문자를 문자로 사용할수있다.

```sql
SELECT MATERIAL_NAME FROM TCO403
WHERE MATERIAL_NAME LIKE '%' + REPLACE(REPLACE('[에이본]', '[', ''), ']', '') + '%'
```

→ 또는 다음과같이 그냥 대문자만 조회조건에서 빼도된다.

## ✅ 검증 및 결과

MSSQL `LIKE` 이스케이프 문법(`%`, `_`, `[]`, `ESCAPE`) 자체는 표준 T-SQL 동작이라 별도 코드 대조가 필요 없음.

## 🔗 참고
