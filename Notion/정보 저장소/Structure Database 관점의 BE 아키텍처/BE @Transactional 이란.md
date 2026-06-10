---

---

---

# @Transactional — 여러 DB 작업을 하나의 단위로 묶는 트랜잭션 처리

> "계좌 이체"를 생각해보세요.
A 계좌에서 돈을 빼고, B 계좌에 돈을 넣는 두 작업이 있습니다.
중간에 오류가 나면 A에서만 돈이 빠지는 재앙이 발생합니다.
**트랜잭션**은 이런 상황을 막기 위해 "모두 성공하거나, 모두 실패하거나"를 보장합니다.

---

## 1. 트랜잭션이란 무엇인가

트랜잭션(Transaction)은 **하나의 논리적 작업 단위**입니다. 여러 개의 DB 작업이 묶여서, 전부 성공하면 반영(Commit)하고 하나라도 실패하면 전부 되돌립니다(Rollback).

```plain text
트랜잭션 시작
    ① events 테이블에 일정 INSERT       ← 성공
    ② notifications 테이블에 알림 INSERT ← 실패! 오류 발생
트랜잭션 종료

→ ①도 자동으로 취소됨 (Rollback)
→ DB에는 아무것도 저장되지 않은 상태로 유지
```

---

## 2. ACID 원칙 — 트랜잭션의 4가지 보장

| 원칙 | 이름 | 설명 |
| --- | --- | --- |
| **A** | Atomicity (원자성) | 전부 성공하거나 전부 실패. 중간 상태 없음 |
| **C** | Consistency (일관성) | 트랜잭션 전후로 DB 무결성 규칙이 유지됨 |
| **I** | Isolation (격리성) | 동시에 실행되는 트랜잭션이 서로 간섭하지 않음 |
| **D** | Durability (지속성) | 커밋된 데이터는 장애가 나도 유지됨 |

실무에서 가장 자주 신경 써야 하는 것은 **A(원자성)** 입니다. `@Transactional` 하나로 원자성을 보장할 수 있습니다.

---

## 3. Spring에서 @Transactional 사용하기

`@Transactional`은 Service 메서드에 붙입니다. 붙이면 해당 메서드 안의 모든 DB 작업이 하나의 트랜잭션으로 묶입니다.

```java
@Service
public class EventServiceImpl {

    @Transactional  // ← 이 메서드 안의 모든 DB 작업이 하나의 트랜잭션
    public void createEventWithNotification(EventRequest req, Long userId) {

        // 1. 일정 저장
        Event event = new Event(req);
        eventMapper.insert(event);           // INSERT INTO events ...

        // 2. 알림 저장
        Notification noti = new Notification(event, userId);
        notificationMapper.insert(noti);     // INSERT INTO notifications ...

        // 위 두 작업 중 하나라도 실패하면 → 둘 다 Rollback
        // 둘 다 성공하면 → 둘 다 Commit
    }
}
```

>  `@Transactional`이 없으면 각 Mapper 호출이 **독립적인 트랜잭션**으로 처리됩니다.
첫 번째 INSERT가 성공해서 저장됐는데 두 번째 INSERT가 실패해도 첫 번째는 그대로 남습니다.

---

## 4. 커밋(Commit)과 롤백(Rollback)

정상 흐름:

```plain text
메서드 시작 → 트랜잭션 시작
    DB 작업 1 실행
    DB 작업 2 실행
    DB 작업 3 실행
메서드 정상 종료 → 커밋 (모든 변경사항 DB에 확정 반영)
```

예외 발생 시:

```plain text
메서드 시작 → 트랜잭션 시작
    DB 작업 1 실행 (임시 저장)
    DB 작업 2 실행 (임시 저장)
    ❌ 예외 발생
→ 자동 롤백 (작업 1, 2 모두 취소)
```

### 롤백이 되는 예외 vs 안 되는 예외

기본적으로 **RuntimeException** (Unchecked Exception)이 발생해야 자동 롤백됩니다.

| 예외 종류 | 기본 롤백 여부 |
| --- | --- |
| `RuntimeException` (NullPointerException, IllegalArgumentException 등) | 롤백 |
| `Error` | 롤백 |
| `Exception` (Checked Exception: IOException, SQLException 등) | 롤백 안 됨 |

Checked Exception도 롤백하고 싶다면 `rollbackFor` 옵션을 사용합니다.

```java
@Transactional(rollbackFor = Exception.class)
public void createEvent(...) { ... }
```

---

