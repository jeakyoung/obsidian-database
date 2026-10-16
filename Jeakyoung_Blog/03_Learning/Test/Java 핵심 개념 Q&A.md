---
title: Java 핵심 개념 Q&A
date: 2026-10-14
type: 학습자료
status: 완료
tags: []
---

# Java 핵심 개념 Q&A

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **분류** | 면접준비 |
| **관련 기술** | Java, OOP, 컬렉션, JVM |
| **정리일** | 2026-10-14 |

> 신입 Java 면접 단골 개념(컬렉션, 예외, 인터페이스/추상클래스, static/final, JVM 메모리)을 Q&A 형태로 정리. ENOVIA 커스터마이징(JPO)도 Java 기반이라 기본기 확인 질문 대비용.

## 🧩 핵심 개념

- 컬렉션: **List(순서O, 중복O) / Set(중복X) / Map(키-값)** 세 갈래로 구분
- 예외: **Checked(컴파일러가 처리 강제) / Unchecked(RuntimeException 계열)**
- JVM 메모리: **Stack(지역변수, 메서드 호출) / Heap(객체) / Method Area(클래스 정보, static)**

## 📖 상세 내용

### 1. 컬렉션

**Q1. List, Set, Map의 차이는?**
> List는 순서가 있고 중복 허용(`ArrayList`), Set은 중복 불가(`HashSet`, 순서 유지하려면 `LinkedHashSet`), Map은 키-값 쌍으로 키는 중복 불가(`HashMap`).

**Q2. HashMap은 어떻게 빠르게 값을 찾나요?**
> 키의 `hashCode()`로 저장할 버킷(배열 칸)을 바로 계산해서 접근하므로 평균 O(1). 같은 버킷에 여러 키가 몰리면(해시 충돌) `equals()`로 실제 같은 키인지 비교한다.

**Q3. `equals()`를 재정의하면 `hashCode()`도 같이 재정의해야 하는 이유는?**
> HashMap/HashSet은 `hashCode()`로 먼저 버킷을 찾고 그 다음 `equals()`를 본다. `equals()`만 재정의하면 내용이 같은 두 객체가 다른 버킷에 들어가서 중복 제거/조회가 깨진다.

```java
public class Part {
    private final String partId;

    public Part(String partId) { this.partId = partId; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Part)) return false;
        return partId.equals(((Part) o).partId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(partId);
    }
}
```

### 2. 예외 처리

**Q4. Checked Exception과 Unchecked Exception의 차이는?**

| | Checked | Unchecked |
|:--|:--|:--|
| 예시 | `IOException`, `SQLException` | `NullPointerException`, `IllegalArgumentException` |
| 처리 강제 | `try-catch` 또는 `throws` 필수 (안 하면 컴파일 에러) | 강제 안 함 |
| 의미 | 외부 요인으로 발생 가능, 복구 시도 가능 | 대부분 코드 버그 |

**Q5. try-with-resources란?**
> `AutoCloseable`을 구현한 자원(DB 커넥션, 파일 스트림 등)을 `try (...)` 안에서 선언하면 블록이 끝날 때 자동으로 `close()`해준다. `finally`에서 직접 닫다가 누락하는 실수를 방지.

```java
String sql = "SELECT PART_NAME FROM PART WHERE PART_ID = ?";
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setString(1, partId);
    try (ResultSet rs = ps.executeQuery()) {
        if (rs.next()) return rs.getString("PART_NAME");
    }
} catch (SQLException e) {
    throw new RuntimeException("부품 조회 실패: " + partId, e);
}
```

- `PreparedStatement`의 `?` 바인딩은 SQL Injection 방지 효과도 있음 — 꼬리질문으로 자주 연결됨

### 3. 객체지향 설계

**Q6. 인터페이스와 추상 클래스의 차이는?**

| | 인터페이스 | 추상 클래스 |
|:--|:--|:--|
| 상속 | 여러 개 구현 가능 (`implements A, B`) | 하나만 상속 (`extends`) |
| 필드 | 상수(`public static final`)만 | 일반 필드 가능 |
| 목적 | "무엇을 할 수 있는가" (역할/규약) | "무엇인가" (공통 기반 코드 공유) |

> Java 8부터 인터페이스도 `default` 메서드로 구현을 가질 수 있지만, 상태(필드)를 못 가진다는 점은 그대로.

**Q7. 접근 제어자 4가지는?**
> `public`(어디서나) > `protected`(같은 패키지 + 자식 클래스) > default(같은 패키지) > `private`(같은 클래스).

### 4. static / final

**Q8. `static`의 의미는?**
> 객체가 아니라 **클래스에 소속**된다는 뜻. 객체를 몇 개 만들든 하나만 존재하고, 객체 생성 없이 `클래스명.멤버`로 접근. 유틸 메서드(`Math.max`)나 공용 상수에 사용.

**Q9. `final`은 어디에 붙이면 각각 무슨 뜻인가요?**
> 변수: 재할당 불가 / 메서드: 오버라이딩 불가 / 클래스: 상속 불가(예: `String`). 단, `final List`는 참조만 고정이고 내부 원소 추가/삭제는 가능.

### 5. JVM 메모리와 GC

**Q10. JVM 메모리 구조를 설명해보세요.**

| 영역 | 저장되는 것 | 특징 |
|:--|:--|:--|
| Stack | 지역 변수, 메서드 호출 정보 | 스레드마다 따로, 메서드 끝나면 자동 해제 |
| Heap | `new`로 만든 객체 | 모든 스레드 공유, GC 대상 |
| Method Area | 클래스 정보, static 변수, 상수 | 모든 스레드 공유 |

**Q11. GC(Garbage Collection)란?**
> 더 이상 어디서도 참조되지 않는 Heap의 객체를 JVM이 자동으로 정리하는 것. 개발자가 직접 메모리를 해제하지 않아도 되지만, static 컬렉션에 객체를 계속 쌓아두는 등 참조가 남아 있으면 GC가 못 치워서 메모리 누수가 생길 수 있다.

### 6. 기타 단골

**Q12. 제네릭(Generic)을 쓰는 이유는?**
> `List<String>`처럼 타입을 지정해서 컴파일 시점에 잘못된 타입이 들어가는 걸 막고, 꺼낼 때 형변환(캐스팅)을 없애준다.

**Q13. 오버로딩 vs 오버라이딩** → [[03_Learning/Test/기술스택 종합 문제]] 1번 참고

## 💡 정리 및 활용

- Q3(equals/hashCode)과 Q5(try-with-resources)는 실무 코드와 바로 연결되는 질문이라, 코드 예시를 손으로 쓸 수 있으면 강하게 어필 가능
- 표로 정리된 비교 질문(Q4, Q6, Q10)은 "차이 → 언제 무엇을 쓰는지" 순서로 답하면 깔끔함
- 모르는 꼬리질문이 나오면 아는 개념까지 연결해서 설명하고 마무리

## 🔗 참고

- [[03_Learning/Test/코딩테스트 기본 개념 문제]]
- [[03_Learning/Test/기술스택 종합 문제]]
- [[03_Learning/Test/JSP·Servlet 웹 구조]]
