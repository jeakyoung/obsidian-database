---
base: "[[정보 저장소.base]]"
우선순위: 높음
종료일: 2025-07-29
상태: 완료
담당자:
  - 안재경
팀: []
---
목표:

그리드 조회 버튼 클릭시


검색조건 3개 파라미터 정의해서


서블릿 서비스 연결 후 데이터 조회 하기

```javascript
Ext.define('AppTest1.view.GW.WGW500.test4', {
  extend: 'Ext.Panel',
  xtype: 'test4',

  controller: 'test4',
  viewModel: 'test4',

  title: replaceLocale('그리드2'),

  layout: {
    type: 'vbox',
    align: 'stretch',
  },

  dockedItems: [
    {
      xtype: 'commonToolbar2',
    },
  ],

  tbar: [
    {
      xtype: 'fieldset',
      title: replaceLocale('상세검색'),
      width: '100%',
      defaults: {
        anchor: '100%',
        flex: 1,
        fieldDefaults: {
          labelSeparator: '',
        },
      },
      items: [
        {
          xtype: 'fieldcontainer',
          fieldLabel: replaceLocale('입사일자'),
          layout: 'hbox',
          defaults: {
            hideLabel: true,
            margin: '0 5 0 0',
          },
          items: [
            {
              xtype: 'datefield',
              itemId: 'df_Start',
              fieldLabel: 'Start',
              value: Ext.Date.add(new Date(), Ext.Date.MONTH, -6),
              inputType: 'search',
              format: 'Y/m/d',
              allowBlank: false,
            },
            {
              xtype: 'datefield',
              itemId: 'df_End',
              fieldLabel: 'End',
              format: 'Y/m/d',
              value: new Date(),
              inputType: 'search',
              allowBlank: false,
            },
          ],
        },
        {
          xtype: 'fieldcontainer',
          fieldLabel: replaceLocale('통합검색'),
          layout: 'hbox',
          defaults: {
            hideLabel: true,
            margin: '0 5 0 0',
          },
          items: [
            {
              xtype: 'textfield',
              emptyText: replaceLocale('부서명, 사원명 검색'),
              inputType: 'search',
              itemId: 'tf_Search',
            },
          ],
        },
      ],
    },
  ],

  items: [
    {
      xtype: 'grid',
      title: replaceLocale('명부'),
      flex: 1,
      itemId: 'grid_Employee',
      bind: {
        store: '{gridStore_Employee}',
      },
      selModel: 'cellmodel',
      columnLines: true,
      plugins: [
        {
          ptype: 'cellediting',
          clicksToEdit: 1,
        },
        {
          ptype: 'gridexporter',
        },
      ],
      columns: [
        {
          xtype: 'rownumberer',
        },

        {
          text: replaceLocale('부서코드'),
          dataIndex: 'DEPARTMENT_CODE',
          flex: 1,
          editor: null,
        },
        {
          text: '<font color="#FF006C">*</font>' + replaceLocale('부서명'),
          dataIndex: 'Department_Name',
          flex: 1,
          editor: null,
        },
        {
          text: replaceLocale('사원번호'),
          dataIndex: 'EMPLOYEE_NO',
          flex: 1,
          editor: null,
        },
        {
          text: '<font color="#FF006C">*</font>' + replaceLocale('이름'),
          dataIndex: 'BASE_NAME',
          flex: 1,
          cls: 'editColumnCls',
          editor: {
            xtype: 'textfield',
            selectOnFocus: true,
          },
        },
        {
          xtype: 'datecolumn',
          text: '<font color="#FF006C">*</font>' + replaceLocale('입사일'),
          align: 'center',
          dataIndex: 'JOIN_DATE',
          cls: 'editColumnCls',
          flex: 1,

        },
      ],
    }
  ],
});

```

[[— View]]

```javascript
Ext.define('AppTest1.view.GW.WGW500.test4Controller', {
  extend: 'Ext.app.ViewController',
  alias: 'controller.test4',

  rRecord: false,

  init: function () {
    this.control({
      test4: {},
      'test4 grid': {
        select: 'onSelect',
      },
    });
  },

  onSelect: function (rowModel, record) {
    var me = this;

    me.rRecord = record;
  },

  onView: function (btn) {
    var me = this;

    const store = me.getViewModel().getStore('gridStore_Employee');
    store.load({
      params: {
        ST_DATE: Ext.util.Format.date(
          me.getView().down('#df_Start').getValue(),
          'Ymd'
        ),
        ED_DATE: Ext.util.Format.date(
          me.getView().down('#df_End').getValue(),
          'Ymd'
        ),
        SEARCH_NAME: me.getView().down('#tf_Search').getValue(),
      },
      callback: function (records, op, success) {
        if (success) {
          Ext.Msg.alert(replaceLocale(TITLE_INFO), replaceLocale('조회완료'));
        } else {
          store.removeAll();
          store.clearData();
        }
      },
    });
    }
});

```

—> Controller

