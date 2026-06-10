---
base: "[[정보 저장소.base]]"
우선순위: 높음
종료일: 2025-08-01
상태: 완료
담당자:
  - 안재경
팀: []
---
목표:

- onNew함수를 활용 신규 버튼 클릭 동작 구현
- 등록중인 데이터를 제일 앞번에서 볼수 있도록 Data Store 제일 앞으로 올수있게 하기
- 저장, 삭제 버튼 클릭시 동작 구현하기
- 삭제시에는 반드시 사용자 요구를 한번 더 확인 할 수 있는 alert메세지 출력하기
등록시에는 필수요소 등록여부 확인하기.
- 저장 삭제시 통합 서블릿 파일의 동작 원리 알아보기


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
          xtype: 'checkcolumn',
          text: replaceLocale('삭제'),
          dataIndex: 'DELETE',
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
          cls: 'editColumncls',
          editor: {
            xtype: 'textfield',
            selectOnFocus: true,
            triggers: {
              search: {
                cls: 'x-form-search-trigger',
                handler: 'onSearch_DEPT',
              },
            },
          }, 
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
    },
  ],
});

```

—> View

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
  },
  
onNew: function () {
    var me = this;
    const grid = me.getView().down('#grid_Employee');
    const store = grid.getStore();

    let record = {
        DEPARTMENT_CODE: '',
        Department_Name: '',
        EMPLOYEE_NO: '',
        BASE_NAME: '',
    };

    console.log(record);
    store.insert(0, record);
},


  onReg: function () {
    var me = this;

    const grid = me.getView().down('#grid_Employee');
    const store = grid.getStore();

    var modifiedRecords = store.getModifiedRecords();
    var removedRecords = store.getRemovedRecords();
    if (modifiedRecords.length == 0 && removedRecords.length == 0) {
      Ext.Msg.alert(
        replaceLocale(TITLE_INFO),
        replaceLocale(MESSAGE_CHECK_STORE)
      );
      return;
    }

    for (var i = 0; i < store.getCount(); i++) {
      var record = store.getAt(i);

      if (!record.get('Department_Name')) {
        onCellEditFocusAlert(i, 'Department_Name', grid);
        return;
      }

      if (!record.get('BASE_NAME')) {
        onCellEditFocusAlert(i, 'BASE_NAME', grid);
        return;
      }

      if (!record.get('JOIN_DATE')) {
        onCellEditFocusAlert(i, 'JOIN_DATE', grid);
        return;
      }

      if (record.dirty) {
        record.set('FACTORY_CODE', gFactoryCode);
        record.set('OPMAN_CODE', gUserId);
        record.set('IUD', 'IU');
      }
      me.onView();
    }

    store.sync({
      success: function () {
        Ext.Msg.alert(replaceLocale(TITLE_INFO), replaceLocale(MESSAGE_REG));
      },
    });
  },

    onDelete: function () {
    var me = this;
    const grid = me.getView().down('#grid_Employee');
    const store = grid.getStore();

    let isThere = false;
    store.each(function (record, index) {
      if (record.get('DELETE')) {
        isThere = true;

        record.set('OPMAN_CODE', gUserId);
        record.set('IUD', 'D');
      }
    });

    if (!isThere) {
      Ext.Msg.alert(
        replaceLocale(TITLE_INFO),
        replaceLocale(MESSAGE_SELECT_COUNT_GRID)
      );
      return;
    }

    Ext.MessageBox.show({
      title: replaceLocale(TITLE_INFO),
      msg: replaceLocale(MESSAGE_DELETE_GRID),
      buttons: Ext.Msg.YESNO,
      icon: Ext.MessageBox.INFO,
      fn: function (btn) {
        if (btn == 'yes') {
          store.sync({
            success: function () {
              Ext.Msg.alert(
                replaceLocale(TITLE_INFO),
                replaceLocale(MESSAGE_DELETE)
              );
              me.onView();
            },
          });
        }
      },
    });
  },
  
  onSearch_DEPT: function () {
    var me = this;

    const win = Ext.create('iPlusERP.view.common.window.AddDept');
    win.getController().pCtrl = me;
    win.show();
  },

  onSetSingleDept: function (location, record) {
    var me = this;

    console.log(record);
    me.rRecord.set('DEPARTMENT_CODE', record.get('DEPT_CD'));
    me.rRecord.set('Department_Name', record.get('DEPT_NM'));
  },

});

```

