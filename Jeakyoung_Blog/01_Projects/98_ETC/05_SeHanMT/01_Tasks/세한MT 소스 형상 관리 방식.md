---
title: 세한MT 소스 형상 관리 방식
date: 2026-06-10
type: 작업
project: 세한MT
status: 완료
priority: 보통
assignee: []
tags: []
created: 2026-06-10T14:29:00
---

# 세한MT 소스 형상 관리 방식

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-06-10 |
| **대상 시스템** | — |
| **관련 화면·프로그램** | — |

## 🔍 현상 및 원인

## 🔧 조치 내용

- gitlab (git runner)
    - SHMT-POP-APP → Master, productionUI, Develop/Bugfix

    - 빌드 파일 자체를 배포 ( Updater ) / CD
        - FTP 설정정보 자동생성 → 앱이름, FTP경로 이름 추가하기
        - 업데이트 재실행 → 배포되어있는 version정보가 운영정보랑 다른경우 업데이트 시행
        - 매번 시행시마다 버전확인 → 최신화

    - 코드 빌드 병합방법 / CI → hook → main브랜치 한정
        - git tag 2.0.0
        - 푸쉬할시 버전태그에 맞게 소스코드가 올라감
        - 빌드 파이프라인에 자동생성

## ✅ 검증 및 결과

## 🔗 참고
