---

---
### `**@SpringBootApplication**`

`**@SpringBootApplication**` 어노테이션은 스프링 부트 애플리케이션의 주 진입점(entry point)을 나타냅니다. 이 어노테이션이 있는 클래스는 스프링 부트 애플리케이션의 시작점으로 인식되며, 스프링 부트의 자동 설정과 구성을 활성화합니다.

```java
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}

```

### `**@RestController**`

`**@RestController**` 어노테이션은 해당 클래스가 RESTful 웹 서비스의 컨트롤러임을 나타냅니다. 이 어노테이션이 있는 클래스는 HTTP 요청에 대한 응답을 생성하는 컨트롤러로 동작합니다.

```java
@RestController
public class MyController {
    @GetMapping("/hello")
    public String hello() {
        return "Hello, World!";
    }
}

```

### `**@Autowired**`

`**@Autowired**` 어노테이션은 스프링의 의존성 주입을 위해 사용됩니다. 해당 필드나 메소드에 이 어노테이션을 추가하면 해당 타입의 빈(bean)이 자동으로 주입됩니다.

```java
@Service
public class MyService {
    private MyRepository repository;

    @Autowired
    public MyService(MyRepository repository) {
        this.repository = repository;
    }

    // 메소드 내용
}

```

### `**@Entity**`

`**@Entity**` 어노테이션은 JPA 엔티티 클래스임을 나타냅니다. 데이터베이스의 테이블과 매핑되는 엔티티 클래스에 사용됩니다.

```java
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

---

# 유사한 어노테이션

## RestController 와 Controller

`**@RestController**`와 `**@Controller**` 어노테이션은 스프링 프레임워크에서 웹 애플리케이션의 컨트롤러를 정의할 때 사용 합니다.

### **@Controller 어노테이션**

`**@Controller**` 어노테이션은 전통적인 스프링 MVC 웹 애플리케이션에서 사용됩니다. 이 어노테이션은 해당 클래스가 웹 요청을 처리하는 컨트롤러임을 나타냅니다.

예를 들어, `**@Controller**` 어노테이션이 있는 클래스에서는 보통 `**@RequestMapping**` 어노테이션을 사용하여 요청 URL과 메소드를 매핑합니다.

```java
@Controller
public class MyController {

    @RequestMapping("/hello")
    public String hello() {
        return "hello";
    }
}

```

`**@Controller**`를 사용하는 경우에는 해당 컨트롤러의 메소드가 주로 View를 반환하도록 설계됩니다. 일반적으로 View를 템플릿 엔진을 통해 HTML 형식으로 렌더링하거나, JSON 형식으로 데이터를 반환합니다.

## @RestController 어노테이션

`**@RestController**` 어노테이션은 `**@Controller**` 어노테이션의 특별한 형태로, 해당 클래스가 RESTful 웹 서비스의 컨트롤러임을 나타냅니다.

`**@RestController**`를 사용하는 경우에는 해당 컨트롤러의 메소드가 주로 데이터를 반환하도록 설계됩니다. 이 데이터는 주로 JSON 형식으로 반환되며, HTTP 요청에 따라 다양한 형태의 데이터를 반환할 수 있습니다.

```java
@RestController
public class MyRestController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello, World!";
    }
}

```

`**@RestController**`를 사용하는 경우에는 `**@Controller**`와 달리 메소드가 단순히 데이터를 반환하기 때문에, 일반적으로 View를 렌더링할 필요가 없습니다. 대신에 해당 데이터가 클라이언트에게 직접 전송됩니다.

따라서, 주로 데이터를 반환하는 API를 작성할 때는 `**@RestController**`를 사용하고, 전통적인 웹 애플리케이션을 개발할 때는 `**@Controller**`를 사용하는 것이 일반적입니다.
