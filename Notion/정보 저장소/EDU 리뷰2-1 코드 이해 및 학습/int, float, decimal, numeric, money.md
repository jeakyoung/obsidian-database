---

---

## int - 정수형 소숫점 X

## float - 부동 소수점을 표현하는 변수단위 (근사치로 저장)

---

## decimal, numeric

- 실수를 표현하는 변수 단위 (numeric과 동일)
- 소수점 이하는 자동 반올림
- DECIMAL( 전체 자릿수, 소수점 자릿수 )
- 정밀도가 높아 돈에 관련된 column은 decimal이나 numeric을 사용하는것이 좋음

```sql
DECIMAL( 전체자릿수, 소수점 자릿수 )
NUMERIC( 전체자릿수, 소수점 자릿수 ) //사용법도 같음
```

## money

```sql
CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  amount MONEY
);

INSERT INTO transactions (amount)
VALUES ('$100.50');

// 로케일 설정
SET lc_monetary = 'de_DE.UTF-8';

// 통화 값 변경
UPDATE transactions
SET amount = '€100.50'
WHERE id = 1;

// 로케일 설정
SET lc_monetary = 'ko_KR.UTF-8';

// 통화 값 변경
UPDATE transactions
SET amount = '₩100,000'
WHERE id = 1;
```

- 통화의 단위를 표현하는 변수단위
- 통화의 단위를 표현하는 변수
