---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:28:00
담당자: []
---
## ㅇ ATC → 파라미터가 없어서 오류가 발생하는 경우에 대해 빈 값 처리 

## ㅇ 입력 값 수정부

![[image 191.png]]

`SP_WEB_FrmBP602_01_03_IUD` → CONFIRM_FLAG, SMS_FLAG, IUD 항목에 대해 빈 값 처리

→ ATC에만 빈 값 처리 완 → 송연 적용 미 진행

![[image 192.png]]

ㅇ ResultList를 만들 때 오류가 발생하는 지점인 request6에 대한 호출을 임시 주석 처리

→ 해당 프로시저가 ATC DB내에 존재하지 않음

→ 단 해당부는 프로시저를 만들면 주석 해제하고 기존 async를 사용해야 함


## ㅇ 출력 값 수정부

![[image 193.png]]

→ BoardService → 서비스 내 Columns를 강제 제거 / 가공하는 부분 주석 처리 후 테스트 진행 시 결제 문서

 관련 조회 기능 전체 정상 동작

→ 단 백엔드 코드 통합시 해당 방식으로 해결 불가능 → ATC 프로시저 내에 해당 두 column을 빈값으로라도 

넘겨서 타 업체와 동일하게 삭제시켜줘야함.


```c#
foreach (DataRow row in filteredTable.Rows)
{
    string employeeNo = row["EMPLOYEE_NO"]?.ToString()?.Trim() ?? string.Empty;
    string empImageGubun = row["EMP_IMAGE_GUBUN"].ToString() ?? string.Empty;
    string imageFtpUrl = _envService.GetImageUrl();
    string empCardUrl = _envService.GetEmpCardUrl();

    // 현재 시간을 밀리초 단위로 Unix Timestamp 변환

    if (empImageGubun == "1")
    {
        row["USER_IMAGE_URL"] = $"{imageFtpUrl}/{employeeNo}?{timestamp}";
        // ftpURL 이후 / 추가
    }
    else
    {
        row["USER_IMAGE_URL"] = $"{imageFtpUrl}0000?{timestamp}";
    }

    if (authFlag)
    {
        row["CARD_URL"] = $"{empCardUrl}" +
                          $"FACTORY_CODE={sFactoryCode}" +
                          $"&EMPLOYEE_NO={employeeNo}" +
                          $"&IMGGBN={empImageGubun}" +
                          $"&DATEMSEC={timestamp}" +
                          $"&FTPURL={imageFtpUrl}" +
                          $"&OPMAN_CODE={employeeNo}";
    }
    else
    {
        row["CARD_URL"] = string.Empty; // 권한이 없으면 빈 값
    }

}
```


ㅇ 조치 전


`**"USER_IMAGE_URL": "http://REDACTED_IP:7070/wf_ftp_134-81-52265/image/userImage000322?1764808897431",**`

→ 기존 URL에서 ftp 주소 뒤에 / 가 추가되지 않음

ㅇ 조치 후

`**"USER_IMAGE_URL": "http://REDACTED_IP:7070/wf_ftp_134-81-52265/image/userImage/000322?1764808897431",**`


## ㅇ [SP_WEB_FrmEA101_Window_04_IUD]

해당 프로시저에서 요구하는 파라미터 @TOP_VIEW_FLAG 에 대해 서비스상 값을 보내주는 부분이 존재하지 않음. 동방, 송연에는 존재하지도 않는 파라미터 값 → 동방, 송연, ATC에 모두 빈값 처리를 진행할지?

아니면 ATC에서 해당 파라미터를 지울지? → 테이블내 저장되고있는 값도 존재하지 않음.

→ [SP_WEB_FrmEA101_Window_04_LIST] 해당 프로시저에서 칼럼으로 쓰고있음
