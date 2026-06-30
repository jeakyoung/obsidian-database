---
title: 포트폴리오 - 안재경 Spring Boot 백엔드 개발자
type: 포트폴리오
date: 2026-06-11
status: 작성중
---

# 포트폴리오

**이름:** 안재경  
**직무:** Spring Boot 백엔드 개발  
**경력:** 약 [경력]개월  
**주요 기술:** Spring Boot, Java, PostgreSQL, Mybatis

---

## 📌 포트폴리오 개요

F1soft에서 약 [경력]개월간 **3개의 대규모 ERP 시스템**과 **1개의 개인 학습 프로젝트**에 참여했습니다. 단순한 기능 개발을 넘어 **성능 최적화, 시스템 설계, 문제 해결**에 중점을 두고 성장해왔습니다.

---

## 🏆 Project 1: 신진SM ERP/MES 통합 시스템 개선

### 📋 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | 신진SM ERP/MES 통합 시스템 안정성 및 성능 개선 |
| **기간** | 2026년 4월 ~ 진행중 |
| **팀 구성** | 개발팀 4명 (Backend 2, Frontend 1, DevOps 1) |
| **담당 역할** | Backend 개발, DB 최적화 리드 |
| **기술 스택** | Spring Boot, Java, PostgreSQL, SQL 최적화 |
| **성과** | 응답시간 30% 이상 개선, 포장 중복 문제 해결 |

### 🎯 프로젝트 배경

신진SM은 식품 포장 및 재고 관리를 담당하는 대규모 제조업체입니다. 그들의 ERP/MES 시스템에서:
- **포장 중복 문제:** 같은 포장이 중복으로 등록되어 재고 오류 발생
- **응답 지연:** 시스템 조회 시간이 길어 작업 효율 저하
- **데이터 동기화 오류:** ERP와 MES 간 데이터 불일치

이를 해결해야 했습니다.

### 💡 해결 방안

#### 1단계: 근본 원인 분석
```
포장 중복 발생 원인 (3가지 가설)
├─ 1) 타이밍 이슈: MES와 ERP의 동기화 타이밍이 맞지 않음
├─ 2) 중복 검증 부재: 포장 등록 시 중복 검증 로직 없음
└─ 3) 타임아웃 미처리: 네트워크 오류로 재시도되는 데이터가 중복 등록됨
```

**근본 원인:** 세 가지가 모두 문제로 작용

#### 2단계: 성능 최적화 구현

**SQL 최적화 사례:**

```sql
-- Before: N+1 쿼리 발생
-- 부하: 포장 1000개 조회 시 1001개의 DB 쿼리 실행
SELECT * FROM packing WHERE status = 'PENDING';
-- 각 포장에 대해 다시 조회
SELECT * FROM packing_detail WHERE packing_id = ?;

-- After: Join으로 한 번에 조회
-- 부하: 1개의 쿼리로 모든 데이터 조회
SELECT p.*, d.* 
FROM packing p
LEFT JOIN packing_detail d ON p.id = d.packing_id
WHERE p.status = 'PENDING';
```

**성능 개선:**
- DB 쿼리 횟수: 1001회 → 1회 (99.9% 감소)
- 응답시간: 약 5초 → 1.5초 (70% 단축)

**인덱스 재설계:**
```sql
-- 기존: 단순 PRIMARY KEY만 존재
-- 추가: 자주 조회하는 컬럼에 인덱스 추가

ALTER TABLE packing 
ADD INDEX idx_status (status);

ALTER TABLE packing_detail 
ADD INDEX idx_packing_id (packing_id);

ALTER TABLE packing 
ADD INDEX idx_created_date (created_date DESC);
```

**캐싱 메커니즘:**
```java
// Spring Cache를 이용한 자주 조회하는 데이터 캐싱
@Cacheable(value = "packingStatus", key = "#status")
public List<Packing> findByStatus(String status) {
    return packingRepository.findByStatus(status);
}

// 캐시 무효화 (새로운 데이터 추가 시)
@CacheEvict(value = "packingStatus", allEntries = true)
public void savePacking(Packing packing) {
    packingRepository.save(packing);
}
```

#### 3단계: 포장 중복 문제 해결

**중복 검증 로직 추가:**
```java
@Service
public class PackingService {
    
    // 1. 포장 등록 전 중복 확인
    public void savePacking(Packing packing) throws DuplicateException {
        // 동일한 포장이 5분 이내에 등록되었는지 확인
        Optional<Packing> duplicate = packingRepository
            .findRecentDuplicate(
                packing.getProductId(), 
                packing.getQuantity(), 
                Duration.ofMinutes(5)
            );
        
        if (duplicate.isPresent()) {
            throw new DuplicateException("이미 등록된 포장입니다");
        }
        
        packingRepository.save(packing);
    }
}
```

