---
base: "[[Notion/프로젝트 문서화/프로젝트/IPACK 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 진행 중
생성 일시: 2026-06-10T14:28:00
담당자: []
---
```sql
USE [iPlusERP_IPACK_DEV]
GO
/****** Object:  StoredProcedure [dbo].[SP_WHR314_01_LIST]    Script Date: 2025-09-24 오후 2:55:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER OFF
GO

ALTER PROCEDURE [dbo].[SP_WHR314_01_LIST]          
(               
    @FACTORY_CODE       VARCHAR(6),
    @KT_DATE            CHAR(8), 
    @WORK_TEAM          VARCHAR(8),
    @DEPARTMENT_NAME    VARCHAR(20),
    @EMPLOYEE_NAME      VARCHAR(20)
)
-- SP_WHR314_01_LIST '000001', '20250917', '', '', ''
AS  
BEGIN              
    SET NOCOUNT ON;     
	BEGIN

	WITH 
    Event_CTE AS (
        -- 1. 당일(@KT_DATE)의 출입기록을 사번별 순서대로 가져옴
        --    NREADERIDN 으로 '입실' / '퇴실' 구분
        SELECT 
              ROW_NUMBER() OVER (PARTITION BY EMPLOYEE_NO ORDER BY KT_DATETIME) AS rn
            , KT_DATETIME AS IO_DATETIME
            , CASE 
                WHEN NREADERIDN IN (546839596, 546839166) THEN '입실'
                WHEN NREADERIDN IN (546839433, 546839434) THEN '퇴실'
                ELSE '기타'
              END AS IO_NAME
            , EMPLOYEE_NO
        FROM TIN334
        
        WHERE CONVERT(CHAR(8), KT_DATETIME, 112) = @KT_DATE
        AND NREADERIDN IN (546839166, 546839433, 546839434, 546839596)
    ),

    Pair_CTE AS (
        -- 2. 퇴실 → 바로 다음 입실을 짝지어서 외출시간(분)을 계산
        SELECT 
              O.EMPLOYEE_NO
            , O.IO_DATETIME AS OUT_TIME
            , I.IO_DATETIME AS IN_TIME
            , DATEDIFF(MINUTE, O.IO_DATETIME, I.IO_DATETIME) AS DURATION_TIME
        FROM Event_CTE O

            LEFT JOIN Event_CTE I
            ON O.EMPLOYEE_NO = I.EMPLOYEE_NO
            AND I.rn = O.rn + 1

        WHERE O.IO_NAME = '퇴실'
        AND I.IO_NAME = '입실'
    ),

    Outsum AS (
        -- 3. 사원별 총 외출시간 합계(분)
        SELECT EMPLOYEE_NO,
               SUM(DURATION_TIME) AS TOTAL_OUT_MINUTES
        FROM Pair_CTE
        GROUP BY EMPLOYEE_NO
    ),

    InOutsum AS (
        -- 4. 사원별 최초 입실, 최종 퇴실 계산
        SELECT EMPLOYEE_NO,
               MIN(CASE WHEN IO_NAME = '입실' THEN IO_DATETIME END) AS FIRST_IN,
               MAX(CASE WHEN IO_NAME = '퇴실' THEN IO_DATETIME END) AS LAST_OUT
        FROM Event_CTE
        GROUP BY EMPLOYEE_NO
    ),

    ValidInOut AS (
        -- 5. 유효한 출퇴근 판별
        --    (최초 입실 < 최종 퇴실일 때만 출근/퇴근 인정) 나중에 쓸일이 있을것같음,
        SELECT EMPLOYEE_NO,
               CASE 
                    WHEN LAST_OUT IS NOT NULL AND FIRST_IN < LAST_OUT 
                         THEN FIRST_IN 
                    ELSE NULL 
               END AS VALID_FIRST_IN,
               CASE 
                    WHEN LAST_OUT IS NOT NULL AND FIRST_IN < LAST_OUT 
                         THEN LAST_OUT 
                    ELSE NULL 
               END AS VALID_LAST_OUT
        FROM InOutsum
    ),

	WGInfo AS (
		SELECT 
			  EMPLOYEE_NO
			, WG_CODE
			, WG_ATTEND_GBN
			--, CAST((CAST(WG_PRDTO AS INT) - CAST(WG_PRDFROM AS INT)) AS FLOAT) / 100.0 AS BASIC_TIME

			, CASE  -- 근무 기본시간 고정
			  WHEN WG_ATTEND_GBN = '001' THEN 8.00
			  ELSE 0.00 END AS BASIC_TIME

			, WG_PRDFROM
			, WG_PRDTO
			, WG_LTIME
			, DU_YMD
			, ROW_NUMBER() OVER (
				PARTITION BY EMPLOYEE_NO, WG_CODE 
				ORDER BY 
					CASE WHEN DU_YMD = @KT_DATE THEN 0 ELSE 1 END,
					CASE WHEN DU_YMD IS NOT NULL THEN 0 ELSE 1 END,
					WG_PRDFROM DESC
			) AS rn
		FROM TIN313
	)

    -- 최종 결과 조회
    SELECT DISTINCT
          A.FACTORY_CODE
		, A.EMPLOYEE_NO
        , A.BASE_NAME
		, B.BASIC_TIME
		, FORMAT(I.FIRST_IN, 'HH:mm') + ' ~ ' + FORMAT(I.LAST_OUT, 'HH:mm') AS BASE_DIS
		, E.WG_CODE
        , C.WG_NAME                  AS WORK_TEAM
		, B.WG_ATTEND_GBN            AS CODE_ID2
		, B.DU_YMD					 AS DU_YMD
        , C.DEF_FROM_TIME            AS WORK_START_TIME
        , C.DEF_TO_TIME              AS WORK_END_TIME
		, D.Department_Name			 AS DEPARTMENT_NAME
        , I.FIRST_IN                 AS FIRST_IN
        , I.LAST_OUT                 AS LAST_OUT

        , ROUND (CAST(DATEDIFF(MINUTE, I.FIRST_IN, I.LAST_OUT) AS FLOAT) / 60.0, 2)				  AS WORK_TIME
        , ROUND (CAST( O.TOTAL_OUT_MINUTES AS FLOAT ) / 60.0 ,2 )								  AS OUT_MINUTES
		--, ROUND (CAST(DATEDIFF(MINUTE, I.FIRST_IN, I.LAST_OUT) AS FLOAT) / 60.0, 2) - BASIC_TIME	  AS OVER_TIME
		--, ROUND (CAST(DATEDIFF(MINUTE, B.WG_PRDTO, I.LAST_OUT) AS FLOAT) / 60.0, 2)				  AS EARLY_TIME
		--, ROUND (CAST(DATEDIFF(MINUTE, B.WG_PRDFROM, I.FIRST_IN ) AS FLOAT) / 60.0, 2)			  AS LATE_TIME  
		
		--, CASE
		--	  WHEN BASIC_TIME < ROUND(CAST(DATEDIFF(MINUTE, B.WG_PRDTO, I.LAST_OUT) AS FLOAT) / 60.0, 2)
		--	  THEN ROUND(CAST(DATEDIFF(MINUTE, B.WG_PRDTO, I.LAST_OUT) AS FLOAT) / 60.0, 2) - BASIC_TIME
		--	  ELSE 0.00 END AS OVER_TIME

		, CASE
			  WHEN CONVERT(FLOAT, REPLACE(CONVERT(CHAR(5), I.LAST_OUT, 108), ':', ''))
					< CAST(B.WG_PRDTO AS FLOAT)
			  THEN ROUND(((CAST(LEFT(B.WG_PRDTO, 2) AS FLOAT) * 60 + CAST(RIGHT(B.WG_PRDTO, 2) AS FLOAT)) 
					 - (DATEPART(HOUR, I.LAST_OUT) * 60 + DATEPART(MINUTE, I.LAST_OUT))) / 60.0, 2)

				ELSE 0
			  END AS EARLY_TIME

		, CASE
			  WHEN CONVERT(FLOAT, REPLACE(CONVERT(CHAR(5), I.LAST_OUT, 108), ':', ''))
					> CAST(B.WG_PRDTO AS FLOAT)
			  THEN  ROUND(((DATEPART(HOUR, I.LAST_OUT) * 60 + DATEPART(MINUTE, I.LAST_OUT))
					- (CAST(LEFT(B.WG_PRDTO, 2) AS FLOAT) * 60 + CAST(RIGHT(B.WG_PRDTO, 2) AS FLOAT))) / 60.0, 2)
			  ELSE 0
			  END AS OVER_TIME

		,CASE 
			 WHEN CONVERT(FLOAT, REPLACE(CONVERT(CHAR(5), I.FIRST_IN, 108), ':', ''))
					> CAST(B.WG_PRDFROM AS FLOAT)
			 THEN ROUND(((DATEPART(HOUR, I.FIRST_IN) * 60 + DATEPART(MINUTE, I.FIRST_IN))
					- (CAST(LEFT(B.WG_PRDFROM, 2) AS FLOAT) * 60 + CAST(RIGHT(B.WG_PRDFROM, 2) AS FLOAT))) / 60.0, 2)
			 ELSE 0
		 END AS LATE_TIME


		--, CASE
		--	  WHEN B.WG_PRDFROM < I.FIRST_IN
		--	  THEN  ROUND (ISNULL(CAST(DATEDIFF(MINUTE, B.WG_PRDFROM, I.FIRST_IN) AS FLOAT), 0) / 60.0  - BASIC_TIME - 0.5 , 3)
		--	  ELSE 0.00 END AS LATE_TIME



		, CASE 
			  WHEN E.WG_CODE = '002' THEN 7.00  
			  ELSE 0.00 END AS NIGHT_TIME

		, CASE 
			  WHEN E.WG_CODE = '002' THEN 1.00   
			  ELSE 0.00 END AS NIGHT_ALLOW 

    FROM TIN114 A

		LEFT JOIN TIN334 F
			ON A.EMPLOYEE_NO = F.EMPLOYEE_NO

        LEFT JOIN TIN122 D 
            ON A.DEPARTMENT_CODE = D.Department_Code

        LEFT JOIN TIN312 E 
            ON A.EMPLOYEE_NO = E.EMPLOYEE_NO

        LEFT JOIN TIN310 C 
            ON E.WG_CODE = C.WG_CODE

		--LEFT JOIN TIN313 B 
		--  ON A.EMPLOYEE_NO = B.EMPLOYEE_NO
		--	AND E.WG_CODE = B.WG_CODE

        --LEFT JOIN ValidInOut V 
        --  ON A.EMPLOYEE_NO = V.EMPLOYEE_NO

		LEFT JOIN WGInfo B
			ON A.EMPLOYEE_NO = B.EMPLOYEE_NO
			AND E.WG_CODE = B.WG_CODE
			AND B.RN=1

        LEFT JOIN InOutsum I 
            ON A.EMPLOYEE_NO = I.EMPLOYEE_NO

        LEFT JOIN Outsum O 
            ON A.EMPLOYEE_NO = O.EMPLOYEE_NO

		

    WHERE ISNULL(A.RETIRE_DATE,'') = ''
      AND ISNULL(A.REAL_USER_GBN,'0') = '1'
	  -- AND CONVERT(VARCHAR(8), F.KT_DATETIME, 112) = @KT_DATE
    ORDER BY A.EMPLOYEE_NO;

	END
END



```

