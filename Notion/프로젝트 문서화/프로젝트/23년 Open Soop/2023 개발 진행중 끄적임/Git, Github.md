---
base: "[[2023 개발 진행중 끄적임.base]]"
상태: 완료 🙌
---
Git과 Github의 차이점 → Git은 기본적으로 터미널을 이용하여 조작할수 있는 로컬 저장소이다.

이를 공유하고 PR과 같은 기능으로 협업할수 있도록 만든 클라우드 서비스가 Github이다.

Git(저장소) 내컴퓨터 ↔ Github(클라우드 서비스)

*PR이란 Pull Request의 약자로 한 서비스 내에 코드를 통합할수 있도록 다른개발자에게 리뷰를 요청하는 기능이다.

→ 협업에 매우 유용함.

*커밋 → history를 남기는것 변경기록, 변경시간등을 기록.

*Push, Pull = 내컴퓨터에서 git을 통해 github codespace에 업로드 → Push 

github codespace에서 git을 통해 내컴퓨터로 가져옴 → Pull


VS code 에서 터미널을 이용 내 github space에 업로드하는방법

1. Git 설치하기 : [https://git-scm.com/](https://git-scm.com/)
2. 설치 완료 후 Git bash 열기
3. git bash 에서 환경설정 하기
    - Step 1 : 유저이름 설정
```plain text
git config --global user.name "your_name"
```
    - Step 2 : 유저 이메일 설정하기
```plain text
git config --global user.email "your_email"

```
→ Github가입시 사용한 이메일로 사용
    - Step 3 : 정보 확인하기
```plain text
git config --list
```
코드 업로드 방법 → VS code이용
    1. 초기화 → git 설치후 VS코드에 사용해봤는데 안됨; →C++컴파일러 추가
```plain text
git init

```
    2. <u>**추가할 파일 더하기**</u>
```plain text
git add .
git add test.cpp
```
. 은 전체를 선택할때 사용함. → 개별 추가시에는 파일이름으로 작성
        - 이렇게하면 내컴퓨터내 모든파일을 검사해서 너무 비효율적임 개별로 진행하기.
    3. 상태 확인 (선택사항)
```plain text
git status

```
    4. <u>**히스토리 만들기**</u>
```plain text
git commit -m "First commit"

```
        - 커밋 히스토리 작성
    5. Github repository랑 내 로컬 프로젝트랑 연결
```plain text
git remote add origin https://github.com/깃허브 주소

```
    6. 잘 연결됬는지 확인
```plain text
git remote -v

```
    7. <u>**Github로 올리기 → push**</u>
```plain text
git push origin master
```

**최초 작성환경 조성 후에는 2, 4, 7만 반복**

git hub 주소 변경시 사용명령어.
```javascript
git remote set-url origin <새로운GITURL>
```