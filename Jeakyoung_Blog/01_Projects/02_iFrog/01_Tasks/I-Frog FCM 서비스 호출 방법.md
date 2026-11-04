---
title: I-Frog FCM 서비스 호출 방법
date: 2026-06-10
type: 작업
project: I-Frog
status: 완료
priority: 보통
assignee: []
tags: []
created: 2026-06-10T14:28:00
---

# I-Frog FCM 서비스 호출 방법

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-06-10 |
| **대상 시스템** | — |
| **관련 화면·프로그램** | — |

## 🔍 현상 및 원인

## 🔧 조치 내용

### ㅇ 서비스 호출 END_POINT - ( /api/Fcm/FcmSendMsg )

- 요청 파라미터

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

notiGbn → 게시판 고유 코드 ( 1 : 기안함 )

companyCode → 회사 코유 코드 ( 추후 회사 별 코드 분리 후 명세 예정 )

senderCode → gUserId

exeId → 결재 문서 번호

exeSeq → 결재 순번

detailDivision → FCM 호출 분기 설정 {

1. validation = ( 확인 )
2. agreement = ( 합의 )
3. confirm = ( 결재완료 )
4. approve = ( 승인 )
5. reject = ( 반려 )

}


### ㅇ FCM 발송 서비스 사용 테이블

TGI001 (토큰 정보 저장 부), TGI002 (발송 내역 저장 부)

### ㅇ 서비스내 프로시저 실행 순서

#### SP_TGI001_01_PATH - 분기를 통한 FCM 발송 대상 사번 찾기

#### **↓**

#### SP_TGI001_01_LIST - FCM 사번으로 토큰 찾아오기 ( 발송은 토큰으로 서비스에서 )

#### **↓**

#### 발송 서비스 시행 ( 백단에서 )

#### **↓**

#### SP_TGI002_01_IUD - 발송한 메시지 로그 저장


( 별도 추가 서비스 )

#### SP_TGI001_01_IUD - 로그인 동작시 FCM 토큰 생성부

#### SP_TGI002_01_LIST - 추후 FCM 알림 발송정보 조회 ( 사용자용 )

## ✅ 검증 및 결과

## 🔗 참고
