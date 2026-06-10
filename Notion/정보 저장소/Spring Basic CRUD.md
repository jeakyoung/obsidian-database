---
base: "[[정보 저장소.base]]"
상태: 시작 전
담당자: []
팀: []
---
CRUD는

CREATE, READ, UPDATE, DELETE

의 약자라고 생각하면 된다~

SQL 기준으로 왼쪽부터

INSERT, SELECT, UPDATE, DELETE가 가장 기본적이다~

물론 무조건적으로 이렇게 쓰는건 아니긴하다~ 하지만 기본적으론 이렇게 4가지가 있구나~ 하면된다

```java
package com.example.demo.service;

import java.util.List;
import com.example.demo.domain.Notice;

public interface NoticeService {
	Notice create(Notice notice);
	Notice getById(int postSeq);
	List<Notice> listAll(int page);
	void update(Notice notice);
	void delete(int postSeq);
	//기능은 임플리먼트로 빼놓고 함수만 불러다가 쓴다~
	//이유는 찾아봐도 좋긴하다~ 기본적으론 유지보수하기 편해서 이렇게쓴다~
}
```

```java
package com.example.demo.service;
//이건 안다고 생각 하겠다~

import java.time.LocalDateTime; //날짜를 받아보겠다~
import java.util.List;          //배열을 쓰고싶다~
//사용할 유틸 선언하는 부분이다~

import org.springframework.stereotype.Service;    //서비스를 표시하겠다~
import org.springframework.transaction.annotation.Transactional; //음,, 이건한번 찾아봐라~ 안전장치같은 느낌이다~
//@뒤에붙어있는 친구들이 다 이친구들이다~

import com.example.demo.domain.Notice; //개별 가공
import com.example.demo.exception.NoticeNotFoundException; //뭐야 아무것도 없어요~
import com.example.demo.exception.UnauthorizedException; //도둑이야~
import com.example.demo.mapper.NoticeMapper; //여기부턴 DB단이랑 관련이있다~
//이 서비스를 실행하려고 여러군대로 파일을 뿌려놓은걸 합치는거다~

import lombok.RequiredArgsConstructor;
//자 여기서 시*롬복이 뭘까요~ 한번 찾아봐야한다~ 굉장이 중요하다~

@Service //아까봤던 서비스
@RequiredArgsConstructor //자동으로 매핑을 시켜준다~
public class NoticeServiceImpl implements NoticeService { //쉽게말하자면 service는 가짜다~
//실제 서비스는 여기서 시행된다~ 대신에 noticeservice에서 정해놓은 규칙은 작용한다~
	private static final int PAGE_SIZE = 10; //한페이지에 10개만 출력할게요~
	private final NoticeMapper mapper; //매퍼 선언
	
	//CRUD의 C에 해당하는 부분이다~
	
	@Override //상속개념은 알아야한다~ 이것도 찾아보면 된다~
	@Transactional //보통 서비스는 이런 예외처리가 없으면 에러상황이 발생할시 어,,,
	//밑에꺼를 했는데 실패하면 동상마냥 굳어버린다~ 그래서 이런걸쓰는데 간단하게 했다가 안되면 말지뭐~ 이거랑똑같은거다
	public Notice create(Notice notice) { 
		mapper.insertNotice(notice); //아까말한것 처럼 매퍼는 DB랑 관련이있다 항상 반드시~
		return notice; //문자그대로 mapper에 지정된 insertNotice에 데이터를 담아 글을넣고 작성글을 롤백시켜준다~
	} //그냥 그런가보다~ 하고넘어가면된다 밑에서 어짜피 또 보게될친구다~
	
	//아래 두가지는 CRUD의 R에 해당하는 부분이다~
	
	@Override
	public Notice getById(int postSeq) { //postSeq (정확힌모르지만 대충 작성번호인듯하다)
		Notice n = mapper.selectById(postSeq);
		//자 또나온 mapper지만 이번엔 selectByID다 아까랑 DB에 다른작용을한다 정도만 알면된다~ 
		if (n == null) throw new NoticeNotFoundException(postSeq);
		//쓸대없이 복잡해보이지만 @Transactional과 의도는 비슷하다~ 만약에 글을 찾지 못했으면
		//못찾은거에 대한 예외상황을 사용자한테 알려주는 과정이다~
		return n; //값이 있으면 출력~
	}
	@Override
	public List<Notice> listAll(int page) {
	//아까는 작성번호로 글을 찾았다면 이번엔 1번페이지 2번페이지처럼 특정 페이지에 해당되는
	//모든 작성글을 리스트 형식으로 찾아오는것이다~ 이런걸로 DB정보도 대략적으로 유추할수있다~
		int offset = (page - 1) * PAGE_SIZE;
	//어떤걸 가져올지 계산하는 과정이다~ PAGE_SIZE는 위에서 10개한다고 정의했으므로
	//page로 가져온 정보가 2페이지라고 친다면 (2-1)*10으로 11번째 글부터 가져온다고 생각하면 된다~
		return mapper.selectAll(offset, PAGE_SIZE);
	//이걸 계산해서 시작점과 몇개를 가져올지 인자에 담아 mapper를 굴려준다~
	}
	
	//아래 하나는 CRUD중 U에 해당되는 부분이다~
	
	@Override //알
	@Transactional //지?
	public void update(Notice notice) { //앞에 정의한것 처럼 업데이트는 이렇게한다~
		Notice existing = mapper.selectById(notice.getPostSeq());
		//글수정은 기본적으로 작성한 사람이나 SU계정만 가능한 일이다~ 때문에 ID를 기반으로 select를 호출할건데
		//getPostSeq의 역활이 여기서나온다~ 기본적으로 Seq값음 키값으로 관리되기에
		//SELECT를할때 인자로 사용하기 굉장히 좋다~ EX) 11 -> 11번째 게시글을 ID기반으로 select해보겠다~
		if (existing == null) throw new NoticeNotFoundException(notice.getPostSeq());
		//근데 글이아무것도 없다? 그럼 때리치와~
		if (!existing.getMembId().equals(notice.getMembId())) {
		//만약에 게시글에 작성자 ID를 까봤더니 지금 사용자랑 ID가 다르다?
			throw new UnauthorizedException();
			//도둑놈의 시키네요~
		}
		mapper.updateNotice(notice);
		//다되었으면 드디어 오케이 업데이트 허가~
	}
	
	//당연히 밑에꺼는 마지막 하나겠죠?
	
	@Override
	@Transactional
	public void delete(int postSeq) {
		Notice existing = mapper.selectById(postSeq);
		//이젠 알겠지? 사실 CRUD는 모든과정이 반복이다 똑같이 글을 찾아와서
		if (existing == null) throw new NoticeNotFoundException(postSeq);
		//찾아왔더니 아무것도 없으면 뭘지우라는거야 임마!
		mapper.softDelete(postSeq, LocalDateTime.now());
		//softDelete과정에 삭제 시간을 담아준다~
		//softDel은 보통 지우지만 지운게 아니다~
		//DB내 삭제된 항목으로 보관하고있는데 여기에 삭제시간도 같아담고있다~
		//용도는,, 다다르긴한데 보통 중요한 게시글을 누군가 악의적으로 삭제했을때'
		//어떤 사람이 나쁜놈인지 언제나쁜짓을 했는지 찾고 중요 게시글을 살리기 위함이다~
	}
}
```

