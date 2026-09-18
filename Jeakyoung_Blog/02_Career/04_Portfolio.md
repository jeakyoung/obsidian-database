---
title: 포트폴리오 - 안재경
date: 2026-09-18
type: 경력문서
status: 진행중
tags: []
---

# 포트폴리오 - 안재경

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **작성일** | 2026-09-18 |
| **소속·역할** | F1soft 솔루션사업팀 · ERP/MES 백엔드, 모바일 백엔드 API |
| **주요 기술** | Java, Sencha Ext JS, C# .NET Core, MSSQL, PostgreSQL, MariaDB |

## 🧭 경력 요약

F1soft에서 여러 고객사의 ERP·MES 시스템과 모바일 백엔드 API를 개발하며, 개인 프로젝트([[01_Projects/06_ReelTrip|ReeL-Trip]])를 병행하고 있습니다. 아래 프로젝트별 상세 내용은 실제 코드 경로와 모듈명을 기준으로 정리했습니다.

## 🛠 주요 수행 내용

### Project 1: 신진SM ERP/MES — 더존 ERP 연동 정합성

| 항목 | 내용 |
|:--|:--|
| **기간** | 2026.04 ~ 진행중 |
| **역할** | MES 개발 |
| **기술 스택** | Sencha Ext JS, Java 서블릿, MSSQL, 더존 ERP 연동(`NEOE.*` 프로시저) |

**구조**

신진SM MES는 저장이 확정되면 별도 JDBC 커넥션(web.xml의 `urlDZ`/`usernameDZ`/`passwordDZ`)으로 더존 ERP DB에 직접 연결해 `NEOE.*` 스토어드 프로시저를 호출하는 방식으로 데이터를 반영합니다. 이 두 저장이 하나의 트랜잭션이 아니라서, "MES 저장 확정 → 더존은 best-effort로 반영"되는 구조입니다.

**대응한 문제들**

- **포장 중복 → 더존 마이너스 재고**: MES 프로시저 레벨에서는 중복이 이미 제한되어 있었지만, 더존 연동부에서 중복이 발생하는 걸 확인. `SP_WPR559_02_IUD_TEST`에 `@ISEXISTS_OUT` OUTPUT 파라미터를 추가하고 `ProdReportService`/`ProdSLService`가 이 값을 보고 더존 문서 재생성을 생략하도록 수정
- **더존-MES 사업장 코드 매핑**: 재고조정 화면의 사업장 `1000` 하드코딩 문제를 계기로 12개 사업장 전체 매핑을 검증 쿼리로 확인
- **더존 월말 재고 집계 불일치**: `MM_OHSLINVM`(월별 집계)과 `MM_OHSLINVD`(일별 상세)가 어긋나는 사례를 탐지 → 세부 확인 → UPDATE 3단계 절차로 표준화 (프로시저 재실행은 `MM_PINVN` 이중 반영 위험이 있어 금지)

> 아직 남은 문제: 포장 단독 생산 시 창고코드가 `ProdSLService.java`에서 무조건 출하창고로 고정되는 버그는 확인만 됐고 미수정 상태입니다. 자세한 내용은 [[01_Projects/01_ShinJinSM/05_Docs/신진SM 개발 이력|신진SM 개발 이력]] 참고.

---

### Project 2: IPACK 근태 시스템 — 시간 계산 로직 및 근태 기능

| 항목 | 내용 |
|:--|:--|
| **기간** | 2025 ~ 진행중 |
| **역할** | 근태 기능 개발·유지보수 |
| **기술 스택** | Sencha Ext JS, Java 서블릿, MSSQL(저장 프로시저) |

**시간 계산 반올림 규칙**

근태 계산(`WHR314_CT.js`)에서 항목마다 반올림 방향이 다릅니다:

```javascript
// 지각/조퇴 — ceil(올림, 불리하게)
convertToMinusHour: function (rawTime) {
    // ...
    var minutes = Math.round((num - hours) * 100);
    minutes = Math.ceil(minutes / 10) * 10;
    // ...
}

// 초과근무 — floor(내림, 불리하게)
convertToPlusHour: function (rawTime) {
    // ...
    var minutes = Math.round((num - hours) * 100);
    minutes = Math.floor(minutes / 10) * 10;
    // ...
}
```

10분 단위로 일관되게 처리하도록 정리했고, 지각/조퇴/초과근무 각각 어느 쪽으로 반올림해야 하는지(직원에게 불리한 방향으로 통일) 파악하는 게 핵심이었습니다.

**주차별 근무조 등록(WHR316) 기능 구현**

근무조 일괄적용/변환, 근태 년-월·주차 콤보 조회조건, 사원명 LIKE 검색 등을 단계적으로 구현했습니다. 상세 이력은 [[01_Projects/02_IPACK/02_TechDocs/근태_2기능스펙/[기술] WHR316 주차별 근무조 등록|WHR316 기술 스펙]] 참고.

