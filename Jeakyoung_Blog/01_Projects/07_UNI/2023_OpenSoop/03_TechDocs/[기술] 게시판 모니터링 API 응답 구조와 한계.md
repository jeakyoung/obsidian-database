---
title: 게시판 모니터링 API 응답 구조와 한계
date: 2026-09-18
type: 기술문서
project: 대학프로젝트
status: 완료
category: API
assignee:
  - 안재경
tags: []
---

# 게시판 모니터링 API 응답 구조와 한계

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | `OpenSoopBack` — `admin.process.FreeAdmin`/`RequestAdmin`/`MarketAdmin`/`AskAdmin` |
| **적용 범위** | API |
| **관련 모듈** | `uni-account-mapping.select*BubInfo`, `uni-community-mapping.selectMarkImgInfo` |

> 관리자가 자유·건의·장터·질문 게시판을 한 번에 훑어보는 모니터링 API 4개의 구현 방식과, 코드를 다시 읽으며 확인한 두 가지 한계(다건 응답 손실, 이미지 목록 미포함)를 정리한다.

## 🎯 배경 및 요구사항

이미 게시판 CRUD용으로 만들어져 있던 `select*BubInfo` 매퍼 쿼리(학교코드 필터링, `MEMB_DEP_CD` 조건부 필터링, `R_NUM` 기반 페이지네이션 포함)를 그대로 재사용해서, 관리자 전용 조회 API 4개(`FreeAdmin`/`RequestAdmin`/`MarketAdmin`/`AskAdmin`)를 빠르게 구현하는 게 목표였다.

## 🏗 설계 및 구현

### 공통 패턴 (Free / Request / Ask)

```java
// FreeAdmin / RequestAdmin / AskAdmin 공통 패턴
List<Map<String, Object>> rtnList = session.selectList("uni-account-mapping.select*BubInfo", param);

for (int i = 0; i < rtnList.size(); i++) {
    jobjMain.put("NICK_NM", rtnList.get(i).get("NICK_NM"));
    jobjMain.put("MEMB_SC_CD", rtnList.get(i).get("MEMB_SC_CD"));
    jobjMain.put("MEMB_DEP_CD", rtnList.get(i).get("MEMB_DEP_CD"));
    jobjMain.put("TIT", rtnList.get(i).get("TIT"));
    jobjMain.put("CRE_DAT", rtnList.get(i).get("CRE_DAT"));
    jobjMain.put("CONT", rtnList.get(i).get("CONT"));
    jary.add(rtnList);   // FreeAdmin은 루프 밖에서 한 번만 add
}
```

### `MarketAdmin`의 이미지 목록 확장

```java
rtnListSub = session.selectList("uni-community-mapping.selectMarkImgInfo", param);
for (int j = 0; j < rtnListSub.size(); j++) {
    jobjSub.put("FILE_PATH", rtnListSub.get(j).get("FILE_PATH"));
    jobjSub.put("IMG_SEQ", rtnListSub.get(j).get("IMG_SEQ"));
    jarrySub.add(jobjSub);
}
jobjSub.put("IMAGE_INFO", jarrySub);
```

## ✅ 검증

> [!warning] 다건 조회 결과가 응답에서 마지막 한 건으로 덮어써짐
> `FreeAdmin`/`RequestAdmin`/`AskAdmin` 세 클래스 모두 `for` 루프 안에서 같은 `JSONObject`(`jobjMain`) 필드에 매 행을 계속 `put`한다. `JSONObject.put`은 같은 키를 덮어쓰므로, 조회된 게시글이 여러 건이어도 클라이언트가 받는 응답에는 마지막으로 순회한 한 건만 남는다.
> `jary`(`JSONArray`)에 `rtnList`(리스트 전체)를 계속 `add`하는 코드도 있지만, `getResult()`가 `jobjMain`만 반환하기 때문에 `jary`는 만들어지기만 하고 응답에 쓰이지 않는 죽은 코드다.

> [!warning] `MarketAdmin`의 이미지 목록이 메인 응답에 연결되지 않음
> `jobjSub.put("IMAGE_INFO", jarrySub)`까지는 실행되지만, 이 `jobjSub`를 `jobjMain`에 붙이는 코드가 없다. `getResult()`가 반환하는 `jobjMain`에는 `IMAGE_INFO` 키 자체가 생기지 않으므로, 프론트가 이 API로 게시글별 첨부 이미지를 받아볼 방법이 없다.

> [!note] 페이지네이션·직책 조건 파라미터 누락 가능성
> 재사용한 `select*BubInfo` 쿼리는 `#{REQ_PAGE}`/`#{LIST_UNIT_CNT}`로 결과 범위를 제한하고, `TIT_CD`가 `"04"`가 아니면 `MEMB_DEP_CD` 조건을 추가로 건다. 그런데 `admin` 패키지의 4개 Servlet은 요청 바디에서 `REQ_PAGE`/`LIST_UNIT_CNT`/`TIT_CD`를 읽어 `param`에 넣는 코드가 없다 — MyBatis가 없는 키를 `null`로 바인딩하면 `R_NUM <= NULL * LIST_UNIT_CNT` 같은 조건은 항상 거짓이 되어 결과가 아예 비어버릴 수 있다. 실제 DB에 연결해 확인한 것은 아니라 "가능성"으로 남겨둔다.

- [x] 4개 Servlet의 요청 파싱 → `param` 구성 → `process` 클래스 호출까지 코드 경로 확인
- [ ] 위 세 가지 한계 모두 실제 DB 연결 환경에서 재현 확인은 못 함 (프로젝트 종료로 재현 환경 없음)

## 🔗 참고

- [[../01_Tasks/게시판 모니터링 페이지 구현|게시판 모니터링 페이지 구현]]
- [\[기술\] Servlet-Process-MyBatis 계층 구조](<[기술] Servlet-Process-MyBatis 계층 구조.md>)
