---
title: I-Frog FCM 서버 세팅
date: 2026-06-10
type: 작업
project: I-Frog
status: 완료
priority: 보통
assignee: []
tags: []
created: 2026-06-10T14:28:00
---

# I-Frog FCM 서버 세팅

## 1. 개요

| 항목 | 내용 |
|------|------|
| 요청자 |  |
| 요청일 | 2026-06-10 |
| 대상 시스템 |  |
| 관련 화면·프로그램 |  |

## 2. 현상 및 원인

## 3. 조치 내용

ㅇ 사내 firebase 계정

- 계정 삭제 처리 ( 민감 정보 ) 26.08.31

ㅇ firebase 구성

ifrog ( android, ios, webapp )

ㅇ firebase 서버세팅

1. “dotnet add package FirebaseAdmin” 사용 firebase 관련 패키지를 프로젝트가 존재하는 

[ ex) starmap.service.csproj ] 경로에서 터미널을 열고 설치


![[image 186.png]]

2. firebase 접속 후 → (webapp)프로젝트 설정 → 서비스 계정에서 비공개키 설정 → 프로젝트 디렉토리 에서 keys파일 생성 → 해당 디렉토리에 맞게 저장 →  이후 사용자 계정 권한 관리 진입

![[image 187.png]]

3. 서비스 계정내 키값이 json형태로 나온 비공개키 값과 일치하는지 확인하고 해당 계정에 대한 iam 권한 부여 

![[image 188.png]]

4. 역활내 fcm api 관리자 → 메시징 권한 관리 해당 역활이 부여되지 않을경우 정상적으로 연결해도 연결 

거부됨.

```c#
// Firebase 초기화
if (FirebaseApp.DefaultInstance == null)
{
    FirebaseApp.Create(new AppOptions()
    {
        Credential = GoogleCredential.FromFile(Path.Combine(builder.Environment.ContentRootPath, "Keys/firebase-admin.json"))
    });
}
//Firebase 의존성 주입
builder.Services.AddScoped<FirebaseMessagingService>();
```

5. 이후 Program.cs 내에서 builder 생성자 바로 아래에 FireBase 의존성 주입

```c#
using FirebaseAdmin.Messaging;

namespace F1Soft.Starmap.Service.Services.Firebase
{
    public class FirebaseMessagingService
    {
        public async Task<string> SendNotificationAsync(string token, string title, string body)
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

            string result = await FirebaseMessaging.DefaultInstance.SendAsync(message);

            return result; // messageId 반환
        }
    }
}

```

```c#
using Microsoft.AspNetCore.Mvc;
using F1Soft.Starmap.Service.Services.Firebase;

namespace F1Soft.Starmap.Service.Controllers.Notification
{
    [ApiController]
    [Route("api/fcm")]
    public class FcmController : ControllerBase
    {
        private readonly FirebaseMessagingService _messagingService;

        public FcmController(FirebaseMessagingService messagingService)
        {
            _messagingService = messagingService;
        }

        [HttpPost("send")]
        public async Task<IActionResult> Send([FromBody] FcmRequest request)
        {
            var result = await _messagingService.SendNotificationAsync(
                request.Token,
                request.Title,
                request.Body
            );

            return Ok(new { messageId = result });
        }
    }

    public class FcmRequest
    {
        public string Token { get; set; }
        public string Title { get; set; }
        public string Body { get; set; }
    }
}

```

6. service, controller 생성후 테스트 진행



→ 테스트 결과 tocken 값이 없어 정상 진행되진 않으나 firebase내 FCM message Create 호출 성공

## 4. 검증 및 결과

## 5. 참고
