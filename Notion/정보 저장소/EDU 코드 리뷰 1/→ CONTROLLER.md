---

---
```javascript
Ext.define('AppTest1.view.GW.WGW500.test5Controller', {
  extend: 'Ext.app.ViewController',
  alias: 'controller.test5',

  requires: ['AppTest1.store.GW.WGW500.test5'],

  rRecord: false,

  init: function () {
    var me = this;
    me.control({
      '#grid_01': {
        select: 'onSelect',
        viewready: 'onMasterViewReady'
      },
      '#grid_02': {
        viewready: 'onDetailViewReady'
      }
    });
    me.isPendingSave = false;
  },

  normKey: function (v) {
  var s = (v || '').toString();
  return s.replace(/\s+/g, '').toUpperCase();              // 모든 공백 제거 + 대소문자 무시
},


  onSelect: function (rowModel, record) {
    var me = this;
    me.rRecord = record;

    var workCode = record.get('WORK_CODE');
    var detailStore = me.getViewModel().getStore('store_02');

    detailStore.load({
      params: {
        WORK_CODE: workCode,
        DELETE_FLAG: '0',
        FACTORY_CODE: gFactoryCode,
        VIEW_SEQ: '0'
      }
    });
  },

  onView: function () {
    var me = this;
    var store = me.getViewModel().getStore('store_01');
    store.load({
      callback: function (records, op, success) {
        if (success) {
          Ext.Msg.alert('정보', '조회 완료');
        } else {
          store.removeAll();
          store.clearData();
        }
      }
    });
  },

  onNew: function () {
    var me = this;
    var grid = me.getView().down('#grid_01');
    var store = grid.getStore();

    var isPendingSave = store.findBy(function (record) {
      return !record.get('WORK_CODE') || !record.get('WORK_NAME');
    }) !== -1;

    if (isPendingSave) {
      Ext.Msg.alert('정보', '이미 등록중인 공정항목이 존재합니다.');
      return;
    }

    var record = { FACTORY_CODE: gFactoryCode, WORK_CODE: '', WORK_NAME: '', VIEW_SEQ: ''};
    store.add(record);
  },

  onReg: function () {
  var me    = this;
  var grid  = me.getView().down('#grid_01');
  var store = grid.getStore();

  var modified = store.getModifiedRecords();
  var removed  = store.getRemovedRecords();
  if (modified.length === 0 && removed.length === 0) {
    Ext.Msg.alert('정보', '변경된 데이터가 없습니다.');
    return;
  }

  var seen  = {};
  var valid = true;

  for (var i = 0; i < store.getCount(); i++) {
    var rec  = store.getAt(i);
    if (rec.get('DELETE') === true) continue;

    var fac  = (rec.get('FACTORY_CODE') || gFactoryCode || '').toString().trim();
    var name = (rec.get('WORK_NAME')    || '').toString().trim();
    var code = (rec.get('WORK_CODE')    || '').toString().trim();

    if (!name) {
      Ext.Msg.alert('정보', '공정명은 필수입니다.');
      valid = false;
      break;
    }

    var key  = fac + '||' + me.normKey(name);
    var prev = seen[key];

    if (!prev) {
      seen[key] = { idx: i, code: code };
      continue;
    }

    var sameCode = (prev.code === code);
    var bothNew  = (!prev.code && !code && prev.idx !== i);

    if (!sameCode || bothNew) {
      Ext.Msg.alert('정보', '중복 공정명입니다: ' + name);
      valid = false;
      break;
    }
  }

  if (!valid) return;

  for (var k = 0; k < store.getCount(); k++) {
    var rec2 = store.getAt(k);
    if (!rec2.get('WORK_NAME')) continue;

    if (rec2.dirty) {
      rec2.set('FACTORY_CODE', gFactoryCode);
      rec2.set('IUD', 'IU');
    }
  }

  var selModel  = grid.getSelectionModel();
  var selRec    = selModel.getSelection()[0] || null;
  var keepCode  = selRec ? (selRec.get('WORK_CODE') || '').toString().trim() : null;
  var keepIndex = selRec ? store.indexOf(selRec) : -1;

  store.sync({
    success: function () {
      Ext.Msg.alert('정보', '저장되었습니다.');
      store.reload({
        callback: function () {
          var rec = null;

          if (keepCode) {
            var idxByCode = store.findExact('WORK_CODE', keepCode);
            if (idxByCode !== -1) rec = store.getAt(idxByCode);
          }
          if (!rec && keepIndex >= 0 && keepIndex < store.getCount()) {
            rec = store.getAt(keepIndex);
          }

          if (rec) {
            selModel.select(rec, false, true);
            var rowIdx = store.indexOf(rec);
            if (rowIdx >= 0) {
              grid.getView().focusRow(rowIdx);
              grid.getView().ensureVisible(rowIdx);
            }
          }
        }
      });
    }
  });
},


  onDelete: function () {
    var me = this;
    var grid = me.getView().down('#grid_01');
    var store = grid.getStore();
    let selected = store.queryBy(r => r.get('DELETE') === true);

    if (selected.length === 0) {
      Ext.Msg.alert('정보', '삭제할 항목을 선택하세요.');
      return;
    }

    selected.each(function (r) { r.set('IUD', 'D'); });

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
      VIEW_SEQ: '',
      FACTORY_CODE: gFactoryCode,
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

  var seen  = {};
    var valid = true;
   
  for (var i = 0; i < store.getCount(); i++) {
    var rec   = store.getAt(i);
    if (rec.get('DELETE') === true) continue;

    var fac   = (rec.get('FACTORY_CODE') || gFactoryCode || '').toString().trim();
    var wcode = (rec.get('WORK_CODE')    || '').toString().trim();
    var lname = (rec.get('LINE_NAME')    || '').toString().trim();
    var lcode = (rec.get('LINE_CODE')    || '').toString().trim();
    
    if (!wcode) {
      Ext.Msg.alert('정보', '상위 공정코드가 없습니다. 먼저 공정을 선택하세요.');
      valid = false;
      break;
    }
    if (!lname) {
      Ext.Msg.alert('정보', '호기명은 필수입니다.');
      valid = false;
      break;
    }

    var key  = fac + '||' + me.normKey(lname);
    var prev = seen[key];

    if (!prev) {
      seen[key] = { idx: i, code: lcode };
      continue;
    }

    var sameCode = (prev.code === lcode);
    var bothNew  = (!prev.code && !lcode && prev.idx !== i);

    if (!sameCode || bothNew) {
      Ext.Msg.alert('정보', '중복 호기명입니다: ' + lname);
      valid = false;
      break;
    }
  }

  if (!valid) return;

  for (var j = 0; j < store.getCount(); j++) {
    var rec2 = store.getAt(j);
    if (!rec2.get('LINE_NAME')) continue;

    if (rec2.dirty) {
      rec2.set('FACTORY_CODE', gFactoryCode);
      rec2.set('IUD', 'IU');
    }
    }

  var selModel  = grid.getSelectionModel();
  var selRec    = selModel.getSelection()[0] || null;
  var keepCode  = selRec ? (selRec.get('LINE_CODE') || '').toString().trim() : null;
  var keepIndex = selRec ? store.indexOf(selRec) : -1;

  store.sync({
    success: function () {
      Ext.Msg.alert('정보', '저장되었습니다.');
      store.reload({
        callback: function () {
          var rec = null;
          if (keepCode) {
            var idxByCode = store.findExact('LINE_CODE', keepCode);
            if (idxByCode !== -1) rec = store.getAt(idxByCode);
          }
          if (!rec && keepIndex >= 0 && keepIndex < store.getCount()) {
            rec = store.getAt(keepIndex);
          }

          if (rec) {
            selModel.select(rec, false, true);
            var rowIdx = store.indexOf(rec);
            if (rowIdx >= 0) {
              grid.getView().focusRow(rowIdx);
              grid.getView().ensureVisible(rowIdx);
            }
          }
        }
      });
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
      Ext.Msg.alert('정보', '부모 행을 먼저 선택하세요.');
      return;
    }

    var childGrid  = me.getView().down('#grid_02');
    var childStore = childGrid ? childGrid.getStore() : null;
    if (!childStore || childStore.getCount() === 0) {
      Ext.Msg.alert('정보', '해당 부모에 대한 자식 데이터가 없습니다.');
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
      Ext.Msg.alert('정보', '전송할 자식 데이터가 없습니다.');
      return;
    }

    var reportForm = document.getElementById('viewerFormTest5');
    if (!reportForm) {
      Ext.Msg.alert('오류', 'view 호출 실패');
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
          { text: '공정이름',       dataIndex: 'WORK_NAME',    flex:  1,   editor: { xtype: 'textfield', allowBlank: false } },
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

```javascript
Ext.define('AppTest1.view.GW.WGW500.test5Controller', {
  extend: 'Ext.app.ViewController',
  alias : 'controller.test5',

  requires: ['AppTest1.store.GW.WGW500.test5'],

  //=========================
  // 상태값
  //=========================
  rRecord: false,   // 선택된 마스터 레코드 보관

  //=========================
  // 헬퍼(축약)
  //=========================
  // N: trim 문자열, K: 공백제거+대문자(중복키용)
  N: function (v) { return (v || '').toString().trim(); },
  K: function (v) { return (v || '').toString().replace(/\s+/g, '').toUpperCase(); },

  //=========================
  // 라이프사이클
  //=========================
  init: function () {
    var me = this;
    me.control({
      '#grid_01': {
        select   : 'onSelectMaster',     // 마스터 선택 시 디테일 로드
        viewready: 'onMasterViewReady'   // DnD drop 바인딩
      },
      '#grid_02': {
        viewready: 'onDetailViewReady'   // DnD drop 바인딩
      }
    });
  },

  //=========================
  // 마스터-디테일 연동
  //=========================
  onSelectMaster: function (rowModel, record) {
    var me = this;
    me.rRecord = record;

    var workCode    = record.get('WORK_CODE');
    var detailStore = me.getViewModel().getStore('store_02');

    detailStore.load({
      params: {
        WORK_CODE   : workCode,
        DELETE_FLAG : '0',
        FACTORY_CODE: gFactoryCode,
        VIEW_SEQ    : '0'
      }
    });
  },

  // 조회(마스터)
  onView: function () {
    var me    = this;
    var store = me.getViewModel().getStore('store_01');

    store.load({
      callback: function (recs, op, ok) {
        if (ok) Ext.Msg.alert('정보', '조회 완료');
        else {
          store.removeAll();
          store.clearData();
        }
      }
    });
  },

  // 신규(마스터)
  onNew: function () {
    var me    = this;
    var grid  = me.getView().down('#grid_01');
    var store = grid.getStore();

    // 아직 입력 중인 빈 필드가 있으면 추가 금지
    var hasPending = store.findBy(function (r) {
      return !r.get('WORK_CODE') || !r.get('WORK_NAME');
    }) !== -1;

    if (hasPending) {
      Ext.Msg.alert('정보', '이미 등록중인 공정항목이 존재합니다.');
      return;
    }

    store.add({
      FACTORY_CODE: gFactoryCode,
      WORK_CODE   : '',
      WORK_NAME   : '',
      VIEW_SEQ    : ''
    });
  },

  // 신규(디테일)
  onNewDetail: function () {
    var me     = this;
    var grid   = me.getView().down('#grid_02');
    var store  = grid.getStore();
    var master = me.rRecord;

    if (!master) {
      Ext.Msg.alert('정보', '상위 공정을 먼저 선택하세요.');
      return;
    }

    store.add({
      LINE_CODE   : '',
      LINE_NAME   : '',
      WORK_CODE   : master.get('WORK_CODE'),
      VIEW_SEQ    : '',
      FACTORY_CODE: gFactoryCode
    });
  },

  //=========================
  // 저장(중복검사 + IUD 세팅)
  //=========================
  // 마스터 저장
  onReg: function () {
    var me   = this;
    var N    = me.N, K = me.K;
    var grid = me.getView().down('#grid_01');
    var s    = grid.getStore();

    var changed = s.getModifiedRecords().length || s.getRemovedRecords().length;
    if (!changed) { Ext.Msg.alert('정보', '변경된 데이터가 없습니다.'); return; }

    // 중복키: (FACTORY_CODE + WORK_NAME[정규화])
    var seen = {};
    for (var i = 0; i < s.getCount(); i++) {
      var r = s.getAt(i);
      if (r.get('DELETE') === true) continue;

      var fac  = N(r.get('FACTORY_CODE') || gFactoryCode);
      var name = N(r.get('WORK_NAME'));
      if (!name) { Ext.Msg.alert('정보', '공정명은 필수입니다.'); return; }

      var key = fac + '||' + K(name);
      if (seen[key]) { Ext.Msg.alert('정보', '중복 공정명: ' + name); return; }
      seen[key] = 1;

      if (r.dirty) {
        r.set('FACTORY_CODE', gFactoryCode);
        if (!r.get('IUD')) r.set('IUD', 'IU');
      }
    }

    s.sync({
      success: function () {
        Ext.Msg.alert('정보', '저장되었습니다.');
        s.reload();
      }
    });
  },

  // 디테일 저장
  onRegDetail: function () {
    var me   = this;
    var N    = me.N, K = me.K;
    var grid = me.getView().down('#grid_02');
    var s    = grid.getStore();

    var changed = s.getModifiedRecords().length || s.getRemovedRecords().length;
    if (!changed) { Ext.Msg.alert('정보', '변경된 데이터가 없습니다.'); return; }

    // 중복키: (FACTORY_CODE + WORK_CODE + LINE_NAME[정규화])
    var seen = {};
    for (var i = 0; i < s.getCount(); i++) {
      var r = s.getAt(i);
      if (r.get('DELETE') === true) continue;

      var fac = N(r.get('FACTORY_CODE') || gFactoryCode);
      var w   = N(r.get('WORK_CODE'));
      var ln  = N(r.get('LINE_NAME'));

      if (!w)  { Ext.Msg.alert('정보', '상위 공정코드가 없습니다.'); return; }
      if (!ln) { Ext.Msg.alert('정보', '호기명은 필수입니다.'); return; }

      var key = fac + '||' + w + '||' + K(ln);
      if (seen[key]) { Ext.Msg.alert('정보', '중복 호기명: ' + ln); return; }
      seen[key] = 1;

      if (r.dirty) {
        r.set('FACTORY_CODE', gFactoryCode);
        if (!r.get('IUD')) r.set('IUD', 'IU');
      }
    }

    s.sync({
      success: function () {
        Ext.Msg.alert('정보', '저장되었습니다.');
        s.reload();
      }
    });
  },

  //=========================
  // 삭제(IUD='D')
  //=========================
  onDelete: function () {
    var me   = this;
    var grid = me.getView().down('#grid_01');
    var s    = grid.getStore();

    var selected = s.queryBy(function (r) { return r.get('DELETE') === true; });
    if (selected.length === 0) {
      Ext.Msg.alert('정보', '삭제할 항목을 선택하세요.');
      return;
    }

    selected.each(function (r) { r.set('IUD', 'D'); });

    Ext.Msg.confirm('확인', '정말 삭제하시겠습니까?', function (btn) {
      if (btn !== 'yes') return;
      s.sync({
        success: function () {
          Ext.Msg.alert('정보', '삭제되었습니다.');
          s.reload();
        }
      });
    });
  },

  onDeleteDetail: function () {
    var me   = this;
    var grid = me.getView().down('#grid_02');
    var s    = grid.getStore();

    var selected = s.queryBy(function (r) { return r.get('DELETE') === true; });
    if (selected.length === 0) {
      Ext.Msg.alert('정보', '삭제할 항목을 선택하세요.');
      return;
    }

    selected.each(function (r) { r.set('IUD', 'D'); });

    Ext.Msg.confirm('확인', '정말 삭제하시겠습니까?', function (btn) {
      if (btn !== 'yes') return;
      s.sync({
        success: function () {
          Ext.Msg.alert('정보', '삭제되었습니다.');
          s.reload();
        }
      });
    });
  },

  //=========================
  // DnD: 구간만 VIEW_SEQ 재부여
  //=========================
  // (핵심1) 영향 구간 계산: 뷰 순서 기준, 삭제행 제외, 제자리 드롭 방지
  getRange: function (view, data, overModel, dropPos) {
    var vStore = (view.store || view.getStore());
    if (!vStore) return null;

    // 드래그된 레코드들의 "뷰 인덱스" 수집
    var draggedIdx = [];
    Ext.Array.each(data.records || [], function (r) {
      if (r.get('DELETE') === true) return;
      var i = vStore.indexOf(r);
      if (i >= 0) draggedIdx.push(i);
    });
    if (!draggedIdx.length) return null;

    var minD = Math.min.apply(Math, draggedIdx);
    var maxD = Math.max.apply(Math, draggedIdx);

    // 떨어뜨릴 목표 인덱스(뷰 기준)
    var toIdx;
    if (!overModel) {
      toIdx = vStore.getCount() - 1;
    } else {
      var over = vStore.indexOf(overModel);
      toIdx = (dropPos === 'after') ? over + 1 : over;
      toIdx = Ext.Number.constrain(toIdx, 0, vStore.getCount() - 1);
    }

    // 같은 블록을 제자리로 떨군 경우 → 변화 없음으로 처리
    var sameBlock = (toIdx >= minD && toIdx <= maxD) &&
                    (draggedIdx.length === (maxD - minD + 1));
    if (sameBlock) return null;

    var start = Math.min(minD, toIdx);
    var end   = Math.max(maxD, toIdx + draggedIdx.length - 1);

    return {
      start: Ext.Number.constrain(start, 0, vStore.getCount() - 1),
      end  : Ext.Number.constrain(end  , 0, vStore.getCount() - 1)
    };
  },

  // (핵심2) 지정 구간만 재번호: 바뀐 행만 IUD='IU' (+필요 필드 세팅)
  reseq: function (grid, seqField, range, extraSetter) {
    if (!range) return;

    var view   = grid.getView();
    var vStore = (view.store || view.getStore());
    var real   = vStore.getSource ? vStore.getSource() : vStore; // ChainedStore 대비

    Ext.suspendLayouts();
    real.suspendEvents();

    try {
      for (var i = range.start; i <= range.end; i++) {
        var r = vStore.getAt(i);
        if (!r || r.get('DELETE') === true) continue;

        var target = i + 1; // 1-base 시퀀스
        if (r.get(seqField) !== target) {
          r.set(seqField, target);
          if (!r.get('IUD')) r.set('IUD', 'IU');
          if (typeof extraSetter === 'function') extraSetter(r);
        }
      }
    } finally {
      real.resumeEvents();
      Ext.resumeLayouts(true);
    }
  },

  // 뷰 준비 시 드롭 이벤트 연결
  onMasterViewReady: function (grid) {
    grid.getView().on('drop', this.onMasterDrop, this);
  },
  onDetailViewReady: function (grid) {
    grid.getView().on('drop', this.onDetailDrop, this);
  },

  // 드롭 핸들러(마스터)
  onMasterDrop: function (node, data, overModel, dropPos) {
    var g     = this.getView().down('#grid_01');
    var view  = g.getView();
    var range = this.getRange(view, data, overModel, dropPos);
    this.reseq(g, 'VIEW_SEQ', range, function (rec) {
      rec.set('FACTORY_CODE', gFactoryCode);
      if (typeof gUserId !== 'undefined') rec.set('OPMAN_CODE', gUserId);
    });
  },

  // 드롭 핸들러(디테일)
  onDetailDrop: function (node, data, overModel, dropPos) {
    // (옵션) 다른 WORK_CODE 로 이동 차단
    if (overModel && data.records && data.records.length) {
      var targetWork = overModel.get('WORK_CODE');
      var cross = Ext.Array.some(data.records, function (r) {
        return r.get('WORK_CODE') !== targetWork;
      });
      if (cross) return; // 다른 공정으로의 이동은 금지
    }

    var g     = this.getView().down('#grid_02');
    var view  = g.getView();
    var range = this.getRange(view, data, overModel, dropPos);
    this.reseq(g, 'VIEW_SEQ', range, function (rec) {
      rec.set('FACTORY_CODE', gFactoryCode);
      if (typeof gUserId !== 'undefined') rec.set('OPMAN_CODE', gUserId);
    });
  }
});

```