---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:29:00
우선순위: 높음
종료일: 2025-12-23
담당자:
  - 안재경
---
## ㅇ 요청

1. 특정 동작 (승인 확인 반송 등)이 발생
2. 다음 flag를 진행해야하는 사람의 EMPNO 를 가져옴
3. EMPNO를 통해 MGI001 에서 TOKEN 을 받아옴
4. 없을 경우 별도 동작 x 있을경우 token과 메세지를 파이어 베이스 서버에 던짐
5. MGI002에 저장

→ ConfirmApproval → 엔드포인트 접근시 EMPNO 가져오는 부분 → 어떤게 다음수신자인지 찾기

→ 다음수신자 EMPNO를 파라미터로 101 프로시저 호출 → 응답으로 토큰값만 가져오기

→ 최종 RS를 만들어서 토큰, 타이틀, 바디를 만들어서 SENDER 호출 (프로시저 한번더 거치지 않기) → SENDER 호출과 동시에 동일한 RS로 102_IUD 쿼리를 생성 → IUD동작 (LOG 생성)

TGI102테이블내 문서번호 필요 → 키는 EA_EXE_ID, EXE_SEQ 복합키로 생성 → 한 문서의 고유 키에 대해 열람한 순서대로 입력 SEQ 생성 → 여기에 로그 남기기

→ 이렇게 해야 IsRead 관리 가능 (이후 적립이 가능함) → IsRead 가 0인것들만 모아서 FCM 메시지 

재발송 가능 / 이렇게 안하면 이후 어디서 발송한 FCM 메시지인지 찾을 방법이 없음.

/*
GBN_CODE: 1. 결재 문서 , 2. 조치 통보

- 1 일 때 버튼 활성화 시켜야함
MULDEC_FLAG: 1. 결재권자, 2. 참조자 3.협의?? 4.합의
- 1 일 때 승인 2 일 때 확인
APP_FLAG: 1. 승인(결재), 2. 확인, 3. 반송
ARRIVAL_TIME: 나한테 도착한 시간 / 승인 활성화 기능 (EXE_TIME == null && ARRIVAL_TIME.isNotEmpty 일 때 승인 활성화)
*/

---

[[기안서 작성 상태값.xlsx]]

## ㅇ FCM 로직

- EXE_SEQ를 받아와서 ORDER_SEQ값이 같은 것 들을 가져온다
- 이후 MULDEC_FLAG값을 확인한다 <u>**1이면 A조건**</u>으로 <u>**4면 B조건**</u>으로


- ELSE IF (LAST_CNFRMER_FLAG == 1)인 경우 EXE_TIME이 있을때
    - 문서 번호내 ORDER_SEQ가 1인것을 찾아서  FCM 발송 → 종료

ㅇ 참조자 REFERENCE_FLAG → 1이나0으로 구분되어있음 0은 결제전, 1은 결제후

---

## ㅇ 조치사항

