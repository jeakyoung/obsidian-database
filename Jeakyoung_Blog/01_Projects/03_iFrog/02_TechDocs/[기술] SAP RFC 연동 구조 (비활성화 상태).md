---
title: "[기술] SAP RFC 연동 구조 (비활성화 상태)"
date: 2025-11-17
type: 기술문서
project: I-Frog
status: 보류
category: 외부연동
assignee: []
tags:
  - SAP
  - RFC
---

# [기술] SAP RFC 연동 구조 (비활성화 상태)

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | `Controllers/Interface/Sap/SapRFCController.cs`, `Controllers/Interface/Models/SapRFC.cs` |
| **적용 범위** | SAP 인터페이스 |
| **관련 모듈** | `SapNwRfc` 라이브러리 |

> `SapRFCController`가 통째로 주석처리돼있어서 현재는 빌드에도 안 들어감. 코드 자체는 SAP RFC(P040) 호출 구조를 갖추고 있음 — 언제/왜 꺼졌는지는 기록에 없어서 확인 필요.

## 🎯 배경 및 요구사항

SAP ZDPSF_* RFC 모듈을 .NET에서 호출하기 위한 인터페이스. `SapNwRfc` NuGet 패키지(`ISapPooledConnection`)로 커넥션 풀을 관리하는 구조.

## 🏗 설계 및 구현

### 요청 → RFC 파라미터 매핑

```
List<SapRFCRequest> (RFCName + Dictionary<string,object> Parameters)
  → RFCName == "P030"일 때만 처리
  → Reflection으로 SapRFC_P040Item의 프로퍼티에 Parameters 값을 하나씩 바인딩
    (string / int / decimal 타입만 처리)
  → ISapPooledConnection.InvokeFunction<SapRFCResult>("ZDPSF_" + rfcID, ...) 호출
```

- SAP 쪽 구조체 필드는 `[SapName("...")]` 어트리뷰트로 C# 프로퍼티에 매핑 (`SapRFC_P040`, `SapRFC_P040Item`, `SapRFCResult`)
- 결과는 `RETCD`/`RETMG` (성공/실패 코드+메시지) 형태로 통일

> [!warning] 확장성이 없는 구조
> `rfcID.Equals("P030")` 하나만 하드코딩돼 있어서, RFC 종류가 늘어나면 이 if/else 블록이 계속 늘어나는 구조. 실제로 쓰게 된다면 RFC ID별 매핑 테이블이나 전략 패턴으로 바꾸는 게 나을 듯.

## ✅ 검증

- [ ] 언제, 왜 비활성화됐는지 확인 (연동 중단? SAP 서버 미가동? 다른 방식으로 대체?)
- [ ] 다시 쓸 계획이 있다면 `SapNwRfc` 패키지 버전/커넥션 설정값 최신 상태인지 확인

## 🔗 참고

- 최초 도입: `33f00ce`(2025-11-17), 이후 별도 수정 이력 없음
