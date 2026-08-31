---
title: I-Frog FCM 알림 시스템 통합 가이드
type: 기술문서
date: 2026-06-11
status: 완료
category: 알림시스템
priority: 높음
---

# I-Frog FCM 알림 시스템 통합 가이드

**시스템:** Firebase Cloud Messaging (FCM)  
**목적:** 실시간 푸시 알림 전송 (주문, 시스템 메시지)  
**상태:** 완료 및 운영 중  
**마지막 업데이트:** 2026-06-11

---

## 📋 개요

I-Frog POS 시스템의 핵심 기능인 FCM 알림 시스템을 위한 서버 설정, 기능 개발, 운영 가이드

---

## 🔧 FCM 시스템 구성

### 1️⃣ 서버 세팅

#### 초기 설정 단계
```
1. Firebase 프로젝트 생성
   - Google Firebase Console 접속
   - 프로젝트 생성 (I-Frog)
   - 서비스 계정 생성
   - Private Key 다운로드

2. Spring Boot 통합
   - firebase-admin-sdk 의존성 추가
   - 서비스 계정 Key 파일 설정
   - FirebaseApp 초기화

3. 권한 설정
   - FCM 토픽 구독 권한
   - 클라이언트 디바이스 토큰 관리
```

#### 설정 파일 예시
```yaml
# application.yml
firebase:
  credentials-path: classpath:firebase-credentials.json
  project-id: ifrog-project-id
  database-url: https://ifrog-project-id.firebaseio.com
```

---

### 2️⃣ 기능 개발

#### A. 디바이스 토큰 관리
```javascript
// 클라이언트에서 토큰 등록
firebase.messaging().getToken().then((token) => {
  // 서버로 토큰 전송
  fetch('/api/fcm/register-token', {
    method: 'POST',
    body: JSON.stringify({ token: token }),
    headers: { 'Content-Type': 'application/json' }
  });
});
```

**서버 처리:**
```java
@PostMapping("/api/fcm/register-token")
public void registerToken(@RequestBody TokenRequest request) {
  // 사용자의 디바이스 토큰 저장
  deviceTokenRepository.save(
    new DeviceToken(userId, request.getToken())
  );
}
```

#### B. 메시지 전송

**단일 기기 전송:**
```java
Message message = Message.builder()
  .setToken(deviceToken)
  .setNotification(new Notification(
    "주문 신청",
    "새로운 주문이 들어왔습니다"
  ))
  .putData("orderId", "ORDER-12345")
  .build();

FirebaseMessaging.getInstance().send(message);
```

**토픽 기반 전송 (다중 기기):**
```java
Message message = Message.builder()
  .setTopic("new-orders")  // 모든 구독자에게 전송
  .setNotification(new Notification(
    "신규 주문",
    "새로운 주문이 들어왔습니다"
  ))
  .putData("timestamp", System.currentTimeMillis())
  .build();

FirebaseMessaging.getInstance().send(message);
```

#### C. 토픽 구독 관리
```java
// 토픽 구독
FirebaseMessaging.getInstance()
  .subscribeToTopic(Arrays.asList(deviceToken), "new-orders");

// 토픽 구독 해제
FirebaseMessaging.getInstance()
  .unsubscribeFromTopic(Arrays.asList(deviceToken), "new-orders");
```

---

### 3️⃣ 시나리오 및 활용

#### 시나리오 1: 주문 수신 알림
```
사용자 → POS 주문 → 매장 POP 화면
                 ↓
         FCM 알림 발송
                 ↓
         웹 브라우저 알림 + 음성
```

**구현:**
```java
@Service
public class OrderService {
  @Autowired
  private FCMService fcmService;
  
  public void createOrder(Order order) {
    // 주문 저장
    orderRepository.save(order);
    
    // FCM 알림 발송
    fcmService.notifyNewOrder(order);
  }
}
```

#### 시나리오 2: 결제함 문서 알림
```
문서 업로드 → 상태 변경 → FCM 알림
     ↓
  결제 담당자에게 알림
```

**구현:**
```java
public void notifyPaymentDocument(Document doc) {
  List<String> tokens = getPaymentManagerTokens();
  
  for (String token : tokens) {
    sendNotification(token, 
      "결제 문서: " + doc.getDocumentNumber(),
      "새로운 결제 문서가 도착했습니다"
    );
  }
}
```

---

## 📊 메시지 포맷

### 알림 메시지 구조
```json
{
  "token": "device-token",
  "notification": {
    "title": "알림 제목",
    "body": "알림 내용"
  },
  "data": {
    "orderId": "ORDER-12345",
    "type": "new_order",
    "timestamp": "2026-06-11T10:30:00"
  }
}
```

### 데이터 필드 정의

