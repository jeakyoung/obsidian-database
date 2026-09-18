---
title: 저장 프로시저 SP_WMA624_01_IUD - 계정 대체 출고 관리
date: 2026-06-11
type: 참고자료
project: 신진SM
status: 진행중
category: SQL
tags: []
database: iPlusERP_SJ
---

# 저장 프로시저 SP_WMA624_01_IUD - 계정 대체 출고 관리

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **용도** | 계정 대체 입/출고(TMA536) UPSERT + 재고 부족 검증 |
| **대상 시스템** | 신진SM ERP (`iPlusERP_SJ`) |
| **호출 위치** | `src/com/MA/WMA620/jvWMA624_01_IUD.java` (`service()`) |
| **최종 확인일** | 2026-09-18 (전문은 [[신진SM 05.28 업무 미팅]] 06-05 내용에 첨부된 백업 스크립트, 2026-06-08 10:44 수정본 기준) |

## ⚙️ 환경 및 전제

- DB: `iPlusERP_SJ`, 위치: `dbo.SP_WMA624_01_IUD`
- 이 SP는 **TMA536(계정대체출고) 테이블만** 다룬다. 더존(DZ) ERP 반영은 이 SP 안에서 일어나지 않고, 호출자인 `jvWMA624_01_IUD.java`가 SP 실행·커밋 이후 **별도 커넥션(`connDZ`)으로** 처리한다 — 자세한 흐름은 [\[통합\] 더존ERP 동기화](<[통합] 더존ERP 동기화.md>) 참고.

## 📖 상세 내용

### 매개변수

| 매개변수 | 타입 | 설명 |
|---------|------|------|
| @FACTORY_CODE | VARCHAR(6) | 사업장 코드 |
| @IO_NO | VARCHAR(12) | 입출고 번호. 빈 값이면 아래 "IO_NO 자동 생성" 참고 |
| @IO_FLAG | VARCHAR(3) | 1=입고, 2=출고 (Java에서 원본 `IO_FLAG` 405/406을 1/2로 변환해서 넘김) |
| @ACC_FLAG | VARCHAR(6) | 계정 코드 |
| @MATERIAL_CODE / @ALTER_MATERIAL_CODE | VARCHAR(30) | 자재 코드 / 대체 자재 코드 |
| @IO_DATE | VARCHAR(8) | 거래 일자 (YYYYMMDD) |
| @IO_CHARGE | VARCHAR(10) | 입출고 담당 구분 |
| @IO_QTY | FLOAT | 입출고 수량 |
| @OUT_WAREHOUSE_CODE / @OUT_LOCATION_CODE | VARCHAR(6) | 출고 창고/위치 |
| @IN_WAREHOUSE_CODE / @IN_LOCATION_CODE | VARCHAR(6) | 입고 창고/위치 |
| @REMARK | VARCHAR(255) | 비고 |
| @OPMAN_CODE | VARCHAR(10) | 조작자 코드 |
| @SYSTEM_LOT_NO / @ALTER_SYSTEM_LOT_NO | VARCHAR(30) | LOT 번호 / 대체 LOT |
| @EXPIRE_DATE / @MANUFACTURE_DATE | VARCHAR(8) | 유효기간 / 제조일자 |
| @PLANT_CODE | VARCHAR(10) | 공장 코드 (기본값 `''`) |
| @IRU | CHAR(2) | `IU`=삽입/수정, 그 외=삭제 |

### 동작 요약 (실제 SP 본문 기준)

#### 1. IO_NO 자동 생성 (호출자가 빈 값을 넘겼을 때만)

```sql
IF @IO_NO = ''
BEGIN
    DECLARE @DATE VARCHAR(12)
    SET @DATE = REPLACE(REPLACE(REPLACE(CONVERT(VARCHAR(10), GETDATE(), 120), '-', ''), ':',''), ' ', '')
    SELECT @IO_NO = @DATE + RIGHT('0000'+LTRIM(STR(ISNULL(MAX(SUBSTRING(IO_NO,9,4)), 0) + 1)),4)
    FROM TMA536 WITH(NOLOCK)
    WHERE SUBSTRING(IO_NO,1,8) = @DATE
END
```

`YYYYMMDD` + 당일 4자리 순번(`WITH(NOLOCK)`으로 MAX 조회 후 +1). **동시에 두 요청이 이 분기를 타면 같은 번호를 받을 수 있는 구조**다 — `NOLOCK` + 잠금 없는 read-then-increment라 레이스 컨디션이 이론상 존재한다.

> [!note] 실제로는 이 분기가 거의 안 탄다
> `jvWMA624_01_IUD.java`는 더존 연결(`connDZ`)이 성공하면 이 SP를 호출하기 *전에* 더존의 `NEOE.CP_GETNO`로 IO_NO를 미리 채번해서 넘긴다(입고/출고 배치당 1개씩 공유). 이 자동 생성 분기는 **더존 연결 실패 시 폴백 경로**로만 동작한다. 즉 SP 자체의 채번 규칙과, 평소 실제로 쓰이는 IO_NO(더존 발번)는 서로 다른 체계다.

#### 2. 재고 부족 검증 (`@IO_FLAG = '2'`, 출고일 때만)

