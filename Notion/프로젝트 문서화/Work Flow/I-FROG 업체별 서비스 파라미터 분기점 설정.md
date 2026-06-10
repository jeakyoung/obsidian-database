---
base: "[[Work Flow.base]]"
할당: []
상태: 검토 중
프로젝트: []
---
```c#
public async Task<object> GetNoticeList(NoticeRequest request)
{
    // 1. 공통 파라미터 생성 (기본 세팅)
    var parameters = new Dictionary<string, object>
    {
        { "TODATE1", request.sDate ?? "" },
        { "FROMDATE1", request.eDate ?? "" },
        { "EMPLOYEE_NO", request.employeeNo ?? "" }
    };

    // 2. 업체별 파라미터 커스텀 (분기 로직 격리)
    ApplyTickerSpecificLogic(parameters, request);

    try 
    {
        using (var helper = new SQLServerHelper(_connectionString, _logger))
        {
            DbProcedureRequest noticeRequest = new DbProcedureRequest
            {
                ProcedureName = "SP_WEB_FrmBP103_01_LIST", // 프로시저명은 동일
                Division = "NoticeList",
                Parameters = parameters // 조립된 파라미터 전달
            };
            
            // ... 실행 로직 ...
        }
    }
    catch (Exception ex) { /* 로깅 */ throw; }
}

// [핵심] 파라미터 분기 전용 메서드
private void ApplyTickerSpecificLogic(Dictionary<string, object> p, NoticeRequest req)
{
    switch (_tickerContext.CurrentTicker)
    {
        case "a":
            // A업체: 특정 관리자 권한 플래그가 반드시 필요함
            p.Add("IS_ADMIN_CHECK", "Y");
            break;

        case "b":
            // B업체: 프로시저는 같지만 사번 검색 시 앞에 접두어를 붙여야 함
            if (p.ContainsKey("EMPLOYEE_NO"))
                p["EMPLOYEE_NO"] = "B_CORP_" + req.employeeNo;
            break;

        case "c":
            // C업체: 날짜 검색 범위가 무조건 한 달 이내여야 함 (값 강제 수정)
            p["FROMDATE1"] = DateTime.Now.AddMonths(-1).ToString("yyyyMMdd");
            break;
    }
}
```

→ 해당 방식을 적용 Switch문을 활용해 파라미터가 다른 업체에 대한 통합 사전 진행

→ 단 저장 로직 자체가 다른 경우는 보류 ( 해당 부분에 대한 통합 작업이 한 회 더 필요.)




## → 단순히 case 문으로 사전 통합 후 작업 방향성

### [Step 1] 파라미터 가공 인터페이스 정의

```c#
public interface ITickerParameterStrategy
{
    string Ticker { get; }
    void Apply(Dictionary<string, object> parameters, object request);
}
```

### [Step 2] 업체별 클래스 구현 (격리된 공간)

새 업체가 추가되면 이 클래스 파일만 하나 더 만들면 됩니다. **기존 코드는 건드릴 필요가 없습니다.**

```c#
// A 업체 전용 로직
public class TickerASpecificStrategy : ITickerParameterStrategy
{
    public string Ticker => "a";
    public void Apply(Dictionary<string, object> p, object req)
    {
        p.Add("STRICT_MODE", "Y");
        p.Add("CORP_TYPE", "A_PREMIUM");
    }
}

// B 업체 전용 로직
public class TickerBSpecificStrategy : ITickerParameterStrategy
{
    public string Ticker => "b";
    public void Apply(Dictionary<string, object> p, object req)
    {
        // B업체는 사번 체계가 다르다고 가정
        if (p.ContainsKey("EMPLOYEE_NO")) 
            p["EMPLOYEE_NO"] = "B_" + p["EMPLOYEE_NO"];
    }
}
```

### [Step 3] 서비스 코드 (if문이 사라진 모습)

서비스는 현재 접속한 티커가 누구인지, 로직이 무엇인지 몰라도 됩니다. 그냥 실행만 합니다.

```c#
public class NoticeService : INoticeService
{
    private readonly IEnumerable<ITickerParameterStrategy> _strategies;
    private readonly TickerContext _context;

    public NoticeService(IEnumerable<ITickerParameterStrategy> strategies, TickerContext context)
    {
        _strategies = strategies;
        _context = context;
    }

    public async Task<object> GetNoticeList(NoticeRequest request)
    {
        var parameters = new Dictionary<string, object> { /* 공통 파라미터 */ };

        // [핵심] 현재 티커에 맞는 전략을 찾아 실행 (if문이 필요 없음)
        var strategy = _strategies.FirstOrDefault(s => s.Ticker == _context.CurrentTicker);
        strategy?.Apply(parameters, request); 

        // DB 실행...
    }
}
```

→ 해당 작업을 진행해야만 구조적인 서비스 통합이 가능함 / 지금 상태처럼 계속 작업을 이어나가면 새 업체 추가 시 전체 로직에 전체 서비스를 다시 추가해줘야 하는 일이 생겨버림

→ 단 타업체도 Default (  지금은 ATC  ) 로직을 전부 다 동일하게 따라가기만 한다면 case방식으로 조치해도 상관은 없음 ( 추가되는 값이 TICKER만 존재할경우 )

→ MVC패턴에 Strategy 패턴을 결합 → 해당 패턴으로 별도 업체에 대한 규칙을 캡슐화 서비스에서는 호출로만 사용

```c#
[클라이언트 요청]
　　↓
[컨트롤러]
　　↓
[공통 서비스] ◀──────▶ [Strategy 인터페이스]
　　↓　　　　　　　　　　　　　　┃
　　↓　　　　　　　　　 [업체별 Strategy 구현체]
　　↓　　　　　　　　　　(ATC, SGY, DBG 등)
[DB (SQLServer)]
　　↓
	[결과 반환]
```


1. 접속과 동시에 헤더로 JWT 토큰, 보안코드를 받음
2. 보안코드를 가지고 커넥션 매핑
3. 커넥션 생성

이후 도메인 정보 같은 DB 정보를 메인 서버로 옮겨와야 하긴 함 ( 백엔드 로직은 준비되어있음 )

4. 6번 서버를 사용 → Window OS
5. Docker 이미지를 통해 세팅을 한번에 불러오기
6. .netcore 프레임워크 8 → 10 ( 마이그레이션 쉬움! )
7. 업체 별 서비스 분리 ( 어떻게 할지 )
8. 메인 서버 이관 → DB가 필수 → 어떤 걸 도입 하는게 좋을지 ( mariaDB, PostgreSQL, DynamoDB  )

→ 찾아보기 어떤게 좋고 유리할지 ( 금액, 편의성, 성능 )

SYG → SYN

TICKER, SEC_CODE, DOMAIN

TICKER → RUN_TYPE으로 가져오기

자동로그인 → JWT토큰, ID, PWD(하드코딩), 

LOGIN → TOKEN → FCMTOKEN

AutoLogin → TOKEN, DeviceType, OsInfo, Domain, FTP서버 (메인서버 DB)

받아서 대기시키고 security_code를 통해 커넥션을 만들고 

메인 디비내의 getTGI003을 만들어서 2000

로그인에서 → security_code

서버 40110(dev), 40220(prd) → 만들기

동방 - ConfirmApproval 서비스 호출시 합의기능을 별도로 호출해주어야함 → ATC, 송연 미존재 프로시저가 존재함
