---
title: 신진SM - 더존 중복 문서처리 방어
date: 2026-09-14
type: 작업
project: 신진SM
status: 진행중
priority: 보통
assignee: []
tags: []
---

# 신진SM - 더존 중복 문서처리 방어

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 내부(재발 방지 조치) |
| **요청일** | 2026-09-14 |
| **대상 시스템** | MES(생산실적/창고이동) ↔ 더존 ERP |
| **관련 화면·프로그램** | `ProdReportService.java`, `ProdSLService.java`, `SP_WPR559_02_IUD_TEST` |

> [[신진SM 중복 포장문제 ( 05.22 )]]에서 처음 보고된 "MES는 정상, 더존만 중복" 문제와 같은 부류이지만 **다른 코드 경로**에 대한 방어책이다 — 05.22 건은 계정대체(WMA624) 쪽, 이 작업은 생산실적 저장(WPR559, `ProdReportService`/`ProdSLService`) 쪽. 자세한 구조 비교는 [\[완료\] 포장중복문제 분석](<../02_TechDocs/[완료] 포장중복문제 분석.md>) 참고.

## 🔍 현상 및 원인

생산실적 저장(포장/자체생산/일반포장) 처리 중 오류·재시도가 겹치면 더존 ERP 쪽에 문서(전표)가 중복 생성되는 현상. `SP_WPR559_02_IUD_TEST`가 MES 쪽 실적 저장과 더존 문서 생성을 같은 흐름에서 처리하는데, 더존 문서가 이미 만들어졌는지 여부를 호출 측(Java)이 알 방법이 없어 매번 생성을 시도하던 것이 원인.

## 🔧 조치 내용

ProdReportService.java
- processProdReport() — IRU='I' 분기에서 ISEXISTS_OUT 확인 후 더존 문서 생성 생략 여부 판단
- createPreparedStatement() — CallableStatement로 전환, 38번 파라미터(ISEXISTS_OUT) OUTPUT 등록

ProdSLService.java
- processSLCrossMove() — 아래 두 지점에서 ISEXISTS_OUT 확인 후 더존 문서 생성 생략 여부 판단
  - "자체생산"(SL_ETC == null) 분기: prodReport() 호출 직후 / prodPacking() 호출 직후
  - "일반 포장"(else) 분기: prodPacking() 호출 직후
- prodReport() — CallableStatement로 전환, 38번 파라미터 OUTPUT 등록
- prodPacking() — CallableStatement로 전환, 38번 파라미터 OUTPUT 등록

SP
- SP_WPR559_02_IUD_TEST — @ISEXISTS_OUT INT = 0 OUTPUT 파라미터 추가 (양쪽 클래스가 공유하는 하나의 SP)

미적용(참고용, 손 안 댄 곳)
- ProdReportService IRU='U'/'D' 분기
- ProdSLService 삭제(IRU='D') 경로의 prodPacking() 호출 2곳

## ✅ 검증 및 결과

신규 저장(`IRU='I'`) 경로는 `ISEXISTS_OUT` 가드 적용 완료. 수정(`U`)·삭제(`D`) 경로는 의도적으로 범위 밖으로 남겨둠 — 해당 경로에서 같은 문제가 재현되는지는 별도 확인 필요.

## 🔗 참고

- [[신진SM 중복 포장문제 ( 05.22 )]] — 같은 부류의 문제, 다른 코드 경로(WMA624)
- [\[완료\] 포장중복문제 분석](<../02_TechDocs/[완료] 포장중복문제 분석.md>)
- [[신진SM 개발 이력]]
