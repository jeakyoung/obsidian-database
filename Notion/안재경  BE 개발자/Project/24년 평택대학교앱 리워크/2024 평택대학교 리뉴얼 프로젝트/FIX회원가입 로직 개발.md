---
base: "[[Notion/안재경  BE 개발자/Project/24년 평택대학교앱 리워크/2024 평택대학교 리뉴얼 프로젝트/2024 평택대학교 리뉴얼 프로젝트.base]]"
생성일: 2025-01-19T18:55:00
태그: []
---
- 회원가입 로직 개발중 중복확인 처리관련해서 서비스, controller를 분리해야됨을 확인
- 분리하지 않을경우 마지막에 일괄 중복처리후 alert메시지가 전송된후 회원가입 단계를 처음부터 다시시작해야함 UX적으로 좋지않음
- 서비스, controller 분할

ID → 학번 → E-MAIL 분할

```javascript
package com.example.Lee.controller;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired; // 스프링의 의존성 주입 기능을 위한 어노테이션
import org.springframework.http.ResponseEntity; // HTTP 응답을 캡슐화하는 클래스
import org.springframework.web.bind.annotation.PostMapping; // POST 요청을 처리하는 메소드를 위한 어노테이션
import org.springframework.web.bind.annotation.RequestBody; // HTTP 요청 본문을 메소드 파라미터로 바인딩하는 어노테이션
import org.springframework.web.bind.annotation.RequestMapping; // 요청 URL을 매핑하기 위한 어노테이션
import org.springframework.web.bind.annotation.RestController; // REST 컨트롤러임을 나타내는 어노테이션
import org.springframework.web.context.request.RequestAttributes; // 요청범위와 세션범위를 지정
import org.springframework.web.context.request.RequestContextHolder; // Attribute 를 관리

import com.example.Lee.model.CommonResponseModel; // 공통 응답 모델 클래스
import com.example.Lee.model.RegiModel; // 회원 등록 정보 모델 클래스
import com.example.Lee.service.RegiService; // 회원 등록 서비스 클래스
import com.example.Lee.service.IdRegiService; // ID 등록 서비스 클래스
import com.example.Lee.service.StdRegiService; // 학번 등록 서비스 클래스
import com.example.Lee.service.MailRegiService; // Mail 등록 서비스 클래스

@RestController // 이 클래스가 REST 컨트롤러로 동작함을 스프링에게 알림
@RequestMapping("/PTU/Register") // "/PTU/Register" 경로로 들어오는 요청을 이컨트롤러로
public class RegiController {

	private final RegiService regiService; // 회원 등록 서비스 객체
	private final IdRegiService idRegiService; // ID 등록 서비스 객체
	private final StdRegiService stdRegiService; // 학번 등록 서비스 객체
	private final MailRegiService mailRegiService; // Mail 등록 서비스 객체

	@Autowired // 의존성 자동 주입. 스프링이 RegiService 타입의 객체를 자동으로 주입
	public RegiController(RegiService regiService, IdRegiService idRegiService, StdRegiService stdRegiService, MailRegiService mailRegiService) {
		this.regiService = regiService; 
		this.idRegiService = idRegiService;
        this.stdRegiService = stdRegiService;
        this.mailRegiService = mailRegiService;	// 생성자를 통해 주입받은 서비스 객체를 필드에 할당
	}
	
	// 세션에 속성 값을 설정함
    private void setSessionAttribute(String name, Object value) {
        RequestContextHolder.currentRequestAttributes().setAttribute(name, value, RequestAttributes.SCOPE_SESSION);
    }

    // 세션에서 속성 값을 가져옴
    private Object getSessionAttribute(String name) {
        return RequestContextHolder.currentRequestAttributes().getAttribute(name, RequestAttributes.SCOPE_SESSION);
    }

    // 전부다 사용한 세션을 제거
    private void removeSessionAttribute(String name) {
        RequestContextHolder.currentRequestAttributes().removeAttribute(name, RequestAttributes.SCOPE_SESSION);
    }

    @PostMapping("/ID") // ID 등록 엔드포인트
    public ResponseEntity<CommonResponseModel> registerId(@RequestBody Map<String, String> requestData) {
        RegiModel regiData = new RegiModel();
        regiData.setMembId(requestData.get("MEMB_ID"));

        // ID 중복 처리 후 결과 코드 확인
        CommonResponseModel idResult = idRegiService.registerId(regiData);
        if (!"00".equals(idResult.getRSLT_CD())) {
            return ResponseEntity.ok(idResult);
        }

        // 세션에 MEMB_ID 저장
        setSessionAttribute("MEMB_ID", requestData.get("MEMB_ID"));
        return ResponseEntity.ok(idResult);
    }

    @PostMapping("/StdNum") // 학번 등록 엔드포인트
    public ResponseEntity<CommonResponseModel> registerStdNum(@RequestBody Map<String, String> requestData) {
        RegiModel regiData = new RegiModel();
        regiData.setStdNum(requestData.get("STD_NUM"));

        // 학번 중복 처리 후 결과 코드 확인
        CommonResponseModel stdResult = stdRegiService.registerStd(regiData);
        if (!"00".equals(stdResult.getRSLT_CD())) {
            return ResponseEntity.ok(stdResult);
        }

        // 세션에 STD_NUM 저장
        setSessionAttribute("STD_NUM", requestData.get("STD_NUM"));
        return ResponseEntity.ok(stdResult);
    }

    @PostMapping("/Mail") // 이메일 등록 엔드포인트
    public ResponseEntity<CommonResponseModel> registerMail(@RequestBody Map<String, String> requestData) {
        RegiModel regiData = new RegiModel();
        regiData.setEmail(requestData.get("EMAIL"));

        // 이메일 중복 처리 후 결과 코드 확인
        CommonResponseModel mailResult = mailRegiService.mailRegister(regiData);
        if (!"00".equals(mailResult.getRSLT_CD())) {
            return ResponseEntity.ok(mailResult);
        }

        // 세션에 EMAIL 저장
        setSessionAttribute("EMAIL", requestData.get("EMAIL"));
        return ResponseEntity.ok(mailResult);
    }

    @PostMapping("/StdInfo") // 전체 정보 등록 엔드포인트
    public ResponseEntity<CommonResponseModel> registerStdInfo(@RequestBody Map<String, String> requestData) {
        // 세션에서 저장된 MEMB_ID, STD_NUM, EMAIL 가져오기
        String membId = (String) getSessionAttribute("MEMB_ID");
        String stdNum = (String) getSessionAttribute("STD_NUM");
        String email = (String) getSessionAttribute("EMAIL");

        RegiModel regiData = new RegiModel();
        regiData.setMembId(membId);
        regiData.setStdNum(stdNum);
        regiData.setEmail(email);
        regiData.setPass(requestData.get("PASS"));
        regiData.setStdDepCd(requestData.get("STD_DEP_CD"));
        regiData.setName(requestData.get("NAME"));

        // 회원 정보 저장
        CommonResponseModel result = regiService.registerUser(regiData);

        // 다 사용한 세션 삭제
        removeSessionAttribute("MEMB_ID");
        removeSessionAttribute("STD_NUM");
        removeSessionAttribute("EMAIL");
        
        //리스트 반환
        return ResponseEntity.ok(result);
    }
}
```

