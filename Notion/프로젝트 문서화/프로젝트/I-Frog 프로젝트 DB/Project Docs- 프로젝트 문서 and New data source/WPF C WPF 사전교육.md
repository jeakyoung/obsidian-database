---
base: "[[Notion/프로젝트 문서화/프로젝트/I-Frog 프로젝트 DB/Project Docs- 프로젝트 문서 and New data source/Project Docs- 프로젝트 문서 and New data source.base]]"
카테고리: []
생성일시: 2026-06-10T14:28:00
상태: 진행 중
---
## WPF, WINFORM, C# 프로그램

POP 프로그램 → 장비 연동 → 장비 정보 요청을 보내기 위해.

장비통신 프로토콜 → MODBUS → TCP, RTU (SERIAL_COMMUNICATION)

→ 통신테스트

→ 빌드시에 나오는 창 → 가상 장비 통신 → function_code를 통한 통신

→ 해당 통신과정을 register에 저장 → 프로토콜을 통해 장비의 저장정보를 불러옴

coil(bool), DI(bool), HR(데이터 입력), IR(데이터 입력) → 네 가지 장비

실제로는 SOKET통신을 이용중

WPF → MVVM으로 구현되어있음 → 이미 구현되어있는 곳은 WINFORM으로 되어있음

→ MVC패턴 적용

xaml → html 과 동일 순수히 view만 그리는 역활을 수행 → wpf내 그리는 방법이 여러가지 존재

- 창 : 팝업 창
- 페이지 : 창 안의 페이지
- 사용자 정의 컨트롤 : 페이지랑 동일
- 리소스 사전 : 외부에서 버튼스타일 같은 것을 가져올 때 활용

→ 시각 트리를 켠 후에 개체 선택을 누르고 원하는 항목에 가서 수정하기

뷰에서 데이터 바인딩을 해서 보여주는 방식 원래는 코드비하인드에 함수가 들어있으면 안됨

그렇지만 이전 구현에서는 전부 코드비하인드에 기능 함수가 밀집되어있음

property, binding

→ 프로퍼티로 지정된 값이 존재하고 바인딩 된 값에 대해 변경사항이 생길 경우 비동기 통신 방식을 사용하여 변경 사항을 감지, 값 수정

converter → 데이터 값을 변환해 주는 역활 db단의 convert와 동일

command → 함수를 바인딩하는 개념 

view <> viewmodels <> Models <> Converters

RelayCommand(모든 프로젝트 공통 함수) → Nuget을 받아서 사용 ( communityToolkit.Mvvm )

view model → view가 모르게 해야 됨 view가 없어도 view model 만으로 동작이 가능하도록 설계하기

장비통신은 배제하기.

VIEW를 잡아 놓고 → 여기다가 살을 붙이는 식으로 진행 .

