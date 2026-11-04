---
title: 신진SM 시스템 설정 원복 쿼리
date: 2026-09-10
type: 작업
project: 신진SM
status: 진행중
priority: 보통
assignee: []
tags: []
---

# 신진SM 시스템 설정 원복 쿼리

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — (내부 조치) |
| **요청일** | 2026-09-10 |
| **대상 시스템** | MSSQL 인스턴스(엔진 레벨 설정) |
| **관련 화면·프로그램** | 해당 없음 — 서버 엔진 파라미터 |

> 이 문서가 참고하는 회의록에는 "언제 무슨 값으로 바꿨는지"에 대한 기록이 없다. 아래 세 값은 모두 SQL Server의 **공장 기본값**과 일치한다 — `cost threshold for parallelism` 기본값 5, `max degree of parallelism` 기본값 0(무제한), `optimize for ad hoc workloads` 기본값 0(off). 즉 이 쿼리는 이전에 성능 튜닝 목적으로 변경했던 병렬처리 관련 설정을 기본값으로 되돌리는 스크립트로 추정된다 — 04-28/05-06 회의록에 언급된 "쿼리 튜닝 작업"([[신진SM 개발 이력]] 1번 항목)과 시기·성격이 맞물리지만, 어떤 값에서 어떤 값으로 바뀐 것인지, 원복 사유(튜닝이 효과가 없어서인지, 부작용이 있었는지)는 확인되지 않음.

## 🔍 현상 및 원인

미상 — 원복하게 된 구체적인 트리거(장애, 성능 저하, 튜닝 실험 종료 등)가 회의록에 남아있지 않음. 값 자체가 SQL Server 기본값이라는 점에서 "실험적으로 바꿔봤던 설정을 되돌리는" 성격의 조치로 보임.

## 🔧 조치 내용

```sql
EXEC sp_configure 'cost threshold for parallelism', 5;
EXEC sp_configure 'max degree of parallelism', 0;
EXEC sp_configure 'optimize for ad hoc workloads', 0;
RECONFIGURE;
```

| 설정 | 원복값 | SQL Server 기본값 | 비고 |
|:--|:--|:--|:--|
| `cost threshold for parallelism` | 5 | 5 | 병렬 실행 계획으로 전환되는 예상비용 임계치 |
| `max degree of parallelism` | 0 | 0 | 쿼리당 사용 가능한 최대 CPU 수(0=제한 없음) |
| `optimize for ad hoc workloads` | 0 (off) | 0 (off) | 1회성 쿼리 계획 캐시 최적화 |

## ✅ 검증 및 결과

이 조치의 효과(원복 후 성능 변화)는 별도로 측정·기록되지 않음.

## 🔗 참고

- [[신진SM 개발 이력]] — 04-28~05-06 "쿼리 튜닝" 작업 시기 참고
