---

---

---

# PreparedStatement — SQL Injection을 막는 쿼리 실행 방식

> SQL Injection은 공격자가 악의적인 SQL을 입력해 DB를 마음대로 조작하는 공격입니다.
실제 서비스에서 발생하면 전체 데이터가 유출되거나 삭제될 수 있는 **치명적인 보안 취약점**입니다.
PreparedStatement는 이를 원천 차단하는 기술입니다.

---

## 1. SQL Injection이란 무엇인가

사용자가 입력한 값이 SQL 쿼리에 **직접 문자열로 삽입**될 때 발생하는 보안 취약점입니다. 공격자가 입력값에 SQL 문법을 섞어 넣어 원래 의도와 다른 쿼리가 실행되도록 만듭니다.

```plain text
개발자 의도:  "사용자가 입력한 username으로 유저를 조회한다"
공격자 의도:  "username 조건을 무력화하고 모든 유저 정보를 꺼낸다"
              또는 "users 테이블 전체를 삭제한다"
```

OWASP(국제 웹 보안 기구)가 발표하는 **웹 보안 취약점 Top 10에 항상 포함**되는 공격입니다.

---

## 2. SQL Injection 공격 예시

### 로그인 우회 공격

취약한 코드 — 입력값을 그대로 SQL에 삽입:

```java
String sql = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'";
```

일반 사용자가 입력하면 정상 동작합니다:

```sql
SELECT * FROM users WHERE username = 'jeakyung' AND password = '1234'
```

공격자가 username에 `' OR '1'='1' --` 를 입력하면:

```sql
SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password = '...'
-- '1'='1'은 항상 참 → 모든 유저 반환 → 비밀번호 없이 로그인 성공
-- -- 이후는 주석 처리되어 password 조건 무시됨
```

### 데이터 삭제 공격

공격자가 검색창에 `'; DROP TABLE users; --` 를 입력하면:

```sql
SELECT * FROM events WHERE title = ''; DROP TABLE users; --'
-- users 테이블 전체 삭제!
```

### 데이터 전체 유출 공격

```sql
SELECT id, title FROM events WHERE space_id = 1 UNION SELECT id, password FROM users --
-- events 데이터와 함께 users의 비밀번호까지 반환
```

---

## 3. PreparedStatement란 무엇인가

PreparedStatement는 SQL의 **구조(틀)와 데이터(값)를 분리해서 실행**하는 방식입니다.

```plain text
일반 Statement (취약):
  SQL = "SELECT * FROM users WHERE username = 'jeakyung'"
  → SQL 전체가 문자열로 DB에 전달됨
  → 입력값이 SQL 명령어로 해석될 수 있음

PreparedStatement (안전):
  SQL 틀  = "SELECT * FROM users WHERE username = ?"
  입력값  = "jeakyung"
  → DB가 먼저 SQL 구조를 파싱하고 실행 계획 수립
  → 입력값을 순수한 "데이터"로만 바인딩
  → 입력값이 절대 SQL 명령어로 해석되지 않음
```

내부 동작 순서:

```plain text
1. DB에 SQL 틀 전송: "SELECT * FROM users WHERE username = ?"
2. DB가 SQL 파싱 및 실행 계획 수립 (이 시점에 SQL 구조 확정)
3. 파라미터 값 전송: "jeakyung" (또는 공격 문자열)
4. DB가 값을 문자열 데이터로만 처리 → SQL 구조 변경 불가
5. 쿼리 실행
```

---

## 4. PreparedStatement가 SQL Injection을 막는 원리

공격자가 `' OR '1'='1' --` 를 입력해도 막히는 이유:

```plain text
SQL 틀: SELECT * FROM users WHERE username = ?

파라미터 바인딩:
  ? = "' OR '1'='1' --"  ← 이 전체가 하나의 문자열 값으로 처리됨

실제 실행:
  → username이 정확히 ' OR '1'='1' -- 인 유저를 찾음
  → 그런 유저가 없으므로 결과 없음 (공격 실패)
```

SQL 구조가 이미 확정된 뒤에 값이 바인딩되므로 **어떤 입력값도 SQL 명령어로 해석되지 않습니다.**

---

## 5. MyBatis에서 `#{}` vs `${}` — 실무 적용

| 구분 | 방식 | SQL Injection |
| --- | --- | --- |
| `#{}` | PreparedStatement — 값을 파라미터로 바인딩 | 방어됨 |
| `${}` | 문자열 직접 치환 — SQL에 값을 그대로 삽입 | 취약 |

