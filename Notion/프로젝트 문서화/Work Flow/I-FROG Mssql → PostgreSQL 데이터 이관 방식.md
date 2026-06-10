---
base: "[[Work Flow.base]]"
할당: []
상태: 검토 중
프로젝트: []
---
ㅇ PostgreSQL → ID, PWD : 맨날쓰던거

→ 마이그레이션툴 ( 이런것도 존재함 레코드 5000개까진 무료지원 )

[https://sanot.tistory.com/241](https://sanot.tistory.com/241)

[https://www.dbsofts.com/articles/postgresql_to_sqlserver/](https://www.dbsofts.com/articles/postgresql_to_sqlserver/)

→ 데이터 타입 매핑 → **DATE 연산 안됨

[https://developerstudymemo.tistory.com/entry/MSSQL-to-PostgreSQL-Migration-%EB%B3%80%ED%99%98-%EC%9E%91%EC%97%85](https://developerstudymemo.tistory.com/entry/MSSQL-to-PostgreSQL-Migration-%EB%B3%80%ED%99%98-%EC%9E%91%EC%97%85)

CAST, CONVERT → MSSQL의 방식

→ 생각보다 문법적 차이가 존재함 ( 사용하던 SP가 단순 조회, 생성용이라 큰문제는 없을듯. )

→pgloader ( 가장 흔하게 사용됨 )

[https://j2doll.tistory.com/1327](https://j2doll.tistory.com/1327)

```sql
-- msSQL
CREATE TABLE [dbo].[TGI003](
	[TICKER] [varchar](3) NOT NULL,
	[EMPLOYEE_NO] [varchar](10) NOT NULL,
	[APPROVAL_CHK_FLAG] [char](1) NULL,
	[BOARD_CHK_FLAG] [char](1) NULL,
	[NOTI_CHK_FLAG] [char](1) NULL,
	[SCHEDULE_CHK_FLAG] [char](1) NULL,
	[OPTIME] [datetime2](7) NULL,
	[OPTIME2] [datetime2](7) NULL,
 CONSTRAINT [PK_TGI003_1] PRIMARY KEY CLUSTERED 
(
	[TICKER] ASC,
	[EMPLOYEE_NO] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

--PostgreSQL
CREATE TABLE TGI003 (
    ticker VARCHAR(3) NOT NULL,
    employee_no VARCHAR(10) NOT NULL,
    approval_chk_flag CHAR(1),
    board_chk_flag CHAR(1),
    noti_chk_flag CHAR(1),
    schedule_chk_flag CHAR(1),
    optime TIMESTAMP(6),
    optime2 TIMESTAMP(6)
);
```

