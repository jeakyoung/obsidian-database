---
base: "[[정보 저장소.base]]"
우선순위: 높음
종료일: 2025-08-07
상태: 완료
담당자:
  - 안재경
팀: []
---
< 목표 > 8.4 ~ 8.12

[[ExtJS_Grid활용교육 1.xlsx]]

1. 리뷰과제 명세서 대로 구현 진행
2. 엑셀 업로드 기능 추가
3. 출력 기능 추가

---

→ 조회, 등록, 수정, 삭제 정상 동작 확인 완료

      조회 명세 

      등록 명세

+  엑셀 IMPORT, EXPORT 

---



---

<코드 저장>

```javascript
Ext.define('AppTest1.view.GW.WGW500.test5', {
  extend: 'Ext.Panel',
  xtype: 'test5',

  controller: 'test5',
  viewModel: 'test5',

  title: replaceLocale('test5'),

  layout: {
    type: 'vbox',
    align: 'stretch'
  },

  dockedItems: [                                                                                                        //상단 toolbar
    {
      xtype: 'commonToolbar2'
    },
    {
      xtype: 'button', text: replaceLocale('엑셀 업로드'), ui: 'btnCls_other2', handler: 'excelUploadWindow',           //excel 업로드 버튼
      height: 50,
      margin: 1
    }
  ],

  items: [
    {
      xtype: 'panel',
      flex: 1,
      layout: {
        type: 'hbox',
        align: 'stretch'
	    },

      items: [
        {
          xtype: 'gridpanel',                                                                                       //부모(공정)그리드
          itemId: 'grid_01',
          flex: 1,
          bind: {
            store: '{store_01}'
          },
          stateId: 'test5_grid01',
          viewConfig: {
            enableTextSelection: true,
            emptyText: '<center>' + replaceLocale('데이터가 없습니다.') + '</center>',                                //데이터 없을경우 출력
            plugins: [{
              ptype: 'gridviewdragdrop',                                                                           //Grid내부 Drag & Drop 영역정의

              pluginId: 'reorderMaster',
              dragGroup: 'ddMaster', 
              dropGroup: 'ddMaster',
              enableDrop: true,
              enableDrag: true
            }],
            listeners: {
            select: 'onParentSelect',                                                                               //행 선택 리스너
            drop: 'onDropReorderMaster'                                                                             //DragDrop 리스너
          }
          },
          plugins: [
            { ptype: 'cellediting', clicksToEdit: 3 },                                                              // cell edit을 위한 필요 클릭 횟수
            { ptype: 'gridexporter' }                                                                               // exporter 플러그인 정의
          ],
          
		  
		  dockedItems: [
            {
              xtype: 'toolbar',                                                                                     //공정 그리드 위 등록 삭제 저장 버튼 분리 -> onNew버튼은 하나기에 분리.
              dock: 'top',
              items: [
                { xtype: 'button', text: replaceLocale('행추가'), ui: 'btnCls_other2', handler: 'onNew'    },
                { xtype: 'button', text: replaceLocale('행삭제'), ui: 'btnCls_other2', handler: 'onDelete' },
                { xtype: 'button', text: replaceLocale('행저장'), ui: 'btnCls_other2', handler: 'onReg'    }
              ]
            }],
		  
          columns: [                                                                                                //삭제 여부 확인을 위한 checkbox 지정
            { xtype: 'rownumberer' },
            {
              xtype: 'checkcolumn',
              text: replaceLocale('삭제'),
              dataIndex: 'DELETE',
              width: 60
            },
            {
              text: replaceLocale('공정코드'),                                                                      //아래 순서대로 WORK_CODE, WORK_NAME textField
              dataIndex: 'WORK_CODE',
              editor: { xtype: 'textfield', allowBlank: false },
              flex: 1
            },
            {
              text: replaceLocale('공정명'),
              dataIndex: 'WORK_NAME',
              flex: 1,
              editor: {
                xtype: 'textfield',
                allowBlank: false,
              },
            }],
        },
        {
          xtype: 'gridpanel',                                                                                   //자식(호기) 그리드 동작 방식은 같으나 인덱스 명칭에 Detail이 들어가있음
          itemId: 'grid_02',
          flex: 1,
          bind: {
            store: '{store_02}'
          },
          stateId: 'test5_grid02',
          viewConfig: {
            enableTextSelection: true,
            emptyText: '<center>' + replaceLocale('데이터가 없습니다.') + '</center>',
            preserveScrollOnRefresh: true,
            plugins: [{
              ptype:     'gridviewdragdrop',
              pluginId:  'reorderDetail',
              dragGroup: 'ddDetail',
              dropGroup: 'ddDetail',
              enableDrop: true,
              enableDrag: true
            }],
            listeners: {
            drop: 'onDropReorderDetail'
          }
          },
          plugins: [
            { ptype: 'cellediting', clicksToEdit: 3 },
            { ptype: 'gridexporter' },
          ],
          dockedItems: [
            {
              xtype: 'toolbar',
              dock: 'top',
              items: [
                { xtype: 'button', text: replaceLocale('행추가'), ui: 'btnCls_other2', handler: 'onNewDetail'    },
                { xtype: 'button', text: replaceLocale('행삭제'), ui: 'btnCls_other2', handler: 'onDeleteDetail' },
                { xtype: 'button', text: replaceLocale('행저장'), ui: 'btnCls_other2', handler: 'onRegDetail'    }
              ]
            }
          ],
          columns: [
            { xtype: 'rownumberer' },
            {
              xtype: 'checkcolumn',
              text: replaceLocale('삭제'),
              dataIndex: 'DELETE',
              width: 60
            },
            {
              text: replaceLocale('호기코드'),
              dataIndex: 'LINE_CODE',
              editor: { xtype: 'textfield', allowBlank: false },
              flex: 1
            },
            {
              text: replaceLocale('호기명'),
              dataIndex: 'LINE_NAME',
              editor: {
                xtype: 'textfield',
                allowBlank: false
              },
              flex: 1
            },
          ]
        }
      ]
    },
    {
      xtype: 'component',
      hidden: true,
      html:
        '<form id="viewerFormTest5">' +
        '<input name="FACTORY_CODE">' +
        '<input name="WORK_CODE">' +
        '<input name="WORK_NAME">' +
        '<input name="LINE_CODE">' +
        '<input name="LINE_NAME">' +
        '</form>',
    }
  ]
});
```

→ VIEW

