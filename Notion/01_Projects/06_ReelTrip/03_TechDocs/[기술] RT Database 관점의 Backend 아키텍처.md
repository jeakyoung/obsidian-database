---
title: RT Database 관점의 Backend 아키텍처 설계
type: 기술문서
date: 2026-06-11
status: 완료
category: 아키텍처
priority: 높음
---

# RT Database 관점의 Backend 아키텍처 설계

**프로젝트:** NoNAME (AI/LLM 기반 애플리케이션)  
**관점:** Real-Time Database 성능 최적화 중심  
**상태:** 완료  
**마지막 업데이트:** 2026-06-11

---

## 📋 개요

RT(Real-Time) Database를 활용하는 현대적인 Backend 아키텍처 설계를 통한 고성능 시스템 구축

### 핵심 원칙
1. **데이터베이스 중심 설계** - DB 성능을 최우선 고려
2. **트랜잭션 관리** - @Transactional로 일관성 보장
3. **동적 SQL** - Mybatis 동적 SQL로 유연성 확보
4. **인덱싱 전략** - 쿼리 성능 극대화

---

## 🏗️ 아키텍처 계층

```
┌─────────────────────────────────────────┐
│         Frontend (React/Vue)            │
├─────────────────────────────────────────┤
│  REST API Controller / GraphQL Gateway  │
├─────────────────────────────────────────┤
│      Service Layer (Business Logic)     │
│    (@Transactional 트랜잭션 관리)       │
├─────────────────────────────────────────┤
│       Repository (Data Access)          │
│     (Mybatis 동적 SQL 활용)             │
├─────────────────────────────────────────┤
│   Database (PostgreSQL/MySQL)           │
│  (준실시간 데이터 동기화)               │
└─────────────────────────────────────────┘
```

---

## 🔧 핵심 기술 1: @Transactional

### 개념
```java
@Transactional: 메서드 실행을 트랜잭션으로 감싸서 
원자성(Atomicity), 일관성(Consistency) 보장
```

### 기본 사용법
```java
@Service
public class OrderService {
  
  @Transactional
  public Order createOrder(OrderRequest req) {
    // 1. Order 저장
    Order order = new Order(req);
    orderRepository.save(order);
    
    // 2. OrderItem 저장
    req.getItems().forEach(item -> {
      orderItemRepository.save(new OrderItem(item, order.getId()));
    });
    
    // 3. Inventory 감소
    inventoryService.decreaseInventory(req.getItems());
    
    // 4. 모든 작업 완료 후 COMMIT
    return order;
    // 중간에 Exception 발생 시 ROLLBACK
  }
}
```

### Propagation (전파 방식)

```java
// REQUIRED (기본값): 기존 트랜잭션 재사용 또는 새로 생성
@Transactional(propagation = Propagation.REQUIRED)
public void methodA() { ... }

// REQUIRES_NEW: 항상 새 트랜잭션 생성
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void methodB() {
  // methodB 실패해도 methodA는 영향 없음
}

// NESTED: 중첩 트랜잭션 (savepoint 생성)
@Transactional(propagation = Propagation.NESTED)
public void methodC() { ... }
```

### Isolation Level (격리 수준)

```java
// READ_UNCOMMITTED: Dirty Read 허용 (위험)
@Transactional(isolation = Isolation.READ_UNCOMMITTED)

// READ_COMMITTED: Dirty Read 방지 (권장 기본값)
@Transactional(isolation = Isolation.READ_COMMITTED)

// REPEATABLE_READ: 반복 읽기 보장
@Transactional(isolation = Isolation.REPEATABLE_READ)

// SERIALIZABLE: 최고 격리 수준 (성능 저하)
@Transactional(isolation = Isolation.SERIALIZABLE)
```

### Timeout 설정
```java
@Transactional(timeout = 30)  // 30초 타임아웃
public void longRunningOperation() { ... }
```

