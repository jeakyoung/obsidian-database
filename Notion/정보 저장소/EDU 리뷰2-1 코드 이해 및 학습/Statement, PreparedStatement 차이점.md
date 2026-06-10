---

---

## 공통사항

ㅇ 두가지 모두 SQL을 실행하는 개체로 사용되지만 방식의 차이가 존재한다.

## Statement

1. 단일로 사용될때 빠른 속도를 보여줌
2. 쿼리에 인자를 부여하지 않음
3. 매 회마다 컴파일을 진행함

```java
query = "EXEC SP_HHR102_IUD"

Statement stmt = conn.createStatement()

ResultSet rs = stmt.executeQuery(sql);
```

- 쿼리에 파라미터 값이 없음 → executeQuery 수행 과정에서 쿼리를 파라미터로 올리므로 실행전까지 무슨 쿼리를 올리는지 알수가 없음. 따라서 반복수행시 실행속도가 psmt에 비교해 떨어짐.
- 객체가 생성될때 SQL을 넘기지 않고 메소드에서 SQL을 넘겨줌

## PreparedStatement

4. 다 건을 수행할때 빠른 속도를 보여줌
5. 쿼리에 인자를 부여해야함
6. 프리 컴파일 이후로 더 이상 컴파일 할 필요가 없음

```java
String sql = "EXEC SP_HHR102_LIST @FACTORY_CODE = ? ";   // 쿼리 정의

            pstmt = conn.prepareStatement(sql); // 해당 쿼리로 pre 컴파일
            
            pstmt.setString(1,  request.getParameter("FACTORY_CODE")); //인자 부여
            
            rs = pstmt.executeQuery();
            //쿼리 실행에 따른 리턴값을 rs로 담기
```

statement와는 다르게 conn.prepareStatement 부분에서 쿼리를 미리생성하여 보내기 때문에 실행할때도 쿼리를 파라미터에 담지 않고 실행이 가능함 때문에 반복수행시 statement보다 훨씬 유리함.


## 결론적으로

Statement처리 방식은 단건 데이터 처리에는 빠를순 있으나 PreparedStatement과정이 

다건 반복 데이터 처리에는 오히려 훨씬 유리하다.

