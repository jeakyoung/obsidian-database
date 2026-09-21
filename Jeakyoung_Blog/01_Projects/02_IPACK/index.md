---
date: 2026-08-31
title: IPACK 근태 시스템
---

# IPACK 근태 시스템

ERP 근태 시스템 담당. `iPlusERP` (Sencha Ext JS + Java Servlet + MSSQL) 코드베이스의 인사(`HR/WHR1xx`)·근태(`HR/WHR3xx`) 모듈, 그리고 영업(`SA/WSA3xx~5xx`) 쪽 유지보수 요청을 같이 처리한다.

## 기술 스택

| 항목 | 내용 |
|:--|:--|
| **담당 업무** | ERP 근태 시스템 개발·유지보수 |
| **프론트엔드** | Sencha Ext JS — `WebContent/app/{view,controller,store}/<그룹>/<모듈그룹>/<폼번호>_{VW,CT,ST}.js` |
| **백엔드** | 순수 Java 서블릿(`HttpServlet`) + JDBC, 프레임워크 없음 — `src/com/<그룹>/<모듈그룹>/jv<폼번호>_*.java` |
| **데이터베이스** | MSSQL, 저장 프로시저 중심(`EXEC SP_...`) |

### 근태 모듈 (`HR/WHR300`)

| 폼번호 | 기능 | 비고 |
|:--|:--|:--|
| `WHR313` | 기간별 근태현황 | 저장 여부에 따라 `TIN313`(저장 완료)/`TIN334`(미저장) 두 경로를 참조한다는 기록이 있으나 코드에서는 확인 안 됨 |
| `WHR314` | 근무조별 일근태등록 | `WHR314_CT.js`(708줄)에 시간 반올림 함수(`convertToMinusHour` 등)와 `calRec`이 있음 |
| `WHR316` | 주차별 근무조 등록 | `WHR316_CT.js`(583줄) |
| `WHR320` | 근무종합집계 | `jvWHR320_01_LIST.java` → 실제 호출 SP는 `SP_WHR320_02_LIST` (파일명과 다름, 확인 완료) |
| `WHR103` | 증명서발급 | `jvWHR103_02_IUD.java` → `SP_WHR103_02_IUD` |

> [!warning] 서블릿이 파라미터를 문자열로 그대로 이어붙여 SP를 호출함
> 예: `jvWHR314_02_IUD.java`는 `PreparedStatement`를 쓰긴 하지만, SQL 문자열 자체를 `"EXEC SP_WHR314_TIN313D_IUD '" + value + "'"` 식으로 직접 이어붙여 만든 뒤 그 문자열을 그대로 실행한다(바인드 파라미터 아님). 작은따옴표만 `''`로 치환해서 방어하는 수준이라 구조적인 SQL Injection 패턴이다. 이 프로젝트 전반에서 반복되는 패턴으로 보이며, 고치라는 요청이 아니라 현재 상태 기록.

> [!warning] 근태구분 공통코드 21/22/23이 문서와 실제 코드에서 다르게 기록됨
> `WHR314_CT.js`(`calRec`, 296행)의 `dsCodeMapping`은 21=야간수당/22=특근(휴무일)/23=특근수당인데, 근태 공통코드 정의서 원본은 21=출장/22=산재/23=공상으로 되어 있다. 어느 쪽이 시스템 전체 기준인지는 DB의 공통코드 마스터를 직접 조회해야 확정 가능 — 자세한 내용은 [[01_Projects/02_IPACK/02_TechDocs/근태_1기본개념/[참고] IPACK 근태 구분 공통코드|근태 구분 공통코드]] 참고.

## 문서 분류

- [[01_Projects/02_IPACK/01_Tasks|작업 목록]] - 근태 기능 개발 및 유지보수, WHR316 주차별 근무조 등록 세부 이력
- [[01_Projects/02_IPACK/02_TechDocs|기술 문서]] - 근태 시스템 기술 스펙, 근태구분 공통코드, BioStar 연동, 유지보수 이력
- [[01_Projects/02_IPACK/03_Meetings|회의록]] - 인수인계 및 회의 기록
