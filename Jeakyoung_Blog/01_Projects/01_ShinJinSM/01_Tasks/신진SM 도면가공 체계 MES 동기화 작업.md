---
title: 신진SM 도면가공 체계 MES 동기화 작업
date: 2026-09-14
type: 작업
project: 신진SM
status: 진행중
priority: 보통
assignee: []
tags: []
---

# 신진SM 도면가공 체계 MES 동기화 작업

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 신진SM 현장 |
| **요청일** | 2026-09-14 |
| **대상 시스템** | MES(WPR559 생산실적등록) ↔ 더존 ERP |
| **관련 화면·프로그램** | `SP_WPR559_02_IUD_TEST`, `SP_WPR559_02_LIST`, `SP_WPR559_01_LIST`, `jvPROD_DATA_FETCH.java`, `ProdSLService.java`, `ProdReportService.java` |

> POP 시스템에서만 동작하던 도면가공 처리 흐름을 MES에도 이식하는 작업. 06-26/07-03 회의록에서 초기 설계(창고코드 3000/3400/6000/7000 체계, [[신진SM 개발 이력]] 참고)가 먼저 논의됐고, 이 문서의 09-14 설계는 최종적으로 다른 창고코드 체계(018/016/225, 더존 ETC 4200/7000)로 구현됐다 — 설계가 진행되며 창고코드 체계 자체가 바뀐 것이므로 06-26/07-03 회의록의 구체적 창고번호는 참고용으로만 볼 것.

## 🔍 현상 및 원인

WPR559(생산실적등록) 화면에서 공정별 실적을 등록할 때, POP 시스템의 도면가공(WORK_CODE=008) 처리 프로세스와 동일한 흐름이 MES에서도 동작해야 하는데 현재 MES는 이 프로세스가 전혀 구현돼 있지 않음 — 도면가공 대상 수주건의 실적을 MES에서 입력하면 재고 위치(더존 ERP 기준)와 실물 상태가 어긋나고, 출하계획이 조기/중복 생성되는 문제가 발생함.

## 🔧 조치 내용

### 2. 작업 범위

**대상 화면**: WPR559(생산실적등록) — grid_02(공정별 실적) 저장 경로만 해당. grid_01(수주 조회), grid_03(투입/반납), grid_04(불량)는 조회용 컬럼 추가 외 로직 변경 없음.

**대상 수주 조건**: `TSA308.FG_USE2 ∈ ('002' 도면가공, '003' 도면가공&출하이월)`인 수주 라인만 해당. 그 외 전 수주는 대상 아님(영향 없음).

**포함**:
- 포장(WORK_CODE=005) 저장 시 1차/2차 분기 처리
- 도면가공(WORK_CODE=008) 저장 시 완료 처리 및 상태 승격
- 관련 DB 스토어드 프로시저 3개 수정
- 관련 Java 서비스 3개 파일 수정

**제외(이번 작업 범위 아님)**:
- FG_USE2 자체를 세팅/변경하는 기능(수주 입력 단계는 건드리지 않음, 이미 세팅된 값을 읽기만 함)
- POP 쪽 코드 변경(대상 아님, 참고용으로만 분석)
- 더존 창고이동 전표를 생성하는 신규 체계 구축(기존 MES `stsMainDZ`/`stsDetailDZ` 재사용)

### 3. 핵심 개념 및 전제조건

| 항목 | 값/내용 | 확인 방법 |
|---|---|---|
| 도면가공 대상 판정 | `TSA308.FG_USE2 IN ('002','003')` | SP_WPR559_01_LIST에서 이미 사용 중, 실사용 데이터로 검증됨 |
| 상태 컬럼 | `TPR601.PLATE_COMPLETE_FLAG` (char(1), nullable) | 이미 존재(POP과 공유), 신규 컬럼 추가 불필요 |
| 상태값 의미 | NULL/공백=미착수, `'1'`=1차포장 완료(도면가공 대기), `'2'`=도면가공 완료(2차포장 가능) | POP 소스(`Drawing_008_Guide.md`, `frmProcess6.cs`)와 대조 확인 |
| 도면가공 MES 창고 | `018`(도면가공창고, plant 000001) | TCO102 조회 확인 |
| 도면가공 더존 ETC | `4200` | TCO102.ETC 조회 확인, POP `DRAWING_WH_ETC` 상수와 일치 |
| 출하창고(기존) | plant 000001→`016`, 000002→`225` | 기존 코드에 이미 하드코딩돼 있음 |
| 출하창고 더존 ETC | `7000`(기존 하드코딩값 유지) | 기존 코드 확인 |
| plant 000002 처리 | 별도 분기 불필요 | 도면가공 대상 수주 0건 확인, POP도 plant 분기 없음 |
| 공정마스터 008 | 이미 등록됨("도면가공") | TPR102 조회 확인 |

### 4. 작업사항

#### DB — 스토어드 프로시저 3개

| 대상 | 변경 내용 |
|---|---|
| `SP_WPR559_02_IUD_TEST` | ① `@PLATE_COMPLETE_FLAG CHAR(1) = NULL` 파라미터 추가 ② UPDATE 2곳에 `PLATE_COMPLETE_FLAG = ISNULL(@PLATE_COMPLETE_FLAG, PLATE_COMPLETE_FLAG)` 추가 ③ INSERT 컬럼/VALUES 추가 ④ 출하계획(TSA407) 생성 조건에 `AND ISNULL(@PLATE_COMPLETE_FLAG,'') <> '1'` 추가 — *(수정 스크립트 작성 완료, 검토 대기)* |
| `SP_WPR559_02_LIST` | 메인 SELECT + `#TMP_TABLE` UNION 양쪽에 `PLATE_COMPLETE_FLAG` 컬럼 추가 — *(스크립트 미작성)* |
| `SP_WPR559_01_LIST` | `PROD_WORK_ALL`과 같은 패턴의 OUTER APPLY로 생산계획 단위 `PLATE_COMPLETE_FLAG`(MAX값) 반환 컬럼 추가 — *(스크립트 미작성)* |

#### Java — `src/com/PR/WPR550/` 3개 파일

| 파일 | 변경 내용 |
|---|---|
| `jvPROD_DATA_FETCH.java` | `fetchDrawingStatus()` 신규 메서드 — `TSA308.FG_USE2` 조회(ORDER_NO/HISTNO/SEQNO 기준, payload에 이미 존재), `TPR601` 현재 `PLATE_COMPLETE_FLAG` 조회(PRODPLAN_DATE/SEQ 기준) |
| `ProdSLService.java` | `processSLCrossMove()` 진입부에 3분기(1차 세팅/진행중 차단/2차 통과) · `prodPacking()` 창고코드 override 분기 + SP 파라미터 추가 · `stsDetailDZ()`의 `P_CD_SL_REF` 하드코딩(`"7000"`)을 1차포장 시 `"4200"`으로 분기 |
| `ProdReportService.java` | `createPreparedStatement()`에서 WORK_CODE='008'이면 창고코드(`018`) 강제 override · `processProdReport()` 저장 성공 후 WORK_CODE='008'이면 `PLATE_COMPLETE_FLAG '1'→'2'` 승격 UPDATE(낙관적 잠금) |

#### Frontend(JS) — 선택 사항, 필수 아님

- `WPR559_VW.js` `grid_01` `getRowClass`에 `PLATE_COMPLETE_FLAG='2'` 조건 추가(2차포장 대상 빨간색 표시)
- `grid_02` WAREHOUSE_CODE 컬럼: WORK_CODE=008 선택 시 읽기전용 처리(UX 개선용, 백엔드가 어차피 강제하므로 없어도 기능엔 문제없음)

### 5. 작업 방식(설계 원리)

1. **판단은 저장 시점 딱 한 곳에서만 한다**: `fetchDrawingStatus()`가 FG_USE2와 현재 PLATE_COMPLETE_FLAG를 조회하는 게 유일한 분기점. 나머지 코드는 이 결과값에 따라 조건부로만 갈라짐.
2. **기존 로직 무영향 보장은 "가드 패턴"으로**: 모든 신규 분기는 `if (FG_USE2 IN ('002','003'))` 또는 `if (WORK_CODE=='008')`로 감싸져 있어, 대상이 아닌 나머지 케이스는 지금 코드와 완전히 동일하게 흐름. SP 레벨에서도 새 파라미터는 기본값 NULL + `ISNULL(...)` 가드로 "값을 안 넘기면 기존값 유지"가 보장됨.
3. **사용자는 1차/2차 개념을 몰라도 됨**: 화면 조작(그리드에서 공정 선택 후 저장)은 지금과 완전히 동일. 서버가 매 저장 시점마다 상태를 다시 판단해서 자동으로 분기.
4. **더존 전표까지 일관되게 처리**: MES DB(TPR601.WAREHOUSE_CODE)뿐 아니라 더존 전표 목적창고(`stsDetailDZ`의 `P_CD_SL_REF`)까지 같이 분기해야 MES와 더존 장부가 항상 일치.
5. **MES 자체 재고(TMA922)는 별도 코드 없이 자동 동기화**: `TG_TPR601LOT_TMA922` 트리거가 `WAREHOUSE_CODE` 값을 그대로 미러링하므로, TPR601LOT에 018을 넣기만 하면 TMA922도 자동으로 맞춰짐.

### 6. 기대되는 정상 프로세스

#### 일반 수주(FG_USE2 ∉ 002,003)
```
각 공정 실적 등록 → 포장(005) 저장
   └ 기존 코드 그대로: 창고=016/225, 출하계획 즉시 생성, 더존전표 목적창고=7000
   → 끝 (변경 없음)
```

#### 도면가공 수주(FG_USE2 ∈ 002,003)
```
길이절단 등 실적 등록 (변경 없음)
   ↓
포장(005) 1회차 = 1차포장 (사용자는 그냥 평소처럼 저장)
   └ 서버 판정: flag=NULL → "1차"
   └ MES 창고=018, PLATE_COMPLETE_FLAG='1'
   └ 출하계획 생성 스킵
   └ 더존전표 목적창고=4200
   → 상태: MES·더존 모두 "도면가공창고에 있음", 출하 대상 아님
   ↓
도면가공(008) 실적 등록
   └ 창고 강제 018
   └ 저장 성공 후 flag '1'→'2' 자동 승격
   ↓
포장(005) 2회차 = 2차포장 (사용자는 그냥 평소처럼 저장)
   └ 서버 판정: flag='2' → "2차"
   └ MES 창고=016/225(기존과 동일), 출하계획 정상 생성
   └ 더존전표: 출발창고 자동으로 4200(직전공정=008 창고 ETC), 목적창고=7000
   → 상태: 실물이 도면가공 끝내고 출하창고 입고된 것과 일치

[안전장치] 도면가공 없이 포장을 또 누르면 flag='1'(진행중)이라 저장 자체가 그 자리에서 차단됨
```

