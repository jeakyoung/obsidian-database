---
base: "[[Notion/프로젝트 문서화/프로젝트/NoNAME 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 진행 중
생성 일시: 2026-06-10T14:29:00
담당자: []
---
---

# 📱 React Native / Expo 빌드 명령어 가이드

| 상황 | 명령어 | 비고 |
| --- | --- | --- |
| **로컬 개발 빌드** | `$env:APP_VARIANT="development"; npx expo run:android` | PowerShell 환경 기준 (Windows) |
| **로컬 운영 빌드** | `npx expo prebuild --clean && npx expo run:android --variant release` | 네이티브 폴더 클린 후 Release 빌드 |
| **EAS 개발 빌드** | `eas build --profile development --platform android` | Expo Cloud 개발용 빌드 |
| **EAS 운영 빌드** | `eas build --profile production --platform android` | 스토어 배포용 최종 빌드 |

---

### 💻 명령어 상세 설명

### 1. 로컬 개발 빌드 (Local Development Build)

> 로컬 머신에서 에뮬레이터나 실기기를 연결하여 개발 모드로 네이티브 빌드를 진행할 때 사용합니다.

```powershell
$env:APP_VARIANT="development"; npx expo run:android
```