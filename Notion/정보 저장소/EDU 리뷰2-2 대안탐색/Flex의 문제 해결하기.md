---

---
---

## Flex 지정시 작은 화면에서 글씨가 작아지는현상

---

![[image 41.png]]

flex는 비율로 공간을 정하는 요소로 전체 공간에서 flex값만큼 나누고 지정한 flex의 비율만큼 화면을 

할당하는 방식으로 다음과 같이 작은 스크린에서는 요소가 자신의 형태를 유지할 수가 없습니다.

flex를 사용하면 화면에 비율에 맞춰 자동으로 조정해주기 때문에 편리한 부분도 있으나 유동적인 부분 때문에

예상하지 못한 플랫폼에서 기능을 시현할 때 개발자가 원하지 않는 UX경험을 줄수 있으므로

Width와 같은 고정값을 부여하고자 합니다.

![[image 42.png]]

다음과 같이 width의 고정값을 사용하면 화면이 작아질 시 화면 뭉개짐이 발생하지 않습니다. 

사용될 스크린 크기가 정해져 있는 것이 아니라면 위와 같이 고정적으로 배치한 후 하단에 좌우 스크롤바를

추가하는 방식으로 진행하는 것이 더 좋을 수도 있다고 생각합니다.

---

## 코드 수정안

```javascript
          columns: [
            { xtype: 'rownumberer' },
            {
              xtype: 'checkcolumn',
              text: replaceLocale('삭제'),
              dataIndex: 'DELETE',
              width: 45
            },
            {
              text: replaceLocale('호기코드'),
              dataIndex: 'LINE_CODE',
              align: 'center',
              editor: null,
              width: 80,
            },
            {
              text: replaceLocale('호기명'),
              width: 80,
              dataIndex: 'LINE_NAME',
              align: 'center',
              editor: {
                xtype: 'textfield',
                allowBlank: false
              },

            },
            {
              text: replaceLocale('생산가능수량(월)'),
              dataIndex: 'PROD_LIMIT_QTY',
              align: 'right',
              width: 150,
              editor: {
                xtype: 'textfield',
                allowBlank: true
              },

            },
            {
              xtype: 'datecolumn',
              align: 'center',
              width: 130,
              text: replaceLocale('예방점검일'),
              dataIndex: 'LINE_INSP_DATE',
              format: 'Y/m/d',

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
              width: 80,
              dataIndex: 'BASE_NAME',
              align: 'center',
              editor: null,

            },
            {
              text: replaceLocale('최종등록일시'),
              width: 150,
              dataIndex: 'OPMAN_TIME',
              align: 'center',
              editor: null,

            },
            {
              xtype: 'checkcolumn',
              text: replaceLocale('중요'),
              dataIndex: 'IMPORTANT_LINE_FLAG',
              width: 45
						}
```

다음과 같이 Flex 비율로 되어있던 요소들을 width로 수정했습니다.

---