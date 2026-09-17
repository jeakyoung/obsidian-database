---
title: Tomcat Container
date: 2026-06-10
type: 학습자료
status: 진행중
tags: []
---

# Tomcat Container

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **분류** | — |
| **관련 기술** | — |
| **정리일** | 2026-06-10 |

## 🧩 핵심 개념

## 📖 상세 내용

- **Engine(엔진)**: 가장 상위 레벨의 컨테이너로, 하나 이상의 호스트(Host)를 포함합니다. 주로 가상 호스팅(Virtual Hosting)을 지원합니다.

[[ContainerEngine]]

- **Host(호스트)**: 단일 도메인 또는 IP 주소에 대한 웹 애플리케이션을 관리하는 컨테이너입니다. 하나의 엔진에 여러 호스트를 설정할 수 있습니다.

[[ContainerHost]]

- **Context(컨텍스트)**: 웹 애플리케이션을 담당하는 컨테이너로, WAR 파일이나 디렉토리를 컨텍스트로서 등록하여 웹 애플리케이션을 실행합니다.

[[ContainerContext]]

- **Wrapper(래퍼)**: 각각의 서블릿을 관리하는 컨테이너로, 서블릿을 실행하고 생명주기를 관리합니다.

[[ContainerWrapper]]

## 💡 정리 및 활용

## 🔗 참고
