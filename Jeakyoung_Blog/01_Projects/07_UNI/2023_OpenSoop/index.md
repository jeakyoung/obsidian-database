---
date: 2026-09-18
title: 23년 Open Soop
---

# 23년 Open Soop

대학교 재학생 대상 커뮤니티 앱. 학교 인증 기반 회원가입, 공지·일정·자유·질문건의·장터 5종 게시판, 익명 투표를 제공한다. React Native(모바일) + Java Servlet/MyBatis(API) 구조이고, 나는 BE 팀원으로 관리자용 게시판 모니터링 API를 맡았다.

## 기술 스택

| 영역                | 경로              | 기술                                                              |
| :---------------- | :-------------- | :-------------------------------------------------------------- |
| **Mobile FE**     | `OpenSoopFront` | React Native 0.72 (Expo 49), React Navigation                   |
| **API (내 담당 영역)** | `OpenSoopBack`  | Java 11, Servlet 3.1 (`@WebServlet`, web.xml 없음), MyBatis 3.5.6 |

### 데이터 계층 (`OpenSoopBack` 기준)

| 항목 | 내용 |
|:--|:--|
| **DB** | MariaDB |
| **ORM · 쿼리 매핑** | MyBatis — `/mybatis-config.xml`이 `/mappings/uni-*.xml` 5개를 등록. JPA/Hibernate 아님 |
| **서비스 계층** | 없음. Servlet이 요청 파라미터를 직접 파싱해 `*TtableOut`/`*process` 클래스(비즈니스 로직+DB 접근 겸용)를 호출 |
| **JSON 처리** | `net.sf.json`(json-lib) — Servlet이 요청 바디를 직접 읽어 `JSONObject.fromObject`로 파싱 |
| **인증** | 세션·토큰 프레임워크 없음. 로그인 성공 시 `LOGIN_ID + UUID`로 만든 문자열을 `TOKEN_ID`로 발급해 DB에 저장, 이후 요청에서 그대로 비교 |
| **메일 발송** | `javax.mail` — Gmail SMTP로 인증 메일 발송 |

> [!warning] DB 계정이 `database.properties`에 평문으로 커밋되어 있음
> MariaDB 접속 계정·비밀번호가 저장소에 그대로 들어있다. 학생 팀 프로젝트라 프로필 분리나 `.gitignore` 처리가 안 된 채로 남은 부분 — 문서에는 값을 옮기지 않는다.


## 문서 분류

- [[01_Projects/07_UNI/2023_OpenSoop/01_Tasks|작업 목록]] - 게시판 모니터링 페이지 구현
- [[01_Projects/07_UNI/2023_OpenSoop/02_Docs|프로젝트 문서]] - 프로젝트 개요, 개발 과정
- [[01_Projects/07_UNI/2023_OpenSoop/03_TechDocs|기술 문서]] - Servlet-Process-MyBatis 계층 구조, 게시판 모니터링 API 응답 구조와 한계
