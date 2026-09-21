---
title: I-Frog Board·Calendar·Emp 그룹웨어 조회 모듈
date: 2025-11-17
type: 작업
project: I-Frog
status: 완료
priority: 낮음
assignee:
  - 안재경
tags:
  - Groupware
---

# I-Frog Board·Calendar·Emp 그룹웨어 조회 모듈

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | — |
| **대상 시스템** | `Controllers/Groupware/{Board,Calendar,Emp}` |
| **관련 화면·프로그램** | 게시판, 일정, 직원 목록 |

> 게시판(공지/이슈 성격), 일정, 직원목록 조회 — 세 개 다 초기 스캐폴딩 이후 큰 변경 없이 쓰이고 있는 기본 그룹웨어 모듈. 실제로 손 댄 부분·앞으로 손볼 부분 확인용으로 정리.

## 🔍 현상 및 원인

세 도메인 다 구조는 거의 동일: `Controller → IXxxService/XxxService → SQLServerHelper → SP`. 엔드포인트는 Board가 4개(이슈 목록/단건 목록/상세/답변 등록)로 제일 많고, Calendar·Emp는 각각 1개(`GetCalendarAllList`, `GetEmpList`)뿐.

## 🔧 조치 내용

| 구분 | 내용 |
|:--|:--|
| 현재 상태 | Board/Calendar/Emp 전부 기능은 도는 상태 |
| 발견한 것 | `BoardController`/`CalendarController`/`EmpController` 셋 다 생성자의 로거 타입이 `ILogger<ApprovalController>`로 되어 있음 — `ApprovalController`에서 복붙하고 자기 타입으로 안 고친 흔적. 로그 카테고리가 실제로는 전부 `ApprovalController`로 찍힘 |
| 필요 여부 | 이대로 둬도 동작엔 문제없지만, 로그로 어느 컨트롤러에서 났는지 구분이 안 되는 게 실사용에서 불편할 수 있음 |

## ✅ 검증 및 결과

- [ ] `ILogger<ApprovalController>` → 각자 타입으로 교체할지 결정
- [ ] Calendar/Emp에 조회 조건(기간, 부서 등) 추가 필요한지 확인

## 🔗 참고

- 최초 도입: `33f00ce`(2025-11-17)
- Board 관련 후속 수정: `f02d066`(공백 정리 수준)
