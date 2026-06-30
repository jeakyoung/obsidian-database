---

---
## Vibe Coding 도입 예상안 ( Claude MCP ↔ InteliJ ↔ Codex )

- LLM API를 활용 작업진행시 광범위 분석에 유리한 Claude 단순 작업에 유리한 Codex를 섞어 쓰기 위한 환경 조성.
- 하나의 LLM의 토큰만 사용하게 되면 작업 계획을 위한 분석 / 시행 하기에 무료 토큰 입장에선 불리함 
- 토큰을 효율적으로 사용하기 위한 구조 개선안 / 대용량 자료 정리, 계획안 수립 ( claude ) / 명세되어있는 작업내용대로 단순 반복작업 ( Codex )
- 이렇게하면 각자 작업이 반반 나뉘기에 무료토큰을 두배로 활용할 수 있는 장점이 있음 ( 효율검증 X 그냥 내 생각 )
- **치명적 단점 : 유료전환 시 이렇게 하면 요금이 두배가 되어버림 ( 양쪽에서 자동충전을 해버리기에 )

```plain text
IntelliJ (개발 환경)
↓
Claude Desktop + MCP (전체 구조 분석 & 설계)
↓
실행 명세
↓
Codex CLI (코드 생성/수정 실행)
↓
IntelliJ (검증 & 테스트)
```

```plain text
현재 프로젝트를 분석해서 아래 형식으로 변경 계획을 작성해줘

[목표]
(무엇을 왜 바꾸는지)

[수정 대상 파일]
- 파일 경로 포함해서 나열

[변경 내용]
- 각 파일별로 무엇을 어떻게 바꾸는지 구체적으로

[의존성 영향]
- 같이 수정해야 할 클래스/로직

[제약 조건]
- 기존 API 유지 여부
- 트랜잭션
- 성능 고려사항

[리스크]
- 깨질 가능성 있는 부분

설명은 최소화하고, 실행 가능한 계획 위주로 작성
```

```plain text
[작업 목표]
User 조회 성능 개선

[수정 파일]
- src/main/java/.../UserService.java
- src/main/java/.../UserRepository.java

[요구사항]
1. N+1 문제 해결
2. fetch join 적용
3. 기존 API 응답 구조 유지

[제약 조건]
- 트랜잭션 범위 변경 금지
- 기존 메서드 시그니처 유지

[출력 형식]
- 수정된 코드만 출력
- 설명 금지
```

---

## 전체 진행 방식 명세

### → 클로드 프롬포트 사용자지정 ( 호출방식** /planning-prompt **)

![[image 88.png]]

### → claude desktop ↔ inteliJ MCP 연결방식

![[image 89.png]]

- C:\Users\USER\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json

```json
{
  "mcpServers": {
    "jetbrains": {
      "command": "C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\jbr\\bin\\java.exe",
      "args": [
        "-classpath",
        "C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\plugins\\mcpserver\\lib\\mcpserver-frontend.jar;C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\lib\\util-8.jar;C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\lib\\intellij.libraries.kotlinx.coroutines.core.jar;C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\lib\\intellij.libraries.ktor.client.cio.jar;C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\lib\\intellij.libraries.ktor.client.jar;C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\lib\\intellij.libraries.ktor.network.tls.jar;C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\lib\\intellij.libraries.ktor.io.jar;C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\lib\\intellij.libraries.ktor.utils.jar;C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\lib\\intellij.libraries.kotlinx.io.jar;C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\lib\\intellij.libraries.kotlinx.serialization.core.jar;C:\\Program Files\\JetBrains\\IntelliJ IDEA 2025.3.2\\lib\\intellij.libraries.kotlinx.serialization.json.jar",
        "com.intellij.mcpserver.stdio.McpStdioRunnerKt"
      ],
      "env": {
        "IJ_MCP_SERVER_PORT": "64342"
      }
    }
  },
  "preferences": {
    "coworkScheduledTasksEnabled": false,
    "ccdScheduledTasksEnabled": false,
    "coworkWebSearchEnabled": true,
    "sidebarMode": "chat"
  }
}
```

### → 프롬포트대로 출력된 결과물 ( ** 반드시 ** 내용 확인, 수정할 것. )

- 요청
```plain text
/planning-prompt  프로젝트 전체구조 확인하고 프롬포트에 맞게 CRUD 오류 수정이 필요한 
부분을 요약해봐
```

- 결과

[[Claude 출력결과.pdf]]

### → 요걸루 코덱스 작업지시서를 작성 ( 1번작업 지시 )

```plain text
[작업 목표]
searchByVector() 런타임 오류 가능성 제거

[수정 파일]
- src/main/java/com/devahn/document/repository/DocumentRepositoryImpl.java

[요구사항]
1. SELECT 절에서 similarity 컬럼 제거
2. embedding <=> 연산 기준 정렬 유지
3. 불필요한 파라미터 제거 (vector 중복 전달 제거)
4. documentRowMapper와 컬럼 구조 일치 유지

[제약 조건]
- DocumentRepository 인터페이스 시그니처 유지
- pgvector 연산자 (<=>) 유지
- 기존 반환 타입 및 구조 변경 금지

[출력 형식]
- 수정된 코드만 출력
- 설명 금지
```

### → 그걸 이제 코덱스놈한테 작업하라고 시킨다.

** 여기부턴 효율 검증이 필요함 코덱스 성능이 너무 안 나오거나 코덱스 토큰이 먼저 달아버리는 현상 발생시 재고려 필요

![[image 90.png]]

### → 그럼 백정 “코덱스”는 순전히 코드 작업만 진행한다 

( 황족 “클로드” 님이 해야 했던 불필요한 노가다를 짬통 코덱스가 대신 처리 )

![[image 91.png]]

~~** 클로드 API가 돈달라길레 꼴받아서 조성해봄.~~

---