```sql
USE [iPlusERP_Test]
GO
/****** Object:  StoredProcedure [dbo].[SP_TGI001_01_LIST]    Script Date: 2025-12-23 오전 8:57:16 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
/*************************************************************************************
  0. 버전              	: SQL Server 2016
  1. 스토어드명        	: SP_TGI001_01_LIST
  2. 목적& 기능        	: FCM 조건 발송 및 저장 통합모듈
  3. 생성일자          	: 2025-12-19
  4. 생성자            	: 안재경
  5. 수정이력 
     1) 수정일자 : 
	    - 수정내역 : 
		- 수정자 : 		
  6. 인자              	: 
 10. 리턴값            	:  
 11. SP TEST 예제	:
(에) 가져와야할것 exe
 ******************************************************************************/

ALTER PROC [dbo].[SP_TGI001_01_LIST]
(
	@CompanyCode		 VARCHAR(10) = '',
	@EmployeeNum		 VARCHAR(10) = '',
	@AppFlag			 CHAR(1) = '',		-- 1:승인 / 2:확인 / 3:반송 / 4:합의 -> 2번은 FCM동작 불필요
	@MuldecFlag			 CHAR(1) = '',	    -- 1:결재 / 2:참조 / 4:합의
	@ExeSeq				 INT = 0,
	@LastCnfrmerFlag	 CHAR(1) = '',
	@LastOwnerFlag		 CHAR(1) = '',
	@exeId				 VARCHAR(30) = ''
)
AS
BEGIN
	DECLARE @CurrentOrderSeq INT;
	DECLARE @REFERENCE_VIEW_CHK CHAR(1);

	--DECLARE 
	--@CompanyCode		 VARCHAR(10) = '000001',
	--@EmployeeNum		 VARCHAR(10) = '0000',
	--@AppFlag			 CHAR(1) = '1',
	--@MuldecFlag			 CHAR(1) = '1',	 
	--@ExeSeq				 INT = 1,
	--@LastCnfrmerFlag	 CHAR(1) = '0',
	--@LastOwnerFlag		 CHAR(1) = '0',
	--@exeId			 VARCHAR(30) = '202103290003'

	SELECT TOP 1 
		@REFERENCE_VIEW_CHK = REFERENCER_VIEW_FLAG,
		@CurrentOrderSeq = ORDER_SEQ
	FROM TEA132
	WHERE EA_EXE_ID = @exeId
	AND EXE_SEQ = @ExeSeq;

SET NOCOUNT ON;
	/**
	결제 시행시 -> EXE_TIME이 전부다 있는경우에만 알림발송 (ELSE 문으로)
	**/
	IF(@MuldecFlag = '1' AND @AppFlag = '1' AND @LastCnfrmerFlag = '0')  
	BEGIN
		IF EXISTS (
			SELECT 1
			FROM TEA132
			WHERE EA_EXE_ID = @exeId
			AND ORDER_SEQ = @CurrentOrderSeq
			AND (EXE_TIME IS NULL OR EXE_TIME = '')
		)
		BEGIN
			RETURN;
		END
		ELSE
		BEGIN

			DECLARE @NextOrderSeq INT = @CurrentOrderSeq + 1;

			INSERT INTO TGI002(EA_EXE_ID, EXE_SEQ, CompanyCode, EmployeeNum, Title, Body, UserId, SentAt)
			SELECT 
				D.EA_EXE_ID,
				D.EXE_SEQ,
				@CompanyCode,
				D.EMPLOYEE_NO,
				'결재요청 알림',
				'다음 결재 순서가 도착했습니다.',
				0,
				GETDATE()
			FROM TEA132 D
			WHERE D.EA_EXE_ID = @exeId
			AND D.ORDER_SEQ = @NextOrderSeq;

			SELECT 
				T.Token,
				M.Title,
				M.Body
			FROM TGI001 T
			JOIN TGI002 M
				ON T.EmployeeNum = M.EmployeeNum
			WHERE M.EA_EXE_ID = @exeId
		END
	END

	/**
	합의 시행시 -> ORDER_SEQ가 같은것들 중 EXE_TIME이 전부다 있는것들만 세어서 다 있는경우에만 다음 FCM 발송
	**/
	IF(@MuldecFlag = '4' AND @AppFlag = '4')
	BEGIN
		DECLARE @Total INT, @NoTime INT;

		SELECT 
			@Total = COUNT(*),
			@NoTime = COUNT(CASE WHEN EXE_TIME IS NULL OR EXE_TIME = '' THEN 1 END)
		FROM TEA132
		WHERE EA_EXE_ID = @exeId
		AND ORDER_SEQ = @CurrentOrderSeq;

		IF(@NoTime = 1)
		BEGIN
			INSERT INTO TGI002(EA_EXE_ID, EXE_SEQ, CompanyCode, EmployeeNum, Title, Body, UserId, SentAt)
			SELECT 
				@exeId,
				@ExeSeq,
				@CompanyCode,
				@EmployeeNum,
				'합의 처리 알림',
				'합의자가 합의하였습니다.',
				0,
				GETDATE()
		END

		ELSE IF(@NoTime > 1 AND @NoTime < @Total)
		BEGIN
			RETURN;
		END


		ELSE IF(@NoTime = 0)
		BEGIN
			DECLARE @NextOrderSeq2 INT = @CurrentOrderSeq + 1;

			INSERT INTO TGI002(EA_EXE_ID, EXE_SEQ, CompanyCode, EmployeeNum, Title, Body, UserId, SentAt)
			SELECT 
				D.EA_EXE_ID,
				D.EXE_SEQ,
				@CompanyCode,
				D.EMPLOYEE_NO,
				'결재요청 알림',
				'다음 결재 순서가 도착했습니다.',
				0,
				GETDATE()
			FROM TEA132 D
			WHERE D.EA_EXE_ID = @exeId
			AND D.ORDER_SEQ = @NextOrderSeq2;

			SELECT 
				T.Token,
				M.Title,
				M.Body
			FROM TGI001 T
			LEFT JOIN TGI002 M
			ON T.EmployeeNum = M.EmployeeNum
			WHERE M.EA_EXE_ID = @exeId
		END
	END

	/**
	결재한 사람이 마지막 결재자인 경우 최종 승인 알림을 게시자에게 송부
	**/

	IF(@LastCnfrmerFlag = '1' AND @AppFlag = '1')
	BEGIN
		INSERT INTO TGI002(EA_EXE_ID, EXE_SEQ, CompanyCode, EmployeeNum, Title, Body, UserId, SentAt)
		SELECT 
			@exeId,
			@ExeSeq,
			@CompanyCode,
			A.EMPLOYEE_NO,
			'결재 완료: ' + EA_TITLE,
			'요청하신 '+EA_TITLE+' 문서가 최종 승인 완료되었습니다.',
			0,
			GETDATE()
		FROM TEA132 A
		LEFT JOIN TEA131 B
		ON A.EA_EXE_ID = B.EA_EXE_ID
		LEFT JOIN TIN114 C
		ON A.EMPLOYEE_NO = C.EMPLOYEE_NO
		WHERE A.EA_EXE_ID = @exeId
		AND ORDER_SEQ = 1;

		SELECT 
			T.Token,
			M.Title,
			M.Body
		FROM TGI001 T
		JOIN TGI002 M
			ON T.EmployeeNum = M.EmployeeNum
		WHERE M.EA_EXE_ID = @exeId
	END

	/**
	반송 요청이 들어왔을 경우 -> 반송메세지를 게시자에게 송부
	**/

	IF (@AppFlag = '3')
	BEGIN
		INSERT INTO TGI002(EA_EXE_ID, EXE_SEQ, CompanyCode, EmployeeNum, Title, Body, UserId, SentAt)
		SELECT
			@exeId,
			@ExeSeq,
			@CompanyCode,
			A.EMPLOYEE_NO,
			'결재 반송: '+B.EA_TITLE,
			C.BASE_NAME + '님에 의해 ' + B.EA_TITLE + '문서가 반려되었습니다.',
			0,
			GETDATE()
		FROM TEA132 A
		LEFT JOIN TEA131 B
		ON A.EA_EXE_ID = B.EA_EXE_ID
		LEFT JOIN TIN114 C
		ON A.EMPLOYEE_NO = C.EMPLOYEE_NO
		WHERE A.EA_EXE_ID = @exeId
		AND ORDER_SEQ = 1;
	END

	/**
	문서에서 참조자로 지정되어있는 경우 결재 문서 알림
	**/

	IF (@MuldecFlag = '2' AND @REFERENCE_VIEW_CHK = '0')
	BEGIN
		INSERT INTO TGI002(EA_EXE_ID, EXE_SEQ, CompanyCode, EmployeeNum, Title, Body, UserId, SentAt)
		SELECT
			@exeId,
			@ExeSeq,
			@CompanyCode,
			A.EMPLOYEE_NO,
			'새 결재 문서 등록',
			C.BASE_NAME+ '님의 '+B.EA_TITLE+'문서가 등록되었습니다. 참조하세요.',
			0,
			GETDATE()
		FROM TEA132 A
		LEFT JOIN TEA131 B
		ON A.EA_EXE_ID = B.EA_EXE_ID
		LEFT JOIN TIN114 C
		ON A.EMPLOYEE_NO = C.EMPLOYEE_NO
		WHERE A.EA_EXE_ID = @exeId
		AND ORDER_SEQ = 1;
	END
END

```

