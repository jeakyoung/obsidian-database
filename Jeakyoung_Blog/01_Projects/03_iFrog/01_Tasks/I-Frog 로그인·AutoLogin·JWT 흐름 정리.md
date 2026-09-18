---
title: I-Frog 로그인·AutoLogin·JWT 흐름 정리
date: 2025-11-17
type: 작업
project: I-Frog
status: 진행중
priority: 높음
assignee:
  - 안재경
tags:
  - Auth
  - JWT
---

# I-Frog 로그인·AutoLogin·JWT 흐름 정리

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | — |
| **대상 시스템** | `Controllers/Auth`, `Services/TokenService` |
| **관련 화면·프로그램** | 로그인, 자동 로그인(토큰 갱신) |

> 로그인/AutoLogin/JWT 코드를 읽으면서 발견한 것들을 정리 — 실제로 고칠지는 확인 후 결정.

## 🔍 현상 및 원인

`AutoLogin`을 코드로 읽어보면 두 가지가 걸림:

1. `ValidateJwtToken`/`DecodeToken` 둘 다 `ValidateLifetime = true`라서, 토큰이 만료되면 AutoLogin도 그냥 401. "자동 로그인"이라는 이름과 달리 만료 전 토큰 재사용에 가까움.
2. AutoLogin 내부에서 `authRequest.UserPassword = "f1soft@6"`로 비밀번호를 하드코딩하고 `SP_WEB_LOGIN`을 다시 호출함. 이 값이 실제 비밀번호와 다른 계정이면 AutoLogin이 실패할 걸로 보임(SP 내부 로직은 안 보여서 단정은 못 함).

## 🔧 조치 내용

(아직 조치 안 함 — 확인 후 결정)

| 구분 | 대상 | 내용 |
|:--|:--|:--|
| 확인 필요 | `AutoLogin` | 만료된 토큰도 받아줄 계획이면 `ValidateLifetime = false`로 디코딩하는 별도 경로 필요 |
| 확인 필요 | `UserPassword = "f1soft@6"` | 왜 고정값을 쓰는지, 전체 계정에 적용 가능한 값인지 |
| 참고 | `TokenService`/`AuthController` | `ConfigurationBuilder`를 매번 새로 만들어 appsettings.json을 반복 파싱 — `IConfiguration` DI로 교체 여지 있음 |

## ✅ 검증 및 결과

- [ ] 실제 클라이언트(WEB/모바일)가 AutoLogin을 만료 토큰 갱신 용도로 쓰고 있는지 확인
- [ ] `f1soft@6`가 테스트 계정 전용인지, 여러 계정에 공통 적용되는 값인지 SP 쪽 확인

## 🔗 참고

- [[[기술] JWT 인증 및 AutoLogin 구조]]
- 최초 도입: `33f00ce`(2025-11-17)
