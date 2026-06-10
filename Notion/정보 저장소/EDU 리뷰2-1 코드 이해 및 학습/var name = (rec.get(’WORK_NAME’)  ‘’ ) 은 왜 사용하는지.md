---

---
## TRIM의 동작방식

Trim은 기본적으로 열의 String객체 내 양쪽 끝에있는 공백을 제거하는 역활을 함 이를 정규식을 활용하여 

원하는 위치의 공백을 제거하는 과정이 가능함

## 기존 코드 분석

< normKey → 정규화 공백, 대소문자 제거 >

```javascript
normKey: function (v) {                                                                         // 공백 제거 + 대문자 변환
    return v.replace(/\s+/g, '').toUpperCase();                                                   // 모든 공백 제거 + 대문자로 변환
  },
```

< Controller → OnReg 함수 내 존재 코드 >

```javascript
for (var i = 0, c = store.getCount(); i < c; i++) {
      var rec  = store.getAt(i);
      var fac  = ((rec.get('FACTORY_CODE') || gFactoryCode) + '').trim();
      var name = ((rec.get('WORK_NAME')    || '') + '').trim();
      var code = ((rec.get('WORK_CODE')    || '') + '').trim();
```

WORK_CODE를 정상적으로 가져왔거나 공백이 들어온 경우중 하나만 true일때 끝에 공백을 더해

trim 동작을 진행, 임의로 추가한 공백부터 처음으로 발견한 공백까지 체크해 열의 시작과 끝으로

보고 공백제거를 진행 → 열의 시작과 끝에 공백이 있지 않더라도 trim동작을 통해 “호   기”와 같은 문자열의

공백제거가 가능
