---
title: URL 파서 수집 전략 (YouTube Shorts · Instagram Reels)
date: 2026-09-17
type: 기술문서
project: ReelTrip
status: 완료
category: 외부연동
assignee:
  - 안재경
tags: []
---

# URL 파서 수집 전략 (YouTube Shorts · Instagram Reels)

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | API (Spring) |
| **적용 범위** | 외부연동 |
| **관련 모듈** | `urlparser.collector.*`, `ai.service.AiService` |

> 서비스 핵심 기능(유튜브 쇼츠/인스타 릴스 링크 하나로 장소 정보 자동 등록)의 뒷단. 플랫폼마다 수집 전략이 완전히 다르다

## 🎯 배경 및 요구사항

사용자가 여행 콘텐츠 링크를 던지면 장소 이름·카테고리·주소·가격대 같은 정보를 자동으로 뽑아서 저장해주는 게 이 서비스의 핵심 기능이다. 근데 유튜브랑 인스타는 콘텐츠 접근 방법 자체가 다르다 — 유튜브는 공식 oEmbed API가 무료로 열려있고, 인스타는 공식 API로 릴스 콘텐츠(캡션, 위치 태그 등)를 가져올 방법이 없다. 그래서 플랫폼별로 아예 다른 수집기(`ContentCollector` 구현체)를 뒀다.

## 🏗 설계 및 구현

### 전체 흐름

```
UrlParserServiceImpl.parse(url)
  → UrlDetector.detect(url)                     // 플랫폼 판별 + ID 추출
  → (youtube_shorts | instagram_reels) 별 Collector.collect()
  → RawCollectedContent (title/caption/transcript/hashtags/locationName/thumbnailUrl)
  → AiService.extractTravelInfo(rawMap)          // Gemini 호출, 구조화된 여행 정보로 변환
  → result (+ sourceUrl, sourcePlatform, thumbnailUrl, rawContent)
```

`ContentCollector` 인터페이스 하나를 두 구현체가 따르는 전략 패턴 — `UrlParserServiceImpl`은 플랫폼이 뭔지만 알고, 실제로 어떻게 데이터를 가져오는지는 전혀 모른다.

### YouTube Shorts — 전부 무료 공개 경로로 처리

```java
// oEmbed로 제목/썸네일
String oEmbedJson = RestClient.create().get()
    .uri("https://www.youtube.com/oembed?url=" + encodedUrl + "&format=json")
    .retrieve().body(String.class);

// 자막(transcript)은 watch 페이지 HTML에서 caption track URL을 정규식으로 긁어낸 뒤
// 그 URL의 timedtext XML을 파싱
Matcher captionMatcher = Pattern.compile(
    "\"captionTracks\":\\[\\{\"baseUrl\":\"(.*?)\"").matcher(html);
```

`youtube-transcript` 같은 npm 패키지가 하는 일을 Java로 직접 재구현한 것 — 공식 API가 아니라 유튜브 페이지 구조에 의존하는 스크래핑이라, 유튜브가 마크업을 바꾸면 이 부분이 조용히 깨질 수 있다. 대신 Apify 같은 유료 서비스를 안 써도 되니 유튜브 콘텐츠는 처리 비용이 0에 가깝다.

### Instagram Reels — Apify 액터 호출

인스타는 공식적으로 릴스 콘텐츠를 가져올 방법이 없어서, Apify의 `instagram-reel-scraper` 액터를 동기 실행 엔드포인트로 호출한다.

```java
String endpoint = "/v2/acts/" + actorId + "/run-sync-get-dataset-items?token=" + apifyToken;
Map<String, Object> body = Map.of("directUrls", List.of(normalizedUrl), "resultsType", "posts");
```

`run-sync-get-dataset-items`는 Apify가 스크래핑을 실제로 끝낼 때까지 응답을 안 주고 기다리는 방식이라, 유튜브 쪽보다 훨씬 느리다. Mobile 쪽 URL 파서 API 타임아웃을 10초 → 30초로 늘린 이유가 이것 — Apify 액터 실행 시간이 10초를 넘기는 경우가 실제로 있었다.

빈 배열이 오면 비공개 계정으로 간주해서 `PRIVATE_CONTENT` 에러를 던진다.

### 수집 결과 → AI 추출

두 수집기 모두 `RawCollectedContent`(title/caption/transcript/hashtags/locationName/thumbnailUrl)라는 동일한 형태로 결과를 맞춰서 반환하고, 그 다음부터는 플랫폼 구분 없이 `AiService.extractTravelInfo()` 하나로 처리된다 — Gemini에게 원본 콘텐츠를 던지고 장소명/카테고리/주소/가격/영업시간 등을 JSON으로 뽑아달라고 요청하는 구조([\[기술\] 모노레포 기반 설정](<[기술] 모노레포 기반 설정.md>)에 정리한 Claude→Gemini 스왑 흔적이 바로 이 메서드).

## ✅ 검증

- [x] 유튜브 쇼츠 링크 파싱 시 제목/썸네일/자막 추출 확인
- [x] 인스타 릴스 링크 파싱 시 캡션/위치/썸네일 추출 확인
- [x] 비공개 인스타 계정 링크 시 `PRIVATE_CONTENT` 에러 확인
- [ ] 유튜브 마크업 변경에 대한 회귀 테스트 (수동 확인 외 자동화 없음)

## 🔗 참고

- `apps/api-spring/src/main/java/com/reeltrip/api/urlparser/collector/YoutubeShortCollector.java`
- `apps/api-spring/src/main/java/com/reeltrip/api/urlparser/collector/InstagramReelsCollector.java`
- [\[기술\] 모노레포 기반 설정](<[기술] 모노레포 기반 설정.md>)
