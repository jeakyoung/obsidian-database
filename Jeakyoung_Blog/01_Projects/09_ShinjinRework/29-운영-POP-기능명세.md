---
title: 운영 POP 기능명세 및 이관 대조
date: 2026-11-26
draft: true
---

# 운영 POP 기능명세 및 이관 대조

원본은 운영 POP 소스 shinjin의 현행 작업 트리(HEAD 84aaa91), 대상은 ShinJin_POP_REWORK의 로컬 통합본(main 8a09e15 기반)이다. 기존 디자인과 업무 흐름을 인수 기준으로 삼는다. 원본과 다른 디자인이 필요한 경우 해당 시점에 운영자에게 원본·변경안과 이유를 제시한다.

| 기능 | 기존 로직과 화면 | React 및 Spring 적용 | 확인 및 남은 차이 |
| --- | --- | --- | --- |
| 로그인 | SJ_SM/frmLogin의 사원번호·비밀번호, 스캔 대화상자. 단말 설정과 등록 공정 수로 첫 화면을 선택한다. | DemoLogin, DemoSessionController. 일반 화면과 테스트 자격 안내를 분리하고 별도 JSON으로 단말을 설정한다. | 기본/대체 fixture 로그인 및 새로고침 확인. 운영 인증과 물리 스캐너의 초점은 현장 대조 대상. |
| 메뉴·공통 업무창 | MainMenu/frmMenu의 5개 분류와 설정별 타일. frmMain에 회사·담당자·홈·로그아웃과 로그아웃 확인이 있다. | App의 인증 헤더, 실제 PNG, 상태별 메뉴 진입과 확인 대화상자. 물류·RFID는 작업별 진입점을 제공한다. | 단말별 전체 권한 매핑과 작업 중 화면 이탈 조건 대조. |
| 작업지시·실적 | frmProcess1의 작업 명령, 선택한 지시, 공정 진행, 투입·반납 그리드. SP_POP_REG_PROCESS1_01_LIST와 바인딩 인수 확인. | WorkOrders·WorkOrderController. 선택행과 명령 상태, 수량 키패드, 계획 조회·자재 상세를 제공한다. | 단일 지시의 시작·중지·재개·완료, 합성 LOT 투입·반납 확인. 원본 전표 대사 및 일괄작업은 별도 인수. |
| 그룹 작업 | frmMenu의 005/105 분기, frmProcess5의 그룹 순서와 계획별 실적 | ProcessGroupController와 ProcessGroupDemo. 인증 단말 설정으로 진입. | 기본/대체 데이터에서 그룹 노출, 다른 단말의 접근 거절 및 단일 슬롯 진입 확인. |
| 도면가공·포장 | frmProcess7·frmProcess6 및 선행 길이절단의 상태·재고·전표 연결 | DrawingWork, DrawingGroupWork, DrawingController. 단건·묶음 및 미확정 요청 복구. | 동시 잔재 배분과 응답 유실·재로그인 회귀 확인. 도면가공 메뉴 전체 및 부분 포장·완료 취소의 원본 일치는 별도 판정. |
| 설정 | SJ_SM/frmLogin의 톱니바퀴가 POPSYS/frmSetting을 연다. 사업장·공정의 저장 시점마다 종속 설정을 초기화한다. | 로그인 전 단말 선택 및 9개 상세 설정을 제공한다. 브라우저와 단말의 파일에 저장하고 사원 로그인 시 업무에 적용한다. | 빈 설정에서 최초 등록·재시작·단말 격리, 005/105 그룹과 단계별 창고를 검증했다. [[31-시스템-설정-기능명세]] |
| 출력·계획 | POPPRINT/frmWorkPrint, 사원 바코드, REPORT의 개별 양식과 생산계획·출력 횟수 | Planning, OutputPreview, PlanningOutputController 등. | 합성 단일/복수 PDF와 오류 시 횟수 보존 확인. 원본 보고서별 레이아웃·인쇄 장치 대조 필요. |

## 검증 데이터와 접속 경계

별도 데이터셋 및 재현 절차는 전환 레포의 tools/demo-dataset/README.md에 있다. 동일한 웹 번들에서 기본 JSON과 대체 JSON을 바꾸어 비어 있는 이력과 1건 이력, 단말별 첫 화면, 작업자 격리를 대조한다. 실제 MSSQL에 배포된 프로시저·함수·트리거 생성·수정·삭제는 이관 범위에서 금지한다. SQL 텍스트가 확인된 경우에도 해당 버전의 내부 분기와 트리거 부작용을 대조하기 전까지 Spring에서 이중 구현하지 않는다.

[[30-Spring-API-명세]]

- [[31-시스템-설정-기능명세]]

- [[32-공통팝업-기능명세]]

- [[33-물류-RFID-관리-인쇄-기능명세]]

- [[34-생산-보고서-기능명세]]

