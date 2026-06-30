---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:28:00
담당자: []
---
## ㅇ 구성정보

토큰관리 테이블 → TGI001 → 토큰을 FCM 에 저장

CLI → TOKEN → APP INSTALL할때 발급 → 첫로그인시 DB에 저장

단순알림보낸리스트 테이블 → TGI002 → 이력을 저장

로그인 → CREATE, 같은정보가 있을경우 UPDATE → 상시체크 DB TOKEN <> 보낸점이 다를시에

문서작성 동작시 결제권자로 등록된 사람들, 참조자로 등록된 사람들

→ 구분자 EXE_TIME( OPMAN_TIME ), ARRIVAL_TIME(문서 작성시간), APP_FLAG(확인, 승인, 반송)

→ 반송시에 다음사람한테 넘기지 않고 → 작성자에게 RETURN + FCM 메시지 발송

→ 전부 열람해서 넘어가면 확인기능이 활성화됨

CREATE 할때 TOKEN, EMP_CODE, COMPANY_CODE, DEVICE_INFO



## ㅇ 테이블 정보

TGI001 -> FCM TOKEN TABLE
TGI002 -> Notification TABLE

## ㅇ 메시지 발송 요청변수

```json
{
  "token": "",
  "title": "FCM testing",
  "body" : "FCM test for me"
}
```

## ㅇ 테이블명 수정사항 

 TGI001  -- UserFCMTockens
 TGI002 -- notifications


