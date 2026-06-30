---

---
---

## 주차별 IUD 동작 개선

```java
USE [iPlusERP_IPACK_DEV]
GO
/****** Object:  StoredProcedure [dbo].[SP_WHR316_01_IUD]    Script Date: 2025-09-12 오전 8:54:55 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


ALTER PROC	[dbo].[SP_WHR316_01_IUD]
(
		@FACTORY_CODE	VARCHAR(6)
	,	@EMPLOYEE_NO	VARCHAR(30)
	,	@WG_CODE		VARCHAR(6)
	,	@OPMAN_CODE		VARCHAR(10)
	,   @WG_FROM_DATE	VARCHAR(8)
)
AS
BEGIN
SET NOCOUNT ON;

	UPDATE TIN312W 
	SET 
			WG_CODE			=	@WG_CODE
		,	OPMAN_CODE		=	@OPMAN_CODE
		,	OPTIME			=	CONVERT(VARCHAR(8), GETDATE(), 112) + LEFT(REPLACE(CONVERT(VARCHAR(8), GETDATE(), 108), ':', ''), 4)
		,	WG_FROM_DATE	=	@WG_FROM_DATE
		,	WG_TO_DATE		=	CONVERT(VARCHAR(8), DATEADD(DAY, 6, CONVERT(DATE, @WG_FROM_DATE)), 112)
	WHERE	FACTORY_CODE	=	@FACTORY_CODE
	AND		EMPLOYEE_NO		=	@EMPLOYEE_NO
	AND		WG_FROM_DATE	=	@WG_FROM_DATE     --주차 시작일이 같은경우에만 업데이트
	IF	@@ROWCOUNT = 0 
		BEGIN
			INSERT INTO TIN312W
			( 
				  FACTORY_CODE 
				, EMPLOYEE_NO 
				, WG_CODE
				, WG_BIGO
				, OPMAN_CODE
				, OPTIME
				, WG_FROM_DATE
				, WG_TO_DATE
			) 
			VALUES 
			( 
				  @FACTORY_CODE
				, @EMPLOYEE_NO
				, @WG_CODE
				, ''
				, @OPMAN_CODE
				, CONVERT(VARCHAR(8), GETDATE(), 112) + LEFT(REPLACE(CONVERT(VARCHAR(8), GETDATE(), 108), ':', ''), 4)
				, @WG_FROM_DATE
				, CONVERT(VARCHAR(8), DATEADD(DAY, 6, CONVERT(DATE, @WG_FROM_DATE)), 112)
			) 
		END
END

```

다른 주차 선택시 insert가 발생되지 않고 계속 update동작하는 문제를 해결하기 위해 UPDATE 정보를

set해주는 조건을 추가했습니다. 주차 시작일이 같은경우에만 UPDATE하고 나머지는 INSERT 하는방식을

사용하여 한 사용자가 주차별로 별개의 값을 받을수 있도록 했습니다.

```javascript
WHR316_VW_btnReg: function (btn) {
        var me = this;

        var grid = me.getView().lookup('grid');
        var store = grid.getStore();
        var selected = me.getView().lookup('combo_06').getValue();
        var RegCheck = false;

        store.each(function (record) {
            if (record.get('SELECT_FLAG') === true) {
                RegCheck = true;
            }
        });

        if (!RegCheck) {
            showToast('알림', '적용할 대상을 선택해주세요.');
            return;
        }

        store.each(function (rec) {
            if (rec.get('SELECT_FLAG') === true) {
                rec.set('FACTORY_CODE', me.getView().lookup('combo_01').getValue());
                rec.set('WG_CODE', selected);
                rec.set('OPMAN_CODE', gUserId);
                rec.set('WG_FROM_DATE', me.getView().lookup('combo_05').getValue());
            }
        });
```

일괄 적용시 WG_FROM_DATE가 null로 넘어가는 문제가 발생하여 해당 부처럼 store 적재 조건에

combo_05정보를 추가했습니다.

---

## 주차 조회시 각 월의 시작, 끝일 조회방법 수정

EX) 9월 첫일 조회시 8월 31일인데 필터가 시작일로 월정보만 비교하기에 겹쳐지지않음

```sql
LEFT OUTER JOIN (
			SELECT FACTORY_CODE, EMPLOYEE_NO, WG_CODE, WG_FROM_DATE
			FROM  TIN312W
			WHERE WG_FROM_DATE = @WG_FROM_DATE
		) T2 ON (T1.EMPLOYEE_NO = T2.EMPLOYEE_NO)
```

조회 조건을 수정했습니다. 기존 년월 정보를 받아와서 월로 자른다음 해당하는 월의 정보만 출력하는 방식이

아닌 주차정보 선택후 조회할때 해당 주차에 맞는 정보만 보여주면 되기에 YYYYMM을 조회 파라미터에서

빼고 조건을 삭제했습니다.

---

## 콤보박스 선택시 선택된 항목대로 바로 조회 기능 수정

기존 방식은 월조회 버튼 클릭마다 onview 동작을 통해 원하는 달에 해당되는 정보를 불러왔지만

주차별 조회이기 때문이 이를삭제하고 combobox에 onview 동작을 주고자 수정했습니다.

```javascript
onComboChange: function (dv, newValue, oldValue, eOpts) {
        var me = this;

        switch (dv.itemId) {
            case 'cbo_Factory': {
                me.onView();
                break;
            }
            case 'combo_02': {
                dv.getTrigger('clear')[dv.getValue() ? 'show' : 'hide']();
                break;
            }
            case 'combo_03': {
                dv.getTrigger('clear')[dv.getValue() ? 'show' : 'hide']();
                break;
            }
            case 'combo_04': {
                dv.getTrigger('clear')[dv.getValue() ? 'show' : 'hide']();
                break;
            }
            case 'combo_05': {
                dv.getTrigger('clear')[dv.getValue() ? 'show' : 'hide']();
                me.onView();
                break;
            }
```

다음과 같이 combo trigger에 onView 동작을 추가하여 주차 정보 선택시 마다 주차에 해당되는 정보를

조회할수있습니다.

---