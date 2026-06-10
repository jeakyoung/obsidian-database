---

---
---

## 요청사항에 따른 기능을 만들기위해 생성한 IUD입니다.

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

@WebServlet("/com/HR/WHR300/jvWHR316_IUD")
public class jvWHR316_IUD extends HttpServlet {
	private static final long serialVersionUID = 1L;

	@Override
	public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {
		
		Connection conn = null;
		PreparedStatement stmt = null;
		ResultSet rs = null;

		String query = "";
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

					query = "EXEC SP_WHR316_01_IUD " 

							+ "\r\n" + "'"  + (String)jsonobj.get("FACTORY_CODE") + "'"
							+ "\r\n" + ",'" + (String)jsonobj.get("EMPLOYEE_NO")  + "'"
							+ "\r\n" + ",'" + (String)jsonobj.get("WG_CODE") 	  + "'"
							+ "\r\n" + ",'" + (String)jsonobj.get("OPMAN_CODE")   + "'";
							
					System.out.println(query);
					
					stmt = conn.prepareStatement(query);
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

→ WHR316_IUD.JAVA

```sql
USE [iPlusERP_IPACK_DEV]
GO
/****** Object:  StoredProcedure [dbo].[SP_WHR316_01_IUD]    Script Date: 2025-09-09 오전 10:42:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


ALTER PROC	[dbo].[SP_WHR316_01_IUD]
(
		@FACTORY_CODE	VARCHAR(6)
	,	@EMPLOYEE_NO	VARCHAR(30)
	,	@WG_CODE		VARCHAR(6)
	,	@OPMAN_CODE		VARCHAR(10)


)
AS
BEGIN

	UPDATE TIN312 
	SET 
			WG_CODE			=	@WG_CODE
		,	OPMAN_CODE		=	@OPMAN_CODE
		,	OPTIME			=	CONVERT(VARCHAR(8), GETDATE(), 112) + left(REPLACE(CONVERT(VARCHAR(8), GETDATE(), 108), ':', ''),4)
	WHERE	FACTORY_CODE	=	@FACTORY_CODE
	AND		EMPLOYEE_NO		=	@EMPLOYEE_NO

	IF	@@ROWCOUNT = 0 
		BEGIN

			INSERT INTO TIN312
			( 
				FACTORY_CODE 
				, EMPLOYEE_NO 
				, WG_CODE
				, WG_BIGO
				, OPMAN_CODE
				, OPTIME
			) 
			VALUES 
			( 
				@FACTORY_CODE
				,	@EMPLOYEE_NO
				,	@WG_CODE
				,	''
				,	@OPMAN_CODE
				,	CONVERT(VARCHAR(8), GETDATE(), 112) + left(REPLACE(CONVERT(VARCHAR(8), GETDATE(), 108), ':', ''),4)
			) 
		END



END





```

→ WHR316_01_IUD.SQL