[https://seungwoolog.tistory.com/88](https://seungwoolog.tistory.com/88)


## → 작업 진행상황

CRU 기능 에 대한 예제 백엔드 코드 작성 완료, 

이후 프로시저 수정 후 테스팅 필요

## → 필요 요구 사항

테이블내 모든 데이터에 대한 저장이 필요

-  TGI001 → 로그인시 FCM 토큰과 함께 사용자 FCM 정보를 갱신하는 부분
- TGI002 → FCM 메시지 발송시 호출하여 개인 토큰정보를 보내줌과 동시에 로그를 저장해서 남겨야함
              → 추가적으로 토큰 정보가 받아온 토큰정보와 일치하는지 체크
- FCM 메시지로 저장된 Title, Body를 보내는것이 아님 → title, body를 받아서 발송하고 테이블에 이력을 저장

근데이걸 저장할때 다시 찾아서 RECEIVE, SEN DATE를 업데이트 시킬 방법이 없음 → 기준이 불명확 

회사코드 사원코드로 저장하는 방식인데 한명의 사원이 여러 메시지를 한번에 보내면 다시 테이블을 참조해서 몇번째 문자메시지가 저사람이 읽은 메시지인지 찾을 기준점이 없음. ( MSG_CODE 같은게 필요할듯? )

수신자 정보를 기록한다고 달라질 점은 없음. 테이블구조 재설계 필요

## ㅇ Service

```c#
using F1Soft.Starmap.Service.Controllers.Database.Models;
using F1Soft.Starmap.Service.Controllers.Notification.Models;
using F1Soft.Starmap.Service.Helper;
using F1Soft.Starmap.Service.Services.EnvService;
using FirebaseAdmin.Messaging;
using NuGet.Common;

namespace F1Soft.Starmap.Service.Services.FirebaseService
{
    /// <summary>
    /// FCM 메시지 발송, 저장 서비스
    /// </summary>
    public class FirebaseMessagingService 
    {
        private readonly IEnvService _envService;
        private readonly string _connectionString;
        private readonly ILogger<FirebaseMessagingService> _logger;

        /// <summary>
        /// FCM 서비스
        /// </summary>
        /// <param name="envService"></param>
        /// <param name="logger"></param>
        public FirebaseMessagingService(
                IEnvService envService,
                ILogger<FirebaseMessagingService> logger)
        {
            _envService = envService;
            _connectionString = envService.GetConnectionString();
            _logger = logger;
        }

        /// <summary>
        /// FCM 메시지 송신 로그 생성
        /// </summary>
        /// <param name="userId"></param>
        /// <param name="token"></param>
        /// <param name="title"></param>
        /// <param name="body"></param>
        /// <returns></returns>
        public async Task<bool> SaveTokenAsync(string userId, string token, string title, string body)
        {
            using (var helper = new SQLServerHelper(_connectionString, _logger))
            {
                var req = new DbProcedureRequest
                {
                    ProcedureName = "SP_TGI002_01_IUD",
                    Division = "save",
                    Parameters = new Dictionary<string, object>
                {
                    {"UserId", userId},
                    {"Token", token},
                    {"Title", title},
                    {"Body", body}
                }
                };

                var result = await helper.CallProcedureAsync(new List<DbProcedureRequest>() { req });
                return result.Result;
            }
        }

        /// <summary>
        /// FCM 메시지 발송
        /// </summary>
        /// <param name = "userId" ></param >
        /// <param name = "token" ></param >
        /// <returns ></returns >
        public async Task<string> SendMessageAsync(string token, string userId)
        {
            using (var helper = new SQLServerHelper(_connectionString, _logger))
            {
                var req = new DbProcedureRequest
                {
                    ProcedureName = "SP_TGI001_01_LIST",
                    Division = "get",
                    Parameters = new Dictionary<string, object>
                {
                    {"UserId", userId},
                    {"Token", token }
                }
                };

                var result = await helper.CallProcedureAsync(new List<DbProcedureRequest>() { req });

                var dt = result.ResultList.FirstOrDefault()?.DataTable;
                if (dt == null)
                    throw new Exception("no result from dt");

                string title = dt.Columns["Title"]?.ToString();
                string body = dt.Columns["Body"]?.ToString();

                var message = new Message
                {
                    Token = token,
                    Notification = new Notification
                    {
                        Title = title,
                        Body = body
                    }
                };

                return await FirebaseMessaging.DefaultInstance.SendAsync(message);
            }
        }
    }
}

```

## ㅇ Controller

```c#
using F1Soft.Starmap.Service.Controllers.Notification.Models;
using F1Soft.Starmap.Service.Services.FirebaseService;
using Microsoft.AspNetCore.Mvc;
using NuGet.Common;

namespace F1Soft.Starmap.Service.Controllers.Notification
{
    /// <summary>
    /// FCM 메시지 컨트롤러
    /// </summary>
    [ApiController]
    [Route("api/Fcm")]
    public class FcmController : ControllerBase
    {
        private readonly FirebaseMessagingService _messagingService;

        /// <summary>
        /// FCM 메시지 서비스 생성
        /// </summary>
        /// <param name="messagingService"></param>
        public FcmController(FirebaseMessagingService messagingService)
        {
            _messagingService = messagingService;
        }

        /// <summary>
        /// FCM 메시지 설정 / 동작시 DB내 메시지 정보 저장
        /// </summary>
        /// <param name="request"></param>
        /// <returns></returns>
        /// <remarks>
        /// Sample request:
        /// 
        ///     {
        ///       "userID": "0000",
        ///       "token" : "",
        ///       "title" : "FCM testing",
        ///       "body"  : "FCM test for me"
        ///     }   
        /// </remarks>
        [HttpPost("FcmRegMsg")]
        public async Task<IActionResult> Reg([FromBody] FcmSendRequest request)
        {
            var result = await _messagingService.SaveTokenAsync(
                request.UserID,
                request.Token,
                request.Title,
                request.Body
            );

            return Ok(new { messageId = result });
        }

        /// <summary>
        /// FCM 메시지 발송 / 저장된 토큰 주소로 FCM 메시지 발송
        /// </summary>
        /// <param name="request"></param>
        /// <returns></returns>
        /// <remarks>
        /// Sample request:
        /// 
        ///     {
        ///       "userID": "0000",
        ///       "token" : ""
        ///     }     
        /// </remarks>
        [HttpPost("FcmSendMsg")]
        public async Task<IActionResult> Send([FromBody] FcmSendRequest request)
        {
            var result = await _messagingService.SendMessageAsync(
                request.UserID,
                request.Token
            );

            return Ok(new { messageId = result });
        }

    }  
}

```

## ㅇ Model

```c#
using System.ComponentModel.DataAnnotations;

namespace F1Soft.Starmap.Service.Controllers.Notification.Models
{
    /// <summary>
    /// FCM 메시지 발송 요청 모델
    /// </summary>
    public class FcmSendRequest
    {
        /// <summary>
        /// FCM 발송자
        /// </summary>
        public string? UserID { get; set; } = string.Empty;

        /// <summary>
        /// FCM 발송 토큰 주소
        /// </summary>
        public string? Token { get; set; } = string.Empty;

        /// <summary>
        /// FCM 메시지 발송 제목
        /// </summary>
        public string? Title { get; set; } = string.Empty;

        /// <summary>
        /// FCM 메시지 발송 내용
        /// </summary>
        public string? Body { get; set; } = string.Empty;
    }
}

```
