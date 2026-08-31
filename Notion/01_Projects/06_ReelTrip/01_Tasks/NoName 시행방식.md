---
base: "[[Notion/프로젝트 문서화/프로젝트/NoNAME 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 진행 중
생성 일시: 2026-06-10T14:29:00
담당자: []
---
빌드 및 실행 방법

cd apps/api-spring

# 의존성 설치 및 빌드

./mvnw clean package -DskipTests

# 실행 (환경변수 필요)

java -jar target/api-0.0.1-SNAPSHOT.jar