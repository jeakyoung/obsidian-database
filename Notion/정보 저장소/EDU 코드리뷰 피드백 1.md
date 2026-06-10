---
base: "[[정보 저장소.base]]"
우선순위: 보통
종료일: 2025-08-19
상태: 완료
담당자:
  - 안재경
팀: []
---
풀리지 않는 의문 : 1841포트와 8080포트의 차이점?

---

1. each문과 for문의 차이점 정리하기 (for문을 더 많이쓴다.) 그 이유는?

for문은 인덱스를 정해 반복 횟수나 조건을 명시적으로 제어 할수 있지만

each문은 인덱스를 자동처리하여 리스트를 순회하기에 좋습니다.

처리속도는 for문이나 each문이나 큰 차이가 없으나 일반적으로 특정컬렉션을 순회하는 역활이면 each문이 

가독성이 좋으나 원하는 횟수만큼 반복제어하며 인덱스까지 활용하기 위해서는 for문이 좋다고 합니다.

---

2. OnReg 동작시 현위치를 기억하는 기능을 놓쳤음. → 해당 로직 추가하기. 

```javascript
getSelectionState: function (grid, keyField) {
    if (!grid) return null;
    var sel = grid.getSelectionModel().getSelection()[0] || null;
    var store = grid.getStore();
    if (!sel) return null;
    return {
      key: (sel.get(keyField) || '').toString().trim(),
      index: store.indexOf(sel)
    };
  },

  setSelectionState: function (grid, keyField, state) {
    if (!grid || !state) return;
    var store = grid.getStore();
    var rec = null;

    if (state.key) {
      var idxByKey = store.findExact(keyField, state.key);
      if (idxByKey !== -1) rec = store.getAt(idxByKey);
    }
    if (!rec && state.index >= 0 && state.index < store.getCount()) {
      rec = store.getAt(state.index);
    }

    if (rec) {
      var sm = grid.getSelectionModel();
      sm.select(rec, false, true);
      var rowIdx = store.indexOf(rec);
      if (rowIdx >= 0) {
        grid.getView().focusRow(rowIdx);
        grid.getView().ensureVisible(rowIdx);
      }
    }
  },
```

```javascript
 if (!valid) return;

    for (var k = 0; k < store.getCount(); k++) {
      var rec2 = store.getAt(k);
      if (!rec2.get('WORK_NAME')) continue;

      if (rec2.dirty) {
        rec2.set('FACTORY_CODE', gFactoryCode);
        rec2.set('IUD', 'IU');
      }
    }

    // 저장 직전 선택 상태 기억
    var selState = me.getSelectionState(grid, 'WORK_CODE');

    store.sync({
      success: function () {
        Ext.Msg.alert('정보', '저장되었습니다.');
        store.reload({
          callback: function () {
            // 저장 전 선택 상태 복구
            me.setSelectionState(grid, 'WORK_CODE', selState);
          }
        });
      }
    });
```

---

3. 중복검사 로직에서 TRIM을 이용 공백을 삭제하고 검사를 진행했음에도 공백시 정상등록이 됨 (버그픽스하기)

```javascript
init: function () {
    var me = this;
    me.control({
      '#grid_01': {
        select: 'onSelect',
        viewready: 'onMasterViewReady'
      },
      '#grid_02': {
        viewready: 'onDetailViewReady'
      }
    });
    me.isPendingSave = false;
  },

  normKey: function (v) {
  var s = (v || '').toString();
  return s.replace(/\s+/g, '').toUpperCase();              // 모든 공백 제거 + 대소문자 무시
},
```

```javascript
var key  = fac + '||' + me.normKey(name);
    var prev = seen[key];

    if (!prev) {
      seen[key] = { idx: i, code: code };
      continue;
    }

    var sameCode = (prev.code === code);
    var bothNew  = (!prev.code && !code && prev.idx !== i);

    if (!sameCode || bothNew) {
      Ext.Msg.alert('정보', '중복 공정명입니다: ' + name);
      valid = false;
      break;
    }
  }

  if (!valid) return;

  for (var k = 0; k < store.getCount(); k++) {
    var rec2 = store.getAt(k);
    if (!rec2.get('WORK_NAME')) continue;

    if (rec2.dirty) {
      rec2.set('FACTORY_CODE', gFactoryCode);
      rec2.set('IUD', 'IU');
    }
  }
```

