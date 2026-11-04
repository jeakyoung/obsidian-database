---
title: SALT 기반 로그인 인증 흐름
date: 2026-09-18
type: 기술문서
project: 대학프로젝트
status: 완료
category: 인증
assignee:
  - 안재경
tags: []
---

# SALT 기반 로그인 인증 흐름

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | `4th_GraduationBack` (`StuInfoController`, `LoginController`, `RegiService`), `4th_GraduationFront`(`crypto-js`) |
| **적용 범위** | 인증 |
| **관련 모듈** | `RegiService.basicRegiUserData`, `StuInfoService.getSaltByMembId`, `LoginService.authenticateUser` |

> 세션·JWT 없이, 회원가입 시 서버가 발급한 SALT를 프론트가 들고 있다가 로그인 직전 비밀번호를 해싱해서 보내는 구조. 서버는 저장된 값과 단순 비교만 한다.

## 🎯 배경 및 요구사항

별도 인증 서버·토큰 발급 인프라를 두지 않고, 비밀번호를 네트워크에 평문으로 흘리지 않는 최소한의 방어만 구현해야 했다.

## 🏗 설계 및 구현

### 전체 흐름

```
[회원가입]
RegiService.basicRegiUserData()
  → SecureRandom 16바이트 SALT 생성 → Base64 인코딩 → stu_info.SALT 컬럼에 저장
  → 응답으로 SALT를 프론트에 전달

RegiController POST /StdInfo
  → 프론트가 SALT로 해싱한 PASS 값을 그대로 전달받아 stu_info.PASS 컬럼에 저장

[로그인]
StuInfoController POST /getSalt
  → StuInfoService.getSaltByMembId() → stu_info.SALT 조회 후 반환

LoginController POST /PTU/Login
  → LoginService.authenticateUser()
     UserModel user = loginDao.findByMembId(membId);
     if (!user.getPass().equals(pass)) → 로그인 실패
```

프론트(`4th_GraduationFront`)는 `crypto-js`를 의존성으로 두고 있어, 로그인 화면 진입 시 `/getSalt`로 SALT를 받아온 뒤 그 SALT로 비밀번호를 해싱해 `/PTU/Login`에 전달하는 것으로 추정된다(프론트 상세 구현은 이 문서 범위 밖).

### 핵심 코드

```java
// LoginService.authenticateUser — 저장된 값과 단순 문자열 비교
UserModel user = loginDao.findByMembId(membId);
if (user == null) {
    return ResponseEntity.ok(new LoginRsltModel("02")); // ID 없음
}
if (!user.getPass().equals(pass)) {
    return ResponseEntity.ok(new LoginRsltModel("01")); // 비밀번호 불일치
}
return ResponseEntity.ok(new LoginRsltModel("00", user.getStdNum(), user.getStdDepCd(), user.getName()));
```

### 알려진 한계

> [!warning] 해시값이 곧 인증 토큰과 동일하게 동작한다
> 서버는 클라이언트가 보낸 값을 저장된 값과 `equals()`로만 비교한다. 즉 SALT+비밀번호로 만든 해시값 자체가 그대로 "비밀번호" 역할을 하므로, 이 값이 유출되면(예: 네트워크 스니핑 방어가 없는 구간, XSS 등) 공격자가 원본 비밀번호를 몰라도 그 값을 그대로 재전송(replay)해 로그인할 수 있다. 매 요청마다 challenge/nonce를 바꾸는 구조가 아니기 때문이다.

> [!note] 로그인 성공 후 세션/토큰이 없다
> `LoginRsltModel`은 학번·학과코드·이름을 응답에 담아 반환할 뿐, 이후 요청을 인증하기 위한 세션 쿠키나 JWT를 발급하지 않는다. 이후 화면들이 어떻게 "로그인 상태"를 유지하는지는 프론트 로컬 저장소 구현에 달려 있다(BE 범위 밖).

## ✅ 검증

- [x] 회원가입 시 SALT가 발급되어 `stu_info.SALT`에 저장되는지 확인
- [x] `/getSalt`로 같은 값을 다시 조회할 수 있는지 확인
- [x] 로그인 시 저장된 `PASS` 값과 다른 값을 보내면 `RSLT_CD 01` 반환 확인
- [ ] 세션/토큰 기반 인증으로의 전환 여부는 프로젝트 중단으로 검토되지 못함

## 🔗 참고

- [[회원가입 절차 다단계 분리 및 SALT 발급 구조 도입]]
- [[평택대학교앱 리워크 개발 과정]]
