---
base: "[[SP 관리 포인트.base]]"
Column: |-
  BOARD_TYPE, BOARD_TYPE_NAME (동방에만 존재)
  빈값으로 넘기기
송연: true
상태: 시작 전
기능명: GetBoardIssueList
특이사항: |-
  서비스 로직상 두개 값을 임의로 지우게 되어있음 
  dt.Columns.Remove("BOARD_TYPE");
  dt.Columns.Remove("BOARD_TYPE_NAME");
Parameter: 일치
메인: ""
동방: false
ATC: true
---
