---
title: 게시판 4종 CRUD 패턴과 예외·CORS 처리
date: 2026-09-18
type: 기술문서
project: 대학프로젝트
status: 완료
category: 게시판
assignee:
  - 안재경
tags: []
---

# 게시판 4종 CRUD 패턴과 예외·CORS 처리

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | `4th_GraduationBack` — 공지/학사/입학/장학 게시판 + `GlobalExceptionHandler`, `CorsConfig` |
| **적용 범위** | 게시판 |
| **관련 모듈** | `NoticeListService`, `BachelorCheckService`, `EntranceCheckService`, `ScholarCheckService`, `SchorolshipService` |

> 공지사항 게시판을 원형으로 삼아 학사/입학/장학 게시판을 거의 그대로 복사해서 만들었다. 다섯 번째로 끼어든 `Schorolship`(장학금) 게시판만 패턴에서 벗어나 있고, 테이블 매핑도 잘못돼 있다.

## 🎯 배경 및 요구사항

공지·학사안내·입학안내·장학안내 4개 게시판이 전부 "제목/내용/작성자/첨부이미지 + 목록 조회(페이지네이션)/등록/수정/삭제"라는 동일한 요구사항을 가져서, 하나를 구현한 뒤 복사해 나머지를 만드는 방식으로 진행했다.

## 🏗 설계 및 구현

### 정상 4종의 공통 패턴

| 게시판 | 테이블 | Controller | Service | 엔드포인트 |
|:--|:--|:--|:--|:--|
| 공지사항 | `notice_list` | `ListController` | `NoticeListService` | `/PTU/Notice/{add,update,delete}` |
| 학사안내 | `bachelor_list` | `BachelorCheckController` | `BachelorCheckService` | `/bachelor`, `/PTU/Bachelor/{add,update,delete}` |
| 입학안내 | `entrance_list` | `EntranceCheckController` | `EntranceCheckService` | `/entrance`, `/PTU/Entrance/{add,update,delete}` |
| 장학안내 | `scholar_list` | `ScholarCheckController` | `ScholarCheckService` | `/scholar`, `/PTU/Scholar/{add,update,delete}` |

네 게시판 서비스 코드는 클래스명·필드명만 다를 뿐 로직이 사실상 동일하다(`diff`로 비교하면 변수명 치환 수준). 목록 조회는 `findAllByOrderByCreDateDesc(Pageable)`로 페이지당 10건씩 최신순 정렬한다. 등록/수정/삭제 시 이미지 처리는 [\[기술\] Base64 이미지 업로드 및 정적 파일 저장소 구조](<[기술] Base64 이미지 업로드 및 정적 파일 저장소 구조.md>) 참고.

### 다섯 번째 게시판(Schorolship)이 패턴에서 벗어난 지점

```java
// ScholarshipModel.java
@Entity
@Table(name = "notice_List")   // ← bachelor/entrance/scholar 처럼 전용 테이블이 아니라 notice_list를 그대로 참조
public class ScholarshipModel { ... }
```

```java
// SchorolshipService.java — 목록 조회/수정/삭제/이미지 처리 전부 없음
@Service
public class SchorolshipService {
    @Transactional
    public ScholarshipModel saveScholarship(ScholarshipModel scholarship) {
        if (scholarship.getTitle() == null || scholarship.getContent() == null) {
            throw new IllegalArgumentException("Title and Content cannot be null");
        }
        return scholarshipDao.save(scholarship);
    }
}
```

> [!warning] `/PTU/Schorolship/add`로 등록한 글이 공지사항 테이블에 들어간다
> `ScholarshipModel`의 `@Table(name = "notice_List")`는 `NoticeModel`의 매핑을 복사해오면서 테이블명을 못 고친 것으로 보인다. MariaDB는 테이블명 대소문자를 구분하지 않아 `notice_List`가 그대로 `notice_list`를 가리키므로 에러 없이 동작하지만, 실제로는 장학금 안내 글이 공지사항 게시판 데이터와 섞이게 된다. `ScholarCheck`(장학안내, `scholar_list` 테이블, 정상 동작)와 이름이 비슷해 둘을 혼동하기 쉽다.
>
> `SchorolshipController`/`Service`는 등록(`add`) 기능만 있고 목록 조회·수정·삭제·이미지 첨부가 없다 — 다른 4종 게시판과 달리 미완성 상태로 남아있다.

### 예외 처리

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(Exception.class)
    public ResponseEntity<CommonResponseModel> handleAllExceptions(Exception ex) {
        return new ResponseEntity<>(new CommonResponseModel("99"), HttpStatus.INTERNAL_SERVER_ERROR);
    }
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<CommonResponseModel> handleIllegalArgumentException(IllegalArgumentException ex) {
        return new ResponseEntity<>(new CommonResponseModel("99"), HttpStatus.BAD_REQUEST);
    }
}
```

일반 예외(500)와 잘못된 요청(400) 둘 다 `RSLT_CD "99"`로 동일하게 응답한다 — HTTP 상태 코드로는 구분되지만, 응답 바디만 보고는 "서버 내부 오류"와 "잘못된 요청"을 구분할 수 없다. 예외 메시지(`ex.getMessage()`)도 응답에 담기지 않아 클라이언트 쪽에서 원인 파악이 어렵다.

### CORS

```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**").allowedOrigins("*").allowedMethods("POST");
    }
}
```

모든 Origin을 허용하되 메서드는 `POST`만 열어뒀다 — 실제로 이 프로젝트의 거의 모든 엔드포인트가 `@PostMapping`(조회 포함)이라 문제없이 동작하지만, `GlobalExceptionHandler`가 던지는 405/404 같은 케이스에는 CORS 헤더가 안 붙어서 브라우저 콘솔에는 CORS 에러로 보일 수 있다.

## ✅ 검증

- [x] 공지/학사/입학/장학 4종 게시판의 등록·수정·삭제·목록 조회 동일 패턴 확인
- [x] `ScholarshipModel`이 `notice_list` 테이블에 실제로 쓰는지 엔티티 매핑 기준으로 확인
- [ ] `Schorolship` 게시판을 별도 테이블로 분리할지, 기능 자체를 제거할지는 프로젝트 중단으로 결정되지 못함

## 🔗 참고

- [[게시판 이미지 첨부 Base64→WebP 저장 구조 구현]]
- [\[기술\] Controller-Service-DAO 3계층 구조](<[기술] Controller-Service-DAO 3계층 구조.md>)