### ReadOnly 최적화
```java
// 읽기 전용 트랜잭션 (INSERT/UPDATE/DELETE 불가)
@Transactional(readOnly = true)
public List<Order> getOrders(String userId) {
  return orderRepository.findByUserId(userId);
}
```

---

## 🔧 핵심 기술 2: PreparedStatement

### 개념
```
컴파일된 SQL 쿼리를 재사용하여 성능 개선
- 파싱 과정 생략
- SQL Injection 방지
- 배치 처리 가능
```

### 기본 사용법
```java
String sql = "SELECT * FROM users WHERE user_id = ? AND status = ?";
PreparedStatement stmt = connection.prepareStatement(sql);
stmt.setString(1, userId);
stmt.setString(2, "ACTIVE");
ResultSet rs = stmt.executeQuery();
```

### Spring Data JPA에서의 적용
```java
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
  // @Query 사용 시 자동으로 PreparedStatement 사용
  @Query("SELECT o FROM Order o WHERE o.userId = :userId AND o.status = :status")
  List<Order> findActiveOrders(
    @Param("userId") String userId,
    @Param("status") String status
  );
}
```

### Mybatis에서의 적용
```xml
<!-- mybatis-mapper.xml -->
<select id="getOrders" parameterType="map" resultType="Order">
  SELECT * FROM orders 
  WHERE user_id = #{userId}
  <if test="status != null">
    AND status = #{status}
  </if>
</select>
```

---

## 🔧 핵심 기술 3: Mybatis 동적 SQL

### 동적 쿼리의 필요성
```
고정 SQL: 조건 수에 따라 여러 쿼리 필요
동적 SQL: 하나의 쿼리로 모든 조건 처리
```

### If 태그
```xml
<select id="searchOrders" parameterType="map" resultType="Order">
  SELECT * FROM orders WHERE 1=1
  <if test="userId != null">
    AND user_id = #{userId}
  </if>
  <if test="status != null">
    AND status = #{status}
  </if>
  <if test="dateFrom != null">
    AND order_date >= #{dateFrom}
  </if>
  <if test="dateTo != null">
    AND order_date <= #{dateTo}
  </if>
</select>
```

### Choose (Switch 문)
```xml
<choose>
  <when test="type == 'ADMIN'">
    SELECT * FROM orders  <!-- 모든 주문 -->
  </when>
  <when test="type == 'MANAGER'">
    SELECT * FROM orders WHERE shop_id = #{shopId}  <!-- 매장 주문만 -->
  </when>
  <otherwise>
    SELECT * FROM orders WHERE user_id = #{userId}  <!-- 사용자 주문만 -->
  </otherwise>
</choose>
```

### Foreach (반복)
```xml
<select id="getOrdersByIds" parameterType="map" resultType="Order">
  SELECT * FROM orders 
  WHERE order_id IN 
  <foreach collection="orderIds" item="id" open="(" separator="," close=")">
    #{id}
  </foreach>
</select>
```

### Where 태그 (자동 WHERE 처리)
```xml
<select id="searchOrders" parameterType="map" resultType="Order">
  SELECT * FROM orders
  <where>
    <if test="userId != null">
      AND user_id = #{userId}
    </if>
    <if test="status != null">
      AND status = #{status}
    </if>
  </where>
</select>
```

---

## 📊 N+1 문제 해결

### 문제 상황
```java
// N+1 쿼리: 1개 주문 조회 + N개 상품 조회
List<Order> orders = orderRepository.findAll();  // Query 1
for (Order order : orders) {
  List<Product> products = productRepository.findByOrderId(order.getId());  // Query N
}
```

### 해결책 1: JOIN Fetch
```java
@Query("""
  SELECT DISTINCT o FROM Order o 
  LEFT JOIN FETCH o.items item
  LEFT JOIN FETCH item.product p
""")
List<Order> findAllWithItems();
```

