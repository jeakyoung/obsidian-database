---
title: DB Foreign Key 제약조건(RESTRICT·CASCADE·SET NULL) 정리
date: 2026-09-18
type: 작업
project: 대학프로젝트
status: 완료
priority: 낮음
assignee:
  - 안재경
tags: []
---

# DB Foreign Key 제약조건(RESTRICT·CASCADE·SET NULL) 정리

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 본인 |
| **요청일** | 2024-05 |
| **대상 시스템** | MariaDB — DBeaver로 FK 제약조건 설정 |
| **관련 화면·프로그램** | `stu_info`, `dep_cd`, `notice_list` 등 참조 관계 테이블 |

> DBeaver에서 FK 생성 시 On Delete/On Update 옵션(RESTRICT/CASCADE/NO ACTION/SET NULL)의 동작 차이가 헷갈려서 정리해둔 기록.

## 🔍 현상 및 원인

### 재현 조건

학과 코드(`dep_cd`)를 참조하는 회원 테이블(`stu_info`) 등 여러 테이블에 FK를 걸면서, 참조 대상 행이 삭제/변경될 때 어떤 옵션을 선택해야 하는지 판단이 서지 않았다.

### 원인

MySQL/MariaDB 계열의 FK 제약조건 옵션을 처음 다뤄봐서 각 옵션의 정확한 동작을 확인하고 넘어갈 필요가 있었다.

## 🔧 조치 내용

| 옵션 | 동작 |
|:--|:--|
| **RESTRICT** | 참조되고 있는 행을 변경/삭제하려 하면 변경/삭제 자체가 취소됨 |
| **CASCADE** | 참조 대상 행이 변경/삭제되면 참조하는 행도 함께 변경/삭제됨 |
| **NO ACTION** | MySQL/MariaDB 기준 RESTRICT와 동일하게 동작 |
| **SET NULL** | 참조 대상 행이 변경/삭제되면 참조하던 컬럼 값을 NULL로 세팅 |

DBeaver의 제약조건(Constraints) 탭에서 FK 생성 시 On Delete/On Update 각각에 위 옵션을 지정하는 방식으로 적용했다.

## ✅ 검증 및 결과

- [x] `dep_cd` 삭제 시 참조 중인 `stu_info` 행 때문에 삭제가 막히는지(RESTRICT) 확인
- [x] 옵션별 동작을 DBeaver GUI로 재현해 확인

## 🔗 참고

- [[평택대학교앱 리워크 개발 과정]]
