---
date: 2026-08-31
title: 동방푸드 ERP
---

# 동방푸드 ERP

동방푸드마스타(식품 납품업체, 소스 제작) · 동방MS(Meat Solution, 육류가공) ERP 기술지원. iPlusERP(`iPlusERP_DONGBANG`) 기반 화면 조회조건 추가, 데이터 정합성 조치 위주. 자세한 조직·업무 흐름은 [\[업무\] 동방푸드 조직 구조 및 업무 프로세스](<04_References/[업무] 동방푸드 조직 구조 및 업무 프로세스.md>) 참고.

## 기술 스택

| 항목 | 내용/경로 |
|:--|:--|
| **담당 업무** | ERP 시스템 기술지원 |
| **프론트엔드** | Sencha Ext JS — `iPlusERP/WebContent/app/**` (MVC: `store`/`view`/`controller`) |
| **백엔드** | 순수 서블릿(`GenericServlet`) + JDBC, 프레임워크 없음 — `iPlusERP/src/com/**` |
| **데이터베이스** | MSSQL(`iPlusERP_DONGBANG`), 저장 프로시저 중심(`EXEC SP_...`) — SP 소스는 DB 안에만 존재, 코드베이스(SVN)에는 없음 |
| **형상관리** | SVN (`https://218.155.74.6/svn/DONGBANG`) |

> [!warning] 조회조건 파라미터가 서버에서 잘못 읽히는 버그 (WRD203)
> `jvWRD203_01_LIST.java`가 `PROC_STATUS`/`SALES_EMP_NO`/`PROC_GBN` 세 파라미터를 전부 `request.getParameter("PROC_GBN")`으로 읽는다 — 클라이언트가 보낸 `PROC_STATUS`/`SALES_EMP_NO` 값이 서버에서 버려지는 구조. 자세한 내용은 [\[기술\] 샘플요청서 담당자 조회조건 (WRD203)](<02_TechDocs/[기술] 샘플요청서 담당자 조회조건 (WRD203).md>) 참고.

> [!note] 접속 URL·계정 정보는 마스킹 유지
> 원본 작업노트에 ERP/POP 접속 URL과 계정 정보가 평문으로 남아있던 것을 문서화 과정에서 마스킹/제거했다. 자세한 내용은 [\[환경\] 동방푸드 시스템 구성 및 접속 정보](<04_References/[환경] 동방푸드 시스템 구성 및 접속 정보.md>) 참고.

## 문서 분류

- [[01_Projects/04_DongBang/01_Tasks|작업 목록]] - DB 반영, 발주, 출하 등 작업 기록
- [[01_Projects/04_DongBang/02_TechDocs|기술 문서]] - WMA202/WPR512/WSA411/WRD203 조회조건 기능 분석
- [[01_Projects/04_DongBang/04_References|참고 자료]] - 시스템 구성·접속 정보, 조직 구조 및 업무 프로세스
