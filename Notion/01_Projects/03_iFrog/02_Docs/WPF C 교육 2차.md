---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project Docs- 프로젝트 문서 and New data source/Project Docs- 프로젝트 문서 and New data source.base]]"
카테고리: []
생성일시: 2026-06-10T14:28:00
상태: 진행 중
---
## 프로젝트 진행 방식

- VISUAL STUDIO 2026 이상으로 사용하는 이유 : 닷넷 10.0을 도입할 준비를 해야 함. (지원 종료 기한 문제)

- C# 소스 형상 관리 도구 → GITLAB으로 진행할 예정 ( LEARNNER 적용 CI/CD 구현 해보기 )

```c#
HTTP://218.155.74.36:8959 -> 외부 망 ( 세종 개발부서용 하지만 써도 된다! )

HTTP://218.155.80.27:2080 -> 내부 망 ( 기존망 )
```

WPF → VIEW, VIEW_MODEL → 교차 분배 작업 하기

개발하는 스크린에 대한 전체적인 공유가 필요

- [PROPERTY], [COMMAND] → 사전 명세 후 명세에 맞게 개발이 필요

비지니스 로직, 통신, 가공부는 VIEW_MODEL로 넘기지 말고 SERVICE내에 공통 함수를 만들어서 쓰기 ( DI구조 활용 )

장비통신 <> 프로토콜과 인터페이스를 가지고 진행

모드버스 통신을 통해 온도를 받아와서 조회, 저장하는 과정 ( 장비 통신에서 가장 기초적인 과정 )

송연 → 시리얼 통신을 진행 ( RS232, TCP, RS485 ) 연결 시도시 테스트통신을 1회 진행하고 반환값을 받아봐야 연결이 되어있는건지 끊어졌는지 확인이 가능함 → IsThread로 관리

BUFFER에 쌓인정보들을 지우고 포맷팅 해주는 사전가공이 필요 → 데이터가 처음들어오는곳

→ 통신시도 시에는 필히 유효성 체크 진행해야함

→ IUD 동작시 SET 동작에 함수를 호출할수 있음 → 굳이 플래그값 바꿔가면서 비교할필요가없음

뷰코드와 뷰에대한 코드비하인드가 존재함 → 기능구현 X 


- behavior 정의시 문자, 숫자 제한용
    - 입력 : 입력되고 있는 문자를 하나씩 확인
    - 출력: 하나라도 정의한 타입에서 벗어나면 입력을 제한함

| 함수 | 의미 | 예시 |
| --- | --- | --- |
| `char.IsDigit(c)` | 숫자(0~9) | '1', '8' |
| `char.IsLetter(c)` | 알파벳 문자 | 'A', 'z' |
| `char.IsLetterOrDigit(c)` | 문자 또는 숫자 | 'A', '3' |
| `char.IsLower(c)` | 소문자 | 'a', 'z' |
| `char.IsUpper(c)` | 대문자 | 'A', 'Z' |
| `char.IsWhiteSpace(c)` | 공백 문자 | ' ', '\t', '\n' |
| `char.IsSymbol(c)` | 수학/기호 문자 | '+', '÷', '=' |
| `char.IsPunctuation(c)` | 구두점 | ',', '.', ';', '?' |
| `char.IsControl(c)` | 제어 문자 | '\n', '\0' |
| `char.IsNumber(c)` | 숫자(유니코드 전체 숫자) | 로마 숫자, 원문 숫자 |
| `char.IsSeparator(c)` | 구분자 | 특수 유니코드 스페이스 |
| `char.IsSurrogate(c)` | UTF-16 Surrogate | 이모지 등 |