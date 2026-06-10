---

---
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
  
onNew: function () {                                       //신규버튼 함수 onNew
    var me = this;                                         //me == this
    const grid = me.getView().down('#grid_Employee');      //View내 데이터를 grid로
    const store = grid.getStore();                         //store 명시

    let record = {                                         //record선언
        DEPARTMENT_CODE: '',                               //부서코드
        Department_Name: '',                               //부서이름
        EMPLOYEE_NO: '',                                   //사번
        BASE_NAME: '',                                     //이름
    };

    store.insert(0, record);                               //index0로 grid내 데이터를
},                                                         //store로 insert


  onReg: function () {                                     //저장버튼 함수 onReg
    var me = this;

    const grid = me.getView().down('#grid_Employee');
    const store = grid.getStore();

    var modifiedRecords = store.getModifiedRecords();
    var removedRecords = store.getRemovedRecords();
    if (modifiedRecords.length == 0 && removedRecords.length == 0) { //데이터 허용범위 확인
      Ext.Msg.alert(
        replaceLocale(TITLE_INFO),
        replaceLocale(MESSAGE_CHECK_STORE)                //초과시 alert
      );
      return;
    }

    for (var i = 0; i < store.getCount(); i++) {           //필수값 Null 비허용
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

      if (record.dirty) {                                 //조건 반복 결과 T/F확인
        record.set('FACTORY_CODE', gFactoryCode);
        record.set('OPMAN_CODE', gUserId);
        record.set('IUD', 'IU');
      }                                       
    }

    store.sync({                          //AJAX호출 서블릿으로 데이터 이동 처리
      success: function () {              //성공 피드백 메세지
        Ext.Msg.alert(replaceLocale(TITLE_INFO), replaceLocale(MESSAGE_REG));
      },
    });
  },

    onDelete: function () {                             //삭제 버튼 실행함수
    var me = this;
    const grid = me.getView().down('#grid_Employee');
    const store = grid.getStore();

    let isThere = false;
    store.each(function (record, index) {                //삭제 항목 확인
      if (record.get('DELETE')) {
        isThere = true;

        record.set('OPMAN_CODE', gUserId);               //사용자 확인
        record.set('IUD', 'D');                          //삭제 코드 대기
      }
    });

    if (!isThere) {                                      //아무것도 없으면    
      Ext.Msg.alert(
        replaceLocale(TITLE_INFO),
        replaceLocale(MESSAGE_SELECT_COUNT_GRID)         //아무것도없어요 출력
      );
      return;
    }

    Ext.MessageBox.show({
      title: replaceLocale(TITLE_INFO),
      msg: replaceLocale(MESSAGE_DELETE_GRID),
      buttons: Ext.Msg.YESNO,
      icon: Ext.MessageBox.INFO,                          //삭제 내용 확인 Y/N
      fn: function (btn) {                                //버튼 동작 정의
        if (btn == 'yes') {                               //yes 클릭시
          store.sync({
            success: function () {                        //정상삭제 동작
              Ext.Msg.alert(                             
                replaceLocale(TITLE_INFO),
                replaceLocale(MESSAGE_DELETE)             //피드백
              );
              me.onView();                                //그리드 초기화(재조회)
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