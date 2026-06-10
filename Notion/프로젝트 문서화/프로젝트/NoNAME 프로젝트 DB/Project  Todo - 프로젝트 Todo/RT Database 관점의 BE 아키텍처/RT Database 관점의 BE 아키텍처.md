---
base: "[[Notion/프로젝트 문서화/프로젝트/샘플 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 진행 중
생성 일시: 2026-06-10T14:29:00
담당자:
  - 안재경
---
# DB 관점의 백엔드 아키텍처

---

## 1. DB 연결은 어떻게 이루어지는가

### DataSourceConfig.java — 백엔드와 DB를 연결하는 설정 파일

백엔드 서버가 시작될 때 가장 먼저 하는 일 중 하나가 **DB에 접속하는 것**입니다.
사람으로 치면 "어느 회사 어느 부서에 출근할지" 알아야 일을 시작할 수 있는 것과 같습니다.
이 설정이 없거나 잘못되면 서버가 실행되자마자 오류가 납니다.

```java
// 환경변수 DATABASE_URL 형태: postgresql://user:password@host:5432/dbname
ds.setJdbcUrl("jdbc:postgresql://host:5432/dbname");
ds.setUsername(username);
ds.setPassword(password);
```

> **왜 환경변수로 관리하나요?**
DB 접속 정보(URL, 비밀번호)를 코드에 직접 쓰면 GitHub에 올렸을 때 누구나 볼 수 있습니다.
그래서 `.env` 파일이나 서버 환경변수에 저장하고, 코드에서는 그 값을 읽어오는 방식을 사용합니다.
이것은 실무에서 **절대 지켜야 하는 보안 규칙**입니다.

### Connection Pool 이란?

DB 연결을 맺고 끊는 작업은 비용이 큽니다. 요청이 올 때마다 연결을 새로 만들면 성능이 떨어집니다.
그래서 미리 여러 개의 연결을 만들어두고 돌려쓰는 방식을 **Connection Pool**이라고 합니다.
이 프로젝트에서 사용하는 `HikariCP`가 대표적인 Connection Pool 라이브러리입니다.

```plain text
서버 시작 시: DB 연결 10개를 미리 생성해둠
요청 A 들어옴 → 연결 1개 빌려줌 → 쿼리 실행 → 연결 반납
요청 B 들어옴 → 연결 1개 빌려줌 → 쿼리 실행 → 연결 반납
```

---

## 2. SQL이 실행되기까지의 흐름

예시 요청: `GET /api/events?spaceId=1&month=2026-05`

백엔드가 이 요청을 받으면 내부에서 다음 순서로 처리됩니다.

```plain text
Controller.java
    → Service.java (권한 체크, 비즈니스 로직)
        → EventMapper.java (함수 호출)
            → EventMapper.xml (SQL 실행)
                → PostgreSQL (실제 DB)
```

이 흐름에서 **DB와 직접 연결된 레이어는 Mapper.xml 단 하나**입니다.
나머지 레이어(Controller, Service)는 SQL을 전혀 모르고, Mapper 함수만 호출합니다.
이렇게 설계하면 SQL을 바꿔도 Controller나 Service 코드는 건드릴 필요가 없습니다.

---

## 3. MyBatis가 하는 일 — Mapper 인터페이스 vs XML

이 프로젝트는 **MyBatis**라는 라이브러리를 사용해 Java 코드와 SQL을 연결합니다.

### Mapper 인터페이스 — `EventMapper.java`

**"이런 DB 조회 함수가 있다"고 선언만 하는 파일입니다.**
함수 이름과 파라미터만 정의하고, 실제 SQL은 작성하지 않습니다.

```java
@Mapper
public interface EventMapper {
    List<Event> findBySpaceIdAndMonth(
        @Param("spaceId") Long spaceId,
        @Param("month") String month
    );
}
```

> `@Mapper` 어노테이션이 붙으면 MyBatis가 이 인터페이스를 자동으로 구현체로 만들어줍니다.
개발자가 직접 구현 클래스를 만들 필요가 없습니다.

### Mapper XML — `EventMapper.xml`

**실제 SQL이 작성되는 파일입니다.**
인터페이스의 함수 이름과 XML의 `id`가 **정확히 일치**해야 연결됩니다.

