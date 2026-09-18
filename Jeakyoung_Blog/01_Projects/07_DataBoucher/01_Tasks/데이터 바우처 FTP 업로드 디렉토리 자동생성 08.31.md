---
title: 데이터 바우처 FTP 업로드 디렉토리 자동생성 08.31
date: 2026-08-31
type: 작업
project: 데이터바우처
status: 완료
priority: 보통
assignee:
  - 안재경
tags: []
---

# 데이터 바우처 FTP 업로드 디렉토리 자동생성 08.31

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-08-31 |
| **대상 시스템** | F1Soft.Starmap.Service — Image 업로드/FTP |
| **관련 화면·프로그램** | `FtpService`, `ImageService` |

> 라벨 이미지 FTP 저장 경로를 `yy/MM/` 날짜 디렉토리 구조로 바꾸고, 업로드 전 디렉토리가 없으면 자동 생성하도록 개선.

## 🔍 현상 및 원인

### 재현 조건

라벨 이미지가 FTP 루트에 파일명만으로 평면 저장되고 있어, 운영이 길어질수록 한 디렉토리에 파일이 계속 쌓이는 구조였다.

### 원인

`FtpService.UploadAsync(fileName, stream)`가 파일명만 받아 `_ftpUrl + fileName`으로 바로 업로드했고, 디렉토리 존재 여부를 확인/생성하는 로직이 없었다.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 코드 | `Common/Ftp/FtpService.cs` | `UploadAsync(string filePath, Stream stream)`로 시그니처 변경, 경로에 디렉토리가 포함되면 `EnsureDirectoryExistsAsync`로 세그먼트별 `MakeDirectory` 시도 후 업로드 (이미 존재하는 디렉토리는 예외를 무시하되, `FtpStatusCode.NotLoggedIn`이면 재throw) |
| 코드 | `Services/Image/ImageService.cs` | 저장 경로를 `yy/MM/DO{yyyyMMdd}{seq:D4}.{ext}` 형태(`datePath + fileNameWithExt`)로 변경, `TB_LabelMaster`에 저장하는 `FILE_NAME`도 날짜 경로 포함 상대경로로 통일 |

```csharp
string datePath = DateTime.Now.ToString(@"yy\/MM\/"); // ex) 26/08/
string ftpFilePath = datePath + fileNameWithExt;       // ex) 26/08/DO202608190001.jpg
await _ftpService.UploadAsync(ftpFilePath, stream);
```

## ✅ 검증 및 결과

- [x] 디렉토리 미존재 시 자동 생성 후 업로드 성공 확인
- [x] 로그인 실패가 아닌 "이미 존재함" 류 FTP 예외는 무시하고 계속 진행되는지 확인
- [ ] 오래된(날짜 디렉토리 도입 이전) 평면 저장 파일들의 URL·경로 마이그레이션 여부 확인 필요

## 🔗 참고

- 커밋 `4bc9f4e` "Fix Ahn / Ftp 경로 최신화, 디렉토리 경로 설정 추가"
