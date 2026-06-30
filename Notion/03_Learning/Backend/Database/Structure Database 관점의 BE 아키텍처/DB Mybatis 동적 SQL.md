---

---

---

# MyBatis 동적 SQL — `<if>`, `<foreach>` 태그로 조건부 쿼리 작성하기

> 실무에서는 검색 조건이 있을 수도 있고 없을 수도 있습니다.
동적 SQL은 이런 상황에서 **조건에 따라 SQL을 유연하게 조합**하는 기술입니다.

---

## 1. 동적 SQL이 왜 필요한가

예를 들어 일정 목록 조회 API가 있다고 합시다. 프론트에서는 다음과 같이 다양한 조합으로 요청을 보낼 수 있습니다.

```plain text
GET /api/events?spaceId=1
GET /api/events?spaceId=1&month=2026-05
GET /api/events?spaceId=1&status=confirmed
GET /api/events?spaceId=1&month=2026-05&status=confirmed
```

조건마다 SQL을 따로 만들면 중복 코드가 폭발합니다. 동적 SQL을 쓰면 **하나의 SQL로 모든 조합을 처리**할 수 있습니다.

---

## 2. `<if>` — 조건이 있을 때만 SQL 추가하기

`<if test="...">` 안의 조건이 참일 때만 해당 SQL 조각이 붙습니다.

```xml
<select id="findEvents" resultMap="eventResultMap">
    SELECT id, space_id, title, start_date, status
    FROM events
    WHERE space_id = #{spaceId}
    <if test="month != null and month != ''">
        AND TO_CHAR(start_date, 'YYYY-MM') = #{month}
    </if>
    <if test="status != null and status != ''">
        AND status = #{status}
    </if>
    ORDER BY start_date ASC
</select>
```

> `month`가 null이면 해당 조건은 SQL에 포함되지 않습니다. Java에서 넘기지 않은 파라미터는 자동으로 null이 됩니다.

Mapper 인터페이스:

```java
List<Event> findEvents(
    @Param("spaceId") Long spaceId,
    @Param("month")   String month,
    @Param("status")  String status
);
```

---

## 3. `<where>` — AND 중복/누락 문제 자동 해결

`<if>`만 쓰면 모든 조건이 null일 때 `WHERE` 뒤에 아무것도 없어서 문법 오류가 납니다. 또 첫 번째 조건에 `AND`를 붙이면 `WHERE AND ...` 처럼 이상한 SQL이 됩니다. `<where>` 태그가 이 두 가지를 자동으로 해결합니다.

❌ 문제가 생기는 방식:

```xml
<select id="findEvents" resultMap="eventResultMap">
    SELECT * FROM events
    WHERE
    <if test="month != null">
        AND TO_CHAR(start_date, 'YYYY-MM') = #{month}
    </if>
</select>
```

`<where>` 태그로 해결:

```xml
<select id="findEvents" resultMap="eventResultMap">
    SELECT * FROM events
    <where>
        <if test="spaceId != null">
            AND space_id = #{spaceId}
        </if>
        <if test="month != null">
            AND TO_CHAR(start_date, 'YYYY-MM') = #{month}
        </if>
        <if test="status != null">
            AND status = #{status}
        </if>
    </where>
    ORDER BY start_date ASC
</select>
```

> `<where>`는 내부에 내용이 있을 때만 `WHERE`를 붙이고, 첫 번째 조건의 `AND` / `OR`는 자동으로 제거해줍니다.

---

## 4. `<foreach>` — IN 절에 여러 값 넣기

여러 개의 ID를 한 번에 조회할 때 `IN (1, 2, 3)` 형태의 SQL이 필요합니다. Java 리스트를 `<foreach>`로 SQL IN 절에 변환할 수 있습니다.

Mapper 인터페이스:

```java
List<Event> findByIds(@Param("ids") List<Long> ids);
```

Mapper XML:

```xml
<select id="findByIds" resultMap="eventResultMap">
    SELECT id, title, start_date
    FROM events
    WHERE id IN
    <foreach collection="ids" item="id" open="(" separator="," close=")">
        #{id}
    </foreach>
</select>
```