→ regicontroller.java

```javascript
package com.example.Lee.dao;

import org.springframework.data.jpa.repository.JpaRepository; // JPA 리포지토리 기능을 제공하는 스프링 프레임워크의 인터페이스
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.transaction.annotation.Transactional;

import com.example.Lee.model.RegiModel; // 회원 등록 모델

// JpaRepository<엔티티 타입, ID 필드 타입>을 상속받음으로써 기본적인 CRUD 및 페이지네이션, 정렬 기능을 사용할 수 있음
public interface RegiRepositoryDao extends JpaRepository<RegiModel, String> {
	// 학번을 기준으로 기존 등록 여부를 확인하는 메서드
	boolean existsByStdNum(String stdNum);

	// 이메일을 기준으로 기존 등록 여부를 확인하는 메서드
	boolean existsByEmail(String email);

	// 회원 ID를 기준으로 기존 등록 여부를 확인하는 메서드
	boolean existsByMembId(String membId);
	
	//membId 등록 쿼리문 (분리된 서비스)
	@Transactional
		@Modifying
		@Query(value="INSERT INTO stu_info(MEMB_ID)VALUES(:membId)", nativeQuery=true)
			void saveMembId(String membId);
	
	//학번 등록 쿼리문 (분리된 서비스)
	@Transactional
		@Modifying
		@Query(value="INSERT INTO stu_info(STD_NUM)VALUES(:stdNum)", nativeQuery=true)
			void saveMembStdNum(String stdNum);
	
	//이메일 등록 쿼리문	(분리된 서비스)
	@Transactional
		@Modifying
		@Query(value="INSERT INTO stu_info(EMAIL)VALUES(:email)", nativeQuery=true)
			void saveEmail(String email);
}
```

