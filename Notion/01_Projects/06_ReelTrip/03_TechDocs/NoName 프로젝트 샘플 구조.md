---

---
## ㅇ Project Structure

```plain text
project-root/
├─ backend/
│   ├─ src/main/java/com/projectname/
│   │   ├─ controller/          # REST API 엔드포인트
│   │   │   └─ LLMController.java
│   │   ├─ service/             # 비즈니스 로직
│   │   │   ├─ LLMService.java
│   │   │   └─ MilvusService.java
│   │   ├─ repository/          # Milvus 연동
│   │   │   └─ MilvusRepository.java
│   │   ├─ model/               # DTO, Document 등
│   │   │   ├─ Document.java
│   │   │   ├─ QuestionRequest.java
│   │   │   └─ AnswerResponse.java
│   │   ├─ config/              # 환경설정
│   │   │   ├─ MilvusConfig.java
│   │   │   ├─ LLMConfig.java
│   │   │   └─ WebConfig.java
│   │   └─ utils/               # Embedding 변환, 공통 함수
│   │       └─ EmbeddingUtil.java
│   ├─ src/main/resources/
│   │   ├─ application.yml      # Milvus, LLM, DB, 서버 설정
│   │   └─ logback-spring.xml   # 로깅 설정
│   └─ Dockerfile               # Spring Boot 배포용
├─ milvus/
│   ├─ docker-compose.yml       # Milvus 컨테이너 구성
│   └─ init/                    # 초기 컬렉션, 스키마 설정
├─ frontend/                     # React/Flutter 앱
│   └─ ...
└─ README.md
```

→ 예상 소스 인프라 구조 정리

```plain text
src/main/java/com/projectname
├─ controller/      # REST API 엔드포인트
│   └─ LLMController.java
├─ service/         # 비즈니스 로직 (LLM 처리, Milvus 검색 등)
│   ├─ LLMService.java
│   └─ MilvusService.java
├─ repository/      # DB/벡터 DB 접근 계층
│   └─ MilvusRepository.java
├─ model/           # DTO, Request/Response, Document 클래스 등
│   ├─ Document.java
│   ├─ QuestionRequest.java
│   └─ AnswerResponse.java
├─ config/          # Milvus, LLM, CORS 등 환경 설정
│   ├─ MilvusConfig.java
│   └─ LLMConfig.java
└─ utils/           # 공통 유틸, Embedding 변환 등
```

→ 기본 백엔드 구조

```java
@PostMapping("/api/ask")
public ResponseEntity<AnswerResponse> ask(@RequestBody QuestionRequest request) {
    AnswerResponse response = llmService.getAnswer(request);
    return ResponseEntity.ok(response);
}
```

→ 샘플 호출 구조

```java
[유저 앱] → POST /api/ask → [Controller]
      ↓                       ↓
  입력 검증                 Service Layer
                              ├─ MilvusService → 유사 문서 검색
                              └─ LLMService → 답변 생성
      ↓
  JSON 응답 → [유저 앱]
```

→ sample data flow

---

## ㅇ Tech Stack

- BE

| 영역 | 기술 / 도구 | 용도 |
| --- | --- | --- |
| **언어 & 프레임워크** | Java 17+, Spring Boot 3 | REST API 개발, 서비스 로직 구현 |
| **웹 서버** | Tomcat 내장 (Spring Boot), Nginx (배포 시) | 요청 처리, HTTPS 리버스 프록시 |
| **REST API 설계** | Spring Web | Controller → Service → Repository 구조 |
| **비즈니스 로직** | Spring Service, @Async | Milvus 검색, LLM 호출, 비동기 처리 |
| **데이터 접근** | Milvus Java SDK / gRPC | 벡터 DB CRUD, 검색 |
| **환경 설정** | Spring @Configuration, application.yml | Milvus 호스트/포트, LLM API 키, 서버 설정 |
| **DTO/모델** | Lombok(Optional), Java Classes | 요청/응답 구조, Document, QuestionRequest 등 |
| **유틸/공통 모듈** | Embedding 변환, JSON 처리 | 텍스트 → 벡터 변환, 공통 기능 |

- FE

| 영역 | 기술 / 도구 | 용도 |
| --- | --- | --- |
| **웹/앱 프론트** | React / Vue / React Native / Flutter | 사용자 인터페이스, API 호출, 질문 입력/답변 표시 |
| **통신** | Axios / Fetch API | REST API 호출 |
|   |   |   |

- vector DB

| 영역 | 기술 / 도구 | 용도 |
| --- | --- | --- |
| **벡터 DB** | Milvus (Docker) | 텍스트/문서 임베딩 벡터 저장, 유사도 검색 |
| **임베딩 생성** | OpenAI Embeddings API / 로컬 LLaMA | 질문/문서 → 벡터 변환 |
| **LLM 처리** | OpenAI GPT API / 로컬 LLaMA/MPT | 질의응답, 요약, 자연어 처리 |

- manage

| 영역 | 기술 / 도구 | 용도 |
| --- | --- | --- |
| **컨테이너** | Docker, Docker Compose | Milvus + Spring Boot 배포 및 관리 |
| **클라우드** | AWS / GCP / Azure | 실제 서비스 배포 환경 |
| **HTTPS/보안** | Nginx + SSL, JWT 인증 | API 보안, 사용자 인증 |
| **CI/CD** | GitHub Actions / Jenkins | 자동 빌드, 테스트, Docker 이미지 배포 |
| **모니터링** | Prometheus, Grafana, ELK | LLM 응답 시간, Milvus 쿼리 시간, 서버 상태 모니터링 |
| **로깅** | Logback / SLF4J | 서버 로그, 에러 추적 |

- Tool

| 영역 | 도구 | 용도 |
| --- | --- | --- |
| **IDE** | IntelliJ IDEA | Spring Boot, Java 개발 |
| **버전 관리** | Git, GitHub | 협업, 코드 관리 |
| **문서화** | Swagger / OpenAPI | REST API 명세 |
| **테스트** | JUnit, Mockito | 단위 테스트, 통합 테스트 |

---

## ㅇ Role

| 역할 | 담당 | 주요 업무 | 신입 적합성 / 참고 |
| --- | --- | --- | --- |
| **팀 리더 / 백엔드 주도** | 재경 | - Spring Boot REST API 설계/구현- Milvus + LLM 연동- 비동기 처리, 예외 처리, 배포- 팀 가이드 및 코드 리뷰 | 핵심 개발자 + 리더 |
| **UI/UX 디자이너** | 미현 | - 앱/웹 화면 설계- 와이어프레임/프로토타입 제작- 사용자 경험 개선 | 디자인 전문, 개발 경험 없어도 가능 |
| **Milvus / LLM 담당** | 형민 | - Milvus + RDBMS 경험 쌓기벡터 DB 컬렉션 관리, 임베딩 처리선택적으로 RDB 설계/쿼리 최적화 실습 | 신입 0~1년 수준 가능 |
| **프론트엔드 / 통합 담당** | 하윤 | - React/Flutter 앱 구현- API 연동 테스트- UI/UX 디자이너와 협업 | 신입 0~2년 수준 가능 |
|   |   |   |   |

---