```javascript
Ext.define('AppTest1.view.GW.WGW500.test5Controller', {
  extend: 'Ext.app.ViewController',
  alias: 'controller.test5',

  requires: ['AppTest1.store.GW.WGW500.test5'],

  rRecord: false,

  init: function () {                                                               //실행시
    var me = this;
    me.control({
      '#grid_01': {
        select: 'onSelect',                                                         //부모그리드 data select, 드래그 리슨준비
        viewready: 'onMasterViewReady'
      },
      '#grid_02': {
        viewready: 'onDetailViewReady'                                              //드래그 리슨준비
      }
    });
    me.isPendingSave = false;                                                       //변경사항 refresh
  },

  onSelect: function (rowModel, record) {                                           //onselect 기능
    var me = this;
    me.rRecord = record;

    var workCode = record.get('WORK_CODE');                                         //work_code 가져오기
    var detailStore = me.getViewModel().getStore('store_02');                       //그걸가지고 자식그리드와 매칭준비

    detailStore.load({                                                              //자식 스토어 로드
      params: {                                                                     //파라미터값
        WORK_CODE: workCode,
        DELETE_FLAG: '0',
        FACTORY_CODE: gFactoryCode,
        VIEW_SEQ: '0'
      }
    });
  },

  onView: function () {                                                             //조회버튼 클릭시
    var me = this;                                                                 
    var store = me.getViewModel().getStore('store_01');                             //부모 그리드 스토어 명시
    store.load({                                                                    //로드 시작
      callback: function (records, op, success) {                                   //피드백 성공시 조회완료 실패시 호출중지
        if (success) {
          Ext.Msg.alert('정보', '조회 완료');
        } else {
          store.removeAll();
          store.clearData();
        }
      }
    });
  },

  onNew: function () {                                                              //신규 버튼 클릭시
    var me = this;
    var grid = me.getView().down('#grid_01');                                       //grid1내 변경사항을 grid로 다운명시
    var store = grid.getStore();                                                    //store에 담고

    var isPendingSave = store.findBy(function (record) {                            //isPendingSave 정의
      return !record.get('WORK_CODE') || !record.get('WORK_NAME');                  // store 내에 WORK_CODE 또는 WORK_NAME이 비어있는 레코드가 하나라도 있으면 true
    }) !== -1;

    if (isPendingSave) {
      Ext.Msg.alert('정보', '이미 등록중인 공정항목이 존재합니다.');                      //등록중인 공정이 있으면 추가등록 불가능
      return;
    }

    var record = { FACTORY_CODE: gFactoryCode, WORK_CODE: '', WORK_NAME: '', VIEW_SEQ: ''};         //record에 형식대로 데이터 저장 명시
    store.add(record);
  },

  onReg: function () {                                                                //저장 버튼 클릭시
  var me    = this;
  var grid  = me.getView().down('#grid_01');
  var store = grid.getStore();

  var modified = store.getModifiedRecords();                                           // 변경사항 감지
  var removed  = store.getRemovedRecords();                                            // 삭제여부 감지 
  if (modified.length === 0 && removed.length === 0) {                                 // 아무것도 한게 없으면
    Ext.Msg.alert('정보', '변경된 데이터가 없습니다.');                                    // 피드백, 리턴
    return;
  }

  function norm(s) { return (s || '').toString().trim().toUpperCase(); }               //norm선언 스트링타입에 공백없에고 대문자로

  var seen = {};
  var valid = true;

  store.each(function (rec, idx) {
    if (rec.get('DELETE') === true) return;                                             //삭제 체크된 데이터 리턴

    var fac  = (rec.get('FACTORY_CODE') || gFactoryCode || '').toString().trim();       //공장코드, 공정이름, 공정코드 get
    var name = (rec.get('WORK_NAME') || '').toString().trim();
    var code = (rec.get('WORK_CODE') || '').toString().trim();

    if (!name) {                                                                        //저장할때 이름이 없으면 피드백출력
      Ext.Msg.alert('정보', '공정명은 필수입니다.');
      valid = false;
      return false;
    }

    var key = fac + '||' + norm(name);
    var prev = seen[key];

    if (!prev) {
      seen[key] = { idx: idx, code: code };
      return;
    }

    var sameCode = (prev.code === code);
    var bothNew  = (!prev.code && !code && prev.idx !== idx);

    if (!sameCode || bothNew) {                                                         //공정 코드가 같으면
      Ext.Msg.alert('정보', '중복 공정명입니다: ' + name);                                 //피드백 출력
      valid = false;
      return false;
    }
  });

  if (!valid) return;                                                                   //모든 조건 통과시 IUD 모델에 입력값

  store.each(function (rec) {                                                           
    if (!rec.get('WORK_NAME')) return;                                                  
    if (rec.dirty) {
      rec.set('FACTORY_CODE', gFactoryCode);
      rec.set('IUD', 'IU');
    }
  });

  store.sync({                                                                          //저장된 값으로 통신시작
    success: function () {
      Ext.Msg.alert('정보', '저장되었습니다.');                                            //성공시 피드백 출력 store 초기화
      store.reload();
    }
  });
},


  onDelete: function () {                                                                //삭제버튼 클릭시
    var me = this;
    var grid = me.getView().down('#grid_01');                                            //적용 그리드 정의
    var store = grid.getStore();
    let selected = store.queryBy(r => r.get('DELETE') === true);                         // 체크박스 클릭시 Delete값을 trueㄹ

    if (selected.length === 0) {                                                         // 체크박스 선택 없이 삭제 클릭시
      Ext.Msg.alert('정보', '삭제할 항목을 선택하세요.');                                    // 피드백 반환
      return;
    }

    selected.each(function (r) { r.set('IUD', 'D'); });                                  // 체크된 데이터는 IUD값을 D로 정의

    Ext.MessageBox.confirm('확인', '정말 삭제하시겠습니까?', function (btn) {                // 사용자 컨펌 메세지 출력
      if (btn === 'yes') {                                                               // 확인 받은후 삭제 진행 store 초기화
        store.sync({
          success: function () {
            Ext.Msg.alert('정보', '삭제되었습니다.');
            store.reload();
          }
        });
      }
    });
  },

  onNewDetail: function () {
    var me = this;
    var grid = me.getView().down('#grid_02');
    var store = grid.getStore();
    var master = me.rRecord;

    if (!master) {
      Ext.Msg.alert('정보', '상위 공정을 먼저 선택하세요.');
      return;
    }

    var record = {
      LINE_CODE: '',
      LINE_NAME: '',
      WORK_CODE: master.get('WORK_CODE'),
      VIEW_SEQ:  '',
      FACTORY_CODE: gFactoryCode
    };

    store.add(record);
  },

  onRegDetail: function () {
  var me    = this;
  var grid  = me.getView().down('#grid_02');
  var store = grid.getStore();

  var modified = store.getModifiedRecords();
  var removed  = store.getRemovedRecords();
  if (modified.length === 0 && removed.length === 0) {
    Ext.Msg.alert('정보', '변경된 데이터가 없습니다.');
    return;
  }

  function norm(s) { return (s || '').toString().trim().toUpperCase(); }

  var dupMap = {};

  store.each(function (rec, idx) {
    if (rec.get('DELETE') === true) return;

    var fac   = (rec.get('FACTORY_CODE') || gFactoryCode || '').toString().trim();
    var wcode = (rec.get('WORK_CODE') || '').toString().trim();
    var lname = (rec.get('LINE_NAME') || '').toString().trim();
    var lcode = (rec.get('LINE_CODE') || '').toString().trim();

    if (!wcode) {
      Ext.Msg.alert('정보', '상위 공정코드가 없습니다. 먼저 공정을 선택하세요.');                   //가져온 work가 없을시 부모행을 클릭하지 않은것으로 저장할수 있는 하위행이 없음
    }
    if (!lname) {
      Ext.Msg.alert('정보', '호기명은 필수입니다.');
    }

      var key = fac + '||' + norm(wcode) + '||' + norm(lname);                                // 공장코드), wcode, lname을 대문자, 공백제거 후 구분자로 합쳐서 unique 키로

    if (!dupMap[key]) {                                                                       // 현재 키가 dupMap에 없다면, 현재 인덱스와 호기코드를 저장 후 함수 종료
      dupMap[key] = { idx: idx, code: lcode };
      return;
    }

    var prev = dupMap[key];                                                                   // 이미 동일한 key가 존재한다면, 이전에 저장된 레코드를 꺼냄

    var isSameCode = (prev.code === lcode);                                                   // 이전 레코드의 호기코드와 현재 레코드의 호기코드가 같은지 여부
    var bothNew    = (!prev.code && !lcode && prev.idx !== idx);                              // 이전/현재 모두 호기코드가 비어있고, 인덱스가 다른 경우(둘 다 신규행인 경우)

    if (!isSameCode || bothNew) {                                                             // 둘중 한가지 경우에도 해당되지 않을경우                                          
      Ext.Msg.alert('정보', '중복 호기명입니다: ' + lname);                                      // 중복 메시지 피드백
    }
  });

  store.each(function (rec) {
    if (!rec.get('LINE_CODE') || !rec.get('LINE_NAME')) return;
    if (rec.dirty) rec.set('IUD', 'IU');
  });

  store.sync({
    success: function () {
      Ext.Msg.alert('정보', '저장되었습니다.');
      store.reload();
    }
  });
},


  onDeleteDetail: function () {
    var me = this;
    var grid = me.getView().down('#grid_02');
    var store = grid.getStore();
    let selected = store.queryBy(r => r.get('DELETE') === true);

    if (selected.length === 0) {
      Ext.Msg.alert('정보', '삭제할 항목을 선택하세요.');
      return;
    }

    selected.each(function (r) {
      r.set('IUD', 'D'); 
    });

    Ext.MessageBox.confirm('확인', '정말 삭제하시겠습니까?', function (btn) {
      if (btn === 'yes') {
        store.sync({
          success: function () {
            Ext.Msg.alert('정보', '삭제되었습니다.');
            store.reload();
          }
        });
      }
    });
  },


```

