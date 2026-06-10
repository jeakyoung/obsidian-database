---
base: "[[정보 저장소.base]]"
우선순위: 높음
상태: 완료
담당자:
  - 안재경
팀: []
---
| Table: HHR101 | Table: HHR102 |
| --- | --- |
| *화면기능 | *화면기능 |
| 1. 행추가는 신규 한줄만 허용공정이 저장되지 않은 상태에서 행추가 불가 | 1. 행추가는 여러줄 추가 가능 |
| 2. 공정을 클릭(선택)하면 오른쪽 호기 정보 조회 | 2. 호기코드는 자동생성 |
| 3. 공정정보를 저장한 후 클릭(선택)했던 행 기억(해당 Row에 자동 선택 되어야 함) | 3. 호기명이 빈값이면 저장을 못하도록 제한(메세지) |
| 4. 공정코드는 자동생성 | 4. 호기명이 동일한게 존재하면 중복 저장 불가(메세지) |
| 5. 공정명이 빈값이면 저장을 못하도록 제한(메세지) | 5. 생산가능수량(월)항목 추가, grid_02의 생산가능수량(월) 항목에 값이 입력되면 grid_01의 생산가능수량(월) 항목에해당공정 모든 호기의 생산가능수량(월)의 값이 합산(삭제호기 제외)되어 자동셋팅. |
| 6. 공정명이 동일한게 존재하면 중복 저장 불가(메세지) | 6. 예방점검일 항목 추가. datecolumn 활용, 오늘 날짜 이전으로 선택 못하도록 제한(메세지) |
| 7. 공정을 삭제할때 삭제 여부 메시지 Yes or No | 7. 중요 항목 체크 기능 추가 checkcolumn 활용 실제 저장되는 값은 '0', '1' |
| 8. 공정을 삭제하면 호기정보도 같이 삭제 | 8. 최종등록자 표기(TIN114 JOIN) |
| 9. 생산가능수량(월)항목 추가, grid_02의 생산가능수량(월) 항목에 값이 입력되면 grid_01의 생산가능수량(월) 항목에해당공정 모든 호기의 생산가능수량(월)의 값이 합산(삭제호기 제외)되어 자동셋팅. 단, grid_01의 생산가능수량은 강제로 변경이 가능 | 9. 최종등록일시 표기(년-월-일 시:분:초 포멧) |
| 10. 외주여부 콤보박스 필드 추가. TCO101의 CODE_ID1 = '999' 활용 |   |
| 11. 공정에 등록된 호기 대수 표시( SP에서 SubQuery 활용)(삭제호기는 미포함)호기를 추가 하거나 삭제하면 실시간으로 반영(CT에서 기능 구현) |   |
| 12. 최종등록자 표기(TIN114 JOIN |   |
| 13. 최종등록일시 표기(년-월-일 시:분:초 포멧) |   |

- 공통 적용
1. 삭제는 실제 데이터를 삭제하는게 아니라 DELETE_FLAG = '1' 로 UPDATE를 하여 조회되지 않도록 한다.
2. 공정과 호기를 저장한 후 행을 드래그하여 위치를 변경하고 저장하면 정렬 순서가 재부여된다.
(VIEW_SEQ 갱신, VIEW_SEQ로 정렬), 공정과 호기 둘다 반영
3. 숫자는 오른쪽 정렬, 천단위 콤마, 조회 or 수정할때 동일 소수점 자릿수 유지(정수 or 소수점)
---

0.코드를 회사스타일로 바꾸기

1.오류수정
공정 저장이 안 됨 (공정 코드가 들어가지 않음): 공정 데이터 저장 시 코드가 제대로 삽
입되지 않는 문제.
호기 그리드에서 이전 날짜를 minValue 대신 메시지로 막기: minValue 속성으로 날짜
를 제한하는 대신, 유효성 검사에서 메시지를 띄워 사용자에게 알림
호기 그리드에서 삭제된 건은 중복 체크 대상으로 두지 않기: 삭제된 행을 중복 검사에서
제외


2.기능 개선
드래그 앤 드랍에 대해서 다시 수정해보기: 드래그 앤 드랍 기능 재검토 및 개선
생산 가능 수량에 대해서 컬럼 업데이트가 아닌 다른 방식으로 해보기: 컬럼 직접 업데이
트 대신, 공정 테이블에 데이터가 있으면 공정의 생산 가능 수량을 사용하고, 없으면 호
기 테이블의 합계를 계산
공통 코드 테이블에서 데이터 가져오기 (store를 통해 DB 조회 후 combo에 뿌려주기):
DB에서 공통 코드 데이터를 불러온 후, ComboBox에 바인딩.


3. 대안 탐색
모델, 서비스 자바 없이 만들어보기 (조회 시): Java 백엔드의 모델/서비스 없이 프론트
에서 직접 조회
각 컬럼별 flex가 아닌 다른 방안을 생각해보기: 컬럼 너비를 flex 대신 사용할 수 있는
다른 방안으로 수정
number 속성인 것들 textfield에서 수정하기: 숫자 필드에 대해 사용한 textfield를 수
정


4.코드 이해 및 학습

OPMAN_CODE, OPMAN_CODE2에 대한 의미
minValue에서 clearTime의 의미
var workname = (rec.get(’WORK_NAME’) || ‘’ ) 은 왜 사용하는지
cellEditing, getRowClass:
Sencha(ExtJS) docs에서 속성 검색해서 기본값, 인자값 확인해보기.
Statement, PreparedStatement 차이점
executeUpdate, executeQuery, execute 차이점
MSSQL 데이터 타입의 특징들 알아보기: Microsoft SQL Server 데이터 타입 특징.
특히 char와 varchar, nvarchar / int, float, decimal, numeric, money



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
            preserveScrollOnRefresh: true,
            plugins: [{
              ptype: 'gridviewdragdrop',                                                                           //Grid내부 Drag & Drop 영역정의
              pluginId:  'reorderMaster',
              enableDrop: true,
              enableDrag: true
            }],
            listeners: {                                                                                            //행 선택 리스너
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
                '->',
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
              align: 'center',
              editor: null,
              flex: 0.5
            },
            {
              text: replaceLocale('공정명'),
              dataIndex: 'WORK_NAME',
              align: 'center',
              flex: 0.5,
              editor: {
                xtype: 'textfield',
                allowBlank: false,
              },
            },
            {
              text: replaceLocale('생산가능수량(월)'),                                                                      //아래 순서대로 WORK_CODE, WORK_NAME textField
              dataIndex: 'PROD_LIMIT_QTY',
              align: 'right',
              flex: 0.7,
              editor: {
                xtype: 'textfield'
              }
            },
            {
              text: replaceLocale('외주여부'),
              dataIndex: 'OUTORDER_FLAG',
              align: 'left',
              flex: 0.5,
              renderer: 'renderOutorderFlag',
              editor: {
                xtype: 'combo',
                queryMode: 'local',
                forceSelection: true,
                editable: false,
                displayField: 'CODE_NAME_ABBR',
                valueField:   'OUTORDER_FLAG',
                store: {
                  fields: ['OUTORDER_FLAG','CODE_NAME_ABBR'],
                  data: [
                    { OUTORDER_FLAG: '1', CODE_NAME_ABBR: '외주' },
                    { OUTORDER_FLAG: '0', CODE_NAME_ABBR: '자사' }
                  ]
              }
              }
            },
            {
              text: replaceLocale('등록호기(대)'),                                                                      //아래 순서대로 WORK_CODE, WORK_NAME textField
              dataIndex: 'LINE_COUNT',
              align: 'right',
              editor: null,
              flex: 0.7
            },
            {
              text: replaceLocale('최종등록자'),                                                                      //아래 순서대로 WORK_CODE, WORK_NAME textField
              dataIndex: 'BASE_NAME',
              align: 'center',
              editor: null,
              flex: 0.5
            },
            {
              text: replaceLocale('최종등록일시'),                                                                      //아래 순서대로 WORK_CODE, WORK_NAME textField
              dataIndex: 'OPTIME',
              align: 'center',
              editor: null,
              flex: 1
            },
          ],
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
            //호기 그리드 호출시 deleted, DELETE_FLAG get해서 record에 담기
            getRowClass: function (record) {
              return String(record.get('DELETE_FLAG')) === '1' ? 'deleted' : '';
            },
            plugins: [{
              ptype: 'gridviewdragdrop',
              pluginId: 'reorderDetail',
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
          dockedItems: [{
            xtype: 'toolbar',
            dock: 'top',
            items: [
            {
              xtype: 'checkbox',
              reference: 'RED_FLAG',
              boxLabel: replaceLocale('삭제호기 포함 조회'),
              margin: '0 12 0 0',
              listeners: { change: 'onToggleRedFlag' } //리스너를 통해 체크박스 클릭시 동작 정의
            },
              '->',
                { xtype: 'button', text: replaceLocale('행추가'), ui: 'btnCls_other2', handler: 'onNewDetail' },
                { xtype: 'button', text: replaceLocale('행삭제'), ui: 'btnCls_other2', handler: 'onDeleteDetail' },
                { xtype: 'button', text: replaceLocale('행저장'), ui: 'btnCls_other2', handler: 'onRegDetail' }
                ]
            }],
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
              align: 'center',
              editor: null,
              flex: 0.5
            },
            {
              text: replaceLocale('호기명'),
              dataIndex: 'LINE_NAME',
              align: 'center',
              editor: {
                xtype: 'textfield',
                allowBlank: false
              },
              flex: 0.7
            },
            {
              text: replaceLocale('생산가능수량(월)'),
              dataIndex: 'PROD_LIMIT_QTY',
              align: 'right',
              editor: {
                xtype: 'textfield',
                allowBlank: true
              },
              flex: 0.7
            },
            {
              xtype: 'datecolumn',
              align: 'center',
              text: replaceLocale('예방점검일'),
              dataIndex: 'LINE_INSP_DATE',
              format: 'Y/m/d',
              flex: 0.7,
              editor: {
                xtype: 'datefield',
                format: 'Y/m/d',                              //입출력 포맷지정
                submitFormat: 'Y/m/d',
                minValue: Ext.Date.clearTime(new Date()),     //최소일자 지정, 오늘 이후여야 지정가능
                minText: '{0} 이후여야 합니다.'
              }
            },
            {
              text: replaceLocale('최종등록자'),
              dataIndex: 'BASE_NAME',
              align: 'center',
              editor: null,
              flex: 0.7
            },
            {
              text: replaceLocale('최종등록일시'),
              dataIndex: 'OPMAN_TIME',
              align: 'center',
              editor: null,
              flex: 1,
            },
            {
              xtype: 'checkcolumn',
              text: replaceLocale('중요'),
              dataIndex: 'IMPORTANT_LINE_FLAG',
              width: 60
            },
          ]
        }
      ]
    }
  ]
});
```

→ view

```javascript
Ext.define('AppTest1.view.GW.WGW500.test5Controller', {
  extend: 'Ext.app.ViewController',
  alias: 'controller.test5',

  requires: ['AppTest1.store.GW.WGW500.test5'],

  rRecord: null,

  _toInt: function (v, def) {                                                                     // 정수형으로 변환
    var n = parseInt(v, 10);                                                                      // 10진수 기준으로 파싱
    return isNaN(n) ? (def || 0) : n;                                                             // 숫자가 아니면 기본값 반환
  },
  _nowStr: function () {                                                                          // 현재 시간을 문자열로 반환하는 함수
    return Ext.Date.format(new Date(), 'Y-m-d H:m:s');                                            // yyyy-MM-dd HH:mm:ss 형태로 반환
  },

  normKey: function (v) {                                                                         // 공백 제거 + 대문자 변환
    return v.replace(/\s+/g, '').toUpperCase();                                                   // 모든 공백 제거 + 대문자로 변환
  },

  getSelectionState: function (grid, keyField) {                                                  // 현재 그리드 선택 상태(키/인덱스) 저장
    if (!grid || !keyField) return null;                                                          // grid나 keyField 없으면 종료
    var sm    = grid.getSelectionModel();                                                         // selectionModel 가져오기
    var sel   = sm && sm.getSelection && sm.getSelection()[0];                                    // 선택된 첫 번째 레코드
    if (!sel) return null;                                                                        // 선택된 게 없으면 null

    var store = grid.getStore();                                                                  // grid의 store 참조
    return {
      key: (sel.get(keyField) || '').toString().trim(),                                           // keyField 값 문자열로 저장
      index: store.indexOf(sel)                                                                   // store에서 해당 레코드의 인덱스
    };
  },

  setSelectionState: function (grid, keyField, state) {                                           // 저장해둔 선택 상태 복원
  if (!grid || !keyField || !state) return;                                                       // 유효성 체크

  var store = grid.getStore();
  if (!store || store.getCount() === 0) return;                                                   // store 없거나 비었으면 종료

  var rec = null;

    
  if (state.key) {                                                                                // 1) key로 우선 복원
    var idxByKey = store.findExact(keyField, state.key);                                          // keyField === state.key 정확 매칭
    if (idxByKey !== -1) rec = store.getAt(idxByKey);
  }
  
  if (!rec && state.index >= 0 && state.index < store.getCount()) {                               // 2) 실패 시 index로 복원
    rec = store.getAt(state.index);
  }
  if (!rec) return;                                                                               // 대상 없으면 종료
  var sm = grid.getSelectionModel();                                                              // 선택 수행 
  sm.select(rec, false, true);
  },


  init: function () {                                                                             // 컨트롤러 초기화
    var me = this;

    me.control({                                                                                  // 이벤트 바인딩
      '#grid_01': {
        select: 'onSelect',
        viewready: 'onMasterViewReady'
      },
      '#grid_02': {
        viewready: 'onDetailViewReady'
      }
    });

    me.onSetCombo01();

    Ext.util.CSS.createStyleSheet(
      '.deleted .x-grid-cell-inner { color:#d40000 !important; }',
      'deleted-css'
    );
  },

  onSetCombo01: function (ITEM_KIND1, ITEM_KIND2) {                                               // 콤보박스 store 로드
    var me = this;
    var vm = me.getView().getViewModel();
    var store = vm && vm.getStore('store_01');
    if (!store) return;

    var cfg = {};
    if (ITEM_KIND1 || ITEM_KIND2) {                                                               // 파라미터가 있으면 params 설정
      cfg.params = { OUTORDER_FLAG: ITEM_KIND1, CODE_NAME_ABBR: ITEM_KIND2 };
    }
    store.load(cfg);                                                                              // store 로드
  },

  renderOutorderFlag: function (value) {                                                          // 콤보박스 값 → 표시 텍스트로 변환
    var me = this;
    var vm = me.getView().getViewModel();
    var store = vm && vm.getStore('store_01');
    if (!store) return value;

    var rec = store.findRecord('OUTORDER_FLAG', value, 0, false, true, true);                     // OUTORDER_FLAG로 검색
    return rec ? rec.get('CODE_NAME_ABBR') : value;                                               // 있으면 CODE_NAME_ABBR 표시, 없으면 원래 값
  },

  onView: function () {
    var me = this;
    var store = me.getView().getViewModel().getStore('store_01');
    if (!store) return;

    store.load({
      callback: function (records, op, success) {
        if (success) {
          Ext.Msg.alert('정보', '조회 완료');
        } else {
          store.removeAll();
          store.clearData();
          Ext.Msg.alert('오류', '조회 실패');
        }
      }
    });
  },

  onNew: function () {
    var me    = this;
    var grid  = me.getView().down('#grid_01');
    if (!grid) return;
    var store = grid.getStore();
    if (!store) return;

    var pending = store.findBy(function (r) {                                                       // 미완성 레코드 여부 확인
      return !r.get('WORK_CODE') || !r.get('WORK_NAME');                                            // 공정코드/명 비어있으면 true
    }) !== -1;

    if (pending) {
      Ext.Msg.alert('정보', '이미 등록중인 공정항목이 존재합니다.');
      return;
    }

    store.add({                                                                                     // 신규 레코드 추가
      FACTORY_CODE:   gFactoryCode,
      WORK_CODE:      '',
      WORK_NAME:      '',
      PROD_LIMIT_QTY: '',
      OUTORDER_FLAG:  '0',
      OPMAN_CODE:     gUserId,
      VIEW_SEQ:       ''
    });
  },

  onSelect: function (rowModel, record) {                                                           // 부모 선택 시 자식 조회
    var me = this;
    me.rRecord = record;

    var vm         = me.getView().getViewModel();
    var detailStore = vm && vm.getStore('store_02');
    if (!detailStore) return;

    detailStore.load({
      params: {
        WORK_CODE:    (record && record.get('WORK_CODE')) || '',                                      // 선택된 공정코드 전달
        DELETE_FLAG:  '0',
        FACTORY_CODE: gFactoryCode,
        VIEW_SEQ:     '0'
      }
    });
  },

  onReg: function () {                                                                                // 공정 저장
    var me    = this;
    var grid  = me.getView().down('#grid_01');
    if (!grid) return;
    var store = grid.getStore();
    if (!store) return;

    var modified = store.getModifiedRecords();                                                        // 수정된 레코드
    var removed  = store.getRemovedRecords();                                                         // 삭제된 레코드
    if (modified.length === 0 && removed.length === 0) {
      Ext.Msg.alert('정보', '변경된 데이터가 없습니다.');
      return;
    }

    var seen  = {};                                                                                   // 중복검사용 map
    var valid = true;

    for (var i = 0, c = store.getCount(); i < c; i++) {
      var rec  = store.getAt(i);
      var fac  = ((rec.get('FACTORY_CODE') || gFactoryCode) + '').trim();
      var name = ((rec.get('WORK_NAME')    || '') + '').trim();
      var code = ((rec.get('WORK_CODE')    || '') + '').trim();

      if (!name) {
        Ext.Msg.alert('정보', '공정명은 필수입니다.');
        valid = false;
        break;
      }

      var key  = fac + '||' + me.normKey(name);                                                       // 공장코드+공정명으로 중복 키 생성
      var prev = seen[key];

      if (!prev) {
        seen[key] = { idx: i, code: code };
        continue;
      }

      var sameCode = (prev.code === code);                                                            // 이전 공정코드와 동일한지 비교
      var bothNew  = (!prev.code && !code && prev.idx !== i);                                         // 둘 다 신규인데 인덱스가 다르면 중복

      if (!sameCode || bothNew) {
        Ext.Msg.alert('정보', '중복 공정명입니다: ' + name);
        valid = false;
        break;
      }
    }
    if (!valid) return;

    for (var k = 0, n = store.getCount(); k < n; k++) {
      var rec2 = store.getAt(k);
      if (!rec2.get('WORK_NAME')) continue;

      if (rec2.dirty) {
        rec2.set('FACTORY_CODE', gFactoryCode);
        rec2.set('OPMAN_CODE',   gUserId);
        rec2.set('OPTIME',       me._nowStr());
        if (!rec2.get('IUD')) rec2.set('IUD', 'IU');
      }
    }

    var selState = me.getSelectionState(grid, 'WORK_CODE');

    store.sync({
      success: function () {
        Ext.Msg.alert('정보', '저장되었습니다.');
        store.reload({
          callback: function () {
            me.setSelectionState(grid, 'WORK_CODE', selState);
          }
        });
      }
    });
  },


  onDelete: function () {
    var me    = this;
    var grid  = me.getView().down('#grid_01');
    if (!grid) return;
    var store = grid.getStore();
    if (!store) return;

    var selected = store.queryBy(function (r) { return r.get('DELETE') === true; });                  // DELETE 체크된 레코드만 필터 
    var count    = selected && selected.getCount ? selected.getCount() : (selected.length || 0);      // 컬렉션/배열 두 경우 모두 카운트

    if (count === 0) {
      Ext.Msg.alert('정보', '삭제할 항목을 선택하세요.');
      return;
    }

    selected.each(function (r) {                                                                      // 선택된 모든 레코드 순회
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

  onNewDetail: function () {
    var me    = this;
    var grid  = me.getView().down('#grid_02');
    if (!grid) return;

    var store  = grid.getStore();
    var master = me.rRecord;

    if (!master) {
      Ext.Msg.alert('정보', '상위 공정을 먼저 선택하세요.');
      return;
    }

    store.add({
      LINE_CODE:            '',
      LINE_NAME:            '',
      WORK_CODE:            master.get('WORK_CODE'),
      PROD_LIMIT_QTY:       '',
      LINE_INSP_DATE:       '',
      IMPORTANT_LINE_FLAG:  false,
      OPMAN_CODE:           gUserId,
      VIEW_SEQ:             '',
      FACTORY_CODE:         gFactoryCode
    });
  },

  onRegDetail: function () {
    var me    = this;
    var grid  = me.getView().down('#grid_02');
    if (!grid) return;

    var store  = grid.getStore();
    if (!store) return;

    var vm     = me.getView().getViewModel();
    var store2 = vm && vm.getStore('store_01');

    var modified = store.getModifiedRecords();                                                        // 수정된 레코드 수집
    var removed  = store.getRemovedRecords();                                                         // 제거된 레코드 수집
    if (modified.length === 0 && removed.length === 0) {                                              // 변경사항 전혀 없으면
      Ext.Msg.alert('정보', '변경된 데이터가 없습니다.');
      return;
    }

    var seen  = {};                                                                                   // 중복 검사용 맵
    var valid = true;                                                                                 // 유효성 플래그

    for (var i = 0, c = store.getCount(); i < c; i++) {                                               // 모든 레코드 순회
      var rec   = store.getAt(i);                                                                     // i번째 레코드

      var fac   = ((rec.get('FACTORY_CODE') || gFactoryCode) + '').trim();
      var wcode = ((rec.get('WORK_CODE')    || '') + '').trim();
      var lname = ((rec.get('LINE_NAME')    || '') + '').trim();
      var lcode = ((rec.get('LINE_CODE')    || '') + '').trim();

      if (!wcode) {
        Ext.Msg.alert('정보', '상위 공정코드가 없습니다. 먼저 공정을 선택하세요.');
        valid = false;                                                                                // 유효성 실패
        break;                                                                                        // 루프 중단
      }
      if (!lname) {
        Ext.Msg.alert('정보', '호기명은 필수입니다.');
        valid = false;                                                                                // 유효성 실패
        break;                                                                                        // 루프 중단
      }

      var key  = fac + '||' + me.normKey(lname);
      var prev = seen[key];                                                                           // 이전에 동일 키가 있었는지 조회

      if (!prev) {                                                                                    // 처음본 키면
        seen[key] = { idx: i, code: lcode };                                                          // 위치, 코드 저장
        continue;                                                                                     // 다음
      }

      var sameCode = (prev.code === lcode);                                                           // 같은 호기코드인지 비교
      var bothNew  = (!prev.code && !lcode && prev.idx !== i);                                        // 두 레코드 모두 코드가 비어있고 서로 다른 행이면 → 행추가 두번누른 상황

      if (!sameCode || bothNew) {                                                                     // 코드가 다르면 이름 충돌, 둘 다 신규인데 이름 같으면 충돌
        Ext.Msg.alert('정보', '중복 호기명입니다: ' + lname);
        valid = false;                                                                                // 유효성 실패
        break;                                                                                        // 루프 중단
      }
    }
    if (!valid) return;                                                                               // 유효성 실패 시 저장 중단

    for (var j = 0, n = store.getCount(); j < n; j++) {                                               // 다시 모든 레코드 순회
      var rec2 = store.getAt(j);                                                                      // j번째 레코드
      if (!rec2.get('LINE_NAME')) continue;                                                           // 호기명이 비어있는 행은 스킵

      if (rec2.dirty) {                                                                               // 변경사항 있는것만 처리
        rec2.set('FACTORY_CODE', gFactoryCode);
        rec2.set('OPMAN_CODE',   gUserId);
        rec2.set('OPMAN_TIME',   me._nowStr());
        if (!rec2.get('IUD')) rec2.set('IUD', 'IU');
      }
    }

    var selState = me.getSelectionState(grid, 'WORK_CODE');
    var selState = me.getSelectionState(grid, 'LINE_CODE');

    store.sync({
      success: function () {
        Ext.Msg.alert('정보', '저장되었습니다.');
        store.reload({
          callback: function () {
            me.setSelectionState(grid, 'LINE_CODE', selState);                                         // 저장 전 보관한 selState로 라인 선택 복원 
          }
        });
        store2.reload({                                                                               // 마스터 스토어 재조회 (합계/라인수 집계 반영)
        });
      }
    });
  },

  onDeleteDetail: function () {
    var me    = this;
    var grid  = me.getView().down('#grid_02');
    if (!grid) return;
    var store = grid.getStore();
    if (!store) return;

    var selected = store.queryBy(function (r) { return r.get('DELETE') === true; });                  // DELETE 체크된 것만 선별
    var count    = selected && selected.getCount ? selected.getCount() : (selected.length || 0);      // 선택된 수 계산

    if (count === 0) {
      Ext.Msg.alert('정보', '삭제할 항목을 선택하세요.');
      return;
    }

    selected.each(function (r) {                                                                      // 선택된 각 레코드 반복
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

  updateViewSeqRange: function (gridItemId, seqField, startIdx, endIdx) {
    var view = this.getView();
    var grid = view && view.down('#' + gridItemId);                                                   // ID로 그리드 조회
    if (!grid) return;

    var store = grid.getStore();
    if (!store) return;

    var count = store.getCount();                                                                     // 전체 행 수
    if (count === 0) return;

    var s = Math.max(0, this._toInt(startIdx, 0));                                                    // 시작 인덱스 s = max(0, 정수화(startIdx)) → 하한선 내리기
    var e = Math.min(count - 1, this._toInt(endIdx, 0));                                              // 종료 인덱스 e = min(count-1, 정수화(endIdx)) → 상한선 올리기
    if (s > e) return;                                                                                // s가 e보다 크면 범위 역전 → 아무 것도 안 함

    for (var i = s; i <= e; i++) {                                                                    // s ~ e까지 범위 내 반복
      var rec = store.getAt(i);                                                                       // i번째 레코드
      if (!rec) continue;

      var targetSeq = i + 1;                                                                          // 화면 표시 순서 = 0+1 → 1기반 순번으로 환산
      if (rec.get(seqField) !== targetSeq) {                                                          // 기존 순번과 다르면
        rec.set(seqField, targetSeq);                                                                 // 순번 갱신

        if (!rec.get('IUD')) rec.set('IUD', 'IU');
      }
    }
  },

  getReorderDirtyRange: function (view, data, overModel, dropPosition) {                              // DnD 시 변경 영향 범위 계산
    var store = (view && (view.store || (view.getStore && view.getStore())));                         // view.store 또는 view.getStore() 사용
    if (!store) return null;

    var records = (data && data.records) || [];                                                       // 드래그 중인 레코드 목록
    if (!records.length) return null;

    var minIdx = Number.POSITIVE_INFINITY;                                                            // 드래그 레코드의 최소 인덱스 초기값 : 양수 아무거나
    var maxIdx = Number.NEGATIVE_INFINITY;                                                            // 최대 인덱스 초기값 : 음수 아무거나

    for (var i = 0; i < records.length; i++) {                                                        // 드래그된 모든 레코드 순회
      var idx = store.indexOf(records[i]);                                                            // 해당 레코드의 현재 인덱스
      if (idx >= 0) {                                                                                 // -1이 아니면 스토어에 존재
        if (idx < minIdx) minIdx = idx;                                                               // minIdx = min(minIdx, idx)
        if (idx > maxIdx) maxIdx = idx;                                                               // maxIdx = max(maxIdx, idx)
      }
    }
    if (!isFinite(minIdx)) return null;                                                               // 드래그 대상이 스토어에 없으면 null

    var count = store.getCount();                                                                     // 전체 행 수
    var toIdx;                                                                                        // 드롭 목표 인덱스

    if (!overModel) {                                                                                 // overModel이 없으면 (빈 공간 드롭)
      toIdx = count - 1;                                                                              // 맨 뒤로 간주
    } else {
      var overIdx = store.indexOf(overModel);                                                         // 마우스 아래 레코드의 인덱스
      if (overIdx < 0) return null;                                                                   // 유효하지 않으면 null

      toIdx = (dropPosition === 'after') ? (overIdx + 1) : overIdx;                                   // 'after'면 overIdx+1, 아니면 같은 위치
      if (toIdx < 0) toIdx = 0;                                                                       // 하한 보정
      if (toIdx > count - 1) toIdx = count - 1;                                                       // 상한 보정
    }

    var movedEnd = toIdx + (records.length - 1);                                                      // 드롭 후 마지막 차지 인덱스 = 시작(toIdx)+드래그개수-1 (예: 3개를 인덱스 5부터 놓으면 마지막은 7)

    var start = Math.min(minIdx, toIdx);                                                              // 영향 시작 범위 = min(원래 최소 위치, 목표 시작 위치)
    var end   = Math.max(maxIdx, movedEnd);                                                           // 영향 끝 범위 = max(원래 최대 위치, 목표 끝 위치)

    if (start < 0) start = 0;                                                                         // 하한 보정
    if (end > count - 1) end = count - 1;                                                             // 상한 보정
    if (start > end) return null;                                                                     // 잘못된 범위면 null

    return { start: start, end: end };                                                                // 더티 범위를 반환 → 해당 범위만 순번 갱신
  },

  onMasterViewReady: function (grid) {                                                                // 마스터 그리드 viewready 후 초기화
    var me = this;
    if (!grid) return;

    var plugin = grid.findPlugin('cellediting');                                                      // 셀 편집 플러그인 조회
    if (plugin && plugin.on) {                                                                        // 플러그인 존재·이벤트 바인딩 가능
      plugin.on('edit', function (ed, ctx) {                                                          // 편집 이벤트
        if (ctx && ctx.field === 'OUTORDER_FLAG' && ctx.record && !ctx.record.get('IUD')) {           // 필드명이 외주여부이고 IUD 미지정이면
          ctx.record.set('IUD', 'IU');                                                                // IUD='IU'로 지정하여 저장 대상으로 표시 (비교는 문자열 동등성)
        }
      });
    }

    var view = grid.getView();
    if (view && view.on) {                                                                             // 이벤트 바인딩 가능하면
      view.on('drop', me.onDropReorderMaster, me);                                                     // DnD drop 시 순번 계산/갱신 핸들러 연결
    }
  },

  onDetailViewReady: function (grid) {                                                                  // 디테일 그리드 viewready 후 초기화
    var me = this;
    if (!grid) return;

    var view = grid.getView();
    if (view && view.on) {                                                                              // 이벤트 바인딩 가능
      view.on('drop', me.onDropReorderDetail, me);                                                      // DnD drop 시 디테일 순번 핸들러 연결
    }
  },

  onDropReorderMaster: function (node, data, overModel, dropPosition) {                                 // 마스터 DnD drop 핸들러
    var me   = this;
    var grid = me.getView().down('#grid_01');                                                           // 대상 그리드
    if (!grid) return;

    var view  = grid.getView();
    var range = me.getReorderDirtyRange(view, data, overModel, dropPosition);                           // 영향 범위 계산
    if (!range) return;                                                                                 // 범위 없으면 종료

    me.updateViewSeqRange('grid_01', 'VIEW_SEQ', range.start, range.end);                               // 계산된 구간만 순번 보정
  },

  onDropReorderDetail: function (node, data, overModel, dropPosition) {                                 // 디테일 DnD drop 핸들러
    var me   = this;
    var grid = me.getView().down('#grid_02');
    if (!grid) return;

    var view  = grid.getView();
    var range = me.getReorderDirtyRange(view, data, overModel, dropPosition);                           // 영향 범위 계산
    if (!range) return;

    me.updateViewSeqRange('grid_02', 'VIEW_SEQ', range.start, range.end);                               // 해당 범위 순번 업데이트
  },

  onToggleRedFlag: function (checkbox, checked) {                                                       // '삭제호기 포함 조회' 체크박스 토글 핸들러
    var me    = this;
    var grid  = me.getView().down('#grid_02');
    if (!grid) return;

    var store  = grid.getStore();                                                                       // 디테일 스토어
    if (!store) return;

    var master = me.rRecord;                                                                            // 현재 선택된 마스터 레코드
    if (!master) return;                                                                                // 부모 없으면 동작 안 함

    store.load({                                                                                        // 디테일 재조회
      params: {
        FACTORY_CODE: gFactoryCode,
        WORK_CODE:    master.get('WORK_CODE'),
        DELETE_FLAG:  checked ? '1' : '0',
        VIEW_SEQ:     '0'
      },
      callback: function () {                                                                           // 로드 후 콜백
        grid.getView().refresh();                                                                       // 뷰 새로고침 (행 클래스/렌더링 반영)
      }
    });
  }
});
```

→ Controller

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
    store_02: {                                                                         //Grid 2 Model -> 동작방식은 같음
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
          encode: true,
          rootProperty: 'data'
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

→store

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
import java.text.DecimalFormat;
import java.util.ArrayList;

@WebServlet("/com/edu/jvEdu5_01_LIST")
public class jvEdu5_01_LIST extends HttpServlet {
    public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {
        response.setContentType("application/json; charset=UTF-8");
        request.setCharacterEncoding("UTF-8");
        JSONArray result = new JSONArray();
        //02List내 주석처리 완료
        try {
            EduService service = new EduService();
            ArrayList<Edu4_1Model> list = service.getFirstList(request, this.getServletContext());
            
            for (Edu4_1Model model : list) {
            	//OPTIME -> 날짜 가공
            	String opman = (model.getOPTIME() == null) ? "" : model.getOPTIME().toString();
            	opman = opman.replaceAll("\\D", "");
            	if (opman.matches("^\\d{14}$")) {
            	    try {
            	    	//inFmt, outFmt -> 입력받을 형식을 지정해 원하는형태로 재가공
            	        java.time.format.DateTimeFormatter inFmt  = java.time.format.DateTimeFormatter.ofPattern("yyyyMMddHHmmss");
            	        java.time.format.DateTimeFormatter outFmt = java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

            	        java.time.LocalDateTime dt = java.time.LocalDateTime.parse(opman, inFmt);
            	        String formatted = dt.format(outFmt);
            	        opman = formatted;
            	    } catch (Exception e) {
            	        System.out.println("날짜 포맷전환 오류 error값 : " + opman + " / " + e.getMessage());
            	    }
            	} else {
            	    System.out.println("지원하지 않는 날짜 형식: " + opman);
            	}
            	
            	//공정 라인 월 생산 수량 천자리 가공 (sum과정은 호기 IUD동작시 상시진행 -> 이미 더해진상태로 값을 받음)
            	String qtyRaw = (model.getPROD_LIMIT_QTY() == null) ? "" : model.getPROD_LIMIT_QTY().toString();
            	String qtyFormatted = qtyRaw;

            	try {
            	    if (!qtyRaw.isEmpty()) {
            	        double val = Double.parseDouble(qtyRaw);
            	        DecimalFormat df = new DecimalFormat("#,###"); 
            	        qtyFormatted = df.format(val);
            	    }
            	} catch (NumberFormatException ignore) {
            	    System.out.println("수량 포맷 변환 실패: " + qtyRaw);
            	}
            	
                JSONObject obj = new JSONObject();
                obj.put("FACTORY_CODE", 	  model.getFACTORY_CODE());
                obj.put("WORK_CODE", 		  model.getWORK_CODE());
                obj.put("WORK_NAME",		  model.getWORK_NAME());
                obj.put("BASE_NAME",		  model.getBASE_NAME());
                obj.put("OPTIME",			  opman);
                obj.put("PROD_LIMIT_QTY",	  qtyFormatted);
                obj.put("LINE_COUNT",		  model.getLINE_COUNT());
                obj.put("VIEW_SEQ", 		  model.getVIEW_SEQ());
                obj.put("OUTORDER_FLAG", 	  model.getOUTORDER_FLAG());
                obj.put("CODE_NAME_ABBR", 	  model.getCODE_NAME_ABBR());
                obj.put("DELETE_FLAG", 		  model.getDELETE_FLAG());
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

→ LIST 1번


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
		//IUD 2 부분에 주석처리 완료
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
	                    System.out.println("up" + jsonobj);

	                    String FACTORY_CODE      = (jsonobj.get("FACTORY_CODE")       == null ? "" : jsonobj.get("FACTORY_CODE").toString()).replace("'", "''");
	                    String WORK_CODE         = (jsonobj.get("WORK_CODE")          == null ? "" : jsonobj.get("WORK_CODE").toString()).replace("'", "''");
	                    String WORK_NAME         = (jsonobj.get("WORK_NAME")          == null ? "" : jsonobj.get("WORK_NAME").toString()).replace("'", "''");
	                    String VIEW_SEQ          = (jsonobj.get("VIEW_SEQ")           == null ? "" : jsonobj.get("VIEW_SEQ").toString()).replace("'", "''");
	                    String LINE_COUNT		 = (jsonobj.get("LINE_COUNT")     	  == null ? "" : jsonobj.get("LINE_COUNT").toString()).replace("'", "''");
	                    String PROD_LIMIT_QTY    = (jsonobj.get("PROD_LIMIT_QTY")     == null ? "" : jsonobj.get("PROD_LIMIT_QTY").toString()).replace("'", "''");
	                    String OPMAN_CODE		 = (jsonobj.get("OPMAN_CODE")      	  == null ? "" : jsonobj.get("OPMAN_CODE").toString()).replace("'", "''");
	                    String OPTIME			 = (jsonobj.get("OPTIME")      		  == null ? "" : jsonobj.get("OPTIME").toString()).replace("'", "''");
	                    String OUTORDER_FLAG	 = (jsonobj.get("OUTORDER_FLAG")      == null ? "" : jsonobj.get("OUTORDER_FLAG").toString()).replace("'", "''");
	                    String IUD               = (jsonobj.get("IUD")                == null ? "" : jsonobj.get("IUD").toString()).replace("'", "''");
	                    
	                  //IUD 동작시 DB단에 넘어가기전에 DB에 정해진 형식으로 가공 (1.공백이랑 ","제거, 2.공백,소문자로 변경후 true시 1, 그외 0)
	                    String PROD_LIMIT_QTY_2 = PROD_LIMIT_QTY.replace(",", "").trim();
	                    String flag = OUTORDER_FLAG.trim().toLowerCase();
	                    String OUTORDER_FLAG_01 =
	                        ("1".equals(flag) || "true".equals(flag)) ? "1" : "0";
	                    
	                    query = "EXEC SP_HHR101_IUD" 		+
	                        "\r\n@FACTORY_CODE = \t'"  	 	+ FACTORY_CODE   	+ "'," +
	                        "\r\n@WORK_CODE = \t\t'" 		+ WORK_CODE      	+ "'," +
	                        "\r\n@WORK_NAME = \t\t'" 		+ WORK_NAME      	+ "'," +
	                        "\r\n@VIEW_SEQ = \t\t'" 		+ VIEW_SEQ      	+ "'," +
	                        "\r\n@LINE_COUNT = \t\t'" 		+ LINE_COUNT        + "'," +
	                        "\r\n@PROD_LIMIT_QTY =\t'" 		+ PROD_LIMIT_QTY_2  + "'," +
	                        "\r\n@OPMAN_CODE =\t\t'" 		+ OPMAN_CODE		+ "'," +
	                        "\r\n@OPTIME =\t\t'" 			+ OPTIME			+ "'," +
	                        "\r\n@OUTORDER_FLAG =\t'" 		+ OUTORDER_FLAG_01  + "'," +
	                        "\r\n@IUD = \t\t\t'" 			+ IUD 				+ "'";
	                    
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

→ IUD 1번


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
import java.text.DecimalFormat;

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
            	
            	//opman_time 원하는 형태로 가공
            	String opman = (model.getOPMAN_TIME() == null) ? "" : model.getOPMAN_TIME().toString();
            	opman = opman.replaceAll("\\D", "");
            	if (opman.matches("^\\d{14}$")) {
            	    try {
            	    	//inFmt, outFmt -> 입력받을 형식을 지정해 원하는형태로 재가공
            	        java.time.format.DateTimeFormatter inFmt  = java.time.format.DateTimeFormatter.ofPattern("yyyyMMddHHmmss");
            	        java.time.format.DateTimeFormatter outFmt = java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

            	        java.time.LocalDateTime dt = java.time.LocalDateTime.parse(opman, inFmt);
            	        String formatted = dt.format(outFmt);
            	        opman = formatted;
            	    } catch (Exception e) {
            	        System.out.println("날짜 포맷전환 오류 error값 : " + opman + " / " + e.getMessage());
            	    }
            	} else {
            	    System.out.println("지원하지 않는 날짜 형식: " + opman);
            	}
            	
            	//중요라인 체크 boolean으로 재가공 저장시 0,1 꺼낼때 1값을 true로
            	Object flagObj = model.getIMPORTANT_LINE_FLAG();
            	boolean important = false;

            	if (flagObj != null) {
            	    if (flagObj instanceof Boolean) {
            	        important = (Boolean) flagObj;
            	    } else if (flagObj instanceof Number) {
            	        important = ((Number) flagObj).intValue() == 1;
            	    } else {
            	        String fs = flagObj.toString().trim();
            	        important = "1".equals(fs) || "true".equalsIgnoreCase(fs) || "t".equalsIgnoreCase(fs);
            	    }
            	}
            	
            	//호기 라인 월 생산 수량 천자리 가공
            	String qtyRaw = (model.getPROD_LIMIT_QTY() == null) ? "" : model.getPROD_LIMIT_QTY().toString();
            	String qtyFormatted = qtyRaw;

            	try {
            	    if (!qtyRaw.isEmpty()) {
            	        double val = Double.parseDouble(qtyRaw);
            	        DecimalFormat df = new DecimalFormat("#,###"); 
            	        qtyFormatted = df.format(val);
            	    }
            	} catch (NumberFormatException ignore) {
            	    System.out.println("수량 포맷 변환 실패: " + qtyRaw);
            	}
            	//JSON배열로 put
                JSONObject obj = new JSONObject();
                obj.put("FACTORY_CODE", 		model.getFACTORY_CODE());
                obj.put("WORK_CODE", 			model.getWORK_CODE());
                obj.put("LINE_CODE", 			model.getLINE_CODE());
                obj.put("LINE_NAME", 			model.getLINE_NAME());
                obj.put("PROD_LIMIT_QTY", 		qtyFormatted);
                obj.put("BASE_NAME", 			model.getBASE_NAME());
                obj.put("LINE_INSP_DATE", 		model.getLINE_INSP_DATE());
                obj.put("OPMAN_TIME", 			opman);
                obj.put("IMPORTANT_LINE_FLAG", 	important);
                obj.put("VIEW_SEQ", 			model.getVIEW_SEQ());
                obj.put("DELETE_FLAG", 			model.getDELETE_FLAG());
                result.add(obj);
                System.out.println(important);
            }
            //예외처리
        } catch (Exception e) {
            JSONObject error = new JSONObject();
            error.put("success", false);
            error.put("message", e.toString());
            result.add(error);
        }
        //출력
        PrintWriter out = response.getWriter();
        out.print(result.toJSONString());
        out.flush();
    }
}
```

→ list 2번

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

            if (data != null) {
                JSONArray array;
                if (data.trim().startsWith("{")) {
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
                    System.out.println("up" + jsonobj);

                    String FACTORY_CODE      = (jsonobj.get("FACTORY_CODE")      	== null ? "" : jsonobj.get("FACTORY_CODE").toString()).replace("'", "''");
                    String WORK_CODE         = (jsonobj.get("WORK_CODE")         	== null ? "" : jsonobj.get("WORK_CODE").toString()).replace("'", "''");
                    String LINE_CODE         = (jsonobj.get("LINE_CODE")         	== null ? "" : jsonobj.get("LINE_CODE").toString()).replace("'", "''");
                    String LINE_NAME         = (jsonobj.get("LINE_NAME")         	== null ? "" : jsonobj.get("LINE_NAME").toString()).replace("'", "''");
                    String VIEW_SEQ          = (jsonobj.get("VIEW_SEQ")          	== null ? "" : jsonobj.get("VIEW_SEQ").toString()).replace("'", "''");
                    String PROD_LIMIT_QTY    = (jsonobj.get("PROD_LIMIT_QTY")    	== null ? "" : jsonobj.get("PROD_LIMIT_QTY").toString()).replace("'", "''");
                    String OPMAN_CODE		 = (jsonobj.get("OPMAN_CODE")      	 	== null ? "" : jsonobj.get("OPMAN_CODE").toString()).replace("'", "''");
                    String OPMAN_TIME		 = (jsonobj.get("OPMAN_TIME")      	 	== null ? "" : jsonobj.get("OPMAN_TIME").toString()).replace("'", "''");
                    String LINE_INSP_DATE    = (jsonobj.get("LINE_INSP_DATE")    	== null ? "" : jsonobj.get("LINE_INSP_DATE").toString()).replace("'", "''");
                    String IMPORTANT_FLAG    = (jsonobj.get("IMPORTANT_LINE_FLAG") 	== null ? "" : jsonobj.get("IMPORTANT_LINE_FLAG").toString()).replace("'", "''");
                    String IUD               = (jsonobj.get("IUD")               	== null ? "" : jsonobj.get("IUD").toString()).replace("'", "''");
                    
                    //IUD 동작시 DB단에 넘어가기전에 DB에 정해진 형식으로 가공 (1.공백이랑 ","제거, 2.공백,소문자로 변경후 true시 1, 그외 0)
                    String PROD_LIMIT_QTY_1 = PROD_LIMIT_QTY.replace(",", "").trim();
                    String flag = IMPORTANT_FLAG.trim().toLowerCase();
                    String IMPORTANT_FLAG_01 =
                        ("1".equals(flag) || "true".equals(flag)) ? "1" : "0";
                    
                    query = "EXEC SP_HHR102_IUD" 			+
                        "\r\n@FACTORY_CODE = \t'" 			+ FACTORY_CODE   		+ "'," +
                        "\r\n@WORK_CODE = \t\t'" 			+ WORK_CODE      		+ "'," +
                        "\r\n@LINE_CODE = \t\t'" 			+ LINE_CODE      		+ "'," +
                        "\r\n@LINE_NAME = \t\t'" 			+ LINE_NAME      		+ "'," +
                        "\r\n@VIEW_SEQ = \t\t'" 			+ VIEW_SEQ        		+ "'," +
                        "\r\n@PROD_LIMIT_QTY =\t'" 			+ PROD_LIMIT_QTY_1		+ "'," +
                        "\r\n@OPMAN_CODE =\t\t'" 			+ OPMAN_CODE			+ "'," +
                        "\r\n@OPMAN_TIME =\t\t'" 			+ OPMAN_TIME			+ "'," +
                        "\r\n@LINE_INSP_DATE =\t'" 			+ LINE_INSP_DATE		+ "'," +
                        "\r\n@IMPORTANT_LINE_FLAG =\t'" 	+ IMPORTANT_FLAG_01 	+ "'," +
                        "\r\n@IUD = \t\t\t'" 				+ IUD 					+ "'";

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

→ IUD 2번

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
            // 프로시저 시그니처 순서에 정확히 맞춤 (10개)
            String sql = "EXEC SP_HHR101_LIST " + " @FACTORY_CODE = ?, " + " @WORK_CODE = ?, " + " @WORK_NAME = ?, " + " @BASE_NAME = ?, " + " @OPTIME = ?, " + " @PROD_LIMIT_QTY = ?, " + " @LINE_COUNT = ?, " + " @OUTORDER_FLAG = ?, " + " @VIEW_SEQ = ?, " + " @DELETE_FLAG = ?";

            pstmt = conn.prepareStatement(sql);
            pstmt.setString(1,  request.getParameter("FACTORY_CODE"));
            pstmt.setString(2,  request.getParameter("WORK_CODE"));
            pstmt.setString(3,  request.getParameter("WORK_NAME"));
            pstmt.setString(4,  request.getParameter("BASE_NAME"));
            pstmt.setString(5,  request.getParameter("OPTIME"));
            pstmt.setString(6,  request.getParameter("PROD_LIMIT_QTY"));
            pstmt.setString(7,  request.getParameter("LINE_COUNT"));
            pstmt.setString(8,  request.getParameter("OUTORDER_FLAG"));
            pstmt.setString(9,  request.getParameter("VIEW_SEQ"));
            pstmt.setString(10, request.getParameter("DELETE_FLAG"));

            rs = pstmt.executeQuery();

            while (rs.next()) {
                Edu4_1Model model = new Edu4_1Model();
                model.setFACTORY_CODE   (rs.getString("FACTORY_CODE"));
                model.setWORK_CODE      (rs.getString("WORK_CODE"));
                model.setWORK_NAME      (rs.getString("WORK_NAME"));
                model.setBASE_NAME      (rs.getString("BASE_NAME"));
                model.setOPTIME         (rs.getString("OPTIME"));
                model.setPROD_LIMIT_QTY (rs.getString("PROD_LIMIT_QTY"));
                model.setLINE_COUNT     (rs.getString("LINE_COUNT"));
                model.setOUTORDER_FLAG  (rs.getString("OUTORDER_FLAG"));
                model.setCODE_NAME_ABBR (rs.getString("CODE_NAME_ABBR")); //프로시저에서 직접내림
                model.setVIEW_SEQ       (rs.getString("VIEW_SEQ"));
                model.setDELETE_FLAG    (rs.getString("DELETE_FLAG"));
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
            String sql = "EXEC SP_HHR102_LIST @FACTORY_CODE = ?, @WORK_CODE = ?, @LINE_CODE = ?, @LINE_NAME = ?, @PROD_LIMIT_QTY = ?, @BASE_NAME = ?, @LINE_INSP_DATE = ?, @OPMAN_TIME = ?, @IMPORTANT_LINE_FLAG = ?, @VIEW_SEQ = ?, @DELETE_FLAG = ?";
            pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, request.getParameter("FACTORY_CODE"));
            pstmt.setString(2, request.getParameter("WORK_CODE"));
            pstmt.setString(3, request.getParameter("LINE_CODE"));
            pstmt.setString(4, request.getParameter("LINE_NAME"));
            pstmt.setString(5, request.getParameter("PROD_LIMIT_QTY"));
            pstmt.setString(6, request.getParameter("BASE_NAME"));
            pstmt.setString(7, request.getParameter("LINE_INSP_DATE"));
            pstmt.setString(8, request.getParameter("OPMAN_TIME"));
            pstmt.setString(9, request.getParameter("IMPORTANT_LINE_FLAG"));
            pstmt.setString(10, request.getParameter("VIEW_SEQ"));
            pstmt.setString(11, request.getParameter("DELETE_FLAG"));
            rs = pstmt.executeQuery();
            while (rs.next()) {
            	Edu4_2Model model = new Edu4_2Model();
                model.setFACTORY_CODE			(rs.getString("FACTORY_CODE"));
                model.setWORK_CODE				(rs.getString("WORK_CODE"));
                model.setLINE_CODE				(rs.getString("LINE_CODE"));
                model.setLINE_NAME				(rs.getString("LINE_NAME"));
                model.setPROD_LIMIT_QTY			(rs.getString("PROD_LIMIT_QTY"));
                model.setBASE_NAME				(rs.getString("BASE_NAME"));
                model.setLINE_INSP_DATE			(rs.getString("LINE_INSP_DATE"));
                model.setOPMAN_TIME				(rs.getString("OPMAN_TIME"));
                model.setIMPORTANT_LINE_FLAG	(rs.getString("IMPORTANT_LINE_FLAG"));
                model.setVIEW_SEQ				(rs.getString("VIEW_SEQ"));
                model.setDELETE_FLAG			(rs.getString("DELETE_FLAG"));
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

→ Service

```java
package com.report.model.edu;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
//Lombok 활용 getter setter 일괄지정
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Edu4_1Model {
    private String FACTORY_CODE;
    private String WORK_CODE;
    private String WORK_NAME;
    private String BASE_NAME;
    private String OPTIME;
    private String PROD_LIMIT_QTY;
    private String OUTORDER_FLAG;
    private String CODE_NAME_ABBR;
    private String DELETE_FLAG;
    private String VIEW_SEQ;
    private String LINE_COUNT;
    private String IUD;
}
```

→ model1

```java
package com.report.model.edu;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
//Lombok 활용 getter setter 일괄지정
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Edu4_2Model {
    private String FACTORY_CODE;
    private String WORK_CODE;
    private String LINE_CODE;
    private String LINE_NAME;
    private String PROD_LIMIT_QTY;
    private String BASE_NAME;
    private String LINE_INSP_DATE;
    private String OPMAN_TIME;
    private String IMPORTANT_LINE_FLAG;
    private String VIEW_SEQ;
    private String DELETE_FLAG;
    private String IUD;
}
```

→ MODEL2

```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_HHR101_LIST]    Script Date: 2025-08-25 오전 9:17:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_HHR101_LIST]

    @FACTORY_CODE   VARCHAR(6),
    @WORK_CODE      VARCHAR(6),
    @WORK_NAME      VARCHAR(8),
    @BASE_NAME      VARCHAR(5),
    @OPTIME         VARCHAR(20),
    @PROD_LIMIT_QTY VARCHAR(20),
    @LINE_COUNT     VARCHAR(10),
    @OUTORDER_FLAG  VARCHAR(2),
    @VIEW_SEQ       VARCHAR(10),
    @DELETE_FLAG    VARCHAR(1)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @TEMP VARCHAR(3) = '999';

    SELECT
          A.FACTORY_CODE
        , A.WORK_CODE
        , A.WORK_NAME
        , B.BASE_NAME
        , A.OPTIME
        , A.PROD_LIMIT_QTY
        , A.LINE_COUNT
        , A.OUTORDER_FLAG
        , C.CODE_NAME_ABBR
        , A.VIEW_SEQ
        , A.DELETE_FLAG
    FROM HHR101 AS A
    LEFT JOIN TIN114 AS B
        ON A.OPMAN_CODE = B.EMPLOYEE_NO
    LEFT JOIN TCO101 AS C
        ON C.CODE_ID1 = @TEMP
       AND C.CODE_ID2 = A.OUTORDER_FLAG
    WHERE ISNULL(A.DELETE_FLAG, '0') <> '1'
    ORDER BY TRY_CAST(A.VIEW_SEQ AS INT) ASC;
END 
```

→ List1 Procedure

```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_HHR101_IUD]    Script Date: 2025-08-25 오후 4:26:40 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_HHR101_IUD]
    @FACTORY_CODE       VARCHAR(6),
    @WORK_CODE          VARCHAR(6),
    @WORK_NAME          VARCHAR(20),
    @PROD_LIMIT_QTY     VARCHAR(20),
    @LINE_COUNT         VARCHAR(10),
    @OPMAN_CODE         VARCHAR(4),
    @OPTIME             VARCHAR(20),
    @VIEW_SEQ           VARCHAR(10),
    @OUTORDER_FLAG      VARCHAR(2),
    @IUD                VARCHAR(2)
AS
BEGIN
    DECLARE @DATE varchar(25)
	SET @DATE = replace(replace(replace(convert(varchar(20), getdate(), 120), '-', ''), ':',''), ' ', '');

    SET NOCOUNT ON;

    IF @IUD = 'IU'
    BEGIN
        UPDATE HHR101
        SET
            WORK_NAME           = @WORK_NAME,
            PROD_LIMIT_QTY      = @PROD_LIMIT_QTY,
            LINE_COUNT          = @LINE_COUNT,
            OPMAN_CODE          = @OPMAN_CODE,
            OPTIME              = @DATE,
            OUTORDER_FLAG       = @OUTORDER_FLAG,
            VIEW_SEQ            = @VIEW_SEQ
        WHERE
            FACTORY_CODE  = @FACTORY_CODE
            AND WORK_CODE = @WORK_CODE

        IF @@ROWCOUNT = 0
            BEGIN 
                IF (@WORK_CODE = '' AND @VIEW_SEQ = '') 
                    BEGIN
                        SELECT @WORK_CODE = RIGHT('000000' + CAST(CAST(ISNULL(MAX(WORK_CODE),'0') AS INT) + 1 AS VARCHAR(6)),6),
                               @VIEW_SEQ = CAST(ISNULL(MAX(VIEW_SEQ),'0') AS INT) + 1
                        FROM   HHR101
                        WHERE  FACTORY_CODE = @FACTORY_CODE
                        
                    END

            INSERT INTO HHR101 (
                FACTORY_CODE,
                WORK_CODE,
                WORK_NAME,
                PROD_LIMIT_QTY,
                LINE_COUNT,
                OPMAN_CODE,
                OPTIME,
                OUTORDER_FLAG,
                VIEW_SEQ
            ) VALUES (
                @FACTORY_CODE,
                @WORK_CODE,
                @WORK_NAME,
                @PROD_LIMIT_QTY,
                @LINE_COUNT,
                @OPMAN_CODE,
                @DATE,
                @OUTORDER_FLAG,
                @VIEW_SEQ
            );
        END
    END

    ELSE IF @IUD = 'D'
    BEGIN
        UPDATE HHR101
        SET DELETE_FLAG = '1'
        WHERE FACTORY_CODE  = @FACTORY_CODE
            AND WORK_CODE = @WORK_CODE;

        UPDATE HHR102
        SET DELETE_FLAG = '1'
        WHERE
            FACTORY_CODE  = @FACTORY_CODE
            AND WORK_CODE = @WORK_CODE;
    END
END
```

→ IUD1 Procedure

```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_HHR102_LIST]    Script Date: 2025-08-26 오후 2:23:21 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_HHR102_LIST]
    @FACTORY_CODE           VARCHAR(6),
    @WORK_CODE              VARCHAR(6),
    @LINE_CODE              VARCHAR(3),
    @LINE_NAME              VARCHAR(8),
    @PROD_LIMIT_QTY         VARCHAR(20),
    @BASE_NAME              VARCHAR(5),
    @LINE_INSP_DATE         VARCHAR(24),
    @OPMAN_TIME             VARCHAR(20),
    @IMPORTANT_LINE_FLAG    VARCHAR(1),
    @VIEW_SEQ               VARCHAR(10),
    @DELETE_FLAG            VARCHAR(1)
AS
BEGIN
    SELECT
       B.FACTORY_CODE
     , B.WORK_CODE
     , A.LINE_CODE
     , A.LINE_NAME
     , A.PROD_LIMIT_QTY
     , C.BASE_NAME
     , A.LINE_INSP_DATE
     , A.OPMAN_TIME
     , A.IMPORTANT_LINE_FLAG
     , A.VIEW_SEQ
     , A.DELETE_FLAG

    FROM  HHR102 A
       LEFT JOIN HHR101 B
         ON A.WORK_CODE = B.WORK_CODE
       LEFT JOIN TIN114 C
         ON A.OPMAN_CODE = C.EMPLOYEE_NO

    WHERE
         B.FACTORY_CODE =  @FACTORY_CODE
         AND A.WORK_CODE = @WORK_CODE
         AND CASE
            WHEN @DELETE_FLAG = '1' THEN 1
            WHEN ISNULL(A.DELETE_FLAG,'１') <> '1' THEN 1
            ELSE 0
          END = 1
    ORDER BY TRY_CAST(A.VIEW_SEQ AS INT) ASC;

END
```

→ LIST2 PROCEDURE

```sql
USE [iPlusERP_New_20250320]
GO
/****** Object:  StoredProcedure [dbo].[SP_HHR102_IUD]    Script Date: 2025-08-25 오전 10:53:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_HHR102_IUD]
    @FACTORY_CODE           VARCHAR(6),
    @WORK_CODE              VARCHAR(6),
    @LINE_CODE              VARCHAR(3),
    @LINE_NAME              VARCHAR(50),
    @VIEW_SEQ               VARCHAR(10),
    @PROD_LIMIT_QTY         VARCHAR(20),
    @OPMAN_CODE             VARCHAR(4),
    @OPMAN_TIME             VARCHAR(14),
    @LINE_INSP_DATE         VARCHAR(24),
    @IMPORTANT_LINE_FLAG    VARCHAR(1),
    @IUD                    VARCHAR(2)
AS
BEGIN
    
    DECLARE @DATE varchar(25)
	SET @DATE = replace(replace(replace(convert(varchar(20), getdate(), 120), '-', ''), ':',''), ' ', '');

    IF @IUD = 'IU'
    BEGIN
        UPDATE HHR102
        SET
            LINE_NAME           = @LINE_NAME,
            VIEW_SEQ            = @VIEW_SEQ,
            PROD_LIMIT_QTY      = @PROD_LIMIT_QTY,
            OPMAN_CODE          = @OPMAN_CODE,
            OPMAN_TIME          = @DATE,
            LINE_INSP_DATE      = @LINE_INSP_DATE,
            IMPORTANT_LINE_FLAG = @IMPORTANT_LINE_FLAG
        WHERE
            FACTORY_CODE        = @FACTORY_CODE 
            AND WORK_CODE       = @WORK_CODE 
            AND LINE_CODE       = @LINE_CODE

        IF @@ROWCOUNT = 0
         BEGIN
            IF ( @LINE_CODE = '' AND @VIEW_SEQ = '' )
                BEGIN
                    SELECT @LINE_CODE = RIGHT('000' + CAST(CAST(ISNULL(MAX(LINE_CODE),'0') AS INT) + 1 AS VARCHAR(3)),3),
                           @VIEW_SEQ = CAST(ISNULL(MAX(VIEW_SEQ),'0') AS INT) + 1 
                    FROM   HHR102
                    WHERE  WORK_CODE = @WORK_CODE
                END


            INSERT INTO HHR102 (
                FACTORY_CODE,
                WORK_CODE,
                LINE_CODE,
                LINE_NAME,
                VIEW_SEQ,
                PROD_LIMIT_QTY,
                OPMAN_CODE,
                OPMAN_TIME,
                LINE_INSP_DATE,
                IMPORTANT_LINE_FLAG
            ) VALUES (
                @FACTORY_CODE,
                @WORK_CODE,
                @LINE_CODE,
                @LINE_NAME,
                @VIEW_SEQ,
                @PROD_LIMIT_QTY,
                @OPMAN_CODE,
                @DATE,
                @LINE_INSP_DATE,
                @IMPORTANT_LINE_FLAG
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
            AND LINE_CODE    = @LINE_CODE
    END

    DECLARE     @sum   VARCHAR(20)
               ,@count VARCHAR(10);
        SELECT  @sum = CONVERT(VARCHAR(20), CAST(ISNULL(SUM(CONVERT(INT, PROD_LIMIT_QTY)),0) AS INT)),
                @count = COUNT(*)
        FROM HHR102
        WHERE FACTORY_CODE      = @FACTORY_CODE
            AND WORK_CODE       = @WORK_CODE
            AND ISNULL(DELETE_FLAG, '0') <> '1'

        UPDATE HHR101
            SET   PROD_LIMIT_QTY    = @sum
                 ,LINE_COUNT        = @count
            WHERE FACTORY_CODE      = @FACTORY_CODE
                  AND WORK_CODE     = @WORK_CODE
END
```

→ IUD2 PROCEDURE

---

[[ExtJS_Grid활용교육.xlsx]]