### 7. 확인된 리스크 / 잔여 이슈

- **DB 트리거 3개**: 전부 검토 완료, 무영향 확인
- **POP↔MES 혼용 시나리오**: 코드상 값은 일치하나 실제 혼용 테스트는 미수행
- **삭제(IRU='D') 시 플래그 복구 로직 없음**: 1차포장 삭제 후 재시도 시 더존전표 중복 가능성(기존 구조의 한계, 이번 작업으로 새로 생기는 문제는 아님)
- **동시성(더블클릭) 보호 없음**: 008 승격은 낙관적 잠금 있으나, 1차/2차 판정 자체는 잠금 없음(기존 시스템 전반의 위험 수준과 동일)
- **1차포장 출발창고 결정 방식**: POP의 세부 품목군 규칙 대신 MES 기존 방식(직전공정 창고 ETC) 재사용 — 대부분 일치하겠으나 100% 동일 보장은 아님

### 8. 다음 단계

1. `SP_WPR559_02_LIST`, `SP_WPR559_01_LIST` 수정 스크립트 작성
2. Java 3개 파일 실제 diff 작성
3. 일반 수주로 회귀 테스트(기존과 동일 동작 확인) 후 도면가공 수주로 전체 시나리오 테스트

### 9. 배포 순서에 대한 검토 (원본 대화 발췌)

Java `ProdSLService`/`SP_WPR559_02_IUD_TEST` 결과 매핑은 SP가 반환하는 컬럼을 이름으로 그대로 JSON에 담는 구조라, DB 스크립트를 먼저 적용해도(컬럼 하나 늘어남) Java·프론트 어느 쪽도 깨지지 않는다. 반대로 Java를 먼저 배포하면, `ProdSLService.java`의 SQL 상수가 파라미터 37개인데 운영 DB의 SP는 아직 36개라 "파라미터 개수 불일치"로 포장/일반실적 저장 전체가 즉시 실패한다(도면가공 건이 아니어도 전부 영향받음).

**권장 배포 순서**
1. DB 스크립트 3개 먼저 적용 (`SP_WPR559_02_IUD_TEST`, `SP_WPR559_02_LIST`, `SP_WPR559_01_LIST`) — 적용 직후 화면이 지금과 완전히 동일하게 동작하는지 확인
2. 문제없음 확인되면, 준비됐을 때 Java만 배포
3. Java 배포가 끝나야 비로소 도면가공 게이팅 로직이 실제로 동작 시작

즉 "Java를 안 배포해도 운영에 문제 없게"는 이 순서만 지키면 자동으로 달성된다 — 별도로 더 손볼 코드는 없고 DB부터 먼저 적용하면 된다.

### 부록 — 원본 스크립트 초안 (적용 전 검토용)

> [!warning] 아래는 검토 대화에서 그대로 옮긴 초안이다. 원본 대화 자체에 붙여넣기 과정에서 일부 줄이 잘린 흔적(`ME =@PROD_ETIME`처럼 문장 중간이 끊긴 부분 등)이 남아있다 — 실제 DB에 적용하기 전에 반드시 운영 SP 원본과 diff로 재대조할 것. 이 부록은 "무엇을 하려 했는지"의 기록이지, 그대로 실행 가능한 최종본이 아니다.


