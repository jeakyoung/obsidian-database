


지금까지 나눈 대화 히스토리는 없는 새 세션이야. 이 디렉토리({새 프로젝트 경로})의 코드베이스를 문서화할 건데,
  아래 순서로 진행해줘.

  1. 이 디렉토리가 git 저장소인지 확인해. git 저장소면 git submodule add https://github.com/jeakyoung/obsidian-database.git obsidian 로
     진짜 서브모듈로 연결하고, git 저장소가 아니면(SVN 등) git clone https://github.com/jeakyoung/obsidian-database.git obsidian 로
     독립된 clone을 만들어서 연결해줘. (커밋/푸시는 그 clone 안에서 바로 자유롭게 할 수 있어야 함, origin은 이미 push 권한 있는 상태)
  2. 방금 연결한 obsidian 폴더 안에서 Jeakyoung_Blog/01_Projects/ 밑에 이 프로젝트({프로젝트명}) 폴더를 찾아줘.
     없으면 다른 프로젝트들(01~08번대) 폴더링 컨벤션(01_Tasks/02_TechDocs/03_Meetings/04_References + index.md)을
     그대로 따라서 새로 만들어줘.
  3. 01_Projects/06_ReelTrip 폴더를 품질 기준으로 삼아줘 — 특히 02_Docs/ReelTrip 프로젝트 개요.md,
     02_Docs/ReelTrip 개발 과정.md, 03_TechDocs/[기술] URL 파서 수집 전략.md 를 먼저 읽고 스타일을 파악해:
     실제 파일 경로·함수명·SP명 기반 서술, 정직한 캐비어트(> [!warning]/> [!note]), 표, [[위키링크]] 교차연결,
     빈 템플릿 섹션 방치 금지. 반대로 ReelTrip의 [기술] RT Database 관점의 Backend 아키텍처.md 같은 건
     일반론적 AI 템플릿 안티패턴이니 참고하지 마.
  4. 이 프로젝트({프로젝트명})의 TechDocs/References/Tasks에 있는 모든 기술적 주장(파일 경로, 클래스명,
     SP/함수명, 코드 예시)을 실제 코드베이스({코드베이스 경로})와 대조해서 검증하고, 틀리거나 지어낸 내용은
     실제 코드 기준으로 고쳐줘. 코드에 없는 걸 지어내지 말고, 확인 안 되는 건 "미확인"이라고 정직하게 표기해.
  5. 회의록(Meetings) 폴더는 원본 기록이니까 내용을 새로 지어내지 말고(없던 참석자/결정사항 창작 금지),
     오탈자·구조 정리, 논의내용 가독성 정리, 이미 있는 결정/후속조치를 논의 내용 속에서 찾아 해당 섹션에
     옮기는 정도의 포맷 정리만 해줘.
  6. 문서 톤은 팩트 기반으로 담백하게 — 문제나 미해결 버그를 지적할 때도 필요 이상으로 날 서게(뼈 때리듯) 쓰지 말고
     담백하게 서술해줘.
  7. 인덱스는 tools/build_index.py/tools/build_format_docs.py가 있으면 그걸로 재생성하고 손으로 고치지 마.
  8. 작업량이 크면(코드베이스 grep, 여러 문서 동시 재작성) 컨텍스트 아끼려고 fork/subagent로 나눠서 진행해도 돼 —
     TechDocs+References → Tasks → Meetings 순서로 단계별로 나눠서 진행해줘.
  9. 다 끝나면 회의록 폴더는 건드리지 않았는지(해당 단계 전까지) git diff --stat로 확인하고,
     커밋 메시지 끝에 Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com> 붙이고,
     git pull --rebase origin main 후 git push origin main 해줘. force-push는 하지 마. 

프로젝트명은 DongBang이야