```javascript
  updateViewSeq: function (gridItemId, seqField) {
  var me       = this;
  var grid     = me.getView().down('#' + gridItemId);
  var view     = grid.getView();
  var viewData = (view.store || grid.getStore()).getRange();

  for (var i = 0; i < viewData.length; i++) {
    var rec    = viewData[i];
    var target = i + 1;
    if (rec.get(seqField) !== target) {
      rec.set(seqField, target);
    }
  }
},

  onMasterViewReady: function (grid) {
    var me = this;
    var view = grid.getView();
    view.on('drop', me.onDropReorderMaster, me);
  },

  onDetailViewReady: function(grid) {
    var me = this;
    var view = grid.getView();
    view.on('drop', me.onDropReorderDetail, me);
  },

  onDropReorderMaster: function () {
    var me = this;
    me.updateViewSeq('grid_01', 'VIEW_SEQ');
  },

  onDropReorderDetail: function () {
    var me = this;
    me.updateViewSeq('grid_02', 'VIEW_SEQ');
  },
  onPrint: function () {
    var me = this;

    var parentGrid   = me.getView().down('#grid_01');
    var parentRecord = me.selectedParent || (parentGrid && parentGrid.getSelectionModel().getSelection()[0]);
    if (!parentRecord) {
      Ext.Msg.alert('정보', '출력할 공정을 먼저 선택하세요.');
      return;
    }

    var childGrid  = me.getView().down('#grid_02');
    var childStore = childGrid ? childGrid.getStore() : null;
    if (!childStore || childStore.getCount() === 0) {
      Ext.Msg.alert('정보', '해당 공정에 대해 출력할 호기 데이터가 없습니다.');
      return;
    }

    var lineCodes = [];
    var lineNames = [];
    childStore.each(function (rec) {
      var code = (rec.get('LINE_CODE') || '').toString().trim();
      var name = (rec.get('LINE_NAME') || '').toString().trim();
      if (code) lineCodes.push(code);
      if (name) lineNames.push(name);
    });

    if (lineCodes.length === 0) {
      Ext.Msg.alert('정보', '전송할 호기 데이터가 없습니다.');
      return;
    }

    var reportForm = document.getElementById('viewerFormTest5');
    if (!reportForm) {
      Ext.Msg.alert('오류', '출력용 VIEW 호출 실패');
      return;
    }

    reportForm.action = 'http://localhost:8080/report/edu/edu4Report.jsp';
    reportForm.target = 'viewerFormTest5';
    reportForm.method = 'POST';

    reportForm.FACTORY_CODE.value = gFactoryCode;
    reportForm.WORK_CODE.value    = parentRecord.get('WORK_CODE') || '';
    reportForm.WORK_NAME.value    = parentRecord.get('WORK_NAME') || '';

    reportForm.LINE_CODE.value    = lineCodes;
    reportForm.LINE_NAME.value    = lineNames;

    reportForm.submit();
  },
  excelUploadWindow: function () {
  var me = this;

  var win = Ext.create('Ext.window.Window', {
    title: '공정(호기) 엑셀 업로드',
    width: '70%',
    height: '60%',
    modal: true,
    maximizable: true,
    layout: { type: 'vbox', align: 'stretch' },
    items: [{
      xtype: 'form',
      itemId: 'formFile',
      flex: 1,
      layout: { type: 'vbox', align: 'stretch' },
      items: [{
        xtype: 'grid',
        flex: 1,
        itemId: 'previewGrid',
        store: Ext.create('Ext.data.Store', {
          autoLoad: false,
          proxy: {
            type: 'ajax',
            api: {
              read   : Ext.manifest.api_url + '/com/edu/Test5_EXCEL_UPLOAD',
              create : Ext.manifest.api_url + '/com/edu/Test5_EXCEL_IUD',
              update : Ext.manifest.api_url + '/com/edu/Test5_EXCEL_IUD',
              destroy: Ext.manifest.api_url + '/com/edu/Test5_EXCEL_IUD'
            },
            reader: { type: 'json', rootProperty: 'data' },
            writer: { type: 'json', writeAllFields: true, encode: true, rootProperty: 'data' }
          }
        }),
        viewConfig: {
          emptyText: '<center>데이터가 없습니다.</center>',
          stripeRows: false,
          enableTextSelection: true
        },
        plugins: [
          { ptype: 'cellediting', clicksToEdit: 1 },
          { ptype: 'gridexporter' }
        ],
        tbar: [
          { xtype: 'label', style: 'font-weight:bold; color:red', html: "<i class='fa fa-info-circle'></i> 상태가 '정상'인 행만 저장됩니다." },
          '->',
          {
            xtype: 'button', text: '엑셀 업로드', ui: 'default-small',
            handler: function () {
              win.down('#fileField').fileInputEl.dom.click();
            }
          },
          {
            xtype: 'filefield', itemId: 'fileField', name: 'uploadFile',
            buttonText: '엑셀 업로드', buttonOnly: true, hideLabel: true, hidden: true,
            listeners: {
              change: function (fileField) {
                var form  = fileField.up('form').getForm();
                var grid  = fileField.up('form').down('#previewGrid');
                var store = grid.getStore();

                form.submit({
                  url: Ext.manifest.api_url + '/com/edu/Test5_EXCEL_UPLOAD',
                  waitMsg: '엑셀 업로드중..',
                  params: {
                    FACTORY_CODE: (typeof gFactoryCode !== 'undefined' ? gFactoryCode : '')
                  },
                  success: function (fp, res) {
                    var obj = res.response.responseText ? JSON.parse(res.response.responseText) : res.result;
                    if (obj && obj.success == 'false') {
                      Ext.MessageBox.show({ title: '에러', msg: obj.message, icon: Ext.MessageBox.ERROR, buttons: Ext.Msg.OK });
                      return;
                    }
                    store.removeAll(); store.clearData();
                    store.add(obj.data || []);
                  },
                  failure: function () {
                    Ext.Msg.alert('알림', '엑셀 업로드중 문제가 발생했습니다. 계속되면 관리자에 문의하세요.');
                  }
                });
              }
            }
          }
        ],
        columns: [
          { xtype: 'rownumberer', text: 'No', align: 'center', width: 60, locked: true },
          {
            text: '상태', dataIndex: 'VALIDATION_FLAG', width: 120, align: 'center', locked: true,
            renderer: function (v, meta, r) {
              if (v == '0') { meta.style = 'background-color:green;color:#fff;font-weight:bold'; return '정상'; }
              if (v == '1') { meta.style = 'background-color:red;color:#fff;font-weight:bold'; return r.get('VALIDATION_NAME') || '오류'; }
              return '';
            }
          },
          { text: '공정코드',       dataIndex: 'WORK_CODE',    width: 120, editor: { xtype: 'textfield', allowBlank: false } },
          { text: '공정이름',       dataIndex: 'WORK_NAME',    flex: 1,    editor: { xtype: 'textfield', allowBlank: false } },
          { text: '호기코드',       dataIndex: 'LINE_CODE',    width: 140, editor: { xtype: 'textfield', allowBlank: false } },
          { text: '호기명',         dataIndex: 'LINE_NAME',    flex : 1,   editor: { xtype: 'textfield', allowBlank: false } }
        ]
      }]
    }],
    buttons: [{
      text: '저장', ui: 'default-small',
      handler: function () {
        var grid  = win.down('#previewGrid');
        var store = grid.getStore();

        var hasError = false, items = [];
        store.each(function (rec) {
          if (rec.get('VALIDATION_FLAG') == '1') { hasError = true; }
          else {

            rec.set('FACTORY_CODE', (typeof gFactoryCode !== 'undefined' ? gFactoryCode : rec.get('FACTORY_CODE') || ''));
            rec.set('IUD', 'IU');
            items.push(rec.data);
          }
        });
        if (hasError) {
          Ext.Msg.alert('알림', '오류가 있는 행이 있습니다. 수정 후 저장하세요.');
          return;
        }
        if (items.length === 0) {
          Ext.Msg.alert('알림', '저장할 데이터가 없습니다.');
          return;
        }

        win.getEl().mask('데이터 처리중..');
        Ext.Ajax.request({
          method: 'POST',
          url: Ext.manifest.api_url + '/com/edu/Test5_EXCEL_IUD',
          params: { data: Ext.encode(items) },
          success: function (resp) {
            win.getEl().unmask();
            var obj = resp.responseText ? Ext.JSON.decode(resp.responseText) : resp.responseJson;
            if (obj && obj.success == 'false') {
              Ext.MessageBox.show({ title: '에러', msg: obj.message, icon: Ext.MessageBox.ERROR, buttons: Ext.Msg.OK });
              return;
            }

            me.onView();
            var childGrid = me.getView().down('#grid_02');
            if (childGrid) { childGrid.getStore().removeAll(); childGrid.getStore().clearData(); }

            showToast && showToast('알림', '저장되었습니다.');
            win.close();
          },
          failure: function () { win.getEl().unmask(); Ext.Msg.alert('알림', '저장 실패'); }
        });
      }
    }, {
      text: '닫기', ui: 'default-small', handler: function () { win.close(); }
    }]
  });
    win.show();
    win.center();
}
});
```

