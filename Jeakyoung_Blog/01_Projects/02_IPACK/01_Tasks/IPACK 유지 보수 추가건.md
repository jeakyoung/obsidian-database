---
title: IPACK 유지 보수 추가건
date: 2026-06-10
type: 작업
project: IPACK
status: 진행중
priority: 보통
assignee: []
tags: []
created: 2026-06-10T14:28:00
---

# IPACK 유지 보수 추가건

## 1. 개요

| 항목 | 내용 |
|------|------|
| 요청자 |  |
| 요청일 | 2026-06-10 |
| 대상 시스템 |  |
| 관련 화면·프로그램 |  |

## 2. 현상 및 원인

## 3. 조치 내용

1. 거래처 등록에 있는 영업담당자 정보를 세금계산서 발행현황에 칼럼으로 추가

WCO202_VW → WSA513_VW

TCO601 → CHARGE_EMP_CODE → EMPLOYEE_CODE → TIN114 → 해당되는 BASE_NAME

```javascript
{
                    name: 'TOTAL_QTY',
                    type: 'number',
                    convert: function (value) {
                        return value > 0 ? Number(value) : null;
                    },
                },
```

숫자가 너무커서 parseInt시에 정상적으로 값을 못읽음 데이터크기문제 x sum시에 과학적 숫자 표기로 넘어가버림

그래서 다음과같이 Number로 정상적으로 읽어들일수있음

## 4. 검증 및 결과

## 5. 참고
