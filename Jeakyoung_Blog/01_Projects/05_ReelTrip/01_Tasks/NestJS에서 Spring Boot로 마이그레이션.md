---
title: NestJS에서 Spring Boot로 마이그레이션
date: 2026-05-20
type: 작업
project: ReelTrip
status: 완료
priority: 높음
assignee:
  - 안재경
tags: []
---

# NestJS에서 Spring Boot로 마이그레이션

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-05-20 |
| **대상 시스템** | API |
| **관련 화면·프로그램** | `apps/api-spring` 전체 |

> 백엔드 프레임워크를 통째로 갈아엎은 가장 큰 규모의 리팩토링. [[ReelTrip 개발 과정]] 3번 항목의 상세 버전

## 🔍 현상 및 원인

초기 백엔드는 NestJS로 시작해서 인증, 벡터 검색용 DTO(`CreateDocumentRequest` 등)까지 붙어있는 상태였다. Vercel 서버리스 환경 위에서 프론트/백엔드를 같이 돌리려다 CORS·라우팅 문제를 계속 겪은 뒤([[ReelTrip 개발 과정]] 2번 항목), 프레임워크 자체를 Java/Spring 생태계로 옮기기로 결정했다. MyBatis + Flyway + pgvector 조합으로 DB 계층을 다시 짜는 게 이번 마이그레이션의 핵심 목표였다.

## 🔧 조치 내용

이관이 아니라 **새로 스캐폴딩 후 한 번에 스왑**하는 방식으로 진행했다. 첫 마이그레이션 커밋 하나가 153개 파일, +2356/-1822줄 — Spring Boot 프로젝트 구조를 통째로 새로 만들면서 기존 NestJS 파일들을 같은 커밋에서 삭제했다.

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 신규 | `pom.xml`, `mvnw` | Maven 기반 Spring Boot 3 프로젝트 스캐폴딩 |
| 신규 | `auth/*` | `AuthController`, `AuthService(Impl)`, `JwtUtil`, `JwtAuthenticationFilter` |
| 신규 | `document/*` | 벡터 검색용 CRUD (Controller/DTO/Model/Repository) |
| 신규 | `ai/*` | `AiService(Impl)` — 임베딩 생성 |
| 신규 | `common/*` | `ApiResponse`, `ErrorCode`, `AppException`, `GlobalExceptionHandler` |
| 신규 | `config/*` | `SecurityConfig`, `WebConfig` |
| 삭제 | NestJS 관련 파일 일체 | 같은 커밋에서 함께 제거 |

이후 `#2` ~ `#11` 커밋으로 이틀에 걸쳐 스칼라(API 문서) 설정, 세부 버그를 순차적으로 잡아나갔다. 마이그레이션이 끝난 직후 바로 `Application 개발 환경 세팅` → `FE Web Page #1` → `BE Web Page #1`로 이어지는 걸 보면, 프레임워크를 확정 짓고 나서야 실제 화면 기능 개발이 본격적으로 시작된 셈이다.

## ✅ 검증 및 결과

- [x] 마이그레이션 후 인증(JWT) 플로우 재검증
- [x] 벡터 검색(document) CRUD 재검증
- [x] Vercel 분리 이후 CORS 이슈 재발 없음 확인

## 🔗 참고

- 커밋 `fb19a7a` (마이그레이션 최초 커밋, 153 files changed)
- [[ReelTrip 개발 과정]]
- [\[기술\] 개발 환경 구성 및 협업 가이드](<../03_TechDocs/[기술] 개발 환경 구성 및 협업 가이드.md>)

> **회고**: "이관"보다는 "재작성"에 가까웠다 — 기존 코드를 최대한 재사용하기보다 Spring 관례에 맞게 새로 짜는 쪽을 택했다. 규모가 작은 초기 단계였기 때문에 가능했던 선택.