![[image 119.png]]


```sql
USE [iPlusERP_IPACK_DEV]
GO
/****** Object:  StoredProcedure [dbo].[SP_WHR314_01_IUD]    Script Date: 2025-09-24 오후 12:58:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROC [dbo].[SP_WHR314_01_IUD]
(
       @FACTORY_CODE	varchar(6)
     , @EMPLOYEE_NO		varchar(6)
     , @WG_CODE			varchar(8)
     , @CODE_ID2		varchar(6)
	 , @WG_PRDFROM		VARCHAR(4)
	 , @WG_PRDTO		VARCHAR(4)
	 , @DS_CODE			VARCHAR(8)
	 , @DS_TIME			VARCHAR(10)
	 , @KT_DATE			VARCHAR(20)
	 , @OPMAN_CODE		varchar(9)
	 , @IRU				varchar(2)
)
  
AS 
  
BEGIN 

	DECLARE @OPTIME	VARCHAR(12) 
	SET @OPTIME = CONVERT(CHAR(8),GETDATE(),112) + REPLACE(CONVERT(CHAR(5),GETDATE(),114),':','')

	IF @IRU = 'IU'
		BEGIN 

			UPDATE TIN313
			SET 
				WG_ATTEND_GBN	= @WG_CODE
			   ,WG_CODE			= @WG_CODE
			   ,WG_PRDFROM		= REPLACE ( CONVERT (VARCHAR(5), @KT_DATE, 108), ':', '')
			   ,OPMAN_CODE		= @OPMAN_CODE
			   ,OPTIME			= @OPTIME
			WHERE	FACTORY_CODE	=	@FACTORY_CODE
			AND		EMPLOYEE_NO		=	@EMPLOYEE_NO
			AND		DU_YMD			=	CONVERT(VARCHAR(10), @KT_DATE, 112)

			UPDATE TIN514
			SET
				 DS_Code  = @DS_CODE
				,DS_TIME  = @DS_TIME 
			WHERE Factory_Code		= @FACTORY_CODE
			AND	  Du_Sbn			= @EMPLOYEE_NO
			AND	  Du_YMD			= CONVERT(VARCHAR(10), @KT_DATE, 112)


			IF	@@ROWCOUNT = 0 
			BEGIN

				INSERT INTO TIN313
							(
								 FACTORY_CODE
								,EMPLOYEE_NO
								,DU_YMD
								,WG_CODE
								,WG_LTIME
								,OPMAN_CODE
								,OPTIME
							)
						VALUES
							(
								 @FACTORY_CODE
								,@EMPLOYEE_NO
								,CONVERT(VARCHAR(10), @KT_DATE, 112)
								,@WG_CODE
								,'0'
								,@OPMAN_CODE
								,@OPTIME
							)

			END

		END
		ELSE IF @IRU = 'D'
		BEGIN	
			DELETE FROM TIN313
			WHERE	FACTORY_CODE	=		@FACTORY_CODE
			AND EMPLOYEE_NO			=		@EMPLOYEE_NO
			AND DU_YMD				=		CONVERT(VARCHAR(10), @KT_DATE, 112)

			DELETE FROM TIN313D
			WHERE	FACTORY_CODE	=		@FACTORY_CODE
			AND EMPLOYEE_NO			=		@EMPLOYEE_NO
			AND DU_YMD				=		CONVERT(VARCHAR(10), @KT_DATE, 112)

		END
END

```