```javascript
Ext.define('AppTest1.store.GW.WGW500.test4', {
  extend: 'Ext.app.ViewModel',
  alias: 'viewmodel.test4',

  stores: {
    gridStore_Employee: {
      fields: [
        {
          name: 'JOIN_DATE',
          type: 'date',
          dateReadFormat: 'Ymd',
          dateWriteFormat: 'Ymd',
        },
        {
          name: 'AMOUNT',
          type: 'number',
        },
      ],
      proxy: {
        type: 'ajax',
        api: {
          read: Ext.manifest.api_url + '/com/edu/jvTest4_01_LIST',
        },
        reader: {
          type: 'json',
          rootProperty: 'data',
        },
        writer: {
          type: 'json',
          writeAllFields: true,
          encode: true,
          rootProperty: 'data',
        },
      },
    },
  },
});

```

—> Store

```java
@Override
public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {

    String strSuccess = "true";
    String strMsg = "";
    String systemMsg = "";

    JSONObject returnObject = new JSONObject();
    JSONArray itemList = new JSONArray();

	try {

        request.setCharacterEncoding("UTF-8");

		String ST_DATE = sanitize(request.getParameter("ST_DATE"));
		String ED_DATE = sanitize(request.getParameter("ED_DATE"));
		String SEARCH_NAME = sanitize(request.getParameter("SEARCH_NAME"));

		String sql = "EXEC SP_EDU4_01_LIST_AJK"
		+ "\\r\\n" + "@STARTDATE = '" 		+ ST_DATE 		+ "'"
		+ "\\r\\n" + ",@ENDDATE = '" 			+ ED_DATE 		+ "'"
		+ "\\r\\n" + ",@SEARCH = '" 			+ SEARCH_NAME 	+ "'";

		log.info(sql);

        try (Connection conn = getConnection(request);
             Statement stmtRead = conn.createStatement();
             ResultSet rs = stmtRead.executeQuery(sql)) {

            ResultSetMetaData rm = rs.getMetaData();

            while(rs.next())
            {
                JSONObject tempJson = new JSONObject();
                for(int nCount=1 ; nCount <=  rm.getColumnCount() ; nCount++)
                {
                    tempJson.put(rm.getColumnName(nCount), sanitize(rs.getString(rm.getColumnName(nCount))));
                }
                itemList.add(tempJson);
            }
        }

	} catch (Exception e) {
        strSuccess = "false";
        systemMsg = e.getMessage();

        if(systemMsg.contains(":") == true){
            String string[] = systemMsg.split(":");
            systemMsg = string[1];
        }

        strMsg = extractErrorMessage(e, systemMsg);
        log.error("Error occurred: ", e);
    }

    returnObject.put("success", strSuccess);
    returnObject.put("message", strMsg);
    returnObject.put("data", itemList);

    response.setContentType("application/json; charset=UTF-8");
    try (PrintWriter out = response.getWriter()) {
        out.print(returnObject);
        out.flush();
    }
}

private Connection getConnection(ServletRequest request) throws Exception {

	Context initContext = new InitialContext();
	DataSource ds = (DataSource) initContext.lookup("java:comp/env/jdbc/iPlusERP");

	return ds.getConnection();
}

private String sanitize(String input) {
    return input == null ? "" : input.trim().replace("'", "''");
}

private String convertToYYYYMMDD(String dateTimeStr) {
    if (dateTimeStr == null || dateTimeStr.trim().isEmpty()) {
        return "";
    }

    try {
        String datePart;
        if (dateTimeStr.contains("T")) {
            datePart = dateTimeStr.split("T")[0];
        } else if (dateTimeStr.contains(" ")) {
            datePart = dateTimeStr.split(" ")[0];
        } else {
            datePart = dateTimeStr;
        }

        LocalDate date = LocalDate.parse(datePart);
        return date.format(DateTimeFormatter.ofPattern("yyyyMMdd"));
    } catch (DateTimeParseException e) {
        log.error("날짜 파싱 오류: " + dateTimeStr, e);
        return "";
    } catch (Exception e) {
        log.error("날짜 형식 변환 오류: " + dateTimeStr, e);
        return "";
    }
}

	String extractErrorMessage(Exception e, String systemMsg) {
    String exceptionClassName = e.getClass().getSimpleName();

    switch (exceptionClassName) {
        case "NullPointerException":
            return ResponseCode.SYSTEM_ERROR.getMessage() + systemMsg;
        case "SQLServerException":
            return ResponseCode.SQL_SERVER_ERROR.getMessage() + systemMsg;
        default:
            return ResponseCode.UNKNOWN_ERROR.getMessage() + systemMsg;
    }
}
}
```

—> Servlet

```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_EDU4_01_LIST_AJK]    Script Date: 2025-08-01 오전 9:47:55 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


ALTER PROC [dbo].[SP_EDU4_01_LIST_AJK]
(
	@STARTDATE	VARCHAR(8),
	@ENDDATE	VARCHAR(8),
	@SEARCH		NVARCHAR(500) = ''
)
AS

BEGIN

	SELECT A.FACTORY_CODE, A.DEPARTMENT_CODE, B.Department_Name, A.EMPLOYEE_NO, A.BASE_NAME, A.JOIN_DATE
	FROM	 TIN114 AS A
	LEFT JOIN	 TIN122 AS B
	ON A.DEPARTMENT_CODE = B.DEPARTMENT_CODE

END
```

[[— Procedure]]


![[image 66.png]]

[[— 최종 실행 화면 Test4]]