[[→ CONTROLLER]]

```javascript
Ext.define('AppTest1.store.GW.WGW500.test5', {
  extend: 'Ext.app.ViewModel',
  alias: 'viewmodel.test5',

  stores: {
    store_01: {                                                                         //Grid 1 Model
      autoLoad: false,
      proxy: {
        type: 'ajax',                                                                   //ajax 방식 통신시도 crud에 해당되는 엔드포인트 주소 담기
        api: {
          create:  Ext.manifest.api_url + '/com/edu/jvEdu5_01_IUD',
          read:    Ext.manifest.api_url + '/com/edu/jvEdu5_01_LIST',
          update:  Ext.manifest.api_url + '/com/edu/jvEdu5_01_IUD',
          destroy: Ext.manifest.api_url + '/com/edu/jvEdu5_01_IUD'
        },
        
        reader: {                                                                       //읽기 형식지정
          type: 'json',
          rootProperty: 'data'
        },
        writer: {                                                                       //쓰기 형식 지정
          type: 'json',
          writeAllFields: true,
          encode: true,
          rootProperty: 'data'
        },
        listeners: {                                                                    //통신장애 리스너
          exception: function(proxy, response, operation) {
            var obj = Ext.JSON.decode(response.responseText);                           //서버단의 통신장애 예외상황 발생시 해당 메시지를 담아 출력
            Ext.MessageBox.show({
              title: '에러',
              msg: obj.message,
              icon: Ext.MessageBox.ERROR,
              buttons: Ext.Msg.OK
            });
          }
        }
      }
    },
    store_02: {
      autoLoad: false,
      proxy: {
        type: 'ajax',
        api: {
          create:  Ext.manifest.api_url + '/com/edu/jvEdu5_02_IUD',
          read:    Ext.manifest.api_url + '/com/edu/jvEdu5_02_LIST',
          update:  Ext.manifest.api_url + '/com/edu/jvEdu5_02_IUD',
          destroy: Ext.manifest.api_url + '/com/edu/jvEdu5_02_IUD'
        },
        reader: {
          type: 'json',
          rootProperty: 'data'
        },
        writer: {
          type: 'json',
          writeAllFields: true,
          rootProperty: 'data',
          encode: true
        },
        listeners: {
          exception: function(proxy, response, operation) {
            var obj = Ext.JSON.decode(response.responseText);
            Ext.MessageBox.show({
              title: '에러',
              msg: obj.message,
              icon: Ext.MessageBox.ERROR,
              buttons: Ext.Msg.OK
            });
          }
        }
      }
    }
  }
});

```

→ STORE

```java
package com.edu;

import com.report.model.edu.Edu4_1Model;
import com.report.service.edu.EduService;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import javax.servlet.*;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

@WebServlet("/com/edu/jvEdu5_01_LIST")
public class jvEdu5_01_LIST extends HttpServlet {
    public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {
        response.setContentType("application/json; charset=UTF-8");
        request.setCharacterEncoding("UTF-8");
        JSONArray result = new JSONArray();

        try {
            EduService service = new EduService();
            ArrayList<Edu4_1Model> list = service.getFirstList(request, this.getServletContext());

            for (Edu4_1Model model : list) {
                JSONObject obj = new JSONObject();
                obj.put("FACTORY_CODE", model.getFACTORY_CODE());
                obj.put("WORK_CODE", 	model.getWORK_CODE());
                obj.put("WORK_NAME",	model.getWORK_NAME());
                obj.put("VIEW_SEQ", 	model.getVIEW_SEQ());
                obj.put("DELETE_FLAG", 	model.getDELETE_FLAG());
                result.add(obj);
            }
        } catch (Exception e) {
            JSONObject error = new JSONObject();
            error.put("success", false);
            error.put("message", e.toString());
            result.add(error);
        }

        PrintWriter out = response.getWriter();
        out.print(result.toJSONString());
        out.flush();
    }
}

```

→ LIST - 1 ( 좌측 부모 그리드 )

```java
package com.edu;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Iterator;

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

@WebServlet("/com/edu/jvEdu5_01_IUD")
public class jvEdu5_01_IUD extends HttpServlet {
	private static final long serialVersionUID = 1L;

	@Override
	public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {

		Connection conn = null;
		PreparedStatement stmt = null;
		ResultSet rs = null;

		String query = "";
		String data;

		JSONArray itemList = new JSONArray();

		try {
			ServletContext sc = this.getServletContext();

			Class.forName(sc.getInitParameter("driver")).newInstance();
			conn = DriverManager.getConnection(sc.getInitParameter("url"), sc.getInitParameter("username"), sc.getInitParameter("password"));

			request.setCharacterEncoding("UTF-8");

			data = (String) request.getParameter("data");
			System.out.println(data);
			  if (data != null) {
	                JSONArray array;
	                if (data.startsWith("{")) {
	                    JSONParser parser = new JSONParser();
	                    JSONObject jsonObject = (JSONObject) parser.parse(data);
	                    array = new JSONArray();
	                    array.add(jsonObject);
	                } else {
	                    array = (JSONArray) JSONValue.parse(data);
	                }

	                Iterator<JSONObject> iterator = array.iterator();
	                while (iterator.hasNext()) {
	                    JSONObject jsonobj = iterator.next();

	                    query = "EXEC SP_HHR101_IUD" +
	                        "\r\n@FACTORY_CODE = '"  + jsonobj.get("FACTORY_CODE").toString().replace("'", "''") + "'," +
	                        "\r\n@WORK_CODE = '"  	 + jsonobj.get("WORK_CODE").toString().replace("'", "''") + "'," +
	                        "\r\n@WORK_NAME = '" 	 + jsonobj.get("WORK_NAME").toString().replace("'", "''") + "'," +
	                        "\r\n@VIEW_SEQ = '" 	 + jsonobj.get("VIEW_SEQ").toString().replace("'", "''") + "'," +
	                        "\r\n@IUD = '" 			 + jsonobj.get("IUD") + "'";
	                    
	                    System.out.println(query);
	                    stmt = conn.prepareStatement(query);
	                    stmt.executeUpdate();
	                }

	                itemList.clear();
	                JSONObject successJson = new JSONObject();
	                successJson.put("success", "true");
	                successJson.put("message", "IUD 처리 완료");
	                itemList.add(successJson);
	            }

		} catch (Exception e) {
			throw new ServletException(e);

		} finally {
			try {
				if (rs != null)
					rs.close();
			} catch (Exception e) {
			}
			try {
				if (stmt != null)
					stmt.close();
			} catch (Exception e) {
			}
			try {
				if (conn != null)
					conn.close();
			} catch (Exception e) {
			}
			JSONObject tempJson = new JSONObject();
			tempJson.put("success", "false");
			tempJson.put("message", "Error message goes here.");
			itemList.add(tempJson);
		}
		
		response.setContentType("application/json; charset=UTF-8");
		PrintWriter out = response.getWriter();
		out.print(itemList);
		out.flush();
		out.close();
	}
}
```