`#{}` — 안전한 방식 (기본으로 항상 사용):

```xml
<select id="findByUsername" resultMap="userResultMap">
    SELECT id, username, email
    FROM users
    WHERE username = #{username}
</select>
```

실제 DB에 전달되는 형태:

```sql
SELECT id, username, email FROM users WHERE username = ?
-- 바인딩: ? = "jeakyung"
```

`${}` — 문자열 직접 삽입 (위험):

```xml
<select id="findByUsername" resultMap="userResultMap">
    SELECT id, username, email
    FROM users
    WHERE username = '${username}'
</select>
```

공격 입력 시:

```sql
-- 공격 입력: ' OR '1'='1' --
SELECT id, username, email FROM users WHERE username = '' OR '1'='1' --'
-- SQL Injection 성공!
```

>  `${}` 는 사용자 입력값을 절대 받으면 안 됩니다. 테이블명, 컬럼명 등 코드에서 직접 제어하는 값에만 제한적으로 사용합니다.

---

## 6. 실제로 위험한 `${}` 사용 사례

검색 기능에서 잘못 사용:

```xml
<select id="searchEvents">
    SELECT * FROM events
    WHERE title LIKE '%${keyword}%'
</select>
```

공격자가 `%'; DROP TABLE events; --` 입력 시:

```sql
SELECT * FROM events WHERE title LIKE '%%'; DROP TABLE events; --%'
-- events 테이블 전체 삭제!
```

올바른 수정 방법 — `#{}` 와 문자열 연결로 처리:

```xml
<select id="searchEvents">
    SELECT * FROM events
    WHERE title LIKE '%' || #{keyword} || '%'
</select>
```

또는 Java에서 미리 `%` 붙여서 넘기기:

```java
String likeKeyword = "%" + keyword + "%";
eventMapper.searchByKeyword(likeKeyword);
```

```xml
WHERE title LIKE #{keyword}
```

---

## 7. `${}` 를 써야만 하는 경우와 안전하게 쓰는 법

`${}` 가 필요한 경우는 **테이블명이나 컬럼명을 동적으로 지정**할 때입니다. PreparedStatement는 값만 파라미터로 바인딩할 수 있고, 테이블명/컬럼명은 바인딩이 불가합니다.

```xml
<select id="findEventsSorted">
    SELECT * FROM events
    WHERE space_id = #{spaceId}
    ORDER BY ${sortColumn} ${sortDirection}
</select>
```

이때 반드시 **화이트리스트 검증**을 Java에서 수행해야 합니다:

```java
private static final Set<String> ALLOWED_COLUMNS =
    Set.of("start_date", "title", "created_at");

private static final Set<String> ALLOWED_DIRECTIONS =
    Set.of("ASC", "DESC");

public List<EventResponse> findEventsSorted(String sortColumn, String sortDirection) {
    if (!ALLOWED_COLUMNS.contains(sortColumn)) {
        sortColumn = "start_date";      // 허용 목록에 없으면 기본값
    }
    if (!ALLOWED_DIRECTIONS.contains(sortDirection.toUpperCase())) {
        sortDirection = "ASC";
    }
    return eventMapper.findEventsSorted(spaceId, sortColumn, sortDirection);
}
```

---

## 8. 자주 하는 실수

### ① `${}` 로 검색어 받기

```xml
<!-- 가장 흔한 실수 -->
WHERE title LIKE '%${keyword}%'

<!-- 항상 #{}로 -->
WHERE title LIKE '%' || #{keyword} || '%'
```

### ② LIKE에 특수문자 이스케이프 안 하기

사용자가 `%`나 `_`를 검색어로 입력하면 LIKE 패턴으로 해석됩니다.

```java
// 특수문자 이스케이프 처리
String safeKeyword = keyword
    .replace("\\", "\\\\")
    .replace("%", "\\%")
    .replace("_", "\\_");
```

### ③ `#{}` 쓸 때 따옴표를 직접 추가하는 실수

`#{}` 는 값 타입에 따라 따옴표를 자동으로 처리합니다. 직접 추가하면 오류가 납니다.

```xml
<!-- 따옴표 직접 추가 — 오류 발생 -->
WHERE username = '#{username}'

<!-- #{} 만 쓰면 됨 -->
WHERE username = #{username}
```

---
