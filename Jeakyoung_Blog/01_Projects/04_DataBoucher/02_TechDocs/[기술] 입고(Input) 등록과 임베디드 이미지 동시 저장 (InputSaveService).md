---
title: 입고(Input) 등록과 임베디드 이미지 동시 저장 (InputSaveService)
date: 2026-09-18
type: 기술문서
project: 데이터바우처
status: 완료
category: 이미지 파이프라인
assignee:
  - 안재경
tags: []
---

# 입고(Input) 등록과 임베디드 이미지 동시 저장 (InputSaveService)

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | F1Soft.Starmap.Service — Input |
| **적용 범위** | 입고 등록/수정/삭제 + 라벨 이미지 동시 저장 |
| **관련 모듈** | `InputListController`, `InputSaveController`, `InputSaveService`, `IImageService` |

> 모바일이 "입고 대상"을 조회해서 고른 뒤, 입고 정보와 라벨 사진(여러 장)을 **한 번의 요청**으로 같이 저장하는 흐름. [[01_Projects/04_DataBoucher/02_TechDocs/[기술] 입고 라벨 이미지 촬영·업로드·적재 파이프라인]]에서 다룬 단순 라벨 등록과 달리, 이쪽은 입고(Input) 레코드 + 이미지가 한 트랜잭션으로 묶인다.

## 🎯 배경 및 요구사항

데이터 바우처의 "입고대상 사진 촬영 → 저장 → DB 적재" 흐름은 단순히 사진만 올리는 게 아니라, 그 사진이 **어떤 입고 건**에 속하는지(거래처·원료·입고번호)가 같이 기록돼야 AI 분석 단계에서 의미를 갖는다. 그래서 입고 저장 API가 이미지 배열을 함께 받아, 입고 레코드 생성과 이미지 업로드를 하나의 작업으로 묶어야 했다.

## 🏗 설계 및 구현

### 조회: 입고 대상 선택 (모바일 쪽 진입점)

```
POST /api/Input/InputTargetList   ← 아직 입고 등록 안 된 대상 목록 (모바일에서 "이 중에 촬영할 것" 선택)
POST /api/Input/InputList         ← 이미 입고 등록된 내역 조회
```

두 엔드포인트 모두 `Dictionary<string, object?>` 리스트를 그대로 반환 — SP 컬럼을 DTO로 고정 매핑하지 않고 동적으로 흘려보내는 방식이라, SP 쪽에 컬럼이 추가되면 별도 배포 없이 응답에 바로 반영된다(대신 클라이언트가 스키마를 신뢰하고 파싱해야 함).

### 저장: SaveInput → InputSaveService.SaveAsync

```
POST /api/Input/SaveInput
  { factoryCode, inputNo(신규 시 ""), inputSeqNo(신규 시 0), inputDate, customerCode,
    materialCode, ..., iud: "IU"|"D",
    images: [ { iud: "IU"|"D", imageBase64, imageExtension }, ... ] }   ← 선택, 여러 장 가능
```

```
InputSaveService.SaveAsync
  ├─ TransactionScope(TransactionScopeAsyncFlowOption.Enabled) 시작
  ├─ isImageOnlyUpdate = 기존 레코드(InputNo 있음) + images만 있는 경우 → SP_APP_INPUT_IUD 스킵
  ├─ (스킵 아니면) SP_APP_INPUT_IUD 호출 — 입고 메인/상세 저장
  ├─ IUD == "D" → 여기서 scope.Complete() 후 바로 반환 (이미지 처리 안 함)
  ├─ 신규 등록이면 SP_APP_INPUT_KEY 로 생성된 INPUT_NO/INPUT_SEQNO 조회
  ├─ images 배열을 순회하며 각 항목을 ImageService.UploadAsync(...) 로 개별 업로드
  │    (InputNo/InputSeqno를 방금 확정된 값으로 채워 넘김)
  │    ※ 반드시 순차(foreach + await) 처리 — Task.WhenAll 사용 시 TransactionScope가
  │      여러 커넥션을 동시에 열게 돼 MSDTC로 트랜잭션이 승격될 수 있어 의도적으로 순차 처리
  └─ scope.Complete()
```

> [!warning] SP 파라미터 이름의 오타를 그대로 쓴다
> `ExecuteInputIudAsync`에서 `{ "CHNAGE_INPUT_QTY", request.ChangeInputQty }`처럼 파라미터 키에 오타(`CHNAGE`)가 그대로 들어간다. C# 쪽 프로퍼티는 정상 철자(`ChangeInputQty`)인데, SP 파라미터 이름 자체가 오타로 정의돼 있어서 맞춰준 것으로 보인다. **이 오타를 "고치면" SP 호출이 깨진다** — SP 정의를 먼저 확인하지 않고 리팩터링하지 말 것.

> [!note] 이미지만 수정하는 경로 최적화
> `isImageOnlyUpdate`(기존 입고건 + 이미지 배열만 요청) 조건일 때는 `SP_APP_INPUT_IUD`를 아예 스킵한다. 입고 메인 정보는 안 바뀌고 사진만 추가/교체하는 모바일 시나리오(예: 촬영 실패 후 재촬영)를 위한 경로로 보인다.

## ✅ 검증

- [x] 신규 등록 시 `SP_APP_INPUT_KEY`로 채번된 `INPUT_NO`/`INPUT_SEQNO`가 이미지 저장에도 그대로 전달되는지 확인
- [x] `Iud == "D"` 요청 시 이미지 처리 없이 바로 종료되는지 확인
- [ ] 이미지 업로드 중 일부만 실패하는 경우(부분 실패) 트랜잭션 전체가 롤백되는지, 이미 FTP에 올라간 파일은 어떻게 되는지 — FTP 업로드는 `TransactionScope`가 롤백할 수 없는 외부 리소스라 별도 확인 필요

## 🔗 참고

- `Services/Input/InputSaveService.cs`, `Controllers/Input/{InputListController,InputSaveController}.cs`, `Models/Input/InputSaveRequest.cs`
- [[01_Projects/04_DataBoucher/02_TechDocs/[기술] 입고 라벨 이미지 촬영·업로드·적재 파이프라인]]
- [[01_Projects/04_DataBoucher/01_Tasks/데이터 바우처 입고·이미지·라벨 등수삭 구현 완료 07.09]]