→ IUD - 1 ( 부모 그리드 CRUD 기능  )

```java
package com.edu;

import com.report.model.edu.Edu4_2Model;
import com.report.service.edu.EduService;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import javax.servlet.*;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
//endpoint 지정
@WebServlet("/com/edu/jvEdu5_02_LIST")
public class jvEdu5_02_LIST extends HttpServlet {
    public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {
        response.setContentType("application/json; charset=UTF-8");
        request.setCharacterEncoding("UTF-8");
        JSONArray result = new JSONArray();

        try {
        	//서비스 호출, 서비스 동작을 통해 들어온 데이터를 model로
            EduService service = new EduService();
            ArrayList<Edu4_2Model> list = service.getSecondList(request, this.getServletContext());
            //JSON 형식으로 데이터를 모델 -> 서블릿으로 Get
            for (Edu4_2Model model : list) {
                JSONObject obj = new JSONObject();
                obj.put("FACTORY_CODE", model.getFACTORY_CODE());
                obj.put("WORK_CODE", 	model.getWORK_CODE());
                obj.put("LINE_CODE", 	model.getLINE_CODE());
                obj.put("LINE_NAME", 	model.getLINE_NAME());
                obj.put("VIEW_SEQ", 	model.getVIEW_SEQ());
                obj.put("DELETE_FLAG", 	model.getDELETE_FLAG());
                result.add(obj);
            }
            //예외처리
        } catch (Exception e) {
            JSONObject error = new JSONObject();
            error.put("success", false);
            error.put("message", e.toString());
            result.add(error);
        }

        PrintWriter out = response.getWriter();
        out.print(result.toJSONString());
        out.flush();
    }
}

```

→ LIST 2 ( 자식 그리드 LIST 기능 )


```java
package com.edu;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Iterator;

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
//endpoint 지정
@WebServlet("/com/edu/jvEdu5_02_IUD")
public class jvEdu5_02_IUD extends HttpServlet {
	private static final long serialVersionUID = 1L;

	@Override
	public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {
		//연결부 정의
		Connection conn = null;		
		PreparedStatement stmt = null;
		ResultSet rs = null;
		//임시 스토리지
		String query = "";
		String data;
		//JSON 담을 배열
		JSONArray itemList = new JSONArray();

		try {
			//연결시도
			ServletContext sc = this.getServletContext();
			Class.forName(sc.getInitParameter("driver")).newInstance();
			conn = DriverManager.getConnection(sc.getInitParameter("url"), sc.getInitParameter("username"), sc.getInitParameter("password"));
			request.setCharacterEncoding("UTF-8");
			//String 타입으로 임시저장
			data = (String) request.getParameter("data");
			//data가 null이 아니라면
			if (data != null) {
                JSONArray array;
                //배열 선언후 값을 Json형식의 array로 정의 if -> 시작부, else -> 뒤따르는 JSON data
                if (data.startsWith("{")) {
                    JSONParser parser = new JSONParser();
                    JSONObject jsonObject = (JSONObject) parser.parse(data);
                    array = new JSONArray();
                    array.add(jsonObject);
                    
                } else {
                    array = (JSONArray) JSONValue.parse(data);
                }
                // Iterator를 이용 다음값을 계속 JSON형식으로 저장
                Iterator<JSONObject> iterator = array.iterator();
                while (iterator.hasNext()) {
                    JSONObject jsonobj = iterator.next();
                    //키:값 구조 만들기
                    query = "EXEC SP_HHR102_IUD"   +
                        "\r\n@FACTORY_CODE = 	'" + jsonobj.get("FACTORY_CODE").toString().replace("'", "''") + "'," +
                        "\r\n@WORK_CODE = 		'" + jsonobj.get("WORK_CODE").toString().replace("'", "''")    + "'," +
                        "\r\n@LINE_CODE = 		'" + jsonobj.get("LINE_CODE").toString().replace("'", "''")    + "'," +
                        "\r\n@LINE_NAME = 		'" + jsonobj.get("LINE_NAME").toString().replace("'", "''")    + "'," +
                        "\r\n@VIEW_SEQ = 		'" + jsonobj.get("VIEW_SEQ").toString().replace("'", "''") 	   + "'," +
                        "\r\n@DELETE_FLAG =	 	'" + (jsonobj.get("DELETE_FLAG") == null ? "0" : jsonobj.get("DELETE_FLAG").toString()) + "'," +
                        "\r\n@IUD = 			'" + jsonobj.get("IUD") + "'";
                    
                    System.out.println(query);
                    //데이터 보내기
                    stmt = conn.prepareStatement(query);
                    stmt.executeUpdate();
                }
                //배열 초기화, 피드백 메시지
                itemList.clear();
                JSONObject successJson = new JSONObject();
                successJson.put("success", "true");
                successJson.put("message", "IUD 처리 완료");
                itemList.add(successJson);
            }
		  //예외처리
		} catch (Exception e) {
			throw new ServletException(e);

		} finally {
			try {
				if (rs != null)
					rs.close();
			} catch (Exception e) {
			}
			try {
				if (stmt != null)
					stmt.close();
			} catch (Exception e) {
			}
			try {
				if (conn != null)
					conn.close();
			} catch (Exception e) {
			}
			JSONObject tempJson = new JSONObject();
			tempJson.put("success", "false");
			tempJson.put("message", "Error message goes here.");
			itemList.add(tempJson);
		}
		
		
		PrintWriter out = response.getWriter();
		out.print(itemList);
		out.flush();
		out.close();
	}
}
```

→ IUD 2 ( 자식 그리드 CRUD 모듈 )

```java

package com.report.service.edu;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import javax.servlet.ServletContext;
import javax.servlet.ServletRequest;

import com.report.model.edu.Edu4_1Model;
import com.report.model.edu.Edu4_2Model;
import com.util.DBClose;
import com.util.DBConnect;

public class EduService {
    DBConnect dbconnect = new DBConnect();

    public ArrayList<Edu4_1Model> getFirstList(ServletRequest request, ServletContext sc) {
        ArrayList<Edu4_1Model> list = new ArrayList<>();
        Connection conn = dbconnect.getConnection2(sc);
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            String sql = "EXEC SP_HHR101_LIST @FACTORY_CODE = ?, @WORK_CODE = ?, @WORK_NAME = ?, @VIEW_SEQ = ?, @DELETE_FLAG = ?";
            pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, request.getParameter("FACTORY_CODE"));
            pstmt.setString(2, request.getParameter("WORK_CODE"));
            pstmt.setString(3, request.getParameter("WORK_NAME"));
            pstmt.setString(4, request.getParameter("VIEW_SEQ"));
            pstmt.setString(5, request.getParameter("DELETE_FLAG"));
            rs = pstmt.executeQuery();

            while (rs.next()) {
            	Edu4_1Model model = new Edu4_1Model();
                model.setFACTORY_CODE(rs.getString("FACTORY_CODE"));
                model.setWORK_CODE(rs.getString("WORK_CODE"));
                model.setWORK_NAME(rs.getString("WORK_NAME"));
                model.setVIEW_SEQ(rs.getString("VIEW_SEQ"));
                model.setDELETE_FLAG(rs.getString("DELETE_FLAG"));
                list.add(model);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            DBClose.close(conn, pstmt, rs);
        }
        return list;
    }

    public ArrayList<Edu4_2Model> getSecondList(ServletRequest request, ServletContext sc) {
        ArrayList<Edu4_2Model> list = new ArrayList<>();
        Connection conn = dbconnect.getConnection2(sc);
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            String sql = "EXEC SP_HHR102_LIST @FACTORY_CODE = ?, @WORK_CODE = ?, @LINE_CODE = ?, @LINE_NAME = ?, @DELETE_FLAG = ?, @VIEW_SEQ = ?";
            pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, request.getParameter("FACTORY_CODE"));
            pstmt.setString(2, request.getParameter("WORK_CODE"));
            pstmt.setString(3, request.getParameter("LINE_CODE"));
            pstmt.setString(4, request.getParameter("LINE_NAME"));
            pstmt.setString(5, request.getParameter("DELETE_FLAG"));
            pstmt.setString(6, request.getParameter("VIEW_SEQ"));
            rs = pstmt.executeQuery();

            while (rs.next()) {
            	Edu4_2Model model = new Edu4_2Model();
                model.setFACTORY_CODE(rs.getString("FACTORY_CODE"));
                model.setWORK_CODE(rs.getString("WORK_CODE"));
                model.setLINE_CODE(rs.getString("LINE_CODE"));
                model.setLINE_NAME(rs.getString("LINE_NAME"));
                model.setVIEW_SEQ(rs.getString("VIEW_SEQ"));
                model.setDELETE_FLAG(rs.getString("DELETE_FLAG"));
                list.add(model);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            DBClose.close(conn, pstmt, rs);
        }
        return list;
    }
}

```

