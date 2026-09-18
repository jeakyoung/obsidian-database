---
title: I-Frog 결재서비스 조회 파라미터 추가
date: 2026-05-22
type: 작업
project: I-Frog
status: 완료
priority: 보통
assignee:
  - 안재경
tags:
  - Groupware
  - Approval
---

# I-Frog 결재서비스 조회 파라미터 추가

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-05-22 |
| **대상 시스템** | F1Soft.Starmap.Service (`Controllers/Groupware/Approval`) |
| **관련 화면·프로그램** | 결재함 조회 API |

> 결재 목록 조회에서 작성자명·제목·문서번호·업무번호로 검색할 수 있도록, 이전에 주석으로만 남겨뒀던 파라미터를 실제로 연결.

## 🔍 현상 및 원인

`ApprovalRequest`에 `RegmanName`(등록자명), `EaTitle`(제목), `EaExeId`(실행 ID), `EabusNo`(업무 번호) 필드가 "추후 사용" 주석(`#region 추후 사용 할 수 있음`)으로만 존재했고, `ApprovalService.GetList`(추정)에서도 해당 값을 항상 빈 문자열로 고정해서 프로시저에 넘기고 있었다. 즉 API 스펙상 파라미터는 있어도 실제 조회 조건으로는 동작하지 않는 상태였다.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 모델 | `Models/ApprovalRequest.cs` | 주석 처리된 4개 필드(`RegmanName`, `EaTitle`, `EaExeId`, `EabusNo`)를 정식 프로퍼티로 전환 |
| 서비스 | `ApprovalService.cs` | `sRegmanName` 등 4개 변수를 하드코딩 빈 문자열 대신 `request.*` 값으로 바인딩 |
| 컨트롤러 | `ApprovalController.cs` | XML 문서 주석(Sample request)에 4개 파라미터 예시 추가 |

빈 값 처리(값이 없으면 `string.Empty`)는 그대로 유지되어 있어, 클라이언트가 값을 안 보내면 기존과 동일하게 동작한다.

## ✅ 검증 및 결과

- [ ] 프론트엔드에서 작성자명/제목/문서번호/업무번호 조회 조건 연동 확인 필요

## 🔗 참고

- 커밋: `9e213c2` Fix Ahn / 결재서비스 조회 파라미터추가
