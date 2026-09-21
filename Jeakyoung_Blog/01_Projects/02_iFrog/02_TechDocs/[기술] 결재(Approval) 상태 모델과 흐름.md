---
title: "[기술] 결재(Approval) 상태 모델과 흐름"
date: 2025-11-17
type: 기술문서
project: I-Frog
status: 진행중
category: Groupware
assignee:
  - 안재경
tags:
  - Approval
---

# [기술] 결재(Approval) 상태 모델과 흐름

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | `Controllers/Groupware/Approval/{ApprovalController,ApprovalService}.cs` |
| **적용 범위** | 결재 문서 조회/승인/반송/합의/댓글 |
| **관련 모듈** | FCM 발송([[[기술] FCM 토큰·메시지 이력 관리 구조]]) |

> 결재는 기존 뼈대 위에서 가장 많이 손본 도메인([[I-Frog 결재서비스 조회 파라미터 추가]] 등). 엔드포인트 5개와 그 밑에서 쓰는 상태 플래그를 정리.

## 🎯 배경 및 요구사항

결재 상태는 `MULDEC_FLAG`(결재구분: 1=결재권자·2=참조자·4=합의), `APP_FLAG`(처리구분: 1=승인·2=확인·3=반송), `LAST_CNFRMER_FLAG`(최종결재자 여부) 조합으로 갈린다. 실제 판정 로직(다음 결재자 찾기 등)은 SP 안에 있어서 여기선 C# 쪽에서 분기하는 부분만 보임.

## 🏗 설계 및 구현

### 엔드포인트

| 라우트 | 메서드 | 프로시저 | 내용 |
|:--|:--|:--|:--|
| `GetApprovalDetailList` | POST | `SP_WEB_FrmEA101_Window_01_LIST2` 외 4개 | 문서 상세 + 첨부/댓글/합의자 목록까지 한 번에 조회 |
| `GetApprovalAllList` | POST | `SP_WEB_FrmEA121_01_LIST` 외 3개 | 결재함 목록(대시보드 포함) |
| `CheckOpenTime` | POST | `SP_WEB_STORE_FUNCTION_ChkOpenTime` | 문서 열람 시간 등록 |
| `ConfirmApproval` | POST | `SP_WEB_STORE_FUNCTION_ChkAnswer_IUD`/`_IUD2` | 승인/확인/합의/반송 처리 |
| `PostAnswer` | POST | `SP_WEB_FrmEA101_Window_04_IUD` + `SP_WEB_STORE_MAX_01` | 댓글 작성 (작성 후 상세를 다시 조회해서 반환) |

### `ConfirmApproval`의 분기

```
APP_FLAG=1, MULDEC_FLAG=4        → "합의"      → ChkAnswer_IUD   (division: agreement)
APP_FLAG=1, LAST_CNFRMER_FLAG=1  → "최종승인"  → ChkAnswer_IUD   (division: confirm)
APP_FLAG=1 (그 외)               → "승인"      → ChkAnswer_IUD   (division: approve)
APP_FLAG=2                       → "확인"      → ChkAnswer_IUD   (division: validation)
APP_FLAG=3                       → "반송"      → ChkAnswer_IUD2  (division: reject)
```

각 분기마다 `ANSWER_GBN_NAME`/`ANSWER_CNT`(예: `"ⓜ[승인 하였습니다.]"`)를 코드에서 직접 만들어서 댓글처럼 같이 저장한다 — 사용자가 입력하는 게 아니라 시스템이 자동 생성하는 코멘트.

### 처리 후 FCM 발송 (실패해도 결재 자체는 성공 처리)

```csharp
try
{
    var regRequest = new FcmSendRequest { notiGbn = "1", exeId = ..., detailDivision = sDetailDivision, companyCode = "000001", ... };
    await _firebaseMessagingService.SendMessageAsync(regRequest);
}
catch (Exception ex)
{
    _logger.LogError(ex, "FCM 메시지 발송 서비스 미지원 업체");
}
```

FCM 발송은 별도 try/catch로 감싸져 있어서, FCM이 실패해도(로그 메시지를 보면 애초에 "업체별 미지원"을 전제로 짠 것으로 보임 — [[[기술] Ticker 전략 패턴(ITickerStrategy) 설계]]의 `FcmDbg`/`FcmSyn` 참고) **결재 처리 자체(SP 커밋)는 그대로 성공**한다.

> [!note] `companyCode = "000001"` 하드코딩
> `ConfirmApproval`뿐 아니라 `WorkStatusService.GetWorkProgress`의 `FACTORY_CODE`도 `"000001"`로 고정돼 있음. 여러 회사를 지원하는 멀티테넌시 구조인데, 정작 이런 값은 `TickerContext`/요청 파라미터가 아니라 상수로 박아둔 곳이 군데군데 있다 — 회사가 늘어나면 하나씩 걸릴 수 있는 지점.

## ✅ 검증

- [ ] `companyCode`/`FACTORY_CODE` 하드코딩 지점 전수 조사 (멀티테넌시 확장 시 리스크)
- [ ] FCM 발송 실패 시 사용자에게 알림이 전혀 안 가는 걸 인지하고 있는지 (조용히 로그만 남음)

## 🔗 참고

- [[I-Frog 결재서비스 조회 파라미터 추가]]
- [[I-Frog 결제함 문서 FCM기능 추가]] - SP_TGI001_01_LIST 기반의 다른 FCM 발송 경로(레거시/실험 버전으로 보임, `SendMessageAsync`와는 별개)
- [[[기술] FCM 토큰·메시지 이력 관리 구조]]
