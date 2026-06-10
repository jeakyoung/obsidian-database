---
base: "[[정보 저장소.base]]"
상태: 완료
담당자: []
팀: []
---
ㅇ 아이팩

외근/외출 등록 (개인)

외근/외출 현황 (관리)


외근일자 기준으로 과거일자는 작성이 불가합니다.

정렬순서 근태대로 재수정하기


- .netCore ATC 웹서버 여는 방법

![[image 25.png]]

ㅇ ATC 원격 접속 이후 → IIS내 사이트 우클릭

![[image 26.png]]

→ 설정

디렉토리 검색 → 사용클릭

→ 디렉토리 경로내에 default 설정 되어있는 webconfig 파일 수정필요

→ webconfig 설정 (.net 관련 버전 설정)

```sql
<?xml version="1.0" encoding="utf-8"?>
<configuration>
<location path="." inheritInChildApplications="false">
<system.webServer>
<handlers>
<add name="aspNetCore" path="" verb="" modules="AspNetCoreModuleV2" resourceType="Unspecified" />
</handlers>
<aspNetCore processPath="dotnet" arguments=".\F1Soft.Starmap.Service.dll" stdoutLogEnabled="false" stdoutLogFile=".\logs\stdout" hostingModel="inprocess" />
</system.webServer>
</location>
</configuration>
<!--ProjectGuid: 1FEEC658-1D2C-404C-904D-28206FFAE714-->
```

→ 해당 webconfig 후 오류 발생시 오류 메시지 그대로 GPT를 활용해서 config파일 재성성하기

→ 일단 ATC 서버에서 사용중인 포트번호는 40110, 40220, 40330 이렇게 세가지

→ 다른 서비스를 오픈했을때 만약 포트충돌이 생긴다면 다른 포트를 열어주어야함

→ 인바운드 규칙을 통해 사용을 원하는 포트를 반드시 허용조치 해줄것.

→ 사용할 포트가 이미 사용중인지 아닌지 명확히 확인할것.



- ATC 빌드 및 배포 방법

ATC 빌드를 할때는 IDE 내 release 항목이 체크되어있는지, http로 설정 되어있는지 명확히 확인할것 https 안됨

→ 빌드 완료후 경로 → 서비스내 bin폴더 → release 내에 존재함 해당 부분을 전부 복사해서

만들어둔 웹서버내 디렉토리 루트에 추가해주면됨

- ATC 내에서도 자동빌드 자동배포 기능 설정이 가능함 매뉴얼보고 조치하기
[[동방 iFrog 개발 환경 및 자동배포.pdf]]

- GITLAB 토큰 관리

[[webconfig.txt]]

expire 해당 없음 → gitlab을 통해 push pull 을 위한 access tocken


- VSstudio 디버깅 방법 break point 선언후 f10을통해 한줄 한줄 넘겨 오류지점찾기

break point 설정후 