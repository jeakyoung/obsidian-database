---

---

---

# N+1 문제 — 잘못된 쿼리 설계로 DB 요청이 폭발적으로 늘어나는 현상

> N+1 문제는 신입 개발자가 가장 많이 마주치는 성능 문제 중 하나입니다.
코드가 멀쩡해 보이는데 DB 요청이 수백 개가 날아가는 상황,
원인과 해결법을 정확히 이해해야 합니다.

---

## 1. N+1 문제란 무엇인가

**N+1 문제**는 목록 1번 조회(1) 후, 각 항목마다 추가 쿼리(N)가 실행되는 현상입니다.

```plain text
스페이스 목록 조회 → 쿼리 1번 실행
  스페이스 1의 멤버 조회 → 쿼리 1번
  스페이스 2의 멤버 조회 → 쿼리 1번
  스페이스 3의 멤버 조회 → 쿼리 1번
  ...
  스페이스 100의 멤버 조회 → 쿼리 1번

총 쿼리 실행 횟수: 1 + 100 = 101번
```

스페이스가 100개면 쿼리가 101번 실행됩니다. 1,000개면 1,001번입니다. 데이터가 늘수록 **선형으로 쿼리가 증가**합니다.

---

## 2. 언제 발생하는가 — 구체적인 시나리오

상황: 팀 스페이스 목록 + 각 스페이스의 멤버 수를 함께 보여줘야 함

 N+1이 발생하는 코드:

```java
public List<SpaceResponse> findAllSpaces() {
    List<TeamSpace> spaces = teamSpaceMapper.findAll();  // 쿼리 1번

    return spaces.stream().map(space -> {
        // 각 스페이스마다 멤버 조회 → N번 추가 실행!
        int memberCount = teamSpaceMemberMapper.countBySpaceId(space.getId());
        return new SpaceResponse(space, memberCount);
    }).toList();
}
```

실제 실행되는 SQL (스페이스가 5개라면):

```sql
SELECT * FROM team_spaces;                                    -- 1번
SELECT COUNT(*) FROM team_space_members WHERE space_id = 1;  -- 2번
SELECT COUNT(*) FROM team_space_members WHERE space_id = 2;  -- 3번
SELECT COUNT(*) FROM team_space_members WHERE space_id = 3;  -- 4번
SELECT COUNT(*) FROM team_space_members WHERE space_id = 4;  -- 5번
SELECT COUNT(*) FROM team_space_members WHERE space_id = 5;  -- 6번
-- 총 6번 실행 (N=5이면 1+5=6번)
```

코드가 직관적이고 틀리지 않아 보이기 때문에 발견하기 어렵습니다.

---

## 3. 왜 문제인가 — 성능 영향

DB 쿼리 한 번 실행에는 다음 비용이 듭니다.

```plain text
네트워크 왕복 시간 (백엔드 서버 ↔ DB 서버)
쿼리 파싱 및 실행 계획 수립
실제 데이터 탐색
결과 전송
```

쿼리 1번당 평균 5ms라고 하면:

| 데이터 수 | 쿼리 횟수 | 총 소요 시간 |
| --- | --- | --- |
| 10개 | 11번 | 55ms |
| 100개 | 101번 | 505ms |
| 1,000개 | 1,001번 | 5,005ms (5초!) |
| 10,000개 | 10,001번 | 50,005ms (50초!) |

데이터가 적을 때는 느낌이 없지만, **실서비스에서는 치명적인 성능 문제**가 됩니다.

---

## 4. 해결법 ① JOIN으로 한 번에 조회

가장 근본적인 해결책은 **JOIN으로 필요한 데이터를 한 번에 가져오는 것**입니다.

```xml
<select id="findAllWithMemberCount" resultMap="spaceWithCountResultMap">
    SELECT
        ts.id,
        ts.name,
        ts.emoji,
        ts.bg_color,
        COUNT(tsm.id) AS member_count
    FROM team_spaces ts
    LEFT JOIN team_space_members tsm ON ts.id = tsm.space_id
    GROUP BY ts.id, ts.name, ts.emoji, ts.bg_color
    ORDER BY ts.created_at DESC
</select>

<resultMap id="spaceWithCountResultMap" type="SpaceWithCountDto">
    <id     property="id"          column="id"/>
    <result property="name"        column="name"/>
    <result property="emoji"       column="emoji"/>
    <result property="bgColor"     column="bg_color"/>
    <result property="memberCount" column="member_count"/>
</resultMap>
```

실행 SQL: 단 1번 → JOIN으로 스페이스 + 멤버 수를 한 번에 조회

---

## 5. 해결법 ② MyBatis resultMap 중첩 매핑

