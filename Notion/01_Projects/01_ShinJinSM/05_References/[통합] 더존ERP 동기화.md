---
type: 참고문서
title: 더존 ERP와의 데이터 동기화 방식
category: 통합
system: 더존(DZ) ERP / 신진SM ERP
---

# 더존 ERP와의 데이터 동기화

## 시스템 구조

```
신진SM 시스템                더존(DZ) ERP
(우리 ERP/MES)        ↔      (고객사 ERP)
                    
- TMA536 (계정대체출고)       - UP_PU_ITR_UPDATE
- TMA922 (재고이력)           - UP_PU_CGI_UPDATE
- TPR601M (투입자재)          - 기타 조정 함수
```

---

## 데이터 동기화 함수

### UP_PU_ITR_UPDATE - 입고 조정

**목적:** 입고(구매입고) 정정 및 조정  
**호출 시기:** 재고 입고 처리 후  
**파라미터:**
```
materialCode    - 자재 코드
systemLotNo     - 시스템 LOT 번호
qty             - 조정 수량
warehouseCode   - 입고 창고 코드
```

### UP_PU_CGI_UPDATE - 기타 조정

**목적:** 비용 가동/개산 조정  
**호출 시기:** 특수한 비용 처리 필요시

---

## Java 연동 코드

### 더존 ERP 데이터베이스 연결

```java
private Connection getConnectionDZ(ServletRequest request, ServletContext sc) throws Exception {
    // 더존 ERP 데이터베이스 드라이버 로드
    Class.forName(sc.getInitParameter("driver")).newInstance();
    
    // 더존 ERP 데이터베이스 연결
    return DriverManager.getConnection(
        sc.getInitParameter("urlDZ"),           // 더존 DB URL
        sc.getInitParameter("usernameDZ"),       // 더존 DB 사용자
        sc.getInitParameter("passwordDZ")        // 더존 DB 비밀번호
    );
}
```

### 환경 설정 (web.xml)

```xml
<context-param>
    <param-name>driver</param-name>
    <param-value>com.microsoft.sqlserver.jdbc.SQLServerDriver</param-value>
</context-param>

<context-param>
    <param-name>urlDZ</param-name>
    <param-value>jdbc:sqlserver://[더존_서버_IP]:1433;databaseName=더존_DB명;...</param-value>
</context-param>

<context-param>
    <param-name>usernameDZ</param-name>
    <param-value>[더존_DB_사용자]</param-value>
</context-param>

<context-param>
    <param-name>passwordDZ</param-name>
    <param-value>[더존_DB_비밀번호]</param-value>
</context-param>
```

---

## 동기화 프로세스

### 정상 흐름

```
신진SM 저장 요청
    ↓
SP_WMA624_01_IUD 실행
    ├─ TMA536 업데이트/삽입
    ├─ TMA922 업데이트
    ↓
트랜잭션 검증 (재고 부족 체크)
    ↓
더존 ERP 연결
    ↓
UP_PU_ITR_UPDATE 호출
    ↓
더존 DB 업데이트 (입고 조정)
    ↓
트랜잭션 COMMIT
    ↓
완료 응답
```

### 오류 흐름 (현재 문제)

```
신진SM 저장 요청
    ↓
SP_WMA624_01_IUD 실행
    ├─ TMA536 업데이트/삽입 ✓
    ├─ TMA922 업데이트 ✓
    ↓
트랜잭션 COMMIT ✓
    ↓
[타임아웃 발생]
    ↓
더존 ERP 연결 ✗ (미실행 또는 지연)
    ↓
[문제] 신진SM: 완료, 더존: 미반영
       또는
       신진SM: 미처리, 더종: 완료 (경쟁 조건)
```

---

## 동기화 수정 계획

### 단계 1: 순차 처리 보장

```java
public void syncMESToERP(String materialCode, String systemLotNo, float qty) throws Exception {
    Connection dzConn = null;
    try {
        // 1단계: 신진SM 처리
        executeStoredProcedure("SP_WMA624_01_IUD", params);
        
        // 2단계: 더존 연결 (동기식)
        dzConn = getConnectionDZ(request, sc);
        
        // 3단계: 더존 함수 호출
        callDozenFunction(dzConn, "UP_PU_ITR_UPDATE", 
            materialCode, systemLotNo, qty);
        
        // 4단계: 트랜잭션 커밋
        dzConn.commit();
        
        // 5단계: 성공 로깅
        logSyncSuccess(materialCode, systemLotNo);
        
    } catch (Exception e) {
        // 롤백 처리
        if (dzConn != null) dzConn.rollback();
        logSyncError(e);
        throw e;
    } finally {
        if (dzConn != null) dzConn.close();
    }
}
```

