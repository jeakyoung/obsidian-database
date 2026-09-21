---
title: IPACK 01.13 화상회의 회의록
date: 2026-01-13
type: 회의록
project: IPACK
status: 진행중
attendees: []
tags: []
created: 2026-06-10T14:29:00
---

# IPACK 01.13 화상회의 회의록

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **일시** | 2026-01-13 |
| **장소** | — |
| **참석자** | — |
| **안건** | — |

## 💬 논의 내용

### 회의 일시 01.13 15:06 ~ 16:00

### ㅇ 회의목적

기존 화면 오류 개선

### ㅇ 문제 사항

구매관리 → 재고관리 → 재고현황 (재고수량이 맞지 않음)

- 전산상 재고와 실제 재고가 맞지 않음 (세무회계 때문에 문제)
- 연말마다 ERP로 관리한 리스트로 감사를 받는데 안 맞아서 문제가 생김
- 기존은 이월, 당기입고, 당기출고, 당기재고로 되어있고
  - 입고량은 생산실적 → 포장작업장 내 데이터로
  - 출고량은 영업관리 → 출하현황으로 가져오는데
  - 저장된 데이터가 끌어온 데이터와 달라 수량차이가 많이 발생함
  - 이월된 내용부터 잘못되어 약간씩 틀어진 부분이 있었음
- 폐기처리화면 → 폐기처리된 수량만큼 재고현황에서 차감되지 않음 / 재고현황과 연동이 안 되어있음
  - 계정대체 등록으로 폐기를 진행했는데 재고현황에 반영이 안 됨
- 영업관리 → 재고조정 (정상)
- 완제품 재고현황과 수주번호를 매칭시켜야 함 (마지막으로 포장된 항목의 수주번호를 보여주세요)
- 재고조정 시 입고와 출고를 동시에 지정해서 반영할 수 없음
- 재고현황 페이지에서 완제품창고의 세부 창고위치를 보여주고 수기입력도 가능하게 해주세요 (품목별로 전부 세부 위치정보를 찾아와야 함)

### ㅇ 요구 사항

- 수동입력으로 재고량을 수정할 수 있도록 해주세요
- 수주번호도 같이 조회할 수 있게 해주세요
- 재고현황에서 재고조정란, 재고위치 추가
- 재고현황 툴바 이름 정정 요청 (당기입고량 → 당월입고량, 당기출고량 → 당월출고량, 당기재고량 → 현재재고량)
- 당월 입고량은 공정별생산수량의 정상수량과 같게, 당월 출하량은 출하현황과 같게
- 수식적용 점검 요청: 이월수량 + 당기입고량 - 당기출고량 ± 재고조정(수동입력값) = 현재재고
- 영업 → 수주등록 → 작업지시서에서 현재 재고수량이 표기될 수 있게 해주세요 (출력물, 완제품 수량을 끌고와서 특이사항 아래쪽에 출력)
- 생산관리 → 공정별제공현황(포장 전) → 수주가 마감된 사안도 여기서 뜨는 경우가 생김 (공정재고 폐기작업 관리에서 폐기처리를 해도 재고현황에서 나오는 상황)

#### 상단 요약

기본적으로는 정상수량을 가져오고, 재고현황에서 재고량을 조절할 수 있는 기능이 필요하다는 요청이었으나, 확인 결과 해당 기능은 이미 구현되어 있는 것으로 결론.

### ㅇ 조치 필요 사안 (진행 상황)

1. ~~완제품 재고현황과 수주번호를 매칭시켜야 함 (마지막으로 포장된 항목의 수주번호를 보여주세요)~~ — **완료.** 김부장 쿼리 수정 (품목계정, 수주처 사이에 컬럼으로 추가)
2. ~~재고조정 테이블 트리거 확인 필요 (로직을 두 번 타서 한 개 삭제했는데 두 개 삭제 처리됨)~~ — **완료.** 유과장 확인
3. ~~재고현황 페이지에서 완제품창고의 세부 창고위치를 보여주고 수기입력도 가능하게 해주세요 (품목별로 전부 세부 위치정보를 찾아와야 함)~~ — **완료.** `TCO403`에 `LOCATION_TXT` 컬럼 신설, 창고 컬럼 바로 뒤에 배치, 수기입력 가능하도록 조치 (담당: 나)
4. 영업 → 수주등록 → 작업지시서에서 현재 재고수량이 표기될 수 있게 해주세요 (완제품 수량을 끌고와서 출력·반영) — 담당 미정
5. 영업관리 → 출하반품처리 → 반품날짜 기준이 아닌 최초 출고일 기준으로 날짜계산 되도록 수정 — 담당 미정

### ㅇ 구현 메모

- `PROD_WAREHOUSE`에도 `LOCATION_TXT` 컬럼 추가
- `SP_TMA922_SAVE02` → 저장부 수정, 운영 반영 완료
- 재고현황 리스트 프로시저(센차 수정 포함): `SP_WMA621_01_LIST`, `SP_WMA621_02_LIST`
- 제품마스터 등록 프로시저·클래스 추가(센차 수정 포함): `jvWCO304_01_IUD.java` / `SP_WCO304_01_IUD`
- 포장 → 박스당수량, 단가 관련 논의 (상세 미기록)

