---

---

## getRowClass

![[image 53.png]]

→ Ext.view.Table.getRowClass

기능

- 랜더링중인 행의 CSS클래스를 원하는 CSS클래스로 변경하고자 이용됨. 여러 클래스 이름을 적용하려면 문자열 내에서 공백으로 구분하여 반환하면 됩니다(예: 'my-class another-class')

인자값

- record               : 현재 행에 해당되는 레코드
- index                 : 행 인덱스
- rowParams      : 사용되지않음
- store                 : 그리드에 바인딩된 스토어

리턴값

- 행에 추가할 CSS class name

```javascript
viewConfig: {
            enableTextSelection: true,
            emptyText: '<center>' + replaceLocale('데이터가 없습니다.') + '</center>',
            preserveScrollOnRefresh: true,
            //호기 그리드 호출시 deleted, DELETE_FLAG get해서 record에 담기
            getRowClass: function (record) {
              return String(record.get('DELETE_FLAG')) === '1' ? 'deleted' : '';
            },
```

다음과 같이 viewConfig내에 사용되어있으며 record에 DELETE_FLAG가 1인것들을 deleted와 담아주게 됨.

```javascript
Ext.util.CSS.createStyleSheet(
      '.deleted .x-grid-cell-inner { color:#d40000 !important; }',
      'deleted-css'
    );
  },
```

여기서 deleted는 Controller내 선언되어있으며 createStyleSheet를 활용 .deleted 에 색을 담은 옵션을 담아 CSS로 선언되어있음.

이를 통해 DELETE_FLAG값이 1와 완전 일치하는 항목에 대해 빨간색으로 강제변경함.