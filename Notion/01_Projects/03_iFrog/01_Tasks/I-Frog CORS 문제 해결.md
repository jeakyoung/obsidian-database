---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:29:00
담당자: []
---
# CORS 에러 해결 가이드

## 📋 제공된 파일

1. **CORSFilter.java** - CORS 필터 (모든 요청에 자동 적용)
2. **jvLCRM_LIST_01_LIST.java** - 개선된 Servlet (SQL Injection 방지 포함)

## 🚀 설치 방법

### 1단계: 파일 배치

```plain text
프로젝트/
├── src/
│   └── main/
│       ├── CORSFilter.java          ← 새로 추가
│       └── jvLCRM_LIST_01_LIST.java ← 기존 파일 교체
```

### 2단계: 컴파일 및 배포

3. 프로젝트를 빌드합니다
4. 서버를 재시작합니다

## ✅ CORS 필터 주요 기능

### 설정된 CORS 헤더

```java
Access-Control-Allow-Origin: <http://localhost:1841>
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 3600
```

### Preflight 요청 자동 처리

- OPTIONS 메서드 요청을 자동으로 처리
- 브라우저의 사전 요청을 차단 없이 통과

## 🔧 환경별 설정 변경

### 개발 환경 (현재 설정)

```java
httpResponse.setHeader("Access-Control-Allow-Origin", "<http://localhost:1841>");
```

### 여러 Origin 허용

```java
String origin = httpRequest.getHeader("Origin");
List<String> allowedOrigins = Arrays.asList(
    "<http://localhost:1841>",
    "<http://localhost:3000>",
    "<https://yourdomain.com>"
);

if (allowedOrigins.contains(origin)) {
    httpResponse.setHeader("Access-Control-Allow-Origin", origin);
}
```

### 모든 Origin 허용 (개발용만, 보안 취약)

```java
httpResponse.setHeader("Access-Control-Allow-Origin", "*");
// 단, Credentials를 사용할 경우 "*"는 불가능
```

## 🔒 보안 개선 사항

### Servlet 코드 개선점

5. **SQL Injection 방지**
    - Statement → CallableStatement 변경
    - 파라미터 바인딩 사용
```java
// 이전 (취약)
String sql = " EXEC SP_WCRM_LIST_01_LIST '" + CUSTOMER_CODE + "','" + ORDER_DATE + "'";

// 개선 (안전)
String sql = "{call SP_WCRM_LIST_01_LIST(?, ?)}";
cstmt = conn.prepareCall(sql);
cstmt.setString(1, CUSTOMER_CODE);
cstmt.setString(2, ORDER_DATE);
```
6. **문자열 비교 개선**
```java
// 이전
if(strSuccess == "false")

// 개선
if(strSuccess.equals("false"))
```

## 🧪 테스트 방법

### 1. 브라우저 개발자 도구에서 확인

7. F12를 눌러 개발자 도구 열기
8. Network 탭 선택
9. 요청 실행
10. 응답 헤더에서 `Access-Control-Allow-Origin` 확인

### 2. CORS 에러 해결 확인

```plain text
이전:
❌ Access to XMLHttpRequest has been blocked by CORS policy

이후:
✅ 정상적으로 데이터 로드됨
```

## ⚠️ 주의사항

11. **필터 우선순위**
    - `@WebFilter("/*")`로 모든 요청에 자동 적용됩니다
    - 다른 필터와 충돌 시 `@WebFilter(filterName="CORSFilter", urlPatterns={"/*"})` 사용
12. **운영 환경 배포 시**
    - Allow-Origin을 실제 도메인으로 변경
    - 불필요한 HTTP 메서드 제거
    - 로깅 추가 권장
13. **성능 고려**
    - `Access-Control-Max-Age: 3600`로 Preflight 캐싱 (1시간)

## 🐛 문제 해결

### CORS 에러가 여전히 발생하는 경우

14. **서버 재시작 확인**
```bash
서버를 완전히 재시작했는지 확인
```
15. **필터가 로드되었는지 확인**
```plain text
서버 로그에서 CORSFilter 로드 메시지 확인
```
16. **브라우저 캐시 삭제**
```plain text
Ctrl + Shift + Delete로 캐시 삭제
```
17. **디버깅**
```java
// CORSFilter.java의 doFilter 메서드에 추가
System.out.println("CORS Filter Applied - Origin: " + httpRequest.getHeader("Origin"));
```

## 📞 추가 지원

문제가 계속되면 다음을 확인해주세요:

- 서버 콘솔 로그
- 브라우저 콘솔의 정확한 에러 메시지
- web.xml 설정 (필터 중복 여부)




→ 결론

```javascript
//  CORS 설정
res.setHeader("Access-Control-Allow-Origin", "http://localhost:1841");
res.setHeader("Access-Control-Allow-Methods", "GET");
res.setHeader("Access-Control-Allow-Headers", "X-Requested-With");
```

해당과 같이 헤더정보설정을 서버내에 실어준다 연결허용 정책
