---

---

---

## 기존방식

```javascript
renderer: function (value) {
                             if (value.replace(/\s/g, '') != '') {
                                 value =
                                     value.substring(0, 4) +
                                     '-' +
                                     value.substring(4, 6) +
                                     '-' +
                                     value.substring(6, 8) +
                                     ' ' +
                                     value.substring(8, 10) +
                                     ':' +
                                     value.substring(10, 12) +
                                     ':' +
                                     value.substring(12, 14);
                             }
                             return value;
                         },
```

다음과 같이 랜더러를 지정해서 데이터의 길이를 하나하나 측정하여 정규식을 만드는 과정으로 원하는 형식으로 변환, 출력해주는 방식을 이용했습니다.

---

## 수정안

```javascript
store_02: {
            fields: [
                { name: 'IMPORTANT_LINE_FLAG', type: 'bool' },
                { name: 'OPMAN_TIME', type: 'date', dateReadFormat: 'YmdHis' },
                { name: 'OPTIME2', type: 'date', dateReadFormat: 'YmdHis' },
            ],
```

Store 파일 내에 ajax 호출 전 field를 지정하여 원하는 이름의 파일에 원하는 형식과 타입으로 먼저 정의해

줍니다.

```javascript
xtype: 'datecolumn',
                text: replaceLocale('최초등록일시'),
                dataIndex: 'OPMAN_TIME',
                align: 'center',
                format: 'Y-m-d H:i:s',
                width: 180,
```

이후 view단에서 xtype을 datecolumn으로 지정해주고 OPMAN_TIME에 대한 fromat으로

Y-m-d H:i:s으로 포맷을 지정해줌으로서 원하는 형태로 정규식 없이 출력 가능합니다.

---

## 실행결과

![[image 32.png]]

---