```sql
-- 1/3. SP_WPR559_02_IUD_TEST

ALTER PROC [dbo].[SP_WPR559_02_IUD_TEST]
 (
  @FACTORY_CODE   VARCHAR(6)       -- 사업장코드
  ,@PLANT_CODE   VARCHAR(6)
  ,@PROD_GROUP_NO   VARCHAR(12) = ''
  ,@PRODPLAN_DATE   VARCHAR(8)
  ,@PRODPLAN_SEQ   INT
  ,@PROD_SEQ    INT  =0       -- 생산실적순번
  ,@WORK_CODE    VARCHAR(6) = ''   -- 공정코드
        ,@WORKCENTER_CODE  VARCHAR(6) = ''   -- 공정코드
        ,@EQUIP_SYS_CD          VARCHAR(10) = ''
  ,@WORK_SEQ    INT =0     -- 작업순번
  ,@PROD_SDATE   VARCHAR(8)              -- PROD_SDATE
  ,@PROD_STIME   VARCHAR(14) =''
  ,@PROD_EDATE   VARCHAR(8)
  ,@PROD_ETIME   VARCHAR(14) =''
  ,@PROD_QTY    FLOAT = 0
  ,@GOOD_QTY    FLOAT = 0
  ,@CYCLE_COUNT   int = 1
  ,@PROD_WORKER   VARCHAR(10)=''
  ,@ITEM_CODE    VARCHAR(15)=''      -- 제품코드
  ,@WAREHOUSE_CODE  VARCHAR(6)=''
  ,@WL_CODE    VARCHAR(6)=''
  ,@LOT_SEQ    INT=0
  ,@SYSTEM_LOT_NO   VARCHAR(20)=''
  ,@INPUT_FLAG   CHAR(1) = '1'
  ,@INPUT_DATE   VARCHAR(8)=''
  ,@LOT_FLAG    VARCHAR(3)=''
  ,@MATERIAL_QUALITY      VARCHAR(100) = ''       -- 재질
  ,@THICKNESS    decimal(18, 4) = 0      -- 두께
  ,@SPEC_X    decimal(18, 4) = 0      -- 폭
  ,@SPEC_Y    decimal(18, 4) = 0      -- 길이
        ,@SHIPPLAN_SEQ          VARCHAR(20) = ''        -- 출하계획번호
  ,@OPMAN_CODE   VARCHAR(10)       -- 등록자
  ,@IRU     VARCHAR(4)       -- IUD
  ,@P_NO_TRACK   NVARCHAR(40)   -- 일보번호
  ,@P_NO_IO    NVARCHAR(40)   -- 수불번호
  ,@P_NO_IOLINE   INT      -- 수불항번
  ,@PLATE_COMPLETE_FLAG   CHAR(1) = NULL   -- ★추가: 도면가공 상태. NULL=변경없음/'1'=1차포장(도면가공 대기)/'2'=도면가공완료(2차포장)
)

AS

BEGIN

 DECLARE @OPTIME VARCHAR(14)
 SET @OPTIME = CONVERT(CHAR(8),GETDATE(),112) + REPLACE(CONVERT(CHAR(
 DECLARE @SEARCH_MAT_CODE    VARCHAR(20) = ''
    DECLARE @INPUT_CNT          INT
    DECLARE @ERR_MSG            VARCHAR(2000)
    DECLARE @NEW_SHIPPLAN_SEQ   NVARCHAR(12) = '',
            @ORDER_NO           VARCHAR(12),
            @ORDER_HISTNO       VARCHAR(2),
            @ORDER_SEQNO        INT

 --SDATE EDATE 변경
 SET @PROD_STIME = @PROD_SDATE + @PROD_STIME + '00'
 IF @PROD_ETIME = '' BEGIN SET @PROD_ETIME = '' END
 ELSE BEGIN SET @PROD_ETIME = @PROD_EDATE + @PROD_ETIME + '00' END

    IF @IRU = 'U'
    BEGIN
        BEGIN
    --------------------------------------창고 변경X-------------------------------------
    UPDATE TPR601 with(updlock,rowlock)
    SET  PROD_STIME =@PROD_STIME
     , PROD_ETIME =@PROD_ETIME
     , PROD_QTY =@PROD_QTY
     , GOOD_QTY =@GOOD_QTY
     , PROD_WORKER =@PROD_WORKER
     , OPMAN_CODE2 = @OPMAN_CODE
     , OPTIME2 = @OPTIME
     , CYCLE_COUNT =@CYCLE_COUNT
     , WORK_CODE =@WORK_CODE
     , P_NO_IOLINE = @P_NO_IOLINE
     , WAREHOUSE_CODE =@WAREHOUSE_CODE
     , PLATE_COMPLETE_FLAG = ISNULL(@PLATE_COMPLETE_FLAG, PLATE_COMPL

    WHERE FACTORY_CODE = @FACTORY_CODE
    and  plant_code = @PLANT_CODE
    and  PRODPLAN_DATE = @PRODPLAN_DATE
    and  PRODPLAN_SEQ = @PRODPLAN_SEQ
    AND  PROD_SEQ = @PROD_SEQ
    UPDATE TPR601LOT with(updlock,rowlock)
    SET  WORK_CODE = @WORK_CODE
     , ITEM_PROD_QTY = @PROD_QTY
     , OPMAN_CODE2 = @OPMAN_CODE
     , OPTIME2 = @OPTIME

     , WAREHOUSE_CODE =@WAREHOUSE_CODE
    WHERE FACTORY_CODE = @FACTORY_CODE
    and  plant_code = @PLANT_CODE
    and  PRODPLAN_DATE = @PRODPLAN_DATE
    and  PRODPLAN_SEQ = @PRODPLAN_SEQ
    AND  PROD_SEQ = @PROD_SEQ
    AND  SYSTEM_LOT_NO = @SYSTEM_LOT_NO
   END
    END


 IF @IRU = 'I'
  BEGIN
   IF @SYSTEM_LOT_NO = ''
   BEGIN
    EXEC SP_WPR559_CREATE_MAT_CODE_BY_PROD @FACTORY_CODE, @PLANT_CODE, @WAREHOUSE_CODE, @ITEM_CODE, @MATERIAL_QUALITY
     , @THICKNESS, @SPEC_X, @SPEC_Y, @GOOD_QTY, @PROD_SDATE, @OPMAN_CODE, @OPTIME
     , @SEARCH_MAT_CODE OUTPUT, @SYSTEM_LOT_NO OUTPUT

   END
ME =@PROD_ETIME
     , PROD_QTY =@PROD_QTY
     , GOOD_QTY =@GOOD_QTY
     , PROD_WORKER =@PROD_WORKER
     , OPMAN_CODE2 = @OPMAN_CODE
     , OPTIME2 = @OPTIME
     , CYCLE_COUNT =@CYCLE_COUNT
     , WORK_CODE =@WORK_CODE
     , P_NO_IOLINE = @P_NO_IOLINE
     , WAREHOUSE_CODE =@WAREHOUSE_CODE
     , PLATE_COMPLETE_FLAG = ISNULL(@PLATE_COMPLETE_FLAG, PLATE_COMPLETE_FLAG)   -- ★추가

    WHERE FACTORY_CODE = @FACTORY_CODE
    and  plant_code = @PLANT_CODE
    and  PRODPLAN_DATE = @PRODPLAN_DATE
    and  PRODPLAN_SEQ = @PRODPLAN_SEQ
    AND  PROD_SEQ = @PROD_SEQ


    UPDATE TPR601LOT with(updlock,rowlock)
    SET  WORK_CODE = @WORK_CODE
     , ITEM_PROD_QTY = @PROD_QTY
     , OPMAN_CODE2 = @OPMAN_CODE
     , OPTIME2 = @OPTIME
     , WAREHOUSE_CODE =@WAREHOUSE_CODE
    WHERE FACTORY_CODE = @FACTORY_CODE
    and  plant_code = @PLANT_CODE
    and  PRODPLAN_DATE = @PRODPLAN_DATE
    and  PRODPLAN_SEQ = @PRODPLAN_SEQ
    AND  SYSTEM_LOT_NO = @SYSTEM_LOT_NO

   END

   /*----------------------------------------------- TPR601 신규 실적-----------------------------------------------*/

   DECLARE @ISEXISTS INT
   SET @ISEXISTS = (
    SELECT COUNT(PROD_SEQ)
    FROM TPR601
    WHERE FACTORY_CODE = @FACTORY_CODE
    and  plant_code = @PLANT_CODE
    and  PRODPLAN_DATE = @PRODPLAN_DATE
    and  PRODPLAN_SEQ = @PRODPLAN_SEQ
    and  PROD_SEQ = @PROD_SEQ
   )
   IF @ISEXISTS = 0
    BEGIN
     IF @PROD_SEQ = 0
     BEGIN
      SELECT @PROD_SEQ = ISNULL(MAX(PROD_SEQ), 0) + 1
      FROM TPR601
      WHERE FACTORY_CODE = @FACTORY_CODE
      and  plant_code = @PLANT_CODE
      and  PRODPLAN_DATE = @PRODPLAN_DATE
      and  PRODPLAN_SEQ = @PRODPLAN_SEQ
     END

     IF @PROD_GROUP_NO = ''
     BEGIN
      SET @PROD_GROUP_NO = (
       SELECT LEFT(@OPTIME, 8) + DBO.FN_FORMAT(ISNULL(MAX(CAST(RIGHT(+ 1,'0000')
       FROM TPR601
       WHERE FACTORY_CODE = @FACTORY_CODE
       AND  PLANT_CODE = @PLANT_CODE
       and  LEFT(PROD_GROUP_NO, 8) = LEFT(@OPTIME, 8)
      )
     END
     IF @SYSTEM_LOT_NO = ''
     BEGIN
LAG = '1'
      BEGIN
       SELECT @EXEISTS_LOT_NO = SYSTEM_LOT_NO
       FROM TLT101
       WHERE MATERIAL_CODE = @SEARCH_MAT_CODE
       AND  SUBSTRING(manufacture_date, 5, 2) = SUBSTRING(@PROD_SDATE, 5, 2)
      END
      ELSE
      BEGIN
       SELECT @EXEISTS_LOT_NO = SYSTEM_LOT_NO
       FROM TLT101
       WHERE MATERIAL_CODE = @SEARCH_MAT_CODE
      END

      IF @EXEISTS_LOT_NO = ''
      BEGIN
       IF @LOT_FLAG = '1'
       BEGIN
        SET @SYSTEM_LOT_NO = (
         SELECT
         'C' + CONVERT(NVARCHAR(6), @PROD_SDATE, 112) +
         RIGHT('000000' + CAST(ISNULL(MAX(CAST(SUBSTRING(A.SYSTEM_LOT_NO, 8, 6) AS INT)), 0) + 1  AS VARCHAR(6)) , 6)  AS COL1
         FROM TLT101 A WITH(NOLOCK)
         WHERE 1 = 1
         AND A.FACTORY_CODE   = @FACTORY_CODE
         AND A.SYSTEM_LOT_NO like 'C' + CONVERT(NVARCHAR(6), @PROD_SDATE, 112)   +'%'
        )
       END
       ELSE
       BEGIN
        SET @SYSTEM_LOT_NO = 'X' + @SEARCH_MAT_CODE
       END
      END
      ELSE
      BEGIN

       SET @SYSTEM_LOT_NO = @EXEISTS_LOT_NO
      END

      IF(ISNULL(@EXEISTS_LOT_NO, '') = '')
      BEGIN
       insert into tlt101
       (
        factory_code         ,plant_code         ,material_code
_flag         ,opman_code         ,optime
       )
       values
       (
        @FACTORY_CODE         ,@PLANT_CODE      ,@SEARCH_MAT_CODE
        ,@SYSTEM_LOT_NO         ,@SYSTEM_LOT_NO      ,@GOOD_QTY
        ,@PROD_SDATE    ,@PROD_SDATE
        ,1         ,1      ,1
        ,@PLANT_CODE  ,@PLANT_CODE ,''
        ,'생산' ,'',@WAREHOUSE_CODE
        ,'0' ,@OPMAN_CODE      ,@optime
       )
      END

     END

                    IF @WORK_CODE = '005' AND LEFT(ISNULL(@P_NO_IO,''),3) = 'MSL'
                       AND ISNULL(@PLATE_COMPLETE_FLAG,'') <> '1'   -- ★추가: 도면가공 1차포장이면 출하계획 생성 스킵
                    BEGIN

                        SELECT @NEW_SHIPPLAN_SEQ = LEFT(@OPTIME,8) + FORMAT(ISNULL(SUBSTRING(MAX(A.SHIPPLAN_SEQ), 9, 4), 0) + 1, '0000')
                        FROM TSA407 AS A
                        WHERE A.FACTORY_CODE = @FACTORY_CODE
                        AND A.SHIPPLAN_SEQ LIKE LEFT(@OPTIME,8) + '%'

                        SELECT @ORDER_NO = ORDER_NO , @ORDER_HISTNO = ORDER_HISTNO , @ORDER_SEQNO = ORDER_SEQNO
                        FROM TPR301R
                        WHERE FACTORY_CODE = @FACTORY_CODE
                        AND PRODPLAN_DATE = @PRODPLAN_DATE
                        AND PRODPLAN_SEQ = @PRODPLAN_SEQ

         INSERT INTO TSA407
                        (
                            FACTORY_CODE, SHIPPLAN_GBN, SHIPPLAN_SEQ, ORDER_NO, ORDER_HISTNO, ORDER_SEQNO, SHIPPLAN_DATE, OPMAN_CODE, OPTIME
                        )
                        VALUES
                        (
                            @FACTORY_CODE, '1', @NEW_SHIPPLAN_SEQ, @ORDER_NO, @ORDER_HISTNO, @ORDER_SEQNO, LEFT(@OPTIME,8), @OPMAN_CODE, @OPTIME
                        )

                        INSERT INTO TSA407L
                        (
                            FACTORY_CODE, SHIPPLAN_SEQ, LOT_SEQ, LOT_NO, OUTPUT_QTY, OUTPUT_DATE, ITEM_CODE, OPMAN_CODE, OPTIME
                        )
                        VALUES
                        (
                            @FACTORY_CODE, @NEW_SHIPPLAN_SEQ, @LOT_SEQ, @SYSTEM_LOT_NO, @GOOD_QTY, @OPTIME, @SEARCH_MAT_CODE, @OPMAN_CODE, @OPTIME
                        )

                    END


     INSERT INTO TPR601
     (
       FACTORY_CODE
      , PROD_GROUP_NO
      , PRODPLAN_DATE
      , PRODPLAN_SEQ
      , PROD_SEQ
      , ITEM_CODE
      , WORK_CODE
                        ,   WORKCENTER_CODE
                        ,   EQUIP_SYS_CD
      , PROD_STIME
      , PROD_ETIME
      , PROD_QTY
      , GOOD_QTY
      , PROD_WORKER
      , OPMAN_CODE
      , OPTIME
      , PLANT_CODE
         ,   P_NO_IOLINE
                        ,   SHIPPLAN_SEQ
                        ,   WORK_GBN
                        ,   PLATE_COMPLETE_FLAG            -- ★추가
     )
     VALUES
     (
       @FACTORY_CODE
      , @PROD_GROUP_NO
      , @PRODPLAN_DATE
      , @PRODPLAN_SEQ
      , @PROD_SEQ
      , CASE WHEN ISNULL(@SEARCH_MAT_CODE,'') = '' THEN @ITEM_CODE ELSE @SEARCH_MAT_CODE END
      , @WORK_CODE
                        ,   @WORKCENTER_CODE
                        ,   @EQUIP_SYS_CD
      , @PROD_STIME
      , @PROD_ETIME
      , @PROD_QTY
      , @GOOD_QTY
      , @PROD_WORKER
      , @OPMAN_CODE
      , @OPTIME
      , @PLANT_CODE
      , @CYCLE_COUNT
      , @WAREHOUSE_CODE
      , @WL_CODE
      , @SYSTEM_LOT_NO
      , @LOT_SEQ
                        ,   @P_NO_TRACK
                        ,   @P_NO_IO

     IF @@ROWCOUNT > 0
     BEGIN
      INSERT INTO TPR601LOT
      (
        FACTORY_CODE
       ,PRODPLAN_DATE
       ,PRODPLAN_SEQ
       ,PROD_SEQ
       ,LOT_SEQ
       ,SYSTEM_LOT_NO
       ,ITEM_CODE
       ,WORK_CODE
       ,ITEM_PROD_QTY
       ,INPUT_FLAG
       ,INPUT_DATE
       ,OPMAN_CODE
       ,OPTIME
       ,PLANT_CODE
       ,WAREHOUSE_CODE
       ,LOCATION_CODE
      )
      VALUES
      (
        @FACTORY_CODE
       ,@PRODPLAN_DATE
       ,@PRODPLAN_SEQ
       ,@PROD_SEQ
       ,@LOT_SEQ
       ,@SYSTEM_LOT_NO
          , CASE WHEN ISNULL(@SEARCH_MAT_CODE,'') = '' THEN @ITEM_COD
       ,@WORK_CODE
       ,@PROD_QTY
       ,'1'
       ,@INPUT_DATE
       ,@OPMAN_CODE
       ,@OPTIME
       ,@PLANT_CODE
       ,@WAREHOUSE_CODE
       ,@WL_CODE
      )
     END

    END
  END


    IF @IRU = 'D'
    BEGIN
        IF (ISNULL(@SHIPPLAN_SEQ,'') <> '' AND @WORK_CODE = '005')
        BEGIN
            DELETE FROM TSA407
            WHERE SHIPPLAN_SEQ = @SHIPPLAN_SEQ

            DELETE FROM TSA407L
            WHERE SHIPPLAN_SEQ = @SHIPPLAN_SEQ
        END

        DELETE FROM TPR601LOT
        WHERE FACTORY_CODE = @FACTORY_CODE
        AND PLANT_CODE = @PLANT_CODE
        AND PRODPLAN_DATE = @PRODPLAN_DATE
        AND PRODPLAN_SEQ = @PRODPLAN_SEQ
        AND PROD_SEQ = @PROD_SEQ
        AND LOT_SEQ = @LOT_SEQ
        AND SYSTEM_LOT_NO = @SYSTEM_LOT_NO

        DELETE FROM TPR603
        WHERE FACTORY_CODE = @FACTORY_CODE
        AND PLANT_CODE = @PLANT_CODE
        AND PRODPLAN_DATE = @PRODPLAN_DATE
        AND PRODPLAN_SEQ = @PRODPLAN_SEQ
        AND PROD_SEQ = @PROD_SEQ

        DELETE FROM TPR601
        WHERE FACTORY_CODE = @FACTORY_CODE
        AND PLANT_CODE = @PLANT_CODE
        AND PRODPLAN_DATE = @PRODPLAN_DATE
        AND PRODPLAN_SEQ = @PRODPLAN_SEQ
        AND PROD_SEQ = @PROD_SEQ

        DECLARE @CNT_PROD_SEQ INT
        SELECT @CNT_PROD_SEQ = ISNULL(COUNT(B.PROD_SEQ), 0)
        FROM tpr301R A
        LEFT JOIN tpr601 B
            ON A.FACTORY_CODE = B.FACTORY_CODE
            AND A.PLANT_CODE = B.PLANT_CODE
            AND A.PRODPLAN_DATE = B.PRODPLAN_DATE
            AND A.PRODPLAN_SEQ = B.PRODPLAN_SEQ
        WHERE B.FACTORY_CODE = @FACTORY_CODE
        AND B.PLANT_CODE = @PLANT_CODE
        AND B.PROD_GROUP_NO = @PROD_GROUP_NO

        PRINT  @CNT_PROD_SEQ
        IF @CNT_PROD_SEQ = 0
        BEGIN
            DECLARE @CUR_PROD_GROUP_NO VARCHAR(50)
            DECLARE group_cursor CURSOR FOR
                SELECT PROD_GROUP_NO
                FROM TPR601M
                WHERE FACTORY_CODE = @FACTORY_CODE
                AND PLANT_CODE = @PLANT_CODE
                AND PROD_GROUP_NO = @PROD_GROUP_NO

            OPEN group_cursor
            FETCH NEXT FROM group_cursor INTO @CUR_PROD_GROUP_NO

            WHILE @@FETCH_STATUS = 0
            BEGIN
                DELETE FROM TPR601M
                WHERE FACTORY_CODE = @FACTORY_CODE

                FETCH NEXT FROM group_cursor INTO @CUR_PROD_GROUP_NO
            END

            CLOSE group_cursor
            DEALLOCATE group_cursor
        END
    END

END

-- 2/3. SP_WPR559_02_LIST

CREATE PROC [dbo].[SP_WPR559_02_LIST]
(
  @FACTORY_CODE    VARCHAR(6),  -- 회사명
  @PLANT_CODE     VARCHAR(6),  -- 사업장
  @ORDER_NO     VARCHAR(12), -- 수주번호
  @ORDER_HISTNO     VARCHAR(12), -- 수주번호
  @ORDER_SEQNO     VARCHAR(12), -- 수주번호
  @OPMAN_CODE     VARCHAR(10)= '0000' -- 작성자
)

WITH RECOMPILE

AS

BEGIN
 SET NOCOUNT ON;

 DECLARE @CUR_FACTORY_CODE VARCHAR(6)
 DECLARE @CUR_PLANT_CODE VARCHAR(6)
 DECLARE @CUR_PROD_GROUP_NO VARCHAR(12)

 CREATE TABLE #TMP_TABLE (
  T_FACTORY_CODE   VARCHAR(6)
 , T_PLANT_CODE   VARCHAR(6)
 , T_PROD_GROUP_NO   VARCHAR(12)
NO   VARCHAR(2)
 , T_ORDER_SEQNO   INT
 , T_PRODPLAN_DATE   VARCHAR(8)
 , T_PROD_DATE    VARCHAR(8)
 , T_PRODPLAN_SEQ   INT
 , T_PROD_SEQ    INT
 , T_PROD_SDATE   VARCHAR(8)
 , T_PROD_EDATE   VARCHAR(8)
 , T_PROD_STIME   VARCHAR(14)
 , T_PROD_ETIME   VARCHAR(14)
 , T_LOT_SEQ    INT
 , T_GOOD_SYSTEM_LOT_NO VARCHAR(20)
 , T_BAD_SYSTEM_LOT_NO  VARCHAR(20)
 , T_PROD_QTY    FLOAT
 , T_GOOD_QTY    FLOAT
 , T_BAD_QTY    FLOAT
 , T_CYCLE_COUNT   INT
 , T_INPUT_FLAG   CHAR(1)
 , T_INPUT_DATE   VARCHAR(8)
 , T_PROD_WORKER   VARCHAR(20)
 , T_PROD_WORKER_DEPT  VARCHAR(20)
 , T_FINISH_FLAG   CHAR(1)
 , T_WORK_GBN    VARCHAR(6)
 , T_PROD_REMARK   VARCHAR(MAX)
 , T_WORK_CNT    INT
 , T_WORK_CODE    VARCHAR(6)
 , T_ITEM_CODE    VARCHAR(15)

 , T_WORK_SEQ    INT
 , T_VIEW_SEQ    INT
 , T_GOOD_WL_CODE   VARCHAR(6)
 , T_GOOD_WL_NAME   VARCHAR(30)
 , T_BAD_WL_NAME   VARCHAR(30)
 , T_BAD_WL_CODE   VARCHAR(6)
 , T_PROD_WORKER_NAME  VARCHAR(50)
 , T_LOT_FLAG    CHAR(1)
 , T_ORDER_UNIT_QTY  FLOAT
 , T_EQUIP_SYS_CD   VARCHAR(15)
 , T_END_WORK_DATE   VARCHAR(8)
 , T_MATERIAL_QUALITY  VARCHAR(100)
 , T_THICKNESS    DECIMAL(18, 4)
 , T_SPEC_X    DECIMAL(18, 4)
 , T_SPEC_Y    DECIMAL(18, 4)
 , T_MATERIAL_CODE   VARCHAR(20)
 , T_MATERIAL_NAME   VARCHAR(400)
 , T_MATERIAL_SPEC   VARCHAR(400)
 , T_PART_NO    VARCHAR(400)


    ,   T_WORKCENTER_NAME       VARCHAR(400)
    ,   T_EQUIP_CD              VARCHAR(100)
    ,   T_EQUIP_NM              VARCHAR(100)
 , T_OLD_MAT_CODE   VARCHAR(400)
 , T_P_NO_TRACK   NVARCHAR(40)
 , T_P_NO_IO    NVARCHAR(40)
 , T_P_NO_IOLINE   NUMERIC(5)
 , T_ITEM_KIND1   NVARCHAR(18)
 , T_ITEM_KIND2   NVARCHAR(18)
 , T_ITEM_KIND3   NVARCHAR(18)
 , T_WORKCENTER_CODE  NVARCHAR(18)
 , T_WORK_STATUS   NVARCHAR(18)
 , T_DZ_PRODPLAN_DATE  VARCHAR(8)
    ,   T_SHIPPLAN_SEQ          VARCHAR(20)
    ,   T_PLATE_COMPLETE_FLAG   VARCHAR(1)          -- ★추가
 )


 DECLARE CUR CURSOR FOR

RY_CODE
  , ISNULL(A.PLANT_CODE    ,'') PLANT_CODE
  , ISNULL(C.PROD_GROUP_NO, '') PROD_GROUP_NO
 FROM TPR301R A WITH(NOLOCK)
   LEFT JOIN TPR301 B WITH(NOLOCK)
   ON A.FACTORY_CODE = B.FACTORY_CODE
   AND A.PLANT_CODE = B.PLANT_CODE
   AND A.PRODPLAN_DATE = B.PRODPLAN_DATE
   AND A.PRODPLAN_SEQ = B.PRODPLAN_SEQ
   INNER JOIN TPR601 C WITH(NOLOCK)
   ON B.FACTORY_CODE = C.FACTORY_CODE
   AND B.PLANT_CODE = C.PLANT_CODE
   AND B.PRODPLAN_DATE = C.PRODPLAN_DATE
   AND B.PRODPLAN_SEQ = C.PRODPLAN_SEQ
 WHERE C.FACTORY_CODE = @FACTORY_CODE
 AND  C.PLANT_CODE = @PLANT_CODE
 AND  A.ORDER_NO = @ORDER_NO
 AND  A.ORDER_HISTNO = @ORDER_HISTNO
 AND  A.ORDER_SEQNO = @ORDER_SEQNO
 GROUP BY A.FACTORY_CODE
  ,  ISNULL(A.PLANT_CODE    ,'')
  ,  ISNULL(C.PROD_GROUP_NO, '')
 OPEN CUR
 FETCH NEXT FROM CUR INTO @CUR_FACTORY_CODE, @CUR_PLANT_CODE, @CUR_PROD_GROUP_NO

 WHILE @@FETCH_STATUS = 0
 BEGIN
  INSERT INTO #TMP_TABLE
  SELECT A.FACTORY_CODE
   , ISNULL(A.PLANT_CODE    ,'')
   , ISNULL(C.PROD_GROUP_NO, '')
   , ISNULL(C.WAREHOUSE_CODE,'')
   , ISNULL(F.WAREHOUSE_NAME,'')
   , ISNULL(I.WAREHOUSE_CODE,'')
   , ISNULL(F2.WAREHOUSE_NAME,'')
   , ISNULL(A.ORDER_NO    ,'')
   , ISNULL(A.ORDER_HISTNO  ,'')
   , ISNULL(A.ORDER_SEQNO   ,'')
   , ISNULL(A.PRODPLAN_DATE ,'')
   , LEFT(C.PROD_STIME, 8)
YSTEM_LOT_NO ,'')
   , ISNULL(I.SYSTEM_LOT_NO, '')
   , ISNULL(C.PROD_QTY    ,0)
   , ISNULL(C.GOOD_QTY    ,0)
   , ISNULL(C.BAD_QTY    ,0)
   , ISNULL(C.CYCLE_COUNT   ,0)
   , ISNULL(C.INPUT_FLAG    ,'')
   , ISNULL(C.INPUT_DATE    ,'')
   , ISNULL(PROD_WORKER    ,'')
   , ISNULL(G.DEPARTMENT_CODE ,'')
   , ISNULL(C.FINISH_FLAG   ,'')
   , ISNULL(WORK_GBN     ,'')
   , ISNULL(PROD_REMARK    ,'')
   , ISNULL(C.WORK_CNT, 0)
   , C.WORK_CODE
   , C.ITEM_CODE
   , ISNULL(B.WORK_SEQ, 0)
   , ISNULL(B.VIEW_SEQ, 0)
   , ISNULL(E.WL_CODE,'')
   , ISNULL(E.WL_NAME,'')
   , ISNULL(E2.WL_NAME,'')
   , ISNULL(I.LOCATION_CODE,'')
   , ISNULL(G.BASE_NAME, '')
   , ''          --READONLY
   , A.ORDER_QTY
            ,   ISNULL(EQ.EQUIP_SYS_CD, '')
   , ''
   , ISNULL(H.MATERIAL_QUALITY,'')
   , ISNULL(H.THICKNESS, 0)
   , ISNULL(H.SPEC_X, 0)
   , ISNULL(H.SPEC_Y, 0)
 ISNULL(EQ.EQUIP_NM, '')

   -- 인터페이스
   , ISNULL(H.OLD_MAT_CODE, '')
   , ISNULL(C.P_NO_TRACK, '')
   , ISNULL(C.P_NO_IO, '')
   , ISNULL(C.P_NO_IOLINE, 0)
   , ISNULL(H.ITEM_KIND1, '')
   , ISNULL(H.ITEM_KIND2, '')
   , ISNULL(H.ITEM_KIND3, '')
   , ISNULL(C.WORKCENTER_CODE, '')

   , ISNULL(F.WORK_STATUS, '')
   , ISNULL(A.PRODPLAN_DATE ,'')  -- DZ_PRODPLAN_DATE
            ,   ISNULL(C.SHIPPLAN_SEQ, '')      -- 포장시 출하계획번호
            ,   ISNULL(C.PLATE_COMPLETE_FLAG, '')  -- ★추가: 도면가공 상태

  FROM TPR301R A WITH(NOLOCK)

    LEFT JOIN TPR301 B WITH(NOLOCK)
    ON A.FACTORY_CODE = B.FACTORY_CODE
    AND A.PLANT_CODE = B.PLANT_CODE
    AND A.PRODPLAN_DATE = B.PRODPLAN_DATE
    AND A.PRODPLAN_SEQ = B.PRODPLAN_SEQ

                INNER JOIN TPR601 C WITH(NOLOCK)
    ON B.FACTORY_CODE = C.FACTORY_CODE
    AND B.PLANT_CODE = C.PLANT_CODE
    AND B.PRODPLAN_DATE = C.PRODPLAN_DATE
    AND B.PRODPLAN_SEQ = C.PRODPLAN_SEQ

LAN_SEQ = D.PRODPLAN_SEQ
    AND C.PROD_SEQ = D.PROD_SEQ
                --AND C.SYSTEM_LOT_NO = D.SYSTEM_LOT_NO

                LEFT JOIN TPR101 WC WITH(NOLOCK)
                ON C.FACTORY_CODE = WC.FACTORY_CODE
                AND C.PLANT_CODE = WC.PLANT_CODE
                AND C.WORKCENTER_CODE = WC.WORKCENTER_CODE

                LEFT JOIN TPR151 EQ WITH(NOLOCK)
                ON C.FACTORY_CODE = EQ.FACTORY_CODE
                AND C.EQUIP_SYS_CD = EQ.EQUIP_SYS_CD

                LEFT JOIN TCO102L E WITH(NOLOCK)
    ON A.FACTORY_CODE = E.FACTORY_CODE
    AND C.WAREHOUSE_CODE = E.WAREHOUSE_CODE
    AND C.WL_CODE = E.WL_CODE

                LEFT JOIN TCO102 F WITH(NOLOCK)
    ON C.FACTORY_CODE = F.FACTORY_CODE
    AND C.PLANT_CODE = F.PLANT_CODE
    AND C.WAREHOUSE_CODE = F.WAREHOUSE_CODE
                LEFT JOIN TIN114 G WITH(NOLOCK)
    ON C.FACTORY_CODE = G.FACTORY_CODE
    AND C.PLANT_CODE = G.PLANT_CODE
    AND C.PROD_WORKER = G.EMPLOYEE_NO

                LEFT JOIN TCO403 H WITH(NOLOCK)
    ON C.FACTORY_CODE = H.FACTORY_CODE
    AND C.ITEM_CODE = H.MATERIAL_CODE

                LEFT JOIN (
     SELECT FACTORY_CODE
      , PLANT_CODE
      , WAREHOUSE_CODE
      , PRODPLAN_DATE
      , PRODPLAN_SEQ
      , PROD_SEQ
      , LOCATION_CODE
      , SYSTEM_LOT_NO
      , SUM(QC_QTY) AS BAD_QTY
     FROM TPR603 WITH(NOLOCK)
     GROUP BY FACTORY_CODE
      , PLANT_CODE
      , WAREHOUSE_CODE
      , PRODPLAN_DATE
      , PRODPLAN_SEQ
      , PROD_SEQ
      , LOCATION_CODE
      , SYSTEM_LOT_NO
    ) I
    ON C.FACTORY_CODE = I.FACTORY_CODE
    AND C.PLANT_CODE = I.PLANT_CODE
    AND C.PRODPLAN_DATE = I.PRODPLAN_DATE
    AND C.PRODPLAN_SEQ = I.PRODPLAN_SEQ
    AND C.PROD_SEQ = I.PROD_SEQ

    LEFT JOIN TCO102L E2 WITH(NOLOCK)
_NO <> @ORDER_NO
  OR  A.ORDER_HISTNO <> @ORDER_HISTNO
  OR  A.ORDER_SEQNO <> @ORDER_SEQNO)
 FETCH NEXT FROM CUR INTO @CUR_FACTORY_CODE, @CUR_PLANT_CODE, @CUR_PROD_GROUP_NO
 END

 --커서 닫고 초기화
 CLOSE CUR
 DEALLOCATE CUR

 SET NOCOUNT OFF;
 SELECT A.FACTORY_CODE
  , ISNULL(A.PLANT_CODE    ,'')     AS PLANT_CODE
  , ISNULL(C.PROD_GROUP_NO, '')     AS PROD_GROUP_NO
  , ISNULL(C.WAREHOUSE_CODE,'')     AS WAREHOUSE_CODE
  , ISNULL(F.WAREHOUSE_NAME,'')     AS WAREHOUSE_NAME
  , ISNULL(I.WAREHOUSE_CODE,'')     AS BAD_WAREHOUSE_CODE
  , ISNULL(F2.WAREHOUSE_NAME,'')    AS BAD_WAREHOUSE_NAME
  , ISNULL(A.ORDER_NO    ,'')     AS ORDER_NO
  , ISNULL(A.ORDER_HISTNO  ,'')     AS ORDER_HISTNO
  , ISNULL(A.ORDER_SEQNO   ,'')     AS ORDER_SEQNO
  , ISNULL(A.PRODPLAN_DATE ,'')     AS PRODPLAN_DATE
  , LEFT(C.PROD_STIME, 8)         AS PROD_DATE
  , ISNULL(A.PRODPLAN_SEQ  ,0)      AS PRODPLAN_SEQ
  , ISNULL(C.PROD_SEQ    ,0)      AS PROD_SEQ
        , SUBSTRING(C.PROD_STIME, 1, 8)   AS PROD_SDATE
  , SUBSTRING(C.PROD_ETIME, 1, 8)   AS PROD_EDATE
  , SUBSTRING(C.PROD_STIME, 9, 4)   AS PROD_STIME
  , SUBSTRING(C.PROD_ETIME, 9, 4)   AS PROD_ETIME
  , ISNULL(D.LOT_SEQ    ,0)      AS LOT_SEQ
  , ISNULL(D.SYSTEM_LOT_NO ,'')     AS GOOD_SYSTEM_LOT_NO
  , ISNULL(I.SYSTEM_LOT_NO, '')     AS BAD_SYSTEM_LOT_NO
  , ISNULL(C.PROD_QTY    ,0)      AS PROD_QTY
  , ISNULL(C.GOOD_QTY    ,0)      AS GOOD_QTY
  , ISNULL(C.BAD_QTY    ,0)      AS BAD_QTY
  , ISNULL(C.CYCLE_COUNT   ,0)      AS CYCLE_COUNT
  , ISNULL(C.INPUT_FLAG    ,'')     AS INPUT_FLAG
  , ISNULL(C.INPUT_DATE    ,'')     AS INPUT_DATE
  , ISNULL(PROD_WORKER    ,'')     AS PROD_WORKER
  , ISNULL(G.DEPARTMENT_CODE,'')    AS PROD_WORKER_DEPT
  , ISNULL(C.FINISH_FLAG   ,'')     AS FINISH_FLAG
  , ISNULL(WORK_GBN     ,'')     AS WORK_GBN
  , ISNULL(PROD_REMARK    ,'')     AS PROD_REMARK
  , ISNULL(C.WORK_CNT, 0)           AS WORK_CNT
  , ISNULL(C.WORK_CODE, '')         AS WORK_CODE
  , ISNULL(C.ITEM_CODE, '')         AS ITEM_CODE
  , ISNULL(B.WORK_SEQ, 0)           AS WORK_SEQ
  , ISNULL(B.VIEW_SEQ, 0)           AS VIEW_SEQ
  , ISNULL(E.WL_CODE,'')            AS GOOD_WL_CODE
  , ISNULL(E.WL_NAME,'')            AS GOOD_WL_NAME
  , ISNULL(E2.WL_NAME,'')           AS BAD_WL_NAME
  , ISNULL(I.LOCATION_CODE,'')      AS BAD_WL_CODE
  , ISNULL(G.BASE_NAME, '')         AS PROD_WORKER_NAME
  , ''                              AS LOT_FLAG
  , A.ORDER_QTY                     AS ORDER_UNIT_QTY
  --, A.ORDER_QTY                     AS ORDER_QTY
  ,   ISNULL(EQ.EQUIP_SYS_CD, '')     AS EQUIP_SYS_CD
  , ''                              AS END_WORK_DATE
  , ISNULL(H.MATERIAL_QUALITY,'')   AS MATERIAL_QUALITY
  , ISNULL(H.THICKNESS, 0)          AS THICKNESS
  , ISNULL(H.SPEC_X, 0)             AS SPEC_X
  , ISNULL(H.SPEC_Y, 0)             AS SPEC_Y
  , ISNULL(H.MATERIAL_CODE, '')     AS MATERIAL_CODE
  , ISNULL(H.MATERIAL_NAME, '')     AS MATERIAL_NAME
  , ISNULL(H.MATERIAL_SPEC, '')     AS MATERIAL_SPEC
  , ISNULL(H.PART_NO, '')           AS PART_NO
        ,   ISNULL(WC.WORKCENTER_NAME, '')  AS WORKCENTER_NAME
        ,   ISNULL(EQ.EQUIP_CD, '')         AS EQUIP_CD
        ,   ISNULL(EQ.EQUIP_NM, '')         AS EQUIP_NM

  , ISNULL(H.OLD_MAT_CODE, '')      AS OLD_MAT_CODE
  , ISNULL(C.P_NO_TRACK, '')        AS P_NO_TRACK
  , ISNULL(C.P_NO_IO, '')           AS P_NO_IO
  , ISNULL(C.P_NO_IOLINE, 0)        AS P_NO_IOLINE
  , ISNULL(H.ITEM_KIND1, '')        AS ITEM_KIND1
  , ISNULL(H.ITEM_KIND2, '')        AS ITEM_KIND2
  , ISNULL(H.ITEM_KIND3, '')        AS ITEM_KIND3
  , ISNULL(C.WORKCENTER_CODE, '')   AS WORKCENTER_CODE
ULL(C.SHIPPLAN_SEQ, '')      AS SHIPPLAN_SEQ         -- 포장시 출하계획번호
        ,   ISNULL(C.PLATE_COMPLETE_FLAG, '') AS PLATE_COMPLETE_FLAG   -- ★추가: 도면가공 상태
 FROM TPR301R A WITH(NOLOCK)

   LEFT JOIN TPR301 B WITH(NOLOCK)
   ON A.FACTORY_CODE = B.FACTORY_CODE
   AND A.PLANT_CODE = B.PLANT_CODE
   AND A.PRODPLAN_DATE = B.PRODPLAN_DATE
   AND A.PRODPLAN_SEQ = B.PRODPLAN_SEQ

   INNER JOIN TPR601 C WITH(NOLOCK)
   ON B.FACTORY_CODE = C.FACTORY_CODE
   AND B.PLANT_CODE = C.PLANT_CODE
   AND B.PRODPLAN_DATE = C.PRODPLAN_DATE
   AND B.PRODPLAN_SEQ = C.PRODPLAN_SEQ

   LEFT JOIN TPR601LOT D WITH(NOLOCK)
   ON C.FACTORY_CODE = D.FACTORY_CODE
   AND C.PLANT_CODE = D.PLANT_CODE
      AND C.PRODPLAN_DATE = D.PRODPLAN_DATE
   AND C.PRODPLAN_SEQ = D.PRODPLAN_SEQ
   AND C.PROD_SEQ = D.PROD_SEQ
            --AND C.SYSTEM_LOT_NO = D.SYSTEM_LOT_NO

            LEFT JOIN TPR101 WC WITH(NOLOCK)
            ON C.FACTORY_CODE = WC.FACTORY_CODE
            AND C.PLANT_CODE = WC.PLANT_CODE
            AND C.WORKCENTER_CODE = WC.WORKCENTER_CODE

            LEFT JOIN TPR151 EQ WITH(NOLOCK)
            ON C.FACTORY_CODE = EQ.FACTORY_CODE
            AND C.EQUIP_SYS_CD = EQ.EQUIP_SYS_CD

   LEFT JOIN TCO102L E WITH(NOLOCK)
   ON A.FACTORY_CODE = E.FACTORY_CODE
   AND C.WAREHOUSE_CODE = E.WAREHOUSE_CODE
   AND C.WL_CODE = E.WL_CODE

   LEFT JOIN TCO102 F WITH(NOLOCK)
   ON C.FACTORY_CODE = F.FACTORY_CODE

   LEFT JOIN TCO403 H WITH(NOLOCK)
   ON C.FACTORY_CODE = H.FACTORY_CODE
   AND C.ITEM_CODE = H.MATERIAL_CODE

   LEFT JOIN (
    SELECT FACTORY_CODE
     , PLANT_CODE
     , WAREHOUSE_CODE
     , PRODPLAN_DATE
     , PRODPLAN_SEQ
     , PROD_SEQ
     , LOCATION_CODE
     , SYSTEM_LOT_NO
     , SUM(QC_QTY) AS BAD_QTY
    FROM TPR603 WITH(NOLOCK)
    GROUP BY FACTORY_CODE
     , PLANT_CODE
     , WAREHOUSE_CODE
     , PRODPLAN_DATE
     , PRODPLAN_SEQ
     , PROD_SEQ
     , LOCATION_CODE
     , SYSTEM_LOT_NO
   ) I
   ON C.FACTORY_CODE = I.FACTORY_CODE
   AND C.PLANT_CODE = I.PLANT_CODE
   AND C.PRODPLAN_DATE = I.PRODPLAN_DATE
   AND C.PRODPLAN_SEQ = I.PRODPLAN_SEQ
   AND C.PROD_SEQ = I.PROD_SEQ

O102 F2 WITH(NOLOCK)
   ON I.FACTORY_CODE = F2.FACTORY_CODE
   AND I.PLANT_CODE = F2.PLANT_CODE
   AND I.WAREHOUSE_CODE = F2.WAREHOUSE_CODE

 WHERE C.FACTORY_CODE = @FACTORY_CODE
 AND  C.PLANT_CODE = @PLANT_CODE
 AND  A.ORDER_NO = @ORDER_NO
 AND  A.ORDER_HISTNO = @ORDER_HISTNO
 AND  A.ORDER_SEQNO = @ORDER_SEQNO

 UNION ALL

 SELECT *
 FROM #TMP_TABLE
 GROUP BY  T_FACTORY_CODE
    , T_PLANT_CODE
    , T_PROD_GROUP_NO
    , T_WAREHOUSE_CODE
    , T_WAREHOUSE_NAME
    , T_BAD_WAREHOUSE_CODE
    , T_BAD_WAREHOUSE_NAME
    , T_ORDER_NO
    , T_ORDER_HISTNO
    , T_ORDER_SEQNO
    , T_PRODPLAN_DATE
    , T_PROD_DATE
    , T_PRODPLAN_SEQ
    , T_PROD_SEQ
    , T_PROD_SDATE
    , T_PROD_EDATE
    , T_PROD_STIME
    , T_PROD_ETIME
    , T_LOT_SEQ
    , T_GOOD_SYSTEM_LOT_NO
    , T_BAD_SYSTEM_LOT_NO
    , T_PROD_QTY
    , T_GOOD_QTY
    , T_BAD_QTY
    , T_CYCLE_COUNT
    , T_INPUT_FLAG
    , T_INPUT_DATE
    , T_PROD_WORKER
    , T_PROD_WORKER_DEPT
    , T_FINISH_FLAG
    , T_WORK_GBN
    , T_PROD_REMARK
    , T_WORK_CNT
    , T_WORK_CODE
    , T_ITEM_CODE
    , T_WORK_SEQ
    , T_VIEW_SEQ
    , T_GOOD_WL_CODE
    , T_GOOD_WL_NAME
    , T_BAD_WL_NAME
    , T_BAD_WL_CODE
    , T_PROD_WORKER_NAME
    , T_LOT_FLAG
    , T_ORDER_UNIT_QTY
    , T_EQUIP_SYS_CD
    , T_END_WORK_DATE
    , T_MATERIAL_QUALITY
    , T_THICKNESS
    , T_SPEC_X
    , T_SPEC_Y
    , T_MATERIAL_CODE
    , T_MATERIAL_NAME
    , T_MATERIAL_SPEC
    , T_PART_NO
             ,  T_WORKCENTER_NAME
_CODE
    , T_P_NO_TRACK
   , T_P_NO_IO
   , T_P_NO_IOLINE
   , T_ITEM_KIND1
   , T_ITEM_KIND2
   , T_ITEM_KIND3
   , T_WORKCENTER_CODE
   , T_WORK_STATUS
   , T_DZ_PRODPLAN_DATE
            ,   T_SHIPPLAN_SEQ
            ,   T_PLATE_COMPLETE_FLAG          -- ★추가

 ORDER BY PROD_GROUP_NO, ORDER_NO
END

-- 3/3. SP_WPR559_01_LIST

ALTER PROC [dbo].[SP_WPR559_01_LIST]
(
        @FACTORY_CODE                VARCHAR(6),        -- 회사명
        @PLANT_CODE                    VARCHAR(6),        -- 사업장(SAMWOO 3)
        @ORDER_DATE_FROM            VARCHAR(8),        -- 수주일자 FROM
        @ORDER_DATE_TO                VARCHAR(8),        -- 수주일자 TO
        @MATERIAL_QUALITY            VARCHAR(100),    -- 재질
        @THICKNESS                    DECIMAL(18, 4) = 0,    -- 두께
        @SPEC_X                        DECIMAL(18, 4) = 0,    --    폭
        @SPEC_Y                        DECIMAL(18, 4) = 0,    -- 길이
        @ORDER_NO                    VARCHAR(12),    -- 수주번호
        @SEARCH_CUST_NAME            VARCHAR(255),    -- 거래처통합검색
        @SEARCH_ITEM_NAME            VARCHAR(255) = '',    -- 거래처통합검색
        @SEARCH_P_NO_TRACK            VARCHAR(255) = '',    -- 거래처통합검색
        @OPMAN_CODE                    VARCHAR(10)= '0000', -- 작성자
        @CLOSING_FLAG                VARCHAR(10) = '1',
        @FG_USE2_FLAG                VARCHAR(1) = '' -- 도면가공 구분자 (1 -> 도면가공, 0 -> 도면가공 제외)
)
--WITH RECOMPILE
AS

        SET NOCOUNT ON;

        -- 임시 테이블 생성
        CREATE TABLE #TempTable
        (
            FACTORY_CODE VARCHAR(50),
            PLANT_CODE VARCHAR(50),
            ORDER_NO VARCHAR(50),
            ORDER_HISTNO VARCHAR(50),
            ORDER_SEQNO VARCHAR(50),
            PROD_GROUP_NO VARCHAR(50),
            P_NO_TRACK VARCHAR(50)
        );
        --CREATE CLUSTERED INDEX CX_TempTable_Order
        --ON #TempTable
        --(
        --      FACTORY_CODE
        --    , PLANT_CODE
        --    , ORDER_NO
        --    , ORDER_HISTNO
        --    , ORDER_SEQNO
        --);
        -- 데이터를 임시 테이블에 삽입
        INSERT INTO #TempTable
        SELECT  A.FACTORY_CODE,
                A.PLANT_CODE,
                A.ORDER_NO,
                A.ORDER_HISTNO,
                A.ORDER_SEQNO,
                MAX(C.PROD_GROUP_NO) AS PROD_GROUP_NO,
                MAX(C.P_NO_TRACK) AS P_NO_TRACK
        FROM    TPR301R A with(nolock)
            INNER JOIN    TSA307 B WITH(NOLOCK)
            ON A.FACTORY_CODE = B.FACTORY_CODE
            AND A.ORDER_NO = B.ORDER_NO
            AND A.ORDER_HISTNO = B.ORDER_HISTNO
            AND B.ORDER_DATE BETWEEN @ORDER_DATE_FROM AND @ORDER_DATE_TO
            outer apply(
                    SELECT  T601.FACTORY_CODE,
                            T601.PLANT_CODE,
                            T601.PRODPLAN_DATE,
                            T601.PRODPLAN_SEQ,
                            T601.PROD_GROUP_NO,
                            T601.P_NO_TRACK
                    FROM    TPR601 as T601 with(nolock)
                    where    A.FACTORY_CODE    = T601.FACTORY_CODE
                    AND     A.PRODPLAN_DATE = T601.PRODPLAN_DATE
                    AND     A.PRODPLAN_SEQ    = T601.PRODPLAN_SEQ
                    AND     A.PLANT_CODE    = T601.PLANT_CODE
                    GROUP BY T601.FACTORY_CODE,
                             T601.PLANT_CODE,
                             T601.PRODPLAN_DATE,
                             T601.PRODPLAN_SEQ,
                             T601.PROD_GROUP_NO,
                             T601.P_NO_TRACK

                ) C
        WHERE    (@ORDER_NO_TEMP = '' OR ( @ORDER_NO_TEMP <>'' AND ISNULL(A.ORDER_NO, '') LIKE '%' + @ORDER_NO_TEMP + '%'))
        AND        B.ORDER_DATE BETWEEN @ORDER_DATE_FROM AND @ORDER_DATE_TO
        GROUP BY A.FACTORY_CODE,
                 A.PLANT_CODE,
                 A.ORDER_NO,
                 A.ORDER_HISTNO,
                 A.ORDER_SEQNO
    SET NOCOUNT OFF;


    SELECT    ORDER_TABLE.FACTORY_CODE
NULL(GROUP_TABLE.P_NO_TRACK, '') P_NO_TRACK
        ,    ORDER_R_PRODPLAN.PRODPLAN_DATE
        ,    ORDER_R_PRODPLAN.PRODPLAN_SEQ
        ,    ORDER_TABLE.ORDER_NO
        ,    ORDER_DETAIL.ORDER_HISTNO
        ,    ORDER_DETAIL.ORDER_SEQNO
        ,    ORDER_TABLE.CUSTOMER_CODE
        ,    CUST.CUSTOMER_NAME
        ,    ORDER_DETAIL.ITEM_CODE
        ,    ORDER_DETAIL.ITEM_CODE MATERIAL_CODE
        ,    WORK.WORK_NAME
        ,    ORDER_DETAIL.DELIVERY_DATE
        ,    ISNULL(MAT.MATERIAL_QUALITY,'') MATERIAL_QUALITY
        ,    ISNULL(MAT_QUALITY.CODE_NAME_FULL, '') MATERIAL_QUALITY_NAME
        ,    ISNULL(MAT.THICKNESS,0) THICKNESS
        ,    ISNULL(MAT.SPEC_X,0) SPEC_X
        ,    ISNULL(MAT.SPEC_Y,0) SPEC_Y
        ,    ORDER_DETAIL.ORDER_UNIT_QTY -- 수량(수주량)

        ,    ISNULL(PROD_WORK_ALL.PROD_QTY_WORK_001, 0) AS PROD_QTY_WORK_001         --폭절단
        ,    ISNULL(PROD_WORK_ALL.PROD_QTY_WORK_002, 0) AS PROD_QTY_WORK_002         --길이절단
        ,    ISNULL(PROD_WORK_ALL.PROD_QTY_WORK_003, 0) AS PROD_QTY_WORK_003         --평면A
        ,    ISNULL(PROD_WORK_ALL.PROD_QTY_WORK_006, 0) AS PROD_QTY_WORK_006         --평면B
        ,    ISNULL(PROD_WORK_ALL.PROD_QTY_WORK_004, 0) AS PROD_QTY_WORK_004         --측면
        ,    ISNULL(PROD_WORK_ALL.PROD_QTY_WORK_007, 0) AS PROD_QTY_WORK_007         --4면가공
        ,    ISNULL(PROD_WORK_ALL.PROD_QTY_WORK_005, 0) AS PROD_QTY_WORK_005         --포장
        ,    ISNULL(PROD_WORK_ALL.PROD_QTY_WORK_008, 0) AS PROD_QTY_WORK_008         --도면가공
        ,   ISNULL(SHIP_DATA.SHIPPING_QTY, 0) AS SHIPPING_QTY                     --출하

        ,    ISNULL(MAT.LOT_FLAG, '0') LOT_FLAG
        ,    ISNULL(MAT.MATERIAL_NAME, '') MATERIAL_NAME
        ,    ISNULL(MAT.MATERIAL_SPEC, '') MATERIAL_SPEC
        ,    ISNULL(MAT.PART_NO, '') PART_NO
        ,   ISNULL(MAT.WORK_STATUS, '') AS WORK_STATUS
        ,    ISNULL(MAT.ITEM_KIND2, '') AS ITEM_KIND2

        ,   ISNULL(ORDER_DETAIL.FG_USE2, '') AS FG_USE2
        ,   ISNULL(ORDER_DETAIL.CLOSING_FLAG,'0') AS CLOSING_FLAG
        ,   ISNULL(PLATE_STATUS.PLATE_FLAG, '') AS PLATE_COMPLETE_FLA 상태

    FROM    TSA307 ORDER_TABLE with(nolock)

            LEFT JOIN TSA308 ORDER_DETAIL with(nolock)
            ON ORDER_TABLE.FACTORY_CODE = ORDER_DETAIL.FACTORY_CODE
            AND ORDER_TABLE.ORDER_NO = ORDER_DETAIL.ORDER_NO
            AND ORDER_TABLE.ORDER_HISTNO = ORDER_DETAIL.ORDER_HISTNO
            AND ORDER_DETAIL.DELETE_FLAG <> '1'

            LEFT JOIN TCO403 MAT with(nolock)
            ON ORDER_DETAIL.FACTORY_CODE = MAT.FACTORY_CODE
            AND ORDER_DETAIL.ITEM_CODE = MAT.MATERIAL_CODE

            LEFT JOIN TCO101 MAT_QUALITY with(nolock)
            ON MAT_QUALITY.CODE_ID1 = '424'
            AND MAT_QUALITY.CODE_ID2 = MAT.MATERIAL_QUALITY

            LEFT JOIN TCO601 CUST with(nolock)
            ON ORDER_TABLE.CUSTOMER_CODE = CUST.CUSTOMER_CODE

            LEFT JOIN #TempTable    GROUP_TABLE with(nolock)
            ON ORDER_DETAIL.FACTORY_CODE = GROUP_TABLE.FACTORY_CODE
            AND ORDER_DETAIL.PLANT_CODE = GROUP_TABLE.PLANT_CODE
            AND ORDER_DETAIL.ORDER_NO = GROUP_TABLE.ORDER_NO
            AND ORDER_DETAIL.ORDER_HISTNO = GROUP_TABLE.ORDER_HISTNO
            AND ORDER_DETAIL.ORDER_SEQNO = GROUP_TABLE.ORDER_SEQNO

            LEFT JOIN TPR301R ORDER_R_PRODPLAN with(nolock)
            ON  ORDER_DETAIL.FACTORY_CODE = ORDER_R_PRODPLAN.FACTORY_CODE
            AND ORDER_DETAIL.PLANT_CODE = ORDER_R_PRODPLAN.PLANT_CODE
            AND ORDER_DETAIL.ORDER_NO = ORDER_R_PRODPLAN.ORDER_NO
            AND ORDER_DETAIL.ORDER_HISTNO = ORDER_R_PRODPLAN.ORDER_HISTNO
            AND ORDER_DETAIL.ORDER_SEQNO = ORDER_R_PRODPLAN.ORDER_SEQNO

            OUTER APPLY(
                SELECT
                      SUM(CASE WHEN SUB_C.WORK_CODE = '001' THEN ISNULL(SUB_C.PROD_QTY, 0) ELSE 0 END) AS PROD_QTY_WORK_001
                    , SUM(CASE WHEN SUB_C.WORK_CODE = '002' THEN ISNULL(SUB_C.PROD_QTY, 0) ELSE 0 END) AS PROD_QTY_WORK_002
                    , SUM(CASE WHEN SUB_C.WORK_CODE = '003' THEN ISNUEND) AS PROD_QTY_WORK_003
     , SUM(CASE WHEN SUB_C.WORK_CODE = '008' THEN ISNULL(SUB_C.PROD_QTY, 0) ELSE 0 END) AS PROD_QTY_WORK_008

                    -- 기존 SP의 WORK_NAME 우선순위 유지 : 001 → 002 → 003 → 004 → 005
                    , COALESCE
                      (
                          MAX(CASE WHEN SUB_C.WORK_CODE = '001' THEN SUB_C.WORK_CODE END)
                        , MAX(CASE WHEN SUB_C.WORK_CODE = '002' THEN SUB_C.WORK_CODE END)
                        , MAX(CASE WHEN SUB_C.WORK_CODE = '003' THEN SUB_C.WORK_CODE END)
                        , MAX(CASE WHEN SUB_C.WORK_CODE = '004' THEN SUB_C.WORK_CODE END)
                        , MAX(CASE WHEN SUB_C.WORK_CODE = '005' THEN SUB_C.WORK_CODE END)
                        , MAX(CASE WHEN SUB_C.WORK_CODE = '006' THEN SUB_C.WORK_CODE END)
                        , MAX(CASE WHEN SUB_C.WORK_CODE = '007' THEN SUB_C.WORK_CODE END)
                        , MAX(CASE WHEN SUB_C.WORK_CODE = '008' THEN SUB_C.WORK_CODE END)
                      ) AS WORK_CODE
                FROM dbo.TPR301R AS SUB_A WITH (NOLOCK)
                LEFT JOIN dbo.TPR301 AS SUB_B WITH (NOLOCK)
                    ON  SUB_A.FACTORY_CODE = SUB_B.FACTORY_CODE
                    AND SUB_A.PLANT_CODE = SUB_B.PLANT_CODE
                    AND SUB_A.PRODPLAN_DATE = SUB_B.PRODPLAN_DATE
                    AND SUB_A.PRODPLAN_SEQ = SUB_B.PRODPLAN_SEQ
                LEFT JOIN dbo.TPR601 AS SUB_C WITH (NOLOCK)
                    ON  SUB_B.FACTORY_CODE = SUB_C.FACTORY_CODE
                    AND SUB_B.PLANT_CODE = SUB_C.PLANT_CODE
                    AND SUB_B.PRODPLAN_DATE = SUB_C.PRODPLAN_DATE
                    AND SUB_B.PRODPLAN_SEQ = SUB_C.PRODPLAN_SEQ
                    AND SUB_C.WORK_CODE IN ('001', '002', '003', '004', '005', '006', '007','008')
                WHERE SUB_A.FACTORY_CODE = ORDER_DETAIL.FACTORY_CODE
                  AND SUB_A.PLANT_CODE = ORDER_DETAIL.PLANT_CODE
                  AND SUB_A.ORDER_NO = ORDER_DETAIL.ORDER_NO
                  AND SUB_A.ORDER_HISTNO = ORDER_DETAIL.ORDER_HISTNO
                  AND SUB_A.ORDER_SEQNO = ORDER_DETAIL.ORDER_SEQNO
★추가: 도면가공 상태(생산계획 단위 MAX PLATE_COMPLETE_FLAG)
            OUTER APPLY (
                SELECT MAX(SUB_C.PLATE_COMPLETE_FLAG) AS PLATE_FLAG
                FROM TPR301R SUB_A WITH(NOLOCK)
                LEFT JOIN TPR601 SUB_C WITH(NOLOCK)
                  ON SUB_A.FACTORY_CODE = SUB_C.FACTORY_CODE
                  AND SUB_A.PLANT_CODE  = SUB_C.PLANT_CODE
                  AND SUB_A.PRODPLAN_DATE = SUB_C.PRODPLAN_DATE
                  AND SUB_A.PRODPLAN_SEQ  = SUB_C.PRODPLAN_SEQ
                WHERE SUB_A.FACTORY_CODE = ORDER_DETAIL.FACTORY_CODE
                  AND SUB_A.ORDER_NO     = ORDER_DETAIL.ORDER_NO
                  AND SUB_A.ORDER_HISTNO = ORDER_DETAIL.ORDER_HISTNO
                  AND SUB_A.ORDER_SEQNO  = ORDER_DETAIL.ORDER_SEQNO
            ) PLATE_STATUS

            LEFT JOIN (
                 SELECT
                        FACTORY_CODE
                      , ORDER_NO
                      , ORDER_HISTNO
                      , ORDER_SEQNO
                      , SUM(ISNULL(SHIPPING_QTY, 0)) AS SHIPPING_QTY
                  FROM TSA403 WITH (NOLOCK)
                  GROUP BY FACTORY_CODE, ORDER_NO, ORDER_HISTNO, ORDER_SEQNO
              )    SHIP_DATA
              ON  ORDER_DETAIL.FACTORY_CODE = SHIP_DATA.FACTORY_CODE
              AND ORDER_DETAIL.ORDER_NO     = SHIP_DATA.ORDER_NO
              AND ORDER_DETAIL.ORDER_HISTNO = SHIP_DATA.ORDER_HISTNO
              AND ORDER_DETAIL.ORDER_SEQNO  = SHIP_DATA.ORDER_SEQNO

            LEFT JOIN TPR102 WORK with(nolock)
            ON WORK.WORK_CODE = PROD_WORK_ALL.WORK_CODE

            WHERE   ORDER_TABLE.FACTORY_CODE = @FACTORY_CODE
            AND        ORDER_TABLE.PLANT_CODE = @PLANT_CODE
            AND        ORDER_TABLE.ORDER_DATE BETWEEN @ORDER_DATE_FROM AND @ORDER_DATE_TO
            AND (
                    (@CLOSING_FLAG = '1' AND ISNULL(ORDER_DETAIL.CLOSING_FLAG,'0') IN ('0','1'))
                 OR (@CLOSING_FLAG = '2' AND ISNULL(ORDER_DETAIL.CLOSING_FLAG,'0') = '0')
                 OR (@CLOSING_FLAG = '3' AND ISNULL(ORDER_DETAIL.CLOSING_FLAG,'0') = '1')
                )
            AND        (@MATERIAL_QUALITY = '' OR (@MATERIAL_QUALITY <> '' AND MAT.MATERIAL_QUALITY= @MATERIAL_QUALITY))
            AND        (@THICKNESS = 0 OR (@THICKNESS <> 0 AND MAT.THICKNESS = @THICKNESS))
            AND        (@SPEC_X = 0 OR (@SPEC_X <> 0 AND MAT.SPEC_X = @SPEC_X))
            AND        (@SPEC_Y = 0 OR (@SPEC_Y <> 0 AND MAT.SPEC_Y = @SPEC_Y))
            AND        (@SEARCH_CUST_NAME = '' OR ( @SEARCH_CUST_NAME <>'' AND ISNULL(CUST.CUSTOMER_NAME, '') LIKE '%'+@SEARCH_CUST_NAME+'%'))
            AND        (@SEARCH_ITEM_NAME = '' OR ( @SEARCH_ITEM_NAME <>'' AND ISNULL(MAT.PART_NO, '') LIKE '%'+@SEARCH_ITEM_NAME+'%'))
            AND        (@SEARCH_P_NO_TRACK = '' OR ( @SEARCH_P_NO_TRACK <>'' AND ISNULL(GROUP_TABLE.P_NO_TRACK, '') LIKE '%'+@SEARCH_P_NO_TRACK+'%'))
            AND        (@ORDER_NO_TEMP = '' OR ( @ORDER_NO_TEMP <>'' AND ISNULL(ORDER_TABLE.ORDER_NO, '') LIKE '%' + @ORDER_NO_TEMP + '%'))
            AND (  (@FG_USE2_FLAG = '')
                OR (@FG_USE2_FLAG = '1' AND ISNULL(ORDER_DETAIL.FG_USE2, '') IN ('002', '003'))
                OR (@FG_USE2_FLAG = '0' AND ISNULL(ORDER_DETAIL.FG_USE2, '') NOT IN ('002', '003'))
               )

            ORDER BY ORDER_TABLE.ORDER_NO, ORDER_TABLE.ORDER_HISTNO, ORDER_DETAIL.ORDER_SEQNO
            OPTION (OPTIMIZE FOR UNKNOWN)
END
```

09-14 시점 남겨진 테스트용 참조값(도면가공 시연에 쓰인 품목/도면번호로 추정, 맥락 정보 없음): `11-20*50*800J`, `7B11BCFH0001`, `7A11BCFH0001`, `MSL20260916906`

## ✅ 검증 및 결과

설계는 완료됐고 위 3개 SP 스크립트는 검토 대기 상태, Java 3개 파일(`jvPROD_DATA_FETCH`/`ProdSLService`/`ProdReportService`) 실제 diff는 미작성 — [8. 다음 단계](#8-다음-단계) 항목 중 1번(스크립트 작성) 이후 진행 상황은 이 문서 기준으로 확인되지 않음. "확인된 리스크/잔여 이슈"(7번 항목)의 항목들도 아직 해소 여부 불명.

## 🔗 참고

- [[신진SM 개발 이력]] — 06-26/07-03의 초기 설계(창고코드 체계가 달랐던 시점) 포함 전체 타임라인
- [[신진SM - 더존 중복 문서처리 방어]] — 같은 `SP_WPR559_02_IUD_TEST`를 다루는 별도 작업(문서 중복 방지)
- [\[완료\] 포장중복문제 분석](<../02_TechDocs/[완료] 포장중복문제 분석.md>)