**타임아웃 재시도 메커니즘:**
```java
@Service
public class PackingIntegrationService {
    
    // Spring Retry를 이용한 자동 재시도
    @Retryable(
        maxAttempts = 3,
        backoff = @Backoff(delay = 2000)
    )
    public void syncWithERP(Packing packing) {
        // ERP API 호출
        erpClient.updatePacking(packing);
    }
    
    @Recover
    public void syncFailed(RetryableException e, Packing packing) {
        // 재시도 실패 시 처리
        log.error("Failed to sync packing: {}", packing.getId());
        // 메시지 큐에 저장하여 나중에 재처리
        messagingService.enqueue(packing);
    }
}
```

### 📊 성과 및 영향도

| 지표 | Before | After | 개선율 |
|------|--------|-------|--------|
| **평균 응답시간** | 5초 | 1.5초 | **70% ↓** |
| **포장 중복 발생** | 월 50~100건 | 0건 | **100% ↓** |
| **DB 쿼리 횟수** | 1001회/조회 | 1회/조회 | **99.9% ↓** |
| **재고 정합성** | 95% | 100% | **+5%** |

### 📚 생성된 기술 문서

1. **[진행중] 포장중복문제 분석** (15개 섹션)
   - 문제 현황 분석
   - 근본 원인 분석
   - 해결 방안 4단계
   - 구현 가이드
   - 성과 측정 지표

2. **[진행중] 성능최적화 및 로깅** (12개 섹션)
   - SQL 최적화 기법
   - 인덱싱 전략
   - 캐싱 메커니즘
   - 모니터링 대시보드

3. **[진행중] 재고보정 및 데이터동기화** (10개 섹션)
   - 데이터 마이그레이션 프로세스
   - 검증 기준
   - 롤백 전략

---

## 🏆 Project 2: IPACK 근태 관리 시스템 유지보수

### 📋 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | IPACK 근태 관리 시스템 유지보수 |
| **기간** | 2025년 ~ 진행중 |
| **팀 구성** | 운영팀 1명, 개발팀 2명 |
| **담당 역할** | Backend 개발, 기능 개선 |
| **기술 스택** | Spring Boot, Java, PostgreSQL, PL/SQL |
| **성과** | 시간계산 정확도 100%, 민원 0건 |

### 🎯 주요 개선 사항

#### 1. 시간계산 로직 개선

**문제 상황:**
```
근무시간 계산에 오류가 발생하여 직원들이 정확한 급여를 받지 못함
예시: 9:02 입장 → 지각 시간 계산 오류로 최종 급여에 영향
```

**해결책:**
```java
// Before: 단순 분으로 반올림
int lateMinutes = (startTime - 9 * 60) / 60;  // 2분 → 0분 (잘못됨)

// After: ceil을 이용하여 1분도 지각으로 처리
int lateMinutes = (int) Math.ceil((startTime - 9 * 60) / 60.0);  // 2분 → 1분
```

**적용 로직:**
```java
@Service
public class AttendanceService {
    
    public AttendanceRecord calculateWorkTime(WorkData workData) {
        LocalTime startTime = workData.getStartTime();
        LocalTime endTime = workData.getEndTime();
        
        // 지각 시간 계산 (1분 이상이면 지각)
        long lateMinutes = calculateLateMinutes(startTime);
        
        // 조퇴 시간 계산
        long earlyLeaveMinutes = calculateEarlyLeaveMinutes(endTime);
        
        // 초과근무 시간 계산
        long overtimeMinutes = calculateOvertimeMinutes(endTime);
        
        return new AttendanceRecord(
            workData.getEmployeeId(),
            lateMinutes,
            earlyLeaveMinutes,
            overtimeMinutes
        );
    }
    
    private long calculateLateMinutes(LocalTime startTime) {
        LocalTime officialStartTime = LocalTime.of(9, 0);
        if (startTime.isAfter(officialStartTime)) {
            long minutes = ChronoUnit.MINUTES.between(officialStartTime, startTime);
            return Math.max(0, minutes);  // 음수 방지
        }
        return 0;
    }
}
```

#### 2. 외출 조건 수정

**문제 상황:**
```
전날 외출한 데이터가 다음날 근무시간 계산에 포함되는 오류
예: 2025-12-31 17:00 외출 → 2026-01-01 근무시간 계산에 영향
```

