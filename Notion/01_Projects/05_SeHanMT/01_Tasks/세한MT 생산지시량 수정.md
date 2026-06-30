---
base: "[[Notion/프로젝트 문서화/프로젝트/세한MT 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:29:00
담당자: []
---
사용한 브랜치: feature/Develop/Bug_Fix


수정한 코드 : Production.Viewmodel

---

1. 작업 공정이 첫 공정일 때 생산 지시량(ex 5000개)일 경우 양품수량이 지시량보다 초과 가능하게 수정, 수정 이후 작업 잔량 음수표시 안되고 0개로 되는지 확인, 다음 공정의 이전 공정 인수량: 5500개로 초과된 양품 갯수만큼 입력되어있게

```c#
if (SelectedItem.InputGoodQty < 0 ||
    SelectedItem.InputBadQty < 0 ||
    SelectedItem.InputGoodQty + SelectedItem.InputBadQty != SelectedItem.InputProdQty ||
    SelectedItem.InputProdQty > SelectedItem.REMAIN_QTY)
{
    _dialogService.ShowMessageBox("수량 입력값이 올바르지 않습니다.");
    return false;
}
```

→ 기존 로직 재한부 잔량이 투입수량보다 많은경우에만 투입 가능했음

```c#
bool isFirstProcess = (SelectedItem.WORK_SEQ == 1);

if (SelectedItem.InputGoodQty < 0 ||
    SelectedItem.InputBadQty < 0 ||
    SelectedItem.InputGoodQty + SelectedItem.InputBadQty != SelectedItem.InputProdQty)
{
    _dialogService.ShowMessageBox("수량 입력값이 올바르지 않습니다.");
    return false;
}

if (!isFirstProcess && SelectedItem.InputProdQty > SelectedItem.REMAIN_QTY)
{
    _dialogService.ShowMessageBox("첫 공정 이후에는 지시량을 초과할 수 없습니다.");
    return false;
}
```

→ 첫공정이 아닐때 잔량이 없어도 더투입할수 있도록 조치 ( 요청사항과 같게 여분재고를 위함 )

```sql
/* 작업 잔량 - 음수면 0으로 표시 */
, CAST(
    CASE
        WHEN PREV_WORK.WORK_NAME IS NULL THEN
            CASE
                WHEN ISNULL(A.PROD_QTY, 0) - ISNULL(H.GOOD_QTY, 0) < 0 THEN 0
                ELSE ISNULL(A.PROD_QTY, 0) - ISNULL(H.GOOD_QTY, 0)
            END
        ELSE
            CASE
                WHEN ISNULL(PREV_QTY.PREV_GOOD_QTY, 0) - ISNULL(H.PROD_QTY, 0) < 0 THEN 0
                ELSE ISNULL(PREV_QTY.PREV_GOOD_QTY, 0) - ISNULL(H.PROD_QTY, 0)
            END
    END
  AS INT) AS REMAIN_QTY
```

→ 작업잔량(REMAIN_QTY)는 DB저장 칼럼이 아닌 가지고 나올때 계산하는 부분임 → 최소값을 0으로제한

```c#
public int PROD_QTY
{
    get => _prodQty;
    set
    {
        if (value < 0) value = 0;

        // 생산수량은 작업지시량 or 인수수량보다 크면 안됨
        //int maxAllowed = Math.Min(PROD_TOTAL_QTY, RCV_QTY == 0 ? PROD_TOTAL_QTY : RCV_QTY);
        //if (value > maxAllowed)
        //    value = maxAllowed;

        if (SetProperty(ref _prodQty, value))
        {
            RecalculateFromGoodBad();
        }
    }
}
```

→ TableModel.cs 내에 제한부 주석처리 → 해당조건이 남아있을시에 양품, 생산수량이 작업지시량을 넘지 못함

```c#
//음수 방어부 이월 최소값을 0으로
int rcvQty = Math.Max(0, SelectedItem.InputRcvQty);

// 601 UPDATE
var sql1 = """
        UPDATE TPR601
        SET
            PROD_ETIME  = GETDATE(),
            PROD_QTY    = @PROD_QTY,
            GOOD_QTY    = @GOOD_QTY,
            BAD_QTY     = @BAD_QTY,
            RCV_QTY     = @RCV_QTY,
            WORKER_CODE = @WORKER_CODE,
            ORDER_FLAG  = '1',
            OPTIME      = GETDATE()
        WHERE TPR601ID   = @TPR601ID
          AND PROD_SEQ   = @PROD_SEQ
         -- AND ORDER_FLAG = '0'
    """;

int affected = _dbManager.SetDataSql(sql1, new[]
{
    new SqlParameter("@PROD_QTY",  SelectedItem.InputProdQty),
    new SqlParameter("@GOOD_QTY",  SelectedItem.InputGoodQty),
    new SqlParameter("@BAD_QTY",   SelectedItem.InputBadQty),
    new SqlParameter("@RCV_QTY",   rcvQty),
    new SqlParameter("@WORKER_CODE", WorkerCode ?? ""),
    new SqlParameter("@TPR601ID",  SelectedItem.TPR601ID),
    new SqlParameter("@PROD_SEQ",  SelectedItem.PROD_SEQ)
});
```