```xml
<select id="findBySpaceIdAndMonth" resultMap="eventResultMap">
    SELECT id, space_id, title, start_date, end_date,
           location, price, color, status, created_by
    FROM events
    WHERE space_id = #{spaceId}
      AND TO_CHAR(start_date, 'YYYY-MM') = #{month}
    ORDER BY start_date ASC
</select>
```

>  `#{spaceId}` 는 Java에서 넘긴 파라미터 값이 들어가는 자리입니다.
실제 실행 시 `WHERE space_id = 1` 처럼 치환됩니다.

> `**#{}**`** vs **`**${}**`** 차이 — 반드시 알아야 할 보안 지식**
> | 구분 | 설명 | 보안 |
> | --- | --- | --- |
> | `#{value}` | PreparedStatement 방식. 값을 안전하게 바인딩 | ✅ SQL Injection 방어됨 |
> | `${value}` | 문자열 그대로 삽입 | ❌ SQL Injection 위험 |
> 
> 특별한 이유가 없는 한 항상 `#{}`를 사용해야 합니다.

---

## 4. resultMap 이란 무엇인가

DB와 Java는 변수명 규칙이 다릅니다.

| 구분 | 규칙 | 예시 |
| --- | --- | --- |
| DB 컬럼명 | snake_case | `space_id`, `start_date`, `created_by` |
| Java 필드명 | camelCase | `spaceId`, `startDate`, `createdBy` |

이 차이 때문에 DB에서 꺼낸 값을 Java 객체에 그냥 넣으면 필드를 못 찾아서 `null`이 됩니다.
`resultMap`은 이 두 이름을 연결해주는 **매핑 규칙 설정**입니다.

```xml
<resultMap id="eventResultMap" type="Event">
    <id     property="id"          column="id"/>
    <result property="spaceId"     column="space_id"/>    <!-- space_id → spaceId -->
    <result property="title"       column="title"/>
    <result property="startDate"   column="start_date"/>  <!-- start_date → startDate -->
    <result property="endDate"     column="end_date"/>
    <result property="location"    column="location"/>
    <result property="price"       column="price"/>
    <result property="color"       column="color"/>
    <result property="status"      column="status"/>
    <result property="createdBy"   column="created_by"/>  <!-- created_by → createdBy -->
</resultMap>
```

> `<id>`는 Primary Key 컬럼에 사용하고, `<result>`는 일반 컬럼에 사용합니다.
PK를 `<id>`로 명시하면 MyBatis가 캐싱 등을 최적화할 때 활용합니다.

### resultMap 없이도 되는 경우

MyBatis 설정에서 `map-underscore-to-camel-case: true`를 켜두면
`snake_case → camelCase` 변환을 자동으로 해줍니다.
하지만 복잡한 매핑(중첩 객체, 1:N 관계 등)은 resultMap을 직접 써야 합니다.

---

## 5. DB에서 데이터를 꺼내 프론트까지 전달되는 전체 과정

데이터가 DB에서 시작해서 프론트 화면에 표시되기까지, 총 **3번의 객체 변환**이 일어납니다.

```plain text
PostgreSQL
  rows (space_id, start_date, ...)   ← DB가 반환하는 원시 데이터
        ↓ [resultMap 변환]
  Event 객체 (spaceId, startDate, ...)  ← Java DB 모델
        ↓ [Service에서 toResponse() 변환]
  EventResponse 객체                 ← 프론트에 보낼 응답 모델
        ↓ [Controller에서 ApiResponse로 감쌈]
  JSON 응답                          ← 프론트가 받는 최종 형태
```

### 왜 Event와 EventResponse를 굳이 분리하나요?

`Event` 객체는 DB 테이블 구조를 그대로 반영합니다.
하지만 프론트에 보낼 때는 DB의 내부 필드를 모두 노출하면 안 되는 경우가 있습니다.

예를 들어 `created_by`는 내부 user ID인데 프론트에 노출할 필요가 없거나,
프론트에서는 `creatorName`처럼 가공된 형태를 원할 수 있습니다.
`EventResponse`를 따로 만들면 **DB 구조가 바뀌어도 API 응답 형태를 유지**할 수 있습니다.

```plain text
Event (DB 모델)          EventResponse (응답 모델)
  id            →           id
  spaceId       →           spaceId
  title         →           title
  startDate     →           startDate
  createdBy     →           (제외하거나 creatorName으로 가공)
```

---

