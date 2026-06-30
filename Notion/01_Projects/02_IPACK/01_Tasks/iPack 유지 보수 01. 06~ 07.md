---
base: "[[Notion/프로젝트 문서화/프로젝트/IPACK 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 진행 중
생성 일시: 2026-06-10T14:28:00
담당자: []
---
## ㅇ 요청사항

1. 제판완료등록 (생산관리 > 생산계회관리 > 제판완료등록)

옵셋제판 체크시  "옵셋제판번호" and "제판일" 동시 부여

- 현재 옵셋제판번호만 있는건들은 왜 번호만 나오는지 원인 확인


2. 공정별 재공현황(생산관리 > 재고관리 > 공정별재공현황)

"량"으로 표시되는 칼럼 합계표시 -> 뷰, 엑셀 둘다 반영

- 엑셀은 "피벗"기능 적용 후 합계되는지까지 테스트


3. 기타입고등록(구매자재 > 자재입고관리 > 기타입고등록)

등록된 입고번호 데이터에서 "입고일" 수정후 기타입고현황에 안나오는 원인 확인

## ㅇ 조치사항

1. 뷰파일 수정

```javascript
{
                    xtype: 'gridcolumn',
                    align: 'left',
                    dataIndex: 'CUST_MAT_CODE',
                    width: 70,
                    text: '옵셋<br>제판번호',
                    renderer: function (value, meta, record) {
                        return record.get('JAEPAN_FLAG') === true ? value : '';
                    },
                    editor: {
                        xtype: 'textfield',
                        selectOnFocus: true,
                    },
                },
```

→ 렌더러로 원하는 값으로 나오게 고정

2. 뷰파일 및 스토어 수정

```javascript
{
                            xtype: 'numbercolumn',
                            dataIndex: 'PROD_QTY_016',
                            align: 'end',
                            text: '생산량',
                            width: 100,
                            format: '0,000',
                            summaryType: 'sum',
                            summaryRenderer: 'onRenderer_numValue',
                            renderer: function (value, metaData, record) {
                                if (record.get('WORK_CODE_016') == '') {
                                    metaData.style = 'background-color: #E0E0E0;';
                                } else if (record.get('GOOD_QTY_016') <= 0 && record.get('PROD_FLAG_016') == '1') {
                                    metaData.style = 'background-color: #FFE5CC;';
                                } else if (record.get('NEXT_SUM_016') > 0 && record.get('GOOD_QTY_016') <= 0) {
                                    metaData.style = 'background-color: red; color:white; text-align: center;';
                                    return '실적미입력';
                                }
                                if (value <= 0) {
                                    value = '';
                                }
                                return Ext.util.Format.number(value, '0,000');
                            },
                            exportRenderer: function (value, metaData, record) {
                                if (record.get('WORK_CODE_016') == '') {
                                } else if (record.get('GOOD_QTY_016') <= 0 && record.get('PROD_FLAG_016') == '1') {
                                } else if (record.get('NEXT_SUM_016') > 0 && record.get('GOOD_QTY_016') <= 0) {
                                    return '실적미입력';
                                }
                                if (value <= 0) {
                                    value = '';
                                }
                                return Ext.util.Format.number(value, '0,000');
                            },
                            exportStyle: {
                                alignment: { horizontal: 'right' },
                                format: '#,##0',
                            },
                        },
                        {
                            xtype: 'numbercolumn',
                            dataIndex: 'STOCK_QTY_016',
                            align: 'end',
                            text: '재고량',
                            width: 100,
                            format: '0,000',
                            summaryType: 'sum',
                            summaryRenderer: 'onRenderer_numValue',
                            renderer: function (value) {
                                if (value <= 0) {
                                    return '';
                                }
                                return Ext.util.Format.number(value, '0,000');
                            },
                            exportRenderer: true,
                            exportStyle: {
                                alignment: { horizontal: 'right' },
                                format: '#,##0',
                            },
                        },
```

→ 공통양식, summary, exportFormat 추가

```javascript
{ name: 'GOOD_QTY_008', type: 'float' },
```

→ store내 인덱스 타입 정의 추가

3. ANY_FLAG 를 업데이트 하는 과정에서 오류 발생

```sql
EXEC SP_WMA322_01_IUD 
@FACTORY_CODE='000001',
@INPUT_NO='202512310001',
@INPUT_TYPE='0',
@INPUT_DATE='20251230',
@CUSTOMER_CODE='000630',
@INPUT_EMP_CODE='0000',
@INPUT_DEPT_CODE='010001',
@REFERENCE='test',
@ANY_FLAG='기타입고',
@OPMAN_CODE='0000',
@IRU='IU'
```

```javascript
for (i = 0; i < store.getCount(); i++) {
            let record = store.getAt(i); // let으로 블록 스코프
            if (record.get('SELECT_FLAG')) {
                var anyFlag = record.get('ANY_FLAG');
                if (Ext.isString(anyFlag)) {
                    //문자열로 들어왔을때 (입고 유형 콤보의 DIRTY요소가 존재하지 않는경우)
                    var comboStore = me.getViewModel().getStore('ANY_FLAG');
                    var comboRec = comboStore.findRecord('CODE_NAME', anyFlag); //문자로 콤보스토어내 일치하는 이름을 찾아와서

                    if (comboRec) {
                        anyFlag = comboRec.get('CODE_ID'); //이름이랑 같은 코드를 찾아오기
                        record.set('ANY_FLAG', anyFlag); // 그걸로 record 정규화
                    }
                }
```

→ 다음방식으로 ANY_FLAG 값을 제한하여 해결


,   ISNULL(EMP2.BASE_NAME, '')                           AS BUSINESS_CHARGE_NAME			-- 영업담당자