[[— Controller]]

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
          name: 'DELETE',
          type: 'bool',
        },
        {
          name: 'AMOUNT',
          type: 'number',
        },
      ],
      proxy: {
        type: 'ajax',
        api: {
          create: Ext.manifest.api_url + '/com/edu/jvTest4_01_IUD',
          read: Ext.manifest.api_url + '/com/edu/jvTest4_01_LIST',
          update: Ext.manifest.api_url + '/com/edu/jvTest4_01_IUD',
          destroy: Ext.manifest.api_url + '/com/edu/jvTest4_01_IUD'
          
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

—> Model

```java
package com.edu;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Iterator;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.sql.DataSource;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.json.simple.parser.JSONParser;

import com.etc.ResponseCode;

import lombok.extern.log4j.Log4j2;

@Log4j2
@WebServlet("/com/edu/jvTest4_01_IUD")
public class jvTest4_01_IUD extends HttpServlet {
	private static final long serialVersionUID = 1L;

	@Override
	public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {
		
        String strMsg = "";
        String systemMsg = "";
        String strSuccess = "true";

        JSONArray itemList = new JSONArray();
        JSONObject returnObject = new JSONObject(); // 리턴

        Connection conn = null;
		
		try {

            request.setCharacterEncoding("UTF-8");         // UTF-8 로 인코딩해서 가져온다.
            
            conn = getConnection(request);
			
						conn.setAutoCommit(false); 
			
            if (request.getParameter("data") != null) {

                String items = request.getParameter("data");
                JSONArray array = parseJsonArray(items);

                Iterator<JSONObject> iterator = array.iterator();

                while (iterator.hasNext()) {

                    JSONObject jsonObject = (JSONObject) iterator.next();

                    try (PreparedStatement stmt = createPreparedStatement(conn, jsonObject)) {
                        stmt.executeUpdate(); // Executes the update statement
                    }
                }
            }
			
			conn.commit(); 
			
		} catch (Exception e) {
//          throw new ServletException(e);
            
          // 예외 처리 및 롤백
          strSuccess = "false";
          systemMsg = e.toString();

          if (conn != null) {
              try {
                  conn.rollback(); // 롤백
              } catch (Exception rollbackEx) {
                  systemMsg += " | Rollback failed: " + rollbackEx.toString();
              }
          }

          if (systemMsg.contains(":")) {
              String string[] = systemMsg.split(":");
              systemMsg = string[1];
          }

          strMsg = extractErrorMessage(e, systemMsg);

          log.error("Error occurred: ", e);

      } finally {
          // Connection 닫기
          if (conn != null) {
              try {
                  conn.close();
              } catch (Exception closeEx) {
                  // Connection 닫기 예외 로깅
              }
          }
      }

      // 응답 생성
      returnObject.put("success", strSuccess);
      returnObject.put("message", strMsg);
      returnObject.put("data", itemList);

      response.setContentType("text/html; charset=UTF-8");
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

  private JSONArray parseJsonArray(String usrItems) throws Exception {
      JSONArray array = null;
      if (usrItems.startsWith("{")) {
          JSONParser parser = new JSONParser();
          JSONObject jsonObject = (JSONObject) parser.parse(usrItems);
          array = new JSONArray();
          array.add(jsonObject);
      } else if (usrItems.startsWith("[")) {
          array = (JSONArray) JSONValue.parse(usrItems);
      }
      return array;
  }

  private PreparedStatement createPreparedStatement(Connection conn, JSONObject jsonObject) throws Exception {
      String sql = "EXEC SP_TEST4_01_IUD_AJK "        +
      "    @FACTORY_CODE = ?, "                     	+
      "    @EMPLOYEE_NO = ?, "                    		+
      "    @BASE_NAME = ?, "                    			+
      "    @JOIN_DATE = ?, "    	 				            +
      "    @DEPARTMENT_CODE = ?, "                 	  +
      "    @OPMAN_CODE = ?, "                 		    +
      "    @IUD = ?"
      ;
      
      log.info(sql);

      PreparedStatement stmt = conn.prepareStatement(sql);
      stmt.setString(1, 	sanitizeInput(jsonObject.get("FACTORY_CODE")));
      stmt.setString(2, 	sanitizeInput(jsonObject.get("EMPLOYEE_NO")));
      stmt.setString(3, 	sanitizeInput(jsonObject.get("BASE_NAME")));
      stmt.setString(4, 	sanitizeInput(jsonObject.get("JOIN_DATE")));
      stmt.setString(5, 	sanitizeInput(jsonObject.get("DEPARTMENT_CODE")));
      stmt.setString(6, 	sanitizeInput(jsonObject.get("OPMAN_CODE")));
      stmt.setString(7, 	sanitizeInput(jsonObject.get("IUD")));
      
      return stmt;
  }
  
  /**
   * 날짜 문자열을 'YYYYMMDD' 형식으로 변환 (Java 8 이상)
   * @param dateTimeStr 변환할 날짜 문자열
   * @return 8자리 날짜 문자열
   */
  private String convertToYYYYMMDD(String dateTimeStr) {
      if (dateTimeStr == null || dateTimeStr.trim().isEmpty()) {
          return "";
      }
      
      try {
          // 날짜 부분만 추출
          String datePart;
          if (dateTimeStr.contains("T")) {
              datePart = dateTimeStr.split("T")[0];
          } else if (dateTimeStr.contains(" ")) {
              datePart = dateTimeStr.split(" ")[0];
          } else {
              datePart = dateTimeStr;
          }
          
          // 날짜 파싱 및 변환
          LocalDate date = LocalDate.parse(datePart);
          return date.format(DateTimeFormatter.ofPattern("yyyyMMdd"));
      } catch (DateTimeParseException e) {
          return "";
      } catch (Exception e) {
          return "";
      }
  }

  private String sanitizeInput(Object input) {
	  log.info(input);
      return (input == null) ? "" : input.toString().trim().replace("'", "''");
  }

  private String extractErrorMessage(Exception e, String systemMsg) {
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

—>Servlet

```sql
CREATE SEQUENCE SEQ_EMP_NO
    START WITH 1001
    INCREMENT BY 1;
```

—> SEQUENCE 사용

```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_TEST4_01_IUD_AJK]    Script Date: 2025-07-31 오후 3:53:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_TEST4_01_IUD_AJK]
    @FACTORY_CODE     VARCHAR(10),
    @EMPLOYEE_NO      VARCHAR(10),
    @BASE_NAME        VARCHAR(10),
    @JOIN_DATE        VARCHAR(8),
    @DEPARTMENT_CODE  VARCHAR(10),
    @OPMAN_CODE       VARCHAR(10),
    @IUD              CHAR(2)
