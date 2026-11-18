---
title: Scheduler-Service 11.18 Tomcat 배포방안 논의
date: 2026-11-18
type: 회의록
project: SchedulerService
status: 완료
attendees:
  - 안재경
tags: []
---

# Scheduler-Service 11.18 Tomcat 배포방안 논의

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **일시** | 2026-11-18 |
| **장소** | (개인 작업, 세션) |
| **참석자** | 안재경 |
| **안건** | 실제 배포 가능 인프라가 Tomcat뿐이라는 제약 하에서 배포 방식, 기존 서비스와의 컨텍스트 충돌, Vercel 분리배포 검토 |

## 💬 논의 내용

"배포한다고 쳤을 때 활용 가능한 건 톰캣밖에 없다"는 전제 확인. 백엔드 WAR 하나로 합치는 방식(단일배포, CORS불필요)과 백엔드/프론트 각각 별도 WAR(기존 분리원칙 유지) 중 전자로 결정. 이어서 "같은 IP에 컨텍스트 분리로 쓰고 있던 기존 서비스들은 어떻게 되는 거냐, 안 꼬이냐"는 우려가 나왔다 — ROOT.war 배치가 기존에 ROOT를 쓰는 서비스가 있으면 덮어쓰는 문제가 될 수 있음을 확인. "다중 톰캣으로 구현하면 문제없지 않냐"는 제안에 — 별도 Tomcat 인스턴스(다른 포트)로 띄우면 ROOT 충돌 자체가 없어짐을 확인하고 그 방향으로 결정. "버셀 배포한다면 백단은 어떻게 하냐"는 질문도 나와 Vercel은 프론트(정적/서버리스)만 가능하고 Quartz가 상시 떠있어야 하는 백엔드는 여전히 Tomcat이 필요함을 확인했지만, 최종적으로 방향을 바꾸지 않고 Tomcat 단일 WAR로 계속 진행하기로 했다.

## ✅ 결정 사항

| # | 결정 내용 | 근거 |
|:--|:--|:--|
| 1 | 백엔드 WAR 하나에 프론트 빌드결과 통합(단일 배포) | 운영 단순성, CORS 불필요 |
| 2 | 별도 Tomcat 인스턴스(다른 포트)에 ROOT.war로 배치 | 기존 서비스들과 컨텍스트 경로 충돌 회피, Vite base/React Router basename 등 서브경로 대응 작업 불필요 |
| 3 | Vercel+Tomcat 분리배포는 검토했으나 기각, Tomcat 단일WAR 방향 유지 | 백엔드(Quartz 상시실행)는 Vercel에 못 올림, 방향 전환 비용 대비 이득 없음 |

## 🔜 후속 조치

| 조치 | 담당 | 기한 | 상태 |
|:--|:--|:--|:--|
| PLAN.md §11 신설, TASKS.md T22~T27 추가·구현 | sched-planner → sched-worker | 즉시 | 완료 |

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] Tomcat 단일 WAR 배포 구조]]
- [[01_Projects/08_MINI/01_SchedulerService/01_Tasks/Scheduler-Service Tomcat 단일WAR 배포 전환 11.17-18]]
