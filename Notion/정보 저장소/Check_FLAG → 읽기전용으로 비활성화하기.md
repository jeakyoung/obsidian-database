---
base: "[[정보 저장소.base]]"
상태: 시작 전
담당자: []
팀: []
---
```javascript
{
                    xtype: 'checkcolumn',
                    dataIndex: 'CANCEL_FLAG',
                    text: '취소',
                    width: 60,
                    listeners: {
                        beforecheckchange: function () {
                            return false;
                        }, //checkbox 작동전 false처리 -> 읽기전용
                    },
                },
```