→ ( SP_TGI001_01_LIST )신규 프로시저 추가 / 조건에 대한 필터링을 미리 진행 후 TGI002에 메시지 적립

→ 추가적으로 적립시에 Title, body에 글의 제목이나 결재자의 이름과 같은 데이터를 select 같이담아줌

→ 적립과 동시에 Token, Title, Body를 Select해서 반환값으로 던져줌으로 FCM 서비스 재호출

```c#
/// <summary>
/// FCM 메시지 발송
/// </summary>
/// <param name = "CompanyCode" ></param>
/// <param name = "EmployeeNum" ></param>
/// <param name = "AppFlag" ></param>
/// <param name = "MuldecFlag" ></param>
/// <param name = "exeSeq" ></param>
/// <param name = "LastCnfrmerFlag" ></param>
/// <param name = "LastOwnerFlag" ></param>
/// <param name = "exeId" ></param>
/// <returns ></returns >
public async Task<object> SendMessageAsync(
    string CompanyCode,
    string EmployeeNum,
    string AppFlag,
    string MuldecFlag,
    int exeSeq,
    string LastCnfrmerFlag,
    string LastOwnerFlag,
    string exeId
)
{
    string sCompanyCode = CompanyCode ?? string.Empty;
    string sEmployeeNum = EmployeeNum ?? string.Empty;
    string sAppFlag = AppFlag ?? string.Empty;
    string sMuldecFlag = MuldecFlag ?? string.Empty;
    int iExeSeq = exeSeq;
    string sLastCnfrmerFlag = LastCnfrmerFlag ?? string.Empty;
    string sLastOwnerFlag = LastOwnerFlag ?? string.Empty;
    string sExeId = exeId ?? string.Empty;

    try
    {
        using (var helper = new SQLServerHelper(_connectionString, _logger))
        {
            var req = new DbProcedureRequest
            {
                ProcedureName = "SP_TGI001_01_LIST",
                Division = "fcm",
                Parameters = new Dictionary<string, object>
                {
                    {"CompanyCode", sCompanyCode},
                    {"EmployeeNum", sEmployeeNum},
                    {"AppFlag", sAppFlag},
                    {"MuldecFlag", sMuldecFlag},
                    {"ExeSeq", iExeSeq},
                    {"LastCnfrmerFlag", sLastCnfrmerFlag},
                    {"LastOwnerFlag", sLastOwnerFlag},
                    {"exeId", sExeId}
                }
            };

            var result = await helper.CallProcedureAsync(new List<DbProcedureRequest> { req });

            if (result.Result)
            {
                var resultItem = result.ResultList?.FirstOrDefault();
                DataTable? dt = resultItem?.DataTable;

                if (dt == null || dt.Rows.Count == 0)
                {
                    _logger.LogInformation("FCM 대상 데이터 없음");
                    return new { Message = "데이터가 없습니다." };
                }

                List<string> sendResults = new();

                foreach (DataRow row in dt.Rows)
                {
                    string token = row["Token"]?.ToString()?.Trim() ?? string.Empty;
                    string title = row["Title"]?.ToString()?.Trim() ?? string.Empty;
                    string body = row["Body"]?.ToString()?.Trim() ?? string.Empty;

                    if (string.IsNullOrEmpty(token))
                    {
                        _logger.LogWarning("토큰 없음, 발송 스킵");
                        continue;
                    }

                    try
                    {
                        var message = new Message
                        {
                            Token = token,
                            Notification = new Notification
                            {
                                Title = title,
                                Body = body
                            }
                        };

                        string msgId = await FirebaseMessaging.DefaultInstance.SendAsync(message);
                        sendResults.Add(msgId);
                    }
                    catch (Exception ex)
                    {
                        _logger.LogError(ex, $"FCM 발송 실패 (Token={token})");
                    }
                }

                if (sendResults.Count == 0)
                {
                    _logger.LogWarning("FCM 전송 결과 없음");
                    return new { Message = "FCM 전송 결과 없음" };
                }

                _logger.LogDebug("FCM 발송 완료");
                return JsonHelper.ConvertDbResultToJsonObject(result);
            }
            else
            {
                throw new Exception("실패");
            }
        }
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "FCM 메시지 처리 중 오류 발생");
        throw new Exception("실패");
    }
}
```

