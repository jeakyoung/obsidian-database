---

---

부서명 출력을 위해 칼럼명 DEPARTMENT_NAME를 테이블내 칼럼명 Department_Name으로 변경

조회기능에 필요없는 일부기능 삭제

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
          dataIndex: 'DEPARTMENT_NAME',
          flex: 1,
          cls: 'editColumnCls',
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
    }
  ],
});

```


