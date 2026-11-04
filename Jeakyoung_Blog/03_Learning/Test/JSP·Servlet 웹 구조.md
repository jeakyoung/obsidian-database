---
title: JSP·Servlet 웹 구조
date: 2026-10-14
type: 학습자료
status: 완료
tags: []
---

# JSP·Servlet 웹 구조

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **분류** | 면접준비 |
| **관련 기술** | JSP, Servlet, Tomcat, MVC, Spring MVC |
| **정리일** | 2026-10-14 |

> 전통적인 ENOVIA 화면이 JSP 기반이므로, 요청이 들어와서 화면이 그려지기까지의 Java 웹 구조를 면접 답변 수준으로 정리.

## 🧩 핵심 개념

- **WAS(Tomcat 등)** 안의 **서블릿 컨테이너**가 HTTP 요청을 받아 서블릿을 실행하고 응답을 돌려준다
- **JSP는 서블릿으로 변환되어 실행**되는, HTML 작성에 특화된 서블릿
- **MVC(Model 2)**: Controller(서블릿)가 요청을 받고, Model(비즈니스 로직/데이터)을 호출하고, View(JSP)가 화면을 그린다

## 📖 상세 내용

### 1. 요청 처리 흐름

```text
브라우저
  → (HTTP 요청) 웹 서버 / WAS(Tomcat)
  → 서블릿 컨테이너: URL 매핑으로 담당 서블릿 결정
  → Filter (인코딩, 로그인 체크 등 공통 처리)
  → Servlet(Controller): 파라미터 받기 → Service/DAO 호출
  → request에 결과 담고 JSP로 forward
  → JSP(View): HTML 생성
  → (HTTP 응답) 브라우저
```

### 2. 서블릿 생명주기

| 단계 | 메서드 | 시점 |
|:--|:--|:--|
| 초기화 | `init()` | 첫 요청 시(또는 서버 시작 시) **딱 한 번** |
| 처리 | `service()` → `doGet()`/`doPost()` | 요청이 올 때마다 |
| 종료 | `destroy()` | 서버 종료/재배포 시 한 번 |

> 꼬리질문: "서블릿은 요청마다 새로 만들어지나요?" → 아니다. **객체는 하나**고 요청마다 스레드가 새로 붙는다. 그래서 서블릿의 멤버 변수에 사용자별 데이터를 저장하면 다른 사용자 요청과 섞이는 동시성 버그가 생긴다 (지역 변수를 써야 함).

```java
@WebServlet("/part/detail")
public class PartDetailServlet extends HttpServlet {
    private final PartService partService = new PartService(); // 상태 없는 객체는 OK

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        String partId = req.getParameter("partId");      // 지역 변수
        req.setAttribute("part", partService.find(partId));
        req.getRequestDispatcher("/WEB-INF/views/partDetail.jsp").forward(req, resp);
    }
}
```

### 3. JSP 문법 기초

```jsp
<%@ page contentType="text/html; charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<h2>${part.partName}</h2>              <%-- EL: request 속성 출력 --%>
<c:forEach var="child" items="${part.children}">
    <p>${child.partId} - ${child.partName}</p>
</c:forEach>
```

- **스크립틀릿**(`<% 자바코드 %>`)은 화면과 로직이 섞여 유지보수가 어려워서, 지금은 **EL + JSTL** 사용을 권장
- **JSP 내장 객체**: `request`, `response`, `session`, `application`, `out`, `pageContext` 등 — 선언 없이 바로 사용 가능

### 4. forward vs redirect

| | forward | redirect |
|:--|:--|:--|
| 동작 | 서버 내부에서 다른 페이지로 넘김 | 브라우저에게 "이 URL로 다시 요청해"라고 응답 |
| 요청 횟수 | 1번 | 2번 |
| 주소창 URL | 안 바뀜 | 바뀜 |
| request 데이터 | 유지됨 | 사라짐 |
| 주 용도 | 조회 결과를 JSP로 전달 | 저장/수정 후 목록으로 이동 (새로고침 시 중복 등록 방지 — PRG 패턴) |

### 5. 세션 vs 쿠키

| | 쿠키 | 세션 |
|:--|:--|:--|
| 저장 위치 | 브라우저 | 서버 |
| 보안 | 사용자가 보거나 조작 가능 | 상대적으로 안전 |
| 동작 | 요청마다 브라우저가 자동 전송 | 세션 ID(`JSESSIONID`)만 쿠키로 주고받고 실제 데이터는 서버에 |
| 용도 | 아이디 저장, 팝업 안 보기 | 로그인 정보 |

> 실무 경험 연결: JWT는 세션 대신 토큰 자체에 사용자 정보를 담아 서버가 상태를 저장하지 않는(stateless) 방식 — 직접 구현해봤다면 비교해서 설명하기 좋은 포인트.

### 6. Filter vs Interceptor, 그리고 Spring MVC

- **Filter**: 서블릿 컨테이너 레벨, 서블릿 실행 **전/후** 공통 처리 (문자 인코딩, 인증 체크, 로깅)
- **Interceptor**: Spring 레벨, 컨트롤러 실행 전/후 처리 (Spring Bean 사용 가능)
- **Spring MVC**는 서블릿 위에 만들어진 프레임워크 — `DispatcherServlet`이라는 서블릿 **하나**가 모든 요청을 받아서 URL에 맞는 `@Controller` 메서드로 분배(프론트 컨트롤러 패턴). 즉 Spring을 써도 내부 원리는 서블릿

## 💡 정리 및 활용

- "JSP는 결국 서블릿이다", "서블릿은 하나의 객체를 여러 스레드가 공유한다" 두 문장이 이 영역 꼬리질문의 출발점
- forward/redirect, 세션/쿠키는 표 그대로 비교형 답변이 가능하도록 정리
- ENOVIA 화면이 JSP 기반이라는 점과 연결해 "레거시 JSP를 읽고 수정할 수 있는 기본기는 있다"는 식으로 마무리하면 좋음

## 🔗 참고

- [[03_Learning/Test/ENOVIA PLM 개념 정리]]
- [[03_Learning/Test/Java 핵심 개념 Q&A]]
- [[03_Learning/Test/기술스택 종합 문제]]
