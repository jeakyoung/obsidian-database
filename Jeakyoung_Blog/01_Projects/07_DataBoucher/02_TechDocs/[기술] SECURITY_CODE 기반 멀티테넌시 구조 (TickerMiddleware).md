---
title: SECURITY_CODE 기반 멀티테넌시 구조 (TickerMiddleware)
date: 2026-09-18
type: 기술문서
project: 데이터바우처
status: 완료
category: 아키텍처
assignee:
  - 안재경
tags: []
---

# SECURITY_CODE 기반 멀티테넌시 구조 (TickerMiddleware)

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | F1Soft.Starmap.Service (foodlink-service 백엔드) |
| **적용 범위** | 아키텍처 · 멀티테넌시 |
| **관련 모듈** | `TickerMiddleware`, `SecurityCodeMapper`, `TickerContext`, `EnvService` |

> 요청 헤더 `SECURITY_CODE` 하나로 회사(Ticker)와 DB 환경(Env)을 동시에 결정해, 배포 하나로 여러 회사·여러 환경을 서빙한다.

## 🎯 배경 및 요구사항

foodlink-service(Starmap)는 DBG, SYN 등 여러 거래처(회사)의 모바일 백엔드를 하나의 배포로 서빙해야 한다. 회사별·환경별(Dev/Prd)로 별도 배포를 두지 않고, 요청 헤더만으로 어떤 회사의 어떤 환경 DB에 붙을지 런타임에 정하는 구조가 필요했다.

## 🏗 설계 및 구현

### 구조

```
Request (Header: SECURITY_CODE)
  └─ TickerMiddleware.InvokeAsync
       ├─ SecurityCodeMapper.GetTicker(code[0..2])  → "10"→DBG, "20"→SYN
       ├─ SecurityCodeMapper.GetEnv(code[2..4])     → "00"→Dev, "02"→Prd
       └─ TickerContext.Initialize(ticker) / EnvInitialize(env)   (요청당 1회, scoped)
            └─ Controller → Service → EnvService.GetConnectionString() 등
                 └─ appsettings.json: ConnSettings:{Ticker}:MsSql{Env}Connection
```

- `SECURITY_CODE`는 최소 4자리: 앞 2자리가 회사 코드, 다음 2자리가 환경 코드.
- `"40"→ATC` 매핑은 `SecurityCodeMapper.GetTicker`에 주석 처리된 상태로 남아 있다(비활성).
- 매핑에 실패하면 `UnauthorizedAccessException`을 던지고, 미들웨어가 이를 401로 변환한다.
- `TickerContext`는 요청 스코프 서비스라 `Initialize`/`EnvInitialize`를 두 번 호출하면 예외가 난다 — 미들웨어가 요청당 정확히 한 번만 호출하는 것을 전제로 한다.
- `EnvService`(`IEnvService`)는 `TickerContext.CurrentTicker`/`CurrentEnv`를 읽어 `ConnSettings:{Ticker}:MsSql{Env}Connection` 같은 config 키를 조합해 커넥션 문자열·FTP URL/자격증명·이미지 base URL을 뽑아낸다. 새 서비스가 DB/FTP에 접근해야 하면 `IConfiguration`을 직접 읽지 않고 반드시 `IEnvService`를 주입받아야 한다.

### 주요 로직

```csharp
// TickerMiddleware.InvokeAsync
var securityCode = context.Request.Headers["SECURITY_CODE"].FirstOrDefault();
if (string.IsNullOrEmpty(securityCode))
{
    await WriteErrorResponseAsync(context, 401, "헤더에 보안코드가 없습니다.");
    return;
}

var ticker = SecurityCodeMapper.GetTicker(securityCode); // chars 0-1
var env = SecurityCodeMapper.GetEnv(securityCode);       // chars 2-3

tickerContext.Initialize(ticker);
tickerContext.EnvInitialize(env);

await _next(context);
```

```csharp
// SecurityCodeMapper
public static string GetTicker(string securityCode) =>
    securityCode.Substring(0, 2) switch
    {
        "10" => "DBG",
        "20" => "SYN",
        // "40" => "ATC", // 비활성
        _ => throw new UnauthorizedAccessException("유효하지 않은 보안코드입니다.")
    };

public static string GetEnv(string securityCode) =>
    securityCode.Substring(2, 2) switch
    {
        "00" => "Dev",
        "02" => "Prd",
        _ => throw new UnauthorizedAccessException("유효하지 않은 보안코드입니다.")
    };
```

미들웨어의 에러 응답은 MVC 파이프라인을 타지 않으므로 `ApiResponse<T>`를 쓰지 못하고, 동일한 모양(`result`/`resultList`/`errorMessage`, camelCase)을 수동으로 `JsonSerializer.Serialize`해 응답한다.

> [!warning] 미들웨어 밖에서 IEnvService를 쓰면 터진다
> `TickerContext`는 정상 HTTP 요청 파이프라인을 거쳐야만 초기화된다. 백그라운드 작업이나 미들웨어를 거치지 않는 경로에서 `IEnvService`/DB 접근을 시도하면 `InvalidOperationException`이 발생한다. 새 기능을 배치/백그라운드로 뺄 때 이 전제를 깨지 않도록 주의.

## ✅ 검증

- [x] `SECURITY_CODE` 미전달 시 401 응답(raw JSON) 확인
- [x] `"10xx"`/`"20xx"` 조합이 각각 DBG/SYN + Dev/Prd 커넥션 문자열로 올바르게 매핑되는지 확인
- [ ] `"40"(ATC)` 활성화 필요 시 매핑 추가 및 `appsettings.json`의 `ConnSettings:ATC:*` 구성 여부 확인

> [!note] I-Frog 쪽 EnvService와 혼동 주의
> I-Frog 프로젝트도 같은 `F1Soft.Starmap.Service` 계열 코드베이스([[01_Projects/03_iFrog/02_TechDocs/[기술] 보안코드 기반 멀티테넌시 커넥션 구조]] 참고)지만, 그쪽은 `EnvService`가 appsettings.json 대신 **PostgreSQL `tgi000_01_list` 프로시저 + 정적 캐시**로 진화되어 있다. 이 저장소(foodlink-service/DataBoucher, `foodlink-service/F1Soft.Starmap.Service/Common/Env/EnvService.cs` 기준)는 여전히 `IConfiguration`으로 `appsettings.json`의 `ConnSettings:{Ticker}:*`를 직접 읽는 원래 방식이다 — 두 프로젝트가 같은 이름의 클래스를 다르게 구현하고 있으니 코드를 옮겨쓸 때 반드시 어느 저장소인지 확인할 것.

## 🔗 참고

- `Common/Env/TickerMiddleware.cs`, `Common/Env/SecurityCodeMapper.cs`, `Contexts/TickerContext.cs`, `Common/Env/EnvService.cs`
- [[01_Projects/07_DataBoucher/02_TechDocs/[기술] Controller-Service-DatabaseHelper 계층과 ApiResponse·인증 구조]]
- [[01_Projects/03_iFrog/02_TechDocs/[기술] 보안코드 기반 멀티테넌시 커넥션 구조]] — 같은 계열 코드베이스의 후속 진화 버전(참고용, 구현은 다름)
