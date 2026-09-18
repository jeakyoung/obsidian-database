---
title: 게시판 이미지 첨부 Base64→WebP 저장 구조 구현
date: 2026-09-18
type: 작업
project: 대학프로젝트
status: 완료
priority: 보통
assignee:
  - 안재경
tags: []
---

# 게시판 이미지 첨부 Base64→WebP 저장 구조 구현

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 본인 (BE 팀장) |
| **요청일** | 2024-07 |
| **대상 시스템** | `4th_GraduationBack` — `ImageFileUploadSystem`, 공지/학사/입학/장학 4종 게시판 서비스 |
| **관련 화면·프로그램** | `POST /PTU/{Notice,Bachelor,Entrance,Scholar}/{add,update,delete}` |

> 게시글 등록 시 이미지를 Base64로 받아 서버 로컬 디스크에 `.webp`로 저장하고, 저장된 URL만 DB에 남기는 구조를 만들어서 공지사항에 먼저 붙이고 나머지 3개 게시판에 그대로 이식했다.

## 🔍 현상 및 원인

### 재현 조건

게시판 등록 화면에서 이미지 첨부가 필요했는데, 별도 이미지 서버/오브젝트 스토리지 없이 학생 프로젝트 인프라(EC2 한 대) 안에서 처리해야 했다.

### 원인

첨부파일 저장 방식을 정하기 전 이미지 프로세스/스토리지 개념을 조사([이미지 프로세스 이해](https://velog.io/@rlaclgns321/이미지-프로세스-이해-이미지-서버-스토리지-포함), [백엔드 이미지 업로드 방식](https://seungyong20.tistory.com/entry/백엔드에서-이미지-업로드는-어떻게-하면-좋을까))했고, 별도 스토리지 서버를 두기엔 여유가 없어 API 서버 로컬 디스크에 날짜별 디렉토리로 저장하는 방식으로 결정했다.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 서비스 신설 | `ImageFileUploadSystem` | Base64 디코딩(`decodeBase64Image`), 날짜별 디렉토리(`/var/www/ptu/uploads/yyyyMMdd`) 생성 후 `.webp`로 저장(`saveImageFile`), 삭제(`deleteImageFile`) |
| 게시판 서비스 4종 | `NoticeListService` / `BachelorCheckService` / `EntranceCheckService` / `ScholarCheckService` | 등록 시 이미지 저장, 수정 시 기존 이미지 삭제 후 신규 저장(또는 빈 값이면 이미지만 삭제), 삭제 시 첨부 이미지도 함께 삭제 |
| 모델 | `BachelorCheck` / `EntranceCheck` / `ScholarCheck` / `NoticeModel` | `IMG_CD` 컬럼(첨부 이미지 접근 URL) 추가 |

```java
// ImageFileUploadSystem.saveImageFile — 날짜별 디렉토리 + 중복 회피 파일명
String dateDir = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd"));
Path userDir = Paths.get(uploadDir, dateDir);
...
String filenameBase = String.format("%s_%s", dateDir, userId);
do {
    String filename = (counter == 0) ? filenameBase : filenameBase + counter;
    imagePath = userDir.resolve(filename + ".webp");
    counter++;
} while (Files.exists(imagePath));
```

동일한 로직(등록/수정/삭제 3분기)을 4개 게시판 서비스에 각각 복사해 넣었다 — 공통 로직이지만 별도 헬퍼로 뽑지는 않았다. 자세한 저장 구조와 알려진 제약(경로 하드코딩 등)은 [\[기술\] Base64 이미지 업로드 및 정적 파일 저장소 구조](<../03_TechDocs/[기술] Base64 이미지 업로드 및 정적 파일 저장소 구조.md>) 참고.

## ✅ 검증 및 결과

- [x] Base64 이미지 첨부 후 등록 시 `.webp` 파일 생성 및 `IMG_CD`에 URL 저장 확인
- [x] 수정 시 기존 이미지 삭제 + 신규 이미지 저장 확인
- [x] 수정 요청에서 `IMAGE` 값을 빈 문자열로 보내면 기존 이미지만 삭제되고 `IMG_CD`가 null로 갱신되는 것 확인
- [x] 게시글 삭제 시 첨부 이미지 파일도 함께 삭제되는 것 확인

## 🔗 참고

- [[평택대학교앱 리워크 개발 과정]]
- [\[기술\] Base64 이미지 업로드 및 정적 파일 저장소 구조](<../03_TechDocs/[기술] Base64 이미지 업로드 및 정적 파일 저장소 구조.md>)
- [\[기술\] 게시판 4종 CRUD 패턴과 예외·CORS 처리](<../03_TechDocs/[기술] 게시판 4종 CRUD 패턴과 예외·CORS 처리.md>)
