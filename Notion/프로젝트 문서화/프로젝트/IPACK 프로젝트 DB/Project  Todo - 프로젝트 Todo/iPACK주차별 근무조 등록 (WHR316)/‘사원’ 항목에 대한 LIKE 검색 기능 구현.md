---

---
---

## 수정사항

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

## 결과화면

![[image 160.png]]

---
