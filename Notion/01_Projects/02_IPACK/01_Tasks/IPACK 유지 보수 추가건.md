---
base: "[[Notion/프로젝트 문서화/프로젝트/IPACK 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 진행 중
생성 일시: 2026-06-10T14:28:00
담당자: []
---
1. 거래처 등록에 있는 영업담당자 정보를 세금계산서 발행현황에 칼럼으로 추가

WCO202_VW → WSA513_VW

TCO601 → CHARGE_EMP_CODE → EMPLOYEE_CODE → TIN114 → 해당되는 BASE_NAME

```javascript
{
                    name: 'TOTAL_QTY',
                    type: 'number',
                    convert: function (value) {
                        return value > 0 ? Number(value) : null;
                    },
                },
```

숫자가 너무커서 parseInt시에 정상적으로 값을 못읽음 데이터크기문제 x sum시에 과학적 숫자 표기로 넘어가버림

그래서 다음과같이 Number로 정상적으로 읽어들일수있음