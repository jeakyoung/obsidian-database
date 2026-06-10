---
base: "[[Work Flow.base]]"
할당: []
상태: 진행 중
프로젝트: []
---
# 1. ATC 서버 이관 ( 03.13 ~16 )

## MSSQL 상 이관 대상

- ATC TABLE
    - TGI001
    - TGI002
    - TGI003

- ATC PROCEDURE
    - SP_TGI001_01_LIST
    - SP_TGI001_01_IUD
    - SP_TGI001_01_PATH ( 보류 발송대상 경로탐색을 위해 TEA132 참조중 )
    - SP_TGI002_01_IUD
    - SP_TGI002_01_LIST  (수정 발송자명 SELECT를 위해 TIN114 참조중 필요한 칼럼인지 재확인 필요 )
    - SP_TGI003_01_IUD
    - SP_TGI003_01_LIST

---

## PostgreSQL 상에 이관한 내용

*소문자로 이관함 PG 상에서 대문자 인식을 위해서는 쌍 따옴표 처리가 필요한데 혼동이 올 여지가 많음

- PG TABLE - 이관 완료
    - tgi001
    - tgi002
    - tgi003

- PG Functions - 이관 완료
    - tgi001_01_list
    - tgi001_01_iud
    - tgi002_01_list
    - tgi002_01_iud
    - tgi003_01_list
    - tgi003_01_iud

- PG Service API


`SaveTokenAsync`  → 토큰정보 저장 API → 이관완료


`GetNotificationAsync`  → 발송 내용 열람 리스트 → 이관완료

`FcmPassivity`  → FCM 메뉴얼 발송 API → 이관완료

`SendMessageAsync` → FCM 자동 발송 API → 진행중

→ 테스트 미시행 서비스 ( 테스트케이스 필요 제작후 시행 )

File FTP 서비스 → 커넥션은 있으나 테스트케이스 필요

→오류 발생 서비스

/Emp/GetEmpList ( 500 error 사원카드 커넥션 확인 필요할듯 )

→ ATC 내부 이관 후 정상 서비스

FCM 전체

로그인 로직 전체

Notice 서비스 전체

Setting 서비스 전체

BOARD 서비스 전체

Approval 서비스 전체

→ 결제라인 0000 → 221712 → 060212 ( 202603160001 )

### ㅇ ATC 잔업 → ATC FTP 테스팅, 유효한 FTP URL 확인

→ 테스트 확인 및 배포완료 / 운영, 개발, DB ( 26.03.16 )

## ** ATC 데이터 이관 마감 기한 → 03/18

---

# 2. 송연 서버 이관 ( 03.17 ~ )

→ 송연 테스트 완료 서비스

Auth 서비스 전체

Approval 서비스 전체

Notice 서비스 전체

Board 서비스 전체 ( 정상 작동하나 사용중인 데이터 없음 )

Setting 서비스 전체 ( DB 호출부를 통합 서버로 이관 )

Emp 서비스 전체


`**eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYnZlZXIzaDUzNW5uM24zNW55bnk1dW1iYnQiLCJqdGkiOiJjZTljMWFiZi05YzQ0LTRhMTYtYTI4Zi1mM2U3YWU0NGRlM2IiLCJpYXQiOiIxNzczNzA3NTA3IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZWlkZW50aWZpZXIiOiIwMDAwIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6IjAwMDAiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9lbWFpbGFkZHJlc3MiOiIwMDAwQGF0Yy1rci5jb20iLCJleHAiOjE3ODE0ODM1MDcsImlzcyI6IkV4YW1wbGVJc3N1ZXIiLCJhdWQiOiJFeGFtcGxlQXVkaWVuY2UifQ.egh4T_z9j8VWVQ3Y-nikFbJ1z8_eEEYJjksZppbMxnc**`

---

# 3. 동방 서버 이관 ( 03.17 ~ )

4000 0011

2000 0101

DBG

→ approval, board, auth, calender, emp, notice, setting 정상

{
"muldecFlag": "1",
"lastCnfrmerFlag": "1",
"lastOwnerFlag": "0",
"eaExeId": "202603170001",
"gbnCode": 1,
"exeSeq": 5,
"orderSeq": 5,
"optionName": "반송",
"appFlag": "3",
"eabusNo": "001",
"employeeNo": "25047"
}

---

# 4. 스케줄링 ( 03.18 ~ )

```java
try {
            ZonedDateTime nowKST = ZonedDateTime.now(KOREA_ZONE);
            DayOfWeek week = nowKST.getDayOfWeek();

        if (week != DayOfWeek.MONDAY) {
            System.out.println("\n[알림] " + nowKST.format(formatter) + "[Task Skip] 월요일이 아니므로 작업 스킵");
            return;
        }
```

→ 해당 구분처럼 스케줄링 주기가 자바 클래스에서 시행되고 있음 ( 하드코딩 되어있는 상황 )

** 주기 관리를 효율적으로 진행하기 위해서는 주기를 클래스에서 들고 있는 것이 아니어야 함 매번 주기 수정마다 요구 사항이 생김

** 클래스의 역활을 단순히 호출했을 때 원하는 작업을 시행하기만 할 수 있게 수정하고 DB단이든 관리 페이지든 주기 관리 책임을 다른 쪽으로 넘기는 작업이 필요함.

** UI → 작업프로시저 생성 → 프로시저로 클래스 호출 → 기능 수행 클래스

```java
INSERT INTO tgi000 VALUES
('DBG','Dev','MSSQL','Data Source=[REDACTED];Initial Catalog=[REDACTED];User Id=erpUser;Password=[removed marker deleted];TrustServerCertificate=True;Encrypt=True;','1',NOW(),NOW()),
('DBG','Dev','FTP','ftp://REDACTED_DOMAIN/','1',NOW(),NOW()),
('DBG','Dev','IMAGE','http://REDACTED_DOMAIN:7070/userImage/','1',NOW(),NOW()),
('DBG','Dev','EMP_CARD','http://REDACTED_DOMAIN/htmlreport/report/HR/WHR100/WHR101_01_REPORT.jsp?','1',NOW(),NOW());
```

```java
INSERT INTO tgi000 VALUES
('DBG','Stg','MSSQL','Data Source=[REDACTED];Initial Catalog=[REDACTED];User Id=sa;Password=;TrustServerCertificate=True;Encrypt=True;','1',NOW(),NOW()),
('DBG','Stg','FTP','ftp://REDACTED_DOMAIN/','1',NOW(),NOW()),
('DBG','Stg','IMAGE','http://REDACTED_DOMAIN:7070/userImage/','1',NOW(),NOW()),
	('DBG','Stg','EMP_CARD','http://REDACTED_DOMAIN/htmlreport/report/HR/WHR100/WHR101_01_REPORT.jsp?','1',NOW(),NOW());
```

```java
INSERT INTO tgi000 VALUES
('DBG','Prd','MSSQL','Data Source=[REDACTED];Initial Catalog=[REDACTED];User Id=sa;Password=;TrustServerCertificate=True;Encrypt=True;','Y',NOW(),NOW()),
('DBG','Prd','FTP','ftp://REDACTED_DOMAIN/','Y',NOW(),NOW()),
('DBG','Prd','IMAGE','http://REDACTED_DOMAIN:7070/userImage/','Y',NOW(),NOW()),
('DBG','Prd','EMP_CARD','http://REDACTED_DOMAIN/htmlreport/report/HR/WHR100/WHR101_01_REPORT.jsp?','Y',NOW(),NOW());
```