→ regirepositoryDAO.java

```javascript
package com.example.Lee.service;

import org.springframework.beans.factory.annotation.Autowired; // 스프링의 의존성 주입을 위한 어노테이션
import org.springframework.stereotype.Service; // 스프링에서 서비스 계층의 컴포넌트를 정의하는 어노테이션
import org.springframework.transaction.annotation.Propagation; //스프링에서 롤백의 범위를 지정하는 어노테이션
import org.springframework.transaction.annotation.Transactional;

import com.example.Lee.dao.RegiRepositoryDao; // 회원 정보에 접근하기 위한 DAO
import com.example.Lee.model.CommonResponseModel; // 클라이언트에 반환될 공통 응답 모델
import com.example.Lee.model.RegiModel;	// 등록할 회원의 정보모델

@Service // 이 클래스가 서비스 계층의 컴포넌트임을 나타냄
public class StdRegiService {

    private final RegiRepositoryDao regiRepository; // 회원 정보에 접근하기 위한 레포지토리 객체

    @Autowired // 스프링이 자동으로 해당 타입의 빈(Bean)을 주입
    public StdRegiService(RegiRepositoryDao regiRepository) {
        this.regiRepository = regiRepository; // 생성자를 통해 주입받은 레포지토리 객체를 필드에 할당
    }

    
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    // 학번을 인자로 받아 중복 여부를 확인하는 메서드
    public CommonResponseModel registerStd(RegiModel regiData) {
        // 학번이 이미 등록되어 있는지 확인
        if (regiRepository.existsByStdNum(regiData.getStdNum())) {
            return new CommonResponseModel("02"); // 학번이 중복인 경우 응답 코드 "02" 반환
        }
        // 학번 등록 성공시 응답코드 "00" 반환
        return new CommonResponseModel("00");
    }
}

```

→ StdRegiService.java

```javascript
package com.example.Lee.service;

import org.springframework.beans.factory.annotation.Autowired; // 스프링의 의존성 주입을 위한 어노테이션
import org.springframework.stereotype.Service; // 스프링에서 서비스 계층의 컴포넌트를 정의하는 어노테이션
import org.springframework.transaction.annotation.Propagation; //스프링에서 롤백의 범위를 지정하는 어노테이션
import org.springframework.transaction.annotation.Transactional;

import com.example.Lee.dao.RegiRepositoryDao; // 회원 정보에 접근하기 위한 DAO
import com.example.Lee.model.CommonResponseModel; // 클라이언트에 반환될 공통 응답 모델
import com.example.Lee.model.RegiModel; // 등록할 회원의 정보 모델

@Service // 이 클래스가 서비스 계층의 컴포넌트임을 나타냄
public class IdRegiService {

	private final RegiRepositoryDao regiRepository; // 회원 정보에 접근하기 위한 레포지토리 객체

	@Autowired // 스프링이 자동으로 해당 타입의 빈(Bean)을 주입
	public IdRegiService(RegiRepositoryDao regiRepository) {
		this.regiRepository = regiRepository; // 생성자를 통해 주입받은 레포지토리 객체를 필드에 할당
	}
	
	@Transactional(propagation = Propagation.REQUIRES_NEW)
	public CommonResponseModel registerId(RegiModel regiData) {
		// 사용자 ID가 이미 등록되어 있는지 확인
		if (regiRepository.existsByMembId(regiData.getMembId())) {
			return new CommonResponseModel("01"); // ID가 중복인 경우 응답 코드 "01" 반환
		}
		// ID 등록 성공 시 응답 코드 "00" 반환
		return new CommonResponseModel("00");
	}
	

}
```

→ IdRegisterService.java

