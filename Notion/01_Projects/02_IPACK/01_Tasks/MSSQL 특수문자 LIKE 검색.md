---
base: "[[Notion/프로젝트 문서화/프로젝트/IPACK 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 진행 중
생성 일시: 2026-06-10T14:28:00
담당자: []
---
# ✅ LIKE 검색에서 문제를 일으키는 특수문자 3개

## **1) **`**%**`** (퍼센트)**

- 의미: 0개 이상의 모든 문자
- 예: `LIKE '%abc%'` → 아무 문자 + abc + 아무 문자

✔ 그대로 검색하고 싶은 경우

```sql
WHERE column LIKE '%\%%' ESCAPE '\'


```

---

## **2) **`**_**`** (언더스코어)**

- 의미: 단일 문자 1개
- 예: `LIKE '_a_'` → 아무 문자 + a + 아무 문자

✔ 그대로 검색하려면

```sql
WHERE column LIKE '%\_%' ESCAPE '\'


```

---

## **3) **`**[]**`** (대괄호 세트)**

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

## 해결방법

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
