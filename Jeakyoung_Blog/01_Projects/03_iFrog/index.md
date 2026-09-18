---
date: 2026-09-18
title: I-Frog
---

# I-Frog

F1Soft.Starmap.Service 백엔드 개발 담당. 합류 당시 기본 틀(프로젝트 구조, EnvService 멀티테넌시 패턴)은 이미 잡혀있었고, 그 위에 Approval·Board·Calendar 세 개만 대략 구현되어 있던 상태였음. 이 세 개도 전부 다시 손봤고, WorkStatus(업무현황판)·FCM·SAP 연동·Setting·Notice·Emp·DB 원시쿼리 컨트롤러 등 나머지는 전부 직접 만든 것.

## 기술 스택

| 항목 | 내용 |
|:--|:--|
| **담당 업무** | 그룹웨어 + ERP 연동 백엔드 API 개발 |
| **백엔드** | C# / ASP.NET Core (`F1Soft.Starmap.Service`) |
| **데이터베이스** | MSSQL (그룹웨어/ERP), PostgreSQL (통합서버), Oracle 조회 지원 |
| **외부 연동** | SAP RFC(`Controllers/Interface/Sap`), Firebase Cloud Messaging |
| **웹 서버** | NginX |

### 도메인 구성 (`Controllers/` 기준)

| 영역 | 경로 | 내용 | 비고 |
|:--|:--|:--|:--|
| Groupware - Approval | `Groupware/Approval` | 결재 | 기존 뼈대 있던 것 → 대부분 재작업 |
| Groupware - Board | `Groupware/Board` | 게시판 | 기존 뼈대 있던 것 → 재작업 |
| Groupware - Calendar | `Groupware/Calendar` | 일정 | 기존 뼈대 있던 것 → 재작업 |
| Groupware - 나머지 | `Groupware/{Emp,Notice,WorkStatus}` | 직원, 공지, 업무현황판(생산현황) | 직접 구현 |
| Auth / Users | `Auth`, `Users` | 로그인(ATC/SYN 전략), 토큰 발급 | 직접 구현 |
| Notification | `Notification/FcmController` | FCM 발송·수신 이력, 업무연락 알림 | 직접 구현 |
| Interface | `Interface/Sap` | SAP RFC 연동 | 직접 구현 |
| Database | `Database/{Oracle,PostgreSQL,SQLServer}` | 원시 쿼리/프로시저 실행 컨트롤러 | 직접 구현 |
| Setting | `Setting` | 사용자·회사 설정 | 직접 구현 |

> [!note] 멀티테넌시
> 요청 헤더의 보안 코드(SECURITY_CODE)로 회사(Ticker)와 DB 환경(Dev/Stg/Prd)을 구분해서 `EnvService`가 연결 문자열을 골라주는 구조. 배포 하나로 여러 회사·환경을 같이 돌림.

> [!note] `F1Soft.Starmap.Core`는 아직 안 씀
> `IApprovalService`, `IEnvService` 인터페이스가 들어있긴 한데 `F1Soft.Starmap.Service` 쪽에서 참조도 안 하고 쓴 적도 없음. 공용 코드 있는 줄 알고 찾지 말 것.

## 문서 분류

- [[01_Projects/03_iFrog/01_Tasks|작업 목록]] - FCM, CORS, 결재/업무현황 파라미터 추가, 배포 등 작업 기록
- [[01_Projects/03_iFrog/02_TechDocs|기술 문서]] - 서버 통합, 환경 설정, 교육 자료
- [[01_Projects/03_iFrog/03_Meetings|회의록]] - 업무 미팅 기록
- [[01_Projects/03_iFrog/04_References|참고 자료]] - 명령어, 설정값 등 참고 자료
