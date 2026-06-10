---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:29:00
담당자: []
---
[[scheduler-test.zip]]

api를 호출하면서
request parameter로 (title,body,empList, type)를 받고,
empList를 TGI001에서 해당 emp들 중 TGI001에 실제 데이터가 있는지 여부를 확인하여
TGI001에 포함된 유저의 token 추려낸 뒤
해당 추려낸 유저들의 리스트를  FCM 메세지에 title, body, empTokenList 를 발송
TGI002 에 알림내역에 저장
firebase Server에 전달 후 유저(client)에게 noti 알림 발생

![[image 177.png]]

→ 단순센더 요청 파라미터

![[image 178.png]]

→ 서버 전달부

