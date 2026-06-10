---
base: "[[Work Flow.base]]"
할당: []
상태: 시작되지 않음
프로젝트: []
---
# **PostgreSQL 명령어 정리**

Config 파일 정리

### **config 파일 설정 (postgresql.conf)**

| **기능** | **명령어** | **설명** |
| --- | --- | --- |
| dev config 파일 | /etc/postgresql/14/dev/postgresql.co | 5110 등 설정 |
| prod config 파일 /etc/postgresql/14/prod/postgresql.conf onf | 5220 등 설정 |   |
| 각 config파일 address추가 | listen_addresses = | 모든 외부 접속 허용 |

## **접속 권한 파일 (pg_hba.conf)**

| **기능** | **명령어** | **설명** |
| --- | --- | --- |
| dev config 파일 | /etc/postgresql/14/dev/pg_hba.conf | host 설정 |
| prod config 파일 | /etc/postgresql/14/prod/pg_hba.conf | host 설정 |
| 각 pg_hba host추가 | host all all 0.0.0.0/0 md5 | 모든 외부 접속 허용 |

## **1. PostgreSQL 클러스터 관리 명령어 (Ubuntu)**

| **기능** | **명령어** | **설명** |
| --- | --- | --- |
| 클러스터 목록 확인 | `pg_lsclusters` | PostgreSQL 클러스터 상태 확인 |
| dev 시작 | `sudo pg_ctlcluster 14 dev start` | dev 클러스터 실행 |
| prod 시작 | `sudo pg_ctlcluster 14 prod start` | prod 클러스터 실행 |
| dev 중지 | `sudo pg_ctlcluster 14 dev stop` | dev 클러스터 정지 |
| prod 중지 | `sudo pg_ctlcluster 14 prod stop` | prod 클러스터 정지 |
| dev 재시작 | `sudo pg_ctlcluster 14 dev restart` | dev 클러스터 재시작 |
| prod 재시작 | `sudo pg_ctlcluster 14 prod restart` | prod 클러스터 재시작 |
| dev 설정 reload | `sudo pg_ctlcluster 14 dev reload` | dev 설정만 재적용 |
| prod 설정 reload | `sudo pg_ctlcluster 14 prod reload` | prod 설정만 재적용 |

---

## **2. PostgreSQL 전체 서비스 관리**

| **기능** | **명령어** | **설명** |
| --- | --- | --- |
| 서비스 시작 | `sudo systemctl start postgresql` | PostgreSQL 서버 시작 |
| 서비스 중지 | `sudo systemctl stop postgresql` | PostgreSQL 서버 중지 |
| 서비스 재시작 | `sudo systemctl restart postgresql` | PostgreSQL 서버 재시작 |
| 상태 확인 | `sudo systemctl status postgresql` | 서비스 상태 확인 |

---

## **3. PostgreSQL 접속 관련 명령어**

| **기능** | **명령어** | **설명** |
| --- | --- | --- |
| dev DB 접속 | `psql -h localhost -p 5110 -U erpUser -d groupware_dev` | dev DB 접속 |
| prod DB 접속 | `psql -h localhost -p 5220 -U erpUser -d groupware_prod` | prod DB 접속 |
| postgres 계정 접속 | `sudo -u postgres psql` | 관리자 접속 |

---

## **4. psql 내부 명령어**

| **기능** | **명령어** | **설명** |
| --- | --- | --- |
| DB 목록 | `\l` | 데이터베이스 목록 |
| 사용자 목록 | `\du` | role / user 목록 |
| 테이블 목록 | `\dt` | 현재 DB 테이블 목록 |
| 테이블 구조 | `\d 테이블명` | 테이블 컬럼 구조 |
| 접속 정보 | `\conninfo` | 현재 접속 DB 정보 |
| 종료 | `\q` | psql 종료 |

scp -r "E:\ajk\devgit\ifrog_test\DBfood_temp\f1soft-starmap-service\F1Soft.Starmap.Service\bin\Debug\net10.0\* " f1soft@:5110/home/f1soft/groupware/groupware_dev