> 이 시스템의 서블릿(`jv*.java`)은 SQL을 `"EXEC SP_... '" + value + "'"` 형태로 문자열 결합해서 실행합니다. 작은따옴표만 이스케이프하는 수준이라 구조적인 SQL Injection 패턴이라는 걸 이번에 문서화하면서 확인했습니다 — 아직 고치지는 않은 상태이고, 사실로만 기록해둡니다.

---

### Project 3: I-Frog — 그룹웨어/ERP 연동 백엔드, 서버 통합

| 항목 | 내용 |
|:--|:--|
| **기간** | 2026.06 ~ 진행중 |
| **역할** | 백엔드 개발, 서버 통합 설계 |
| **기술 스택** | C# .NET Core(`F1Soft.Starmap.Service`), MSSQL/PostgreSQL, NginX, Firebase Cloud Messaging |

합류 당시 Auth/Approval/Board/Calendar/Emp의 기본 틀은 있었고(업체마다 서비스 코드를 커스터마이징해서 그 업체 서버에 따로 얹는 방식), Approval·Board·Calendar는 다시 손봤습니다. 이후 진행한 **서버 통합**(업체별 커스텀 서버 → 단일 백엔드)은 직접 설계·구현했습니다.

**멀티테넌시 구조**

요청 헤더의 보안 코드(SECURITY_CODE)로 회사(Ticker)와 DB 환경(Dev/Stg/Prd)을 구분해서 `EnvService`가 연결 문자열을 골라주는 구조. 배포 하나로 여러 회사·환경을 같이 운영합니다.

**FCM 알림**

업무연락 알림, 결재함 문서 알림에 Firebase Cloud Messaging을 연동했습니다.

**기타**

SAP RFC 연동(`Controllers/Interface/Sap`), 원시 쿼리/프로시저 실행 컨트롤러(Oracle/PostgreSQL/SQLServer) 구현.

---

### Project 4: ReeL-Trip — 개인 프로젝트, 풀스택

| 항목 | 내용 |
|:--|:--|
| **기간** | 2026.02 ~ 진행중 |
| **특성** | 개인 프로젝트 (회사 업무와 무관) |
| **기술 스택** | Turborepo 모노레포 · Next.js 15(Web) + React Native/Expo(Mobile) + Spring Boot 3(API) · PostgreSQL(Supabase), MyBatis, Flyway, pgvector |

여행 콘텐츠 링크(유튜브 쇼츠/인스타그램 릴스)를 던지면 파싱해서 장소 후보로 자동 등록해주는 서비스. Web/Mobile/API 세 개를 혼자(+합류한 팀원들) 힘으로 같이 굴리고 있습니다.

**백엔드 프레임워크 마이그레이션**

NestJS로 시작했다가 CORS/배포 이슈를 겪으면서 Spring Boot 3 + MyBatis로 갈아엎었습니다. 프론트/백엔드 런타임을 물리적으로 분리하는 게 처음부터 맞는 선택이었다는 걸 이 과정에서 배웠습니다.

**URL 파서 — 플랫폼별 수집 전략**

`ContentCollector` 인터페이스를 두고 유튜브 쇼츠는 공식 oEmbed API + 자체 스크래핑(무료), 인스타그램 릴스는 Apify 액터 호출(유료, `run-sync-get-dataset-items`)로 처리하는 전략 패턴을 구현했습니다. 수집한 콘텐츠는 플랫폼 구분 없이 동일한 형태(`RawCollectedContent`)로 맞춰서 AI(Gemini)에게 넘겨 장소/카테고리/가격 등을 추출합니다.

**인증 — 리프레시 토큰 회전**

액세스 토큰 수명을 24시간에서 30분으로 줄이고, DB에 저장한 리프레시 토큰(30일)으로 재발급받는 구조로 전환했습니다.

**아직 안 된 것**

- 테스트 코드 없음 (Dockerfile도 `-DskipTests`로 빌드)
- AI 추천 섹션(`AiScreen`)이 아직 더미 데이터로 남아있음 — Spring 쪽에 추천 API가 없어서 방향 미정

상세 진행 과정은 [[01_Projects/06_ReelTrip/02_Docs/ReelTrip 개발 과정|ReelTrip 개발 과정]] 참고.

## 🏆 성과 및 역량

| 영역 | 경험 |
|:--|:--|
| **Java / 서블릿** | ERP·MES 백엔드 (신진SM, IPACK) — 프레임워크 없는 코드베이스 유지보수 |
| **C# .NET Core** | 모바일 백엔드 API (I-Frog) — 멀티테넌시 구조 설계, FCM 연동 |
| **MSSQL** | 저장 프로시저 중심 시스템에서의 데이터 정합성 문제 분석 |
| **Spring Boot 3** | 개인 프로젝트(ReeL-Trip)에서 마이그레이션·설계 경험 |
| **시스템 연동** | MES↔더존ERP 비동기 연동 문제 분석 및 개별 방어 로직 구현 |

## 🔗 참고

- [[01_Technical_Skills|경력기술서]]
- [[02_Resume|이력서]]
- [[03_CoverLetter|자기소개서]]
- [[01_Projects|전체 프로젝트 목록]]
