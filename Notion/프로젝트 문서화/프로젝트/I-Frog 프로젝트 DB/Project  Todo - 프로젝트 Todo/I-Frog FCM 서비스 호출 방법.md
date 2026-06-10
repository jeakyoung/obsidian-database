---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:28:00
담당자: []
---
## ㅇ 서비스 호출 END_POINT - ( /api/Fcm/FcmSendMsg )

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


## ㅇ FCM 발송 서비스 사용 테이블

TGI001 (토큰 정보 저장 부), TGI002 (발송 내역 저장 부)

## ㅇ 서비스내 프로시저 실행 순서

### SP_TGI001_01_PATH - 분기를 통한 FCM 발송 대상 사번 찾기

### **↓**

### SP_TGI001_01_LIST - FCM 사번으로 토큰 찾아오기 ( 발송은 토큰으로 서비스에서 )

### **↓**

### 발송 서비스 시행 ( 백단에서 )

### **↓**

### SP_TGI002_01_IUD - 발송한 메시지 로그 저장


( 별도 추가 서비스 )

### SP_TGI001_01_IUD - 로그인 동작시 FCM 토큰 생성부

### SP_TGI002_01_LIST - 추후 FCM 알림 발송정보 조회 ( 사용자용 )
