---
base: "[[Notion/프로젝트 문서화/프로젝트/IPACK 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:28:00
담당자:
  - 안재경
---
[[업무_전달-안재경.pdf]]

[[업무_전달-안재경 (수정).pdf]]

[[인사테이블정보.pdf]]

[[업무_전달-안재경 (1).pdf]]



[[업무_전달-안재경 (3).pdf]]

근태 일자

부서명

사원 번호

직위

사원 성명

근무조

출근구분

출근

퇴근

외출

귀사

전체 필터

주간조인지 야간조인지

범위가 - 로 가는경우 시간계산방법 ( 직장에서 밤샐때 )

기본시간

→ 주간 : 0900 ~ 1800 → 9시간

→ 야간: 21:00 ~ 0600 → 9시간

지각시간

→ 주간 : 출근시간  - 0900 → 계산후에 4자리 선언후 빈공간 0채우기

→ 야간 : 출근시간 - 2100

시간외 시간

→ 주간 : 기본시간 - ( 총 근무시간 - 9시간 )

→ 야간 : 기본시간 - ( 총 근무시간 - 9시간 )

조퇴 시간

→ 주간 : 기본시간 - 총 근무 시간

→ 야간 : 기본시간 - 총 근무 시간

심야시간

→ 주간 : IF (  근태일자에 22시 ≤ 날짜포함 퇴근시간 )

→ 야간 : IF (  근태일자에 22시 ≤ 날짜포함 퇴근시간 )

                    날짜포함 퇴근시간 - 날짜포함 근태일자의 22시

철야수당 계산법 : 통상시급 * 1.5 * 심야시간


주간조가 18시까지 퇴근인데 퇴근할때 다음날 00시를 넘어가는 경우 계산??

19일 1800  20일 0000

1일 -1800

날짜계산으로 1일을 받았을때

-로 받은값을 2400에다 더해주면 6시간

19일 1800 20일 0230

-1600

2400

08

날짜 + ( 시간, 분) → 여기서 날짜때고 시간분 계산해서 퇴근일자가 근태일자보다 크다면 2400더해주고

시간, 분때서 출력

파라미터

공장코드, 사원번호, 근무조, 

( 근무시간, 기본시간 ) → 참조?

조회에서 파라미터로 받아온 KT_DATE랑 테이블내 저장되어있던 KT_DATE를 둘다 년 월로 때어서

WHERE조건에 넣기

15 ~ 19까지


