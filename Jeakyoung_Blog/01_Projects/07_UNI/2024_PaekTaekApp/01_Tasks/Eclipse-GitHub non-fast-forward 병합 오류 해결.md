---
title: Eclipse-GitHub non-fast-forward 병합 오류 해결
date: 2026-09-18
type: 작업
project: 대학프로젝트
status: 완료
priority: 낮음
assignee:
  - 안재경
tags: []
---

# Eclipse-GitHub non-fast-forward 병합 오류 해결

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 본인 |
| **요청일** | 2024-04 |
| **대상 시스템** | Eclipse EGit — `4th_GraduationBack` 원격 저장소 |
| **관련 화면·프로그램** | Eclipse Git Perspective — Fetch/Push 설정 |

> Eclipse에서 GitHub로 커밋을 push할 때 `Rejected - non-fast-forward` 에러가 반복돼서, Fetch 경로 설정을 재구성해 해결했다.

## 🔍 현상 및 원인

### 재현 조건

Eclipse에서 로컬 커밋을 GitHub 원격 저장소로 push할 때 `Rejected - non-fast-forward` 에러가 발생.

### 원인

Git Perspective의 Configure Fetch 설정에 남아있던 기존 fetch 경로가 원격 브랜치 상태와 어긋나 있었다. (참고: [Rejected non-fast-forward 해결기](https://winterandsnow.tistory.com/3))

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| Eclipse 설정 | Git Perspective → Configure Fetch | Advanced에서 기존 fetch 경로 삭제 후 재설정 |
| 로컬 작업 | 로컬 저장소 | `master` 브랜치로 원격 변경사항을 먼저 merge한 뒤 프로젝트 push |

## ✅ 검증 및 결과

- [x] Fetch 경로 재설정 후 정상 push 확인

## 🔗 참고

- [[평택대학교앱 리워크 개발 과정]]
- [Rejected non-fast-forward 해결기](https://winterandsnow.tistory.com/3)
