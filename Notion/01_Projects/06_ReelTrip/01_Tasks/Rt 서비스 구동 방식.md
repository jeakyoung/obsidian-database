---
base: "[[Notion/프로젝트 문서화/프로젝트/NoNAME 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 완료
생성 일시: 2026-06-10T14:29:00
담당자: []
---
---

회원가입 요청 전체 흐름

클라이언트 (Web/Mobile)

POST /api/auth/signup

{ username, password, email }

---

1단계 — middleware.ts (CORS 검사)

요청이 Route Handler에 도달하기 전에 무조건 먼저 통과합니다.

요청 origin이 ALLOWED_ORIGINS에 있는가?
→ 없으면: 403 차단 (OPTIONS일 때) 또는 CORS 헤더 없이 통과
→ 있으면: Access-Control-Allow-Origin 헤더 추가 후 다음으로

middleware.ts의 matcher: "/api/:path*" 때문에 /api/ 하위 모든 경로에 적용됩니다.

---

2단계 — route.ts (Route Handler, 진입점)

// signup/route.ts
const body = await request.json()       // 요청 body 파싱
const dto = SignupSchema.parse(body)    // ← DTO 검증
const data = await authService.signup(dto)
return ok(data)

Zod 검증 실패 시 → AppError(400, VALIDATION_ERROR) 즉시 반환
통과 시 → AuthService로 넘김

---

3단계 — auth.service.ts (비즈니스 로직)

// 1. username 중복 확인
await userRepository.existsByUsername(dto.username)  // 있으면 400 에러

// 2. email 중복 확인
await userRepository.existsByEmail(dto.email)        // 있으면 400 에러

// 3. 비밀번호 해싱
const hashedPassword = await bcrypt.hash(dto.password, 10)

// 4. DB 저장
await userRepository.create({ username, password: hashedPassword, email, role: "USER" })

// 5. JWT 발급
return { accessToken: await signToken({ sub: username, role }), ... }

---

4단계 — user.repository.ts (DB 접근)

prisma.user.count({ where: { username } })   // 중복 확인
prisma.user.create({ data })                  // 저장

User 테이블은 Prisma ORM을 정상적으로 사용합니다. (Document와 달리 vector 타입이 없어서 raw SQL 불필요)

---

5단계 — response.ts (응답 포맷)

성공/실패 모두 동일한 구조로 반환됩니다.

// 성공 (200)
{
"success": true,
"data": { "accessToken": "eyJ...", "tokenType": "Bearer", "username": "...", "email": "...", "role": "USER" },
"message": "success",
"errorCode": null,
"timestamp": 1234567890
}

// 실패 (400)
{
"success": false,
"data": null,
"message": "Username already exists: hong",
"errorCode": "USERNAME_ALREADY_EXISTS",
"timestamp": 1234567890
}

---

전체 계층 구조 한눈에

HTTP 요청
↓
middleware.ts       CORS 검사 (모든 /api/* 공통)
↓
route.ts            요청 파싱 + DTO(Zod) 검증 + 에러 캐치
↓
auth.service.ts     비즈니스 로직 (중복확인, 해싱, JWT 발급)
↓
user.repository.ts  DB CRUD (Prisma ORM)
↓
prisma.ts           PrismaClient 싱글톤 → PostgreSQL
↑
response.ts         ok() / handleError() 로 응답 포맷 통일

---


---

prisma db push 실행 시 Prisma가 내부적으로 하는 일:

schema.prisma의 현재 정의

↓

실제 DB의 현재 테이블 구조 조회
↓
둘을 비교 (diff)
↓
차이가 없으면 → 아무것도 안 함
차이가 있으면 → ALTER TABLE or CREATE TABLE 실행

---

예시

// schema.prisma에 age 컬럼 추가
model User {
id       BigInt @id
username String
age      Int     ← 새로 추가
}

prisma db push 실행
→ DB에 age 컬럼 없음을 감지
→ ALTER TABLE users ADD COLUMN age INTEGER 자동 실행

---

이미 테이블이 있으면 건드리지 않고, 없거나 다른 부분만 찾아서 최소한으로 변경해줍니다. 이게 Prisma가 편한 이유입니다.