```javascript
/*******************************************************************************
 * 프로그램명 : 인사급여>근태관리>근무조별 일근태등록
 * 파 일 명 : WHR314_CT.js
 * 작 성 자 : 안재경
 ******************************************************************************/

Ext.define('iPlusERP.controller.HR.WHR300.WHR314_CT', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.WHR314_CT',

    init: function () {
        this.control({
            'WHR314_VW textfield': {
                specialkey: this.onKeyPress,
            },
        });

        this.onInit();
    },

    // 근무조 콤보
    onSetCombo_workteam: function () {
        var store = this.getViewModel().getStore('storeCombo_workteam');
        store.load({
            params: {
                FACTORY_CODE: gFactoryCode,
            },
            callback: function (records, operation, success) {
                if (success) {
                }
            },
        });
    },
    //출근구분 콤보
    onSetcombo_ChulGbn: function () {
        var store = this.getViewModel().getStore('cboStore_CHUL_GBN1');
        var me = this;

        store.load({
            params: {
                CODE_ID1: '256',
            },
            callback: function (records, operation, success) {
                if (success) {
                    me.onView();
                }
            },
        });
    },

    onInit: function () {
        var me = this;

        me.onSetCombo_workteam(); // 근무조코드
        me.onSetcombo_ChulGbn(); // 근무형태
        me.onView();
    },

    onView: function () {
        var me = this;
        var store = this.getViewModel().getStore('store_01');

        store.load({
            params: {
                FACTORY_CODE: gFactoryCode,
                KT_DATE: Ext.util.Format.date(me.getView().down('#KT_DATE').getValue(), 'Ymd'),
                WORK_TEAM: me.getView().down('#cbo_workteam').getValue() || '',
                DEPARTMENT_NAME: me.getView().down('#tf_dept').getValue() || '',
                EMPLOYEE_NAME: me.getView().down('#tf_emp').getValue() || '',
            },
            callback: function (records, op, success) {
                if (success) {
                    Ext.each(records, function (rec) {});
                }
            },
        });
    },

    /* 
    kt:  20250915
    null
    result:  null
    
    */

    // var arrayRecords = [];

    // Store.each(function (rec) {
    //     if (rec.get('SELECT_FLAG') === true) {
    //         var baseData = {
    //             FACTORY_CODE: gFactoryCode,
    //             EMPLOYEE_NO: rec.get('EMPLOYEE_NO'),
    //             KT_DATE: me.getView().down('#KT_DATE').getValue() || '',
    //             WG_CODE: rec.get('WG_CODE'),
    //             CODE_ID2: rec.get('CODE_ID2') || '',
    //             OPMAN_CODE: gUserId,
    //             IRU: 'IU',
    //         };
    //         if (rec.get('CODE_ID2') == '001') {
    //             var newRec = Ext.create(
    //                 Store.getModel(),
    //                 Ext.apply({}, baseData, {
    //                     DS_CODE: '01',
    //                     DS_TIME: 8.0,
    //                 })
    //             );
    //             arrayRecords.push(newRec);
    //         }
    //         if (rec.get('CODE_ID2') == '002') {
    //             var newRec = Ext.create(
    //                 Store.getModel(),
    //                 Ext.apply({}, baseData, {
    //                     DS_CODE: '33',
    //                     DS_TIME: 7.0,
    //                 })
    //             );
    //             arrayRecords.push(newRec);
    //         }
    //         if (parseFloat(rec.get('BASIC_TIME')) > parseFloat(rec.get('WORK_TIME'))) {
    //             var newRec = Ext.create(
    //                 Store.getModel(),
    //                 Ext.apply({}, baseData, {
    //                     DS_CODE: '10',
    //                     DS_TIME: parseFloat(rec.get('BASIC_TIME')) - parseFloat(rec.get('WORK_TIME')),
    //                 })
    //             );
    //             arrayRecords.push(newRec);
    //         }
    //         if (parseFloat(rec.get('WORK_TIME')) > parseFloat(rec.get('BASIC_TIME'))) {
    //             var newRec = Ext.create(
    //                 Store.getModel(),
    //                 Ext.apply({}, baseData, {
    //                     DS_CODE: '12',
    //                     DS_TIME: parseFloat(rec.get('WORK_TIME')) - parseFloat(rec.get('BASIC_TIME')),
    //                 })
    //             );
    //             arrayRecords.push(newRec);
    //         }
    //         if (parseFloat(rec.get('LAST_OUT')) < parseFloat(rec.get('WG_PRDTO'))) {
    //             var newRec = Ext.create(
    //                 Store.getModel(),
    //                 Ext.apply({}, baseData, {
    //                     DS_CODE: '21',
    //                     DS_TIME: parseFloat(rec.get('BASIC_TIME')) - parseFloat(rec.get('WORK_TIME')),
    //                 })
    //             );
    //             arrayRecords.push(newRec);
    //         }
    //     }
    // });

    // Store.add(arrayRecords);
    onReg: function () {
        var me = this;
        var grid = me.getView().down('grid');
        var originalStore = grid.getStore();

        var dsCodeMapping = {
            BASIC_TIME: '01',
            LATE_TIME: '10',
            OVER_TIME: '33',
            EARLY_TIME: '12',
            NIGHT_TIME: '37',
            NIGHT_ALLOW: '35',
        };

        var tempStore = Ext.create('Ext.data.Store', {
            model: originalStore.getModel(),
            proxy: originalStore.getProxy(),
        });

        originalStore.each(function (rec) {
            if (rec.dirty) {
                var baseData = {
                    FACTORY_CODE: gFactoryCode,
                    EMPLOYEE_NO: rec.get('EMPLOYEE_NO'),
                    KT_DATE: me.getView().down('#KT_DATE').getValue() || '',
                    WG_CODE: rec.get('WG_CODE') || '',
                    CODE_ID2: rec.get('CODE_ID2') || '',
                    OPMAN_CODE: gUserId,
                    IRU: 'IU',

                    if (WG_CODE = '001' && rec.get('WG_PRDFROM') == null){
                        rec.set('WG_PRDFROM' = '0900')
                    },
                    if (WG_CODE = '001' && rec.get('WG_PRDTO') == null){
                        rec.set('WG_PRDFROM' = '1800')
                    },
                    if (WG_CODE = '002' && rec.get('WG_PRDTO') == null){
                        rec.set('WG_PRDFROM' = '2100')
                    },
                    if (WG_CODE = '002' && rec.get('WG_PRDTO') == null){
                        rec.set('WG_PRDFROM' = '0600')
                    }
                };

                Ext.Object.each(dsCodeMapping, function (key, code) {
                    var dsTime = rec.get(key) || '0.00';
                    var realIn = parseFloat(rec.get('FIRST_IN'));
                    var realOut = parseFloat(rec.get('LAST_OUT'));
                    var planIn = parseFloat(rec.get('WG_PRDFROM'));
                    var planIn2 = parseFloat(rec.get('WG_PRDFROM')) + 2400.0; //야간조 익일계산
                    var planOut = parseFloat(rec.get('WG_PRDTO'));
                    var planOut2 = parseFloat(rec.get('WG_PRDTO')) + 2400.0;
                    console.log(realIn, realOut, planIn, planOut);

                    /*
                    01 기본 시간, 10 지각 시간, 12 조퇴 시간
                    33 시간 외 시간, 35 철야 시간, 37 심야 시간
                    주간, 야간에 따른 조건이 다름 ex 2200 ~ 0122를 주간 계산과 같게 돌리면 - 나옴
                    */
                    if (code == '01') {
                        dsTime = '8.00';
                    } else if (code == '37' && rec.get('WG_CODE') == '002') {
                        dsTime = '7.00';
                    } else if (code == '37' && rec.get('WG_CODE') == '001') {
                        dsTime = '0.00';
                    } else if (code == '35' && rec.get('WG_CODE') == '002') {
                        dsTime = '1.00';
                    } else if (code == '35' && rec.get('WG_CODE') == '001') {
                        dsTime = '0.00';
                    } else if (code == '10' && planIn < realIn) {
                        dsTime = (realIn - planIn) / 100.0;
                    } else if (code == '33' && planOut < realOut && rec.get('WG_CODE') == '001') {
                        dsTime = (realOut - realIn - (planOut - planIn)) / 100.0 - 0.5;
                        if (dsTime <= 0) {
                            dsTime = '0.00';
                        }
                    } else if (code == '33' && planOut < realOut && rec.get('WG_CODE') == '002') {
                        dsTime = (realOut - realIn - (planOut2 - planIn)) / 100.0 - 0.5;
                        if (dsTime <= 0) {
                            dsTime = '0.00';
                        }
                    } else if (code == '12' && realOut < planOut) {
                        dsTime = (planOut - realOut) / 100.0;
                    }

                    var newRec = Ext.create(
                        originalStore.getModel(),
                        Ext.apply({}, baseData, {
                            DS_CODE: code,
                            DS_TIME: dsTime,
                        })
                    );

                    tempStore.add(newRec);
                });
            }
        });

        tempStore.sync({
            success: function () {
                showToast('알림', '저장 하였습니다.');
            },
            failure: function () {
                showToast('알림', '저장에 실패하였습니다.');
                return;
            },
            callback: function () {
                me.onView();
            },
        });
    },

    onKeyPress: function (textfield, event, options) {
        var me = this;
        if (event.getKey() == event.ENTER) {
            // this.onReg();
            this.onView();
        }
    },

    onDelete: function () {
        var me = this;
        var grid = me.getView().down('#grid_01');
        if (!grid) return;
        var store = grid.getStore();
        if (!store) return;

        var selected = store.queryBy(function (r) {
            return r.get('SELECT_FLAG') === true;
        });
        var count = selected && selected.getCount ? selected.getCount() : selected.length || 0;

        if (count === 0) {
            Ext.Msg.alert('정보', '삭제할 항목을 선택하세요.');
            return;
        }

        selected.each(function (r) {
            // r.set('FACTORY_CODE' = gFactoryCode),
            // r.set('EMPLOYEE_NO' = rec.get('EMPLOYEE_NO') ),
            r.set('KT_DATE', me.getView().down('#KT_DATE').getValue());
            r.set('IRU', 'D');
        });

        Ext.MessageBox.confirm('확인', '정말 삭제하시겠습니까?', function (btn) {
            if (btn === 'yes') {
                store.sync({
                    success: function () {
                        Ext.Msg.alert('정보', '삭제되었습니다.');
                        store.reload();
                    },
                });
            }
        });
    },

    // 근무조 그리드
    onRenderer_workteam: function (value, meta, rec) {
        var store = this.getViewModel().getStore('storeCombo_workteam');
        var record = store.findRecord('WG_CODE', value);
        if (record) {
            value = record.get('WG_NAME');
        }
        if (value == null || value == 'null') {
            value = '';
        }
        return value;
    },
    onRenderer_storeCombo_01: function (value, meta, rec) {
        var me = this;

        var store = this.getViewModel().getStore('cboStore_CHUL_GBN1');
        var record = store.findRecord('CODE_ID2', value);
        if (record) {
            value = record.get('CODE_NAME_FULL');
        }

        if (value == null || value == 'null') {
            value = '';
        }
        return value;
    },
});

```

→ VIEW

```javascript
/*******************************************************************************
 * 프로그램명 : 인사급여>근태관리>근무조별 일근태등록
 * 파 일 명 : WHR314_CT.js
 * 작 성 자 : 안재경
 ******************************************************************************/

Ext.define('iPlusERP.controller.HR.WHR300.WHR314_CT', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.WHR314_CT',

    init: function () {
        this.control({
            'WHR314_VW textfield': {
                specialkey: this.onKeyPress,
            },
        });

        this.onInit();
    },

    // 근무조 콤보
    onSetCombo_workteam: function () {
        var store = this.getViewModel().getStore('storeCombo_workteam');
        store.load({
            params: {
                FACTORY_CODE: gFactoryCode,
            },
            callback: function (records, operation, success) {
                if (success) {
                }
            },
        });
    },
    //출근구분 콤보
    onSetcombo_ChulGbn: function () {
        var store = this.getViewModel().getStore('cboStore_CHUL_GBN1');
        var me = this;

        store.load({
            params: {
                CODE_ID1: '256',
            },
            callback: function (records, operation, success) {
                if (success) {
                    me.onView();
                }
            },
        });
    },

    onInit: function () {
        var me = this;

        me.onSetCombo_workteam(); // 근무조코드
        me.onSetcombo_ChulGbn(); // 근무형태
        me.onView();
    },

    onView: function () {
        var me = this;
        var store = this.getViewModel().getStore('store_01');

        store.load({
            params: {
                FACTORY_CODE: gFactoryCode,
                KT_DATE: Ext.util.Format.date(me.getView().down('#KT_DATE').getValue(), 'Ymd'),
                WORK_TEAM: me.getView().down('#cbo_workteam').getValue() || '',
                DEPARTMENT_NAME: me.getView().down('#tf_dept').getValue() || '',
                EMPLOYEE_NAME: me.getView().down('#tf_emp').getValue() || '',
            },
            callback: function (records, op, success) {
                if (success) {
                    Ext.each(records, function (rec) {
                        if (rec.get('OVER_TIME') < 0) {
                            rec.set('OVER_TIME', '');
                        }
                    });
                }
            },
        });
    },

    /* 
    kt:  20250915
    null
    result:  null
    
    */

    onReg: function () {
        var me = this;
        var grid = me.getView().down('grid');
        var store = grid.getStore();
        var RegCheck = false;

        // var modifiedRecords = store.getModifiedRecords(); //수정여부 확인
        // var removedRecords = store.getRemovedRecords(); //삭제여부 확인
        // if (modifiedRecords.length == 0 && removedRecords.length == 0) {
        //     Ext.Msg.alert('알림', '변경된 내용이 없습니다.');
        //     return;
        // }

        store.each(function (record) {
            if (record.get('SELECT_FLAG') === true) {
                RegCheck = true;
            }
        });
        if (!RegCheck) {
            showToast('알림', '저장할 항목을 선택해주세요.');
            return;
        }

        for (var i = 0; i < store.getCount(); i++) {
            var rec = store.getAt(i);
            if (rec.get('SELECT_FLAG') === true) {
                rec.set('FACTORY_CODE', gFactoryCode);
                // rec.set('EMPLOYEE_NO', me.getView().lookup('EMPLOYEE_NO').getValue());
                // rec.set('WG_CODE', me.getView().lookup('WG_CODE').getValue());
                rec.set('OPMAN_CODE', gUserId);
                //rec.set('KT_DATE', me.getView().lookup('KT_DATE').getValue());
                rec.set('IRU', 'IU');
            } else {
                rec.set('SELECT_FLAG', false);
                continue;
            }
        }

        store.sync({
            success: function () {
                showToast('알림', '저장 하였습니다.');
            },
            callback: function () {
                me.onView();
            },
        });
    },

    OnDelete: function () {},

    onKeyPress: function (textfield, event, options) {
        var me = this;
        if (event.getKey() == event.ENTER) {
            this.onView();
        }
    },

    // 근무조 그리드
    onRenderer_workteam: function (value, meta, rec) {
        var store = this.getViewModel().getStore('storeCombo_workteam');
        var record = store.findRecord('WG_CODE', value);
        if (record) {
            value = record.get('WG_NAME');
        }
        if (value == null || value == 'null') {
            value = '';
        }
        return value;
    },
    onRenderer_storeCombo_01: function (value, meta, rec) {
        var me = this;

        var store = this.getViewModel().getStore('cboStore_CHUL_GBN1');
        var record = store.findRecord('CODE_ID2', value);
        if (record) {
            value = record.get('CODE_NAME_FULL');
        }

        if (value == null || value == 'null') {
            value = '';
        }
        return value;
    },
});

```

