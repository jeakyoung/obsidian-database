---
title: NginX 서버 라우팅 설정 - 포트 4110
date: 2026-06-11
type: 참고자료
project: 신진SM
status: 진행중
category: 배포
tags: []
server: 신진SM 프로덕션
---

# NginX 서버 라우팅 설정 - 포트 4110

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **용도** | 신진SM 서비스 트래픽을 경로 기준으로 여러 백엔드 포트에 분기 |
| **대상 시스템** | 배포 서버 nginx (IPlusMES 소스 저장소 밖 — 설정 파일은 이 SVN 리포지토리에 없음) |
| **최종 확인일** | 2026-06-11, [[신진SM 05.28 업무 미팅]](문서 내부 날짜 06-05)에 공유된 설정 원문 기준 |

## ⚙️ 환경 및 전제

> [!note] 출처
> 아래 `server` 블록은 미팅 노트에 실제로 붙여넣어진 설정 원문이다. 포트 번호(4110 / 40110 / 40111 / 40112)는 그 출처를 신뢰한 값이며, IPlusMES 코드 저장소 자체에는 nginx 설정 파일이 없다(배포 서버에서 직접 관리). 아래 "트러블슈팅/성능 튜닝" 항목 중 실제로 이 서버에서 확인된 것은 없고, nginx 일반 지식 기준의 참고용이다 — 실제 파일 경로·운영 방식(systemd vs 다른 방식)은 서버 담당자 확인 필요.

## 📖 상세 내용

### 라우팅 규칙 (미팅 노트 원문)

```nginx
server {
    listen 4110;
    underscores_in_headers on;  # 언더스코어가 있는 헤더 허용

    location /abc {
        proxy_pass http://localhost:40111;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection keep-alive;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /abcd {
        proxy_pass http://localhost:40112;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection keep-alive;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

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

`/abc`, `/abcd`는 실제 운영 경로명을 그대로 옮긴 것이 아니라 미팅 노트에 있던 예시 표기다 — 실제 경로 프리픽스는 서버 설정 파일에서 확인 필요.

### 라우팅 흐름

```
클라이언트 요청 → NginX (:4110)
                    ├─ /abc  시작 → :40111
                    ├─ /abcd 시작 → :40112
                    └─ 그 외        → :40110 (기본 WAS)
```

`underscores_in_headers on`은 nginx 기본값이 헤더의 언더스코어(`_`)를 무시/제거하는 것과 관련된 표준 옵션이다 — 신진SM 쪽에서 언더스코어 포함 커스텀 헤더를 쓰는지는 이 문서만으로 확인되지 않는다.

## ⚠️ 주의사항

- 이 설정 파일의 실제 위치, `nginx -t` / `systemctl restart nginx` 등 운영 방식은 이 리포지토리에서 검증할 수 없다 — 배포 서버 담당자 확인 필요.
- 40110/40111/40112가 각각 어떤 WAS 인스턴스(Tomcat 등)에 대응하는지는 미팅 노트에 명시돼 있지 않다.
- 포트 4110이 외부에 노출되는지, 사내망 전용인지는 미확인 — 방화벽/보안 설정은 별도 확인 필요.

## 🔗 참고

- [[신진SM 05.28 업무 미팅]] (원본 설정 출처)
- [\[통합\] 더존ERP 동기화](<[통합] 더존ERP 동기화.md>)
