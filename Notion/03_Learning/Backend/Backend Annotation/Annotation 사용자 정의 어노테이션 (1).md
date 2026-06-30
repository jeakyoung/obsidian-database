---

---
사용자 정의 어노테이션은 개발자가 직접 정의하여 자신의 코드에 적용할 수 있는 어노테이션입니다. 이를 통해 코드를 더욱 명확하게 표현하고 의미를 부여할 수 있습니다. 사용자 정의 어노테이션을 만들고 사용하는 방법은 다음과 같습니다.

### **사용자 정의 어노테이션 만들기**

사용자 정의 어노테이션을 만들기 위해서는 `**@interface**` 키워드를 사용하여 어노테이션을 정의합니다. 이 때, 메타 어노테이션 중 `**@Retention**`과 `**@Target**`을 활용하여 어노테이션이 유지되는 범위와 적용 가능한 대상을 지정합니다.

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface MyCustomAnnotation {
    String value() default "default value";
}

```

위의 예제에서 `**@Retention(RetentionPolicy.RUNTIME)**`은 어노테이션이 런타임 시에도 유지되어야 함을 나타내고, `**@Target(ElementType.METHOD)**`는 해당 어노테이션이 메소드에만 적용될 수 있음을 나타냅니다. `**MyCustomAnnotation**` 어노테이션은 `**value()**`라는 요소를 가지며 기본값은 "default value"로 설정되어 있습니다.

---

### **사용자 정의 어노테이션 사용하기**

사용자 정의 어노테이션을 사용하기 위해서는 해당 어노테이션을 클래스, 메소드 또는 필드 등에 적용합니다. 사용자 정의 어노테이션은 다른 어노테이션과 마찬가지로 `**@**` 기호를 이용하여 사용됩니다.

```java
public class MyClass {
    @MyCustomAnnotation(value = "custom value")
    public void myMethod() {
        // 메소드 내용
    }
}

```

위의 예제에서 `**@MyCustomAnnotation(value = "custom value")**`는 `**MyMethod()**` 메소드에 `**MyCustomAnnotation**` 어노테이션을 적용하고 있습니다. `**value**` 요소의 값을 "custom value"로 설정하였습니다.

이렇게 정의된 사용자 정의 어노테이션은 개발자가 원하는 대로 의미를 부여하고 코드에 적용할 수 있습니다. 사용자 정의 어노테이션은 코드의 가독성과 유지 보수성을 높이는 데에 유용하게 활용될 수 있습니다.