스페이스 목록과 각 스페이스의 멤버 **목록(List)** 을 함께 가져와야 할 때 사용합니다. MyBatis의 `<collection>` 태그로 1:N 관계를 한 번에 매핑할 수 있습니다.

```xml
<select id="findAllWithMembers" resultMap="spaceWithMembersResultMap">
    SELECT
        ts.id          AS space_id,
        ts.name        AS space_name,
        ts.emoji,
        u.id           AS user_id,
        u.username,
        tsm.role
    FROM team_spaces ts
    LEFT JOIN team_space_members tsm ON ts.id = tsm.space_id
    LEFT JOIN users u ON tsm.user_id = u.id
    ORDER BY ts.id
</select>

<resultMap id="spaceWithMembersResultMap" type="TeamSpaceDto">
    <id     property="id"    column="space_id"/>
    <result property="name"  column="space_name"/>
    <result property="emoji" column="emoji"/>
    <collection property="members" ofType="MemberDto">
        <id     property="userId"   column="user_id"/>
        <result property="username" column="username"/>
        <result property="role"     column="role"/>
    </collection>
</resultMap>
```

MyBatis가 JOIN 결과에서 `space_id`가 같은 rows를 자동으로 묶어 `TeamSpaceDto.members` 리스트에 채워줍니다. 실행 SQL은 단 1번이고, MyBatis가 자동으로 5개의 SpaceDto로 그루핑해줍니다.

---

## 6. 해결법 ③ 별도 쿼리 + IN절 일괄 조회

JOIN이 복잡하거나, 이미 스페이스 목록을 가져온 상황에서 멤버 정보를 추가로 가져와야 할 때 사용합니다.

```java
public List<SpaceResponse> findAllSpaces() {
    List<TeamSpace> spaces = teamSpaceMapper.findAll();       // 쿼리 1번

    List<Long> spaceIds = spaces.stream()
        .map(TeamSpace::getId)
        .toList();

    // IN절으로 모든 멤버를 한 번에 조회
    List<TeamSpaceMember> allMembers =
        teamSpaceMemberMapper.findBySpaceIds(spaceIds);       // 쿼리 1번

    // Java에서 spaceId 기준으로 그룹핑
    Map<Long, List<TeamSpaceMember>> memberMap = allMembers.stream()
        .collect(Collectors.groupingBy(TeamSpaceMember::getSpaceId));

    return spaces.stream().map(space ->
        new SpaceResponse(space, memberMap.getOrDefault(space.getId(), List.of()))
    ).toList();
}
```

```xml
<select id="findBySpaceIds" resultMap="memberResultMap">
    SELECT id, space_id, user_id, role
    FROM team_space_members
    WHERE space_id IN
    <foreach collection="spaceIds" item="id" open="(" separator="," close=")">
        #{id}
    </foreach>
</select>
```

실행 SQL: 2번 (스페이스 조회 1번 + 멤버 전체 조회 1번) → 스페이스 수에 관계없이 항상 2번만 실행됩니다.

---

## 7. 실무에서 N+1 탐지하는 방법

`application.yml`에 다음 설정을 추가하면 실행되는 SQL을 콘솔에서 볼 수 있습니다.

```yaml
logging:
  level:
    your.package.mapper: DEBUG
```

로그에서 아래처럼 비슷한 쿼리가 반복적으로 찍히면 N+1을 의심하세요.

```plain text
DEBUG - SELECT * FROM team_spaces
DEBUG - SELECT COUNT(*) FROM team_space_members WHERE space_id = 1
DEBUG - SELECT COUNT(*) FROM team_space_members WHERE space_id = 2
DEBUG - SELECT COUNT(*) FROM team_space_members WHERE space_id = 3
```

---

## 8. 자주 하는 실수

### ① 데이터가 적을 때 발견 못 하는 경우

로컬 개발 환경에서는 데이터가 5~10개라서 느린 줄 모릅니다. 실서비스에서 데이터가 쌓이면 갑자기 API가 느려집니다. **항상 "데이터가 1,000개면 쿼리가 몇 번 실행될까?"를 생각하는 습관**이 중요합니다.

### ② 반복문 안에서 DB 호출

```java
// ❌ N+1 패턴 — 반복문 안에서 DB 호출
for (TeamSpace space : spaces) {
    List<Event> events = eventMapper.findBySpaceId(space.getId());  // N번 실행
}

// ✅ IN절로 한 번에 가져온 뒤 Java에서 그루핑
List<Event> allEvents = eventMapper.findBySpaceIds(spaceIds);  // 1번 실행
Map<Long, List<Event>> eventMap = allEvents.stream()
    .collect(Collectors.groupingBy(Event::getSpaceId));
```

---
