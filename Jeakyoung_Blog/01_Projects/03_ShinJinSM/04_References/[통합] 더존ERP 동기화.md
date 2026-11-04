---
title: 더존 ERP와의 데이터 동기화 방식
date: 2026-06-11
type: 참고자료
project: 신진SM
status: 진행중
category: 통합
tags: []
system: 더존(DZ) ERP / 신진SM ERP
---

# 더존 ERP와의 데이터 동기화 방식

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **용도** | MES/신진SM ERP(TMA536) 입출고를 더존(DZ) ERP 수불 체계로 반영 |
| **대상 시스템** | `src/com/MA/WMA620/jvWMA624_01_IUD.java` |
| **최종 확인일** | 2026-09-18 (실제 소스 기준) |

## ⚙️ 환경 및 전제

- 두 개의 서로 다른 DB에 대한 커넥션을 하나의 서블릿에서 연다: `conn`(신진SM `iPlusERP_SJ`)과 `connDZ`(더존). 접속 정보는 `web.xml`의 `driver`/`url`/`username`/`password`(MES)와 `urlDZ`/`usernameDZ`/`passwordDZ`(더존) context-param.
- **더존 연결은 best-effort다.** `connDZ` 생성이 실패하면 `catch`로 잡아 경고 로그만 남기고 `connDZ = null`로 진행 — MES 저장은 더존 연결 여부와 무관하게 계속된다.

## 📖 상세 내용

### 전체 흐름 (jvWMA624_01_IUD.service() 기준)

```
1. conn(MES) / connDZ(더존) 연결. connDZ 실패해도 계속 진행(null)
2. JSON 배열의 레코드들 중 IO_DATE(연월) 추출
3. connDZ != null 이면: 입고(405)/출고(406) 그룹별로 딱 1번씩
   NEOE.CP_GETNO(cdClass 20=입고→TGI.., 19=출고→TGO..) 호출해
   "배치 공용 IO_NO"를 미리 채번 (sharedInputIoNo / sharedOutputIoNo)
4. 레코드 루프:
   a. EXEC SP_WMA624_01_IUD (MES, IO_NO=3번 값 또는 connDZ 없으면 '')
   b. conn.commit()  ← 더존 처리 결과와 무관하게 MES는 여기서 확정
   c. (connDZ != null 이면) 창고/품목 매핑 후 더존 반영:
      - TCO102/TCO101/TCO403(MES) + DZSN_MA_PITEM(더존)으로
        CD_PLANT / CD_ITEM / CD_QTIOTP 조회
      - 배치 내 첫 레코드에서만 NEOE.UP_PU_MM_QTIOH_INSERT (헤더, IO_NO당 1회)
      - 레코드마다 NEOE.UP_PU_ITR_INSERT(입고) 또는 NEOE.UP_PU_CGI_INSERT(출고)
5. connDZ.commit() (전체 레코드 처리 후 1회)
```

> [!warning] MES와 더존은 하나의 트랜잭션이 아니다
> `conn.commit()`이 3단계 루프 **안에서 레코드마다** 먼저 실행되고, 더존 쪽 INSERT들은 그 이후 별도 커넥션(`connDZ`)으로 진행된다. 즉 MES 저장은 성공했는데 더존 반영 단계(품목 매핑 실패, `NEOE.UP_PU_ITR_INSERT` 예외 등)에서 문제가 생겨도 **MES 쪽 커밋은 이미 끝난 뒤**라 자동으로 되돌아가지 않는다. `catch` 블록에서 `connDZ.rollback()`을 시도하긴 하지만 MES(`conn`)는 이미 커밋된 상태라 의미가 없다. [\[완료\] 포장중복문제 분석](<../02_TechDocs/[완료] 포장중복문제 분석.md>)에서 다루는 "MES는 맞는데 더존만 틀어짐" 현상의 구조적 원인이 여기 있다.

### IO_NO 채번 — 두 가지 체계가 공존

| 구분 | 채번 로직 | 사용 시점 |
|---|---|---|
| 더존 발번 (`NEOE.CP_GETNO`) | `docu_ym` + `cdClass`(19/20) 기준, 더존 DB에서 발급 | `connDZ`가 정상 연결됐을 때 — 입고/출고 배치당 1개, 여러 레코드가 공유 |
| SP 자체 발번 | `SP_WMA624_01_IUD` 내부, `YYYYMMDD`+당일 4자리 순번, `TMA536` 기준 | `connDZ`가 null이거나 IO_NO 사전 채번을 못 받은 레코드 — 레코드마다 새로 채번됨 |