## 2026-11-26 · 디자인 결정

원본 소스에서 근거를 확인한 복원은 진행한다. 화면 배치·색·라벨·아이콘·상세 설정·버튼 동작을 원본과 다르게 정해야 하면 결정 전에 운영자에게 차이와 이유를 제시한다. 승인한 예외는 웹 POP 프로그램 자체의 종료(X) 생략이다. 창 내부의 닫기, 편집 취소, 로그아웃은 각각 원본의 기능으로 유지한다.
- 최신 사용자 결정으로 인쇄는 원본 호출별 동작을 따른다. 사원번호 바코드·QR과 수동 작업지시서는 Printer1을 설정한 뒤 미리보기를 연다. 출하 거래명세서는 Printer2를 사용하며 수동 미리보기와 자동 직접 출력 경로가 따로 있다. 모든 출력을 브라우저 인쇄창으로 통일하지 않는다. 실물 장치 연동 방식은 미정이다. 프로그램 종료(X) 생략 승인은 유지한다.

데모에서 요청한 로그인 편의 기능으로 스캔 창에 0000을 입력하면 선택 단말의 관리자 샘플 계정으로 입장한다. 사번과 비밀번호 입력란 및 터치 키패드는 각각 붙여넣기를 지원한다.

사용자 승인에 따라 웹 로그인·사원번호 인쇄·작업지시서 인쇄 화면은 사용할 수 있는 창 크기에 맞춰 입력란과 버튼을 배치한다. 출력물의 원본 용지 크기와 바코드·QR 양식을 유지한다.

## 2026-11-26 공개 합본 검수

공개 조합은 JAR `d8ce00bca93d…`, 웹 `index-D47DWB9a.js`, CSS `index-BnBwCRHc.css`이다. 008 작업 전 수동 + 및 재고이동 위치 재스캔 포커스 복원, 005·105와 008 투입자재 스캔, 003·103 반납 추가와 005 불량이력을 확인했다. 003·103 투입/반납 체크행 삭제와 재입장, 그룹 공정 하위창 취소/X 뒤 부모 조회, 다른 브라우저에서 먼저 완료한 설비 호출의 복귀를 반영했다. 006/106 포장 15자리 목록·16자리 수주/규격, 001 투입자재 위치스캔의 낮은 창 닫기, 그룹 등록부 수정 후 기존 단말 배정 보존을 확인했다. 로그인 전 톱니바퀴에서 현재 단말의 9개 설정을 편집한다. POP A는 003 참조 단말이고 그룹은 별도 합성 POP A2의 P1·005 또는 105에서 확인한다. 기존 주소에서 로그아웃 후 새로고침하거나 새 시크릿 창을 사용한다. [15179 통합 POP](http://127.0.0.1:15179/) · [데이터셋별 검증과 절차](file:///E:/ajk/devgit/shinjin/.team/menu-screen/README.md)

원본 폼·보고서 107개 각각의 진입, 조건, 미구현, 검수 자료는 [원본 107개 대조표](file:///E:/ajk/devgit/shinjin/.rework-visual-qa/final-107.md)에서 확인한다. 해당 분류는 검사 당시의 단말 설정·데이터·인증 상태에서 어느 화면을 열 수 있었는지를 나타낸다. 저장·취소·재조회·인쇄 등 개별 이벤트 검수는 행별 증거를 따른다.

| 확인할 항목 | 실제 화면·기록 |
| --- | --- |
| 원본 화면 및 설정·데이터별 진입 조건 | [상태별 원본·웹 자료](file:///E:/ajk/devgit/shinjin/.rework-visual-qa/coverage.md) · [담당자별 실행 근거](file:///E:/ajk/devgit/shinjin/.rework-visual-qa/owner-evidence.md) |
| 생산 명령·스캔·투입·반납·계획 팝업 | [원본과 웹 캡처 비교](file:///E:/ajk/devgit/shinjin/.rework-production-visual-staging/비교-캡처.html) · [생산별 검사 조건](file:///E:/ajk/devgit/shinjin/.rework-production-visual-staging/시각-QA-인계.md) |
| 공개판 메뉴·로그인·사원번호·작업지시서 인쇄 | [1280×800 메뉴](file:///E:/ajk/devgit/shinjin/.team/menu-screen/15179-current/menu-1280x800.png) · [1024×768 로그인](file:///E:/ajk/devgit/shinjin/.team/menu-screen/15179-current/login-1024.png) · [사원번호](file:///E:/ajk/devgit/shinjin/.team/menu-screen/15179-current/employee-1024.png) · [작업지시서](file:///E:/ajk/devgit/shinjin/.team/menu-screen/15179-current/work-print-1024.png) · [다섯 양식의 18쪽 PDF 용지 실측](file:///E:/ajk/devgit/shinjin/.team/menu-screen/15179-current/report-paper.tsv) |
