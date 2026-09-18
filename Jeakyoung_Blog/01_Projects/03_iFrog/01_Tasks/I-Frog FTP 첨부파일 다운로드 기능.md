---
title: I-Frog FTP 첨부파일 다운로드 기능
date: 2025-11-17
type: 작업
project: I-Frog
status: 완료
priority: 보통
assignee:
  - 안재경
tags:
  - FTP
  - File
---

# I-Frog FTP 첨부파일 다운로드 기능

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | — |
| **대상 시스템** | `Controllers/Groupware/Common/FileController.cs` |
| **관련 화면·프로그램** | 결재 문서 등 첨부파일 다운로드 |

> 기안 문서 등에 첨부된 파일을 ERP의 FTP 저장소에서 받아서 그대로 클라이언트에 스트리밍해주는 기능.

## 🔍 현상 및 원인

첨부파일은 FTP 서버에 `wf_ftp/{구분}/{yyyymm}/{FileCode}` 경로로, **zlib으로 압축된 상태**로 저장돼 있음. 그냥 받아서 내려주면 안 되고 압축을 풀어야 함.

## 🔧 조치 내용

| 구분 | 내용 |
|:--|:--|
| `DownloadFile` | `GubunCode`(01~06, Docu/Library/SaleDocu/BusiProcess/Itempicture/RND)로 폴더를 정하고, `FileCode`의 3~6번째 글자를 연/월로 잘라 하위 폴더 경로를 만듦. `IFtpService.GetStream`으로 받은 스트림을 `ZLibStream(..., CompressionMode.Decompress)`로 풀어서 `File(...)`로 반환 |
| `DownloadFileByEaExeID` | 결재 실행 ID(`EaExeID`)로 `SP_WEB_FrmEA101_07_LIST`를 호출해 첨부파일 코드/이름/확장자를 조회한 뒤 `DownloadFile`을 그대로 호출(내부 위임) |

## ✅ 검증 및 결과

- [x] 압축 해제 후 정상적으로 파일이 열리는지 확인된 상태로 보임(운영 코드에 남아있음)
- [ ] `GubunCode` 07 이상 폴더가 추가될 경우 `switch`에 케이스 추가 필요

## 🔗 참고

- 최초 도입: `33f00ce`(2025-11-17)
