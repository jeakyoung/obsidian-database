---
base: "[[DB_토이 프로젝트.base]]"
우선순위: 높음
상태: 완료
이슈번호: 1
Displayed_우선순위: 우선순위 높음
이슈 타입: 버그
생성일시: 2025-03-09T17:30:00
---
### 버그 설명

Multiple markers at this line

- 'dependencies.dependency.version' for javax.servlet:jstl:jar is missing.
- Project build error: 'dependencies.dependency.version' for javax.servlet:jstl:jar is missing.

![[image 8.png]]

### 해결방법

에러 원인은 버전이 없었기 때문이었다

<version>1.2</version> 한줄 추가함으로써 빌드 완료