## 6. 자주 하는 실수와 주의할 점

### ① Mapper 함수명과 XML id가 다를 때

```java
// EventMapper.java
List<Event> findBySpaceIdAndMonth(...);  // 함수명

// EventMapper.xml
<select id="findBySpaceAndMonth" ...>    // ❌ id가 다름 → 런타임 오류 발생
```

MyBatis는 함수명과 XML `id`를 연결하므로 **철자 하나까지 정확히 일치**해야 합니다.

---

### ② `#{}` 안의 파라미터명이 `@Param`과 다를 때

```java
// EventMapper.java
List<Event> findBySpaceIdAndMonth(
    @Param("spaceId") Long spaceId,   // @Param("spaceId") 로 선언
    @Param("month") String month
);

// EventMapper.xml
WHERE space_id = #{spaceId}   // ✅ @Param 이름과 일치
  AND ... = #{month}          // ✅
```

```xml
WHERE space_id = #{id}        // ❌ @Param("spaceId") 인데 #{id} 쓰면 null
```

---

### ③ resultMap을 안 쓰고 snake_case 컬럼을 그냥 받으면

```java
// Event.java
private Long spaceId;   // camelCase 필드

// resultMap 없이 조회하면
event.getSpaceId();     // → null (DB에서 space_id로 오는데 매핑 안 됨)
```

`resultMap` 또는 `map-underscore-to-camel-case: true` 설정 중 하나는 반드시 있어야 합니다.

---

### ④ DB에 없는 컬럼을 FE에서 쓰려고 할 때

이 프로젝트에서 실제로 발생한 이슈들입니다.

| 테이블 | 없는 컬럼 | 증상 |
| --- | --- | --- |
| `users` | `plan` | FE에서 plan 필드 항상 null |
| `team_spaces` | `start_date`, `end_date`, `budget` | Travel Map "기간/예산" → `-` 표시 |
| `places` | `status` | "확정" 버튼 동작 불가 |

**DB에 컬럼이 없으면 아무리 Java 코드를 고쳐도 값이 나오지 않습니다.**
FE에서 특정 필드가 계속 null이거나 `-`로 뜬다면 DB 컬럼부터 확인하세요.

---

## ✅ 핵심 요약

| 개념 | 한 줄 요약 |
| --- | --- |
| DataSourceConfig | 백엔드가 어느 DB에 붙을지 설정. 환경변수로 관리 |
| Connection Pool | 연결을 미리 만들어두고 재사용. HikariCP 사용 |
| Mapper 인터페이스 | DB 함수 목록만 선언. SQL 없음 |
| Mapper XML | 실제 SQL 작성. 함수명과 id 반드시 일치 |
| `#{}` | PreparedStatement 방식. SQL Injection 방어 |
| `${}` | 문자열 직접 삽입. 보안 위험 — 사용 지양 |
| resultMap | DB snake_case ↔ Java camelCase 매핑 규칙 |
| Event vs EventResponse | DB 모델과 응답 모델 분리. API 안정성 확보 |

---

## 참고 문서

[[Notion/프로젝트 문서화/프로젝트/NoNAME 프로젝트 DB/Project  Todo - 프로젝트 Todo/RT Database 관점의 BE 아키텍처/RT DB 테이블 구조 (1)]]

[[Notion/프로젝트 문서화/프로젝트/NoNAME 프로젝트 DB/Project  Todo - 프로젝트 Todo/RT Database 관점의 BE 아키텍처/DB Mybatis 동적 SQL]]

[[Notion/프로젝트 문서화/프로젝트/NoNAME 프로젝트 DB/Project  Todo - 프로젝트 Todo/RT Database 관점의 BE 아키텍처/BE @Transactional 이란]]

[[Notion/프로젝트 문서화/프로젝트/NoNAME 프로젝트 DB/Project  Todo - 프로젝트 Todo/RT Database 관점의 BE 아키텍처/DB N+1 문제란]]

[[Notion/프로젝트 문서화/프로젝트/NoNAME 프로젝트 DB/Project  Todo - 프로젝트 Todo/RT Database 관점의 BE 아키텍처/DB 인덱싱의 중요성]]

[[Notion/프로젝트 문서화/프로젝트/NoNAME 프로젝트 DB/Project  Todo - 프로젝트 Todo/RT Database 관점의 BE 아키텍처/BE PreparedStatement란]]
