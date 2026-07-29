---
title: Notion 문서 저장소 - 구조 가이드
type: 안내
date: 2026-06-30
---

# 📚 Notion 문서 저장소 구조 가이드

> **완전히 정리된 직관적인 문서 관리 시스템**

---

## 🗂️ 전체 구조

```
Notion/
├── 01_Projects/                    📁 프로젝트 문서 (회사 & 개인)
│   ├── 01_ShinJinSM/              📂 신진SM ERP/MES 프로젝트
│   ├── 02_IPACK/                  📂 IPACK 근태 시스템
│   ├── 03_iFrog/                  📂 I-Frog POS 시스템
│   ├── 04_DongBang/               📂 동방푸드 ERP
│   ├── 05_SeHanMT/                📂 세한MT POP 시스템
│   ├── 06_NoNAME/                 📂 NoNAME 학습 프로젝트
│   ├── Template/                  📂 신규 프로젝트 템플릿
│   └── Archive/                   📂 완료된 프로젝트
│       ├── 2023_OpenSoop/
│       └── 2024_PaekTaekApp/
│
├── 02_Career/                      📁 경력 서류
│   ├── 01_Technical_Skills.md      📄 경력기술서
│   ├── 02_Resume.md                📄 이력서
│   ├── 03_CoverLetter.md           📄 자기소개서
│   └── 04_Portfolio.md             📄 포트폴리오
│
├── 03_Learning/                    📁 학습 & 기술 자료
│   ├── Backend/                    📂 백엔드 개발
│   │   ├── SpringBoot/             📂 Spring Boot 가이드
│   │   ├── Database/               📂 데이터베이스
│   │   └── Architecture/           📂 아키텍처 설계
│   ├── DevOps/                     📂 DevOps & 배포
│   ├── Tools/                      📂 개발 도구
│   └── References/                 📂 참고 자료
│
├── 04_WorkFlow/                    📁 일상 작업 기록
│   ├── DailyTasks/                 📂 프로젝트별 작업
│   ├── Meetings/                   📂 회의 기록
│   └── Logs/                       📂 작업 로그
│
├── 05_Archive/                     📁 보관함
│   └── Old_Structure/              📂 이전 폴더 구조 (참고용)
│
└── README.md                       📄 이 파일

```

---

## 📖 각 폴더 설명

### 01_Projects - 프로젝트 문서
모든 프로젝트의 기술 문서, 회의록, 작업 기록을 관리합니다.

**각 프로젝트 폴더 구조:**
```
01_ShinJinSM/
├── README.md              프로젝트 메인 인덱스
├── 01_Tasks/              작업 기록 (Task/Todo)
├── 02_Docs/               프로젝트 문서
├── 03_TechDocs/           기술 명세서
├── 04_Meetings/           회의록
└── 05_References/         참고 문서
```

**프로젝트 목록:**
- **01_ShinJinSM** - 신진SM ERP/MES 통합 시스템
- **02_IPACK** - IPACK 근태 관리 시스템
- **03_iFrog** - I-Frog POS 시스템
- **04_DongBang** - 동방푸드 ERP 시스템
- **05_SeHanMT** - 세한MT POP 시스템
- **06_NoNAME** - NoNAME AI/LLM 프로젝트 (개인 학습)
- **Template** - 신규 프로젝트 시작 템플릿
- **Archive** - 완료된 프로젝트 (2023_OpenSoop, 2024_PaekTaekApp)

---

### 02_Career - 경력 서류
Spring Boot 백엔드 지원용 경력 서류를 관리합니다.

| 파일 | 설명 |
|------|------|
| **01_Technical_Skills.md** | 경력기술서 (프로젝트별 기술 상세 분석) |
| **02_Resume.md** | 이력서 (기본정보, 경력, 기술스택) |
| **03_CoverLetter.md** | 자기소개서 (STAR 기법 적용) |
| **04_Portfolio.md** | 포트폴리오 (실제 사례, 코드 예시) |

---

### 03_Learning - 학습 & 기술 자료
개발 기술 및 학습 자료를 체계적으로 관리합니다.

```
03_Learning/
├── Backend/
│   ├── SpringBoot/        Spring Boot 심화
│   ├── Database/          DB 최적화, 인덱싱
│   └── Architecture/      시스템 아키텍처
├── DevOps/                Docker, Kubernetes, CI/CD
├── Tools/                 Git, IDE, 개발 도구
└── References/            API 문서, 가이드
```