```java
package com.example.demo.mapper;
// 그래서 그놈에 메퍼가 무엇이냐.
import java.time.LocalDateTime;
import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.example.demo.domain.Notice;

@Mapper
public interface NoticeMapper {
	int insertNotice(Notice notice);
	Notice selectById(int postSeq);
	List<Notice> selectAll( int offset, int limit);
	int updateNotice(Notice notice);
	int softDelete( int postSeq, LocalDateTime deleteAt);
	
	//사실 보다싶이 별거없다 어떤식으로 돌아가는지 궁금하다면 DTO를 찾아보면 된다~
}
```

```java
package com.example.demo.domain;

import java.time.LocalDateTime;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
//시#롬복이다 사실 생성자 자동주입은 굉장이 편하지만 개발환경 세팅할때마다 굉장히 말을
//안들어먹는편이다~
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Notice {
	private Integer postSeq;
	private String membId;
	private String postTit;
	private String postCont;
	private LocalDateTime createdAt;
	private LocalDateTime updatedAt;
	private LocalDateTime deleteAt;
 //원래는 GETTER랑 SETTER를 일일히 손으로 지정해주어야하지만
 //롬복을쓰면 생성자 주입자를 자동주입할수 있다~ 이게없으면 코드길이가 이거에 3배는 나올걸?
}
```

---

슬슬 피곤한 관계로 여기서 제일 중요한 DTO랑 controller를 빼놓고 자러갈듯하다.. 내일하지 뭐~

여기서 CRUD 백단부터 알려주는 이유는 가장 기초적이기도 하고 백단 코드에 대해 어느정도 까지 이해를

하고 DB단을 보면 선녀가 따로없다~