→ trim 자체 문제인가 싶어 trim동작을 함수로 뺴서 검사 모듈을 분리해봤습니다. 하지만 해당 수정안때문에 정상동작하는것은 아닌듯합니다. [localhost:8080](http://localhost:8080/) 포트를 EXCEL 업로드 허용 포트 제한 때문에 이용하고 동일한 포트로 해당 기능을 테스트했으나 IUD가 백단에 NULL로 전해지는 증상이 똑같이 지속적으로 발생해 [localhost:1841](http://localhost:1841/) 포트로 접근 후 테스트를 진행하자 정상동작함을 확인했습니다.

해당 포트 내에서는 호기 그리드 내 IU 동작도 정상동작합니다.

---

4. 호기 그리드 저장동작시 valId를 활용하여 조건 유효성 검사를 진행했는데 무슨 이유인지 호기 그리드 저장 로직에서 빠져있음 추가하기.

```javascript
if (!wcode) {
      Ext.Msg.alert('정보', '상위 공정코드가 없습니다. 먼저 공정을 선택하세요.');
      valid = false;
      break;    //return = false를 break로 수정했습니다.
    }
    if (!lname) {
      Ext.Msg.alert('정보', '호기명은 필수입니다.');
      valid = false;
      break;
    }

    var key  = fac + '||' + me.normKey(lname);
    var prev = seen[key];

    if (!prev) {
      seen[key] = { idx: i, code: lcode };
      continue;
    }

    var sameCode = (prev.code === lcode);
    var bothNew  = (!prev.code && !lcode && prev.idx !== i);

    if (!sameCode || bothNew) {
      Ext.Msg.alert('정보', '중복 호기명입니다: ' + lname);
      valid = false;
      break;
    }
  }

  if (!valid) return;
```

→ OnRegDetail내 valid로 조건유효 검사를 진행하여 조건을 만족하지 않는 경우에만 데이터를 넘길수 있도록 추가했습니다.

---

5. 프로시저단에서 view_seq와 같은 레이블을 시퀀스로 늘리는것은 일관성 유지에 좋지않음 → 인덱스의 max값을 따서 1을 더하는식으로

```sql
 IF @@ROWCOUNT = 0
BEGIN
IF @WORK_CODE = ''
BEGIN
SELECT @WORK_CODE = RIGHT('000000' + CAST(CAST(ISNULL(MAX(WORK_CODE),'0') AS INT) + 1 AS VARCHAR(6)),6)
FROM   HHR101
WHERE  FACTORY_CODE = @FACTORY_CODE
END

 INSERT INTO HHR101 (
     FACTORY_CODE,
     WORK_CODE,
     WORK_NAME,
     VIEW_SEQ
 ) VALUES (
     @FACTORY_CODE,
     @WORK_CODE,
     @WORK_NAME,
     NEXT VALUE FOR seq_view_seq
 );
END
```

```sql
IF @@ROWCOUNT = 0
 BEGIN
    IF @LINE_CODE = ''
        BEGIN
            SELECT @LINE_CODE = RIGHT('000' + CAST(CAST(ISNULL(MAX(LINE_CODE),'0') AS INT) + 1 AS VARCHAR(3)),3)
            FROM   HHR102
            WHERE  WORK_CODE = @WORK_CODE
        END

    INSERT INTO HHR102 (
        FACTORY_CODE,
        WORK_CODE,
        LINE_CODE,
        LINE_NAME,
        VIEW_SEQ,
        DELETE_FLAG
    ) VALUES (
        @FACTORY_CODE,
        @WORK_CODE,
        @LINE_CODE,
        @LINE_NAME,
        NEXT VALUE FOR seq_view_seq,
        @DELETE_FLAG
    );
END
END
```

위와 같은 방법으로 최댓값에 1을 더하는 방법에 기본 양식을 000000이나 000으로 지정하여 오른쪽부터 값을 채우는 방식을 사용하여 Sequence 사용 없이 Auto Increment와 같은 동작을 구현 할 수 있습니다.

---

6. drag&drop 진행 시 잡아다가 던지는 과정에 모든 데이터를 다 훓고 가는 과정이 있어 그리드 라인이 많아질수록 백단에서 너무 많은 트래픽이 발생함. 다른방식 찾아보기 → 같은방식으로 진행 가능하고 프로시저단에서 처리도 가능함

```javascript
getRange: function (view, data, overModel, dropPos) {
    var vStore = (view.store || view.getStore());
    if (!vStore) return null;

    // 드래그된 레코드들의 인덱스수집
    var draggedIdx = [];
    Ext.Array.each(data.records || [], function (r) {
      if (r.get('DELETE') === true) return;
      var i = vStore.indexOf(r);
      if (i >= 0) draggedIdx.push(i);
    });
    if (!draggedIdx.length) return null;

    var minD = Math.min.apply(Math, draggedIdx);
    var maxD = Math.max.apply(Math, draggedIdx);

    // 떨어뜨릴 목표 인덱스
    var toIdx;
    if (!overModel) {
      toIdx = vStore.getCount() - 1;
    } else {
      var over = vStore.indexOf(overModel);
      toIdx = (dropPos === 'after') ? over + 1 : over;
      toIdx = Ext.Number.constrain(toIdx, 0, vStore.getCount() - 1);
    }

    // 같은 블록을 제자리로 떨군 경우 → 변화 없음
    var sameBlock = (toIdx >= minD && toIdx <= maxD) &&
                    (draggedIdx.length === (maxD - minD + 1));
    if (sameBlock) return null;

    var start = Math.min(minD, toIdx);
    var end   = Math.max(maxD, toIdx + draggedIdx.length - 1);

    return {
      start: Ext.Number.constrain(start, 0, vStore.getCount() - 1),
      end  : Ext.Number.constrain(end  , 0, vStore.getCount() - 1)
    };
  },

  // 지정 구간에서 바뀐 행만 IU동작
  reseq: function (grid, seqField, range, extraSetter) {
    if (!range) return;

    var view   = grid.getView();
    var vStore = (view.store || view.getStore());
    var real   = vStore.getSource ? vStore.getSource() : vStore; // ChainedStore 대비

    Ext.suspendLayouts();
    real.suspendEvents();

    try {
      for (var i = range.start; i <= range.end; i++) {
        var r = vStore.getAt(i);
        if (!r || r.get('DELETE') === true) continue;

        var target = i + 1;
        if (r.get(seqField) !== target) {
          r.set(seqField, target);
          if (!r.get('IUD')) r.set('IUD', 'IU');
          if (typeof extraSetter === 'function') extraSetter(r);
        }
      }
    } finally {
      real.resumeEvents();
      Ext.resumeLayouts(true);
    }
  },

  onMasterViewReady: function (grid) {
    grid.getView().on('drop', this.onMasterDrop, this);
  },
  onDetailViewReady: function (grid) {
    grid.getView().on('drop', this.onDetailDrop, this);
  },

  onMasterDrop: function (node, data, overModel, dropPos) {
    var g     = this.getView().down('#grid_01');
    var view  = g.getView();
    var range = this.getRange(view, data, overModel, dropPos);
    this.reseq(g, 'VIEW_SEQ', range, function (rec) {
      rec.set('FACTORY_CODE', gFactoryCode);
      if (typeof gUserId !== 'undefined') rec.set('OPMAN_CODE', gUserId);
    });
  },

  onDetailDrop: function (node, data, overModel, dropPos) {
    var g     = this.getView().down('#grid_02');
    var view  = g.getView();
    var range = this.getRange(view, data, overModel, dropPos);
    this.reseq(g, 'VIEW_SEQ', range, function (rec) {
      rec.set('FACTORY_CODE', gFactoryCode);
      if (typeof gUserId !== 'undefined') rec.set('OPMAN_CODE', gUserId);
    });
  }
});
```


---