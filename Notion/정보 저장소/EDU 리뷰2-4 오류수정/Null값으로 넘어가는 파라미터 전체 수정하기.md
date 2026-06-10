---

---

---

## 문제 확인

```sql
ALTER PROCEDURE [dbo].[SP_HHR101_IUD]
    @FACTORY_CODE       VARCHAR(6),
    @WORK_CODE          VARCHAR(6),
    @WORK_NAME          VARCHAR(20),
    @PROD_LIMIT_QTY     FLOAT,
    @LINE_COUNT         VARCHAR(10),
    @OPMAN_CODE         VARCHAR(4),
    @VIEW_SEQ           INT,
    @OUTORDER_FLAG      VARCHAR(2),
    --@FORCE_CNG        VARCHAR(2),
    @IUD                VARCHAR(4)
```

- 프로시저 내 저장된 파일 형태

해당 증상은 IUD 동작 시 LINE_COUNT의 신규 등록 파라미터 값을 NULL값으로 넘긴 후 프로시저에서 INT

형태로 가공하려는 형태를 가지고 있어  발생되었습니다.

---

## 코드 재수정

```javascript
store.add({                                                                                     // 신규 레코드 추가
      FACTORY_CODE:   gFactoryCode,
      WORK_CODE:      '',
      WORK_NAME:      '',
      PROD_LIMIT_QTY: '',
      OUTORDER_FLAG:  '',
      OPMAN_CODE:     gUserId,
      //FORCE_CNG: '0',
      DELETE_FLAG: '',
      LINE_COUNT: 0,
      VIEW_SEQ: '',
      OPTIME: '',
    });
```

- Controller 내부 수정

OnNew함수 내부에 store.add 부분을 수정했습니다 LINE_COUNT를 default 0 값으로 넘겨 공정 그리드 내 

정상적으로 저장 가능 합니다.

---