→ SERVICE


![[스크린샷_2025-08-06_173145.png]]

→ HHR 101, 102 TABLE


```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_HHR101_LIST]    Script Date: 2025-08-11 오후 2:13:59 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_HHR101_LIST]
    @FACTORY_CODE       VARCHAR(6),
    @WORK_CODE          VARCHAR(6),
    @WORK_NAME          VARCHAR(8),
    @VIEW_SEQ           VARCHAR(10),
    @DELETE_FLAG        VARCHAR(1)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT FACTORY_CODE
         , WORK_CODE
         , WORK_NAME
         , VIEW_SEQ
         , DELETE_FLAG
    FROM   HHR101
    WHERE  ISNULL(DELETE_FLAG, '0') <> '1'
    ORDER BY TRY_CAST(VIEW_SEQ AS INT) ASC;
END
```

→ LIST 1 프로시저


```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_HHR102_LIST]    Script Date: 2025-08-11 오후 2:14:03 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_HHR102_LIST]
    @FACTORY_CODE   VARCHAR(6),
    @WORK_CODE      VARCHAR(6),
    @LINE_CODE      VARCHAR(3),
    @LINE_NAME      VARCHAR(8),
    @VIEW_SEQ       VARCHAR(10),
    @DELETE_FLAG    VARCHAR(1)
AS
BEGIN
    SELECT
       B.FACTORY_CODE
     , B.WORK_CODE
     , A.LINE_CODE
     , A.LINE_NAME
     , A.VIEW_SEQ
     , B.DELETE_FLAG

    FROM  HHR102 A
         LEFT JOIN HHR101 B
         ON A.WORK_CODE = B.WORK_CODE

    WHERE
         B.FACTORY_CODE =  @FACTORY_CODE
         AND A.WORK_CODE = @WORK_CODE
         AND ISNULL(A.DELETE_FLAG, '0') <> '1'
         AND ISNULL(B.DELETE_FLAG, '0') <> '1'
    ORDER BY TRY_CAST(A.VIEW_SEQ AS INT) ASC;
END
```

[[→ LIST 2 프로시저]]

```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_HHR101_IUD]    Script Date: 2025-08-18 오전 10:29:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_HHR101_IUD]
    @FACTORY_CODE VARCHAR(6),
    @WORK_CODE    VARCHAR(6),
    @WORK_NAME    VARCHAR(20),
    @VIEW_SEQ     VARCHAR(10),
    @IUD          VARCHAR(2)
AS
BEGIN
    SET NOCOUNT ON;

    IF @IUD = 'IU'
    BEGIN
        UPDATE HHR101
        SET
            WORK_NAME = @WORK_NAME,
            VIEW_SEQ  = @VIEW_SEQ
        WHERE
            FACTORY_CODE  = @FACTORY_CODE
            AND WORK_CODE = @WORK_CODE

        IF @@ROWCOUNT = 0
            BEGIN 
                IF @WORK_CODE = ''
                    BEGIN
                        SELECT @WORK_CODE = RIGHT('000000' + CAST(CAST(ISNULL(MAX(WORK_CODE),'0') AS INT) + 1 AS VARCHAR(6)),6) 
                        FROM   HHR101
                        WHERE  FACTORY_CODE = @FACTORY_CODE
                    END

            INSERT INTO HHR101 (
                FACTORY_CODE,
                WORK_CODE,
                WORK_NAME,
                VIEW_SEQ
            ) VALUES (
                @FACTORY_CODE,
                @WORK_CODE,
                @WORK_NAME,
                NEXT VALUE FOR seq_view_seq
            );
        END
    END

    ELSE IF @IUD = 'D'
    BEGIN
        UPDATE HHR101
        SET DELETE_FLAG = '1'
        WHERE
            FACTORY_CODE  = @FACTORY_CODE
            AND WORK_CODE = @WORK_CODE;

        UPDATE HHR102
        SET DELETE_FLAG = '1'
        WHERE
            FACTORY_CODE  = @FACTORY_CODE
            AND WORK_CODE = @WORK_CODE;
    END
END
```

→ IUD 1 프로시저 (임시)

```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_HHR102_IUD]    Script Date: 2025-08-18 오전 10:29:26 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_HHR102_IUD]
    @FACTORY_CODE VARCHAR(6),
    @WORK_CODE    VARCHAR(6),
    @LINE_CODE    VARCHAR(3),
    @LINE_NAME    VARCHAR(50),
    @VIEW_SEQ     VARCHAR(10),
    @DELETE_FLAG  VARCHAR(1),
    @IUD          VARCHAR(2)
AS
BEGIN
    SET NOCOUNT ON;

    IF @IUD = 'IU'
    BEGIN
        UPDATE HHR102
        SET
            LINE_NAME   = @LINE_NAME,
            VIEW_SEQ    = @VIEW_SEQ,
            DELETE_FLAG = @DELETE_FLAG
        WHERE
            FACTORY_CODE     = @FACTORY_CODE 
            AND WORK_CODE    = @WORK_CODE 
            AND LINE_CODE    = @LINE_CODE;

        IF @@ROWCOUNT = 0
         BEGIN
            IF @LINE_CODE = ''
                BEGIN
                    SELECT @LINE_CODE = RIGHT('000' + CAST(CAST(ISNULL(MAX(LINE_CODE),'0') AS INT) + 1 AS VARCHAR(3)),3)
                    FROM   HHR102
                    WHERE  WORK_CODE = @WORK_CODE
                END

            INSERT INTO HHR102 (
                FACTORY_CODE,
                WORK_CODE,
                LINE_CODE,
                LINE_NAME,
                VIEW_SEQ,
                DELETE_FLAG
            ) VALUES (
                @FACTORY_CODE,
                @WORK_CODE,
                @LINE_CODE,
                @LINE_NAME,
                NEXT VALUE FOR seq_view_seq,
                @DELETE_FLAG
            );
        END
    END

    ELSE IF @IUD = 'D'
    BEGIN
        UPDATE HHR102
        SET DELETE_FLAG = '1'
        WHERE
            FACTORY_CODE     = @FACTORY_CODE 
            AND WORK_CODE    = @WORK_CODE 
            AND LINE_CODE    = @LINE_CODE;
    END
END

```

→ IUD 2 프로시저 (임시)


