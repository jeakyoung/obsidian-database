---
base: "[[Work Flow.base]]"
할당: []
상태: 시작되지 않음
프로젝트: []
---
# **NginX 명령어 정리**

## **Nginx 관리 명령어**

| **기능** | **명령어** | **설명** |
| --- | --- | --- |
| 상태 확인 | `sudo systemctl status nginx` | nginx 서비스 상태 확인 |
| 시작 | `sudo systemctl start nginx` | nginx 서버 실행 |
| 중지 | `sudo systemctl stop nginx` | nginx 서버 정지 |
| 재시작 | `sudo systemctl restart nginx` | nginx 완전 재시작 |
| 설정 reload | `sudo systemctl reload nginx` | 설정만 재적용 (다운타임 없음) |
| 직접 reload | `sudo nginx -s reload` | nginx 설정 재적용 |
| 설정 테스트 | `sudo nginx -t` | nginx 설정 문법 검사 |
| 프로세스 확인 | `ps -ef | grep nginx` | nginx 실행 프로세스 확인 |

---

## **Nginx 로그 확인**

| **기능** | **명령어** | **설명** |
| --- | --- | --- |
| access 로그 확인 | `tail -f /var/log/nginx/access.log` | 접속 로그 실시간 확인 |
| error 로그 확인 | `tail -f /var/log/nginx/error.log` | 에러 로그 확인 |
| 최근 로그 확인 | `tail -n 100 /var/log/nginx/error.log` | 최근 100줄 로그 |

---

## **Nginx 설정 파일 위치 (Ubuntu)**

| **항목** | **경로** |
| --- | --- |
| 메인 설정 | `/etc/nginx/nginx.conf` |
| 사이트 설정 | `/etc/nginx/sites-available/` |
| 활성 사이트 | `/etc/nginx/sites-enabled/` |
| 로그 디렉토리 | `/var/log/nginx/` |

---

## **실제 운영에서 가장 많이 쓰는 순서**

1. 설정 수정

/etc/nginx/sites-available/파일

sudo nginx -t

2. 설정 적용

sudo systemctl reload nginx

---

→ 백엔드 서비스 배포 정리

```sql
# 0: E드라이브로 변경
e:

# 1. 빌드 경로로 이동
cd "E:\ajk\devgit\ifrog_test\DBfood_temp\f1soft-starmap-service\F1Soft.Starmap.Service\bin\Debug\net10.0"
cd "E:\ajk\devgit\ifrog_test\DBfood_temp\f1soft-starmap-service\F1Soft.Starmap.Service\bin\Release\net10.0"


# 2. 현재 폴더(.)의 모든 내용을 리눅스로 전송
scp -r . f1soft@:/home/f1soft/groupware/groupware_dev
scp -r . f1soft@:/home/f1soft/groupware/groupware_prod
```

nginx → availed_site내에 헤더 underscore 허용 규칙 추가함 ( security_code를 못가져와서 추가함 )

```sql
# 개발 닷넷 서비스 시행
cd /home/f1soft/groupware/groupware_dev
nohup dotnet F1Soft.Starmap.Service.dll --urls "http://localhost:40110" --serviceName dotnet_dev > service_dev.log 2>&1 &
```

```sql
# 운영 닷넷 서비스 시행
cd /home/f1soft/groupware/groupware_prod
nohup dotnet F1Soft.Starmap.Service.dll --urls "http://127.0.0.1:40220" --serviceName dotnet_prod > service_prod.log 2>&1 &
```

```sql
# 어떤포트에 어떤서비스가 몇번 pid인지 확인가능
ps -ef | grep dotnet

# 확인하고 특정 서비스만 내리는것또한 가능
	kill -9 PID번호
```

```sql
# 실행 예시 (경로와 라이브러리 파일명은 환경에 맞게 수정)
nohup java -cp ".:./lib/*" com.scheduler.SchedulerContextListener > scheduler.log 2>&1 &

# 배포 경로
scp -r . f1soft@:/home/f1soft/groupware/groupware_cls/com/scheduler

# ps id 탑색
ps -ef | grep SchedulerContextListener
```

dotnet F1Soft.Starmap.Service.dll --urls "[http://localhost:40110](http://localhost:40110/)"

**nohup dotnet F1Soft.Starmap.Service.dll --urls** "http://127.0.0.1:40220" > prd_service.log>&1 &

→ 닷넷 서비스 실행 40110으로 BG실행임 ( 로그는 service.log로 쌓기 )

ps -ef | grep dotnet

→ dotnet 사용중인지 확인

netstat -nlp | grep :40110 → 서비스 포트 가져오기


tail -f service.log → 서비스 로그확인



배포용

[](http://:4110/swagger/index.html)

[http://:4220/swagger/index.html](http://:4110/swagger/index.html)

nohup dotnet F1Soft.Starmap.Service.dll --urls "http://localhost:30110" --serviceName data_boucher > data_boucher.log 2>&1 &



4111

4222

5110

5220