→ 작업종료시 저장할때 이월 잔량 RCV_QTY값이 0보다 작아지지 않도록 최솟값 0조치



---

2. 작업잔량 수정 ( 첫공정일 경우에도 작업지시량 - 양품수량 - 불량수량 )

```sql
/* 작업 잔량 - 음수면 0으로 표시 */
, CAST(
    CASE
        WHEN PREV_WORK.WORK_NAME IS NULL THEN
            CASE 
                WHEN ISNULL(A.PROD_QTY, 0) - ISNULL(H.GOOD_QTY, 0) - ISNULL(H.BAD_QTY, 0) < 0 THEN 0
                ELSE ISNULL(A.PROD_QTY, 0) - ISNULL(H.GOOD_QTY, 0) - ISNULL(H.BAD_QTY, 0)
            END
        ELSE
            CASE 
                WHEN ISNULL(PREV_QTY.PREV_GOOD_QTY, 0) - ISNULL(H.PROD_QTY, 0) < 0 THEN 0
                ELSE ISNULL(PREV_QTY.PREV_GOOD_QTY, 0) - ISNULL(H.PROD_QTY, 0)
            END
    END
  AS INT) AS REMAIN_QTY
```

→ ShowData 쿼리내 작업잔량 계산식에 BAD_QTY 추가

![[image 87.png]]

```c#
private DateTime GetLocalNowOnceFromDb()
{
    // 원하는 날짜와 시간을 하드코딩 (연, 월, 일, 시, 분, 초)
    // 예: 2026년 4월 15일 10시 30분 0초
    return new DateTime(2026, 4, 15, 10, 30, 0);
}
```

→ 초기 시간 설정부 하드코딩 ( 테스트 )



`_serverNow = await Task.Run(GetLocalNowOnceFromDb); //Test Tick 시작점 수정`

→ 기존로직내 _serverNow만 수정


---

<!-- Column 1 -->


<!-- Column 2 -->
~~메인 ui의 환경설정에서 Cycle Time Setting화
환경설정에서 CycleTime입력 시 502테이블?로 이동할 텐데 그게 설비별로 계속 유지되게 수정~~

⇒ 보류

→ ProdSettingViewModel내의에  바인딩 메서드 `CycleTime` → ITEM_CT_TIME → TPR504


```c#
/// <summary>
/// 환경 설정 팝업 출력
/// </summary>
[RelayCommand]
private void Settings()
{
    if (SelectedItem == null)
        return;

    if (!_vm.TryGetValue("settings", out var baseVm))
        return;

    switch (baseVm)
    {
        case ProdSettingViewModel prodVm:
            {
                prodVm.IsProd = IsEquip;
                //prodVm.CycleTime = IsEquip ? 0 : SelectedItem.ITEM_CT_TIME;
                prodVm.CycleTime = SelectedItem.ITEM_CT_TIME;
                prodVm.OnePerQty = SelectedItem.ITEM_ONT_PER_QTY;

                if (_win.ShowWindow(prodVm))
                {
                    SelectedItem.ITEM_CT_TIME = prodVm.CycleTime;
                    SelectedItem.ITEM_ONT_PER_QTY = prodVm.OnePerQty;

                    _dbRepo.UpdateSettings(
                        SelectedItem.PRODPLAN_DATE,
                        SelectedItem.PRODPLAN_SEQ,
                        SelectedItem.PRODWORK_SEQ,
                        SelectedItem.WORK_SEQ,
                        SelectedItem.ITEM_CT_TIME,
                        SelectedItem.ITEM_ONT_PER_QTY);
                }
                break;
            }
    }

```

→ IsEquip 상태일때 CycleTime값을 0으로 고정하는 부분 해제 → 저장된걸로 가지고 나오게

```c#

, ISNULL(NULLIF(A.ITEM_CT_TIME, 0), (
    SELECT TOP 1 ITEM_CT_TIME
    FROM TPR504
    WHERE FACTORY_CODE  = A.FACTORY_CODE
      AND WORK_CODE     = A.WORK_CODE
      AND EQUIP_SYS_CD  = A.EQUIP_SYS_CD
      AND ITEM_CT_TIME IS NOT NULL
      AND ITEM_CT_TIME  > 0
    ORDER BY PRODPLAN_DATE DESC, PRODPLAN_SEQ DESC
)) AS ITEM_CT_TIME

, ISNULL(NULLIF(A.ITEM_ONE_PER_QTY, 0), (
    SELECT TOP 1 ITEM_ONE_PER_QTY
    FROM TPR504
    WHERE FACTORY_CODE      = A.FACTORY_CODE
      AND WORK_CODE         = A.WORK_CODE
      AND EQUIP_SYS_CD      = A.EQUIP_SYS_CD
      AND ITEM_ONE_PER_QTY IS NOT NULL
      AND ITEM_ONE_PER_QTY  > 0
    ORDER BY PRODPLAN_DATE DESC, PRODPLAN_SEQ DESC
)) AS ITEM_ONE_PER_QTY
```