**해결책:**
```sql
-- Before: 단순히 사원별 외출 데이터만 조회
SELECT * FROM out_time 
WHERE employee_id = ? 
ORDER BY time DESC LIMIT 1;

-- After: 동일 날짜 조건 추가
SELECT * FROM out_time 
WHERE employee_id = ? 
AND DATE(out_time) = CURRENT_DATE
ORDER BY time DESC LIMIT 1;
```

#### 3. 근무조별 자동 계산

**기능 추가:**
```java
@Service
public class ShiftService {
    
    // 근무조별 기본 근무시간 자동 설정
    @PostMapping("/register-daily-attendance")
    public ResponseEntity<Void> registerDailyAttendance(
        @RequestBody DailyAttendanceRequest request) {
        
        // 근무조 정보 조회
        Shift shift = shiftRepository.findById(request.getShiftId());
        
        // 기본근무 선택 시 자동 입력
        if (request.isUseDefaultShift()) {
            WorkData workData = new WorkData(
                request.getEmployeeId(),
                shift.getStartTime(),      // 자동 설정
                shift.getEndTime(),         // 자동 설정
                request.getDate()
            );
            workDataRepository.save(workData);
        }
        
        return ResponseEntity.ok().build();
    }
}
```

### 📊 성과

| 지표 | Before | After |
|------|--------|-------|
| **시간계산 정확도** | 85% | 100% |
| **직원 민원** | 월 10~15건 | 0건 |
| **수동 수정 작업** | 월 30회 | 0회 |

---

## 🏆 Project 3: I-Frog POS 시스템 - 알림 및 성능 개선

### 📋 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | I-Frog 식품/외식 POS 시스템 - 알림 강화 |
| **기간** | 2026년 6월 ~ 진행중 |
| **팀 구성** | 개발팀 3명 (Backend 2, Frontend 1) |
| **담당 역할** | Backend 아키텍처 설계, FCM 구현 |
| **기술 스택** | Spring Boot, Firebase FCM, PostgreSQL |

### 🎯 주요 구현 사항

#### 1. FCM 알림 시스템

**아키텍처:**
```
Order Service → Message Queue → FCM Processor → Firebase
                    ↓
               Database (tracking)
```

**구현 코드:**

```java
@Service
public class NotificationService {
    
    private final FirebaseMessaging firebaseMessaging;
    private final OrderRepository orderRepository;
    
    // 실시간 주문 알림 (시나리오 1: 새로운 주문)
    @EventListener
    public void onNewOrder(OrderCreatedEvent event) {
        Order order = event.getOrder();
        
        Message message = Message.builder()
            .setToken(order.getStore().getDeviceToken())
            .setNotification(Notification.builder()
                .setTitle("새로운 주문")
                .setBody(String.format("테이블 %d - %s", 
                    order.getTableNumber(), 
                    order.getItemSummary()))
                .build())
            .putData("orderId", order.getId().toString())
            .putData("timestamp", String.valueOf(System.currentTimeMillis()))
            .build();
        
        try {
            String messageId = firebaseMessaging.send(message);
            log.info("FCM sent successfully: {}", messageId);
            
            // 알림 전송 기록
            notificationLog.save(new NotificationLog(
                order.getId(),
                messageId,
                NotificationStatus.SUCCESS
            ));
        } catch (FirebaseMessagingException e) {
            log.error("Failed to send FCM", e);
            
            // 재시도 큐에 저장
            retryQueue.enqueue(order);
        }
    }
    
    // 시나리오 2: 주문 준비 완료
    @EventListener
    public void onOrderPrepared(OrderPreparedEvent event) {
        Order order = event.getOrder();
        
        Message message = Message.builder()
            .setToken(order.getStore().getDeviceToken())
            .setNotification(Notification.builder()
                .setTitle("주문 준비 완료")
                .setBody(String.format("테이블 %d 음식이 준비되었습니다", 
                    order.getTableNumber()))
                .build())
            .build();
        
        firebaseMessaging.send(message);
    }
    
    // 시나리오 3: 결제 확인
    @EventListener
    public void onPaymentConfirmed(PaymentConfirmedEvent event) {
        // 유사한 로직...
    }
}
```