### 해결책 2: 배치 조회
```java
// 1번의 IN 쿼리로 모든 상품 조회
List<Order> orders = orderRepository.findAll();
List<Long> orderIds = orders.stream()
  .map(Order::getId)
  .collect(Collectors.toList());

Map<Long, List<Product>> productsByOrder = 
  productRepository.findByOrderIdIn(orderIds)
    .stream()
    .collect(Collectors.groupingBy(Product::getOrderId));

orders.forEach(o -> o.setItems(productsByOrder.get(o.getId())));
```

### 해결책 3: 쿼리 통합
```sql
-- 1번 쿼리로 주문 + 상품 정보 모두 조회
SELECT 
  o.order_id, o.order_date,
  p.product_id, p.product_name
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE o.user_id = ?
```

---

## ⚡ 성능 최적화 전략

### 데이터베이스 수준
1. **인덱싱**: 자주 조회되는 컬럼에 인덱스
2. **쿼리 최적화**: 실행 계획 분석
3. **파티셔닝**: 대용량 테이블 분할

### 애플리케이션 수준
1. **캐싱**: Redis 캐시 활용
2. **배치 처리**: 대량 데이터 처리
3. **비동기 처리**: @Async로 장시간 작업 분리

### 트랜잭션 최적화
1. **범위 최소화**: 필요한 부분만 @Transactional
2. **격리 수준**: READ_COMMITTED 활용
3. **타임아웃**: 무한 대기 방지

---

## 🏆 Best Practices

### 1. 트랜잭션 설계
```java
✅ 좋은 예:
@Transactional
public Order createOrder(OrderRequest req) {
  // 필요한 작업만 트랜잭션 내에서 처리
  Order order = new Order(req);
  orderRepository.save(order);
  return order;
}

❌ 나쁜 예:
@Transactional
public Order createOrderWithUI(OrderRequest req) {
  Order order = new Order(req);
  orderRepository.save(order);
  
  // UI 렌더링은 트랜잭션 외부에서!
  return renderOrderForm(order);
}
```

### 2. 쿼리 최적화
```java
✅ 좋은 예:
@Query("""
  SELECT DISTINCT o FROM Order o
  LEFT JOIN FETCH o.items
  WHERE o.userId = :userId
""")
List<Order> findByUser(@Param("userId") String userId);

❌ 나쁜 예:
public List<Order> findByUser(String userId) {
  List<Order> orders = orderRepository.findAll();
  return orders.stream()
    .filter(o -> o.getUserId().equals(userId))
    .collect(Collectors.toList());
}
```

### 3. 데이터 일관성
```java
✅ 좋은 예:
@Transactional
public void transferInventory(Long fromShop, Long toShop, int qty) {
  inventoryRepository.decreaseInventory(fromShop, qty);
  inventoryRepository.increaseInventory(toShop, qty);
  // 둘 다 완료되거나 둘 다 실패
}

❌ 나쁜 예:
public void transferInventory(Long fromShop, Long toShop, int qty) {
  inventoryRepository.decreaseInventory(fromShop, qty);  // 완료
  inventoryRepository.increaseInventory(toShop, qty);   // 실패?
  // 데이터 불일치 발생 가능
}
```

---

## 📈 성능 모니터링

### 로깅 설정
```yaml
logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE
  pattern:
    console: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"
```

### 메트릭 수집
```java
@Component
public class QueryMetrics {
  private final MeterRegistry meterRegistry;
  
  public void recordQueryTime(String queryName, long duration) {
    meterRegistry.timer("query.time", "query", queryName)
      .record(duration, TimeUnit.MILLISECONDS);
  }
}
```

---

## ✅ 아키텍처 체크리스트

- [ ] @Transactional 전략 정의
- [ ] 트랜잭션 격리 수준 설정
- [ ] PreparedStatement 활용
- [ ] Mybatis 동적 SQL 구현
- [ ] N+1 쿼리 제거
- [ ] 인덱싱 계획 수립
- [ ] 캐싱 전략 구현
- [ ] 성능 모니터링 설정

---

**작성일:** 2026-06-11  
**상태:** 완료  
**담당자:** NoNAME 아키텍처팀

