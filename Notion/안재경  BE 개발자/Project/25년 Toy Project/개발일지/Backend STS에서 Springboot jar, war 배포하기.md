---
base: "[[개발일지.base]]"
응답자: 안재경
제출 시간: 2025-03-09T23:14:00
---
jar 파일로 배포할 것인지 war 파일로 배포할 것인지 결정해서 pom.xml 을 열고 입력하자.

<packaging> 태그값을 바꾸면 된다. 기존에 해당 태그가 없다면 추가하자.

나는 war를 선택했는데 이유는 jsp를 사용하기 위해서다.

STS 상에서 기동하면 jsp가 잘 나오더라도, jar로 만들어서 java -jar 로 기동하면 jsp가 나오지 않고 Whitelabel Error Page 에러가 발생한다. jsp를 사용하려면 war로 묶도록 하자.

![[image.png]]