→ CT

```javascript
Ext.define('iPlusERP.store.HR.WHR300.WHR314_ST', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.WHR314_VM',

    stores: {
        store_01: {
            fields: [
                { name: 'SELECT_FLAG', type: 'bool' },
                // { name: 'KT_DATE', type: 'String' },
            ],
            autoLoad: false,
            proxy: {
                type: 'ajax',
                api: {
                    create: ipAddr + '/com/HR/WHR300/jvWHR314_01_IUD',
                    update: ipAddr + '/com/HR/WHR300/jvWHR314_01_IUD',
                    destroy: ipAddr + '/com/HR/WHR300/jvWHR314_01_IUD',
                    read: ipAddr + '/com/HR/WHR300/jvWHR314_01_LIST',
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
                listeners: {
                    exception: function (proxy, response, operation) {
                        var obj = Ext.JSON.decode(response.responseText);
                        Ext.MessageBox.show({
                            title: '에러',
                            msg: obj.message,
                            icon: Ext.MessageBox.ERROR,
                            buttons: Ext.Msg.OK,
                        });
                    },
                },
            },
        },

        //근무조설정
        storeCombo_workteam: {
            autoLoad: false,
            proxy: {
                type: 'ajax',
                api: {
                    read: ipAddr + '/com/common/jvStoreCombo_TIN310',
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

        //근무형태 선택
        cboStore_CHUL_GBN1: {
            fields: [{ name: 'CODE_ID2', type: 'string' }],
            autoLoad: false,
            proxy: {
                type: 'ajax',
                url: ipAddr + '/com/common/jvStoreFunction_GetTCO101',
                reader: {
                    type: 'json',
                    rootProperty: 'data',
                },
            },
        },
    },
});

```

→ ST

```java
package com.HR.WHR300;

import java.sql.*;
import org.json.simple.JSONObject;
import org.json.simple.JSONArray;
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.GenericServlet;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebServlet;

@WebServlet("/com/HR/WHR300/jvWHR314_01_LIST")
public class jvWHR314_01_LIST extends GenericServlet {
	private static final long serialVersionUID = 1L;

	@Override
	public void service(ServletRequest request, ServletResponse response)
			throws ServletException, IOException {
			Connection conn = null;
			Statement stmt = null;
			ResultSet rs = null;

			JSONArray itemList = new JSONArray();
			
		try {	
			
			ServletContext sc = this.getServletContext();
			
			Class.forName(sc.getInitParameter("driver")).newInstance();
			conn = DriverManager.getConnection(
					sc.getInitParameter("url"), //JDBC URL
					sc.getInitParameter("username"),	// DBMS 사용자 아이디
					sc.getInitParameter("password"));	// DBMS 사용자 암호
			stmt = conn.createStatement();
			
			response.setContentType("text/html; charset=UTF-8");
			
			request.setCharacterEncoding("UTF-8"); 

			String FACTORY_CODE = request.getParameter("FACTORY_CODE");
			String KT_DATE = request.getParameter("KT_DATE");
			String WORK_TEAM = request.getParameter("WORK_TEAM");
			String DEPARTMENT_NAME = request.getParameter("DEPARTMENT_NAME");
			String EMPLOYEE_NAME = request.getParameter("EMPLOYEE_NAME");
//			String DEPTNM = request.getParameter("DEPTNM");
//			String EMPLOYEENM = request.getParameter("EMPLOYEENM");
//			String DEF_WG_ATTEND_GBN = request.getParameter("DEF_WG_ATTEND_GBN");
	
			String sql = "EXEC SP_WHR314_01_LIST "
						+ "\r\n" + "'" + FACTORY_CODE + "'"
						+ "\r\n" + ",'" + KT_DATE + "'"
						+ "\r\n" + ",'" + WORK_TEAM + "'"
						+ "\r\n" + ",'" + DEPARTMENT_NAME + "'"
						+ "\r\n" + ",'" + EMPLOYEE_NAME + "'"
						;
					
//						+ "\r\n" + ",'" + DEF_WG_ATTEND_GBN + "'" 
						

			rs = stmt.executeQuery(sql);
			
			ResultSetMetaData rm = rs.getMetaData();
			
			System.out.println(sql);
			
			while(rs.next())
			{
				JSONObject tempJson = new JSONObject();
				for(int nCount=1 ; nCount <=  rm.getColumnCount() ; nCount++)
				{
					tempJson.put(rm.getColumnName(nCount), rs.getString(rm.getColumnName(nCount)));
				}
				itemList.add(tempJson);
			}
			
		} catch (Exception e) {
			throw new ServletException(e);
			
		} finally {
			try {if (rs != null) rs.close();} catch(Exception e) {}
			try {if (stmt != null) stmt.close();} catch(Exception e) {}
			try {if (conn != null) conn.close();} catch(Exception e) {}
		}
		PrintWriter out = response.getWriter();
		out.print(itemList);
		out.flush();

	}
}

```

→ LIST PRC