```javascript
package com.example.Lee.service;

import org.springframework.beans.factory.annotation.Autowired; // 스프링의 의존성 주입을 위한 어노테이션
import org.springframework.stereotype.Service; // 스프링에서 서비스 계층의 컴포넌트를 정의하는 어노테이션
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import com.example.Lee.dao.RegiRepositoryDao; // 회원 정보에 접근하기 위한 DAO
import com.example.Lee.model.CommonResponseModel; // 클라이언트에 반환될 공통 응답 모델
import com.example.Lee.model.RegiModel; // 등록할 회원의 정보 모델

@Service // 이 클래스가 서비스 계층의 컴포넌트임을 나타냄
public class MailRegiService {

	private final RegiRepositoryDao regiRepository; // 회원 정보에 접근하기 위한 레포지토리 객체

	@Autowired // 스프링이 자동으로 해당 타입의 빈(Bean)을 주입
	public MailRegiService(RegiRepositoryDao regiRepository) {
		this.regiRepository = regiRepository; // 생성자를 통해 주입받은 레포지토리 객체를 필드에 할당
	}
	
	@Transactional(propagation = Propagation.REQUIRES_NEW)
	// 메일을 인자로 받아 중복여부를 확인하는 메서드
	public CommonResponseModel mailRegister(RegiModel regiData) {
		// 이메일이 이미 등록되어 있는지 확인
		if (regiRepository.existsByEmail(regiData.getEmail())) {
			return new CommonResponseModel("03"); // 메일이 중복인 경우 응답 코드 "03" 반환
		}
		// 이메일 등록 성공 시 응답 코드 "00" 반환
		return new CommonResponseModel("00");
	}
}

```

→MailRegiService.java

```javascript
package com.example.Lee.service;

import org.springframework.beans.factory.annotation.Autowired; // 스프링의 의존성 주입을 위한 어노테이션
import org.springframework.stereotype.Service; // 스프링에서 서비스 계층의 컴포넌트를 정의하는 어노테이션

import com.example.Lee.dao.RegiRepositoryDao; // 회원 정보에 접근하기 위한 DAO
import com.example.Lee.model.CommonResponseModel; // 클라이언트에 반환될 공통 응답 모델
import com.example.Lee.model.RegiModel; // 등록할 회원의 정보 모델

@Service // 이 클래스가 서비스 계층의 컴포넌트임을 나타냄
public class RegiService {

	private final RegiRepositoryDao regiRepository; // 회원 정보에 접근하기 위한 레포지토리 객체

	@Autowired // 스프링이 자동으로 해당 타입의 빈(Bean)을 주입
	public RegiService(RegiRepositoryDao regiRepository) {
		this.regiRepository = regiRepository; // 생성자를 통해 주입받은 레포지토리 객체를 필드에 할당
	}

	public CommonResponseModel registerUser(RegiModel regiData) {
		regiRepository.save(regiData);
		// 회원 등록 성공 시 응답 코드 "00" 반환
		return new CommonResponseModel("00");
	}
}

```

→ RegiService.java

```javascript
package com.example.Lee.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

// 엔티티를 나타내며, 데이터베이스의 stu_info 테이블에 매핑됨 재경 test
@Entity
@Table(name = "stu_info")
public class RegiModel {

	@Id // 기본 키(PK) 필드임을 나타냄
	private String membId;

	@Column(unique = true) // 학번은 유니크(고유)해야 함
	private String stdNum;

	@Column(unique = true) // 이메일 또한 유니크(고유)해야 함
	private String email;

	private String pass; // 패스워드
	private String stdDepCd; // 학과 코드
	private String name; // 이름

	// 기본 생성자: JPA에서 엔티티 클래스는 기본 생성자를 가지고 있어야 함
	public RegiModel() {
	}

	// 모든 속성을 포함하는 생성자
	public RegiModel(String membId, String stdNum, String email, String pass, String stdDepCd, String name) {
		this.membId = membId;
		this.stdNum = stdNum;
		this.email = email;
		this.pass = pass;
		this.stdDepCd = stdDepCd;
		this.name = name;
	}

	// Getter and Setter 메서드: 엔티티의 속성에 접근하기 위한 메서드
	public String getMembId() {
		return membId;
	}

	public void setMembId(String membId) {
		this.membId = membId;
	}

	public String getStdNum() {
		return stdNum;
	}

	public void setStdNum(String stdNum) {
		this.stdNum = stdNum;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public String getPass() {
		return pass;
	}

	public void setPass(String pass) {
		this.pass = pass;
	}

	public String getStdDepCd() {
		return stdDepCd;
	}

	public void setStdDepCd(String stdDepCd) {
		this.stdDepCd = stdDepCd;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
}

```

→ RegiModel.java