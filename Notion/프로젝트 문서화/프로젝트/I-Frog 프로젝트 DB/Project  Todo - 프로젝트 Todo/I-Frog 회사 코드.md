---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 진행 중
생성 일시: 2026-06-10T14:28:00
담당자: []
---
## ㅇ TCO101 → 131, 132 → 000001 공통코드 조회

![[image 180.png]]

ㅇATC

![[image 181.png]]

ㅇ 동방

![[image 182.png]]

ㅇ 송연

- 위는 WEB에서 회사 코드를 관리하는 방안입니다, 보통 000001이 자사, 아래로 붙는 것들이 외주사로 관리되고 있습니다. 

![[image 183.png]]

ㅇ TGI 001, 2, 3

→ 작업 사항은 추후 진행할 통합처리를 위해 COMPANY_CODE + EMPLOYEE_NO 조합이 유일하게 만드는 것이었습니다.

→ 그런데 여기서 COMPANY_CODE를 임의로 COMPANY_NAME 처리 하게 되면 문제가 발생합니다. 

기존 웹에서 기준정보로 공통 코드 관리하는 이름을 COMPANY_CODE를 사용해서 끌어오는 식으로 이름을 

표기하고 있는데 이미 관리되고 있는 기준 정보를 새로 만들어서 사용자의 공통코드 수정사항에 따라 

매번 하드코딩으로 관리해야 하는 상황이 생깁니다.

(000001로 ATC의 이름을 가져와서 저장할 순 있지만 WEB 기준정보 - 공통코드에서 수정 사항이 생길경우

나중에 역으로 불러올때 ATC로 저장된 데이터가 000001인지 알수가 없습니다. )

→ ATC, 동방, 송연 DATABASE를 하나로 통합할 계획이라면 위 3개의 사진처럼 공통 코드를 만들어서 

ATC, 동방, 송연에 대한 COMPANY_CODE를 다르게 관리 하는것이 맞을것 같습니다. 

→ 기존대로 데이터 베이스를 분리해서 사용한다면 000001에 대한 값이 3가지 DB 모두 자사 이름으로 다르게 들어가 있기에 똑같은 로직으로 같은 값이더라도 각 회사마다 고유한 값을 이미 만들수 있습니다.


→ 보안코드 인증 → TICKER를 넘겨받음 → TICKER로 CONN 생성 → DB 연결후 로그인 시도시에

→ TGI000을  SELECT → 도메인주소, 회사이름 반환


[https://mong-dev-note.tistory.com/18](https://mong-dev-note.tistory.com/18)

[로그인 성공]
↓
[사용자 소속 회사/DB 결정]
↓
[JWT Claim에 ticker 포함]
↓
[모든 요청에서 JWT 자동 전달]
↓
[서버에서 Claim 꺼내서 DB 라우팅]


api/Connect/Conn

request:

- paramter "보안코드"

response:

- data : mgi000

ex :

data : "companyName : "atc",

"domain" : "[http://www.atc.com](http://www.atc.com/)"

- ---

String domain = response.data["domain"];  //클라이언트에서 전역사용

[보안코드 입력] → 해당단계에서부터 어떤DB를 타겟팅하는지 알고있어야함

↓

[ticker와 함께 도메인 반환 ( TGI000 )]  

↓

[ticker로 db커넥션 재설정]

↓

[소스내 전역변수로 선언된 ticker로 db연결]

↓

[보안코드로 지정된 DB로 서비스진행]


1. 전역변수를 만들어 첫 서비스에 대한 리턴값으로 앞으로 있을 모든 서비스 요청에서 동일한 값의 Ticker

( 동일한 db ) 타겟팅할수 있는지

2. 보안코드로 받고 ticker를 만들고 ticker로 db를찾아서 도메인 정보를 select 해와야 하는데 3개의 DB 커넥션을 동시관리 해야하는 상황에 이런게 가능한지