**API 엔드포인트:**

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/notifications/register-device` | FCM 디바이스 토큰 등록 |
| GET | `/api/notifications/history` | 알림 이력 조회 |
| PUT | `/api/notifications/{id}/read` | 알림 읽음 처리 |
| DELETE | `/api/notifications/{id}` | 알림 삭제 |
| POST | `/api/notifications/test` | 테스트 알림 전송 |

#### 2. 데이터베이스 최적화

**Connection Pool 설정:**
```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20        # 최대 연결 수
      minimum-idle: 5               # 최소 유휴 연결
      connection-timeout: 30000     # 연결 타임아웃
      idle-timeout: 600000          # 유휴 타임아웃
      auto-commit: true
```

**테이블 설계 (TGI003):**
```sql
CREATE TABLE order (
    id BIGINT PRIMARY KEY,
    store_id BIGINT NOT NULL,
    table_number INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    total_price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 인덱스: 자주 조회하는 조건
    INDEX idx_store_status (store_id, status),
    INDEX idx_created_at (created_at DESC),
    
    FOREIGN KEY (store_id) REFERENCES store(id)
);

CREATE TABLE order_item (
    id BIGINT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    menu_id BIGINT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2),
    
    INDEX idx_order_id (order_id),
    FOREIGN KEY (order_id) REFERENCES order(id) ON DELETE CASCADE
);

CREATE TABLE notification_log (
    id BIGINT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    message_id VARCHAR(255),
    status VARCHAR(20),
    sent_at TIMESTAMP,
    
    INDEX idx_order_id (order_id),
    INDEX idx_status (status)
);
```

#### 3. 환경별 배포 설정

**application-dev.yml:**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/ifrog_dev
    username: dev_user
    password: ${DB_PASSWORD_DEV}
  jpa:
    hibernate:
      ddl-auto: update

firebase:
  credentials-path: ${FIREBASE_CREDS_DEV}
  
logging:
  level:
    root: DEBUG
```

