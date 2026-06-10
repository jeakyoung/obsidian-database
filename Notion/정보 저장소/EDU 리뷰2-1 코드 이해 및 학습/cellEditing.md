---

---
**       **

## CellEditing 기본값

```javascript
Ext.create('Ext.data.Store', {
    storeId: 'simpsonsStore',
    fields:[ 'name', 'email', 'phone'],
    data: [
        { name: 'Lisa', email: 'lisa@simpsons.com', phone: '555-111-1224' },
        { name: 'Bart', email: 'bart@simpsons.com', phone: '555-222-1234' },
        { name: 'Homer', email: 'homer@simpsons.com', phone: '555-222-1244' },
        { name: 'Marge', email: 'marge@simpsons.com', phone: '555-222-1254' }
    ]
});

Ext.create('Ext.grid.Panel', {
    title: 'Simpsons',
    store: Ext.data.StoreManager.lookup('simpsonsStore'),
    columns: [
        {header: 'Name', dataIndex: 'name', editor: 'textfield'},
        {header: 'Email', dataIndex: 'email', flex:1,
            editor: {
                completeOnEnter: false,

                field: {
                    xtype: 'textfield',
                    allowBlank: false
                }
            }
        },
        {header: 'Phone', dataIndex: 'phone'}
    ],
    selModel: 'cellmodel',       
    plugins: {
        cellediting: {           //cellediting 선언
            clicksToEdit: 1      //1번클릭으로 edit하기
        }
    },
    height: 200,
    width: 400,
    renderTo: Ext.getBody()
});

```


## CellEditing Configs

![[image 52.png]]

- clicksToEdit 시행시 클릭횟수를 충족할시에만 edit하겠다는 선언 1, 2 만 가능
    - Defaults → 2

```javascript
plugins: [
            { ptype: 'cellediting' /* clicksToEdit: 3 */ },                                                              // cell edit을 위한 필요 클릭 횟수
            { ptype: 'gridexporter' }                                                                               // exporter 플러그인 정의
          ],
```

→ 해당부에서 clicksToEdit은 최대 2번까지만 가능하여 3으로 적어도 2로 적용됨.

따라서 default도 더블클릭으로 되어있길레 무의미한 호출임.