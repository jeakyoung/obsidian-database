---
date: 2026-08-31
title: 데이터 바우처
---

# 데이터 바우처

신규사업. [[01_Projects/03_iFrog/index.md|I-Frog]] 프로젝트(같은 `F1Soft.Starmap.Service` 코드베이스)를 카피해서 새로운 시스템으로 구현.

**프로젝트 목표**: 입고등록 대상 라벨 사진을 대량으로 수집해, AI 모듈로 라벨 내 함량표시 변경 여부를 자동 분류·모니터링하는 것.

**담당 범위**(이 저장소 기준): 그 중 데이터 수집 단계 — 모바일에서 입고대상 라벨 사진을 촬영·저장하고 DB(`TB_LabelMaster`)에 이력을 쌓는 모바일 백엔드 API 파이프라인. AI 분석(함량표시 변경 판별) 자체는 별도 모듈이며 이 저장소 범위 밖.

## 기술 스택

| 항목 | 내용 |
|:--|:--|
| **담당 업무** | 입고 라벨 이미지 촬영·업로드·DB 적재 파이프라인 개발 (신규사업) |
| **백엔드** | C# .NET Core |
| **데이터베이스** | MSSQL |
| **원본 코드베이스** | I-Frog (`F1Soft.Starmap.Service`)를 카피해 시작 |

> [!note] AI 분석 연동은 아직 미구현
> `TB_LabelMaster`에 `LABEL_STATUS`/`ANALYSIS_STATUS` 컬럼과 이를 조회하는 `SP_APP_LABEL_LIST` 연동 코드가 이미 스케폴딩돼 있지만 컨트롤러/서비스에서 주석 처리된 채로 비활성 상태다. 자세한 내용은 [[01_Projects/07_DataBoucher/02_TechDocs/[기술] 입고 라벨 이미지 촬영·업로드·적재 파이프라인]] 참고.

## 문서 분류

- [[01_Projects/07_DataBoucher/01_Tasks|작업 목록]] - 데이터 분석 결과, FTP 업로드 경로 개선, 검색 파라미터 정리
- [[01_Projects/07_DataBoucher/02_TechDocs|기술 문서]] - 멀티테넌시(TickerMiddleware) 구조, 계층 구조·ApiResponse·인증, 라벨 이미지 파이프라인
- [[01_Projects/07_DataBoucher/03_Meetings|회의록]] - 프로젝트 회의 기록
