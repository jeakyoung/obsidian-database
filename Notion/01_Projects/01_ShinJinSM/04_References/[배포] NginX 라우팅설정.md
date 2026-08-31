---
type: 참고문서
title: NginX 서버 라우팅 설정 - 포트 4110
category: 배포
server: 신진SM 프로덕션
---

# NginX 라우팅 설정

## 서버 정보

**포트:** 4110  
**용도:** 신진SM 시스템 트래픽 분기  
**설정 파일:** `/etc/nginx/sites-available/sinjin` (또는 `nginx.conf`)

---

## 라우팅 규칙

### 포트 4110 설정
```nginx
server {
    listen 4110;
    underscores_in_headers on;  # 언더스코어가 있는 헤더 허용
    
    # 1. /abc 로 시작하는 요청
    location /abc {
        proxy_pass http://localhost:40111;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection keep-alive;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # 2. /abcd 로 시작하는 요청
    location /abcd {
        proxy_pass http://localhost:40112;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection keep-alive;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # 3. 기본 라우팅 (나머지 모든 요청)
    location / {
        proxy_pass http://localhost:40110;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection keep-alive;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 라우팅 흐름도

```
클라이언트 요청 → NginX (포트 4110)
                    │
                    ├─ /abc 시작 → localhost:40111
                    │
                    ├─ /abcd 시작 → localhost:40112
                    │
                    └─ 기타 경로 → localhost:40110
```

---

## 백엔드 서버 포트

| 포트 | 용도 | 상태 |
|------|------|------|
| 40110 | 기본 라우팅 (주 서비스) | [ ] |
| 40111 | /abc 경로 처리 | [ ] |
| 40112 | /abcd 경로 처리 | [ ] |

---

## 설정 상세 해석

### underscores_in_headers on
```
목적: HTTP 헤더에 언더스코어(_) 문자 허용
이유: 신진SM 시스템이 헤더에 언더스코어를 사용할 경우 필요
```

### proxy_http_version 1.1
```
목적: HTTP/1.1 프로토콜 사용
효과: Keep-Alive 연결 지원으로 성능 향상
```

### proxy_set_header Connection keep-alive
```
목적: 백엔드와의 연결 유지
효과: 반복적 요청시 재연결 오버헤드 감소
```

### proxy_cache_bypass $http_upgrade
```
목적: WebSocket 업그레이드 시 캐시 무효화
효과: 실시간 통신 기능 정상 작동
```

---

## 사용 예시

### 기본 요청
```
GET http://localhost:4110/data
→ GET http://localhost:40110/data
```

### /abc 경로 요청
```
GET http://localhost:4110/abc/query
→ GET http://localhost:40111/abc/query
```

### /abcd 경로 요청
```
GET http://localhost:4110/abcd/status
→ GET http://localhost:40112/abcd/status
```

---

## 설정 적용 방법

### 1. 설정 파일 수정
```bash
sudo nano /etc/nginx/sites-available/sinjin
# 또는
sudo nano /etc/nginx/nginx.conf
```

### 2. 설정 문법 검증
```bash
sudo nginx -t
```

**성공 메시지:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 3. NginX 재시작
```bash
sudo systemctl restart nginx
```

또는

```bash
sudo /etc/init.d/nginx restart
```

### 4. 상태 확인
```bash
sudo systemctl status nginx
```

---

## 트러블슈팅

### 문제 1: 502 Bad Gateway 오류

**원인:** 백엔드 서버(40110, 40111, 40112) 미실행  
**해결:**
```bash
# 백엔드 프로세스 확인
ps aux | grep java
ps aux | grep tomcat

# 포트 열림 확인
netstat -tulpn | grep :4010
```

### 문제 2: 언더스코어 헤더 오류

**원인:** `underscores_in_headers off` 설정  
**해결:**
```nginx
underscores_in_headers on;  # 추가 필수
```

### 문제 3: Connection refused 오류

**원인:** 백엔드 서버 연결 실패  
**확인:**
```bash
telnet localhost 40110
telnet localhost 40111
telnet localhost 40112
```

### 문제 4: 설정 변경 후에도 적용 안됨

**원인:** NginX 재시작 미실행  
**해결:**
```bash
sudo systemctl restart nginx
# 또는
sudo nginx -s reload
```

---

## 모니터링

### 접근 로그 확인
```bash
tail -f /var/log/nginx/access.log
```

### 에러 로그 확인
```bash
tail -f /var/log/nginx/error.log
```

### 각 포트별 트래픽 확인
```bash
netstat -antp | grep nginx
ss -tulpn | grep nginx
```

---

## 성능 튜닝

### 연결 수 제한 조정
```nginx
upstream backend {
    server localhost:40110 max_fails=3 fail_timeout=30s;
    server localhost:40111 max_fails=3 fail_timeout=30s;
    server localhost:40112 max_fails=3 fail_timeout=30s;
}
```

### 타임아웃 설정
```nginx
proxy_connect_timeout 5s;    # 백엔드 연결 타임아웃
proxy_send_timeout 60s;      # 요청 전송 타임아웃
proxy_read_timeout 60s;      # 응답 수신 타임아웃
```

---

## 보안 고려사항

⚠️ **주의:**
1. 포트 4110이 필요한 내부망에서만 접근 허용
2. 외부 노출 필요시 방화벽 규칙 추가
3. SSL/TLS 암호화 고려

---

## 관련 문서

- [[20260605] 포장중복문제 및 성능최적화]] - 서버 설정 언급
- [[진행중] 성능최적화 및 로깅]] - 성능 모니터링

