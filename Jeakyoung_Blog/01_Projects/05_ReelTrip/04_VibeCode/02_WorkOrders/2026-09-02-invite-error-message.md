---
title: 초대 에러 메시지 처리
date: 2026-09-02
type: 작업지시서
project: ReelTrip
status: 완료
assignee:
  - 안재경
tags: []
---

# 작업지시서

> Claude가 요구사항을 분석해 작성하는 문서입니다.
> 사용자 컨펌 후 작업이 시작됩니다.

---

## 작업 개요

| 항목 | 내용 |
|------|------|
| **작성일** | 2026-09-02 |
| **대상 앱** | Web |
| **대상 파일** | `InviteMemberModal.tsx` |
| **작업 유형** | 버그 수정 (UX) |
| **예상 영향 범위** | `InviteMemberModal.tsx` 단일 파일 |

---

## 요구사항 분석 요약

초대 요청 실패 시 에러 메시지가 `errorCode`에 관계없이 항상 동일한 문구를 표시한다.
`res.errorCode`를 활용해 실패 원인에 맞는 메시지를 표시하도록 수정한다.

---

## 작업 계획

### 1단계 — 에러 메시지 분기 처리

`handleSubmit` 내 `else` 블록을 아래와 같이 변경한다.

**변경 전:**
```typescript
} else {
  setError("초대에 실패했습니다. 사용자 이름을 확인해주세요.");
}
```

**변경 후:**
```typescript
} else {
  if (res.errorCode === "USER_NOT_FOUND") {
    setError("해당 사용자를 찾을 수 없습니다. 사용자 이름을 확인해주세요.");
  } else if (res.errorCode === "ALREADY_MEMBER") {
    setError("이미 이 스페이스의 멤버입니다.");
  } else {
    setError("초대에 실패했습니다. 잠시 후 다시 시도해주세요.");
  }
}
```

---

## 변경 대상 파일

| 파일 경로 | 변경 유형 | 변경 내용 요약 |
|-----------|-----------|----------------|
| `apps/web/src/domains/teamspace/components/InviteMemberModal.tsx` | 수정 | errorCode 기반 에러 메시지 분기 |

---

## 사이드 이펙트 검토

- 단일 파일, 단일 블록 수정 — 다른 파일 영향 없음
- 기존 에러 처리 구조 유지, 메시지 텍스트만 분기

---

## 컨펌

- [ ] 위 계획대로 진행 승인
- [ ] 수정 후 재검토 필요
