---
title: I-Frog 보안코드 기반 멀티테넌시 DB 커넥션 구현
date: 2026-01-23
type: 작업
project: I-Frog
status: 완료
priority: 매우높음
assignee:
  - 안재경
tags:
  - Multi-Tenancy
  - EnvService
---

# I-Frog 보안코드 기반 멀티테넌시 DB 커넥션 구현

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-01-22 |
| **대상 시스템** | F1Soft.Starmap.Service |
| **관련 화면·프로그램** | 전체 API (미들웨어 단) |

> ATC/동방/송연 DB 통합 대비, 배포 하나로 회사·환경별 DB 커넥션을 갈아끼우는 구조로 전환.

## 🔍 현상 및 원인

기존에는 커넥션이 사실상 고정/하드코딩에 가까워서(`9f7f3e9` ATC 커넥션 임시설정), 회사가 늘어나거나 환경(Dev/Stg/Prd)이 바뀔 때마다 배포를 새로 하거나 설정을 손으로 바꿔야 했음.

## 🔧 조치 내용

| 날짜 | 커밋 | 내용 |
|:--|:--|:--|
| 01-22 | `a7122a1` | Ticker 구분자로 DB 커넥션 생성 + 도메인 반환 로직 준비 |
| 01-23 | `9fee22e` | `TickerMiddleware`/`SecurityCodeMapper`/`TickerContext` 최초 구현 — 헤더의 SECURITY_CODE → Ticker/Env 매핑 |
| 01-26 | `106a29e` | `EnvService` 통합, `TickerContext.EnvInitialize` 추가 (Ticker/Env 분리 초기화) |
| 03-13 | `c388966` | PostgreSQL 커넥션 추가 |
| 03-17 | `cd5cc1a`, `bde9b8c`, `8c35454` | ATC 로직 단일화, DBG/SYN/ATC 통합 테스트, empCard 오류 해결 |
| 03-20 | `e552739` | 남아있던 DB 커넥션 하드코딩 제거 |

자세한 구조는 [[[기술] 보안코드 기반 멀티테넌시 커넥션 구조]] 참고.

## ✅ 검증 및 결과

- [x] DBG/SYN/ATC 통합 테스트 완료 (`bde9b8c`, 2026-03-17 기준)
- [ ] 이후 회사/환경 추가 시 회귀 테스트 범위 재정리 필요

## 🔗 참고

- [[[기술] 보안코드 기반 멀티테넌시 커넥션 구조]]
- [[I-Frog IFROG 환경정보]]