| 속성 | 설명 | 예시 |
| --- | --- | --- |
| `collection` | 반복할 Java 파라미터 이름 | `"ids"` |
| `item` | 반복 변수 이름 | `"id"` |
| `open` | 시작 문자 | `"("` |
| `separator` | 구분자 | `","` |
| `close` | 종료 문자 | `")"` |

실행 결과 SQL:

```sql
SELECT id, title, start_date FROM events WHERE id IN (1, 2, 3)
```

---

## 5. `<choose>` — if-else처럼 분기 처리

여러 조건 중 **하나만** 적용하고 싶을 때 사용합니다. Java의 `if - else if - else`와 동일한 구조입니다.

```xml
<select id="findEventsSorted" resultMap="eventResultMap">
    SELECT * FROM events
    WHERE space_id = #{spaceId}
    ORDER BY
    <choose>
        <when test="sort == 'date'">
            start_date ASC
        </when>
        <when test="sort == 'title'">
            title ASC
        </when>
        <otherwise>
            created_at DESC
        </otherwise>
    </choose>
</select>
```

---

## 6. `<set>` — UPDATE할 때 동적으로 컬럼 지정

UPDATE 시 변경된 컬럼만 골라서 업데이트할 때 사용합니다. `<where>`와 마찬가지로 마지막 콤마(`,`)를 자동으로 제거해줍니다.

```xml
<update id="updateEvent">
    UPDATE events
    <set>
        <if test="title != null">
            title = #{title},
        </if>
        <if test="status != null">
            status = #{status},
        </if>
        <if test="location != null">
            location = #{location},
        </if>
        updated_at = NOW()
    </set>
    WHERE id = #{id}
</update>
```

> `<set>`이 없으면 마지막 `,` 때문에 문법 오류가 납니다. `<set>`이 자동으로 불필요한 쉼표를 처리해줍니다.

---

## 7. 실무 예시 — 복합 검색 쿼리

실제로 검색 기능을 만들 때 위 태그들을 조합해서 사용합니다.

```xml
<select id="searchEvents" resultMap="eventResultMap">
    SELECT e.id, e.title, e.start_date, e.status, e.location
    FROM events e
    <where>
        <if test="spaceId != null">
            AND e.space_id = #{spaceId}
        </if>
        <if test="month != null and month != ''">
            AND TO_CHAR(e.start_date, 'YYYY-MM') = #{month}
        </if>
        <if test="status != null and status != ''">
            AND e.status = #{status}
        </if>
        <if test="keyword != null and keyword != ''">
            AND (e.title LIKE '%' || #{keyword} || '%'
              OR e.location LIKE '%' || #{keyword} || '%')
        </if>
        <if test="ids != null and ids.size() > 0">
            AND e.id IN
            <foreach collection="ids" item="id" open="(" separator="," close=")">
                #{id}
            </foreach>
        </if>
    </where>
    ORDER BY e.start_date ASC
</select>
```

---

## 8. 자주 하는 실수

### ① 문자열 비교 시 null 체크 누락

```xml
<!-- ❌ status가 null이면 NullPointerException 발생 -->
<if test="status == 'confirmed'">

<!-- ✅ null 체크를 먼저 -->
<if test="status != null and status == 'confirmed'">
```

### ② `<foreach>` collection 이름이 @Param과 다를 때

```java
List<Event> findByIds(@Param("ids") List<Long> ids);
```

```xml
<!-- ❌ collection="idList" 로 다르게 쓰면 오류 -->
<foreach collection="idList" ...>

<!-- ✅ @Param 이름과 정확히 일치 -->
<foreach collection="ids" ...>
```

---

## 핵심 요약

| 태그 | 역할 | 사용 상황 |
| --- | --- | --- |
| `<if>` | 조건부 SQL 추가 | 파라미터가 있을 때만 조건 추가 |
| `<where>` | WHERE 자동 관리 | 여러 `<if>` 조합 시 AND/WHERE 문제 방지 |
| `<foreach>` | 컬렉션 → IN 절 변환 | 여러 ID를 한 번에 조회 |
| `<choose>` | if-else 분기 | 정렬 기준, 단일 조건 선택 |
| `<set>` | UPDATE 컬럼 동적 지정 | 변경된 필드만 UPDATE |

---