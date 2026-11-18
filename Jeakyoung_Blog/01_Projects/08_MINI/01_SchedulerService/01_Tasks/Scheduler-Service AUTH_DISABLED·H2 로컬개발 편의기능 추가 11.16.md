---
title: Scheduler-Service AUTH_DISABLED·H2 로컬개발 편의기능 추가 11.16
date: 2026-11-16
type: 작업
project: SchedulerService
status: 완료
priority: 보통
assignee:
  - 안재경
tags: []
---

# Scheduler-Service AUTH_DISABLED·H2 로컬개발 편의기능 추가 11.16

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 본인 — 로컬 테스트가 번거로워 요청 |
| **요청일** | 2026-11-16 |
| **대상 시스템** | Scheduler-Service 백엔드/프론트엔드 |
| **관련 화면·프로그램** | `SecurityConfig`, `AuthContext.tsx`, `application.yml`, Flyway |

> 로컬에서 SQL Server 없이, 로그인 없이 바로 테스트할 수 있게 만든 opt-in 편의기능.

## 🔍 현상 및 원인

매번 로컬 SQL Server를 Docker로 띄우고 관리자 계정을 시드해야 테스트가 가능해서 번거로웠다. "로그인 일단 패스할 수 있게 해줘", "DB 선택 안 해도 구동이 되어야 하는데"라는 요청이 있었다.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 백엔드 인증 | `AUTH_DISABLED`(env, 기본 false) | true면 `/api/**` 전체 `permitAll`+JWT 필터 미적용, 기동 시 WARN 경고 |
| 프론트 인증 | `VITE_AUTH_DISABLED`(env, 기본 false) | true면 `AuthContext`가 더미 유저로 즉시 채워져 로그인 화면 리다이렉트 안 함, 네비바에 경고 배지 |
| 메타DB | `DB_URL` 미설정 시 | H2 파일 DB로 자동 fallback, H2 전용 Flyway 마이그레이션+Quartz `StdJDBCDelegate` 자동 분기 |

진행 중 테스트가 호스트 쉘의 `AUTH_DISABLED` 값에 영향받아 실패하는 격리결함과, H2 전환 중 드러난 벤더종속 SQL(`enabled = 1` 정수리터럴, `SYSUTCDATETIME()`) 2건도 함께 발견·수정했다.

## ✅ 검증 및 결과

- [x] `AUTH_DISABLED=true`로 백엔드를 띄우고 `VITE_AUTH_DISABLED=true`로 프론트를 띄우면 로그인 없이 전체 화면 접근 가능
- [x] `DB_URL` 미설정 시 H2로 자동 기동, Flyway/Quartz 정상
- [x] `AUTH_DISABLED` 설정된 채로도/안 된 채로도 `mvn test` 100/100 그린

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] JWT stateless 인증과 로컬개발 편의기능]]
- `.team/LOG.md` AUTH_DISABLED/H2 fallback 섹션 (Scheduler-Service 레포)
