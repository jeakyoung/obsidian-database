---
base: "[[Work Flow.base]]"
날짜: 2026-01-27
할당:
  - 안재경
상태: 완료
프로젝트:
  - "[[I-Frog 프로젝트 DB|I-Frog 프로젝트 DB]]"
---
## → Schedule 관리 예제 코드

```java
```

@Component
public class SchedulerTasks {

main() {
연락스케쥴러();
}

//// 스케쥴링 기능 (서버가 켜져있으면 계속 옵저빙 하지만 특정 동작이 원하는 시간은 설정시간)
    // 초 분 시 일 월 요일
    // 0 0 9 * * MON-FRI : 월~금 오전 9시 0분 0초
    @Scheduled(cron = "0 0 9 * * MON-FRI")
    public void 연락스케쥴러 () {
        // 실제 실행할 기능 함수
        Schedular("연락");
    }
    
    @Scheduled(cron = "0 0 8 * * MON-FRI")
    public void 기안스케쥴러 () {
        // 실제 실행할 기능 함수
        Schedular("기안");
    }
    
    SAFE_INVOICE //DB스케쥴러 전용
    SAFE_INVOICE_Notification //server 스케쥴러 전용 -> output: empList 

    
    private void Schedular(String type) {
        List<String> employeeIDList = await SP.SAFE_INVOICE(); //호출해서 돌리고 있음 
        FCM fcm = new FCM();
        await fcm.sendMessage(title: "업무 연락이 도착했습니다", 
         empList:employeeIDList, type: type );
         }
    
//common/fcm -> FCM -> sendMessage(String title, List<String>empList, type : "연락");
--- > 이 부분에 FCM이 제일 중요해짐 -> 공통화 



    	
}
```
```

---

## Target DB → [dbo].[SAFE_INVOICE_NOTICE]

→ 데이터 조회용 쿼리 작성

```sql
SELECT B.EA_TITLE, A.*  FROM TEA132 A
LEFT JOIN TEA131 B
ON	  A.EA_EXE_ID = B.EA_EXE_ID 
WHERE A.EABUS_NO NOT IN ('001', '004', '008', '031', '033')
```

- TEA132 → EABUS_NO → ( 001 = 기안, 008 = 연락, 031 = 근태, 004 회계, 033 = 이상발생? 연락확인?  )

---

## 연락알림 → TEA132 ( EABUS_NO : 008 )

![[image 214.png]]

→ 서버 스케쥴링 할떄 EXE_TIME 없는 EMPLOYEE_NO → LIST로 만들어서 JAVA 스캐쥴링으로 잡아주기

![[image 215.png]]

![[image 216.png]]

![[image 217.png]]

{
"eaExeId": "202601150014",
"eabusNo": "031",
"employeeNo": "16075",
"gbnCode": 1,
"exeSeq": 2
}

SP_WEB_STORE_FUNCTION_ChkAnswer_IUD4




{
"muldecFlag": "1",
"lastCnfrmerFlag": "1",
"lastOwnerFlag": "0",
"eaExeId": "202601150014",
"gbnCode": 1,
"exeSeq": 2,
"orderSeq": 2,
"optionName": "작성",
"appFlag": "1",
"eabusNo": "031",
"employeeNo": "16075"
}



`**eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYnZlZXIzaDUzNW5uM24zNW55bnk1dW1iYnQiLCJqdGkiOiI1MTRkYWVlNi1lYjhlLTQ0MjctYWQxMi1iZmFhMzc3NzAxODgiLCJpYXQiOiIxNzcyMDg3NTg3IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZWlkZW50aWZpZXIiOiIwMDAwIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6IjAwMDAiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9lbWFpbGFkZHJlc3MiOiIwMDAwQGRvbmdiYW5nZm9vZC5jb20iLCJleHAiOjE3Nzk4NjM1ODcsImlzcyI6IkV4YW1wbGVJc3N1ZXIiLCJhdWQiOiJFeGFtcGxlQXVkaWVuY2UifQ.BtoBSyPteUAZfVpMhzTkr8RKtjyBVgyu3jsKDVF_5LM**`

```c#
switch (sEabusNo) {

    case "001":
        request3 = new DbProcedureRequest
        {
            ProcedureName = "SP_WEB_FrmEA101_Window_02_LIST",
            Division = "sign",
            Parameters = new Dictionary<string, object> { { "EA_EXE_ID", sEaExeId } }
        };
    break;

    case "031":
    request3 = new DbProcedureRequest
    {
        ProcedureName = "SP_WEB_FrmEA131_01_LIST",
        Division = "sign",
        Parameters = new Dictionary<string, object> { { "EA_EXE_ID", sEaExeId } }
    };
    break;

default:
        return new { Message = "지원하지 않는 업무 번호입니다." };
}
```
