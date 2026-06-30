---
type: 참고문서
title: 저장 프로시저 SP_WMA624_01_IUD - 계정 대체 출고 관리
category: SQL
database: iPlusERP_SJ
---

# SP_WMA624_01_IUD - 계정 대체 출고 관리

## 프로시저 개요

신진SM ERP 시스템의 **계정 대체 출고(TMA536)** 데이터를 관리하는 핵심 저장 프로시저

**데이터베이스:** `iPlusERP_SJ`  
**위치:** `dbo.SP_WMA624_01_IUD`  
**마지막 수정:** 2026-06-08 10:44:37

---

## 매개변수

| 매개변수 | 타입 | 설명 |
|---------|------|------|
| @FACTORY_CODE | VARCHAR(6) | 사업장 코드 (필수) |
| @IO_NO | VARCHAR(12) | 입출고 번호 (빈값시 자동생성) |
| @IO_FLAG | VARCHAR(3) | 입출고 구분: 1=입고, 2=출고 |
| @ACC_FLAG | VARCHAR(6) | 계정 코드 |
| @MATERIAL_CODE | VARCHAR(30) | 자재 코드 |
| @ALTER_MATERIAL_CODE | VARCHAR(30) | 대체 자재 코드 |
| @IO_DATE | VARCHAR(8) | 거래 일자 (YYYYMMDD) |
| @IO_CHARGE | VARCHAR(10) | 입출고 담당자 |
| @IO_QTY | FLOAT | 입출고 수량 |
| @OUT_WAREHOUSE_CODE | VARCHAR(6) | 출고 창고 코드 |
| @OUT_LOCATION_CODE | VARCHAR(6) | 출고 위치 코드 |
| @IN_WAREHOUSE_CODE | VARCHAR(6) | 입고 창고 코드 |
| @IN_LOCATION_CODE | VARCHAR(6) | 입고 위치 코드 |
| @REMARK | VARCHAR(255) | 비고 |
| @OPMAN_CODE | VARCHAR(10) | 조작자 코드 |
| @SYSTEM_LOT_NO | VARCHAR(30) | 시스템 LOT 번호 |
| @ALTER_SYSTEM_LOT_NO | VARCHAR(30) | 대체 LOT 번호 |
| @EXPIRE_DATE | VARCHAR(8) | 유효 기간 (YYYYMMDD) |
| @MANUFACTURE_DATE | VARCHAR(8) | 제조 일자 (YYYYMMDD) |
| @PLANT_CODE | VARCHAR(10) | 공장 코드 (기본값: '') |
| @IRU | CHAR(2) | 입출고 구분 (IU) |

---

## 주요 기능

### 1. IO_NO 자동 생성
```sql
IF @IO_NO = '' BEGIN
    DECLARE @DATE VARCHAR(12)
    SET @DATE = REPLACE(REPLACE(REPLACE(CONVERT(VARCHAR(10), GETDATE(), 120), '-', ''), ':',''), ' ', '')
    SELECT @IO_NO = @DATE + RIGHT('0000'+LTRIM(STR(ISNULL(MAX(SUBSTRING(IO_NO,9,4)), 0) + 1)),4)
    FROM TMA536 WITH(NOLOCK)
    WHERE SUBSTRING(IO_NO,1,8) = @DATE
END
```

**생성 방식:** `YYYYMMDD + 0001` (일일 순번)

### 2. 재고 부족 검증 (IO_FLAG = '2' 출고시)
```sql
IF @IO_FLAG = '2' BEGIN
    -- 재고량 정보 JOIN
    SELECT @CNT = COUNT(*)
    FROM ESMMTGL AS A
    LEFT JOIN (재고량 집계) AS MAT ON ...
    LEFT JOIN (재고 이력) AS B ON ...
    WHERE A.WERKS = @PLANT_CODE 
      AND A.ITEM_CD = @MATERIAL_CODE
      AND MAT.WAREHOUSE_CODE = @OUT_WAREHOUSE_CODE
      AND MAT.SYSTEM_LOT_NO = @SYSTEM_LOT_NO
      AND MAT.STOCK_QTY < @IO_QTY  -- 재고 부족 체크
    
    IF @CNT = 1 BEGIN
        SET @ERR_MSG = '[LOT] ' + @SYSTEM_LOT_NO + ' 현재재고가 변경되어 수량이 부족합니다.'
        RAISERROR (@ERR_MSG, 16, 1) WITH LOG
    END
END
```

