---
title: SchlSrchData
date: 2026-06-10
type: 프로젝트문서
project: 대학프로젝트
status: 진행중
tags: []
---

# SchlSrchData

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **프로젝트** | 대학프로젝트 |
| **기간** | 2026-06-10 |
| **역할** | — |
| **기술 스택** | — |

## 🎯 목표 및 범위

## 🏗 진행 내용

```typescript
// 대학교명 데이터의 전체 형식을 정의하는 SchlSrchData 인터페이스
export interface SchlSrchData {
    RSLT_CD: string;                            // 결과 코드
    SCH_NM_INFO: SchlSrchItem[];                // 대학교명 아이템 배열
  }
  
  // 대학교명 하나의 형식을 정의하는 SchlSrchItem 인터페이스
  export interface SchlSrchItem {
    SCH_CD: number;                            // 대학교 코드
    SCH_NM: string;                            // 대학교 이름
  }
  
  
  // 서버에서 받아온 데이터를 SchlSrchData 형식으로 파싱하는 함수
  export function parseSchlSrchData(rawData: any): SchlSrchData {
    const schlsrchdata: SchlSrchData = {
      RSLT_CD: rawData.RSLT_CD || '',            // 결과 코드, 없을 경우 빈 문자열
      SCH_NM_INFO: [],                              // 대학교명 아이템 배열 초기화
    };
  
    if (Array.isArray(rawData.SCH_NM_INFO)) {
      schlsrchdata.SCH_NM_INFO = rawData.SCH_NM_INFO.map((item: any) => {
        const schlsrchItem: SchlSrchItem = {
          SCH_CD: item.SCH_CD === 'number' ? item.SCH_CD : 0,           //대학교 코드 숫자로 변환, 없을 경우 0
          SCH_NM: typeof item.SCH_NM || '',           // 대학교 이름, 없을 경우 빈 문자열
        };
  
        return schlsrchItem;
      });
    }
  
    return schlsrchdata;
  }
```

## ✅ 결과 및 회고

## 🔗 참고
