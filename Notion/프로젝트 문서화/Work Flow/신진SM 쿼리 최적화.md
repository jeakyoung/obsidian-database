---
base: "[[Work Flow.base]]"
할당: []
상태: 완료
프로젝트: []
---
투입 자재에 따라 공정을 선택해야함

- 폭절단
- 평면
    - 평탄
- 길이절단
    - 포장 → 포장실적 생성 
    - 출하계획 → 출하처리 + 재고차감
        - 이름은 포장이지만 길이절단으로 공정 실적을 만들고 → 제품창고
    - 수불번호만 포함해서 한줄을 더만든 뒤에 → 출하창고


단일 출하 계획에 → TPR601LOT에도 두 줄이 생기는 경우가 발생

## MES

신진 → 생산 실적 조회 → 재질 SEARCH_BOX 오류 해결 필요 → X버튼을 눌러도 필터 초기화가 안됨

→ onRemove_FieldValue 의 미존재로 인해 실제 검색 파라미터 Value 미초기화

![[image 210.png]]

![[image 211.png]]

→ ClearTrigger 트리거내 초기화 로직 추가

## POP

CARBON → LABEL 프린터 내용 추가

I-PACK → 속도 개선 필요

→ 매일 17시30분에 중복 데이터 점검 필요 / 중복데이터를 MES상에서 삭제해주어야함

```sql
select c.system_lot_no, * from tpr601 a with(nolock)
	left outer join  tpr601lot c with(nolock)
	on a.PRODPLAN_DATE = c.PRODPLAN_DATE 
	and a.PRODPLAN_SEQ = c.prodplan_seq
	and a.prod_seq = c.prod_seq
	, tpr301r b with(nolock)
where a.PRODPLAN_DATE = b.PRODPLAN_DATE 
and a.PRODPLAN_SEQ = b.prodplan_seq
and b.order_no = '202605S06360'
--and a.work_code = '002'
and a.work_code = '005'

--P202605009423


select * from tpr601 where prodplan_date = 'DZ260512' and prodplan_seq = 	414	and prod_seq = 2
select * from tpr601lot where prodplan_date = 'DZ260512' and prodplan_seq = 	414	and prod_seq = 2

--중복건 조회(포장공정)
select b.order_no,b.order_seqno, a.prodplan_date, a.prodplan_seq, a.prod_seq, a.work_code,a.ITEM_CODE
,count(c.system_lot_no) cnt  from tpr601 a with(nolock)
left outer join tpr301r b with(nolock)
on a.PRODPLAN_DATE = b.PRODPLAN_DATE
and a.PRODPLAN_SEQ = b.PRODPLAN_SEQ
left outer join tpr601lot c with(nolock)
on a.PRODPLAN_DATE = c.PRODPLAN_DATE
and a.PRODPLAN_SEQ = c.PRODPLAN_SEQ
and a.prod_seq = c.prod_seq
--where b.order_no like '202604S16861'
where a.prod_stime >= '202605120900'
and a.work_code = '005'
--and b.order_no = '202604S19888'
group by  b.order_no,b.order_seqno, a.prodplan_date, a.prodplan_seq, a.prod_seq, a.work_code,a.ITEM_CODE
having count(c.system_lot_no) > 1
order by b.order_no



select * from tpr601 where prodplan_date = 'DZ260512' and prodplan_seq = 	414	and prod_seq = 2
select * from tpr601lot where prodplan_date = 'DZ260512' and prodplan_seq = 	414	and prod_seq = 2
select * from tsa407 where order_no = '202605S06360' and order_seqno = 2
select * from tsa407l where SHIPPLAN_SEQ IN ('202605121235','202605121238')
 
```


백단 → 코드방어부

```c#
#region 중복포장 DB 레벨 체크 (다른 PC/사용자 동시 접근 방어)
_stepStart = DateTime.Now;
sQuery = new StringBuilder();
sQuery.Append(" SELECT ISNULL(prod_etime, '') AS prod_etime ");
sQuery.Append("   FROM tpr601 WITH(NOLOCK) ");
sQuery.Append("  WHERE factory_code  = @factory_code ");
sQuery.Append("    AND prodplan_date = @prodplan_date ");
sQuery.Append("    AND prodplan_seq  = @prodplan_seq ");
sQuery.Append("    AND prod_seq      = @prod_seq ");

sqlParams = new SqlParameter[]
{
     new SqlParameter("@factory_code",  sFactoryCode)
    ,new SqlParameter("@prodplan_date", sProdPlanDate)
    ,new SqlParameter("@prodplan_seq",  iProdPlanSeq)
    ,new SqlParameter("@prod_seq",      iProdSeq)
};

dt = _DB.GetDataView_Tran("DupCheck", sQuery, sqlParams, conn, sTran).Table;
LogStep("중복포장 사전 체크", "(inline-tpr601)", dt != null,
    $"ProdPlanDate={sProdPlanDate}  ProdPlanSeq={iProdPlanSeq}  ProdSeq={iProdSeq}");

if (dt.Rows.Count > 0 && !string.IsNullOrEmpty(dt.Rows[0]["prod_etime"]?.ToString()))
{
    COMMON.LogHelper.Debug($"  ├─ [ROW{i + 1}/{gv1.RowCount}] ★ 중복포장 차단 ★ 이미 완료된 건 (prod_etime={dt.Rows[0]["prod_etime"]})  OrderNo={sOrderNo}  ProdSeq={iProdSeq}");
    gv1Cnt++;
    continue;
}
#endregion
```

lot601_IUD → 조회조건 주석처리

pack_ins_tpr601Lot → 조회먼저하게 수정

길이 절단 → 소형절단 과정시 작업시간이 너무 짧아서 동시접근될 가능성이 높음

→ 타임아웃 타임아웃이 1초이상 발생시 3회 재시도 / 세번다 실패시에 타임아웃 ( 일단 로그부터 )

출하 더블 클릭 방지 추가 ( UIHelper ) → LOCK으로 공통 함수 씌워주기만 하면 됨

예약 업데이트 → wpf + C# ( 정기 업데이트 일자 사전 정의 필요 ) / exe형식 배포

→ FTP서버 에 올리는 업데이트 스케줄링 프로그램 / 시간대 별 업데이트 항목 삭제 / 상시 스케줄링으로 폴더내 값이 있는지 없는지 확인 → 업데이트
