---

---

---

# Index — DB 조회 성능을 높이는 색인 구조

> 두꺼운 책에서 원하는 내용을 찾을 때, 처음부터 한 장씩 넘기지 않고 **목차(인덱스)**를 먼저 봅니다.
DB Index도 마찬가지입니다. 수백만 rows에서 원하는 데이터를 빠르게 찾도록 도와주는 **색인**입니다.

---

## 1. Index란 무엇인가

Index는 특정 컬럼의 값과 그 값이 저장된 위치(row)를 미리 정렬해서 따로 저장해둔 구조입니다. Index는 DB 내부에서 **B-Tree(균형 트리)** 자료구조로 구현되며, 정렬된 트리에서 값을 찾으므로 탐색 시간이 `O(log N)`으로 매우 빠릅니다.

Index 없이 탐색할 때:

```plain text
row 1: space_id = 1 → 아님, 다음
row 2: space_id = 3 → 아님, 다음
row 3: space_id = 5 → 발견!
row 4: space_id = 2 → 아님, 다음
...row 10만개까지 전부 확인  ← Full Table Scan
```

Index 있을 때:

```plain text
space_id 인덱스: [1→row1, 2→row4, 3→row2, 5→row3, ...]  ← 정렬된 상태
→ 5를 이진 탐색으로 즉시 찾음 → row3으로 바로 이동
```

---

## 2. Index 없을 때 vs 있을 때 — 탐색 방식 비교

| 구분 | 방식 | 10만 rows에서 탐색 |
| --- | --- | --- |
| Index 없음 | Full Table Scan — 처음부터 끝까지 전부 확인 | 최대 10만 번 비교 |
| Index 있음 | B-Tree 탐색 — 절반씩 줄여가며 탐색 | 약 17번 비교 (log₂ 100,000 ≈ 17) |

데이터가 많을수록 Index의 효과는 기하급수적으로 커집니다.

---

## 3. Index를 생성하는 방법

기본 Index 생성:

```sql
-- 단일 컬럼 Index
CREATE INDEX idx_events_space_id ON events(space_id);

-- 복합 Index (여러 컬럼 조합)
CREATE INDEX idx_events_space_month ON events(space_id, start_date);

-- Unique Index (중복 값 허용 안 함)
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

Primary Key와 Unique 제약조건은 자동으로 Index가 생성됩니다:

```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,  -- ← 자동으로 PK Index 생성
    ...
);

ALTER TABLE users ADD CONSTRAINT uq_username UNIQUE(username);  -- 자동 Index 생성
```

Index 삭제:

```sql
DROP INDEX idx_events_space_id;
```

현재 Index 목록 확인 (PostgreSQL):

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'events';
```

---

## 4. 어떤 컬럼에 Index를 걸어야 하는가

Index가 효과적인 컬럼:

```plain text
- WHERE 절에 자주 등장하는 컬럼
   SELECT * FROM events WHERE space_id = 1
   → space_id에 Index

- JOIN 조건에 사용되는 FK 컬럼
   JOIN team_space_members tsm ON ts.id = tsm.space_id
   → tsm.space_id에 Index

- ORDER BY에 자주 사용되는 컬럼
   ORDER BY start_date ASC
   → start_date에 Index

- 카디널리티(고유값 수)가 높은 컬럼
   email: 모든 row가 다름 → Index 효과 큼
   is_read: TRUE/FALSE 2가지뿐 → Index 효과 작음
```

Index가 효과 없거나 역효과인 컬럼:

```plain text
- 카디널리티가 낮은 컬럼 — boolean, 성별, 상태값(2~5가지) 등
- 자주 UPDATE되는 컬럼 — Index도 함께 갱신되므로 쓰기 성능 저하
- 데이터가 매우 적은 테이블 — 100개 이하라면 Full Scan이 오히려 빠름
```

---

## 5. Index의 종류

### 단일 Index vs 복합 Index

```sql
-- 단일 Index
CREATE INDEX idx_space ON events(space_id);

-- 복합 Index
CREATE INDEX idx_space_date ON events(space_id, start_date);
```

복합 Index는 **왼쪽 컬럼부터** 순서대로 사용됩니다.

```sql
WHERE space_id = 1                                   -- 활용됨
WHERE space_id = 1 AND start_date > '2026-01-01'     -- 활용됨
WHERE start_date > '2026-01-01'                      -- 활용 안 됨
```

