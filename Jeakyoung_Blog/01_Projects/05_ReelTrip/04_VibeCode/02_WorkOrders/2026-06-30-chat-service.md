---
title: 채팅 서비스
date: 2026-06-30
type: 작업지시서
project: ReelTrip
status: 완료
assignee:
  - 안재경
tags: []
---

---
작성일: 2026-06-30
요구사항 참조: docs/orders/2026-06-30-chat-service.md
대상 앱: Web / API
대상 페이지/화면: /dashboard/chat
작업 유형: 기능추가
예상 영향 범위: ChatScreen.tsx, SecurityConfig.java, 신규 chat 레이어
---

# 작업지시서 — 채팅 서비스 연결

## 요구사항 분석 요약

- 팀스페이스별 채팅(1 스페이스 = 1 채팅방) REST API를 구현하고, 프론트에서 연결
- 실시간성은 **5초 폴링** 방식으로 구현 (WebSocket 없음)
- 백엔드: Notification 레이어 패턴을 그대로 따라 Message 레이어 신규 생성
- 프론트: `DUMMY_MESSAGES` 제거 후 실제 API 호출로 교체, 폴링 추가

---

## 작업 계획

### 1단계: DB 스키마 정의
- [ ] `chat_messages` 테이블 DDL 작성 (`schema.sql` 또는 init 스크립트에 추가)

### 2단계: 백엔드 — Message 레이어 생성 (Notification 패턴 준수)
- [ ] `Message.java` (model)
- [ ] `MessageResponse.java` (dto)
- [ ] `SendMessageRequest.java` (dto)
- [ ] `MessageMapper.java` (mapper interface)
- [ ] `MessageMapper.xml` (MyBatis XML)
- [ ] `MessageService.java` (service interface)
- [ ] `MessageServiceImpl.java` (service impl)
- [ ] `MessageController.java` (controller)
- [ ] `SecurityConfig.java` — `/api/messages/**` 인증 경로 추가

### 3단계: 프론트엔드 — chat API + ChatScreen 교체
- [ ] `apps/web/src/domains/chat/api.ts` 신규 생성
- [ ] `ChatScreen.tsx` — 더미 데이터 제거, 실제 API + 5초 폴링으로 교체

---

## 변경 대상 파일

| 파일 경로 | 변경 유형 | 변경 내용 요약 |
|-----------|-----------|----------------|
| `apps/api-spring/.../chat/model/Message.java` | 생성 | 메시지 모델 |
| `apps/api-spring/.../chat/dto/MessageResponse.java` | 생성 | 응답 DTO |
| `apps/api-spring/.../chat/dto/SendMessageRequest.java` | 생성 | 전송 요청 DTO |
| `apps/api-spring/.../chat/mapper/MessageMapper.java` | 생성 | MyBatis 매퍼 인터페이스 |
| `apps/api-spring/src/main/resources/mapper/MessageMapper.xml` | 생성 | MyBatis XML |
| `apps/api-spring/.../chat/service/MessageService.java` | 생성 | 서비스 인터페이스 |
| `apps/api-spring/.../chat/service/impl/MessageServiceImpl.java` | 생성 | 서비스 구현체 |
| `apps/api-spring/.../chat/controller/MessageController.java` | 생성 | REST 컨트롤러 |
| `apps/api-spring/.../config/SecurityConfig.java` | 수정 | `/api/messages/**` 인증 추가 |
| `apps/web/src/domains/chat/api.ts` | 생성 | 프론트 API 함수 |
| `apps/web/src/domains/dashboard/components/ChatScreen.tsx` | 수정 | 더미 제거 + 실API 연결 |

---

## API 설계

### GET /api/messages?spaceId={id}
- 인증: Bearer JWT 필수
- 응답: `ApiResponse<List<MessageResponse>>`
- 정렬: `sent_at ASC` (오래된 순)

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "spaceId": 3,
      "authorUsername": "민수",
      "content": "숙소 예약 어떻게 됐어요?",
      "sentAt": "2026-06-30T10:12:00"
    }
  ]
}
```

### POST /api/messages
- 인증: Bearer JWT 필수
- 요청 바디: `{ "spaceId": 3, "content": "메시지 내용" }`
- 응답: `ApiResponse<MessageResponse>`

---

## DB 스키마

```sql
CREATE TABLE IF NOT EXISTS chat_messages (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    space_id   BIGINT       NOT NULL,
    user_id    BIGINT       NOT NULL,
    content    TEXT         NOT NULL,
    sent_at    DATETIME     NOT NULL DEFAULT NOW(),
    FOREIGN KEY (space_id) REFERENCES team_spaces(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)  REFERENCES users(id)
);
```

---

## 사이드 이펙트 검토

- `SecurityConfig.java` 수정 → `/api/messages/**` 추가 시 다른 경로에 영향 없음
- `ChatScreen.tsx` 폴링 → 컴포넌트 언마운트 시 `clearInterval` 처리 필수 (메모리 누수 방지)
- 신규 테이블이므로 기존 데이터에 영향 없음

---

## 확인 필요 사항

- [x] WebSocket 대신 HTTP 폴링(5초) 방식으로 진행 — 요구사항 확정
- [x] 팀스페이스 1개 = 채팅방 1개 — 확정
- [x] Zustand/TanStack Query 미설치, `useState + useEffect + setInterval` 사용 — 확정
- [ ] DB `schema.sql` 위치 확인 필요 (init 스크립트가 어디 있는지)

---

## 컨펌

- [ ] 위 계획대로 진행 승인
- [ ] 수정 후 재검토 필요