```java
package com.HR.WHR300;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Iterator;
import java.util.Locale;

import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.json.simple.parser.JSONParser;

@WebServlet("/com/HR/WHR300/jvWHR314_01_IUD")
public class jvWHR314_01_IUD extends HttpServlet {
	private static final long serialVersionUID = 1L;

	@Override
	public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {

		
		Connection conn = null;
		PreparedStatement stmt = null;
		ResultSet rs = null;

		String query = "";
		String data;
		
		String strReturn 	=	"";
		String strMsg		=	"";
		String strSuccess	=	"true";
		
		String FACTORY_CODE;
		String OPMAN_CODE;
		String MAX_DS_CODE;
		String IRU;

		try {
			ServletContext sc = this.getServletContext();

			Class.forName(sc.getInitParameter("driver")).newInstance();
			conn = DriverManager.getConnection(sc.getInitParameter("url"), // JDBC
																			// URL
			sc.getInitParameter("username"), // DBMS 사용자 아이디
			sc.getInitParameter("password")); // DBMS 사용자 암호

			request.setCharacterEncoding("UTF-8"); // UTF-8 로 인코딩해서 가져온다.
			
			conn.setAutoCommit(false); 
			
			data = (String) request.getParameter("data");
			
			FACTORY_CODE = (String) request.getParameter("FACTORY_CODE");
			OPMAN_CODE = (String) request.getParameter("OPMAN_CODE");
			MAX_DS_CODE= (String) request.getParameter("MAX_DS_CODE");
			IRU = (String) request.getParameter("IRU");
			
			if (data != null) {
				JSONArray array = null;
				if (data.substring(0, 1).equals("{")) {
					JSONParser parser = new JSONParser();
					Object object = parser.parse(data);
					JSONObject jsonObject = (JSONObject) object;
					array = new JSONArray();
					array.add(jsonObject);
				} else if (data.substring(0, 1).equals("[")) {
					Object obj = JSONValue.parse(data);
					array = (JSONArray) obj;
				}

				Iterator<JSONObject> iterator = array.iterator();

				while (iterator.hasNext()) {

					JSONObject jsonobj = (JSONObject) iterator.next();
					if(IRU.equals("IU")){
						query = " EXEC SP_WHR314_01_IUD "
								+ "\r\n" + "'" +  FACTORY_CODE + "'" 
								+ "\r\n" + ",'" +  (String)jsonobj.get("EMPLOYEE_NO").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_ATTEND_GBN").toString().replace("'", "''") + "'" 
								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_CODE").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_PRDFROM").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_PRDTO").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_PRDFROM2").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_PRDTO2").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ","  + jsonobj.get("WG_LTIME").toString().replace(",", "") + "" 
								+ "\r\n" + ",'" +  (String)jsonobj.get("KT_DATE").toString().replace("'", "''") + "'" 
								+ "\r\n" + ",'" +  OPMAN_CODE + "'" 
								+ "\r\n" + ",'" +  IRU + "'" ;
						
//						System.out.println(query);
//						stmt = conn.prepareStatement(query);
//						stmt.executeUpdate();
						
						String nParam1 = "";
						String nParam2 = "";
	
						int DsCnt = Integer.parseInt(MAX_DS_CODE);
						
						for(int rcnt = 1 ; rcnt<=DsCnt ;rcnt++){
							nParam1 = "" + rcnt ;
							nParam1 = "0" + nParam1;
							nParam1 = nParam1.substring(nParam1.length()-2, nParam1.length());
							nParam2 = "DS" + nParam1;
							
							if(jsonobj.get(nParam2) != null ) {
								query += "' '";
								query += "EXEC SP_WHR314_02_IUD ";
								query += "'" + FACTORY_CODE +	"'";
								query += ",'" + (String)jsonobj.get("EMPLOYEE_NO").toString().replace("'", "''") +	"'";
								query += ",'" + (String)jsonobj.get("DU_YMD").toString().replace("'", "''") +	"'";
								query += ",'" + nParam1 + "'" ;
								query += "," + jsonobj.get(nParam2) + "";
								query += ",'" + OPMAN_CODE 	+ "'" ;							
								query += ",'" + IRU +	"'";

//								System.out.println(query);
//								stmt = null;
//								stmt = conn.prepareStatement(query);
//								stmt.executeUpdate();
								
								query += "' '";
								query += "EXEC SP_WHR314_03_IUD ";
								query += "'" + FACTORY_CODE +	"'";
								query += ",'" + (String)jsonobj.get("EMPLOYEE_NO").toString().replace("'", "''") +	"'";
								query += ",'" + (String)jsonobj.get("BASE_NAME").toString().replace("'", "''") +	"'";
								query += ",'" + nParam1 + "'" ;
								query += ",'" + (String)jsonobj.get("DU_YMD").toString().replace("'", "''") +	"'";
								query += "," + jsonobj.get(nParam2) + "";
								query += ",'" + OPMAN_CODE 	+ "'" ;							
								query += ",'" + IRU +	"'";
	
//								System.out.println(query);
//								stmt = null;
//								stmt = conn.prepareStatement(query);
//								stmt.executeUpdate();
								
//								query += "' '";
//								query += "EXEC SP_WHR314_04_IUD ";
//								query += "'" + FACTORY_CODE +	"'";
//								query += ",'" + (String)jsonobj.get("DU_YMD").toString().replace("'", "''") +	"'";
//								query += ",'" + (String)jsonobj.get("EMPLOYEE_NO").toString().replace("'", "''") +	"'";
//								query += ",'" + nParam1 + "'" ;
//								query += ",'" + (String)jsonobj.get("BASE_NAME").toString().replace("'", "''") +	"'";
//								query += "," + jsonobj.get(nParam2) + "";
//								query += ",'" + OPMAN_CODE 	+ "'" ;							
//								query += ",'" + IRU +	"'";
	
//								System.out.println(query);
//								stmt = null;
//								stmt = conn.prepareStatement(query);
//								stmt.executeUpdate();
												
							}
						}
						stmt = null;
						stmt = conn.prepareStatement(query);
						stmt.executeUpdate();
					}
					else{

//						query = " EXEC SP_WHR314_01_IUD "
//								+ "\r\n" + "'" +  FACTORY_CODE + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("EMPLOYEE_NO").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("DU_YMD").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_ATTEND_GBN").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_CODE").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_PRDFROM").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_PRDTO").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_PRDFROM2").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ",'" +  (String)jsonobj.get("WG_PRDTO2").toString().replace("'", "''") + "'" 
//								+ "\r\n" + ","  + jsonobj.get("WG_LTIME").toString().replace(",", "") + "" 
//								+ "\r\n" + ",'" +  OPMAN_CODE + "'" 
//								+ "\r\n" + ",'" +  IRU + "'" ;
						
						query = " EXEC SP_WHR314_01_IUD "
								+ "\r\n" + "'" +  FACTORY_CODE + "'" 
								+ "\r\n" + ",'" +  (String)jsonobj.get("EMPLOYEE_NO").toString().replace("'", "''") + "'" 
								+ "\r\n" + ",'" +  (String)jsonobj.get("DU_YMD").toString().replace("'", "''") + "'" 
								+ "\r\n" + ",''" 
								+ "\r\n" + ",''" 
								+ "\r\n" + ",''" 
								+ "\r\n" + ",''" 
								+ "\r\n" + ",''" 
								+ "\r\n" + ",''" 
								+ "\r\n" + ",0"   
								+ "\r\n" + ",'" +  OPMAN_CODE + "'" 
								+ "\r\n" + ",'" +  IRU + "'" ;
						
//						System.out.println(query);
						
						stmt = conn.prepareStatement(query);
						stmt.executeUpdate();
					}
					query = " EXEC SP_EIS002_SAVE "
							+ "\r\n" + "'" +  FACTORY_CODE + "'" 
							+ "\r\n" + ",'" +  (String)jsonobj.get("EMPLOYEE_NO").toString().replace("'", "''") + "'" 
							+ "\r\n" + ",'" +  (String)jsonobj.get("DU_YMD").toString().replace("'", "''") + "'" 
							+ "\r\n" + ",'" +  OPMAN_CODE + "'" 
							+ "\r\n" + ",'" +  IRU + "'" ;
					
//					System.out.println(query);
					stmt = conn.prepareStatement(query);
					stmt.executeUpdate();
				
				}
			}
			
			conn.commit(); 
			
		} catch (Exception e) {
			
			try {
				if(conn != null){
					conn.rollback();
				}
			} 
			catch (Exception exConn) {
			}
			
			
			strSuccess = "false";
			strMsg =  e.toString() ;
			if(strMsg.contains(":") == true){
				String string[] = strMsg.split(":");
				strMsg = string[1];
			}

		} finally {
			try {if(rs != null){rs.close();}} catch (Exception exRs) {}
			try {if(stmt != null){stmt.close();}} catch (Exception exStmt) {}
			try {if(conn != null){conn.close();}} catch (Exception exConn) {}
		}
		
		response.setContentType("text/html; charset=EUC-KR");
		strMsg = strMsg.replace("'", " ");
		strReturn = "{'success':" + strSuccess + ",'data':'','message':'" + strMsg + "'}";
		
		PrintWriter out = response.getWriter();
		out.print(strReturn);
		out.flush();
		out.close();
	}
}

```

