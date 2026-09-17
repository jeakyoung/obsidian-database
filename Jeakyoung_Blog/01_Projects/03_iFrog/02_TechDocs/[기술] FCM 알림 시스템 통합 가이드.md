---
title: I-Frog FCM 알림 시스템 통합 가이드
date: 2026-06-11
type: 기술문서
project: I-Frog
status: 완료
category: 알림시스템
assignee: []
tags: []
---

# I-Frog FCM 알림 시스템 통합 가이드

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | I-Frog 모바일 백엔드 (`F1Soft.Starmap.Service`) |
| **적용 범위** | 알림시스템 |
| **관련 모듈** | `FirebaseMessagingService`, `TGI001`, `TGI002`, `TGI003` |


## 🎯 배경 및 요구사항

결재 문서의 상태가 바뀔 때 모바일 앱으로 푸시를 보낸다.
Android / iOS / WebApp 세 가지를 하나의 Firebase 프로젝트에서 처리한다.

## 🏗 설계 및 구현

### 1. 패키지 설치

`.csproj` 가 있는 경로에서 실행한다.

```bash
dotnet add package FirebaseAdmin
```

### 2. 서비스 계정 키 준비

1. Firebase 콘솔 → **프로젝트 설정 → 서비스 계정 → 비공개 키 생성**
2. 내려받은 JSON 을 프로젝트의 `Keys/` 디렉토리에 둔다 (`Keys/firebase-admin.json`)
3. 서비스 계정 화면의 키 값과 내려받은 JSON 의 키가 같은지 확인한다
4. 해당 계정에 IAM 권한을 준다

> [!warning] 권한이 없으면 연결이 거부된다
> IAM 역할에서 **FCM API 관리자 → 메시징 권한**이 부여되어 있어야 한다.
> 이 권한이 없으면 설정이 전부 맞아도 연결 거부로 떨어진다.
> 발송이 안 될 때 코드부터 보지 말고 여기를 먼저 확인한다.

> [!warning] 키 파일은 커밋하지 않는다
> `Keys/firebase-admin.json` 은 서비스 계정 비공개 키다.
> 저장소에 올라가지 않도록 하고, 노출되면 즉시 콘솔에서 키를 폐기한다.

### 3. 초기화 및 의존성 주입

`Program.cs` 에서 builder 생성 직후에 넣는다.

```csharp
// Firebase 초기화
if (FirebaseApp.DefaultInstance == null)
{
    FirebaseApp.Create(new AppOptions()
    {
        Credential = GoogleCredential.FromFile(
            Path.Combine(builder.Environment.ContentRootPath, "Keys/firebase-admin.json"))
    });
}

// Firebase 의존성 주입
builder.Services.AddScoped<FirebaseMessagingService>();
```

### 4. 발송 엔드포인트

```
POST /api/Fcm/FcmSendMsg
```

요청 본문:

```json
{
    "notiGbn": "1",
    "companyCode": "000001",
    "senderCode": "0000",
    "exeId": "202103290003",
    "exeSeq": 1,
    "detailDivision": "approve"
}
```

| 파라미터 | 의미 |
|:--|:--|
| `notiGbn` | 게시판 고유 코드 (`1` = 기안함) |
| `companyCode` | 회사 고유 코드 |
| `senderCode` | `gUserId` |
| `exeId` | 결재 문서 번호 |
| `exeSeq` | 결재 순번 |
| `detailDivision` | 호출 분기 |

`detailDivision` 값: `validation`(확인), `agreement`(합의), `confirm`(결재완료),
`approve`(승인), `reject`(반려)

### 5. 사용 테이블

| 테이블 | 용도 |
|:--|:--|
| `TGI001` | 토큰 정보 저장부 |
| `TGI002` | 발송 내역 저장부 |
| `TGI003` | 사용자별 알림 수신 설정 |

`TGI003` 은 `COMPANY_CODE` + `EMPLOYEE_NO` 가 키이고, 알림 종류별 수신 여부를 가진다.

| 컬럼 | 의미 |
|:--|:--|
| `APPROVAL_CHK_FLAG` | 결재 알림 |
| `BOARD_CHK_FLAG` | 게시 현황 알림 |
| `NOTI_CHK_FLAG` | 공지 알림 |
| `SCHEDULE_CHK_FLAG` | 일정 알림 |

**FCM 발송 여부는 `APPROVAL_CHK_FLAG` 로 판단한다.**

### 6. 발송 흐름

```
SP 호출 → 결과를 JSON 으로 담기 → API 로 전달 → FCM 발송 → TGI002 에 내역 기록
```

토큰은 ACCESS(만료 2주) / REFRESH 구조이며 REFRESH 는 헤더로 넘긴다.
업체별 교환코드로 도메인을 넘겨준다.

## ✅ 검증

- [ ] IAM 에 FCM 메시징 권한이 부여되어 있는지
- [ ] `Keys/firebase-admin.json` 이 저장소에 올라가지 않는지
- [ ] `TGI001` 에 디바이스 토큰이 정상 적재되는지
- [ ] `APPROVAL_CHK_FLAG = N` 인 사용자에게 발송되지 않는지
- [ ] `detailDivision` 5종이 각각 의도한 문구로 가는지
- [ ] 발송 후 `TGI002` 에 내역이 남는지

## 🔗 참고

- [[I-Frog FCM 서버 세팅]]
- [[I-Frog FCM 서비스 호출 방법]]
- [[I-Frog FCM 시나리오]]
- [[I-Frog TGI003 테이블 설계 명세]]
- [[I-Frog 결제함 문서 FCM기능 추가]]
