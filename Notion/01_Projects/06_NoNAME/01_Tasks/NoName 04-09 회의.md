---
base: "[[Notion/프로젝트 문서화/프로젝트/NoNAME 프로젝트 DB/Project  Todo - 프로젝트 Todo/Project  Todo - 프로젝트 Todo.base]]"
태그: []
상태: 진행 중
생성 일시: 2026-06-10T14:29:00
담당자: []
---
주제 -  여행 일정 수립 → 공유 캘린더

**지도 API 어디꺼쓸지 ( 카카오, 네이버 : **[https://navermaps.github.io/maps.js.ncp/](https://navermaps.github.io/maps.js.ncp/)** )**

**릴스 기반 위치 토큰 생성 ( 웹에서 할수있는지 주소로만 파싱해야함 )**

## Design


# FE 

## TS + NextJS

- MSW
- Tailwind *** **( 요즘유행 )**
- zustand, tanStack query, axios **( 요즘유행 )**

Orval

# BE

## JAVA + Spring Boot


# Server

Vercel

Docker

## PostgreSQL + pgvector (Hybrid Search) **(Vector DB) 요즘 유행 ( AI 메모리 )**

→ 

1. IVF(Inverted File Index)
IVF방식은 데이터셋을 미리 정의된 수의 군집(centroid)으로 나누고, 각 벡터를 가장 가까운 centroid에 할당함으로써 검색범위를 제한하는 방식으로 ANN에 공헌한다. 검색 시, 쿼리벡터가 속하는 군집을 먼저 찾고, 해당 군집내에서 가장 유사한 벡터를 찾는 방식이라고 이해하면 된다.
빠른 검색속도를 구현했지만, 매 검색 시 적절한 군집수를 선택해야하고, 군집화에 시간이 소요될 수 있다는 점이 단점이다.
2. PQ(양자화 기반 검색, Product Quantization)
PQ방식은 고차원 벡터를 여러개의 하위 벡터로 분할하고, 각 하위 벡터를 양자화하여 저장공간을 줄이는 방식이다.
조금 더 구체적으로 설명하면, 예를들어 2차원 벡터공간에서 4개의 코드워드로 구성된 코드북을 생성했다고 가정하자.
이때, 코드워드는 벡터공간내의 대표 포인트를 의미하는데, centroid와 비슷한 개념으로 이해했다.
그리고 코드북은 이러한 코드워드들의 집합이다.
결국 모든 포인트는 가장 가까운 코드워드로 대체되며 전체 데이터포인트의 크기는 줄어들게 된다.
이를 양자화로 표현하는것이고, 이로 인해 줄어든 공간에서의 검색속도 또한 범위가 줄어들기 때문에 빨라질 수 밖에 없다는
원리이다.
3. HNSW(Hierarchical Navigable Small World)
HNSW방식은 다계층 그래프 구조를 사용하여, 고차원 데이터에 대한 효윬적인 최근접 이웃 검색을 수행하는 방법이다.
HNSW방식은 속도도 빠르고, 다른 인덱싱 기법에 비해 정확하다는 강점을 가진다.
4. LSH(Locality-Sensitive Hashing)
데이터 포인트를 해시 테이블에 매핑하여, 쿼리 벡터와 유사한 데이터 포인트들을 빠르게 검색하는 방법이다. LSH는 유사한 객체가
'같은 버킷'에 할당될 확률을 높이는 해시 함수를 사용한다.

1안 : ReeL Trips

2안 : Trip Piece

3안 : Trip Guide

4안 : TriPicker


3안 : Reel Ri Ri Ah (3R Ah~)

4안 : Reel Hybrid ( 릴하 )

5안 : Gradient ( 10cm )

6안 : Discovery NIKE

7안 : 



릴 트 reelTravel

여명808

여명1004

릴스 픽커
