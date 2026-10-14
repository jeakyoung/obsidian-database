---
title: JavaScript·React 기본
date: 2026-10-14
type: 학습자료
status: 완료
tags: []
---

# JavaScript·React 기본

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **분류** | 면접준비 |
| **관련 기술** | JavaScript, React |
| **정리일** | 2026-10-14 |

> JavaScript 단골 개념(호이스팅, 클로저, this, 이벤트 루프)과 React 기본(컴포넌트, props, state, useEffect)을 면접 답변 수준으로 정리.

## 🧩 핵심 개념

- JavaScript는 **싱글 스레드** 언어지만, 이벤트 루프 덕분에 비동기 작업을 막힘 없이 처리한다
- 함수는 **자신이 만들어진 환경(스코프)을 기억**한다 — 클로저
- React는 **state가 바뀌면 컴포넌트 함수가 다시 실행되어 화면을 갱신**하는 구조 (Vue의 반응성과 같은 철학)

## 📖 상세 내용

### 1. JavaScript 기본

**Q1. `==`와 `===`의 차이는?**
> `==`는 타입을 자동 변환한 뒤 비교(`'1' == 1`은 `true`), `===`는 타입까지 같아야 `true`. 예기치 않은 변환을 막기 위해 실무에서는 `===`를 기본으로 쓴다.

**Q2. 호이스팅(Hoisting)이란?**
> 변수/함수 선언이 스코프 맨 위로 끌어올려진 것처럼 동작하는 현상. `var`는 선언 전에 접근하면 `undefined`, `let`/`const`는 선언 전 접근 시 에러(TDZ, 일시적 사각지대).

```javascript
console.log(a); // undefined
var a = 1;

console.log(b); // ReferenceError
let b = 2;
```

**Q3. 클로저(Closure)란?**
> 함수가 선언될 때의 바깥 변수를 기억해서, 바깥 함수가 끝난 뒤에도 그 변수에 접근할 수 있는 것. 외부에서 직접 못 건드리는 private 변수처럼 활용 가능.

```javascript
function makeCounter() {
  let count = 0;            // 외부에서 직접 접근 불가
  return () => ++count;     // 이 함수가 count를 기억
}
const counter = makeCounter();
counter(); // 1
counter(); // 2
```

**Q4. `this`는 무엇을 가리키나요?**
> 일반 함수의 `this`는 **호출한 방식**에 따라 결정된다(`obj.method()`면 `obj`). 화살표 함수는 자신의 `this`가 없고 **선언된 위치 바깥의 `this`**를 그대로 쓴다. 그래서 콜백 안에서 `this`가 바뀌는 문제를 화살표 함수로 피한다.

### 2. 비동기와 이벤트 루프

**Q5. 아래 코드의 출력 순서는?**

```javascript
console.log('1');
setTimeout(() => console.log('2'), 0);
Promise.resolve().then(() => console.log('3'));
console.log('4');
```

A. `1 → 4 → 3 → 2`

- 동기 코드(`1`, `4`)가 콜 스택에서 먼저 전부 실행
- 그 다음 **마이크로태스크 큐**(Promise의 `then`)가 먼저 처리되어 `3`
- 마지막으로 **태스크 큐**(`setTimeout`)의 `2` — 지연 시간이 0이어도 Promise보다 늦다

**Q6. `fetch`로 API를 호출하는 코드를 `async/await`로 작성하세요.**

```javascript
async function loadPart(partId) {
  try {
    const res = await fetch(`/api/parts/${partId}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (e) {
    console.error('부품 조회 실패', e);
    return null;
  }
}
```

- `fetch`는 404/500 응답에서도 reject되지 않음 → `res.ok`를 직접 확인해야 한다는 점이 단골 꼬리질문

### 3. React 기본

**Q7. props와 state의 차이는?**

| | props | state |
|:--|:--|:--|
| 주인 | 부모 컴포넌트가 내려줌 | 컴포넌트 자기 자신 |
| 변경 | 자식이 직접 수정 불가 (읽기 전용) | `setState`로 변경 → 리렌더링 |
| 비유 | 함수의 매개변수 | 함수 안의 기억하는 변수 |

**Q8. 기본 컴포넌트 예시**

```jsx
function PartList({ parts }) {               // props로 목록을 받음
  const [keyword, setKeyword] = useState(''); // state

  const filtered = parts.filter(p => p.name.includes(keyword));

  return (
    <div>
      <input value={keyword} onChange={e => setKeyword(e.target.value)} />
      <ul>
        {filtered.map(p => <li key={p.id}>{p.name}</li>)}
      </ul>
    </div>
  );
}
```

- 리스트 렌더링 시 `key`는 React가 어떤 항목이 바뀌었는지 구분하는 기준 — 배열 인덱스 대신 고유 id를 쓰는 게 원칙

**Q9. `useEffect`의 의존성 배열은 무슨 역할인가요?**

```jsx
useEffect(() => {
  loadPart(partId).then(setPart);
}, [partId]); // partId가 바뀔 때만 다시 실행
```

| 의존성 배열 | 실행 시점 |
|:--|:--|
| 생략 | 렌더링될 때마다 |
| `[]` | 처음 화면에 나타날 때 한 번 |
| `[a, b]` | 처음 + `a` 또는 `b`가 바뀔 때 |

**Q10. state를 직접 수정하면 안 되는 이유는?**
> React는 state의 **참조가 바뀌었는지**로 변경을 감지한다. `list.push(x)`처럼 원본을 고치면 참조가 같아서 화면이 갱신되지 않는다. `setList([...list, x])`처럼 새 배열/객체를 만들어 넘겨야 한다(불변성).

## 💡 정리 및 활용

- JS는 Q3(클로저)와 Q5(이벤트 루프 출력 순서)가 가장 자주 나오는 개념 문제
- React는 "state가 바뀌면 다시 그린다" 한 문장에서 props/state, 불변성, useEffect가 전부 파생된다는 흐름으로 설명
- Vue와 비교 질문이 나오면 [[03_Learning/Test/Vue.js 기본 개념]]의 비교표 활용

## 🔗 참고

- [[03_Learning/Test/Vue.js 기본 개념]]
- [[03_Learning/Test/기술스택 종합 문제]]
- [[03_Learning/Test/면접 예상 질문 정리]]