→ 호출되는 FCM 서비스 로직 →  결재 중에 받아오는 값들을 파라미터로 담아와서 검색조건으로 재활용

→ reuslt를 다시 받아와서 Token, Title, Body에 적재 → 세가지로 FCM 서비스 호출

---

## ㅇ결과화면

<!-- Column 1 -->
![[178a736a-0f4f-4428-86b3-aa6430cd6c64.png]]

<!-- Column 2 -->
![[image_(3).png]]


→ 테스트 결과 정상 발송 가능,  결재 처리 동작 시

결재 정보 저장 → FCM 서비스 로직 호출 → 테이블 내 FCM 로그 생성 → 반환 값으로 FCM메시징 서버 호출 → 사용자 알림 

순으로 동작이 진행되며 /ConfirmApproval 에 request 전달 시 위 과정이 전부다 동시 진행됨

---

## ㅇ 프로시저 명세

- SP_TGI001_01_LIST

| ㅇ Parameter | ㅇ Response |
| --- | --- |
| CompanyCode | Token |
| EmployeeNum | Title |
| AppFlag | Body |
| MuldecFlag |   |
| ExeSeq |   |
| LastCnfrmerFlag |   |
| LastOwnerFlag |   |
| exeId |   |

---

## ㅇ 프로시저명 수정작업

<!-- Column 1 -->
![[image 169.png]]

<!-- Column 2 -->
![[image 170.png]]

TGI001_01_IUD

@CompanyCode
@EmployeeNum
@UserID		
@DeviceType	
@OsInfo		
@Token

TGI001_01_LIST

@CompanyCode	
@EmployeeNum	
@AppFlag		
@MuldecFlag		
@ExeSeq			
@LastCnfrmerFlag
@LastOwnerFlag	
@exeId

TGI002_01_IUD

@EA_EXE_ID	
@EXE_SEQ		
@CompanyCode	
@EmployeeNum	
@TITLE		
@BODY		
@SenderCode

TGI002_01_LIST

@EmployeeNum