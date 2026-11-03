
USE [iPlusERP_SJ]
GO
/****** Object:  StoredProcedure [dbo].[SP_WPR303_EXCEL01_IUD]    Script Date: 2026-10-21 오후 4:47:15 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
/*************************************************************************************
  0. 버전              	: SQL Server 2016
  1. 스토어드명        	: SP_WSA303_01_IUD
  2. 목적& 기능        	: 영업관리>견적관리>수리견적서 등록
  3. 생성일자          	: 2020-01-09
  4. 생성자            	: 김남기
  5. 수정이력 
     1) 수정일자 : 2020-02-03
	    - 수정내역 : 총공급가액, 총합계 저장
		- 수정자 : 김남기			
     2) 수정일자 : 2020-02-12
	    - 수정내역 : SERIAL_SEQNO 추가
		- 수정자 : 김남기			
  6. 인자              	: 
 7. 리턴값            	:  
 8. SP TEST 예제	:
(에) EXEC SP_WSA303_01_IUD

 ******************************************************************************/
ALTER PROC [dbo].[SP_WPR303_EXCEL01_IUD]
 (
       @FACTORY_CODE			VARCHAR(6)		-- 회사코드
     , @PLANT_CODE				VARCHAR(6)		-- 사업장 (정남, 장수)
	 , @YEAR					VARCHAR(4)		-- 년 (2024)
	 , @MONTH					VARCHAR(2)		-- 월 (06)
     , @DAY                     VARCHAR(2)      -- 일 (20)
	 , @WORK_STATUS				VARCHAR(8)		-- 공정구분
	 , @MATERIAL_QUALITY		VARCHAR(10)		-- 재질코드,PR_NO
	 , @THICKNESS			    VARCHAR(20)		-- 두께
	 , @SPEC_X					VARCHAR(50)		-- 폭
	 , @SPEC_Y					VARCHAR(50)		-- 길이

	 , @MATERIAL_CODE			VARCHAR(20)		-- 품목 채번한거 들어감
	 , @MATERIAL_SPEC			VARCHAR(50)		-- 재질명-두께*폭*길이+공정구분 (예시, SS400-20*30*1250L)
	 , @MATERIAL_NAME			VARCHAR(255)	-- 대분류 + ' ' + 소분류명
	 , @ITEM_KIND1				VARCHAR(20)		-- 엑셀파일에 대분류
	 , @ITEM_KIND2				VARCHAR(10)		-- 엑셀파일에 중분류
	 , @ITEM_KIND3				VARCHAR(20)		-- 엑셀파일에 소분류
	 , @PART_NO					VARCHAR(20)		-- 엑셀파일에 품목코드 (예시, 11-20*30*1250L) --ETC 중간두자리
	 , @ITEM_GBN				VARCHAR(30)		-- A
	 , @OLD_MAT_CODE			VARCHAR(30)		-- PART_NO와 동일
	 , @ITEM_MODEL_NAME			VARCHAR(30)		-- ITEM_MODEL_NAME
	 , @PRODPLAN_NO				VARCHAR(30)		-- PRODPLAN_NO
	 , @ITEM_CODE				VARCHAR(30)		-- ITEM_CODE
	 , @WAREHOUSE_CODE			VARCHAR(30)		-- WAREHOUSE_CODE
	 , @HIST_SEQ				VARCHAR(30)		-- HIST_SEQ
	 , @SALE_PLAN_QTY			int				-- SALE_PLAN_QTY
	 , @NM_ITEMGRP				VARCHAR(30)		-- 품목군명
	 , @OPMAN_CODE    			VARCHAR(30)		-- 로그인 사용자
     , @ORDER_NO                VARCHAR(30)     -- ORDER_NO
	 , @IUD						VARCHAR(2)		-- IUD
 )
  
 AS 

 SET NOCOUNT ON

 BEGIN 
	DECLARE @OPTIME	VARCHAR(14) 
	SET @OPTIME = CONVERT(CHAR(8),GETDATE(),112) + REPLACE(CONVERT(CHAR(5),GETDATE(),114),':','')

	IF @PRODPLAN_NO = ''
		BEGIN
			SELECT @PRODPLAN_NO = @YEAR + @MONTH + FORMAT(ISNULL(MAX(CAST(SUBSTRING(PRODPLAN_NO, 7, 6) AS INT)), 0) + 1, 'D6')
			FROM TPR201 A
			WHERE A.FACTORY_CODE = @FACTORY_CODE
			AND A.PLANT_CODE = @PLANT_CODE
			AND A.IYEAR = @YEAR
			AND A.IMONTH = @MONTH
		END

	IF @MATERIAL_QUALITY = ''
		BEGIN
			SELECT @MATERIAL_QUALITY = CODE_ID2
			FROM TCO101    WITH(NOLOCK)         
			WHERE CODE_ID1 = '424'
			AND CODE_NAME_FULL = @NM_ITEMGRP
		END

	SELECT @WAREHOUSE_CODE = WAREHOUSE_CODE
	FROM TCO102     WITH(NOLOCK)
	WHERE PLANT_CODE = @PLANT_CODE
	AND ETC = @WAREHOUSE_CODE

	SELECT  @ITEM_CODE = MATERIAL_CODE
	FROM TCO403     WITH(NOLOCK)
	WHERE OLD_MAT_CODE = RTRIM(LTRIM(@PART_NO))
    AND DELETE_FLAG = '0'

	DECLARE @ETC	VARCHAR(30) 
	SELECT @ETC = @NM_ITEMGRP + '-' + @THICKNESS + '*' + @SPEC_X + '*' + @SPEC_Y +@WORK_STATUS
	FROM TCO101    WITH(NOLOCK)         
	WHERE CODE_ID1 = '424'
	AND CODE_NAME_FULL = @NM_ITEMGRP
		
	IF ISNULL(@ITEM_CODE,'') = ''

	BEGIN
		SELECT @ITEM_CODE = RIGHT('0000000000' + CAST(ISNULL(MAX(CAST(A.MATERIAL_CODE AS INT)), 0) + 1  AS VARCHAR(20)) , 10)	 
		FROM TCO403 A 
		WHERE A.FACTORY_CODE = @FACTORY_CODE
	
        BEGIN
			INSERT INTO TCO403		with(rowlock)																												    
			(																																		    
				FACTORY_CODE				,PLANT_CODE				,MATERIAL_CODE				,MATERIAL_SPEC				,PART_NO				    
				,MATERIAL_QUALITY			,THICKNESS				,SPEC_X						,SPEC_Y						,WORK_STATUS			    
				,OPMAN_CODE					,OPTIME					,OPMAN_CODE2				,OPTIME2											    
				,MATERIAL_NAME				,SYSTEM_FLAG			,ITEM_KIND1					,ITEM_KIND2					,ITEM_KIND3				    
				,ITEM_ENG_NAME				,ITEM_MODEL_NAME		,UNIT						,UNIT_WEIGHT				,PACKING_WEIGHT			    
				,PACKING_EA					,PALET_BOX_EA			,LEAD_TIME					,STANDARD_PRICE				,FOREIGN_PRICE			    
				,ORDERING_UNIT				,MATERIAL_FLAG			,AVERAGE_LIFETIME			,LIFETIME_UNIT				,CUSTOMER_CODE			    
				,SAFE_INVOICE				,CHARGE_CODE			,ACCOUNTING_CODE			,AUTO_IO_FLAG				,WAREHOUSE_CODE			    
				,DRAWING					,SIL_COUNT				,ALTERNATE					,ITEM_GROUP					,REORDER				    
				,LOTSIZE					,MIN_ORDER_QUANTITY		,ORDER_METHOD				,ETC						,INSPECTFLAG			    
				,FLOWINOUT					,UNIT_STORE				,UNIT_SALE					,LOT_FLAG					,UNIT_PURCHASE			    
				,UNIT_PACKING				,CONVERSION_FACTOR		,WORKORDER_CODE				,SUBUL_USE_FLAG				,CURRENCY_CODE			    
				,STD_START_REG_DATE			,STD_END_REG_DATE		,STD_START_REGMAN_CODE		,STD_END_REGMAN_CODE		,INSPECT_TYPE_CODE		    
				,INSPECT_FLAG2				,REPRESENT_FLAG			,REPRESENT_CODE				,ROHS_FLAG					,MAT_ADD_FLAG			    
				,SAFE_INVOICE_CALL_FLAG		,LEVEL_NAME				,MAT_STATUS_CODE			,INTER_LOCK_FLAG			,STORE_METHOD			    
				,QUANTIFY_METHOD			,EXPIRY_DAY_CNT			,EXPIRY_MONTH_CNT			,MANUFACTORY				,PROD_DEPT				    
				,STOCK_USE_FLAG				,NOT_PUR_FLAG			,DELETE_DATE				,DELETE_FLAG				,ITEM_BARCODE			    
				,WORK_TYPE_CODE				,MAT_CATA_GBN			,LOCATION					,MATERIAL_SPEC2				,CUST_PART_NO			    
				,CUST_LAUNCH_DATE			,ST_BOM_MANAGER			,TRACE_MNG_FLAG				,NOT_PUR_PLAN_DATE			,NOT_PUR_CHARGER		    
				,SERVICE_MATERIAL_FLAG		,NOT_PUR_DATE			,FIRST_ARTICLE				,FIRST_ARTICLE_SET_DATE		,FIRST_ARTICLE_OUT_DATE	    
				,NOT_PUR_BIGO				,ITEM_PROD_DVLP_GBN		,BAR_CODE_FLAG				,KFDA_REPORT_NO				,ITEM_GBN				    
				,QC_KIND1					,QC_KIND2				,DATA_AUDITER				,DATA_AUDIT_TIME			,DATA_AUDIT_FLAG		    
				,DATA_AUDIT_BIGO			,CONVERSION_FACTOR_OI	,CONVERSION_FACTOR_PK		,UNIT_PALLETE				,UNIT_KG				    
				,MAKER_CUST					,SUPPLIER_CUST			,DEFROST_TIME				,FREEZING_TIME				,DB_MATERIAL_CODE		    
				,BOXING_MACHINE				,CAP					,HOTFILL_FLAG				,RETORT_FLAG				,DIRECT_PIPING_FLAG		    
				,MASH_NET					,BOXING_TYPE			,PACKING_PAPER_KIND			,CONTAINER					,QCCM_KIND_CD			    
				,MAKEDATE_DISP_FLAG			,AVG_PROD_RATIO			,CUST_MAKEDATE_DISP_FLAG	,KFDA_REPORT_MNG_NO			,COUNTRYOFORIN_CODE		    
				,SEARCH_ITEM_NAME			,ITEM_GROUP_FLAG		,ITEM_GROUP_CODE			,MATERIAL_NAME_TEMP			,WEIGHT_ERROR_PLUS		    
				,WEIGHT_ERROR_MINUS			,LIMIT_MIX_QTY			,ADD_FLAG					,OLD_MAT_CODE										    
			)																																		    
			VALUES																																		
			(																																		    
				@FACTORY_CODE				,@PLANT_CODE			,@ITEM_CODE				    ,@ETC						,@PART_NO				    
				,@MATERIAL_QUALITY			,@THICKNESS				,@SPEC_X					,@SPEC_Y					,@WORK_STATUS		        
				,@OPMAN_CODE				,@OPTIME				,''							,''													    
				,@MATERIAL_NAME             ,'0'		            ,@ITEM_KIND1	            ,@ITEM_KIND2	            ,@ITEM_KIND3                 
				,''			                ,@NM_ITEMGRP			,'001'			    	    ,0				            ,0		                    
				,0				            ,0			            ,0				            ,0			                ,0		                    
				,''			                ,'1120402'	            ,0			                ,''			                ,''		                    
				,0				            ,''			            ,''			                ,''				            ,''		                    
				,''					        ,''			            ,''				            ,''				            ,0				            
				,0					        ,0	                    ,''				            ,''						    ,'0'		                
				,'1'				            ,''			            ,''				            ,'1'					    ,''		                    
				,''				            ,0	                    ,''			                ,'0'			                ,''		                    
				,''		                    ,''		                ,''	                        ,''		                    ,''	                        
				,''			                ,''		                ,''			                ,'0'				        ,''			                
				,'0'	                    ,''			            ,''			                ,''			                ,''			                
				,''			                ,0		                ,0			                ,''				            ,''			                
				,'0'			            ,'0'		            ,''				            ,'0'				        ,''			                
				,0			                ,'A'                    ,''					        ,''			                ,''			                
				,''			                ,''		                ,'0'			            ,'0'		                ,'0'            		    
				,''                         ,'0'			        ,''			                ,''	                        ,''	                        
				,''				            ,''	                    ,''			                ,''			                ,@ITEM_GBN		            
				,'0'					    ,'0'				    ,''				            ,''			                ,''		                    
				,''			                ,0	                    ,0		                    ,''				            ,''				            
				,''				            ,''		                ,0				            ,0			                ,''		                    
				,''			                ,''					    ,''				            ,''				            ,''		                    
				,''					        ,''			            ,''		                    ,''				            ,'0'		                
				,''		                    ,0		                ,''	                        ,''		                    ,''		                    
				,''			                ,''		                ,''			                ,''		                    ,0		                    
				,0		                    ,0						,'1'						,@OLD_MAT_CODE						                    
			)						
		END	 
    END
    
    -- TPR202 COL_SEQ 순번 채번
    DECLARE @COL_SEQ	VARCHAR(5) 
    SELECT @COL_SEQ = ISNULL(MAX(A.COL_SEQ), 0) + 1
    FROM TPR202 AS A
    WHERE A.FACTORY_CODE = @FACTORY_CODE
    AND A.PRODPLAN_NO = @PRODPLAN_NO

    ---- TSA307 ORDER_NO 채번
    --DECLARE @ORDER_NO	VARCHAR(20) 
    ----SELECT @ORDER_NO = CONVERT(VARCHAR(10),GETDATE(),112) + FORMAT(ISNULL(MAX(CAST(SUBSTRING(A.ORDER_NO, 9, 4) AS INT)), 0) + 1, 'D4')
    --SELECT @ORDER_NO = @YEAR + @MONTH + @DAY + FORMAT(ISNULL(MAX(CAST(SUBSTRING(A.ORDER_NO, 9, 4) AS INT)), 0) + 1, 'D4')
    --FROM TSA307 AS A
    --WHERE A.FACTORY_CODE = @FACTORY_CODE
    ----AND SUBSTRING(A.ORDER_NO, 1, 8) = CONVERT(VARCHAR(10),GETDATE(),112)
    --AND SUBSTRING(A.ORDER_NO, 1, 8) = @YEAR + @MONTH + @DAY

   -- TSA308 ORDER_SEQNO 채번
    DECLARE @ORDER_SEQNO	VARCHAR(5) 
    SELECT @ORDER_SEQNO = ISNULL(MAX(A.ORDER_SEQNO), 0) + 1
    FROM TSA308 AS A
    WHERE A.FACTORY_CODE = @FACTORY_CODE   
    AND A.ORDER_NO = @ORDER_NO
    AND A.ORDER_HISTNO = '1'       -- 1 고정
   
   -- TPR301 PRODPLAN_DATE, PRODPLAN_SEQ 채번
    DECLARE @PRODPLAN_DATE	VARCHAR(20) 
    DECLARE @PRODPLAN_SEQ	VARCHAR(5) 
    --SELECT @PRODPLAN_DATE = CONVERT(VARCHAR(10),GETDATE(),112) 
    SELECT @PRODPLAN_DATE = @YEAR + @MONTH + @DAY
    , @PRODPLAN_SEQ = ISNULL(MAX(A.PRODPLAN_SEQ), 0) + 1 
    FROM TPR301 AS A
    WHERE A.FACTORY_CODE = @FACTORY_CODE   
    --AND A.PRODPLAN_DATE = CONVERT(VARCHAR(10),GETDATE(),112)
    AND A.PRODPLAN_DATE = @YEAR + @MONTH + @DAY
   
   DECLARE @DELIVERY_DATE	VARCHAR(20) 
   DECLARE @DELIVERY_DATE2	VARCHAR(20) 

   --SELECT @DELIVERY_DATE = FORMAT(EOMONTH(GETDATE()), 'yyyyMMdd')
   --SELECT @DELIVERY_DATE2 = FORMAT(EOMONTH(GETDATE()), 'yyyyMMdd')

   SELECT @DELIVERY_DATE = @YEAR + @MONTH + @DAY
   SELECT @DELIVERY_DATE2 = @YEAR + @MONTH + @DAY

    BEGIN

        IF @IUD = 'IU'
        BEGIN
            UPDATE TPR201 with(updlock,rowlock) SET
                WAREHOUSE_CODE = @WAREHOUSE_CODE,
                HIST_SEQ = @HIST_SEQ,
                SALE_PLAN_QTY = @SALE_PLAN_QTY,
                OPMAN_CODE2 = @OPMAN_CODE,
                OPTIME2 = @OPTIME
            WHERE FACTORY_CODE = @FACTORY_CODE
            AND PLANT_CODE = @PLANT_CODE
            AND PRODPLAN_NO = @PRODPLAN_NO
            AND IYEAR = @YEAR
            AND IMONTH = @MONTH

            IF @@ROWCOUNT = 0 
            BEGIN
                INSERT INTO TPR201		with(rowlock)	
                (
                    FACTORY_CODE, PLANT_CODE, PRODPLAN_NO, ITEM_CODE, WAREHOUSE_CODE,
                    IYEAR, IMONTH, HIST_SEQ, SALE_PLAN_QTY, SALE_PLAN_1_QTY,
                    SALE_PLAN_2_QTY, START_STOCK_QTY, IN_PROD_PLAN_QTY, OUT_PROD_PLAN_QTY, END_STOCK_QTY,
                    BIGO, OPMAN_CODE, OPTIME, OPMAN_CODE2, OPTIME2, PLAN_DATE, PLAN_EMP
                )
                VALUES
                (
                    @FACTORY_CODE, @PLANT_CODE, @PRODPLAN_NO, @ITEM_CODE, @WAREHOUSE_CODE,
                    @YEAR, @MONTH, @HIST_SEQ, @SALE_PLAN_QTY, 0,
                    0, 0, 0, 0, 0,
                    '', @OPMAN_CODE, @OPTIME, '', '', @YEAR+@MONTH+@DAY, @OPMAN_CODE
                )
           
            -- TPR202 INSERT
                INSERT INTO TPR202 		with(rowlock)	                                               
                (
                    FACTORY_CODE      ,PLANT_CODE      ,PRODPLAN_NO        ,COL_SEQ            ,GBN_CODE
                   ,CUSTOMER_CODE     ,REQUEST_QTY     ,DELIVERY_DATE1     ,DELIVERY_DATE2     ,ORDER_NO
                    ,ORDER_HISTNO      ,ORDER_SEQNO
                    ,OPMAN_CODE        ,OPTIME          ,OPMAN_CODE2        ,OPTIME2
                )
                VALUES
                (
                    @FACTORY_CODE      ,@PLANT_CODE       ,@PRODPLAN_NO      ,@COL_SEQ         ,'1'
                   ,'000001'           ,@SALE_PLAN_QTY    ,''                ,''               ,@ORDER_NO
                    ,'1'               ,@ORDER_SEQNO
                    ,@OPMAN_CODE       ,@OPTIME           ,''                ,''
                )
            
                ---- TSA307 INSERT
                --INSERT INTO TSA307                                                                        
                --(                                                                                    
                --    FACTORY_CODE         ,PLANT_CODE               ,ORDER_NO            ,ORDER_HISTNO      ,REG_DATE   
                --   ,ORDER_DATE            ,ORDER_GBN               ,CUSTOMER_CODE         ,VAT_FLAG         ,VAT_TYPE   
                --   ,VAT_INC_FLAG         ,DELIVERY_CUSTOMER_CODE      ,SALES_CUSTOMER_CODE   ,CURRENCY_CODE      ,ORDER_STATUS
                --   ,APPROVE_FLAG         ,CLOSE_FLAG               ,PROD_REQ_FLAG         ,LAST_FLAG         ,CANCEL_FLAG
                --   ,ORDER_GUBUN1         ,ORDER_GUBUN2            ,ORDER_GUBUN3                                 
                --   ,OPMAN_CODE            ,OPTIME                  ,OPMAN_CODE2         ,OPTIME2         ,DELETE_FLAG
                --)                                                                                    
                --VALUES                                                                                 
                --(                                                                                    
                --    @FACTORY_CODE         ,@PLANT_CODE            ,@ORDER_NO            ,'1'                ,LEFT(@OPTIME, 8) 
                --   ,LEFT(@OPTIME, 8)      ,'3'                    ,'000001'             ,'1'                ,'0'         
                --   ,'0'                   ,'000001'               ,'000001'             ,'000001'           ,'0'          
                --   ,'0'                   ,'0'                    ,'0'                  ,'0'                ,'0'          
                --   ,'001'                 ,'001'                    ,'001'
                --   ,@OPMAN_CODE           ,@OPTIME               ,''                     ,''                 ,'0'
                --)
            
            -- TSA308 INSERT
                INSERT INTO TSA308   		with(rowlock)	                                                        
                (                                                                              
                    FACTORY_CODE         ,PLANT_CODE         ,ORDER_NO         ,ORDER_HISTNO      ,ORDER_SEQNO   
                   ,ITEM_CODE            ,DELIVERY_DATE      ,PROD_REQ_DATE      ,ORDER_UNIT         ,ORDER_UNIT_QTY   
                   ,ORDER_UPRICE_UNIT      ,ORDER_UPRICE_QTY   ,VAT_GBN         ,VAT_FLAG         ,DELIVERY_CUSTOMER
                   ,SALES_CUSTOMER_CODE   ,CLOSING_FLAG      ,STOCK_USE_FLAG      ,ISSUE_FLAG         ,ADD_ORDER_FLAG   
                   ,DELIVERY_DATE2           ,CURRENCY_CODE      ,CURRENCY_RATE      ,ORDER_QTY           ,DELETE_FLAG          
                   ,OPMAN_CODE             ,OPTIME            ,OPMAN_CODE2       ,OPTIME2           ,WORK_QTY             
                )                                                                              
                VALUES                                                                           
                (                                                                              
                    @FACTORY_CODE         ,@PLANT_CODE      ,@ORDER_NO          ,'1'                 ,@ORDER_SEQNO   
                   ,@ITEM_CODE            ,@DELIVERY_DATE   ,LEFT(@OPTIME, 8)   ,'001'               ,@SALE_PLAN_QTY
                   ,'003'                 ,@SALE_PLAN_QTY   ,'0'                ,'1'                 ,'000001'            
                   ,'000001'              ,'0'              ,'0'                ,'0'                 ,'0'                
                   ,@DELIVERY_DATE2       ,'000001'         ,'1'                ,@SALE_PLAN_QTY      ,'0'                    
                   ,@OPMAN_CODE           ,@OPTIME          ,''                  ,''                 ,@SALE_PLAN_QTY
                )
           
            -- TPR301 INSERT
                INSERT INTO TPR301    		with(rowlock)	                                                  
                (                                                                           
                    FACTORY_CODE         ,PLANT_CODE         ,WORKCENTER_CODE   ,PRODPLAN_DATE      ,PRODPLAN_SEQ
                   ,PRODPLAN_NO         ,COL_SEQ         ,WORK_CODE         ,PROD_DATE         ,PROD_QTY   
                   ,EQUIP_SYS_CD         ,ITEM_CODE         ,VIEW_SEQ         ,WORK_CNT         ,PROD_DESC   
                   ,MAT_OUT_DATE         ,MAT_OUT_DESC      ,OUTORDER_FLAG      ,OUTORDER_CUST      ,FINISH_DATE
                   ,MAT_OUT_REAL_DATE      ,FINISH_FLAG      ,WORK_SEQ         ,LAST_WORK_FLAG               
                   ,OPMAN_CODE            ,OPTIME            ,OPMAN_CODE2      ,OPTIME2                  
                )                                                                           
                VALUES                                                                        
                (                                                                           
                    @FACTORY_CODE         ,@PLANT_CODE      ,''   ,@PRODPLAN_DATE      ,@PRODPLAN_SEQ
                   ,@PRODPLAN_NO         ,@COL_SEQ         ,''         ,''                 ,@SALE_PLAN_QTY   
                   ,'0000'                 ,@ITEM_CODE         ,1                 ,1                 ,''             
                   ,''                     ,''                  ,'0'              ,''                  ,''              
                   ,''                      ,'0'              ,0                 ,'0'                          
                   ,@OPMAN_CODE         ,@OPTIME         ,''                  ,''                            
                )
            
                -- TPR301R INSERT
                INSERT INTO TPR301R     		with(rowlock)	                  
                (                                                
                    FACTORY_CODE   ,PLANT_CODE      ,PRODPLAN_DATE   ,PRODPLAN_SEQ
                   ,ORDER_NO      ,ORDER_HISTNO   ,ORDER_SEQNO            
                   ,ORDER_QTY      ,WORK_QTY      ,PROD_QTY               
                   ,OPMAN_CODE      ,OPTIME         ,OPMAN_CODE2   ,OPTIME2   
                )                                                
                VALUES                                             
                (                                                
                    @FACTORY_CODE   ,@PLANT_CODE   ,@PRODPLAN_DATE   ,@PRODPLAN_SEQ
                   ,@ORDER_NO      ,'1'   ,@ORDER_SEQNO            
                   ,@SALE_PLAN_QTY      ,@SALE_PLAN_QTY      ,@SALE_PLAN_QTY               
                   ,@OPMAN_CODE   ,@OPTIME      ,''               ,''               
                ) 
            END
        END 
    END
 END 



![[Pasted image 20261023170849.png|664]]