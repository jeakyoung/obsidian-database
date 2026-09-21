---
title: "[기술] JWT 인증 및 AutoLogin 구조"
date: 2025-11-17
type: 기술문서
project: I-Frog
status: 진행중
category: Auth
assignee: []
tags:
  - JWT
  - Auth
---

# [기술] JWT 인증 및 AutoLogin 구조

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | `Controllers/Auth/AuthController.cs`, `Services/TokenService.cs`, `Controllers/Auth/Models/UserManager.cs` |
| **적용 범위** | 로그인, 자동 로그인, JWT 발급/검증 |
| **관련 모듈** | `SP_WEB_LOGIN`(로그인 프로시저, 이 저장소엔 소스 없음) |

> Login/AutoLogin/JWT 발급-검증 흐름을 코드 기준으로 정리. 몇 군데 눈에 띄는 이상한 부분이 있어서 있는 그대로 적어둠 — 의도한 동작인지 버그인지는 확인 필요.

## 🎯 배경 및 요구사항

- 로그인은 `USER_ID`/`USER_PW`를 `SP_WEB_LOGIN`에 넘겨서 서버(SP)에서 검증 — 비밀번호 비교 로직 자체는 SP 안에 있어서 이 저장소 코드로는 안 보임
- 로그인 성공 시 90일짜리 JWT 발급, 이후 요청은 `[Authorize]` + 이 토큰으로 인증

## 🏗 설계 및 구현

### 로그인 흐름

```
POST /api/Auth/Login (AuthRequest: userID, userPassword, deviceType, osInfo, token)
  → UserManager.GetAppUserAsync → SP_WEB_LOGIN(USER_ID, USER_PW, IP_INFO)
  → 로그인 성공 시 TokenService.CreateToken → JWT(90일) 발급
  → request.Token(FCM 토큰)이 있으면 IEnumerable<ITickerStrategy<AuthRequest>>에서
    현재 Ticker와 일치하는 전략(Apply)을 찾아 파라미터 조정 후 FirebaseMessagingService.SaveTokenAsync 호출
```

### AutoLogin의 실제 동작

```
POST /api/Auth/AutoLogin (Authorization: Bearer {token})
  → ValidateJwtToken(token)  // ValidateLifetime = true
      └ 유효하지 않으면(서명 불일치 *또는* 만료) 401
  → TokenService.DecodeToken(token)  // 여기도 ValidateLifetime = true
  → 디코딩된 UserId로 AuthRequest 재구성, UserPassword = "f1soft@6" (하드코딩)
  → Authenticate(authRequest) 재호출 → SP_WEB_LOGIN 다시 태움
```

> [!warning] "자동 로그인"인데 만료된 토큰은 못 받는다
> `ValidateJwtToken`과 `TokenService.DecodeToken` 둘 다 `ValidateLifetime = true`로 검증한다. 즉 토큰이 **만료되면 AutoLogin도 그냥 401**이다. 이름은 AutoLogin/자동로그인이지만, 지금 코드로는 "아직 유효한 토큰으로 세션을 다시 만드는 것"에 가깝고 "만료된 토큰으로 재로그인"은 안 된다.

> [!warning] 비밀번호가 하드코딩돼 있음
> `authRequest.UserPassword = "f1soft@6";` — 토큰에서 복원한 사용자로 재로그인할 때 실제 비밀번호 대신 고정 문자열을 넣는다. XML 문서 주석의 샘플 로그인도 `userID: "0000"`, `userPassword: ""`으로 되어 있는 걸 보면 테스트 계정 비밀번호를 그대로 박아둔 것으로 보인다. `SP_WEB_LOGIN`이 이 값을 그대로 비교한다면, **"f1soft@6"가 실제 비밀번호인 계정만 AutoLogin이 성공**하는 구조라 일반 사용자에게는 동작하지 않을 가능성이 있다. SP 내부 로직을 볼 수 없어서 단정은 못 하지만, 소스에 평문 비밀번호가 박혀있는 것 자체가 검토 대상.

### JWT 생성/검증 구현상 비효율

`TokenService`의 `CreateJwtToken`/`CreateClaims`/`CreateSigningCredentials`/`DecodeToken`, `AuthController.ValidateJwtToken` 전부 필요할 때마다

```csharp
new ConfigurationBuilder().AddJsonFile("appsettings.json").Build().GetSection("JwtTokenSettings")["..."]
```

식으로 **매번 appsettings.json을 새로 읽어서 파싱**한다. DI로 이미 `IConfiguration`을 받을 수 있는데 안 쓰고 있음 — 토큰 하나 만들 때마다 파일 I/O가 여러 번 도는 구조.

## ✅ 검증

- [ ] `SP_WEB_LOGIN`이 `USER_PW = "f1soft@6"`을 실제로 어떻게 처리하는지 확인 (특정 계정만 통과? 전체 계정 공통 비밀번호?)
- [ ] AutoLogin을 "만료된 토큰으로도 재로그인" 용도로 쓸 계획이면 `ValidateLifetime = false`로 디코딩하는 경로 별도 필요
- [ ] `ConfigurationBuilder` 반복 생성을 `IConfiguration` DI 주입으로 교체할지 결정

## 🔗 참고

- 최초 도입: `33f00ce`(2025-11-17)
- [[[기술] Ticker 전략 패턴(ITickerStrategy) 설계]]
