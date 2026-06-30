---

---
# 매핑(mapping)

매핑(mapping)은 두 가지 다른 개념에서 사용될 수 있습니다. 하나는 객체와 관계형 데이터베이스 간의 매핑을 의미하고, 다른 하나는 데이터 전송을 의미합니다.

### **객체-관계 매핑(Object-Relational Mapping, ORM)**

- 객체-관계 매핑은 객체 지향 프로그래밍 언어에서 사용되는 객체와 관계형 데이터베이스의 테이블 간의 매핑을 의미합니다.
- 이 매핑은 개발자가 객체를 데이터베이스 테이블로 매핑하고, 데이터베이스의 레코드를 객체로 매핑하는 프로세스를 다룹니다.
- 객체-관계 매핑을 통해 개발자는 데이터베이스에 직접적인 SQL을 사용하지 않고도 객체를 통해 데이터베이스를 조작할 수 있습니다.
- 예를 들어, 하나의 클래스는 데이터베이스의 한 테이블에 매핑되며, 클래스의 필드는 테이블의 열에 매핑됩니다. 이렇게 매핑된 객체는 데이터베이스 작업을 수행하기 위해 사용됩니다.

### **데이터 전송 매핑(Data Transfer Mapping)**

- 데이터 전송 매핑은 다른 시스템 간에 데이터를 전송하는 과정을 의미합니다.
- 이 매핑은 보통 다른 형식의 데이터를 서로 맞추는 작업으로 이루어집니다. 예를 들어, JSON 형식의 데이터를 받아서 XML 형식으로 변환하는 것 등이 해당됩니다.
- 데이터 전송 매핑은 시스템 간의 호환성을 유지하기 위해 필요한 프로세스 중 하나입니다.

따라서 매핑은 두 가지 다른 시스템 또는 개념 간의 관계를 정의하고 매치시키는 프로세스를 의미합니다. 객체-관계 매핑은 주로 객체 지향 프로그래밍과 관계형 데이터베이스 간의 관계를 다루는 반면, 데이터 전송 매핑은 다른 시스템 간의 데이터 전송에 관련됩니다.

---

# Spring boot mapping

스프링 부트에서의 "매핑"이라 함은 주로 두 가지 맥락에서 사용됩니다: URL 매핑과 데이터베이스 매핑입니다.

### **URL 매핑**

스프링 부트 애플리케이션에서 URL 매핑은 HTTP 요청을 처리하는 컨트롤러 메소드와 URL 주소를 매핑하는 과정을 의미합니다. 일반적으로 Spring MVC에서는 `**@Controller**` 또는 `**@RestController**` 어노테이션을 사용하여 컨트롤러 클래스를 정의하고, 각 메소드에 `**@RequestMapping**` 또는 `**@GetMapping**`, `**@PostMapping**`, `**@PutMapping**`, `**@DeleteMapping**` 등의 어노테이션을 사용하여 요청 매핑을 정의합니다.

```java
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {
    
    @GetMapping("/hello")
    public String hello() {
        return "Hello, World!";
    }
}

```

### **데이터베이스 매핑**

스프링 부트에서의 데이터베이스 매핑은 엔티티(데이터베이스의 테이블과 매핑되는 Java 클래스)와 데이터베이스 스키마 간의 매핑을 의미합니다. 이를 통해 애플리케이션의 Java 코드에서 객체를 사용하여 데이터베이스와 상호 작용할 수 있습니다. 주로 Spring Data JPA를 사용하여 이러한 매핑을 처리합니다.

```java
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String username;
    private String email;

    // Getters and setters
}

```

위의 코드에서 `**@Entity**` 어노테이션은 이 클래스가 JPA 엔티티임을 나타냅니다. 또한 `**@Id**` 어노테이션은 해당 필드가 엔티티의 식별자(primary key)임을 나타냅니다. 스프링 부트는 이러한 엔티티 클래스를 데이터베이스 테이블과 자동으로 매핑하여 사용할 수 있도록 해줍니다.


---

# 아주 쉽게 풀어 헤쳐놓은 설명

### **URL 매핑**

URL 매핑은 사용자가 웹 애플리케이션의 특정 URL을 요청했을 때, 해당 URL에 대응하는 컨트롤러 메소드를 실행하는 것입니다. 이 방식은 웹 애플리케이션에서 사용자의 요청을 처리하고 응답을 생성하는 데 사용됩니다. 예를 들어, 사용자가 "/home" URL을 요청하면, "/home"에 대응하는 컨트롤러 메소드가 실행되어 홈 페이지를 표시할 수 있습니다.

### **데이터베이스 매핑**

데이터베이스 매핑은 애플리케이션의 객체와 데이터베이스의 테이블 간의 매핑을 의미합니다. 이 방식은 데이터베이스의 데이터를 객체로 다룰 수 있도록 해주며, 주로 데이터베이스와의 상호 작용을 담당합니다. 예를 들어, 사용자 정보를 저장하는 User 객체를 정의하면, 이를 데이터베이스 테이블에 매핑하여 사용자 데이터를 읽고 쓸 수 있습니다.
