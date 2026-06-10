---
base: "[[Work Flow.base]]"
할당: []
상태: 시작되지 않음
프로젝트: []
---
[[27server.zip]]

# **inux서버 사용법**

### **LINUX 서버 정보**

```plain text
Host : 
[removed]
[removed]
```

## **#### 서버 접속 cmd : ssh f1soft@**

# **서버 구축 정리**

## **1. 서버 기본 정보**

| **항목** | **내용** |
| --- | --- |
| 서버 OS | Ubuntu 22.04.5 LTS |
| 접속 방식 | SSH |
| 개발 환경 | Mac |
| API Runtime | .NET Runtime |
| Web Server | Nginx |
| Database | PostgreSQL |
| DB 관리툴 | DBeaver |

---

# **2. SSH 서버 접속**

| **설명** | **명령어** |
| --- | --- |
| 서버 접속 | `ssh USER@SERVER_IP` |
| 예시 | `ssh ubuntu@SERVER_IP` |

---

# **3. 시스템 업데이트**

| **설명** | **명령어** |
| --- | --- |
| 패키지 목록 업데이트 | `sudo apt update` |
| 시스템 업그레이드 | `sudo apt upgrade -y` |
| 커널 업데이트 후 재부팅 | `sudo reboot` |

---

# **4. .NET 패키지 저장소 등록**

| **설명** | **명령어** |
| --- | --- |
| Microsoft 패키지 다운로드 | `wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb` |
| 패키지 등록 | `sudo dpkg -i packages-microsoft-prod.deb` |
| 패키지 업데이트 | `sudo apt update` |

---

# **5. .NET Runtime 설치**

| **설명** | **명령어** |
| --- | --- |
| Runtime 설치 | `sudo apt install dotnet-runtime-10.0 -y` |
| 설치 확인 | `dotnet --version` |

---

# **6. Nginx 설치**

| **설명** | **명령어** |
| --- | --- |
| Nginx 설치 | `sudo apt install nginx -y` |
| 버전 확인 | `nginx -v` |
| 서비스 상태 확인 | `sudo systemctl status nginx` |

---

# **7. PostgreSQL 설치**

| **설명** | **명령어** |
| --- | --- |
| PostgreSQL 설치 | `sudo apt install postgresql postgresql-contrib -y` |
| 버전 확인 | `psql --version` |
| 서비스 상태 확인 | `sudo systemctl status postgresql` |

---

# **8. PostgreSQL 사용자 및 DB 생성**

| **설명** | **명령어** |
| --- | --- |
| postgres 계정 접속 | `sudo -u postgres psql` |
| 사용자 생성 | `CREATE USER apiuser WITH PASSWORD 'password';` |
| DB 생성 | `CREATE DATABASE apidb OWNER apiuser;` |
| 권한 부여 | `GRANT ALL PRIVILEGES ON DATABASE apidb TO apiuser;` |
| psql 종료 | `\q` |

---

# **9. PostgreSQL 외부 접속 설정**

| **파일** | **설정** |
| --- | --- |
| `/etc/postgresql/14/main/postgresql.conf` | `listen_addresses = '*'` |
| `/etc/postgresql/14/main/pg_hba.conf` | `host all all 0.0.0.0/0 md5` |

적용

---

```plain text
sudo systemctl restart postgresql
```

---

---

# **10. PostgreSQL 외부 접속 정보**

| **항목** | **값** |
| --- | --- |
| Host | 서버 IP |
| Port | (5432), 5110, 5220 |
| Database | apidb |
| User | apiuser |
| Password | 설정한 비밀번호 |

---

# **11. Nginx 포트 구조**

| **구분** | **DEV** | **PROD** |
| --- | --- | --- |
| 외부 포트 | 4110 | 4220 |
| 내부 API 포트 | 40110 | 40220 |

---

# **12. Nginx Reverse Proxy 설정**

파일 경로

---

```plain text
/etc/nginx/sites-available/api
```

---

설정

---

```plain text
server {

listen 4110;

location / {
    proxy_pass http://localhost:40110;
    proxy_http_version 1.1;

    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection keep-alive;
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
}
}

server {

listen 4220;

location / {
    proxy_pass http://localhost:40220;
    proxy_http_version 1.1;

    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection keep-alive;
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
}
}

```

---

# **13. Nginx 사이트 활성화**

| **설명** | **명령어** |
| --- | --- |
| 사이트 활성화 | `sudo ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled/` |
| 설정 검사 | `sudo nginx -t` |
| 설정 적용 | `sudo systemctl reload nginx` |

---

# **14. 서버 포트 확인**

| **설명** | **명령어** |
| --- | --- |
| 전체 포트 확인 | `ss -tulpn` |
| 특정 포트 확인 | `ss -tulpn | grep 40110` |

---

# **15. Nginx 주요 명령어**

| **기능** | **명령어** |
| --- | --- |
| 상태 확인 | `sudo systemctl status nginx` |
| 시작 | `sudo systemctl start nginx` |
| 중지 | `sudo systemctl stop nginx` |
| 재시작 | `sudo systemctl restart nginx` |
| 설정 적용 | `sudo systemctl reload nginx` |
| 설정 검사 | `sudo nginx -t` |
| 에러 로그 | `tail -f /var/log/nginx/error.log` |
| 접속 로그 | `tail -f /var/log/nginx/access.log` |

---

# **16. 주요 서버 디렉토리**

| **경로** | **설명** |
| --- | --- |
| `/etc/nginx/nginx.conf` | nginx 메인 설정 |
| `/etc/nginx/sites-available` | nginx 사이트 설정 |
| `/etc/nginx/sites-enabled` | 활성화된 사이트 |
| `/var/log/nginx` | nginx 로그 |

---

# **17. 현재 서버 요청 흐름**

| **단계** | **설명** |
| --- | --- |
| 1 | Client 요청 |
| 2 | 외부 포트 4110 / 4220 |
| 3 | Nginx Reverse Proxy |
| 4 | 내부 API 포트 40110 / 40220 |
| 5 | ASP.NET API (추후 실행) |
| 6 | PostgreSQL DB |

---

# **18. 현재 서버 구조**

| **계층** | **시스템** |
| --- | --- |
| Client | 외부 사용자 |
| Server | Ubuntu |
| Web Server | Nginx |
| Backend | .NET API |
| Database | PostgreSQL |

---

# **현재 서버 상태**

| **항목** | **상태** |
| --- | --- |
| SSH 접속 | 완료 |
| 시스템 업데이트 | 완료 |
| .NET Runtime | 설치 완료 |
| Nginx | 설치 및 설정 완료 |
| PostgreSQL | 설치 및 외부 접속 설정 완료 |
| Reverse Proxy | 설정 완료 |
| API 실행 | 아직 안함 |

최주임님이 이따가 ERP연동하는 MES웹쪽 코드를 주면

기능개발은 제가 할건데

구현계획서를 한번 작성해볼래요

어느부분에? 어떻게? JAVA 에서 어떻게 c#으로 변환방법 or 호출방법 2가지 ERP쪽 코드가 JAVA 