### Partial Index — 조건부 Index

자주 조회하는 특정 조건의 데이터만 Index를 만들어 크기를 줄일 수 있습니다.

```sql
-- status = 'pending'인 row만 Index 생성
CREATE INDEX idx_pending_events ON events(space_id)
WHERE status = 'pending';
```

---

## 6. Index의 단점 — 무조건 많이 걸면 안 되는 이유

Index는 **읽기(SELECT) 성능을 높이지만, 쓰기(INSERT/UPDATE/DELETE) 성능을 낮춥니다.**

```plain text
INSERT row 1개 발생 시:
  - events 테이블에 row 추가
  - idx_events_space_id 인덱스 갱신
  - idx_events_start_date 인덱스 갱신
  - idx_events_status 인덱스 갱신
  → Index가 많을수록 쓰기마다 추가 작업 발생
```

| Index 수 | 읽기 성능 | 쓰기 성능 | 디스크 사용 |
| --- | --- | --- | --- |
| 0개 | 느림 | 빠름 | 적음 |
| 적당히 | 빠름 | 적당 | 적당 |
| 과도하게 | 빠름 | 느림 | 많음 |

> 조회가 많고 쓰기가 적은 테이블 → Index 적극 활용
쓰기가 매우 많은 테이블(로그, 이벤트 수집) → Index 최소화

---

## 7. 이 프로젝트에서 Index를 걸어야 할 곳

```sql
-- events 테이블
CREATE INDEX idx_events_space_id   ON events(space_id);
CREATE INDEX idx_events_start_date ON events(start_date);
CREATE INDEX idx_events_space_date ON events(space_id, start_date);  -- 복합

-- places 테이블
CREATE INDEX idx_places_space_id ON places(space_id);
CREATE INDEX idx_places_lat_lng  ON places(latitude, longitude);

-- team_space_members 테이블
CREATE INDEX idx_tsm_space_id ON team_space_members(space_id);
CREATE INDEX idx_tsm_user_id  ON team_space_members(user_id);

-- notifications 테이블
CREATE INDEX idx_noti_user_id ON notifications(user_id);
CREATE INDEX idx_noti_unread  ON notifications(user_id) WHERE is_read = FALSE;  -- Partial
```

---

## 8. EXPLAIN으로 Index 활용 여부 확인하기

```sql
EXPLAIN SELECT * FROM events WHERE space_id = 1;
```

결과 해석:

```plain text
Seq Scan on events  (cost=0.00..450.00 rows=1000)
  Filter: (space_id = 1)
↑ Full Table Scan — Index 미사용. 성능 나쁨

Index Scan using idx_events_space_id on events  (cost=0.43..8.45 rows=10)
  Index Cond: (space_id = 1)
↑ Index 사용됨. 성능 좋음
```

| 키워드 | 의미 |
| --- | --- |
| `Seq Scan` | Full Table Scan — Index 없거나 미사용 |
| `Index Scan` | Index를 통해 접근 — 효율적 |
| `Index Only Scan` | Index만으로 결과 반환 — 가장 효율적 |
| `cost` | 예상 비용. 숫자가 낮을수록 빠름 |

---

## 9. 자주 하는 실수

### ① 컬럼에 함수를 씌우면 Index를 못 씀

```sql
-- ❌ TO_CHAR()로 감싸면 Index 미사용, Seq Scan 발생
WHERE TO_CHAR(start_date, 'YYYY-MM') = '2026-05'

-- ✅ 범위 조건으로 바꾸면 Index 사용 가능
WHERE start_date >= '2026-05-01'
  AND start_date < '2026-06-01'
```

### ② LIKE 검색에서 앞에 와일드카드 사용

```sql
-- ❌ 앞에 % 붙이면 Index 못 씀
WHERE title LIKE '%여행%'

-- ✅ 뒤에만 % 붙이면 Index 사용 가능
WHERE title LIKE '서울%'
```

### ③ 카디널리티 낮은 컬럼에 단독 Index

```sql
-- ❌ TRUE/FALSE 2가지뿐 → Index 효과 거의 없음
CREATE INDEX idx_noti_is_read ON notifications(is_read);

-- ✅ Partial Index로 대체
CREATE INDEX idx_noti_unread ON notifications(user_id) WHERE is_read = FALSE;
```

---