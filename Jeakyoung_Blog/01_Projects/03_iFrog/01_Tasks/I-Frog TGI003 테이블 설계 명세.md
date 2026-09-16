---
title: I-Frog TGI003 테이블 설계 명세
date: 2026-06-10
type: 작업
project: I-Frog
status: 완료
priority: 보통
assignee: []
tags: []
created: 2026-06-10T14:28:00
---

# I-Frog TGI003 테이블 설계 명세

## 1. 개요

| 항목 | 내용 |
|------|------|
| 요청자 |  |
| 요청일 | 2026-06-10 |
| 대상 시스템 |  |
| 관련 화면·프로그램 |  |

## 2. 현상 및 원인

## 3. 조치 내용

필요한 저장부 →

- 결재 알림 체크여부
- 게시 현황 알림 체크여부
- 공지 알림 체크여부
- 일정 알림 체크여부

KEY → COMPANY_CODE, EMPLOYEE_NO

- 결재 알림 체크여부 → APPROVAL_CHK_FLAG
- 게시 현황 알림 체크여부 → BOARD_CHK_FLAG
- 공지 알림 체크여부 → NOTI_CHK_FLAG
- 일정 알림 체크여부 → SCHEDULE_CHK_FLAG

→ FCM 발송여부 → APPROVAL_CHK_FLAG

12일 기준부터 수정된 프로시저, 테이블 배포필요

## 4. 검증 및 결과

## 5. 참고
