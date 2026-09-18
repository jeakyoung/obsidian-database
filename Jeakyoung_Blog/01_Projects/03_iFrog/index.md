---
date: 2026-09-18
title: I-Frog
---

# I-Frog

그룹웨어·ERP 연동 백엔드 API(F1Soft.Starmap.Service) 개발 담당. 결재/게시판/일정/공지 등 그룹웨어 기능과 SAP·생산현황(MES) 연동, FCM 푸시를 하나의 ASP.NET Core 서비스로 제공.

## 기술 스택

| 항목 | 내용 |
|:--|:--|
| **담당 업무** | 그룹웨어 + ERP 연동 백엔드 API 개발 |
| **백엔드** | C# / ASP.NET Core (`F1Soft.Starmap.Service`) |
| **데이터베이스** | MSSQL (그룹웨어/ERP), PostgreSQL (통합서버), Oracle 조회 지원 |
| **외부 연동** | SAP RFC(`Controllers/Interface/Sap`), Firebase Cloud Messaging |
| **웹 서버** | NginX |

### 도메인 구성 (`Controllers/` 기준)

| 영역 | 경로 | 내용 |
|:--|:--|:--|
| **Auth / Users** | `Auth`, `Users` | 로그인(ATC/SYN 전략), 토큰 발급 |
| **Groupware** | `Groupware/Approval`, `Board`, `Calendar`, `Emp`, `Notice`, `WorkStatus` | 결재, 게시판, 일정, 직원, 공지, 업무현황판(생산현황) |
| **Notification** | `Notification/FcmController` | FCM 발송·수신 이력, 업무연락 알림 |
| **Interface** | `Interface/Sap` | SAP RFC 연동 |
| **Database** | `Database/{Oracle,PostgreSQL,SQLServer}` | 원시 쿼리/프로시저 실행 컨트롤러 |
| **Setting** | `Setting` | 사용자·회사 설정 |

> [!note] 멀티테넌시
> 요청 헤더의 보안 코드(SECURITY_CODE)로 회사(Ticker)와 DB 환경(Dev/Stg/Prd)을 구분해 `EnvService`가 연결 문자열을 동적으로 선택하는 구조. 배포는 하나지만 여러 회사·환경을 동시에 서비스함.

> [!note] `F1Soft.Starmap.Core`는 아직 미사용
> `IApprovalService`, `IEnvService` 등 인터페이스가 존재하지만 `F1Soft.Starmap.Service`에서 프로젝트 참조·사용 이력이 없는 빈 스텁 상태. 공용 코드가 있다고 가정하지 말 것.

## 문서 분류

- [[01_Projects/03_iFrog/01_Tasks|작업 목록]] - FCM, CORS, 결재/업무현황 파라미터 추가, 배포 등 작업 기록
- [[01_Projects/03_iFrog/02_TechDocs|기술 문서]] - 서버 통합, 환경 설정, 교육 자료
- [[01_Projects/03_iFrog/03_Meetings|회의록]] - 업무 미팅 기록
- [[01_Projects/03_iFrog/04_References|참고 자료]] - 명령어, 설정값 등 참고 자료