| 필드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| title | String | 알림 제목 | "주문 신청" |
| body | String | 알림 본문 | "새로운 주문이 들어왔습니다" |
| orderId | String | 주문 번호 | "ORDER-12345" |
| type | String | 메시지 타입 | "new_order", "payment", "status" |
| timestamp | String | 발송 시간 | "2026-06-11T10:30:00" |

---

## 🔌 API 엔드포인트

### 클라이언트 API

#### 토큰 등록
```
POST /api/fcm/register-token
{
  "token": "device-token",
  "deviceType": "web|mobile"
}
```

#### 알림 권한 확인
```
GET /api/fcm/permission-status
응답:
{
  "granted": true,
  "permission": "granted|denied|default"
}
```

#### 토픽 구독/해제
```
POST /api/fcm/subscribe
{
  "topic": "new-orders"
}

POST /api/fcm/unsubscribe
{
  "topic": "new-orders"
}
```

### 서버 API

#### 단일 기기에 알림 전송
```
POST /admin/fcm/send-to-device
{
  "deviceToken": "...",
  "notification": { "title": "...", "body": "..." },
  "data": { ... }
}
```

#### 토픽으로 알림 전송
```
POST /admin/fcm/send-to-topic
{
  "topic": "new-orders",
  "notification": { "title": "...", "body": "..." },
  "data": { ... }
}
```

---

## ⚙️ 환경 설정

### 개발 환경
```properties
# dev-config.properties
fcm.enabled=true
fcm.credentials-path=/config/dev-firebase.json
fcm.retry-count=3
fcm.timeout=10000
```

### 운영 환경
```properties
# prod-config.properties
fcm.enabled=true
fcm.credentials-path=/config/prod-firebase.json
fcm.retry-count=5
fcm.timeout=30000
fcm.batch-size=100
```

---

## 🐛 문제 해결

### 문제 1: CORS 이슈
```
에러: Cross-Origin Request Blocked
원인: 브라우저 보안 정책
해결:
```

```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {
  @Override
  public void addCorsMappings(CorsRegistry registry) {
    registry.addMapping("/api/**")
      .allowedOrigins("*")
      .allowedMethods("GET", "POST", "PUT", "DELETE")
      .allowedHeaders("*");
  }
}
```

### 문제 2: 토큰 만료
```
에러: Invalid Token
원인: 토큰 유효기간 만료 (약 60일)
해결: 클라이언트에서 토큰 갱신 후 재등록
```

```javascript
// 토큰 갱신 모니터링
firebase.messaging().onTokenRefresh(() => {
  firebase.messaging().getToken().then((newToken) => {
    // 서버에 새 토큰 등록
    registerNewToken(newToken);
  });
});
```

### 문제 3: 알림 미수신
```
확인 사항:
1. 브라우저 알림 권한 확인
2. Service Worker 등록 확인
3. 디바이스 토큰 유효성 확인
4. 네트워크 연결 확인
```

---

## 📈 성능 최적화

### 배치 전송
```java
// 대량의 기기에 한 번에 전송
List<String> tokens = getAllActiveDeviceTokens();
List<Message> messages = tokens.stream()
  .map(token -> Message.builder()
    .setToken(token)
    .setNotification(notification)
    .build())
  .collect(Collectors.toList());

FirebaseMessaging.getInstance().sendAll(messages);
```

### 토픽 활용 (권장)
```
개별 토큰: 1대1 전송 (느림)
토픽: N명에게 한 번에 전송 (빠름)
```

---

## 🔒 보안

### 1. 자격증명 관리
- Firebase 서비스 계정 Key는 환경 변수로 관리
- Git에 포함되지 않도록 .gitignore에 추가

```bash
# .gitignore
firebase-credentials.json
```

### 2. 토큰 보안
- 토큰은 사용자별로 저장 및 관리
- 토큰 갱신 시 이전 토큰 무효화

### 3. 메시지 검증
- 메시지 서명 검증 (선택)
- Rate Limiting 적용

```java
@Component
public class RateLimitingFilter implements Filter {
  @Override
  public void doFilter(ServletRequest request, 
                       ServletResponse response,
                       FilterChain chain) {
    // Rate limiting 구현
  }
}
```

---

## 📚 참고 자료

- Firebase Documentation: https://firebase.google.com/docs
- FCM 최신 기능: https://firebase.google.com/docs/cloud-messaging
- Spring Boot Firebase Integration: [관련 기술 문서]

---

## ✅ 체크리스트

- [ ] Firebase 프로젝트 생성
- [ ] 서비스 계정 Key 다운로드
- [ ] Spring Boot 의존성 추가
- [ ] FirebaseApp 초기화
- [ ] 디바이스 토큰 관리 API 구현
- [ ] 메시지 전송 API 구현
- [ ] CORS 설정 완료
- [ ] 개발 환경 테스트
- [ ] 운영 환경 배포
- [ ] 모니터링 대시보드 설정

---

**작성일:** 2026-06-11  
**상태:** 완료 및 운영 중  
**담당자:** I-Frog 개발팀

