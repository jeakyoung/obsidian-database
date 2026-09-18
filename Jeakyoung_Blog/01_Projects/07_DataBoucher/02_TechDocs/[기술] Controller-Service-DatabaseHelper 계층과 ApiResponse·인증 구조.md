---
title: Controller-Service-DatabaseHelper 계층과 ApiResponse·인증 구조
date: 2026-09-18
type: 기술문서
project: 데이터바우처
status: 완료
category: 아키텍처
assignee:
  - 안재경
tags: []
---

# Controller-Service-DatabaseHelper 계층과 ApiResponse·인증 구조

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | F1Soft.Starmap.Service (foodlink-service 백엔드) |
| **적용 범위** | 아키텍처 · 레이어링 · 인증 |
| **관련 모듈** | `Controllers/*`, `Services/*`, `SQLServerHelper`, `ApiResponse<T>`, `AuthController`, `TokenService` |

> `Controller → Service → *DatabaseHelper → 저장 프로시저(SP_*)` 4단 구조 + `ApiResponse<T>` 봉투 + JWT/SECURITY_CODE 이중 보안.

## 🎯 배경 및 요구사항

컨트롤러에 로직이 섞이면 회사·환경별 분기(SECURITY_CODE)와 비즈니스 로직(SP 호출)이 뒤엉켜 유지보수가 어려워진다. 컨트롤러는 얇게 유지하고, 실제 로직은 대부분 SQL Server 저장 프로시저로 두어 C# 쪽은 얇은 오케스트레이션/매핑 계층으로만 동작하게 한다.

## 🏗 설계 및 구현

### 구조

```
Controller (Controllers/<Area>/)
  - 모델 검증, 서비스 메서드 1회 호출, ApiResponse<T>로 래핑, 예외 시 로깅 + 500
Service (Services/<Area>/, I*Service + impl)
  - 비즈니스 로직 보유, 호출마다 using var helper = new SQLServerHelper(...)
  - DbProcedureRequest로 저장 프로시저(SP_*) 이름+파라미터 지정
IDatabaseHelper 구현체 (SQLServerHelper / PostgreSQLHelper / OracleHelper)
  - 트랜잭션 열고 CallProcedureAsync/ExecuteSqlCommandAsync 실행
  - DataReader → DataTable 변환
  - DbException 발생 시 롤백, 예외를 던지지 않고 DbResult.ErrorMessage 로 반환
```

- 새 영역은 `Controllers/<Area>/`, `Services/<Area>/I*Service`+impl, `Models/<Area>/*Request.cs`+`*Response.cs` 구조를 그대로 따른다.
- 다단계 쓰기가 다른 서비스도 건드릴 때(예: `InputSaveService`가 임베디드 이미지 업로드 때문에 `IImageService`를 호출)는 `System.Transactions.TransactionScope`로 전체를 감싸되, 서브 단계는 **순차 실행**한다(MSDTC 승격을 피하려고 `Task.WhenAll` 안 씀).

### 응답 봉투: ApiResponse\<T\>

```csharp
public class ApiResponse<T>
{
    public bool Result { get; set; }
    public List<ApiResultItem<T>>? ResultList { get; set; }
    public string? ErrorMessage { get; set; }

    public static ApiResponse<T> Success(T data, string name = "", string? division = null, int returnValue = 1) => ...
    public static ApiResponse<T> Fail(string errorMessage) => ...
}
```

컨트롤러는 `ApiResponse<T>.Success(...)`/`Fail(...)`만 쓰고 raw 객체를 직접 만들지 않는다. `Program.cs`의 전역 예외 핸들러와 `TickerMiddleware`의 에러 응답은 MVC 모델 바인딩 밖에서 도니까, 같은 모양(camelCase)을 수동 `JsonSerializer`로 흉내 낸다 — 실제 타입을 공유하지 않으므로 필드를 바꿀 땐 두 군데(클래스 + 미들웨어의 익명 객체)를 같이 고쳐야 한다.

### 인증: JWT + SECURITY_CODE 이중 구조

| 메커니즘 | 범위 | 비고 |
|:--|:--|:--|
| JWT `[Authorize]` | 개별 액션 단위 | 상당수 `#if !DEBUG`로 감싸져 있어 **Debug 빌드에서는 인증이 사실상 우회됨** — 인증 동작 검증은 Release/Staging 빌드로 해야 함 |
| `SECURITY_CODE` 헤더 | 파이프라인 전체 | [[01_Projects/07_DataBoucher/02_TechDocs/[기술] SECURITY_CODE 기반 멀티테넌시 구조 (TickerMiddleware)]] 참고 |

- `AuthController`가 `SP_WEB_LOGIN`(→ `UserService.GetAppUserAsync`)으로 토큰 발급.
- `TokenService`/`ITokenService`가 생성/검증/디코드를 담당. 서명은 유효하지만 **만료된** 토큰도 자동로그인/리프레시 흐름에서 디코드해 허용한다(`AuthController.AutoLogin` 주석 참고) — 만료만으로 바로 reject하지 않는 설계임을 놓치기 쉽다.
- 엔드포인트 접근 가능 여부를 볼 때 이 두 메커니즘을 **항상 같이** 따져야 한다: SECURITY_CODE가 없으면 컨트롤러 진입 자체가 안 되고, JWT `[Authorize]`는 Debug 빌드에서 빠질 수 있다.

## ✅ 검증

- [x] `Controllers/Search/SearchListController.cs` 등에서 컨트롤러가 검증 + 서비스 호출 + `ApiResponse` 래핑 외 로직을 갖지 않는지 확인
- [x] `SQLServerHelper` 사용 시 `using var helper = new SQLServerHelper(_connectionString, _logger)` 패턴 준수 여부 확인
- [ ] Release/Staging 빌드로 `[Authorize]` 우회 없는지 별도 검증 필요 (Debug 빌드 검증은 무효)

## 🔗 참고

- `Common/Models/ApiResponse.cs`, `Common/Database/`, `Services/Auth/TokenService.cs`, `Controllers/Auth/AuthController.cs`
- `foodlink-service/API.md` — `ApiResponse`/`DbResult` 상태코드 규약 원문
- [[01_Projects/07_DataBoucher/02_TechDocs/[기술] SECURITY_CODE 기반 멀티테넌시 구조 (TickerMiddleware)]]
