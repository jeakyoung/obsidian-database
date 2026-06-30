---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:29:00
담당자: []
---
```c#
"<span style=\"font-size:14px;\">총무팀 최성호 입니다.<br />\n<br />\n아이폰에서 ATC 전자결재 어플이 배포되어 알려드립니다.<br />\n<br />\n<br />\n검색&nbsp; : ifrog<br />\n<br />\n서버주소 :&nbsp; http://218.38.64.99<br />\n<br />\n포트 :&nbsp; 5500<br />\n<br />\n<br />\n아이디 : 사번<br />\n비번 : 사번<br />\n<br />\n<br />\n--------------------------------------------------<br />\n<br />\n1. 안드로이드에서는 메일 및 전자결재 첨부 문서가 다운로드 가능해졌습니다.<br />\n<br />\n2. 아이폰에서도 3일후 업데이트 될 예정입니다.<br />\n<br />\n<br />\n이상입니다.</span>"
```

→ 기존 칼럼에서 넘겨주는 정보들 { COMMENT } → 해당 값에서 태그를 분류해서 빼주는 작업이 필요

```c#
"총무팀 최성호 입니다.
\n
\n아이폰에서 ATC 전자결재 어플이 배포되어 알려드립니다.
\n
\n
\n검색  : ifrog
\n
\n서버주소 :  http://218.38.64.99
\n
\n포트 :  5500
\n
\n
\n아이디 : 사번
\n비번 : 사번
\n
\n
\n--------------------------------------------------
\n
\n1. 안드로이드에서는 메일 및 전자결재 첨부 문서가 다운로드 가능해졌습니다.
\n
\n2. 아이폰에서도 3일후 업데이트 될 예정입니다.
\n
\n
\n이상입니다."
```

→ 원하는 출력결과

→ \N 태그도 지워주는 과정이 필요 → JS에서 읽을게 아님

```c#
using System.Text.RegularExpressions;
using System.Web;

public string HtmlToPlainText(string html)
{
    if (string.IsNullOrEmpty(html))
        return string.Empty;

    // HTML 인코딩 해제
    string decoded = HttpUtility.HtmlDecode(html);

    // <br> 등을 개행으로 변환
    decoded = decoded
        .Replace("<br>", "\n")
        .Replace("<br/>", "\n")
        .Replace("<br />", "\n");

    // HTML 태그 제거
    string noTag = Regex.Replace(decoded, "<.*?>", string.Empty);

    // HTML 특수문자 &nbsp; 치환
    noTag = noTag.Replace("&nbsp;", " ");

    return noTag.Trim();
}

```

→ 해당 방식과 같이 정규식을 써서 지워줄 수 있음.

```json
"TITLE": "6월 대청소 실시의 건. (청소담당구역 변경)",
          "EMPNM": "최성호",
          "EMPLOYEE_NO": "060212",
          "WRITE_DATE": "202106291402",
          "VALID_DATE": "20210629",
          "SHEET_NO": "",
          "POPUP_VIEW": "0",
          "COL_SEQ": 2,
          "HIGHLIGHT": "0",
          "NUMBER": 20,
          "DOCU_CNT": 0,
          "VIEW_CNT": 52,
          "ME_VIEW_FLAG": 0,
          "COMMENT":
```

## 

ㅇ 조치 후 추가 개선 필요

![[image 171.png]]

→ JS 태그는 다 삭제했지만 html 태그내에 base64형식 이미지를 src 링크로 그대로 다 넣어버린 부분이 존재

![[image 172.png]]

→ SP내 공지사항 리스트 파라미터가 TODATE가 시작일 FROMDATE가 종료일로 꼬여있음

→ 백엔드 코드에서 억지로 수정해서 반대로 넣어주고 있지만 웹단 확인 후 프로시저 수정 필요

![[image 173.png]]

→ 해당부내에 COMMENT 칼럼은 댓글이아님 CONT에 해당되는 값을 담아주는중 (html요소 그대로)

불러오는데는 문제 X
