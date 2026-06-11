---
type: 참고문서
title: PostgreSQL 서버 관리 명령어 가이드
category: 배포
date: 2026-06-11
---

# PostgreSQL 명령어 가이드

PostgreSQL 데이터베이스 서버의 관리, 설정, 접속을 위한 필수 명령어 모음

---

## 🔧 0. 설정 파일 위치 (Ubuntu)

### postgresql.conf (주 설정 파일)
```
dev 환경:   /etc/postgresql/14/dev/postgresql.conf
prod 환경:  /etc/postgresql/14/prod/postgresql.conf
```

**주요 설정:**
```
listen_addresses = '*'    # 모든 외부 접속 허용 (프로덕션에서는 제한)
port = 5110               # dev 포트
port = 5220               # prod 포트
```

### pg_hba.conf (접속 권한 파일)
```
dev 환경:   /etc/postgresql/14/dev/pg_hba.conf
prod 환경:  /etc/postgresql/14/prod/pg_hba.conf
```

**주요 설정:**
```
host all all 0.0.0.0/0 md5   # 모든 외부 접속 허용
```

---

## 🎯 1. PostgreSQL 클러스터 관리

### 클러스터 목록 확인
```bash
pg_lsclusters
```

출력 예시:
```
Ver Cluster Port Status Owner    Data directory
14  dev     5110 online postgres /var/lib/postgresql/14/dev
14  prod    5220 online postgres /var/lib/postgresql/14/prod
```

### dev 클러스터 관리
```bash
# 시작
sudo pg_ctlcluster 14 dev start

# 중지
sudo pg_ctlcluster 14 dev stop

# 재시작 (완전 재시작)
sudo pg_ctlcluster 14 dev restart

# 설정만 재적용 (다운타임 없음)
sudo pg_ctlcluster 14 dev reload
```

### prod 클러스터 관리
```bash
# 시작
sudo pg_ctlcluster 14 prod start

# 중지
sudo pg_ctlcluster 14 prod stop

# 재시작
sudo pg_ctlcluster 14 prod restart

# 설정만 재적용
sudo pg_ctlcluster 14 prod reload
```

---

## 🔌 2. PostgreSQL 전체 서비스 관리

```bash
# 전체 PostgreSQL 서비스 시작
sudo systemctl start postgresql

# 전체 PostgreSQL 서비스 중지
sudo systemctl stop postgresql

# 전체 서비스 재시작
sudo systemctl restart postgresql

# 상태 확인
sudo systemctl status postgresql
```

---

## 📍 3. 데이터베이스 접속

### dev 환경 접속
```bash
psql -h localhost -p 5110 -U erpUser -d groupware_dev
```

**파라미터:**
- `-h localhost` : 접속 호스트
- `-p 5110` : 포트
- `-U erpUser` : 사용자명
- `-d groupware_dev` : 데이터베이스명

### prod 환경 접속
```bash
psql -h localhost -p 5220 -U erpUser -d groupware_prod
```

### 관리자로 접속
```bash
sudo -u postgres psql
```

---

## 💬 4. psql 내부 명령어

### 데이터베이스 정보 조회

```bash
# 데이터베이스 목록
\l
```

출력:
```
                                  List of databases
         Name      | Owner    | Encoding |  Collate   |    Ctype
groupware_dev     | postgres | UTF8     | ko_KR.UTF-8| ko_KR.UTF-8
groupware_prod    | postgres | UTF8     | ko_KR.UTF-8| ko_KR.UTF-8
```

### 사용자 및 권한

```bash
# 사용자(role) 목록
\du
```

출력:
```
           List of roles
 Role name | Attributes | Member of
-----------+------------+-----------
 erpUser   |            | {}
 postgres  | Superuser  | {}
```

### 테이블 정보

```bash
# 현재 DB의 테이블 목록
\dt
```

출력:
```
              List of relations
 Schema |      Name       | Type  | Owner
--------+-----------------+-------+----------
 public | users           | table | erpUser
 public | departments     | table | erpUser
```

### 테이블 상세 구조

```bash
# 테이블의 칼럼 구조 보기
\d 테이블명
```

예시:
```bash
\d users
```

출력:
```
             Table "public.users"
 Column |            Type | Collation | Nullable
--------+-----------------+-----------+----------
 id     | integer         |           | not null
 name   | character varying|           |
 email  | character varying|           |
```

### 현재 접속 정보

```bash
# 현재 접속 정보 확인
\conninfo
```

출력:
```
You are connected to database "groupware_dev" as user "erpUser" via socket
```

### 종료

```bash
# psql 종료
\q
```

---

## 🔑 주요 SQL 명령어 (psql 내부)

```sql
-- 데이터베이스 생성
CREATE DATABASE database_name;

-- 사용자 생성
CREATE USER username WITH PASSWORD 'password';

-- 권한 부여
GRANT ALL PRIVILEGES ON DATABASE database_name TO username;

-- 테이블 조회
SELECT * FROM table_name LIMIT 10;

-- 쿼리 실행
\i /path/to/script.sql
```

---

## 🔄 일반적인 워크플로우

### 1. 상태 확인
```bash
pg_lsclusters        # 클러스터 상태 확인
systemctl status postgresql  # 서비스 상태 확인
```

### 2. DB 접속 및 작업
```bash
psql -h localhost -p 5110 -U erpUser -d groupware_dev
```

### 3. 설정 변경 후 재적용
```bash
# 설정 파일 수정
nano /etc/postgresql/14/dev/postgresql.conf

# 재시작 (또는 reload)
sudo pg_ctlcluster 14 dev reload
```

### 4. 연결 종료
```bash
\q  # psql 종료
```

---

## ⚠️ 문제 해결

### 문제: "Connection refused"
```
psql: error: could not connect to server: Connection refused
```

**해결:**
```bash
# 클러스터가 실행 중인지 확인
pg_lsclusters

# 실행 중이 아니면 시작
sudo pg_ctlcluster 14 dev start

# 포트 확인
sudo netstat -tulpn | grep postgres
```

### 문제: "role does not exist"
```
psql: error: FATAL: role "erpUser" does not exist
```

**해결:**
```bash
# 관리자로 접속하여 사용자 생성
sudo -u postgres psql

# 사용자 생성
CREATE USER erpUser WITH PASSWORD 'password';
```

### 문제: "cannot connect to X.X.X.X"
```
psql: could not connect to server: No such file or directory
```

**해결:**
```bash
# 설정 파일에서 listen_addresses 확인
grep listen_addresses /etc/postgresql/14/dev/postgresql.conf

# 필요시 '*'로 변경 (모든 외부 접속 허용)
listen_addresses = '*'

# 설정 재적용
sudo pg_ctlcluster 14 dev reload
```

---

## 📌 자주 사용하는 명령어 (Top 5)

```bash
# 1. 클러스터 상태 확인
pg_lsclusters

# 2. dev DB 접속
psql -h localhost -p 5110 -U erpUser -d groupware_dev

# 3. 설정 재적용
sudo pg_ctlcluster 14 dev reload

# 4. 테이블 목록 (내부)
\dt

# 5. 종료
\q
```

---

**작성일:** 2026-06-11  
**카테고리:** 배포/데이터베이스 관리  
**환경:** Ubuntu + PostgreSQL 14