---

### 04_WorkFlow - 일상 작업 기록
프로젝트별 작업, 회의, 로그를 기록합니다.

```
04_WorkFlow/
├── DailyTasks/            일일 업무, 프로젝트별 작업
├── Meetings/              회의 기록, 의사결정 사항
└── Logs/                  작업 로그, 회고
```

---

### 05_Archive - 보관함
이전 폴더 구조를 참고용으로 보관합니다.

```
05_Archive/
└── Old_Structure/         이전 구조 (참고용)
    ├── _프로젝트_문서화_OLD
    ├── _안재경_BE개발자_OLD
    ├── _정보저장소_OLD
    └── _기타문서_OLD
```

---

## 📝 파일 이름 규칙

### ✅ 명확한 이름
```
README.md                     프로젝트 메인 인덱스
01_Technical_Skills.md        순서_영문_이름
Task_Database_Optimization    Task_주제
2026-06-30_DailyLog.md       날짜_제목
Meeting_2026-06-30.md        Type_Date
```

### ❌ 복잡한 이름 (변경됨)
```
Project  Todo - 프로젝트 Todo           → 01_Tasks/
Project Docs- 프로젝트 문서             → 02_Docs/
[기술] 공통 배포 방법                  → 간단한 이름으로
```

---

## 🚀 사용 가이드

### 새 프로젝트 시작
```
1. 01_Projects/Template 복사
2. 폴더명을 프로젝트명으로 변경
3. README.md 수정
4. 하위 폴더에 문서 추가
```

### 문서 추가
```
프로젝트별 작업 → 04_WorkFlow/DailyTasks/
기술 문서       → 01_Projects/[ProjectName]/03_TechDocs/
회의록         → 01_Projects/[ProjectName]/04_Meetings/
참고 문서       → 01_Projects/[ProjectName]/05_References/
```

### 학습 자료 추가
```
백엔드 기술       → 03_Learning/Backend/
DevOps/배포      → 03_Learning/DevOps/
도구 사용법       → 03_Learning/Tools/
API 문서 등      → 03_Learning/References/
```

---

## 📊 정리 현황

| 항목 | 상태 | 설명 |
|------|------|------|
| **폴더 구조** | ✅ 완료 | 5개 대분류, 15+ 소분류 |
| **프로젝트 문서** | ✅ 완료 | 9개 프로젝트 정리 |
| **경력 서류** | ✅ 완료 | 4개 문서 정리 |
| **학습 자료** | ✅ 완료 | Backend, DevOps 등 분류 |
| **파일명 정리** | ✅ 완료 | 직관적 이름으로 통일 |
| **기존 폴더** | 📦 보관 | Archive/Old_Structure에 보관 |

---

## 💡 핵심 개선사항

```
Before (혼란스러웠던 구조)
├── 프로젝트 문서화/
│   ├── 프로젝트/
│   │   └── 신진SM 프로젝트 DB/
│   │       └── Project  Todo - 프로젝트 Todo/
│   └── Work Flow/프로젝트별 작업/
├── 안재경  BE 개발자/
└── 정보 저장소/

After (깔끔한 구조)
├── 01_Projects/01_ShinJinSM/01_Tasks/
├── 02_Career/
├── 03_Learning/Backend/
├── 04_WorkFlow/DailyTasks/
└── 05_Archive/
```

---

## ⚠️ 이전 구조 위치

이전 폴더는 다음 위치에 보관되어 있습니다:
```
05_Archive/Old_Structure/
```

필요한 경우 참고할 수 있습니다.

---

## 📞 문서 유지보수

### 월별 관리
- **1주차:** 폴더 구조 검증
- **2주차:** 파일명 일관성 확인
- **3주차:** 오래된 문서 아카이빙
- **4주차:** 신규 템플릿 업데이트

### 문서 추가 시 확인사항
- [ ] 올바른 폴더에 저장했는가?
- [ ] 파일명이 명확한가?
- [ ] README가 있는가?
- [ ] 상위 폴더와 링크되어 있는가?

---

**구조화 완료일:** 2026-06-30  
**상태:** ✅ 정리 완료  
**Quartz 배포:** 2026-07-29 ✨  
**다음 단계:** GitHub Pages 블로그 운영