→ IUD PRC

```sql
USE [iPlusERP_IPACK_DEV]
GO
/****** Object:  StoredProcedure [dbo].[SP_WHR314_01_IUD]    Script Date: 2025-09-19 오전 9:34:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROC [dbo].[SP_WHR314_01_IUD]
(
       @FACTORY_CODE	varchar(6)
     , @EMPLOYEE_NO		varchar(10)
     --, @DU_YMD			varchar(8)
     --, @WG_ATTEND_GBN	varchar(6)
     , @WG_CODE			varchar(6)
	 , @KT_DATE			VARCHAR(8)
     --, @WG_PRDFROM		varchar(8)
     --, @WG_PRDTO		varchar(8)
     --, @WG_PRDFROM2		varchar(8)
     --, @WG_PRDTO2		varchar(8)
     --, @WG_LTIME		int
     , @OPMAN_CODE		varchar(10)
	 , @IRU				varchar(2)
)
  
AS 
  
BEGIN 

	DECLARE @OPTIME	VARCHAR(12) 
	SET @OPTIME = CONVERT(CHAR(8),GETDATE(),112) + REPLACE(CONVERT(CHAR(5),GETDATE(),114),':','')
	
	IF @IRU = 'IU'
		BEGIN 
		
			UPDATE TIN313 
			SET 
				WG_ATTEND_GBN	= @WG_CODE
			   --,WG_CODE			= @WG_CODE
			   --,WG_PRDFROM		= @WG_PRDFROM
			   --,WG_PRDTO		= @WG_PRDTO
			   --,WG_PRDFROM2		= @WG_PRDFROM2
			   --,WG_PRDTO2		= @WG_PRDTO2
			   --,WG_LTIME		= @WG_LTIME
			   ,WG_PRDFROM		= @KT_DATE
			   ,OPMAN_CODE		= @OPMAN_CODE
			   ,OPTIME			= @OPTIME
			WHERE	FACTORY_CODE	=	@FACTORY_CODE
			AND		EMPLOYEE_NO		=	@EMPLOYEE_NO
			AND		DU_YMD			=	@KT_DATE

			IF	@@ROWCOUNT	=	0 
			BEGIN

				INSERT INTO TIN313
							(
								 FACTORY_CODE
								,EMPLOYEE_NO
								,DU_YMD
								,WG_ATTEND_GBN
								--,WG_CODE
								--,WG_PRDFROM
								--,WG_PRDTO
								--,WG_PRDFROM2
								--,WG_PRDTO2
								--,WG_LTIME
								,OPMAN_CODE
								,OPTIME
							)
						VALUES
							(
								 @FACTORY_CODE
								,@EMPLOYEE_NO
								,@KT_DATE
								,@WG_CODE
								--,@WG_CODE
								--,@WG_PRDFROM
								--,@WG_PRDTO
								--,@WG_PRDFROM2
								--,@WG_PRDTO2
								--,@WG_LTIME
								,@OPMAN_CODE
								,@OPTIME
							)

			END

		END
		--ELSE IF @IRU = 'D'
		--BEGIN	
		--	DELETE FROM TIN313
		--	WHERE	FACTORY_CODE	=		@FACTORY_CODE
		--	AND EMPLOYEE_NO			=		@EMPLOYEE_NO
		--	AND DU_YMD				=		@DU_YMD

		--	DELETE FROM TIN313D
		--	WHERE	FACTORY_CODE	=		@FACTORY_CODE
		--	AND EMPLOYEE_NO			=		@EMPLOYEE_NO
		--	AND DU_YMD				=		@DU_YMD

		--END
END


```

IUD PROCEDURE


