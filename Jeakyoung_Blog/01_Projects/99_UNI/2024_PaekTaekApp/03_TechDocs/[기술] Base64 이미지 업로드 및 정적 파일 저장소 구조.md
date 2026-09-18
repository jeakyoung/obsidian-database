---
title: Base64 이미지 업로드 및 정적 파일 저장소 구조
date: 2026-09-18
type: 기술문서
project: 대학프로젝트
status: 완료
category: 파일저장
assignee:
  - 안재경
tags: []
---

# Base64 이미지 업로드 및 정적 파일 저장소 구조

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | `4th_GraduationBack` — `ImageFileUploadSystem` |
| **적용 범위** | 파일저장 |
| **관련 모듈** | `service/ImageFileUploadSystem.java` |

> 별도 오브젝트 스토리지 없이, API 서버가 떠 있는 EC2 로컬 디스크에 날짜별 디렉토리로 이미지를 저장한다. 입력 포맷과 무관하게 전부 `.webp` 확장자로 저장한다.

## 🎯 배경 및 요구사항

게시판(공지·학사·입학·장학) 4종 모두 이미지 첨부가 필요했는데, S3 같은 별도 스토리지를 두지 않고 API 서버 자체에 저장하기로 했다.

## 🏗 설계 및 구현

### 저장 구조

```
/var/www/ptu/uploads/
└── yyyyMMdd/                        # 오늘 날짜 디렉토리 (LocalDate.now())
    └── {yyyyMMdd}_{userId}[N].webp  # 중복 시 숫자 접미사 증가
```

```java
public String saveImageFile(MultipartFile file, byte[] imageBytes, String userId) throws IOException {
    String dateDir = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd"));
    Path userDir = Paths.get(uploadDir, dateDir);
    if (Files.notExists(userDir)) Files.createDirectories(userDir);

    String filenameBase = String.format("%s_%s", dateDir, userId);
    Path imagePath;
    int counter = 0;
    do {
        String filename = (counter == 0) ? filenameBase : filenameBase + counter;
        imagePath = userDir.resolve(filename + ".webp");
        counter++;
    } while (Files.exists(imagePath));

    if (file != null) {
        Files.copy(file.getInputStream(), imagePath, StandardCopyOption.REPLACE_EXISTING);
    } else if (imageBytes != null) {
        Files.write(imagePath, imageBytes);
    } else {
        throw new IllegalArgumentException("No valid image data provided");
    }
    return clientBaseUrl + "/uploads/" + dateDir + "/" + imagePath.getFileName();
}
```

- `MultipartFile`과 Base64 `byte[]` 두 입력 경로를 모두 지원하지만, 게시판 4종은 전부 Base64 경로(`decodeBase64Image` → `saveImageFile(null, imageBytes, userId)`)만 사용한다.
- 확장자는 입력 이미지의 실제 포맷(JPEG/PNG 등)과 무관하게 항상 `.webp`로 고정된다 — 실제 파일 내용을 WebP로 변환하는 코드는 없고, 확장자만 `.webp`로 붙인다.
- DB(`IMG_CD` 컬럼)에는 파일시스템 경로가 아니라 `client.base.url` 설정값을 붙인 클라이언트 접근용 URL을 저장한다.

### 삭제 로직의 하드코딩

```java
public boolean deleteImageFile(String imagePath) {
    ...
    String serverFilePath = imagePath.replaceFirst("^http://89.168.40.124:8080/uploads/", "/var/www/ptu/uploads/");
    Path filePath = Paths.get(serverFilePath);
    if (Files.exists(filePath)) {
        Files.delete(filePath);
        return true;
    }
    ...
}
```

> [!warning] 저장 시에는 설정값을, 삭제 시에는 하드코딩된 IP를 쓴다
> `saveImageFile`은 `@Value("${client.base.url}")`로 주입받은 `clientBaseUrl`을 사용하지만, `deleteImageFile`은 URL에서 서버 경로를 되돌릴 때 IP(`89.168.40.124:8080`)를 정규식에 직접 박아뒀다. `client.base.url` 설정값이 바뀌면(예: 도메인 전환) 저장은 새 URL로 되는데 삭제는 여전히 옛 IP 기준으로 매칭을 시도해 실패하게 된다 — 실제로 값이 바뀐 적은 없어서 드러나지 않았던 잠재 버그.

## ✅ 검증

- [x] Base64 이미지 등록 시 날짜별 디렉토리에 `.webp` 파일 생성 확인
- [x] 같은 사용자·같은 날짜에 여러 장 등록 시 숫자 접미사로 파일명 충돌 회피 확인
- [x] 게시글 삭제 시 첨부 이미지 삭제 확인 (`client.base.url` 값이 코드의 하드코딩된 IP와 일치하는 동안에는 정상 동작)
- [ ] `client.base.url` 변경 시나리오에 대한 삭제 로직 회귀 테스트는 없음

## 🔗 참고

- [[게시판 이미지 첨부 Base64→WebP 저장 구조 구현]]
- [\[기술\] 게시판 4종 CRUD 패턴과 예외·CORS 처리](<[기술] 게시판 4종 CRUD 패턴과 예외·CORS 처리.md>)