## 5. @Transactional 주요 옵션

### readOnly — 읽기 전용 트랜잭션

```java
@Transactional(readOnly = true)
public List<EventResponse> findBySpace(Long spaceId) {
    return eventMapper.findBySpaceId(spaceId)
        .stream().map(this::toResponse).toList();
}
```

> `readOnly = true`를 붙이면 DB가 쓰기 잠금을 걸지 않아 **성능이 향상**됩니다.
데이터를 조회만 하는 메서드에는 항상 붙이는 것이 좋습니다.

### propagation — 트랜잭션 전파 방식

이미 트랜잭션이 실행 중인데 또 다른 `@Transactional` 메서드를 호출하면 어떻게 될까요?

| 옵션 | 동작 |
| --- | --- |
| `REQUIRED` (기본값) | 기존 트랜잭션에 합류. 없으면 새로 생성 |
| `REQUIRES_NEW` | 기존 트랜잭션과 별개로 새 트랜잭션 생성 |
| `NESTED` | 기존 트랜잭션 안에 중첩 트랜잭션 생성 |

```java
@Transactional
public void createEventWithNotification(...) {
    eventMapper.insert(event);         // 부모 트랜잭션에 포함
    sendNotification(event, userId);   // 같은 트랜잭션으로 합류
}

@Transactional  // propagation = REQUIRED (기본값)
public void sendNotification(Event event, Long userId) {
    notificationMapper.insert(...);    // 위 트랜잭션에 합류
}
```

---

## 6. 트랜잭션이 적용되지 않는 함정

### ① 같은 클래스 내부 호출 (Self-Invocation)

`@Transactional`은 Spring이 프록시(Proxy)로 처리합니다. 같은 클래스 안에서 `this.`로 직접 호출하면 프록시를 거치지 않아 트랜잭션이 적용되지 않습니다.

```java
@Service
public class EventService {

    public void outerMethod() {
        this.innerMethod();  // ❌ 트랜잭션 미적용
    }

    @Transactional
    public void innerMethod() {
        eventMapper.insert(...);
        notificationMapper.insert(...);
    }
}
```

해결: 별도 Service 클래스로 분리하거나, ApplicationContext에서 Bean을 꺼내서 호출합니다.

### ② private 메서드에 붙일 때

```java
@Transactional  // ❌ private 메서드엔 트랜잭션 적용 안 됨
private void saveEvent(Event event) {
    eventMapper.insert(event);
}
```

`@Transactional`은 `public` 메서드에만 적용됩니다.

### ③ Controller에 붙일 때

```java
@RestController
public class EventController {

    @Transactional  // ❌ Controller에 붙이는 것은 안티패턴
    @PostMapping
    public ResponseEntity<?> create(...) { ... }
}
```

트랜잭션은 **Service 레이어**에만 붙이는 것이 올바른 설계입니다.

---

## 7. 실무 예시 — 스페이스 생성 + 멤버 자동 추가

팀 스페이스를 만들 때 생성자를 자동으로 멤버로 등록해야 합니다. 두 INSERT가 반드시 함께 성공하거나 함께 실패해야 합니다.

```java
@Transactional
public TeamSpaceResponse createTeamSpace(TeamSpaceRequest req, String username) {
    User user = getUser(username);

    // 1. 팀 스페이스 생성
    TeamSpace space = TeamSpace.builder()
        .name(req.getName())
        .emoji(req.getEmoji())
        .bgColor(req.getBgColor())
        .ownerId(user.getId())
        .build();
    teamSpaceMapper.insert(space);           // INSERT INTO team_spaces

    // 2. 생성자를 멤버로 자동 등록
    TeamSpaceMember member = TeamSpaceMember.builder()
        .spaceId(space.getId())
        .userId(user.getId())
        .role("owner")
        .build();
    teamSpaceMemberMapper.insert(member);    // INSERT INTO team_space_members

    // 둘 중 하나 실패 → 둘 다 롤백
    return toResponse(space);
}
```

---

## 8. 자주 하는 실수 — 오류 발생 시 직접 catch 해버리기

```java
@Transactional
public void createEvent(...) {
    try {
        eventMapper.insert(event);
        notificationMapper.insert(noti);
    } catch (Exception e) {
        log.error("오류 발생", e);  // ❌ 예외를 잡아버리면 롤백이 안 됨!
    }
}
```

```java
// ✅ 예외를 반드시 다시 던져야 롤백 작동
} catch (Exception e) {
    log.error("오류 발생", e);
    throw e;
}
```

---