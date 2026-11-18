---
title: Scheduler-Service 11.13 아키텍처 교정
date: 2026-11-13
type: 회의록
project: SchedulerService
status: 완료
attendees:
  - 안재경
tags: []
---

# Scheduler-Service 11.13 아키텍처 교정

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **일시** | 2026-11-13 |
| **장소** | (개인 작업, 세션) |
| **참석자** | 안재경 |
| **안건** | 백엔드/프론트 분리, 프론트엔드 기술, 인증 방식, Spring Boot 버전 베껴쓰기 문제 확정 |

## 💬 논의 내용

T1에서 생성된 `pom.xml`의 Spring Boot 버전(3.3.5)·Lombok 빌드설정이 전혀 무관한 `ReeL-Trip` 프로젝트의 설정과 완전히 동일한 걸 발견 — worker가 독립적으로 판단하지 않고 베낀 것으로 확인. 이어서 "관리자 화면을 Thymeleaf로 같은 Java 앱에 넣을지, 프론트엔드 언어를 뭘 쓸지 정해지지 않은 상태 아니냐"는 질문이 나와 아키텍처를 다시 확정했다.

## ✅ 결정 사항

| # | 결정 내용 | 근거 |
|:--|:--|:--|
| 1 | 백엔드(Spring Boot REST API)/프론트(React SPA) 완전 분리 | Thymeleaf 서버렌더링 폐기 |
| 2 | 스케줄링 엔진 코어는 Spring Boot 프레임워크 유지 | Quartz 연동/설정주입 편의성 근거 유효 |
| 3 | 프론트엔드 기술은 React로 확정 | — |
| 4 | 인증은 세션 쿠키가 아니라 JWT(stateless)로 확정 | SPA가 다른 오리진이라 SameSite/CORS Allow-Credentials/CSRF까지 다 갖추는 복잡도가 불필요 |
| 5 | Spring Boot 패치버전은 지금 고정하지 않고 구현시점에 독립적으로(Maven Central 조회) 확인 | 다른 프로젝트를 베껴쓴 사실이 드러난 데 대한 교정 |

## 🔜 후속 조치

| 조치 | 담당 | 기한 | 상태 |
|:--|:--|:--|:--|
| PLAN.md/TASKS.md에 반영 후 T1부터 backend/frontend 분리로 재작업 | sched-planner → sched-worker | 즉시 | 완료 |

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] Herdr 멀티에이전트 오케스트레이션 구조와 레거시 포팅 원칙]]