```html
<%@ page contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<%@ page import="java.util.*"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt"%>
<%@ page import="com.report.model.edu.*"%>
<jsp:useBean id="dao" class="com.report.service.edu.EduService" />


<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="shortcut icon" type="image/x-icon" href="../resources/images/icon/report.ico" />
<link rel="stylesheet" href="../resources/css/report.css" />
<script src="../resources/js/report.js"></script>
<title>호기목록 출력</title>

<style type="text/css">
@import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@700&display=swap')
	;

body {
	width: 100%;
	height: 100%;
	margin: 0;
	padding: 0;
	font: "굴림", Malgun Gothic, Tahoma;
	font-size: 12px;
}

* {
	box-sizing: border-box;
	-moz-box-sizing: border-box;
	margin: 0;
	padding: 0;
}


    ul li {
	list-style: none;
}

.clear {
	clear: both;
}

.base_table table, .base_table_blue table {
	border-collapse: collapse;
	table-layout: fixed;
	margin-bottom: 0px;
	width: 100%;
}

.base_table04 table, .base_table04_blue table {
	border-collapse: collapse;
	table-layout: fixed;
	margin-bottom: 4px;
}

.base_table table {
	border: 1px solid #c36f6f;
}

.base_table_blue table {
	border: 1px solid #2116ff !important;
}

.base_table th, .base_table_blue th {
	border-bottom: 1px solid #c36f6f;
	padding: 0px;
	text-align: center;
	vertical-align: middle;
	font-size: 12px;
	font-weight: 500;
	color: #a92424;
}

.base_table_blue th {
	border-bottom: 1px solid #2116ff !important;
	color: #2116ff !important;
}

.base_table td, .base_table_blue td {
	border-bottom: none;
	padding: 0px 2px;
	height: 16px;
	font-size: 12px;
	vertical-align: middle;
	color: #000;
}

.wt02 table, .wt04 table {
	border: none !important;
}

.wt02 td, .wt02 th {
	border-bottom: 1px solid #c36f6f;
	border-right: 1px solid #c36f6f;
	border-left: 1px solid #c36f6f;
}

.wt04 td, .wt04 th {
	border-bottom: 1px solid #2116ff !important;
	border-right: 1px solid #2116ff !important;
	border-left: 1px solid #2116ff !important;
}

.base_table04 th, .base_table04_blue th {
	border: 1px solid #c36f6f;
	padding: 0px 1px;
	text-align: center;
	vertical-align: middle;
	font-size: 11px;
	line-height: 12px;
	font-weight: 500;
	color: #a92424;
}

.base_table04_blue th {
	border: 1px solid #2116ff;
	color: #2116ff;
}

.base_table04 td, .base_table04_blue td {
	border: 1px solid #c36f6f;
	text-align: left;
	padding: 0px 5px;
	text-align: center;
	font-size: 12px;
	line-height: 14px;
	vertical-align: middle;
	color: #a92424;
	font-weight: 400;
}

.base_table04_blue td {
	border: 1px solid #2116ff;
	color: #2116ff;
}

.wt01 td:nth-child(4), .wt01 td:nth-child(5), .wt01 td:nth-child(3),
	.wt01 th:nth-child(4), .wt01 th:nth-child(5), .wt01 th:nth-child(3),
	.wt03 td:nth-child(4), .wt03 td:nth-child(5), .wt03 td:nth-child(3),
	.wt03 th:nth-child(4), .wt03 th:nth-child(5), .wt03 th:nth-child(3) {
	text-align: right !important;
}

.wt01 th:nth-child(1), .wt01 th:nth-child(2), .wt03 th:nth-child(1),
	.wt03 th:nth-child(2) {
	text-align: left !important;
}

.wt01 td:nth-child(5), .wt01 th:nth-child(5), .wt01 td:nth-child(1),
	.wt01 th:nth-child(1), .wt03 td:nth-child(5), .wt03 th:nth-child(5),
	.wt03 td:nth-child(1), .wt03 th:nth-child(1) {
	padding-right: 10px;
	padding-left: 10px;
}

.wt02 td:nth-child(2), .wt02 td:nth-child(3), .wt02 td:nth-child(4),
	.wt02 td:nth-child(5), .wt04 td:nth-child(2), .wt04 td:nth-child(3),
	.wt04 td:nth-child(4), .wt04 td:nth-child(5) {
	text-align: right !important;
}

.wt02 td:nth-child(1), .wt04 td:nth-child(1) {
	text-align: left;
}

.page {
	width: 21cm;
	min-height: 29.7cm;
	padding: 1.25cm;
	margin: 1cm auto;
	border-radius: 5px;
	box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

@media print {
	.page {
		margin: 0;
		padding-top: 70px;
		border: initial;
		border-radius: initial;
		width: initial;
		min-height: initial;
		box-shadow: initial;
		background: initial;
		page-break-after: always;
	}
}

@page {
	size: A4;
	margin: 0;
}
</style>
</head>

<body>
	<% 	
		ServletContext sc = this.getServletContext(); 
		List<Edu4_1Model> firstList = dao.getFirstList(request, getServletContext());
		List<Edu4_2Model> secondList = dao.getSecondList(request, getServletContext());
		
		request.setAttribute("firstList", firstList);
	    request.setAttribute("secondList", secondList);
	%>

	<div class="page">
		<div class="btn no-print-page">
			<a onclick="printDiv('printableArea')"><button>인쇄</button></a>
			<a onclick="javascript:self.close()"><button>닫기</button></a>
		</div>
		<div style="margin-bottom: 8mm;">
			<div class="base_table04 mg_1p clear">
				<table>
					<tr>
						<th style="width: 3px; border-top: none; border-left: none; border-bottom: none;" rowspan="4"></th>
						<th style="width: 16px;" rowspan="4">공</th>
						<th>사업자번호</th>
						<td colspan="3">109-81-32545</td>
					</tr>
				</table>
			</div>

			<div class="base_table wt01">
				<table>
					<colgroup>
						<col style="width: 80px;">
						<col style="width: 90px;">
						<col style="width: 20px;">
					</colgroup>
					<thead>
						<tr>
							<th>[호기코드]</th>
							<th>[호기명]</th>
							<th>[작업수]</th>
						</tr>
					</thead>
					<tbody>
						<c:choose>
							<c:when test="${not empty secondList}">
								<c:forEach var="row" items="${secondList}">
									<tr>
										<td>
											<c:out value="${row.LINE_CODE}" />
										</td>
										<td>
											<c:out value="${row.LINE_NAME}" />
										</td>
										<td>
											<fmt:formatNumber value="12345" pattern="#,###" />
										</td>
									</tr>
								</c:forEach>
							</c:when>
							<c:otherwise>
								<tr>
									<td colspan="3" style="text-align:center;"> [server] 호기 데이터가 없습니다. </td>
								</tr>
							</c:otherwise>
						</c:choose>
					</tbody>


				</table>
			</div>
		</div>
	</div>
</body>

</html>
```

→ JSP 수정필요