```sql
USE [iPlusERP_IPACK_DEV]
GO
/****** Object:  StoredProcedure [dbo].[SP_WHR314_01_LIST]    Script Date: 2025-09-22 오전 9:00:40 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER OFF
GO

ALTER PROCEDURE [dbo].[SP_WHR314_01_LIST]          
(               
    @FACTORY_CODE       VARCHAR(6),
    @KT_DATE            CHAR(8), 
    @WORK_TEAM          VARCHAR(8),
    @DEPARTMENT_NAME    VARCHAR(20),
    @EMPLOYEE_NAME      VARCHAR(20)
)
-- SP_WHR314_01_LIST '000001', '20250917', '', '', ''
AS  
BEGIN              
    SET NOCOUNT ON;     
	BEGIN

	WITH 
    Event_CTE AS (
        -- 1. 당일(@KT_DATE)의 출입기록을 사번별 순서대로 가져옴
        --    NREADERIDN 으로 '입실' / '퇴실' 구분
        SELECT 
              ROW_NUMBER() OVER (PARTITION BY EMPLOYEE_NO ORDER BY KT_DATETIME) AS rn
            , KT_DATETIME AS IO_DATETIME
            , CASE 
                WHEN NREADERIDN IN (546839596, 546839166) THEN '입실'
                WHEN NREADERIDN IN (546839433, 546839434) THEN '퇴실'
                ELSE '기타'
              END AS IO_NAME
            , EMPLOYEE_NO
        FROM TIN334
        
        WHERE CONVERT(CHAR(8), KT_DATETIME, 112) = @KT_DATE
        AND NREADERIDN IN (546839166, 546839433, 546839434, 546839596)
    ),

    Pair_CTE AS (
        -- 2. 퇴실 → 바로 다음 입실을 짝지어서 외출시간(분)을 계산
        SELECT 
              O.EMPLOYEE_NO
            , O.IO_DATETIME AS OUT_TIME
            , I.IO_DATETIME AS IN_TIME
            , DATEDIFF(MINUTE, O.IO_DATETIME, I.IO_DATETIME) AS DURATION_TIME
        FROM Event_CTE O

            LEFT JOIN Event_CTE I
            ON O.EMPLOYEE_NO = I.EMPLOYEE_NO
            AND I.rn = O.rn + 1

        WHERE O.IO_NAME = '퇴실'
        AND I.IO_NAME = '입실'
    ),

    Outsum AS (
        -- 3. 사원별 총 외출시간 합계(분)
        SELECT EMPLOYEE_NO,
               SUM(DURATION_TIME) AS TOTAL_OUT_MINUTES
        FROM Pair_CTE
        GROUP BY EMPLOYEE_NO
    ),

    InOutsum AS (
        -- 4. 사원별 최초 입실, 최종 퇴실 계산
        SELECT EMPLOYEE_NO,
               MIN(CASE WHEN IO_NAME = '입실' THEN IO_DATETIME END) AS FIRST_IN,
               MAX(CASE WHEN IO_NAME = '퇴실' THEN IO_DATETIME END) AS LAST_OUT
        FROM Event_CTE
        GROUP BY EMPLOYEE_NO
    ),

    ValidInOut AS (
        -- 5. 유효한 출퇴근 판별
        --    (최초 입실 < 최종 퇴실일 때만 출근/퇴근 인정) 나중에 쓸일이 있을것같음,
        SELECT EMPLOYEE_NO,
               CASE 
                    WHEN LAST_OUT IS NOT NULL AND FIRST_IN < LAST_OUT 
                         THEN FIRST_IN 
                    ELSE NULL 
               END AS VALID_FIRST_IN,
               CASE 
                    WHEN LAST_OUT IS NOT NULL AND FIRST_IN < LAST_OUT 
                         THEN LAST_OUT 
                    ELSE NULL 
               END AS VALID_LAST_OUT
        FROM InOutsum
    ),

	WGInfo AS (
		SELECT 
			  EMPLOYEE_NO
			, WG_CODE
			, WG_ATTEND_GBN
			--, CAST((CAST(WG_PRDTO AS INT) - CAST(WG_PRDFROM AS INT)) AS FLOAT) / 100.0 AS BASIC_TIME

			, CASE  -- 계산식 테스트용 삭제예정
			  WHEN WG_ATTEND_GBN = '001' THEN 10.00
			  ELSE 0.00 END AS BASIC_TIME

			, WG_PRDFROM
			, WG_PRDTO
			, WG_LTIME
			, DU_YMD
			, ROW_NUMBER() OVER (
				PARTITION BY EMPLOYEE_NO, WG_CODE 
				ORDER BY 
					CASE WHEN DU_YMD = @KT_DATE THEN 0 ELSE 1 END,
					CASE WHEN DU_YMD IS NOT NULL THEN 0 ELSE 1 END,
					WG_PRDFROM DESC
			) AS rn
		FROM TIN313
	)

    -- 최종 결과 조회
    SELECT DISTINCT
          A.FACTORY_CODE
		, A.EMPLOYEE_NO
        , A.BASE_NAME
		, B.BASIC_TIME
		, E.WG_CODE
        , C.WG_NAME                  AS WORK_TEAM
		, B.WG_ATTEND_GBN            AS CODE_ID2
		, B.DU_YMD					 AS DU_YMD
        , C.DEF_FROM_TIME            AS WORK_START_TIME
        , C.DEF_TO_TIME              AS WORK_END_TIME
		, D.Department_Name			 AS DEPARTMENT_NAME
        , I.FIRST_IN                 AS FIRST_IN
        , I.LAST_OUT                 AS LAST_OUT

        , ROUND (CAST(DATEDIFF(MINUTE, I.FIRST_IN, I.LAST_OUT) AS FLOAT) / 60.0, 2)				  AS WORK_TIME
        , ROUND (CAST( O.TOTAL_OUT_MINUTES AS FLOAT ) / 60.0 ,2 )								  AS OUT_MINUTES
		, ROUND (CAST(DATEDIFF(MINUTE, I.FIRST_IN, I.LAST_OUT) AS FLOAT) / 60.0, 2) - BASIC_TIME  AS OVER_TIME
		--, ROUND (CAST(DATEDIFF(MINUTE, B.WG_PRDTO, I.LAST_OUT) AS FLOAT) / 60.0, 2)				  AS EARLY_TIME
		--, ROUND (CAST(DATEDIFF(MINUTE, B.WG_PRDFROM, I.FIRST_IN ) AS FLOAT) / 60.0, 2)			  AS LATE_TIME  
		
		--, CASE
		--	  WHEN BASIC_TIME < ROUND(CAST(DATEDIFF(MINUTE, B.WG_PRDTO, I.LAST_OUT) AS FLOAT) / 60.0, 2)
		--	  THEN ROUND(CAST(DATEDIFF(MINUTE, B.WG_PRDTO, I.LAST_OUT) AS FLOAT) / 60.0, 2) - BASIC_TIME
		--	  ELSE 0.00 END AS OVER_TIME

		, CASE
			  WHEN B.WG_PRDTO > I.LAST_OUT
			  THEN ROUND(CAST(DATEDIFF(MINUTE, B.WG_PRDTO, I.LAST_OUT) AS FLOAT) / 60.0, 2)
			  ELSE 0.00 END AS EARLY_TIME

		, CASE
			  WHEN B.WG_PRDFROM < I.FIRST_IN
			  THEN ROUND (CAST(DATEDIFF(MINUTE, B.WG_PRDFROM, I.FIRST_IN ) AS FLOAT) / 60.0, 2)
			  ELSE 0.00 END AS LATE_TIME

		, CASE 
			  WHEN E.WG_CODE = '002' THEN 7.00  
			  ELSE 0.00 END AS NIGHT_TIME

		, CASE 
			  WHEN E.WG_CODE = '002' THEN 1.00   
			  ELSE 0.00 END AS NIGHT_ALLOW 

    FROM TIN114 A

        LEFT JOIN TIN122 D 
            ON A.DEPARTMENT_CODE = D.Department_Code

        LEFT JOIN TIN312 E 
            ON A.EMPLOYEE_NO = E.EMPLOYEE_NO

        LEFT JOIN TIN310 C 
            ON E.WG_CODE = C.WG_CODE

		--LEFT JOIN TIN313 B 
		--  ON A.EMPLOYEE_NO = B.EMPLOYEE_NO
		--	AND E.WG_CODE = B.WG_CODE

        --LEFT JOIN ValidInOut V 
        --  ON A.EMPLOYEE_NO = V.EMPLOYEE_NO

		LEFT JOIN WGInfo B
			ON A.EMPLOYEE_NO = B.EMPLOYEE_NO
			AND E.WG_CODE = B.WG_CODE
			AND B.RN=1

        LEFT JOIN InOutsum I 
            ON A.EMPLOYEE_NO = I.EMPLOYEE_NO

        LEFT JOIN Outsum O 
            ON A.EMPLOYEE_NO = O.EMPLOYEE_NO

		LEFT JOIN TIN334 F
			ON A.EMPLOYEE_NO = F.EMPLOYEE_NO

    WHERE ISNULL(A.RETIRE_DATE,'') = ''
      AND ISNULL(A.REAL_USER_GBN,'0') = '1'
	  AND CONVERT(VARCHAR(8), F.KT_DATETIME, 112) = @KT_DATE
    ORDER BY A.EMPLOYEE_NO;

	END
END


```

→ LIST

```sql
USE [iPlusERP_IPACK_DEV]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROC [dbo].[SP_WHR314_01_DS_IUD]
(
     @FACTORY_CODE    VARCHAR(6),
     @EMPLOYEE_NO     VARCHAR(10),
     @KT_DATE         VARCHAR(8),
     @BASIC_TIME      NUMERIC(10,2),
     @LATE_TIME       NUMERIC(10,2),
     @EARLY_TIME      NUMERIC(10,2),
     @OVER_TIME       NUMERIC(10,2),
     @NIGHT_TIME      NUMERIC(10,2),
     @NIGHT_ALLOW     NUMERIC(10,2),
     @OPMAN_CODE      VARCHAR(10),
     @IRU             VARCHAR(2)   -- 'IU' or 'D'
)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @OPTIME VARCHAR(12)
    SET @OPTIME = CONVERT(CHAR(8), GETDATE(), 112) + REPLACE(CONVERT(CHAR(5), GETDATE(), 114), ':', '')

    IF @IRU = 'IU'
    BEGIN
        -- 처리 대상 코드들
        DECLARE @Codes TABLE (DS_CODE VARCHAR(2), DS_VALUE NUMERIC(10,2))
        INSERT INTO @Codes VALUES
            ('02', @BASIC_TIME),
            ('10', @LATE_TIME),
            ('12', @EARLY_TIME),
            ('33', @OVER_TIME),
            ('04', @NIGHT_TIME),
            ('34', @NIGHT_ALLOW)

        -- UPSERT (Update or Insert)
        MERGE DS_TIME AS target
        USING (
            SELECT DS_CODE, DS_VALUE
            FROM @Codes
        ) AS source
        ON target.FACTORY_CODE = @FACTORY_CODE
           AND target.EMPLOYEE_NO = @EMPLOYEE_NO
           AND target.DU_YMD = @KT_DATE
           AND target.DS_CODE = source.DS_CODE
        WHEN MATCHED THEN
            UPDATE SET 
                DS_VALUE = source.DS_VALUE,
                OPMAN_CODE = @OPMAN_CODE,
                OPTIME = @OPTIME
        WHEN NOT MATCHED THEN
            INSERT (FACTORY_CODE, EMPLOYEE_NO, DU_YMD, DS_CODE, DS_VALUE, OPMAN_CODE, OPTIME)
            VALUES (@FACTORY_CODE, @EMPLOYEE_NO, @KT_DATE, source.DS_CODE, source.DS_VALUE, @OPMAN_CODE, @OPTIME);
    END

    ELSE IF @IRU = 'D'
    BEGIN
        DELETE FROM DS_TIME
        WHERE FACTORY_CODE = @FACTORY_CODE
          AND EMPLOYEE_NO = @EMPLOYEE_NO
          AND DU_YMD = @KT_DATE
          AND DS_CODE IN ('02', '10', '12', '33', '04', '34')
    END
END

```

