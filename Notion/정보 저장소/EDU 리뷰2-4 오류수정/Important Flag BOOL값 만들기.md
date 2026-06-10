---

---
---

## 기존방식

```java
String flag = IMPORTANT_FLAG.trim().toLowerCase();
                    String IMPORTANT_FLAG_01 =
                        ("1".equals(flag) || "true".equals(flag)) ? "1" : "0";
```

IUD로 저장할때 T, F 값을 1이나 0으로 변환해서 프로시저를 통해 테이블에 저장한뒤

```java
//중요라인 체크 boolean으로 재가공 저장시 0,1 꺼낼때 1값을 true로
            	Object flagObj = model.getIMPORTANT_LINE_FLAG();
            	boolean important = false;

            	if (flagObj != null) {
            	    if (flagObj instanceof Boolean) {
            	        important = (Boolean) flagObj;
            	    } else if (flagObj instanceof Number) {
            	        important = ((Number) flagObj).intValue() == 1;
            	    } else {
            	        String fs = flagObj.toString().trim();
            	        important = "1".equals(fs) || "true".equalsIgnoreCase(fs) || "t".equalsIgnoreCase(fs);
            	    }
            	}
```

저장된 값을 꺼내서 Boolean 값으로 변환하는 과정을 통해 importantflag의 체크 여부를 체크하는 과정을

거쳐 등록, 조회가 가능했습니다.

---

## 수정안

```java
String flag = (String)jsonobj.get("IMPORTANT_LINE_FLAG").toString().trim();
                    String IMPORTANT_FLAG_01 =
                        ("1".equals(flag) || "true".equals(flag)) ? "1" : "0";
```

IUD 서블릿에서 T/F값을 1이나 0으로 변환만 해서 등록 한뒤

```javascript
store_02: {
    fields: [
				{name: 'IMPORTANT_LINE_FLAG', type: 'bool'}
			],
```

간단히 IMPORTANT_LINE_FLAG를 bool 타입으로 정의하는 field를 store파일에 추가하여 해결 가능합니다.
