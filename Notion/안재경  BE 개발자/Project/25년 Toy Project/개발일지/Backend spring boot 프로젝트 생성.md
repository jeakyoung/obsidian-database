---
base: "[[개발일지.base]]"
응답자: 안재경
제출 시간: 2025-03-09T22:29:00
---
1. spring boot project 생성

![[image 1.png]]


2. 각종 의존성 추가
- mariaDB → MySQL

![[image 2.png]]


3. src/main/resources/application.properties 수정하기
- 실제 SQL정보는 아니나 mySQL드라이버의 오류 해결을 위해 임시 작성

![[image 3.png]]

```javascript
spring.mvc.view.prefix=/WEB-INF/views/
spring.mvc.view.suffix=.jsp
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost:3306/SchemaName
spring.datasource.username=username
spring.datasource.[placeholder]
server.servlet.encoding.charset=utf-8
server.servlet.encoding.enabled=true
server.servlet.encoding.force=true

```

4. porm.xml 파일 dependency 수정

```xml
<!-- TOMCAT -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-tomcat</artifactId>
    <scope>provided</scope>
</dependency>

<!-- JSP -->
<dependency>
    <groupId>org.apache.tomcat.embed</groupId>
    <artifactId>tomcat-embed-jasper</artifactId>
</dependency>

<!-- JSTL -->
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>jstl</artifactId>
</dependency>

```

5. 테스트 파일 생성후 출력

![[image 4.png]]

![[image 5.png]]

![[image 6.png]]