---
date: 2026-09-18
title: 2024 평택대학교앱 리워크
---

# 2024 평택대학교앱 리워크

평택대학교 공식 모바일 앱을 대체하기 위해 팀 단위로 처음부터 다시 만든 학교 앱. React Native(모바일) + Spring Boot(API) 구조이고, 나는 BE 팀장 겸 PL로 API 서버 전체를 맡았다.

## 기술 스택

| 영역 | 경로 | 기술 |
|:--|:--|:--|
| **Mobile FE** | `4th_GraduationFront` | React Native 0.73 (TypeScript, React Navigation) |
| **API (내 담당)** | `4th_GraduationBack` | Spring Boot 3 (Java 17), Spring Data JPA |

### 데이터 계층 (`4th_GraduationBack` 기준)

| 항목 | 내용 |
|:--|:--|
| **DB** | MariaDB (AWS RDS) |
| **ORM** | Spring Data JPA — 대부분 메서드 이름 기반 쿼리, 일부만 `@Query` 네이티브 SQL |
| **인증** | 세션·토큰 없음. 클라이언트가 서버 발급 SALT로 비밀번호를 해싱해 전송하고, 서버는 저장된 값과 단순 비교 |
| **이미지 저장** | 서버 로컬 디스크(`/var/www/ptu/uploads`) + 날짜별 디렉토리, Base64 → `.webp` 변환 저장 |
| **메일 발송** | Spring Mail (Gmail SMTP) — 이메일 인증 코드 발송 |

> [!warning] 커넥션 정보가 `application.properties`에 평문으로 커밋되어 있음
> DB 계정, RDS 호스트, Gmail SMTP 앱 비밀번호가 전부 저장소에 그대로 들어있다. 팀 프로젝트 특성상 정리가 안 된 채로 남은 부분 — 문서에는 값을 옮기지 않는다.


## 문서 분류

- [[01_Projects/99_UNI/2024_PaekTaekApp/01_Tasks|작업 목록]] - 회원가입 다단계 분리·SALT 도입, 이미지 업로드 구조, 이메일 인증, DB FK 제약조건, Git 병합 오류
- [[01_Projects/99_UNI/2024_PaekTaekApp/02_Docs|프로젝트 문서]] - 프로젝트 개요, 개발 과정
- [[01_Projects/99_UNI/2024_PaekTaekApp/03_TechDocs|기술 문서]] - 3계층 구조, SALT 인증 흐름, 이미지 저장 구조, 게시판 CRUD 패턴
