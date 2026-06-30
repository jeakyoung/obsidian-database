---
base: "[[Notion/프로젝트 문서화/프로젝트/세한MT 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:29:00
담당자: []
---
00. 통합 뷰 로그인 화면- 아이디/비밀번호 입력- 확인 버튼 클릭

![[image 77.png]]


01. 메인 메뉴 화면-생산 실적 입력 선택 OR 설비 연동 관리 선택-각각 선택된 팝업 이동

![[image 78.png]]

2026-03-06 11:28:13.3630000

WORK_CODE → PR095

EQUIP_SYS_CD → EQ053

000001	EQ053	HG001


02. 생산 실적 관리 화면-작업장, 공정, 설비 선택-진행할 작업 선택-작업 시작 및 생산량 입력,불량수량 입력, 작업중단, 작업 종료-DB저장 확인



03. 설비 연동 관리-작업장, 작업공정선택



04. 생산 일정-지정된 기간 내의 생산 계획 출력



05 작업 일보-지정된 설비의 하루치 작업에 대한 기록 출력


→ 수정 필요사항



- Vercel에 올리는 실제 절차를 기준으로, 지금 저장소 구조에서 어디를 눌러야 하는지까지 정리하겠습니다. 최신 기준과 맞추기 위해 Vercel 공식 문서도 확인한 뒤, 이 프로젝트에 맞는 배포 순서를 바로 적용 가능한 형태로 답하겠습니다.

◦ Searching the web

- Searched Vercel official docs import git repository root directory next.js environment variables build command 2026

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

- 지금 프로젝트는 Spring Boot처럼 서버를 직접 띄워서 올리는 방식이 아니라, front-end를 Vercel에 배포하면 Next.js 서버 함수가 API를 대신 실행하는 구조입니다.

핵심만 먼저 적으면:

1. GitHub에 현재 코드를 push
2. Vercel에서 저장소 import
3. Root Directory를 front-end로 설정
4. 환경변수 등록
5. Deploy
6. 배포 URL에서 /test-ui, /api-docs, /docs, /api/documents/health로 확인

이 프로젝트 기준으로는 이렇게 하면 됩니다.

7. 먼저 로컬에서 최종 확인
루트가 아니라 front-end 기준입니다.

cd C:\Github\back-end\front-end
npm run build

이건 이미 현재 구조상 통과하도록 맞춰둔 상태입니다.

8. GitHub에 올리기
Vercel은 보통 Git 연동으로 배포합니다.

cd C:\Github\back-end
git add .
git commit -m "migrate backend to nextjs"
git push

9. Vercel에서 프로젝트 생성
Vercel 대시보드에서:
- Add New...
- Project
- GitHub 저장소 선택
- Import

중요:

- Root Directory를 반드시 front-end로 지정해야 합니다.

이걸 안 하면 루트에서 빌드하려고 해서 실패합니다.

10. Vercel Build 설정
이 프로젝트는 보통 자동 인식됩니다.
- Framework Preset: Next.js
- Root Directory: front-end
- Install Command: npm install
- Build Command: npm run build

front-end/package.json에서 build는 이미 prisma generate && next build로 되어 있어서 추가 수정은 보통 필요 없습니다.

11. 환경변수 등록
Vercel Dashboard > Project > Settings > Environment Variables 에 아래 추가:
- DATABASE_URL
- OPENAI_API_KEY
- JWT_SECRET
- JWT_EXPIRATION
- NEXT_PUBLIC_APP_URL

예시:

DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require
OPENAI_API_KEY=
JWT_SECRET=replace-with-a-long-random-secret
JWT_EXPIRATION=86400000
NEXT_PUBLIC_APP_URL=https://your-project.vercel.app

주의:

- 환경변수 변경은 기존 배포에 소급 적용되지 않고, 새 배포부터 적용됩니다.
12. DB는 로컬 Docker 말고 외부 DB 필요
중요한 최신 사항 하나:
- Vercel 공식 문서 기준, Vercel Postgres는 신규용으로 직접 제공되지 않고 외부 Postgres Marketplace 연동 방식이며 기존 것은 2024년 12월에 Neon으로 이전되었습니다.
- 지금은 Neon 같은 외부 Postgres를 연결하는 쪽이 현실적입니다.

즉 배포용 DB는 이런 걸 쓰면 됩니다.

- Neon
- Supabase Postgres
- pgvector 지원 PostgreSQL

필수 조건:

- pgvector extension 가능
- SSL 연결 가능
13. 배포 후 확인 방법
배포 주소가 예를 들어:

[https://example.vercel.app](https://example.vercel.app/)

라면 확인 순서는:

- 앱 홈: [https://example.vercel.app](https://example.vercel.app/)
- 테스트 페이지: [https://example.vercel.app/test-ui](https://example.vercel.app/test-ui)
- Scalar 문서 UI: [https://example.vercel.app/api-docs](https://example.vercel.app/api-docs)
- OpenAPI JSON: [https://example.vercel.app/docs](https://example.vercel.app/docs)
- 헬스체크: [https://example.vercel.app/api/documents/health](https://example.vercel.app/api/documents/health)

가장 먼저 볼 주소:

- /api/documents/health
- /api-docs
- /test-ui
14. Spring Boot처럼 “올리고 확인”하는 감각으로 보면
대응 관계는 이렇습니다.
- Spring Boot jar 실행 → Vercel Deploy
- Spring Boot Swagger UI → Vercel 배포 후 /api-docs
- Spring Boot actuator/health 비슷한 확인 → /api/documents/health
- Spring Boot Postman 테스트 → /test-ui 또는 /api-docs

즉 서버 프로세스를 직접 관리하는 게 아니라:

- Git push
- Vercel이 build
- URL 접속해서 확인

이 흐름입니다.

15. CLI로도 가능
Vercel CLI를 쓰면 더 Spring Boot 배포 감각에 가깝게 할 수 있습니다.

npm i -g vercel
cd C:\Github\back-end\front-end
vercel

운영 배포는:

vercel --prod

다만 처음 한 번은 대시보드에서 Root Directory와 환경변수 설정하는 방식이 더 안전합니다.

16. 지금 바로 권장 순서
17. GitHub push
18. Vercel에서 Import
19. Root Directory front-end
20. 환경변수 입력
21. Deploy
22. 배포 URL에서 /api-docs 확인
23. /api/documents/health 확인
24. /test-ui에서 signup/login 확인

공식 문서:

- Builds: [https://docs.vercel.com/docs/builds](https://docs.vercel.com/docs/builds)
- Environment Variables: [https://vercel.com/docs/environment-variables](https://vercel.com/docs/environment-variables)
- Postgres on Vercel: [https://vercel.com/docs/postgres](https://vercel.com/docs/postgres)
- Next.js on Vercel: [https://vercel.com/docs/concepts/next.js/overview](https://vercel.com/docs/concepts/next.js/overview)

원하면 다음 답변에서 바로

- Vercel 대시보드에서 어디를 눌러야 하는지
- Neon DB를 붙이는 순서
- 배포 후 첫 테스트 체크리스트
이 3개를 화면 순서대로 적어드리겠습니다.