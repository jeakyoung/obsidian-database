---
title: Controller-Service-DAO 3계층 구조
date: 2026-09-18
type: 기술문서
project: 대학프로젝트
status: 완료
category: 아키텍처
assignee:
  - 안재경
tags: []
---

# Controller-Service-DAO 3계층 구조

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | `4th_GraduationBack` (Spring Boot 3, Java 17) |
| **적용 범위** | 아키텍처 |
| **관련 모듈** | `controller/`, `service/`, `dao/`, `model/`, `repository/`, `config/`, `exception/` |

> `Controller → Service → DAO(JpaRepository) → MariaDB` 3계층 구조. 패키지가 전부 `com.example.Lee` 밑에 있고, 도메인이 아니라 계층 기준으로 나뉜다.

## 🎯 배경 및 요구사항

MVC 패턴을 그대로 따라가되, 팀 프로젝트 규모(백엔드 1~2인)에 맞춰 도메인별 패키지 분리 없이 계층별 패키지 하나씩만 두는 단순한 구조로 시작했다.

## 🏗 설계 및 구현

### 디렉토리 구조 (실제 코드 기준)

```
src/main/java/com/example/Lee/
├── controller/    # @RestController — 요청 파싱, 서비스 호출, ResponseEntity 반환
├── service/       # @Service — 비즈니스 로직, DAO/Repository 조합
├── dao/           # JpaRepository 확장 인터페이스 (게시판·회원 도메인)
├── repository/    # JpaRepository 확장 인터페이스 (학과 코드·이메일 인증 도메인)
├── model/         # @Entity + 일부 순수 응답 DTO 혼재
├── config/        # CorsConfig, ObjectMapperConfiguration
├── exception/     # GlobalExceptionHandler, ResourceNotFoundException
└── LeeApplication.java
```

> [!note] 계획과 실제 구현이 다른 부분
> 초기 설계 문서에는 `security/` 패키지가 있었으나 실제 코드에는 존재하지 않는다 — 인증은 세션/JWT 없이 [\[기술\] SALT 기반 로그인 인증 흐름](<[기술] SALT 기반 로그인 인증 흐름.md>)에 정리한 방식으로만 처리된다.

`dao`와 `repository`는 이름만 다를 뿐 둘 다 `JpaRepository`를 확장하는 동일한 성격의 인터페이스다 — 게시판·회원 관련은 `dao` 패키지에, 학과 코드(`DepartmentRepository`)·이메일 인증(`EmailAuthRepository`)은 `repository` 패키지에 있다. 두 패키지를 나눈 기준이 코드상 명확하지 않다(도메인·시점에 따라 갈린 것으로 보인다).

### 요청 처리 흐름 (예: 학사안내 등록)

```
POST /PTU/Bachelor/add
  → BachelorCheckController.createBachelor()      // MEMB_ID/TIT/CONT/IMAGE 파싱, null 체크
  → BachelorCheckService.saveBachelor()            // @Transactional, 이미지 저장 위임
  → ImageFileUploadSystem.saveImageFile()          // Base64 → .webp 저장
  → BachelorCheckDao.save()                        // JpaRepository, bachelor_list 테이블
  → CommonResponseModel(RSLT_CD)                   // 00/01/02 코드만 반환
```

네 게시판(공지/학사/입학/장학) 모두 이 흐름을 거의 동일하게 반복한다 — 자세한 패턴은 [\[기술\] 게시판 4종 CRUD 패턴과 예외·CORS 처리](<[기술] 게시판 4종 CRUD 패턴과 예외·CORS 처리.md>).

### 응답 모델

전용 `ApiResponse<T>` 봉투 없이, 대부분 `CommonResponseModel`(성공/실패 코드 `RSLT_CD` 하나만 담음) 아니면 도메인별 커스텀 응답 모델(`LoginRsltModel`, `SaltResponseModel`, `BasicUserDataSave`)을 직접 반환한다. `RSLT_CD` 값의 의미는 컨트롤러/서비스마다 로컬로 정의돼 있고(예: 회원가입은 `01`=ID중복, `02`=학번중복, `03`=기본정보 없음), 전역으로 통일된 코드 체계는 없다.

## ✅ 검증

- [x] 게시판 4종·회원가입·로그인·이메일인증 전 엔드포인트가 동일한 3계층 흐름을 따르는지 코드 확인
- [ ] `dao`/`repository` 패키지 분리 기준 문서화 (현재는 코드에서 역추적한 추정)

## 🔗 참고

- [[평택대학교앱 리워크 프로젝트 개요]]
- [\[기술\] 게시판 4종 CRUD 패턴과 예외·CORS 처리](<[기술] 게시판 4종 CRUD 패턴과 예외·CORS 처리.md>)