```java
package com.HR.WHR300;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Iterator;
import java.util.Locale;

import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.json.simple.parser.JSONParser;

@WebServlet("/com/HR/WHR300/jvWHR314_01_IUD")
public class jvWHR314_01_IUD extends HttpServlet {
	private static final long serialVersionUID = 1L;

	@Override
	public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {
		
		Connection conn = null;
		PreparedStatement stmt = null;
		ResultSet rs = null;

		String data;
		
		String strReturn 	=	"";
		String strMsg		=	"";
		String strSuccess	=	"true";

		try {
			ServletContext sc = this.getServletContext();

			Class.forName(sc.getInitParameter("driver")).newInstance();
			conn = DriverManager.getConnection(sc.getInitParameter("url"), // JDBC
																			// URL
					sc.getInitParameter("username"), // DBMS 사용자 아이디
					sc.getInitParameter("password")); // DBMS 사용자 암호

			request.setCharacterEncoding("UTF-8"); // UTF-8 로 인코딩해서 가져온다.
			
			conn.setAutoCommit(false); 
			
			data = (String) request.getParameter("data");
			
			
			if (data != null) {
				JSONArray array = null;
				if (data.substring(0, 1).equals("{")) {
					JSONParser parser = new JSONParser();
					Object object = parser.parse(data);
					JSONObject jsonObject = (JSONObject) object;
					array = new JSONArray();
					array.add(jsonObject);
				} else if (data.substring(0, 1).equals("[")) {
					Object obj = JSONValue.parse(data);
					array = (JSONArray) obj;
				}

				Iterator<JSONObject> iterator = array.iterator();
				
				while (iterator.hasNext()) {

					JSONObject jsonobj = (JSONObject) iterator.next();
					
					
					String EMPLOYEE_NO = (String)jsonobj.get("EMPLOYEE_NO");
					String FACTORY_CODE = (String)jsonobj.get("FACTORY_CODE");
					String KT_DATE = (String)jsonobj.get("KT_DATE");
					String WG_CODE = (String)jsonobj.get("WG_CODE");
					String CODE_ID2 = (String)jsonobj.get("CODE_ID2");
					String OPMAN_CODE = (String)jsonobj.get("OPMAN_CODE");
					String IRU = (String)jsonobj.get("IRU");
					String DS_CODE = (String)jsonobj.get("DS_CODE");
					String DS_TIME = (String)jsonobj.get("DS_TIME");
					System.out.println("EMPLOYEE: "+EMPLOYEE_NO);
					System.out.println("FACTORY_CODE: "+FACTORY_CODE);
					System.out.println("KT_DATE: "+KT_DATE);
					System.out.println("WG_CODE: "+WG_CODE);
					System.out.println("CODE_ID2: "+CODE_ID2);
					System.out.println("OPMAN_CODE: "+OPMAN_CODE);
					System.out.println("IRU: "+IRU);

					String DEPTNM = request.getParameter("DEPTNM");
					String EMPLOYEENM = request.getParameter("EMPLOYEENM");
					String DEF_WG_ATTEND_GBN = request.getParameter("DEF_WG_ATTEND_GBN");
					
					
				        
				        String sql = "EXEC SP_WHR314_01_IUD "
				                + "\r\n" + "'" + FACTORY_CODE + "'"
				                + "\r\n" + ",'" + EMPLOYEE_NO + "'"
				                + "\r\n" + ",'" + KT_DATE + "'"
				                + "\r\n" + ",'" + WG_CODE + "'"
				                + "\r\n" + ",'" + CODE_ID2 + "'"
				                + "\r\n" + ",'" + OPMAN_CODE + "'"
				                + "\r\n" + ",'" + IRU + "'"
				                + "\r\n" + ",'" + DS_CODE + "'"
				                + "\r\n" + ",'" + DS_TIME + "'"
				                ;

				        System.out.println(sql);
					
					stmt = conn.prepareStatement(sql);
					stmt.executeUpdate();
				}
			}
			conn.commit(); 
			
		} catch (Exception e) {
			
			try {
				if(conn != null){
					conn.rollback();
				}
			} 
			catch (Exception exConn) {
			}
			
			
			strSuccess = "false";
			strMsg =  e.toString() ;
			if(strMsg.contains(":") == true){
				String string[] = strMsg.split(":");
				strMsg = string[1];
			}

		} finally {
			try {if(rs != null){rs.close();}} catch (Exception exRs) {}
			try {if(stmt != null){stmt.close();}} catch (Exception exStmt) {}
			try {if(conn != null){conn.close();}} catch (Exception exConn) {}
		}
		
		response.setContentType("text/html; charset=EUC-KR");
		strMsg = strMsg.replace("'", " ");
		strReturn = "{'success':" + strSuccess + ",'data':'','message':'" + strMsg + "'}";
		
		PrintWriter out = response.getWriter();
		out.print(strReturn);
		out.flush();
		out.close();
	}
}



```