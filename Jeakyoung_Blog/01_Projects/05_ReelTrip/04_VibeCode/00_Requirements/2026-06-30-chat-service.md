---
title: 채팅 서비스
date: 2026-06-30
type: 요구사항서
project: ReelTrip
status: 완료
assignee:
  - 안재경
tags: []
---

---
작성일: 2026-06-30
대상 앱: Web (apps/web) / API (apps/api-spring)
대상 페이지/화면: /dashboard/chat (ChatScreen.tsx)
작업 유형: 기능추가
우선순위: 높음
---

# 요구사항지시서 — 채팅 서비스 연결

## 현재 상태 (As-Is)

- `ChatScreen.tsx`에 채팅 UI(메시지 목록, 입력창, 전송 버튼)는 완성된 상태
- 메시지 데이터는 `DUMMY_MESSAGES` 하드코딩 배열로만 표시
- 전송 시 `setMessages()`로 로컬 상태에만 추가됨 (서버 저장 없음)
- 새로고침 시 더미 데이터로 초기화됨
- 백엔드에 chat/message 관련 Controller, Service, Entity, Mapper 전무
- WebSocket/실시간 통신 미구현

## 원하는 상태 (To-Be)

- 팀스페이스 단위로 채팅 가능
- 메시지 전송 → DB 저장 → 다른 멤버들이 확인 가능
- 페이지 진입 시 기존 메시지 로딩
- 실시간성: HTTP 폴링(5초 간격) 방식으로 구현 (WebSocket은 이후 단계에서 고려)

## 상세 요구사항

### 기능 요구사항
1. 메시지 전송 (`POST /api/messages`) — 팀스페이스 ID + 텍스트 전송
2. 메시지 목록 조회 (`GET /api/messages?spaceId={id}`) — 최신순 조회
3. 프론트엔드에서 5초 폴링으로 새 메시지 자동 갱신
4. 더미 데이터 제거 및 실제 API 데이터로 교체

### UI/UX 요구사항
1. 기존 ChatScreen.tsx UI 유지 (변경 최소화)
2. 메시지 로딩 중 스피너 표시
3. 전송 후 입력창 초기화 + 스크롤 최하단 이동

### 제약 조건
- WebSocket/STOMP 미사용 (HTTP REST + 폴링)
- Zustand/TanStack Query 신규 설치 없이 기존 `useState + useEffect`로 구현
- MyBatis XML Mapper 패턴 준수 (기존 NotificationMapper.xml 참고)
- JWT Bearer 토큰 인증 방식 유지
- 팀스페이스 1개 = 채팅방 1개 (1:1 매핑)
