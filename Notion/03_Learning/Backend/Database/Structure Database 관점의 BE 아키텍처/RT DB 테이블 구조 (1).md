---

---

# 📦 DB 테이블 구조

---

## 👤 users `V1`

| 컬럼 | 타입 | 비고 |   |
| --- | --- | --- | --- |
| id | BIGSERIAL | PK |   |
| username | VARCHAR(50) | UNIQUE |   |
| password | VARCHAR(255) |   |   |
| email | VARCHAR(100) | UNIQUE |   |
| role | VARCHAR(20) | DEFAULT 'USER' |   |
| created_at / updated_at | TIMESTAMP |   |   |

> ⚠️ `plan` 컬럼 없음 — FE에서 `plan` 필드를 사용 중이나 DB에 존재하지 않음

---

## 🏠 team_spaces `V2`

| 컬럼 | 타입 | 비고 |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| name | VARCHAR(100) |   |
| emoji | VARCHAR(10) |   |
| bg_color | VARCHAR(7) |   |
| owner_id | BIGINT | FK → users |
| created_at / updated_at | TIMESTAMP |   |

> ⚠️ `start_date`, `end_date`, `budget` 컬럼 없음 — Travel Map 화면 "기간/예산" 항목이 `-`로 표시되는 원인

---

## 👥 team_space_members `V2`

| 컬럼 | 타입 | 비고 |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| space_id | BIGINT | FK → team_spaces |
| user_id | BIGINT | FK → users |
| role | VARCHAR(20) | DEFAULT 'member' |
| joined_at | TIMESTAMP |   |

---

## 📅 events `V3`

| 컬럼 | 타입 | 비고 |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| space_id | BIGINT | FK → team_spaces |
| title | VARCHAR(255) |   |
| description | TEXT |   |
| start_date / end_date | DATE |   |
| location | VARCHAR(255) |   |
| price | VARCHAR(100) |   |
| color | VARCHAR(7) | DEFAULT '#4A6CF7' |
| status | VARCHAR(20) | DEFAULT 'pending' |
| created_by | BIGINT | FK → users |

---

## 📍 places `V4`

| 컬럼 | 타입 | 비고 |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| space_id | BIGINT | FK → team_spaces |
| name | VARCHAR(255) |   |
| category | VARCHAR(50) |   |
| address / region / country | TEXT / VARCHAR |   |
| latitude / longitude | DECIMAL |   |
| price_desc / price_min / price_max / currency |   |   |
| hours | TEXT |   |
| thumbnail_url / source_url / source_platform | TEXT / VARCHAR |   |
| tags / menu | TEXT[] | 배열 |
| confidence | VARCHAR(10) |   |
| created_by | BIGINT | FK → users |

> ⚠️ `status` 컬럼 없음 — Travel Map "확정" 버튼 동작 불가

---

## 🔔 notifications `V5`

| 컬럼 | 타입 | 비고 |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| user_id | BIGINT | FK → users |
| message | TEXT |   |
| type | VARCHAR(50) |   |
| related_space_id | BIGINT | FK → team_spaces |
| is_read | BOOLEAN | DEFAULT FALSE |
| created_at / read_at | TIMESTAMP |   |

---

## 📄 documents `V1`

| 컬럼 | 타입 | 비고 |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| title | VARCHAR(255) |   |
| content | TEXT |   |
| embedding | vector(1536) | pgvector |

> ⚠️ 장소 검색용 벡터 저장 테이블 — 현재 `places` 테이블과 연결 없음