EXEC SP_WHR314_01_LIST
'000001'
,'20250916'
,''
,''
,''

메시지 242, 수준 16, 상태 3, 프로시저 SP_WHR314_01_LIST, 줄 16 [배치 시작 줄 4]
varchar 데이터 형식을 datetime 데이터 형식으로 변환하는 중 값 범위를 벗어났습니다.
경고: 집계 또는 다른 SET 작업에 의해 Null 값이 제거되었습니다.

완료 시간: 2025-09-22T10:52:12.1200767+09:00

---


```java

USE [iPlusERP_IPACK_DEV]
GO
/****** Object:  StoredProcedure [dbo].[SP_WHR314_01_LIST]    Script Date: 2025-09-30 오전 8:55:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER OFF
GO

ALTER PROCEDURE [dbo].[SP_WHR314_01_LIST]          
(               
    @FACTORY_CODE       VARCHAR(8),
    @KT_DATE            VARCHAR(20), 
    @DEPARTMENT_NAME    VARCHAR(20),
	@WORK_TEAM          VARCHAR(8),
    @EMPLOYEE_NAME      VARCHAR(20)
)
-- SP_WHR314_01_LIST '000001', '20250917', '', '', ''
AS  
BEGIN              
    SET NOCOUNT ON;     
	BEGIN

	WITH 
    Event_CTE AS (
        -- 1. 당일(@KT_DATE)의 출입기록을 사번별 순서대로 가져옴
        --    NREADERIDN 으로 '입실' / '퇴실' 구분
        SELECT 
              ROW_NUMBER() OVER (PARTITION BY EMPLOYEE_NO ORDER BY KT_DATETIME) AS rn
            , KT_DATETIME AS IO_DATETIME
            , CASE 
                WHEN NREADERIDN IN (546839596, 546839166) THEN '입실'
                WHEN NREADERIDN IN (546839433, 546839434) THEN '퇴실'
                ELSE '기타'
              END AS IO_NAME
            , EMPLOYEE_NO
        FROM TIN334
        
        WHERE CONVERT(CHAR(8), KT_DATETIME, 112) = @KT_DATE
        AND NREADERIDN IN (546839166, 546839433, 546839434, 546839596)
    ),

    Pair_CTE AS (
        -- 2. 퇴실 → 바로 다음 입실을 짝지어서 외출시간(분)을 계산
        SELECT 
              O.EMPLOYEE_NO
            , O.IO_DATETIME AS OUT_TIME
            , I.IO_DATETIME AS IN_TIME
            , DATEDIFF(MINUTE, O.IO_DATETIME, I.IO_DATETIME) AS DURATION_TIME
        FROM Event_CTE O

            LEFT JOIN Event_CTE I
            ON O.EMPLOYEE_NO = I.EMPLOYEE_NO
            AND I.rn = O.rn + 1

        WHERE O.IO_NAME = '퇴실'
        AND I.IO_NAME = '입실'
    ),

    Outsum AS (
        -- 3. 사원별 총 외출시간 합계(분)
        SELECT EMPLOYEE_NO,
               SUM(DURATION_TIME) AS TOTAL_OUT_MINUTES
        FROM Pair_CTE
        GROUP BY EMPLOYEE_NO
    ),

    InOutsum AS (
        -- 4. 사원별 최초 입실, 최종 퇴실 계산
        SELECT EMPLOYEE_NO,
               MIN(CASE WHEN IO_NAME = '입실' THEN IO_DATETIME END) AS FIRST_IN,
               MAX(CASE WHEN IO_NAME = '퇴실' THEN IO_DATETIME END) AS LAST_OUT
        FROM Event_CTE
        GROUP BY EMPLOYEE_NO
    ),

    ValidInOut AS (
        -- 5. 유효한 출퇴근 판별
        --    (최초 입실 < 최종 퇴실일 때만 출근/퇴근 인정) 나중에 쓸일이 있을것같음,
        SELECT EMPLOYEE_NO,
               CASE 
                    WHEN LAST_OUT IS NOT NULL AND FIRST_IN < LAST_OUT 
                         THEN FIRST_IN 
                    ELSE NULL 
               END AS VALID_FIRST_IN,
               CASE 
                    WHEN LAST_OUT IS NOT NULL AND FIRST_IN < LAST_OUT 
                         THEN LAST_OUT 
                    ELSE NULL 
               END AS VALID_LAST_OUT
        FROM InOutsum
    ),

	WGInfo AS (
		SELECT 
			  EMPLOYEE_NO
			, WG_CODE
			, WG_ATTEND_GBN
			--, CAST((CAST(WG_PRDTO AS INT) - CAST(WG_PRDFROM AS INT)) AS FLOAT) / 100.0 AS BASIC_TIME

			, CASE  -- 근무 기본시간 고정
			  WHEN WG_ATTEND_GBN = '001' THEN 8.00
			  ELSE 0.00 END AS BASIC_TIME

			, WG_PRDFROM
			, WG_PRDTO
			, WG_LTIME
			, DU_YMD
			, ROW_NUMBER() OVER (
				PARTITION BY EMPLOYEE_NO, WG_CODE 
				ORDER BY 
					CASE WHEN DU_YMD = @KT_DATE THEN 0 ELSE 1 END,
					CASE WHEN DU_YMD IS NOT NULL THEN 0 ELSE 1 END,
					WG_PRDFROM DESC
			) AS rn
		FROM TIN313
	)

    -- 최종 결과 조회
    SELECT 
	--DISTINCT
          MAX(A.FACTORY_CODE)
		, MAX(A.EMPLOYEE_NO)
        , A.BASE_NAME
		--, B.BASIC_TIME
		--, RIGHT('00' + LEFT(B.WG_PRDFROM, 2), 2) + ':' + RIGHT(B.WG_PRDFROM, 2) 
		--+ ' ~ ' + 
		--  RIGHT('00' + LEFT(B.WG_PRDTO, 2), 2) + ':' + RIGHT(B.WG_PRDTO, 2) AS BASE_DIS

		 , CONVERT(CHAR(8), MAX(I.FIRST_IN), 8)
			 + ' ~ ' + 
		   CONVERT(CHAR(8), MAX(I.LAST_OUT), 8) AS BASE_DIS

		, MAX(B.WG_CODE)
		--, B.WG_LTIME				 AS OUT_MINUTES
        , STRING_AGG(C.WG_NAME, ',')     AS WORK_TEAM
		, MAX(B.WG_ATTEND_GBN)            AS CODE_ID2
		, STRING_AGG(D.Department_Name, ',') AS DEPARTMENT_NAME
        , RIGHT('0' + CAST(DATEPART(HOUR, MAX(I.FIRST_IN)) AS VARCHAR), 2) +
		  RIGHT('0' + CAST(DATEPART(MINUTE, MAX(I.FIRST_IN)) AS VARCHAR), 2) AS FIRST_IN
		, RIGHT('0' + CAST(DATEPART(HOUR, MAX(I.LAST_OUT)) AS VARCHAR), 2) +
		  RIGHT('0' + CAST(DATEPART(MINUTE, MAX(I.LAST_OUT)) AS VARCHAR), 2) AS LAST_OUT
		, MAX(B.WG_PRDFROM)
		, MAX(B.WG_PRDTO)
        , FORMAT (CAST(DATEDIFF(MINUTE, MAX(I.FIRST_IN), MAX(I.LAST_OUT)) AS FLOAT) / 60.0, 'N2')				  AS WORK_TIME
        , FORMAT (CAST( MAX(O.TOTAL_OUT_MINUTES) AS FLOAT ) / 60.0 ,'N2' )								  AS OUT_MINUTES
		--, ROUND (CAST(DATEDIFF(MINUTE, I.FIRST_IN, I.LAST_OUT) AS FLOAT) / 60.0, 2) - BASIC_TIME	  AS OVER_TIME
		--, ROUND (CAST(DATEDIFF(MINUTE, B.WG_PRDTO, I.LAST_OUT) AS FLOAT) / 60.0, 2)				  AS EARLY_TIME
		--, ROUND (CAST(DATEDIFF(MINUTE, B.WG_PRDFROM, I.FIRST_IN ) AS FLOAT) / 60.0, 2)			  AS LATE_TIME  
		
		--, CASE
		--	  WHEN BASIC_TIME < ROUND(CAST(DATEDIFF(MINUTE, B.WG_PRDTO, I.LAST_OUT) AS FLOAT) / 60.0, 2)
		--	  THEN ROUND(CAST(DATEDIFF(MINUTE, B.WG_PRDTO, I.LAST_OUT) AS FLOAT) / 60.0, 2) - BASIC_TIME
		--	  ELSE 0.00 END AS OVER_TIME

		--, CASE
		--	  WHEN CONVERT(FLOAT, REPLACE(CONVERT(CHAR(5), I.LAST_OUT, 108), ':', ''))
		--			< CAST(B.WG_PRDTO AS FLOAT)
		--	  THEN ROUND(((CAST(LEFT(B.WG_PRDTO, 2) AS FLOAT) * 60 + CAST(RIGHT(B.WG_PRDTO, 2) AS FLOAT)) 
		--			 - (DATEPART(HOUR, I.LAST_OUT) * 60 + DATEPART(MINUTE, I.LAST_OUT))) / 60.0, 2)

		--		ELSE 0
		--	  END AS EARLY_TIME

		--, CASE
		--	  WHEN CONVERT(FLOAT, REPLACE(CONVERT(CHAR(5), I.LAST_OUT, 108), ':', ''))
		--			> CAST(B.WG_PRDTO AS FLOAT)
		--	  THEN  ROUND(((DATEPART(HOUR, I.LAST_OUT) * 60 + DATEPART(MINUTE, I.LAST_OUT))
		--			- (CAST(LEFT(B.WG_PRDTO, 2) AS FLOAT) * 60 + CAST(RIGHT(B.WG_PRDTO, 2) AS FLOAT))) / 60.0, 2)
		--	  ELSE 0
		--	  END AS OVER_TIME

		--,CASE 
		--	 WHEN CONVERT(FLOAT, REPLACE(CONVERT(CHAR(5), I.FIRST_IN, 108), ':', ''))
		--			> CAST(B.WG_PRDFROM AS FLOAT)
		--	 THEN ROUND(((DATEPART(HOUR, I.FIRST_IN) * 60 + DATEPART(MINUTE, I.FIRST_IN))
		--			- (CAST(LEFT(B.WG_PRDFROM, 2) AS FLOAT) * 60 + CAST(RIGHT(B.WG_PRDFROM, 2) AS FLOAT))) / 60.0, 2)
		--	 ELSE 0
		-- END AS LATE_TIME


		--, CASE
		--	  WHEN B.WG_PRDFROM < I.FIRST_IN
		--	  THEN  ROUND (ISNULL(CAST(DATEDIFF(MINUTE, B.WG_PRDFROM, I.FIRST_IN) AS FLOAT), 0) / 60.0  - BASIC_TIME - 0.5 , 3)
		--	  ELSE 0.00 END AS LATE_TIME


		, CASE 
			  WHEN MAX(T.DS_Code) = '01' AND MAX(T.Du_Sbn) = MAX(A.EMPLOYEE_NO) AND MAX(T.Du_YMD) =  CAST(CONVERT(CHAR(8), CAST(@KT_DATE AS DATETIME), 112) AS VARCHAR)
			  THEN MAX(T.DS_TIME)  
			  ELSE null END AS BASIC_TIME
		, CASE 
			  WHEN MAX(T.DS_Code) = '10' AND MAX(T.Du_Sbn) = MAX(A.EMPLOYEE_NO) AND MAX(T.Du_YMD) =  CAST(CONVERT(CHAR(8), CAST(@KT_DATE AS DATETIME), 112) AS VARCHAR)
			  THEN MAX(T.DS_TIME)  
			  ELSE null END AS LATE_TIME
		, CASE 
			  WHEN MAX(T.DS_Code) = '33' AND MAX(T.Du_Sbn) = MAX(A.EMPLOYEE_NO) AND MAX(T.Du_YMD) =  CAST(CONVERT(CHAR(8), CAST(@KT_DATE AS DATETIME), 112) AS VARCHAR)
			  THEN MAX(T.DS_TIME) 
			  ELSE null END AS OVER_TIME
		, CASE 
			  WHEN MAX(T.DS_Code) = '12' AND MAX(T.Du_Sbn) = MAX(A.EMPLOYEE_NO) AND MAX(T.Du_YMD) =  CAST(CONVERT(CHAR(8), CAST(@KT_DATE AS DATETIME), 112) AS VARCHAR)
			  THEN MAX(T.DS_TIME)  
			  ELSE null END AS EARLY_TIME
		, CASE 
			  WHEN MAX(T.DS_Code) = '37' AND MAX(T.Du_Sbn) = MAX(A.EMPLOYEE_NO) AND MAX(T.Du_YMD) =  CAST(CONVERT(CHAR(8), CAST(@KT_DATE AS DATETIME), 112) AS VARCHAR) 
			  THEN MAX(T.DS_TIME)  
			  ELSE null END AS NIGHT_TIME
		, CASE 
			  WHEN MAX(T.DS_Code) = '35' AND MAX(T.Du_Sbn) = MAX(A.EMPLOYEE_NO) AND MAX(T.Du_YMD) =  CAST(CONVERT(CHAR(8), CAST(@KT_DATE AS DATETIME), 112) AS VARCHAR)
			  THEN MAX(T.DS_TIME)  
			  ELSE null END AS NIGHT_ALLOW


    FROM TIN114 A

		LEFT JOIN TIN313 B 
		  ON A.EMPLOYEE_NO = B.EMPLOYEE_NO
			AND B.DU_YMD = CAST(CONVERT(CHAR(8), CAST(@KT_DATE AS DATETIME), 112) AS VARCHAR)

		LEFT JOIN TIN310 C 
            ON B.WG_CODE = C.WG_CODE
        
		LEFT JOIN TIN122 D 
            ON A.DEPARTMENT_CODE = D.Department_Code

		LEFT JOIN TIN514 T
			ON A.EMPLOYEE_NO = T.Du_Sbn
			AND T.Du_YMD = CAST(CONVERT(CHAR(8), CAST(@KT_DATE AS DATETIME), 112) AS VARCHAR)

        LEFT JOIN TIN312 E 
            ON A.EMPLOYEE_NO = E.EMPLOYEE_NO

		LEFT JOIN TIN334 F
			ON A.EMPLOYEE_NO = F.EMPLOYEE_NO

        LEFT JOIN ValidInOut V 
          ON A.EMPLOYEE_NO = V.EMPLOYEE_NO

		LEFT JOIN WGInfo W
			ON A.EMPLOYEE_NO = W.EMPLOYEE_NO
			AND E.WG_CODE = W.WG_CODE
			AND W.RN=1

        LEFT JOIN InOutsum I 
            ON A.EMPLOYEE_NO = I.EMPLOYEE_NO

        LEFT JOIN Outsum O 
            ON A.EMPLOYEE_NO = O.EMPLOYEE_NO

		

    WHERE ISNULL(A.RETIRE_DATE,'') = ''
      AND ISNULL(A.REAL_USER_GBN,'0') = '1'
	  --AND T.DU_YMD = CAST(CONVERT(CHAR(8), CAST(@KT_DATE AS DATETIME), 112) AS VARCHAR)
	 GROUP BY  A.EMPLOYEE_NO
	 --ORDER BY A.EMPLOYEE_NO

	END
END


```
