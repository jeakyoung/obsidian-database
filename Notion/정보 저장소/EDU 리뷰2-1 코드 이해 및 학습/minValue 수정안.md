---

---



```javascript
{
              xtype: 'datecolumn',
              align: 'center',
              text: replaceLocale('예방점검일'),
              dataIndex: 'LINE_INSP_DATE',
              format: 'Y/m/d',
              flex: 0.7,
              editor: {
                xtype: 'datefield',
                format: 'Y/m/d',
                submitFormat: 'Y/m/d',
                minValue: Ext.Date.clearTime(new Date()),     //최소일자 지정, 오늘 이후여야 지정가능
                minText: '{0} 이후여야 합니다.'
              }
            },
```

→ 때문에 이전 코드 에서의 clearTime은 썸머타임 기준지를 벗어난 지역에서 서비스하므로 필요가없다.

```javascript
{
              xtype: 'datecolumn',
              align: 'center',
              text: replaceLocale('예방점검일'),
              dataIndex: 'LINE_INSP_DATE',
              format: 'Y/m/d',
              flex: 0.7,
              editor: {
                xtype: 'datefield',
                format: 'Y/m/d',
                submitFormat: 'Y/m/d',
                minValue: Ext.Date.new Date(),                //수정부
                minText: '{0} 이후여야 합니다.'
              }
            },
```