```java
package com.edu;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.List;

import javax.servlet.GenericServlet;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServletRequest;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;
import org.apache.poi.ss.usermodel.*;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.etc.ResponseCode;

@WebServlet("/com/edu/Test5_EXCEL_UPLOAD")
public class Test5_EXCEL_UPLOAD extends GenericServlet {
	private static final long serialVersionUID = 1L;

	@Override
	public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {

		String strMsg = "";
		String systemMsg = "";
		String strSuccess = "true";

		JSONArray itemList = new JSONArray();
		JSONObject returnObject = new JSONObject();

		try {
			String factoryCode = (request.getParameter("FACTORY_CODE"));
			DataFormatter formatter = new DataFormatter();

			List<FileItem> multiparts = new ServletFileUpload(new DiskFileItemFactory())
					.parseRequest((HttpServletRequest) request);
			Workbook tempWorkbook = null;

			for (FileItem item : multiparts) {
				if (!item.isFormField()) {
					tempWorkbook = WorkbookFactory.create(item.getInputStream());
					break;
				} else {
					if ("FACTORY_CODE".equalsIgnoreCase(item.getFieldName()) && (factoryCode == null || factoryCode.isEmpty())) {
						factoryCode = sanitizeInput(item.getString("UTF-8"));
					}
				}
			}

			try (Workbook workbook = tempWorkbook) {
				Sheet sheet = workbook.getSheetAt(0);

				int rows = 0;
				for (Row row : sheet) {
					if (rows >= 1) {
						int cells = row.getLastCellNum();
						JSONObject cellJson = new JSONObject();

						for (int columnindex = 0; columnindex < cells; columnindex++) {
							Cell cell = row.getCell(columnindex);
							if (cell != null) {
								String value = formatter.formatCellValue(cell).trim();
								cellJson.put(columnindex, sanitizeInput(value));
							}
						}

						String workCode = cellJson.get(0) == null ? "" : (String) cellJson.get(0);
						String workName = cellJson.get(1) == null ? "" : (String) cellJson.get(1);
						String lineCode = cellJson.get(2) == null ? "" : (String) cellJson.get(2);
						String lineName = cellJson.get(3) == null ? "" : (String) cellJson.get(3);
						
						if ((workCode + workName + lineCode + lineName).isEmpty()) {
							rows += 1;
							continue;
						}

						JSONObject tempJson = new JSONObject();
						tempJson.put("FACTORY_CODE", factoryCode == null ? "" : factoryCode);
						tempJson.put("WORK_CODE",   workCode);
						tempJson.put("WORK_NAME",   workName);
						tempJson.put("LINE_CODE",   lineCode);
						tempJson.put("LINE_NAME",   lineName);
						String vFlag = "0";
						String vName = "정상";
						if (workCode.isEmpty()) { vFlag = "1"; vName = "공정코드 없음"; }
						else if (workName.isEmpty()) { vFlag = "1"; vName = "공정이름 없음"; }
						else if (lineCode.isEmpty()) { vFlag = "1"; vName = "호기코드 없음"; }
						else if (lineName.isEmpty()) { vFlag = "1"; vName = "호기명 없음"; }


						tempJson.put("VALIDATION_FLAG", vFlag);
						tempJson.put("VALIDATION_NAME", vName);
						System.out.println(vName);
						itemList.add(tempJson);
					}
					rows += 1;
				}
				workbook.close();
			}
		} catch (Exception e) {
			strSuccess = "false";
			systemMsg = e.toString();

			if (systemMsg.contains(":")) {
				String string[] = systemMsg.split(":");
				systemMsg = string.length > 1 ? string[1] : systemMsg;
			}

			strMsg = extractErrorMessage(e, systemMsg);
		}

		returnObject.put("success", strSuccess);
		returnObject.put("message", strMsg);
		returnObject.put("data", itemList);

		response.setContentType("text/html; charset=UTF-8");
		try (PrintWriter out = response.getWriter()) {
			out.print(returnObject);
		}
	}

	private Connection getConnection(ServletRequest request) throws Exception {
		ServletContext sc = this.getServletContext();
		Class.forName(sc.getInitParameter("driver")).newInstance();
		return DriverManager.getConnection(
			sc.getInitParameter("url"),
			sc.getInitParameter("username"),
			sc.getInitParameter("password")
		);
	}

	private String sanitizeInput(String input) {
		return (input == null) ? "" : input.trim().replace("'", "''");
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

→ EXEL_UPLOADER 서블릿


```java
package com.edu;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Iterator;

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

@WebServlet("/com/edu/Test5_EXCEL_IUD")
public class Test5_EXCEL_IUD extends HttpServlet {
	private static final long serialVersionUID = 1L;

	@Override
	public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {

		Connection conn = null;
		PreparedStatement stmt = null;
		ResultSet rs = null;

		String query = "";
		String data;

		JSONArray itemList = new JSONArray();

		try {
			ServletContext sc = this.getServletContext();

			Class.forName(sc.getInitParameter("driver")).newInstance();
			conn = DriverManager.getConnection(sc.getInitParameter("url"), sc.getInitParameter("username"), sc.getInitParameter("password"));
			request.setCharacterEncoding("UTF-8");

			data = (String) request.getParameter("data");
			System.out.println(data);
			if (data != null) {
                JSONArray array;
                if (data.startsWith("{")) {
                    JSONParser parser = new JSONParser();
                    JSONObject jsonObject = (JSONObject) parser.parse(data);
                    array = new JSONArray();
                    array.add(jsonObject);
                } else {
                    array = (JSONArray) JSONValue.parse(data);
                }

                Iterator<JSONObject> iterator = array.iterator();
                while (iterator.hasNext()) {
                    JSONObject jsonobj = iterator.next();

                    query = "EXEC SP_HHR102_EXCEL_UPLOAD"   +
                        "\r\n@FACTORY_CODE  = 		'" + jsonobj.get("FACTORY_CODE").toString().replace("'", "''") + "'," +
                        "\r\n@WORK_CODE 	= 		'" + jsonobj.get("WORK_CODE").toString().replace("'", "''") + "'," +
                        "\r\n@WORK_NAME 	= 		'" + jsonobj.get("WORK_NAME").toString().replace("'", "''") + "'," +
                        "\r\n@LINE_CODE 	= 		'" + jsonobj.get("LINE_CODE").toString().replace("'", "''") + "'," +
                        "\r\n@LINE_NAME 	= 		'" + jsonobj.get("LINE_NAME").toString().replace("'", "''") + "'," +
                        "\r\n@VIEW_SEQ	 	=	 	'" + (jsonobj.get("VIEW_SEQ") 	 == null ? "0" : jsonobj.get("VIEW_SEQ").toString()) + "'," +
                        "\r\n@DELETE_FLAG 	=	 	'" + (jsonobj.get("DELETE_FLAG") == null ? "0" : jsonobj.get("DELETE_FLAG").toString()) + "'," +
                        "\r\n@IUD 			= 		'" + jsonobj.get("IUD") + "'";

                    System.out.println(query);
                    stmt = conn.prepareStatement(query);
                    stmt.executeUpdate();
                }

                itemList.clear();
                JSONObject successJson = new JSONObject();
                successJson.put("success", "true");
                successJson.put("message", "IUD 처리 완료");
                itemList.add(successJson);
            }

		} catch (Exception e) {
			throw new ServletException(e);

		} finally {
			try {
				if (rs != null)
					rs.close();
			} catch (Exception e) {
			}
			try {
				if (stmt != null)
					stmt.close();
			} catch (Exception e) {
			}
			try {
				if (conn != null)
					conn.close();
			} catch (Exception e) {
			}
			JSONObject tempJson = new JSONObject();
			tempJson.put("success", "false");
			tempJson.put("message", "Error message goes here.");
			itemList.add(tempJson);
		}

		
		PrintWriter out = response.getWriter();
		out.print(itemList);
		out.flush();
		out.close();
	}
}
```

→ EXCEL_IUD

```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_HHR102_EXCEL_UPLOAD]    Script Date: 2025-08-12 오전 10:38:07 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_HHR102_EXCEL_UPLOAD]
@FACTORY_CODE VARCHAR(6),
@WORK_CODE    VARCHAR(6),
@WORK_NAME    VARCHAR(8),
@LINE_CODE    VARCHAR(3),
@LINE_NAME    VARCHAR(50),
@VIEW_SEQ     VARCHAR(10),
@DELETE_FLAG  VARCHAR(1),
@IUD          CHAR(2)
AS
BEGIN
SET NOCOUNT ON;
BEGIN
INSERT INTO HHR101(
FACTORY_CODE,
WORK_CODE,
WORK_NAME,
VIEW_SEQ,
DELETE_FLAG
) VALUES (
@FACTORY_CODE,
@WORK_CODE,
@WORK_NAME,
NEXT VALUE FOR seq_view_seq,
@DELETE_FLAG
);
END
BEGIN
INSERT INTO HHR102 (
FACTORY_CODE,
WORK_CODE,
LINE_CODE,
LINE_NAME,
VIEW_SEQ,
DELETE_FLAG
) VALUES (
@FACTORY_CODE,
@WORK_CODE,
NEXT VALUE FOR seq_list,
@LINE_NAME,
NEXT VALUE FOR seq_view_seq,
@DELETE_FLAG
);
END
END
```

→ Exel_Upload 프로시저


---

결과화면


![[스크린샷_2025-08-12_125126.png]]

![[스크린샷_2025-08-12_125142.png]]

![[image 54.png]]

![[image 55.png]]

![[스크린샷_2025-08-12_125545.png]]

![[스크린샷_2025-08-12_125605.png]]

![[스크린샷_2025-08-12_125622.png]]

![[image 56.png]]