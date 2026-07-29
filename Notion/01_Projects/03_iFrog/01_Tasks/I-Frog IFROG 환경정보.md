---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 시작 전
생성 일시: 2026-06-10T14:28:00
담당자: []
---
동방이랑 송연 두군데 서비스 구현되어있음

→ 기본세팅, 프로시저 몇개

ATC와의 차이점

## ㅇ프로젝트 구조

CT → 파라미터를 받아오고 내놓기만함

엔드포인트로 서비스를 호출→ 반환하기전에 가공을 거치고 프로시저 호출 → 리턴

앞단 하나에 → 백단에서 분기 / 권한관리는 테이블을 통해 진행 / 사용자권한으로 확인


---

## ㅇ 프로세스

IIS (인터넷 정보 서비스) → 사이트를 통해 백단접근가능 

사이트 우클릭 → 웹사이트추가 → 사이트 이름 GroupwareTest → 경로로 지정되어있는 파일을 통해

→ d드라이브내 존재하는 백엔드 스토리지로 사이트를 오픈 → 사용안하는 포트를 찾아서 열기

→ 명령어를 통해 사용안하는 포트를 찾아서 열기 → ex)40110, 40112 → 포트를 같이 열어주어야함

→ 방화벽 → 고급설정 → 인바운드 allow 열어주기 포트는 같게 (TCP로)

(테스팅 방법 → 허용되어있는 포트 확인법 찾아보기)

40112

백엔드) 디렉터리 검색을 열어주어야함 → 열면 WEB.CONFIG가 열림 → 해당 파일을 수정해야한함

RELEASE로 빌드를 돌리면 로컬로 빌드파일이 생성됨 → CI/CD도 가능

→ 해당 빌드파일을 서버에 넣어주면 됨 → 개별 세팅

SWAGGER → 이용해서 문서화를 진행되어있음 (IP주소 + / + SWAGGER)

JSON으로 요청변수 넣어주면 결과값까지 다보여줌 AUTHCONTROLLER 내에 요청변수 예제 들어있음

MVC패턴으로 구성되어있음 CONTROLLER에서 서비스 호출만 구현되어있고

SERVICE에서 데이터 가공 → CONTROLLER 하나에 서비스하나

→ 전부 PARAMETER에 담아서 프로시저로 던지는 방식 가공이 많진않음

**오류 검출시 프로시저를 확인해야함 → 파라미터 갯수가 약간씩 맞지않는 경우가 생김


모바일 플랫폼

그룹웨어 → 업무연락작성, 결재문서 작성 (기안, 업무, 근태 연락 결재서류)

[ASP.NET](http://asp.net/) → 뒷단

FLUTTER → 앞단


---

ATC 서버정보를 통해 서버를 열고 프로젝트를 DB에 맞게 연결하기

→ APPSETTINGS.JSON

권한관리는 포트권한으로 하드코딩되어있음.

JWT-TOKEN

SWAGGER → 칼럼명을 한글로 변환할수있는지

→ JAVA에 찍힌 로그랑 프로시저내 실행결과를 비교 → 다른데이터가 있는지 확인

→ 새로 인터페이스를 하나 만들게 되면 아예 없는 값을 가져와야 할수도있음

→ 미리 요청 내용은 정해줌

문서 양식은 HTML형식으로 소스그대로 넘기는 형식임

→ 맞는 항목 안의 CONTROLLER내부 함수를 하나 임의추가 → 의존성주입 → 모델생성 →

ENDPOINT 지정해주고 → SERVICE에서 파라미터 정보 입력 호출 

SKIPDIVISIONS?

배포법 → 빌드를 돌리면 RELEASE내부에있는 모든 빌드파일을 열린 서버에 복사붙여넣기 해야함

159개 CI/CD 적용 가능하나 현재 정상동작X

형상관리는 GIT으로

빌드적용휴 서버 재시작하기

APP SETTING도 붙여넣기

테스트용 / 운영 나뉘어져있음

DEBUG

RELEASE

STAGING -

---

Git clone 위치

> ⚠️ Git 자격증명 정보는 보안상 제거되었습니다.
> 프로젝트 관리자에게 접근 정보를 요청하세요.

→ branch → lkh_org

— IDE는 vscode로 안됨 Visual Studio 받아서 진행하기

→ .net이랑 개발도구 확장정도만 받기

그룹 웨어 서비스 분류

AUTH - 인증, 로그인

APPROVAL - 결재 서류

BOARD - 게시판

CALENDAR - 캘린더

COMMON - 파일 전송 CT

EMP - 조직도 열람


GetApprovalDetailList (approval) - 500

SP_WEB_FUNCTION_GET_DISCUSSION_USER_LIST → 미존재

GetUssuesBoardList (board) - 500

SP_WEB_FrmBP601_01_LIST → column내 board_type이 미존재

GetBoardDetail → MarkAsReadBoard (board) - 500

SP_WEB_FrmBP602_01_03_IUD → service 파일 내 입력 파라미터에 CONFIRM_FLAG, SMS_FLAG 값을

받아오지도 않고 프로시저, 테이블내 저장부도 미존재