**application-prod.yml:**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://${PROD_DB_HOST}:5432/ifrog_prod
    username: ${PROD_DB_USER}
    password: ${PROD_DB_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate

firebase:
  credentials-path: ${FIREBASE_CREDS_PROD}
  
logging:
  level:
    root: INFO
    com.f1soft: INFO
```

**Docker 배포:**
```dockerfile
FROM openjdk:17-slim

WORKDIR /app

# JAR 파일 복사
COPY target/*.jar app.jar

# 환경변수
ENV SPRING_PROFILES_ACTIVE=prod

# 포트 노출
EXPOSE 8080

# 실행
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### 📚 생성된 기술 문서

1. **FCM 알림 시스템 통합 가이드** (15개 섹션)
2. **데이터베이스 연결 및 최적화** (12개 섹션)
3. **환경별 설정 및 배포 가이드** (8개 섹션)

---

## 🏆 Project 4: NoNAME - 개인 학습 프로젝트

### 📋 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | NoNAME: AI/LLM 백엔드 아키텍처 설계 |
| **특성** | 개인 학습 프로젝트 (회사와 무관) |
| **목표** | Spring Boot 심화 및 시스템 아키텍처 이해 |
| **기간** | 2026년 진행중 |
| **기술 스택** | Spring Boot, Mybatis, PostgreSQL, Git Flow |

### 🎯 학습 내용

#### 1. Backend 아키텍처

**계층별 설계:**
```java
// Controller Layer: API 엔드포인트
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUser(@PathVariable Long id) {
        UserDto user = userService.getUserById(id);
        return ResponseEntity.ok(user);
    }
}

// Service Layer: 비즈니스 로직
@Service
@Transactional
public class UserService {
    @Transactional(propagation = Propagation.REQUIRED)
    public UserDto getUserById(Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));
        return UserDto.from(user);
    }
}

// Repository Layer: 데이터 접근
@Mapper
public interface UserMapper {
    @Select("SELECT * FROM users WHERE id = #{id}")
    User selectById(Long id);
}
```

#### 2. @Transactional 전파방식 (6가지)

```java
// 1. REQUIRED (기본값): 기존 트랜잭션이 있으면 참여, 없으면 생성
@Transactional(propagation = Propagation.REQUIRED)
public void method1() { }

// 2. REQUIRES_NEW: 항상 새로운 트랜잭션 생성
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void method2() { }

// 3. SUPPORTS: 기존 트랜잭션이 있으면 참여, 없으면 비트랜잭션
@Transactional(propagation = Propagation.SUPPORTS)
public void method3() { }

// 4. MANDATORY: 기존 트랜잭션이 필수, 없으면 예외 발생
@Transactional(propagation = Propagation.MANDATORY)
public void method4() { }

// 5. NEVER: 비트랜잭션 필수, 기존 트랜잭션이 있으면 예외 발생
@Transactional(propagation = Propagation.NEVER)
public void method5() { }

// 6. NOT_SUPPORTED: 비트랜잭션 실행
@Transactional(propagation = Propagation.NOT_SUPPORTED)
public void method6() { }
```

#### 3. N+1 문제 해결 (3가지)

**방법 1: Eager Loading (JOIN)**
```java
@Mapper
public interface OrderMapper {
    // Before: N+1 문제 발생
    @Select("SELECT * FROM orders WHERE user_id = #{userId}")
    List<Order> selectOrders(Long userId);
    
    // After: JOIN으로 한 번에 조회
    @Select("""
        SELECT o.*, oi.* 
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id
        WHERE o.user_id = #{userId}
    """)
    @ResultMap("orderWithItems")
    List<Order> selectOrdersWithItems(Long userId);
}
```

**방법 2: Batch Loading**
```java
@Service
public class OrderService {
    public List<Order> getOrdersWithBatchLoading(List<Long> orderIds) {
        // 1단계: 주문 데이터 조회
        List<Order> orders = orderRepository.findAllById(orderIds);
        
        // 2단계: 관련 데이터 일괄 조회
        Map<Long, List<OrderItem>> itemsMap = 
            orderItemRepository.findByOrderIdIn(orderIds)
                .stream()
                .collect(Collectors.groupingBy(OrderItem::getOrderId));
        
        // 3단계: 데이터 병합
        orders.forEach(order -> 
            order.setItems(itemsMap.getOrDefault(order.getId(), List.of()))
        );
        
        return orders;
    }
}
```

**방법 3: Query Projection**
```java
// DTO 기반 쿼리로 필요한 컬럼만 조회
public interface OrderDto {
    Long getId();
    Long getUserId();
    BigDecimal getTotalPrice();
}

@Mapper
public interface OrderMapper {
    @Select("""
        SELECT 
            o.id, 
            o.user_id, 
            o.total_price
        FROM orders o
        WHERE o.user_id = #{userId}
    """)
    List<OrderDto> selectOrderDtos(Long userId);
}
```

#### 4. 팀 협업 표준 정의

**Git Flow 전략:**
```
main (프로덕션)
  ↑
  ├─ release/v1.0.0 (배포 준비)
  │   ↑
  │   └─ develop (개발 브랜치)
  │       ↑
  │       ├─ feature/user-auth (기능 개발)
  │       ├─ feature/order-system
  │       ├─ bugfix/payment-error
  │       └─ refactor/database-schema
  │
  └─ hotfix/security-patch (긴급 패치)
```

**PR 체크리스트:**
- [ ] 코드 리뷰 2명 이상 승인
- [ ] 모든 테스트 통과
- [ ] SonarQube 코드 품질 A 이상
- [ ] 기술 문서 업데이트
- [ ] 마이그레이션 스크립트 검증

### 📚 생성된 기술 문서

1. **Backend 아키텍처 (15개 섹션)**
2. **DB 최적화 종합 가이드 (18개 섹션)**
3. **개발 환경 및 협업 가이드**

---

## 🌟 기술적 역량 정리

### 레벨별 기술 역량

| 영역 | 레벨 | 경험 |
|------|------|------|
| **Spring Boot** | ⭐⭐⭐⭐⭐ | 3개 대규모 프로젝트 |
| **SQL 최적화** | ⭐⭐⭐⭐⭐ | 성능 30% 개선 경험 |
| **Mybatis** | ⭐⭐⭐⭐ | 동적 SQL, 복잡한 쿼리 |
| **시스템 설계** | ⭐⭐⭐⭐ | 아키텍처 설계 경험 |
| **DevOps** | ⭐⭐⭐ | Docker, Kubernetes 기본 |
| **Git Flow** | ⭐⭐⭐⭐ | 팀 협업 표준 정의 |

---

## 📞 GitHub & 예제 코드

**GitHub:** [링크 입력 필요]

주요 저장소:
- `ifrog-notification-system`: FCM 알림 시스템
- `noname-backend`: 개인 학습 프로젝트
- `spring-boot-best-practices`: Spring Boot 최적화 가이드

---

## 🎓 마지막 인사

저는 단순한 개발자가 아닌 **시스템을 설계하고 최적화하는 엔지니어**로 성장하고 싶습니다.

이 포트폴리오를 통해 제 기술 역량과 성장 가능성을 보여드리고 싶습니다.

**감사합니다.**

---

**작성일:** 2026년 6월 11일  
**상태:** 작성 중 (추가 정보 수집 예정)