![[image 96.png]]

### ㅇ 참고: 회사별 DB 커넥션 설정 스니펫

회의 중 공유된 멀티 테넌트(회사별) DB 접속 설정 구조 예시. 값은 이미 `[REDACTED]` 처리된 상태로 기록되어 있어 그대로 남김.

```json
"CompanyConnections": {
  "ATC": {
    "MsSqlDevConnection": "Data Source=[REDACTED];Initial Catalog=[REDACTED];",
    "MsSqlStgConnection": "Data Source=[REDACTED];Initial Catalog=[REDACTED];",
    "MsSqlPrdConnection": "Data Source=[REDACTED];Initial Catalog=[REDACTED];",

    "FtpDevUrl": "ftp://REDACTED_IP/",
    "FtpStgUrl": "ftp://REDACTED_IP/",
    "FtpPrdUrl": "ftp://REDACTED_IP/",

    "FtpDevUserImageUrl": "http://REDACTED_IP:7070/wf_ftp_134-81-52265/image/userImage"
  },

  "DONGBANG": {
    "MsSqlDevConnection": "Data Source=[REDACTED];Initial Catalog=[REDACTED];",
    "MsSqlStgConnection": "Data Source=[REDACTED];Initial Catalog=[REDACTED];",
    "MsSqlPrdConnection": "Data Source=[REDACTED];Initial Catalog=[REDACTED];"
  }
}
```

```c#
public class DevEnvService : IEnvService
{
    private readonly IConfiguration _configuration;
    private readonly IHttpContextAccessor _httpContext;

    public DevEnvService(
        IConfiguration configuration,
        IHttpContextAccessor httpContext)
    {
        _configuration = configuration;
        _httpContext = httpContext;
    }

    public string GetEnvironmentName()
    {
        return "Dev";
    }

    public string GetConnectionString()
    {
        string env = GetEnvironmentName(); // Dev
        string key = $"MsSql{env}Connection";

        // 1️⃣ ticker 기반 설정 먼저 조회
        string? ticker = _httpContext.HttpContext?.Items["TICKER"]?.ToString();

        if (!string.IsNullOrEmpty(ticker))
        {
            string? tickerConn =
                _configuration[$"CompanyConnections:{ticker}:{key}"];

            if (!string.IsNullOrEmpty(tickerConn))
                return tickerConn;
        }

        // 2️⃣ fallback → 기존 설정 그대로 사용
        return _configuration.GetConnectionString(key) ?? string.Empty;
    }

    public string GetFtpUrl()
    {
        string env = GetEnvironmentName();
        string key = $"Ftp{env}Url";
        string? ticker = _httpContext.HttpContext?.Items["TICKER"]?.ToString();

        if (!string.IsNullOrEmpty(ticker))
        {
            var value = _configuration[$"CompanyConnections:{ticker}:{key}"];
            if (!string.IsNullOrEmpty(value))
                return value;
        }

        return _configuration.GetConnectionString(key) ?? string.Empty;
    }

    public string GetImageUrl()
    {
        string env = GetEnvironmentName();
        string key = $"Ftp{env}UserImageUrl";
        string? ticker = _httpContext.HttpContext?.Items["TICKER"]?.ToString();

        if (!string.IsNullOrEmpty(ticker))
        {
            var value = _configuration[$"CompanyConnections:{ticker}:{key}"];
            if (!string.IsNullOrEmpty(value))
                return value;
        }

        return _configuration[$"ConnectionStrings:{key}"] ?? string.Empty;
    }
}
```

## ✅ 결정 사항

- 재고수량 불일치 문의는 재확인 결과 기능 자체는 정상 구현되어 있는 것으로 결론
- 완제품 재고현황-수주번호 매칭: 김부장 쿼리 수정 완료 (품목계정, 수주처 사이 컬럼 추가)
- 재고조정 테이블 트리거 중복 삭제 문제: 유과장 확인 완료
- 완제품창고 세부 위치 수기입력: `TCO403.LOCATION_TXT` 컬럼 신설로 처리 완료 (담당: 나)
- `SP_TMA922_SAVE02` 저장부 수정, 운영 반영 완료

## 🔜 후속 조치

- 수주등록 → 작업지시서 출력물에 현재 재고수량(완제품 수량) 표기 반영 — 담당 미정
- 출하반품처리 반품일 기준 날짜계산 로직을 최초 출고일 기준으로 수정 — 담당 미정
- 위 두 건은 금주 내 해결 후 익주 중 후속 화상회의 예정
- (추후 적용) 생산관리 → 공정별제공현황(포장 전)에서 폐기처리된 수량이 노출되지 않도록 조치

## 🔗 참고

- `TCO403` — 품목 마스터 (`LOCATION_TXT` 컬럼 추가 대상)
- `PROD_WAREHOUSE` — 완제품창고 (`LOCATION_TXT` 컬럼 추가 대상)