AS
BEGIN
    SET NOCOUNT ON;

    IF @IUD = 'IU'
    BEGIN
        UPDATE TIN114 SET DEPARTMENT_CODE = @DEPARTMENT_CODE
        WHERE EMPLOYEE_NO = @EMPLOYEE_NO	

        IF @@ROWCOUNT = 0

            BEGIN
                INSERT INTO TIN114 (
                    FACTORY_CODE,
                    EMPLOYEE_NO,
                    BASE_NAME,
                    JOIN_DATE,
                    DEPARTMENT_CODE,
                    OPMAN_CODE          
                )
                VALUES (
                    @FACTORY_CODE,
                    NEXT VALUE FOR TEST_SEQ,
                    @BASE_NAME,
                    @JOIN_DATE,
                    @DEPARTMENT_CODE,
                    @OPMAN_CODE
                );

            END
    END
    ELSE IF @IUD = 'D'
    BEGIN
        DELETE FROM TIN114
        WHERE
            FACTORY_CODE = @FACTORY_CODE
            AND EMPLOYEE_NO = @EMPLOYEE_NO;
    END
END
```

[[— 프로시져]]

[[Notion/정보 저장소/EDU 과제 3, 4/SQL Server IUD 통합프로시저 처리방식]]

---

→ RESULT

![[image 58.png]]

![[image 59.png]]

![[image 60.png]]

→ onNew → onReg ( IU중 프로시저 INSERT 처리) →

신규등록 개체는 controller에서 인덱스를 임의 0 처리하여 1열에서 볼수있음.

![[image 61.png]]

![[image 62.png]]

→ onReg내 update 동작 ( IU중 프로시저 UPDATE 처리) →

![[image 63.png]]

![[image 64.png]]

→ onDel ( D → 프로시저 DELETE 처리)