---

---

## Execute

```java
boolean result2 = pstmt.execute();
```

→ 반환값이 Boolean 타입인 값을 반환해 주는 함수입니다.

→ 반환값이 bool타입이 아닌경우 에러가 발생합니다.

## ExecuteQuery

```java
ResultSet rs = pstmt.executeQuery();
```

→ 쿼리문의 수행 결과로 받게된 값을 rs로 반환합니다.

→ 보통 SELECT문의 수행결과를 담아주는 함수입니다.

## ExecuteUpdate

```java
int result2 = pstmt.executeUpdate();
```

→ 수행결과로 int를 반환합니다.

→ 주로 IUD 구문중 레코드 건수를 세서 반환하는 역활을 수행합니다.