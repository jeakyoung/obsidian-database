---
title: Servlet-Process-MyBatis 계층 구조
date: 2026-09-18
type: 기술문서
project: 대학프로젝트
status: 완료
category: 아키텍처
assignee:
  - 안재경
tags: []
---

# Servlet-Process-MyBatis 계층 구조

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | `OpenSoopBack` 전체 (`account`/`home`/`community`/`gallery`/`admin` 패키지) |
| **적용 범위** | 아키텍처 |
| **관련 모듈** | `*Srv`(Servlet), `*TtableOut`/`*process`(비즈니스 로직+DB 접근), `/mybatis-config.xml`, `/mappings/uni-*.xml` |

> Spring 없이 순수 Servlet 3.1 + MyBatis 3.5.6으로 짜인 구조. Controller/Service/DAO가 분리되지 않고, Servlet이 요청을 파싱한 뒤 곧바로 "비즈니스 로직 + DB 접근"을 겸하는 클래스 하나를 호출하는 2계층 구조다.

## 🎯 배경 및 요구사항

학기 프로젝트라 별도 프레임워크 학습 없이 Java 표준 Servlet API와 MyBatis만으로 API 서버를 구현해야 했다. `pom.xml`에 Spring 의존성이 없고, `web.xml` 배포 서술자도 없다 — 서블릿 매핑은 전부 `@WebServlet` 애노테이션으로 처리된다.

## 🏗 설계 및 구현

### 요청 흐름

```
[Client] --JSON body--> @WebServlet("/XxxSvc") extends HttpServlet
    doPost()
      1. request.setCharacterEncoding("utf8")
      2. BufferedReader로 요청 바디를 한 줄씩 읽어 문자열로 합치기
      3. JSONObject.fromObject(문자열) 로 파싱 (json-lib)
      4. 필요한 키를 하나씩 꺼내 Map<String,Object> param 구성
      5. new XxxProcess(param)  ← 생성자 안에서 바로 DB 작업 수행
      6. process.getResult() 로 JSONObject 결과 획득
      7. response.getWriter().print(결과)
```

`XxxProcess`(파일명 관례상 `*TtableOut` 또는 그냥 도메인명, 예: `LonginTtableOut`, `MembReglns`, `FreeAdmin`)는 생성자에서:

```java
String resource = "/mybatis-config.xml";
InputStream inputStream = Resources.getResourceAsStream(resource);
SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
SqlSession session = sqlSessionFactory.openSession();
try {
    Map<String, Object> rtn = session.selectOne("uni-account-mapping.selectXxx", param);
    // ... JSONObject 조립
    session.commit();
} catch (Exception e) {
    e.printStackTrace();
} finally {
    if (session != null) session.close();
}
```

요청마다 `SqlSessionFactoryBuilder().build()`를 새로 호출해 `mybatis-config.xml`을 다시 파싱한다 — MyBatis 내부의 `POOLED` 데이터소스가 커넥션 자체는 재사용하지만, 설정 파싱과 `SqlSessionFactory` 생성 자체는 요청마다 반복된다.

### 응답 규약

서비스 계층이 없어 예외/결과 코드를 응답 JSON의 `RSLT_CD` 필드로 직접 표현한다. 관례상:

| 값 | 의미 |
|:--:|:--|
| `00` | 정상 |
| `01` | 조회 결과 없음 / 실패 |
| `03` | 중복(ID·닉네임 등) |
| `99` | 예외 발생(`catch` 블록에서 설정) |

컨트롤러 레벨 공통 예외 처리기가 없어서, 이 코드 규약을 지키는지는 클래스마다 개별 구현에 달려 있다 — `admin` 패키지의 `FreeAdmin`/`RequestAdmin`/`MarketAdmin`/`AskAdmin`처럼 `catch` 블록에 `RSLT_CD` 세팅이 아예 빠진 경우도 있다.

### 매퍼 등록

```xml
<!-- mybatis-config.xml -->
<mappers>
  <mapper resource="/mappings/uni-mapping.xml"/>
  <mapper resource="/mappings/uni-account-mapping.xml"/>
  <mapper resource="/mappings/uni-home-mapping.xml"/>
  <mapper resource="/mappings/uni-community-mapping.xml"/>
  <mapper resource="/mappings/uni-gallery-mapping.xml"/>
</mappers>
```

패키지(`account`/`home`/`community`/`gallery`)와 매퍼 XML이 1:1로 대응하지만, `admin` 패키지는 별도 매퍼 없이 `uni-account-mapping.xml`/`uni-community-mapping.xml`의 쿼리를 그대로 가져다 쓴다.

## ✅ 검증

- [x] `@WebServlet` 매핑 경로와 Servlet 클래스 1:1 대응 확인 (`web.xml` 없이도 Tomcat이 애노테이션 스캔으로 인식)
- [x] `mybatis-config.xml`의 매퍼 5개가 각 도메인 패키지와 대응되는지 확인
- [ ] 요청마다 `SqlSessionFactory`를 새로 빌드하는 비용이 실제 트래픽에서 문제가 되는 수준인지는 별도로 측정된 적 없음

## 🔗 참고

- [[../02_Docs/23년 Open Soop 개발 과정|23년 Open Soop 개발 과정]]
- [\[기술\] 게시판 모니터링 API 응답 구조와 한계](<[기술] 게시판 모니터링 API 응답 구조와 한계.md>)
