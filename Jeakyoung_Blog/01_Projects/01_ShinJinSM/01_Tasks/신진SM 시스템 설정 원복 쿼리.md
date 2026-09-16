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

## 1. 개요

| 항목 | 내용 |
|------|------|
| 요청자 |  |
| 요청일 | 2026-09-10 |
| 대상 시스템 |  |
| 관련 화면·프로그램 |  |

## 2. 현상 및 원인

## 3. 조치 내용

EXEC sp_configure 'cost threshold for parallelism', 5;
EXEC sp_configure 'max degree of parallelism', 0;
EXEC sp_configure 'optimize for ad hoc workloads', 0;
RECONFIGURE;

## 4. 검증 및 결과

## 5. 참고