```sql
-- MAT: TMA922M(재고 현황 뷰) 기준 현재고, B: TMA922에서 @IO_DATE 이전 누계
-- MAT.STOCK_QTY < @IO_QTY 이면 @CNT = 1 → RAISERROR
IF @CNT = 1
BEGIN
    SET @ERR_MSG = '[LOT] ' + @SYSTEM_LOT_NO + ' 현재재고가 변경되어 수량이 부족합니다.'
    RAISERROR (@ERR_MSG,16,1) with log;
END
```

입고(`@IO_FLAG='1'`)일 때는 이 검증 자체가 없다. 참고: 대체 조건 `(B.TARGET_QTY > @IO_QTY) AND MAT.STOCK_QTY - (B.TARGET_QTY - @IO_QTY) < 0`는 주석 처리된 채 남아 있다 — 과거 다른 기준으로 검증하다가 현재의 단순 `MAT.STOCK_QTY < @IO_QTY` 조건으로 바뀐 흔적.

#### 3. UPSERT (UPDATE 우선, `@@ROWCOUNT = 0`이면 INSERT)

`@IRU = 'IU'`일 때: `WHERE FACTORY_CODE = @FACTORY_CODE AND IO_NO = @IO_NO` 조건으로 UPDATE 시도 → 영향받은 행이 0개면 같은 값으로 INSERT. `@IRU`가 그 외 값이면 동일 키로 DELETE.

> [!warning] 호출부는 파라미터를 문자열로 직접 이어붙인다
> `jvWMA624_01_IUD.java`는 `PreparedStatement`를 쓰지만 실제로는 `"EXEC SP_WMA624_01_IUD ... @X = '" + value + "'"` 형태로 SQL 문자열을 조립한 뒤 `prepareStatement(sql)`에 넣는다(바인드 파라미터 미사용). 각 값은 `.replace("'", "''")`로 수동 이스케이프만 되어 있다. 이 파일의 다른 서블릿들(`jvWMA624_01_VERIFY` 등)도 동일 패턴 — 이 프로젝트 전반의 기존 스타일이라 이 문서만으로 고칠 범위는 아니지만, 값 검증 없이 신뢰할 수 없는 입력이 들어오는 화면이 있다면 SQL 인젝션 여지가 있다는 점은 기록해 둔다.

### 관련 조회 프로시저

```sql
EXEC SP_WMA624_01_LIST
    @FACTORY_CODE = '000001', @DATE = '20260528', @SEARCH_NAME = '',
    @WAREHOUSE_CODE = '001', @OPMAN_CODE = '0000', @PLANT_CODE = '000001',
    @MATERIAL_QUALITY = ''
```

`SP_WMA624_01_LIST`는 2026-09-04에 `TCO403.PLANT_CODE`와 `TMA922.PLANT_CODE` 불일치로 품목이 조회 안 되던 문제 때문에 수정됐다 — 자세한 diff는 [[신진SM MES 품목 정보 조치 방안]] 참고.

### 관련 테이블

| 테이블 | 역할 |
|---|---|
| `TMA536` | 계정 대체 입/출고 (이 SP가 직접 쓰는 테이블) |
| `TMA922` / `TMA922M` | 재고 이력 / 재고 현황(뷰) — 재고 부족 검증에 사용 |
| `ESMMTGL` | 재고 부족 검증 서브쿼리의 기준 테이블 (품목 마스터 성격) |
| `TCO102` | 창고 코드 ↔ 더존 창고 코드(`ETC`) 매핑 |
| `TCO403` | MES 자재코드 ↔ 더존 품목코드(`PART_NO`) 매핑 |

## ⚠️ 주의사항

1. `@IO_DATE` 등 날짜류는 반드시 `YYYYMMDD` 8자리.
2. `@IO_FLAG='2'`(출고) 시에만 재고 부족 검증이 돈다 — 입고는 검증 없음.
3. `@IO_NO`를 직접 채워서 호출하면 UPSERT 특성상 기존 행을 덮어쓴다. 보통은 빈 값으로 호출해 자동 채번(또는 더존 CP_GETNO 채번값)에 맡긴다.
4. 이 SP는 더존 반영을 하지 않는다 — 더존까지 반영하려면 반드시 `jvWMA624_01_IUD.java` 경유([\[통합\] 더존ERP 동기화](<[통합] 더존ERP 동기화.md>)). SP를 다른 배치/스크립트에서 직접 호출하면 더존 장부와 어긋난다.

## 🔗 참고

- `src/com/MA/WMA620/jvWMA624_01_IUD.java`
- `src/com/MA/WMA620/jvWMA624_01_VERIFY.java` (동일 패턴의 조회 전용 서블릿, `SP_WMA624_01_VERIFY` 호출)
- [\[통합\] 더존ERP 동기화](<[통합] 더존ERP 동기화.md>)
- [\[완료\] 포장중복문제 분석](<../02_TechDocs/[완료] 포장중복문제 분석.md>)
- [\[완료\] 재고보정 및 데이터동기화](<../02_TechDocs/[완료] 재고보정 및 데이터동기화.md>)
- [[신진SM 중복 포장문제 ( 05.22 )]]
- [[신진SM MES 품목 정보 조치 방안]]