```java
package com.example.demo.controller;

import java.util.List;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;
import com.example.demo.domain.Notice;
import com.example.demo.dto.CreateNoticeRequest;
import com.example.demo.dto.DeleteNoticeRequest;
import com.example.demo.dto.UpdateNoticeRequest;
import com.example.demo.model.CommonResponseModel;
import com.example.demo.model.DataResponseModel;
import com.example.demo.model.ResultCode;
import com.example.demo.service.NoticeService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.ExampleObject;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;


@Tag(name = "POST CRUD", description = "공지사항 조등수삭 API")
@RestController
@RequestMapping("/api/notices")
@RequiredArgsConstructor
public class NoticeController {
	private final NoticeService service;
	
	@Operation(summary = "공지사항 등록", description = "공지사항을 등록합니다.")
	@ApiResponse(responseCode = "200", content = @Content(schema = @Schema(implementation = CommonResponseModel.class), examples = {
			@ExampleObject(name = "성공", value = "{\"RSLT_CD\":\"00\",\"PostSeq\":1,\"MemmId\":user123,\"PostTit\":TITLE,\"PostCont\":CONTENT}") }))
	@PostMapping
	public CommonResponseModel create(@Valid @RequestBody CreateNoticeRequest req) {
		Notice n = new Notice();
		n.setMembId(req.getMembId());
		n.setPostTit(req.getPostTit());
		n.setPostCont(req.getPostCont());
		service.create(n);
		return new CommonResponseModel(ResultCode.OK);
	}
	
	@Operation(summary = "공지사항 하나 조회", description = "하나의 공지사항만을 조회합니다.")
	@ApiResponse(responseCode = "200", content = @Content(schema = @Schema(implementation = DataResponseModel.class), examples = {
			@ExampleObject(name = "성공", value = "{\"RSLT_CD\":\"00\",\"게시글\":\"01\"}") }))
	@GetMapping("/{postSeq}")
	public DataResponseModel<Notice> getOne(@PathVariable int postSeq) {
		Notice n = service.getById(postSeq);
		return new DataResponseModel<>(ResultCode.OK, n);
	}
	
	@Operation(summary = "모든 공지사항 조회", description = "모든 공지사항을 조회합니다.")
	@ApiResponse(responseCode = "200", content = @Content(schema = @Schema(implementation = DataResponseModel.class), examples = {
			@ExampleObject(name = "성공", value = "{\"RSLT_CD\":\"00\",\"게시글 리스트\":\"01, 02, 03 ...\"}") }))
	@GetMapping
	public DataResponseModel<List<Notice>> listAll(int page) {
		List<Notice> list = service.listAll(page);
		return new DataResponseModel<>(ResultCode.OK, list);
	}
	
	@Operation(summary = "공지사항 수정", description = "공지사항을 수정합니다.")
	@ApiResponse(responseCode = "200", content = @Content(schema = @Schema(implementation = CommonResponseModel.class), examples = {
			@ExampleObject(name = "성공", value = "{\"RSLT_CD\":\"00\",\"PostSeq\":1,\"MemmId\":user123,\"PostTit\":title,\"PostCont\":content}") }))
	@PutMapping
	public CommonResponseModel update(@Valid @RequestBody UpdateNoticeRequest req) {
		Notice n = new Notice();
		n.setPostSeq(req.getPostSeq());
		n.setMembId(req.getMembId());
		n.setPostTit(req.getPostTit());
		n.setPostCont(req.getPostCont());
		service.update(n);
		return new CommonResponseModel(ResultCode.OK);
	}
	
	@Operation(summary = "공지사항 삭제", description = "공지사항을 삭제합니다.")
	@ApiResponse(responseCode = "200", content = @Content(schema = @Schema(implementation = CommonResponseModel.class), examples = {
			@ExampleObject(name = "성공", value = "{\"RSLT_CD\":\"00\",\"PostTit\":null,\"PostCont\":null}") }))
	@DeleteMapping
	public CommonResponseModel delete(@Valid @RequestBody DeleteNoticeRequest req) {
		service.delete(req.getPostSeq());
		return new CommonResponseModel(ResultCode.OK);
	}
	
}
```




```java
package com.example.demo.model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class DataResponseModel<T> extends CommonResponseModel {
	private T data;
	
	public DataResponseModel(ResultCode resultCode, T data) {
		super(resultCode);
		this.data = data;
	}
}
```

```java
package com.example.demo.dto;

import jakarta.validation.constraints.NotBlank;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class CreateNoticeRequest {
	@Schema(description = "회원 ID", example = "user123", requiredMode = Schema.RequiredMode.REQUIRED)
	@NotBlank
	private String membId;
	
	@Schema(description = "공지사항 제목", example = "공지사항 제목입니다.", requiredMode = Schema.RequiredMode.REQUIRED)
	@NotBlank
	private String postTit;
	
	@Schema(description = "공지사항 내용", example = "공지사항 내용입니다.", requiredMode = Schema.RequiredMode.REQUIRED)
	@NotBlank
	private String postCont;
	
	
}
```

```java
package com.example.demo.dto;


import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class DeleteNoticeRequest {
	@Positive
	@Schema(description = "공지사항 일련번호", example = "1", requiredMode = Schema.RequiredMode.REQUIRED)
	@NotBlank
	private Integer postSeq;
}
```
