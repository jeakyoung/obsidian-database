---
base: "[[정보 저장소.base]]"
상태: 시작 전
담당자: []
팀: []
---
```javascript
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
            listeners: {
                load: function (dataStore, rows, bool) {
                    dataStore.insert(0, {
                        WG_CODE: '',
                        WG_NAME: '전체',
                    });
                },
                scope: this,
            },
        },
```
