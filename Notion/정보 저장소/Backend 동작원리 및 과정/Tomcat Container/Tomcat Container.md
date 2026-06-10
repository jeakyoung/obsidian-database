---

---
- **Engine(엔진)**: 가장 상위 레벨의 컨테이너로, 하나 이상의 호스트(Host)를 포함합니다. 주로 가상 호스팅(Virtual Hosting)을 지원합니다.

[[Notion/정보 저장소/Backend 동작원리 및 과정/Tomcat Container/ContainerEngine]]

- **Host(호스트)**: 단일 도메인 또는 IP 주소에 대한 웹 애플리케이션을 관리하는 컨테이너입니다. 하나의 엔진에 여러 호스트를 설정할 수 있습니다.

[[Notion/정보 저장소/Backend 동작원리 및 과정/Tomcat Container/ContainerHost]]

- **Context(컨텍스트)**: 웹 애플리케이션을 담당하는 컨테이너로, WAR 파일이나 디렉토리를 컨텍스트로서 등록하여 웹 애플리케이션을 실행합니다.

[[Notion/정보 저장소/Backend 동작원리 및 과정/Tomcat Container/ContainerContext]]

- **Wrapper(래퍼)**: 각각의 서블릿을 관리하는 컨테이너로, 서블릿을 실행하고 생명주기를 관리합니다.

[[Notion/정보 저장소/Backend 동작원리 및 과정/Tomcat Container/ContainerWrapper]]
