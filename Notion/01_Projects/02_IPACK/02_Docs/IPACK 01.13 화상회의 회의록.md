---
base: "[[Notion/프로젝트 문서화/프로젝트/IPACK 프로젝트 DB/Project Docs- 프로젝트 문서 and New data source/Project Docs- 프로젝트 문서 and New data source.base]]"
카테고리: []
생성일시: 2026-06-10T14:28:00
상태: 진행 중
담당자: []
---
## 회의 일시 01.13 15:06 ~ 16:00

## ㅇ 회의목적

기존 화면 오류 개선

## ㅇ 문제 사항

구매관리 → 재고관리 → 재고현황 (재고수량이 맞지않음)

- 전산상 재고와 실제 재고가 맞지 않음 (세무회계때문에 문제)
- 연말마다 erp로 관리한 리스트로 감사를 받는데 안맞아서 문제가 생김
- 기존은 이월, 당기입고, 당기출고, 당기재고로 되어있고
- 입고량은 생산실적 → 포장작업장내 데이터로
- 출고량은 영업관리 → 출하현황으로 가져오는데
- 저장된 데이터가 끌어온 데이터와 달라 수량차이가 많이 발생함
- 이월된 내용부터 잘못되어 약간씩 틀어진 부분이 있었음
- 폐기처리화면 → 폐기처리된 수량만큼 재고현황에서 떨어주질않음 / 재고 현황과 연동이 안되어있음

      계정대체 등록으로 폐기를 진행했는데 재고현황에 반영이 안됨. 

- 영업관리 → 재고조정 (정상)

- 완제품 제고현황과 수주번호를 매칭시켜야함 (마지막으로 포장된 항목의 수주번호를 보여주세요.)
- 재고조정시에 입고와 출고를 동시에 지정해서 반영할수 없음
- 재고현황 페이지에서 완제품창고의 세부 창고위치를 보여주고 수기입력 또한 가능하게 해주세요.

품목별로 전부다 세부 위치정보를 찾아와야함.

## ㅇ 요구 사항

- 따라서 수동입력으로 재고량을 수정할수 있도록 해주세요
- 수주번호도 같이 조회할수 있게 해주세요
- 현재현황에서 재고조정란, 재고위치 추가
- 재고현황의 툴바 이름 정정요청 (당기입고량 → 당월입고량, 당기출고량 → 당월출고량, 당기재고량 → 현재재고량)
- 당월 입고량은 공정별생산수량의 정상수량과 같게, 당월 출하량은 출하현황과 같게
- 수식적용 점검요청 : 이월수량 + 당기입고량 - 당기출고량 +- 재고조정(수동입력값) = 현재재고
- 영업 → 수주등록 → 작업지시서에서 현재 재고수량이 표기될수 있게해주세요 (출력물)

→ 완제품 수량을 끌고와서 출력할수있게 (특이사항 아래쪽에)

- 생산관리 → 공정별제공현황(포장 전) → 수주가 마감된 사안도 여기서 뜨는 경우가 생김

→ 공정재고 폐기작업 관리에서 폐기처리를해도 재고 현황에서 나오는 상황이 생김



### **상단 요약 : 기본적으로는 정상수량을 가져오고 재고현황에서 재고량을 조절할수 있는 기능이 필요하다. (수량이 맞지않음)**

## 상단 결론 : 다 정상적으로 기능이 구현되어 있음.

## ㅇ 조치 필요 사안

1. ~~완제품 재고현황과 수주번호를 매칭시켜야함 (마지막으로 포장된 항목의 수주번호를 보여주세요.)~~

~~→ 김부장님이 쿼리를 수정해주실 예정 추후에 (품목계정, 수주처 사이에 칼럼으로 추가하기)~~

2. ~~재고조정 테이블 트리거 확인 필요 (로직을 두번타서 한개삭제했는데 두개삭제처리함)~~

~~→ 유과장님~~

3. ~~**재고현황 페이지에서 완제품창고의 세부 창고위치를 보여주고 수기입력 또한 가능하게 해주세요.**~~

~~**품목별로 전부다 세부 위치정보를 찾아와야함.**~~

~~**→ 품목마스터에서 텍스트로 업데이트 되게 OR TCO403을 가져와서 보여주기 칼럼을 텍스트로 입력할수있게 (CODE로 입력되어 있음) / LOCATION_TXT 칼럼을 TCO403에서 만들고 수기입력할수있도록 조치**~~

~~→LOCATION_TXT 칼럼 위치는 창고 바로뒤에 보여주기~~

→ 나

4. 영업 → 수주등록 → 작업지시서에서 현재 재고수량이 표기될수 있게해주세요 (출력물)

→ 완제품 수량을 끌고와서 출력할수있게 / 반영하기 

→ ?

5. 영업관리 → 출하반품처리 → 반품날짜 기준으로 날짜계산을 하는것이 아닌 최초 출고일 기준으로 날짜를계산함 

→ ?


## 위 사안은 이번주 안에 해결 후 다음 주 중에 화상회의 진행 예정

## 아래 사안은 추후 적용 예정

- 생산관리 → 공정별제공현황(포장 전) → 수주가 마감된 사안도 여기서 뜨는 경우가 생김

→ 공정재고 폐기작업 관리에서 폐기처리를해도 재고 현황에서 나오는 상황이 생김

→ 공정별 제공현황에서 폐기처리 수량이 보이지 않도록 조치하기





PROD_WAREHOUSE 밑에 LOCATION_TXT 칼럼 추가


SP_TMA922_SAVE02 → 저장부 수정 (운영 반영 완)

포장 → 박스당수량

단가

![[image 117.png]]

TCO403 테이블 칼럼 추가 → LOCATION_TXT

재고현황 리스트 프로시저, 센차수정

SP_WMA621_01_LIST

SP_WMA621_02_LIST

제품마스터 등록 프로시저, 클래스추가, 센차 수정

jvWCO304_01_IUD.java

SP_WCO304_01_IUD



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
