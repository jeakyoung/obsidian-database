---
title: I_Frog 단순 발송 공통화 작업
date: 2026-06-10
type: 작업
project: I-Frog
status: 완료
priority: 보통
assignee: []
tags: []
created: 2026-06-10T14:29:00
---

# I_Frog 단순 발송 공통화 작업

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-06-10 |
| **대상 시스템** | — |
| **관련 화면·프로그램** | — |

## 🔍 현상 및 원인

## 🔧 조치 내용

api를 호출하면서
request parameter로 (title,body,empList, type)를 받고,
empList를 TGI001에서 해당 emp들 중 TGI001에 실제 데이터가 있는지 여부를 확인하여
TGI001에 포함된 유저의 token 추려낸 뒤
해당 추려낸 유저들의 리스트를  FCM 메세지에 title, body, empTokenList 를 발송
TGI002 에 알림내역에 저장
firebase Server에 전달 후 유저(client)에게 noti 알림 발생

![[Pasted image 20260831132642.png]]

→ 단순센더 요청 파라미터

![[Pasted image 20260831132652.png]]

→ 서버 전달부

## ✅ 검증 및 결과

## 🔗 참고