두 체계가 같은 `TMA536.IO_NO` 컬럼에 섞여 들어간다. 더존이 정상일 때는 "입고 1건당 공용 IO_NO", 더존이 끊겼을 때는 "레코드마다 새 IO_NO" — 이 전환 자체가 암묵적이라 코드만 봐서는 지금 어느 쪽 번호 체계로 저장됐는지 구분하기 어렵다. 자세한 채번 로직은 [\[SQL\] SP_WMA624_01_IUD](<[SQL] SP_WMA624_01_IUD.md>) 참고.

### 품목/창고 코드 매핑

| MES | 더존 | 조회 테이블 |
|---|---|---|
| `WAREHOUSE_CODE` | `CD_SL`(창고) | `TCO102.ETC` |
| `PLANT_CODE`(창고로 역산) | `CD_PLANT`(사업장) | `TCO101` (`CODE_ID1='132'`) `.ETC` |
| `MATERIAL_CODE` | `CD_ITEM`(품목) | `TCO403.PART_NO` (FACTORY_CODE 단위 관리) |
| 더존 `CLS_ITEM`(품목계정) | `CD_QTIOTP`(수불형태) | `DZSN_MA_PITEM.CLS_ITEM` → `005`=상품→`906`, `003`=제품→`908`, `004`=반제품→`930`, `001`=원자재→`910` (입고 세부는 별도로 `410`, 출고 세부는 `400` 고정값 사용) |

### 더존 쪽 실제 호출 프로시저

- `NEOE.CP_GETNO` — 수불번호 채번
- `NEOE.UP_PU_MM_QTIOH_INSERT` — 수불 헤더(QTIOH) 생성, IO_NO당 1회
- `NEOE.UP_PU_ITR_INSERT` — 입고 세부내역
- `NEOE.UP_PU_CGI_INSERT` — 출고 세부내역

> [!note] 회의 시점 설계와 실제 구현이 다르다
> [[신진SM 05.28 업무 미팅]](문서 내부 날짜는 06-05)에서 논의된 초안은 "`SP_WMA624_01_IUD` 저장 시 더존 `UP_PU_ITR_UPDATE`/`UP_PU_CGI_UPDATE`를 같이 호출"하는 방식이었다. 실제 구현은 `UPDATE`가 아니라 **헤더(QTIOH)+세부(ITR/CGI) 분리 INSERT** 방식으로, 그리고 SP 안이 아니라 **Java 서블릿에서 별도 커넥션으로** 호출하는 방식으로 바뀌었다 — 배치당 헤더 1개 + 라인 여러 개 구조가 필요해지면서 설계가 진화한 것으로 보인다. 회의록 원문은 그대로 두되, 이 문서가 "지금 실제로 동작하는 방식"의 기준이다.

## ⚠️ 주의사항

- 더존 연결 실패는 예외로 튀지 않고 조용히 경고 로그(`더존 DB 연결 실패 (MES 저장은 계속 진행)`)만 남긴다 — 더존 미반영 여부를 알려면 로그(`C:/logs/Log.log`)를 직접 봐야 한다. 화면상 저장 성공 메시지만으로는 더존 반영 여부를 알 수 없다.
- `TCO403`/`TCO102`/`TCO101` 매핑 조회 중 하나라도 빈 값이면 그 이후 더존 INSERT 전체가 조용히 스킵된다(`if (connDZ != null && !CD_ITEM_DZ.isEmpty())` 가드) — 매핑 누락이 곧 "더존 미반영"으로 이어지지만 사용자에게는 알림이 없다.

## 🔗 참고

- `src/com/MA/WMA620/jvWMA624_01_IUD.java`
- [\[SQL\] SP_WMA624_01_IUD](<[SQL] SP_WMA624_01_IUD.md>)
- [\[완료\] 포장중복문제 분석](<../02_TechDocs/[완료] 포장중복문제 분석.md>)
- [\[완료\] 재고보정 및 데이터동기화](<../02_TechDocs/[완료] 재고보정 및 데이터동기화.md>)
- [[신진SM 중복 포장문제 ( 05.22 )]]
- [[신진SM 05.28 업무 미팅]]
