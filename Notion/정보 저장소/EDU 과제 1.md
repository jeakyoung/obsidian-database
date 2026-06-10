---
base: "[[정보 저장소.base]]"
우선순위: 높음
종료일: 2025-07-29
상태: 완료
담당자:
  - 안재경
팀: []
---

Grid에서 선택된 모든 값 한번에 FormPanel로 로드하기 ( loadRecord 활용 )

```javascript
Ext.define('AppTest1.view.edu.edu3', {
    extend: 'Ext.Panel',
    xtype: 'edu3',

    controller: 'edu3',
    viewModel: 'edu3',
    
    title: '그리드',
  
    layout: {
    	type: 'hbox',
    	align: 'stretch'
    },
    	
    items: [
    	{
    		xtype: 'grid',
    		title: '리스트',
    		flex: 2,
    		bind: {
    			store: '{gridStore_Board}'
    		},
    		columns: [
    			{
    	            xtype: 'rownumberer',
    	            text: '번호',
    	            width: 70,
    	            align: 'center'
    	        },
    	        {
    	            text: '제목',
    	            dataIndex: 'title',
    	            flex: 1
    	        },
    	        {
    	            text: '이름',
    	            dataIndex: 'username',
    	            flex: 1
    	        }
    		],
    	    bbar: {
    	        xtype: 'pagingtoolbar',
    	        displayInfo: true,
    	        displayMsg: '게시글 {0} - {1} of {2}',
    	        emptyMsg: "게시글이 없습니다."
    	    },
    		listeners: {
    			select: 'onSelect'
    		}	
    	},
    	{
    		xtype: 'form',
    		title: '정보',
    		itemId: 'formInfo',
    		flex: 1,
    		bodyPadding: 10,
    		margin: '0 0 0 10',
    		layout: {
    			type: 'vbox',
    			align: 'stretch'
    		},
    		items: [
    			{
    				xtype: 'textfield',
    				fieldLabel: '유저아이디',
					itemId: 'tf_userId',
    				name: 'userid'
    			},
    			{
    				xtype: 'textfield',
    				fieldLabel: '유저명',
    				itemId: 'tf_userName',
    				name: 'username'
    			},
    			{
    				xtype: 'textfield',
    				fieldLabel: '제목',
    				name: 'title'
    			},
    			{
    				xtype: 'textfield',
    				fieldLabel: '포럼아이디',
    				name: 'forumid'
    			},
    			{
    				xtype: 'textfield',
    				fieldLabel: '포럼타이틀',
    				name: 'forumtitle'
    			},
    			{
    				xtype: 'textfield',
    				fieldLabel: '자기이름'
    			}
    		]
    	}
    ]
});
```

```javascript
Ext.define('App_Edu1.store.edu.edu3', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.edu3',

    stores: {
        gridStore_Board: {
            data: [
            	{userid: '111', title: '타이틀1', username: '이름1'},
            	{userid: '222', title: '타이틀2', username: '이름2'},
            	{userid: '333', title: '타이틀3', username: '이름3'}
            ]
        },
        gridStore_Board2: {
        	fields: [
                { name: 'replycount', type: 'int' },
                { name: 'lastpost', mapping: 'lastpost', type: 'date', dateFormat: 'timestamp' }
            ],
            pageSize: 30,
            autoLoad: true,
			proxy: {
				type: 'jsonp',
                url: 'https://www.sencha.com/forum/topics-browse-remote.php',
                reader: {
                    rootProperty: 'topics',
                    totalProperty: 'totalCount'
                }
            }
        }
    }
});

```

```javascript
Ext.define('AppTest1.view.edu.edu3Controller', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.edu3',

    onSelect: function (grid, record, index) {
        const formPanel = this.getView().down('#formInfo');
				const form = formPanel.getForm();
		
        form.loadRecord(record);

        record.set('forumid', record.get('userid'));
    }
});
```


![[image 68.png]]


참고자료

[https://docs.sencha.com/extjs/7.2.0/modern/src/Store.js-1.html#Ext.data.Store-method-loadRecords](https://docs.sencha.com/extjs/7.2.0/modern/src/Store.js-1.html#Ext.data.Store-method-loadRecords)

[https://wikidocs.net/3384](https://wikidocs.net/3384)

[https://wikidocs.net/1986](https://wikidocs.net/1986)

### 문서

[]()

![]()

[]()
