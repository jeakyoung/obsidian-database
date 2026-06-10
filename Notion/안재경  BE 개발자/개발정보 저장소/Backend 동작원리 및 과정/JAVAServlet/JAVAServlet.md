---

---
### **서블릿의 역할**

- **요청 처리(Request Handling)**: 클라이언트의 요청을 받아들이고 해당 요청을 처리합니다.
- **응답 생성(Response Generation)**: 요청에 대한 응답을 생성하여 클라이언트에게 반환합니다.
- **웹 애플리케이션의 비즈니스 로직 처리(Business Logic)**: 데이터베이스 액세스, 파일 처리 등과 같은 비즈니스 로직을 처리합니다.
- **세션 관리(Session Management)**: 클라이언트와의 상태를 유지하고 세션 정보를 관리합니다.

### **서블릿의 구조**

서블릿은 보통 다음과 같은 구조를 가집니다

- **javax.servlet.Servlet 인터페이스를 구현**: 이 인터페이스를 구현하여 사용자 정의 서블릿을 생성합니다.
- **서블릿 생명주기(Lifecycle)**: 초기화(init), 서비스(service), 소멸(destroy) 등의 메서드를 통해 서블릿의 생명주기를 관리합니다.

[[[Servlet] 생명주기]]

- **HttpServletRequest 및 HttpServletResponse 객체**: 클라이언트의 요청과 서버의 응답을 처리하기 위해 사용됩니다.


```javascript
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class MyServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        // 클라이언트로부터의 GET 요청을 처리하는 로직
        response.setContentType("text/html");
        response.getWriter().println("<html><body>");
        response.getWriter().println("<h1>Hello Servlet!</h1>");
        response.getWriter().println("</body></html>");
    }
}

```


```javascript
package com.example.Lee.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {
	@GetMapping("/test")
	public String test() {
		return "안녕하세요";
	}
}
```
