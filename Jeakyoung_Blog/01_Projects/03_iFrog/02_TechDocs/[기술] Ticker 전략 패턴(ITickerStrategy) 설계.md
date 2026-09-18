---
title: "[기술] Ticker 전략 패턴(ITickerStrategy) 설계"
date: 2026-03-05
type: 기술문서
project: I-Frog
status: 진행중
category: 멀티테넌시
assignee:
  - 안재경
tags:
  - Strategy Pattern
  - DI
---

# [기술] Ticker 전략 패턴(ITickerStrategy) 설계

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | `Strategies/ITickerStrategy.cs`, `Controllers/Auth/Strategy/*`, `Services/FirebaseService/Strategy/*` |
| **적용 범위** | 회사(Ticker)별로 로직이 갈라지는 지점 |
| **관련 모듈** | `LoginAtc`, `LoginSyn`, `FcmDbg`, `FcmSyn` |

> 회사마다 조금씩 다른 처리(로그인 시 FCM 토큰 저장 여부, FCM 발송 조건 등)가 `if (ticker == "ATC")` 식으로 여기저기 흩어지는 걸 막으려고, 제네릭 전략 인터페이스 하나로 묶어봄.

## 🎯 배경 및 요구사항

멀티테넌시 커넥션 구조([[I-Frog 보안코드 기반 멀티테넌시 DB 커넥션 구현|관련 작업]])를 넣고 나니, 이번엔 "DB는 같은 구조인데 회사별로 비즈니스 로직이 미묘하게 다른" 지점들이 문제였음. 예를 들어 ATC는 로그인 시 FCM 토큰을 같이 받아야 하는데 다른 회사는 아님.

## 🏗 설계 및 구현

```csharp
public interface ITickerStrategy<TRequest>
{
    string Ticker { get; }
    void Apply(Dictionary<string, object> parameters, TRequest request);
    void PostProcess(DataTable dt) { }
}
```

- `Ticker`로 자기가 어떤 회사 전략인지 표시
- `Apply`로 프로시저에 넘길 파라미터를 회사별로 조정
- `PostProcess`는 기본 구현이 비어있는 훅(옵션) — 결과 DataTable을 후처리해야 하는 회사가 있으면 오버라이드

### 현재 적용된 곳

| 도메인 | 전략 클래스 | 등록 (`Program.cs`) |
|:--|:--|:--|
| 로그인 | `LoginAtc : ITickerStrategy<AuthRequest>`, `LoginSyn : ITickerStrategy<AuthResponse>` | `AddScoped<ITickerStrategy<AuthRequest>, LoginAtc>()` 등 |
| FCM 토큰 등록 | `FcmDbg`, `FcmSyn : ITickerStrategy<RegTokenRequest>` | 동일 |

> [!note] 제네릭 타입이 통일돼 있지 않음
> `LoginAtc`는 `ITickerStrategy<AuthRequest>`인데 `LoginSyn`은 `ITickerStrategy<AuthResponse>`로 등록돼 있음. 같은 "로그인 전략"인데 요청/응답 타입이 갈려서 DI에서 하나의 리스트로 주입받아 `Ticker`로 골라 쓰는 구조는 아니고, 타입 자체로 분기되는 형태. 나중에 전략을 더 추가할 때 이 비대칭이 헷갈릴 수 있음.

### Notice에도 시도했다가 걷어낸 이력

`f02d066`에서 `Groupware/Notice`에도 `GetNoticeAtc`/`GetNoticeSgy` 전략을 넣었었는데, 이후(`bc683d3`)에 다시 제거됨. 공지사항 쪽은 회사별 분기가 이 패턴을 쓸 만큼 복잡하지 않았던 것으로 보임 — Notice에 이 패턴 다시 쓸지 말지는 아직 결정 안 된 상태.

## ✅ 검증

- [ ] `LoginAtc`/`LoginSyn` 제네릭 타입 통일 여부 검토
- [ ] 전략 클래스가 3개 이상으로 늘어나면 `IEnumerable<ITickerStrategy<T>>` 주입 + `Ticker`로 필터링하는 방식으로 리팩터링할지 결정

## 🔗 참고

- 커밋: `f02d066`(Notice 최초 적용), `4e22bbc`(Auth/FCM으로 확장, Notice는 이후 제거)
- [[I-Frog Ticker 전략 패턴 도입 (Auth·FCM)]]
