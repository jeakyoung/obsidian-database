---
type: 참고문서
title: NginX 서버 관리 명령어 가이드
category: 배포
date: 2026-06-11
---

# NginX 명령어 가이드

NginX 웹 서버의 관리, 설정, 디버깅을 위한 필수 명령어 모음

---

## 🔧 1. 서비스 관리 명령어

### 상태 확인
```bash
sudo systemctl status nginx
```
- nginx 서비스 현재 상태 확인
- 실행 중/중지 상태 파악

### 시작/중지/재시작
```bash
# 시작
sudo systemctl start nginx

# 중지
sudo systemctl stop nginx

# 재시작 (완전 재시작)
sudo systemctl restart nginx
```

### 설정 재적용 (다운타임 없음)
```bash
# systemctl 사용 (권장)
sudo systemctl reload nginx

# 직접 명령어
sudo nginx -s reload
```

**차이점:**
- `restart`: 완전히 종료 후 재시작 (잠깐 다운타임 있음)
- `reload`: 설정만 다시 로드 (다운타임 없음)

### 프로세스 확인
```bash
ps -ef | grep nginx
```

출력 예시:
```
root     1234  0.0  0.1  20000  5000 ?  Ss  10:00  0:00 nginx: master process
www-data 1235  0.0  0.2  25000  8000 ?  S   10:00  0:01 nginx: worker process
```

---

## 📋 2. 설정 검사 및 디버깅

### 설정 문법 검사
```bash
sudo nginx -t
```

**성공 응답:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

**실패 응답:**
```
nginx: [emerg] duplicate upstream "backend" in /etc/nginx/nginx.conf:50
```

### 설정 파일 위치 확인
```bash
nginx -T
```
- 모든 설정 파일 경로 표시
- 설정 상세 내용도 출력

---

## 📊 3. 로그 확인

### Access 로그 실시간 확인
```bash
tail -f /var/log/nginx/access.log
```

**로그 형식:**
```
[REDACTED_IP] - - [11/Jun/2026:10:30:45 +0900] "GET /index.html HTTP/1.1" 200 512 "-" "Mozilla/5.0"
```

**필드 해석:**
- IP: [REDACTED_IP]
- 시간: 11/Jun/2026:10:30:45 +0900
- 요청: GET /index.html HTTP/1.1
- 상태코드: 200
- 응답 크기: 512 bytes

### Error 로그 실시간 확인
```bash
tail -f /var/log/nginx/error.log
```

**예시 에러:**
```
2026/06/11 10:30:45 [error] 1234#0: *5 connect() failed (111: Connection refused)
```

### 최근 N줄 로그 확인
```bash
# 최근 100줄
tail -n 100 /var/log/nginx/error.log

# 최근 50줄
tail -n 50 /var/log/nginx/access.log
```

### 로그 파일 크기 확인
```bash
ls -lh /var/log/nginx/
```

---

## 🗂️ 4. 설정 파일 위치 (Ubuntu)

| 항목 | 경로 | 설명 |
|------|------|------|
| **메인 설정** | `/etc/nginx/nginx.conf` | 전체 설정의 중심 |
| **사이트 설정** | `/etc/nginx/sites-available/` | 모든 사이트 설정 (include되지 않은 것도 포함) |
| **활성 사이트** | `/etc/nginx/sites-enabled/` | 실제 활성화된 사이트 (보통 symlink) |
| **Conf.d 설정** | `/etc/nginx/conf.d/` | 추가 설정 파일 |
| **Access 로그** | `/var/log/nginx/access.log` | 접속 로그 |
| **Error 로그** | `/var/log/nginx/error.log` | 에러 로그 |
| **Pid 파일** | `/var/run/nginx.pid` | NginX 프로세스 ID |

---

## 💡 5. 실제 운영 플로우 (권장)

### 설정 변경 시
```bash
# 1단계: 설정 파일 수정
sudo nano /etc/nginx/sites-available/mysite

# 2단계: 설정 검사
sudo nginx -t

# 3단계: 다운타임 없이 재적용
sudo systemctl reload nginx

# 4단계: 결과 확인
tail -f /var/log/nginx/access.log
```

### 문제 발생 시
```bash
# 1단계: 에러 로그 확인
tail -f /var/log/nginx/error.log

# 2단계: 설정 재검사
sudo nginx -t

# 3단계: 프로세스 확인
ps -ef | grep nginx

# 4단계: 필요시 재시작
sudo systemctl restart nginx
```

---

## 🔍 6. 트러블슈팅
	
### 문제: "Address already in use"
```
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
```

**해결:**
```bash
# 포트 점유 프로세스 확인
sudo lsof -i :80
sudo netstat -tulpn | grep :80

# 기존 프로세스 종료
sudo kill -9 [PID]

# nginx 재시작
sudo systemctl start nginx
```

### 문제: "Permission denied"
```
nginx: [emerg] open() "/var/log/nginx/error.log" failed (13: Permission denied)
```

**해결:**
```bash
# 권한 확인 및 변경
sudo chown -R www-data:www-data /var/log/nginx
sudo chmod -R 755 /var/log/nginx

# nginx 재시작
sudo systemctl restart nginx
```

### 문제: 설정 파일이 많아서 어디서 에러가 나는지 모를 때
```bash
# 전체 설정 출력 (모든 include 파일 포함)
sudo nginx -T | grep -A5 "error" 

# 특정 문자열 검색
sudo nginx -T | grep "server_name"
```

---

## 📌 자주 사용하는 명령어 (Top 5)

```bash
# 1. 상태 확인
sudo systemctl status nginx

# 2. 설정 재적용 (가장 자주)
sudo systemctl reload nginx

# 3. 에러 로그 확인
tail -f /var/log/nginx/error.log

# 4. 설정 검사
sudo nginx -t

# 5. 프로세스 확인
ps -ef | grep nginx
```

---

## 📚 참고

- **Ubuntu 버전에 따라 경로가 다를 수 있음**
- **권한 부족 시 `sudo` 필수**
- **설정 변경 후 반드시 `nginx -t` 실행**

---

**작성일:** 2026-06-11  
**카테고리:** 배포/서버 관리

/home/f1soft/data_boucher/dev\
220이 운영
110이 개발


nohup dotnet F1Soft.Starmap.Service.dll --urls "http://localhost:30110" --serviceName data_boucher > data_boucher_prd.log 2>&1 &

nohup dotnet F1Soft.Starmap.Service.dll --urls "http://localhost:30110" --serviceName data_boucher > data_boucher_dev.log 2>&1 &