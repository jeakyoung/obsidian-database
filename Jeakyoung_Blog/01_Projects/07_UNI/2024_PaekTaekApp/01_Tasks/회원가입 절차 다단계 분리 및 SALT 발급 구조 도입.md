---
title: 회원가입 절차 다단계 분리 및 SALT 발급 구조 도입
date: 2026-09-18
type: 작업
project: 대학프로젝트
status: 완료
priority: 높음
assignee:
  - 안재경
tags: []
---

# 회원가입 절차 다단계 분리 및 SALT 발급 구조 도입

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 본인 (BE 팀장) |
| **요청일** | 2024-06 |
| **대상 시스템** | `4th_GraduationBack` — `RegiController`, `RegiService` |
| **관련 화면·프로그램** | `POST /PTU/Register/*`, `POST /getSalt` |

> 회원가입을 한 번에 처리하면 중복확인 실패를 마지막에서야 알려주는 문제가 있어, ID → 학번 → 이메일 → 기본정보(SALT 발급) → 최종정보 순으로 단계를 쪼갰다.

## 🔍 현상 및 원인

### 재현 조건

회원가입 폼에서 ID·학번·이메일을 전부 입력하고 제출한 뒤에야 서버가 일괄로 중복 여부를 검사하는 구조였다.

### 원인

`RegiController`/`RegiService`가 하나의 엔드포인트로 회원 정보를 통째로 받아 저장하던 구조라, 중복된 값이 있으면 사용자는 화면 맨 처음부터 다시 입력해야 했다. UX상 각 필드를 입력하는 시점에 바로 중복 여부를 알려줄 필요가 있었다.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 컨트롤러 | `RegiController` | `/PTU/Register/ID`, `/StdNum`, `/Mail`, `/basic-info-save`, `/StdInfo` 5개 엔드포인트로 분리 |
| 서비스 | `IdRegiService` / `StdRegiService` / `MailRegiService` | 각각 `existsByMembId`/`existsByStdNum`/`existsByEmail`만 확인하는 단일 책임 서비스로 분리 |
| 서비스 | `RegiService.basicRegiUserData` | 학과명 → 학과코드 변환(`DepartmentRepository.findByMembDep`), `SecureRandom` 16바이트 SALT 생성·저장 후 `BasicUserDataSave`(RSLT_CD/MEMB_ID/SALT)로 응답 |
| 서비스 | `RegiService.completeRegistration` | 기존 `stu_info` 레코드를 조회해 이메일·비밀번호(클라이언트에서 SALT로 해싱된 값)만 채워 최종 저장 |
| 모델 | `RegiModel` | `stu_info` 테이블 매핑, `salt` 컬럼 추가 (`@JsonProperty`로 `MEMB_ID`/`STD_NUM`/`EMAIL`/`PASS`/`STD_DEP_CD`/`NAME`/`SALT` 직렬화) |

```java
// RegiService.basicRegiUserData — 학과코드 변환 + SALT 발급
DepartMentCodeModel department = departmentRepository.findByMembDep(membDep)
        .orElseThrow(() -> new IllegalArgumentException("Invalid department name: " + membDep));
regiData.setStdDepCd(department.getStdDepCd());

byte[] saltBytes = new byte[16];
random.nextBytes(saltBytes);
String salt = Base64.getEncoder().encodeToString(saltBytes);
regiData.setSalt(salt);
```

발급된 SALT는 이후 로그인 시 `GET /getSalt`(`StuInfoController`)로도 다시 조회할 수 있다 — 프론트가 로그인 폼에서 비밀번호를 서버로 보내기 전 이 SALT로 해싱하기 위함이다. 인증 흐름 전체 설계는 [\[기술\] SALT 기반 로그인 인증 흐름](<../03_TechDocs/[기술] SALT 기반 로그인 인증 흐름.md>) 참고.

## ✅ 검증 및 결과

- [x] ID/학번/이메일 각 단계에서 중복 시 해당 단계에서 바로 에러 코드 반환 확인
- [x] `basic-info-save` 단계에서 학과명이 유효하지 않으면 `IllegalArgumentException` → `GlobalExceptionHandler`가 `RSLT_CD 99`로 변환해 응답하는 것 확인
- [x] `completeRegistration` 시 `existingData`가 없으면(=`basic-info-save`를 안 거쳤으면) `RSLT_CD 03` 반환 확인

## 🔗 참고

- [[평택대학교앱 리워크 개발 과정]]
- [\[기술\] SALT 기반 로그인 인증 흐름](<../03_TechDocs/[기술] SALT 기반 로그인 인증 흐름.md>)
- [\[기술\] Controller-Service-DAO 3계층 구조](<../03_TechDocs/[기술] Controller-Service-DAO 3계층 구조.md>)
