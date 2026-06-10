---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:29:00
담당자: []
---
** 심시작업 java 소스내 최상단 servlet 설정부 바꾸기

** application.js 파일 내 경로 배포용으로 바꾸기

** 켈린더 입력을 마우스로하니까 불편해서 editable 설정 true로 임시처리했음

++ cors 설정도 폐기하기

## ㅇ 업무현황

![[스크린샷_2026-02-02_오후_5.55.01.png]]

→ flutter Webview를 활용 구현예정

ㅇ 사용 예정 화면배치

![[image_(3) 1.png]]

![[image_(3) 2.png]]

---

```javascript
launch: function () {
        Ext.create('iPlusCustOrder.view.main.Test', {
            renderTo: Ext.getBody()
        });
    }
```

[http://localhost:1841/?modern](http://localhost:1841/?modern=)

→ 이걸로 로컬 접속 가능 modern 필수 < 어떤기기인지 판별할수있게 파라미터로 경로를 바꾸게되어있음 >

[http://localhost:1841/?](http://localhost:1841/?modern=)classic

→ 웹서버

Sencha Cmd v6.5.0.180

동방 빌드용 센차 버젼 → 7.4.0.42


```javascript
/**
 * This class is the controller for the main view for the application. It is specified as
 * the "controller" of the Main view class.
 */
Ext.define('iPlusCustOrder.view.main.LoginController', {
    extend: 'Ext.app.ViewController',

    alias: 'controller.Login',
	init: function() {
		this.control(
			{
				'Login button': {
					click: this.onClick_Button
				}
			}
		);
	},

	// 버튼을 클릭했을때
	onClick_Button: function(btn) {
		const me = this;
		
		switch (btn.itemId) {
			case 'LonginConfirm': {
				me.onLoginClick(btn);
				break;
			}
		}
	},
	onLoginClick: function (btn) {
		
		var me = this ;

		var USER_ID = me.getView().down('#loginID').getValue();
		var USER_PW = me.getView().down('#loginPW').getValue();
		
		if((USER_ID==null||USER_ID=='') && (USER_PW==null||USER_PW=='')){
			Ext.Msg.alert('알림', 'ID와 비밀번호를 입력해주세요.');
			return;
		}
		
      	var store = me.getViewModel().getStore('store01');
		
		store.load({
			params: {
				USER_ID : USER_ID
				,USER_PW : USER_PW
			},
			callback: function(records, op, success) {
				if (success) {
					if(store.getCount() != 0){
						rec = records[0];
						gCustomerCode = rec.get('CUSTOMER_CODE');
						gCustomerName = rec.get('CUSTOMER_NAME');
						// Remove Login Window
						//Ext.Viewport.remove(me.getView(),true); 
						//var nMainMenuController = me.getApplication().getController("iPlusCustOrder.view.main.MainController");		
						//nMainMenuController.onViewShow();
						
						me.getView().destroy();

						var mainView = Ext.create('iPlusCustOrder.view.main.Main');
					    if (Ext.Viewport.add) {
					        Ext.Viewport.add(mainView);
					    } 
	
					}
					else{
						Ext.Msg.alert('알림', '해당하는 ID 또는 비밀번호가 존재하지 않습니다!');
						return;
					}
				}
				else{
					Ext.Msg.alert('알림', '해당하는 ID 또는 비밀번호가 존재하지 않습니다!');
					return;
				}
			}
		});
    }
});

```

→ 기존 로직 백업 ( 로그인 인증부분 로그인 미동작시 원래대로면  main 접근 불가능 )


```javascript
/**
 * This class is the controller for the main view for the application. It is specified as
 * the "controller" of the Main view class.
 */
Ext.define('iPlusCustOrder.view.main.LoginController', {
    extend: 'Ext.app.ViewController',

    alias: 'controller.Login',
	init: function() {
		this.control(
			{
				'Login button': {
					click: this.onClick_Button
				}
			}
		);
	},

	// 버튼을 클릭했을때
	onClick_Button: function(btn) {
		const me = this;
		
		switch (btn.itemId) {
			case 'LonginConfirm': {
				me.onLoginClick(btn);
				break;
			}
		}
	},

	onLoginClick: function (btn) {
    var me = this;

    // 2. 현재 로그인 창 파괴 (메모리 해제)
    me.getView().destroy();

    // 3. 메인 뷰 생성 및 Viewport에 추가
    var mainView = Ext.create('iPlusCustOrder.view.main.Main');
    
    if (Ext.Viewport && Ext.Viewport.add) {
        Ext.Viewport.add(mainView);
    } else {
    }
}


		// var USER_ID = me.getView().down('#loginID').getValue();
		// var USER_PW = me.getView().down('#loginPW').getValue();
		
		// if((USER_ID==null||USER_ID=='') && (USER_PW==null||USER_PW=='')){
		// 	Ext.Msg.alert('알림', 'ID와 비밀번호를 입력해주세요.');
		// 	return;
		// }
		
      	// var store = me.getViewModel().getStore('store01');
		
		// store.load({
		// 	params: {
		// 		USER_ID : USER_ID
		// 		,USER_PW : USER_PW
		// 	},
		// 	callback: function(records, op, success) {
		// 		if (success) {
		// 			if(store.getCount() != 0){
		// 				rec = records[0];
		// 				gCustomerCode = rec.get('CUSTOMER_CODE');
		// 				gCustomerName = rec.get('CUSTOMER_NAME');
		// 				// Remove Login Window
		// 				//Ext.Viewport.remove(me.getView(),true); 
		// 				//var nMainMenuController = me.getApplication().getController("iPlusCustOrder.view.main.MainController");		
		// 				//nMainMenuController.onViewShow();
						
		// 				me.getView().destroy();

		// 				var mainView = Ext.create('iPlusCustOrder.view.main.Main');
		// 			    if (Ext.Viewport.add) {
		// 			        Ext.Viewport.add(mainView);
		// 			    } 
	
		// 			}
		// 			else{
		// 				Ext.Msg.alert('알림', '해당하는 ID 또는 비밀번호가 존재하지 않습니다!');
		// 				return;
		// 			}
		// 		}
		// 		else{
		// 			Ext.Msg.alert('알림', '해당하는 ID 또는 비밀번호가 존재하지 않습니다!');
		// 			return;
		// 		}
		// 	}
		// });
    // }
});

```

→ 이런식으로 우회 메인테스트

---

## ㅇ 서비스 분리 필요

전환부 관리는 WebView가 아닌 app단 코드로 도메인을 갈아끼우며 진행할것임

네비게이션 다뜯기

```javascript
launch: function() {
    // 1. URL의 쿼리 스트링(? 이후의 문자열)을 가져옵니다.
    var searchParams = new URLSearchParams(window.location.search);
    
    // 2. 'service' 파라미터 값이 'custorder'인지 직접 확인합니다.
    var isCustOrder = searchParams.get('service') === 'custorder';
    
    var mainView;

    if (isCustOrder) {
        mainView = Ext.create('iPlusCustOrder.view.main.Main'); 
    } else {
        mainView = Ext.create('iPlusCustOrder.view.main.Login');
    }

    if (Ext.Viewport && Ext.Viewport.add) {
        Ext.Viewport.add(mainView);
    } else {
        // 뷰포트가 없을 경우를 대비한 대체 코드
        Ext.create('Ext.container.Viewport', {
            layout: 'fit',
            items: [mainView]
        });
    } 
}
```

→ 서비스 뜯기 백업본 엔드포인트 별로 로그인 없이 바로 별도 서비스에 접근가능하게
• **모던 주문 화면 접근 (Modern UI)**

- [`http://localhost:1841/?modern&service=order`](http://localhost:1841/?modern=&service=order) → 수주현황
- [`http://localhost:1841/?modern&service=order`](http://localhost:1841/?modern=&service=order) → 
- `http://localhost:1841/?modern&service=order`

```javascript
launch: function() {
		//var loggedIn=false;
		var mainView = Ext.create('iPlusCustOrder.view.main.Login');
	    if (Ext.Viewport.add) {
	        Ext.Viewport.add(mainView);
	    } 
	}
```

→ 기본방식

[https://218.155.74.35/status/?service=order](https://218.155.74.35/status/?service=order)

[https://218.155.74.35/status/?service=prod](https://218.155.74.35/status/?service=prod)

[https://218.155.74.35/status/?service=deliver](https://218.155.74.35/status/?service=deliver)

```javascript
launch: function() {
    // 1. URL의 파라미터를 분석합니다.
    var searchParams = new URLSearchParams(window.location.search);
    
    // 2. 'service' 파라미터 값을 직접 가져옵니다. (order, prod, deliver 등)
    var serviceType = searchParams.get('service');

    var mainView;

    // 디버깅: 어떤 서비스가 들어왔는지 확인
    console.log('Requested Service:', serviceType);

    if (serviceType === 'order') {
        mainView = Ext.create('iPlusCustOrder.view.main.OrderList'); 
    } else if (serviceType === 'prod') {
        mainView = Ext.create('iPlusCustOrder.view.main.ProdList'); 
    } else if (serviceType === 'deliver') {
        mainView = Ext.create('iPlusCustOrder.view.main.DeliverList'); 
    } else {
        // service 파라미터가 없거나 잘못된 경우 로그인 페이지
        mainView = Ext.create('iPlusCustOrder.view.main.Login');
    }

    if (Ext.Viewport && Ext.Viewport.add) {
        Ext.Viewport.add(mainView);
    }
}
```



→ 경로 재설정 완료 최종 테스트 주소

http://218.155.74.35:40110/status/?service=order


---


```javascript
/**
 * 업무현황 리스트 View (실제 데이터 바인딩 버전)
 */
Ext.define('iPlusCustOrder.view.main.OrderList', {
    extend: 'Ext.form.Panel',
    xtype: 'orderlist',
    requires: [
        'iPlusCustOrder.store.OrderListStore',
        'iPlusCustOrder.view.main.OrderListController',
        'Ext.dataview.DataView'
    ],
    controller: 'OrderList',
    viewModel: 'OrderListStore',
    layout: 'fit',

    tbar: [ 
        {
            xtype: 'fieldcontainer',
            layout: {
                type: 'hbox',
                align: 'stretch'
            },
            items: [
                {
                    xtype: 'displayfield',
                    hideEmptyLabel: false,
                    value: '수주일'
                },
                {
                    xtype: 'button',
                    itemId: 'btn_ArrowLeft',
                    padding: 11,
                    scale: 'large',
                    ui: 'default-large',
                    iconCls: 'x-fa fa-angle-left fa-2x',
                    listeners: {
                        element: 'element',
                        click: 'onArrowLeft'
                    }
                },
                {
                    xtype: 'datepickerfield',
                    itemId: 'df_ORDERDATE',
                    width: 150,
                    picker: {
                        yearFrom: 2020,
                        yearTo: 2030,
                        slotOrder: ['year', 'month' ,'day']
                    },
                    value: new Date(),
                    format :'Ymd',
                    editable: true
                },
                {
                    xtype: 'button',
                    itemId: 'btn_ArrowRight',
                    padding: 11,
                    scale: 'large',
                    ui: 'default-large',
                    iconCls: 'x-fa fa-angle-right fa-2x',
                    listeners: {
                        element: 'element',
                        click: 'onArrowRight'
                    }
                },
                {
                    xtype: 'button',
                    name: "btnSearch",
                    ui: 'search',
                    iconCls: 'x-fa fa-search',
                    iconMask: true,
                    flex: 1        
                }
            ]
        }
    ],
    
    items: [
        {
            xtype: 'container',
            layout: 'vbox',
            scrollable: true,
            items: [
                // 1. 상단 요약 정보 (이 부분은 나중에 ViewModel 필드에 바인딩하면 실시간으로 변합니다)
                {
                    xtype: 'container',
                    padding: 15,
                    style: 'background: #fff; border-bottom: 1px solid #eee;',
                    html: `
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span style="font-size:1.1em; color:#333;">총 건수</span>
                            <span style="font-weight: bold; font-size: 1.4em;">1,026<small style="font-size:0.7em;">건</small></span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px; color: #1890ff;">
                            <span style="font-size:1.1em;">출하 건수</span>
                            <span style="font-weight: bold; font-size: 1.4em;">1<small style="font-size:0.7em;">건</small></span>
                        </div>
                        <div style="display: flex; justify-content: space-between; color: #ff4d4f;">
                            <span style="font-size:1.1em;">미출하건수</span>
                            <span style="font-weight: bold; font-size: 1.4em;">1,025<small style="font-size:0.7em;">건</small></span>
                        </div>
                    `
                },
                // 2. 리스트 데이터 영역 
                {
                    xtype: 'dataview',
                    itemId: 'grid01', // 기존 아이디 유지 또는 변경
                    bind: '{store01}', // 실제 데이터 소스 연결
                    scrollable: false, // 부모 컨테이너가 스크롤을 담당함
                    itemTpl: [
                        '<div style="background:#fff; border-bottom: 1px solid #eee; padding: 15px;">',
                        '    <div style="font-size: 1.1em; font-weight: bold; color: #000; margin-bottom: 5px;">{ITEM_NAME}-{ITEM_SPEC}</div>',
                        '    <div style="color: #888; font-size: 0.9em; margin-bottom: 10px;">{ORDER_REMARK}</div>', // 비고(REMARK)를 설명칸으로 활용
                        '    <div style="display: flex; font-size: 0.9em; color: #666;">',
                        '        <div style="flex: 1;">납기일: {DELIVERY_DATE}</div>',
                        '        <div style="flex: 1;">수주량: {ORDER_QTY} {UNIT_NAME}</div>',
                        '    </div>',
                        '    <div style="display: flex; font-size: 0.9em; color: #666; margin-top: 5px; align-items: center;">',
                        '        <div style="flex: 1;">출하일: ',
                        '            <tpl if="!SHIPPING_DATE">', // 데이터 필드에 SHIPPING_DATE가 없을 경우
                        '                <span style="background: #ff4d4f; color: #fff; padding: 2px 6px; border-radius: 3px; font-size: 0.8em;">미출하</span>',
                        '            <tpl else>',
                        '                <span style="background: #e1f5fe; color: #01579b; padding: 2px 6px; border-radius: 3px; font-size: 0.8em;">{SHIPPING_DATE}</span>',
                        '            </tpl>',
                        '        </div>',
                        '        <div style="flex: 1;">출하량: {SHIPPING_QTY} {UNIT_NAME}</div>',
                        '    </div>',
                        '</div>'
                    ],
                    listeners: {
                        childtap: 'onItemSelected'
                    }
                }
            ]
        }
    ]
});
```

```javascript
Ext.define('iPlusCustOrder.view.main.OrderListItem', {
    extend: 'Ext.dataview.DataItem',
    xtype: 'orderlistitem',

    requires: [
        'Ext.dataview.DataItem'
    ],

    items: [
        {
            xtype: 'component',
            itemId: 'html',
            cls: 'order-card'
        }
    ],

    updateRecord: function(record) {
        if (!record) return;

        var shipDate = record.get('SHIPPING_DATE');
        var badge = shipDate ? '<span class="badge-info">' + shipDate + '</span>' : '<span class="badge-danger">미출하</span>';

        this.down('#html').setHtml(`
            <div class="order-title">
                ${record.get('ITEM_NAME')} - ${record.get('ITEM_SPEC')}
            </div>
            <div class="item-detail">
                ${record.get('ITEM_DETAIL') || ''}
            </div>
            <div class="order-row">
                <span>납기일: ${record.get('DELIVERY_DATE')}</span>
                <span style="float:right;">수주량: ${record.get('ORDER_QTY')}${record.get('UNIT_NAME')}</span>
            </div>
            <div class="order-row">
                <span>출하일: ${badge}</span>
                <span style="float:right;">출하량: ${record.get('SHIPPING_QTY')}${record.get('UNIT_NAME')}</span>
            </div>
        `);
    }
});

```

---

# ㅇ 결과화면

### → 수주현황 스크린

![[image 174.png]]

### → 생산현황 스크린

![[image 175.png]]


### → 납품현황 스크린

![[image 176.png]]


[https://218.155.74.35/status/?service=order](https://218.155.74.35/status/?service=order)

[https://218.155.74.35/status/?service=prod](https://218.155.74.35/status/?service=prod)

[https://218.155.74.35/status/?service=deliver](https://218.155.74.35/status/?service=deliver)

→ 최종 배포 URL 