### 3. 데이터 관리 (IUD)
- **U(Update):** 기존 데이터 수정
- **I(Insert):** 신규 데이터 생성
- **D(Delete):** @IRU ≠ 'IU'일 때 삭제

---

## 사용 예시

### 입고 처리 (IO_FLAG = '1')
```sql
EXEC SP_WMA624_01_IUD
    @FACTORY_CODE = '000001',
    @IO_NO = '',  -- 자동 생성
    @IO_FLAG = '1',
    @ACC_FLAG = '001',
    @MATERIAL_CODE = '',
    @ALTER_MATERIAL_CODE = '0000792977',
    @IO_DATE = '20260528',
    @IO_CHARGE = '0000',
    @IO_QTY = 5,
    @OUT_WAREHOUSE_CODE = '',
    @OUT_LOCATION_CODE = '',
    @IN_WAREHOUSE_CODE = '001',
    @IN_LOCATION_CODE = '000000',
    @REMARK = '입고 처리',
    @OPMAN_CODE = '0000',
    @SYSTEM_LOT_NO = 'A0000116371',
    @ALTER_SYSTEM_LOT_NO = 'A0000116371',
    @EXPIRE_DATE = '',
    @MANUFACTURE_DATE = '',
    @PLANT_CODE = '000001',
    @IRU = 'IU'
```

**결과:** TMA536 테이블에 신규 레코드 생성

### 출고 처리 (IO_FLAG = '2')
```sql
EXEC SP_WMA624_01_IUD
    @FACTORY_CODE = '000001',
    @IO_NO = '202605280001',  -- 기존 번호
    @IO_FLAG = '2',
    @OUT_WAREHOUSE_CODE = '001',
    @OUT_QTY = 3,
    -- 기타 매개변수...
    @IRU = 'IU'
```

**검증:** 창고 '001'의 LOT 'A0000116371' 재고 3개 이상 필수

---

## 조회 프로시저

### SP_WMA624_01_LIST
```sql
EXEC SP_WMA624_01_LIST
    @FACTORY_CODE = '000001',
    @DATE = '20260528',
    @SEARCH_NAME = '',
    @WAREHOUSE_CODE = '001',
    @OPMAN_CODE = '0000',
    @PLANT_CODE = '000001',
    @MATERIAL_QUALITY = ''
```

---

## 관련 테이블

### TMA536 - 계정 대체 출고
```sql
CREATE TABLE TMA536 (
    FACTORY_CODE VARCHAR(6),
    IO_NO VARCHAR(12) PRIMARY KEY,
    IO_FLAG VARCHAR(3),
    MATERIAL_CODE VARCHAR(30),
    SYSTEM_LOT_NO VARCHAR(30),
    WAREHOUSE_CODE VARCHAR(6),
    IO_QTY FLOAT,
    IO_DATE VARCHAR(8),
    -- 기타 칼럼...
)
```

### TMA922M - 재고 현황 (VIEW)
```
입고누계(IN_QTY) - 출고누계(OUT_QTY) = 현재 재고(STOCK_QTY)
```

### ESMMTGL - SAP 통합 데이터
```
재고 기본 정보 조인 대상
```

---

## 주의사항

⚠️ **중요:**
1. @IO_DATE 형식: 반드시 **YYYYMMDD** 형식 사용
2. @IO_FLAG = '2' (출고)시 재고 부족 검증 필수
3. 타임아웃 시 트랜잭션 롤백 자동 처리
4. 대규모 배치 처리시 성능 영향 고려

---

## 최근 수정 사항

### 2026-06-08 수정
- 재고 부족 검증 로직 강화
- ERP/MES 동기화 오류 처리 추가 (진행중)
- 타임아웃 재시도 메커니즘 구현 (진행중)

---

## 트러블슈팅

### 오류: "현재재고가 변경되어 수량이 부족합니다"
**원인:** 출고 수량이 현재 재고보다 큼  
**해결:** 재고 현황 확인 후 수량 조정

### 오류: "타임아웃"
**원인:** 대량 데이터 처리 중 시간 초과  
**해결:** 배치 크기 축소 또는 성능 최적화 필요

### 문제: ERP에는 반영되지만 MES에는 미반영
**원인:** 더존 동기화 함수(UP_PU_ITR_UPDATE) 미호출  
**해결:** 프로시저 호출 후 동기화 함수 추가 호출 필요

---

## 관련 문서

- [[20260605] 포장중복문제 및 성능최적화]] - 기술 논의
- [[진행중] 포장중복문제 분석]] - 근본 원인 분석
- [[진행중] 재고보정 및 데이터동기화]] - 구현 계획