### 단계 2: 더존 함수 호출 래퍼

```java
private void callDozenFunction(Connection dzConn, String funcName, 
        String materialCode, String systemLotNo, float qty) throws Exception {
    
    String sql = "EXEC " + funcName + " @MATERIAL_CODE=?, @SYSTEM_LOT_NO=?, @QTY=?";
    
    try (PreparedStatement pstmt = dzConn.prepareStatement(sql)) {
        pstmt.setString(1, materialCode);
        pstmt.setString(2, systemLotNo);
        pstmt.setFloat(3, qty);
        
        // 타임아웃 설정 (5초)
        pstmt.setQueryTimeout(5);
        
        int result = pstmt.executeUpdate();
        
        if (result == 0) {
            throw new Exception("더존 ERP 함수 실행 실패: " + funcName);
        }
        
    } catch (SQLException e) {
        throw new Exception("더존 ERP 연동 오류 [" + funcName + "]: " + e.getMessage());
    }
}
```

### 단계 3: 타임아웃 재시도

```java
private void callDozenFunctionWithRetry(Connection dzConn, String funcName,
        String materialCode, String systemLotNo, float qty, int maxRetries) throws Exception {
    
    int attempts = 0;
    long backoffMs = 1000;  // 시작: 1초
    
    while (attempts < maxRetries) {
        try {
            callDozenFunction(dzConn, funcName, materialCode, systemLotNo, qty);
            return;  // 성공
        } catch (Exception e) {
            attempts++;
            
            if (attempts >= maxRetries) {
                throw e;  // 최종 실패
            }
            
            // Exponential backoff
            Thread.sleep(backoffMs);
            backoffMs *= 2;  // 2초, 4초, 8초...
            
            logRetryAttempt(funcName, attempts, e);
        }
    }
}
```

---

## 데이터 매핑

### 신진SM TMA536 → 더존 UP_PU_ITR_UPDATE

| 신진SM | 더존 | 설명 |
|--------|------|------|
| MATERIAL_CODE | @MATERIAL_CODE | 자재 코드 |
| SYSTEM_LOT_NO | @SYSTEM_LOT_NO | LOT 번호 |
| IO_QTY | @QTY | 수량 |
| WAREHOUSE_CODE | @WAREHOUSE_CODE | 창고 |
| IO_DATE | @IO_DATE | 거래 일자 |
| ACC_FLAG | @ACC_FLAG | 계정 코드 |

---

## 동기화 상태 모니터링

### 로깅 항목

```java
public class SyncLog {
    String materialCode;
    String systemLotNo;
    long startTime;
    long endTime;
    String status;  // SUCCESS, FAILED, TIMEOUT
    String errorMsg;
    int retryCount;
}
```

### 조회 쿼리

```sql
-- 동기화 실패 목록
SELECT *
FROM SYNC_LOG
WHERE STATUS = 'FAILED'
AND SYNC_DATE >= DATEADD(DAY, -1, GETDATE())
ORDER BY SYNC_DATE DESC
```

---

## 더존 ERP 함수 확인

### 더존에서 확인 필요한 항목

1. **UP_PU_ITR_UPDATE 함수 위치**
   ```
   데이터베이스: [더존_DB명]
   스키마: dbo
   함수명: UP_PU_ITR_UPDATE
   ```

2. **파라미터 확인**
   - 정확한 파라미터명
   - 데이터 타입
   - 필수/선택 여부

3. **반환값**
   - 성공/실패 코드
   - 오류 메시지

---

## 테스트 시나리오

### 시나리오 1: 정상 동기화

```
1. 신진SM에서 입고 처리
2. 더존 ERP에 UP_PU_ITR_UPDATE 호출
3. 양쪽 모두 데이터 반영 확인
```

### 시나리오 2: 타임아웃 후 재시도

```
1. 신진SM에서 입고 처리
2. 더존 연결 타임아웃 (5초)
3. 자동 재시도 (1초 후)
4. 성공 확인
```

### 시나리오 3: 실패 및 롤백

```
1. 신진SM에서 입고 처리
2. 더존 함수 실행 실패
3. 신진SM 트랜잭션 롤백
4. 동기화 로그에 기록
```

---

## 참고 링크

- [[20260605] 포장중복문제 및 성능최적화]] - 기술 논의
- [[진행중] 포장중복문제 분석]] - 근본 원인
- [[진행중] 재고보정 및 데이터동기화]] - 구현 계획

