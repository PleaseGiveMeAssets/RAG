# PleaseGiveMeAssets RAG Project
- **공통 사항**
  - 배포전 프로젝트 자동정렬 및 import 필수!!!(PyCharm CE)
    - 정렬
      - macOS : option + command + L
      - Window : Ctrl + Alt + L
    - import
      - macOS : control + option + O
      - Window : Ctrl + Alt + O
  - Git 배포시 commit message는 필수로 입력한다.
  - Git branch naming rule
    - feature : 기능 개발 브랜치 ex) feature/home
    - release : 버전 개발 브랜치 ex) release-1.0.0
    - hotfix : 긴급 개발 브랜치 ex) hotfix-1.0.0
    - 일반적으로 운영중이지 않은 소규모 프로젝트에서 hotfix는 사용할 필요가 없습니다. 대부분 feature 형태의 브랜치를 만들어 dev에 merge 해주시면 됩니다. release 브랜치는 테스트가 완료되면 팀장이 취합해 한번에 배포합니다.
  - 문의 사항은 Git issue나 comment, 디스코드를 통해 질문한다.
  - README.me 파일은 생각나는 기타 사항들을 모두 작성해주면 됩니다.

- **RAG 개발 가이드**
  - 링크 : https://bjhbhm.atlassian.net/wiki/spaces/cqdnDRC50KdZ/pages/4194305/RAG

#### 커밋 메시지 규칙 
|type | 사용예|
|-------|--------|
feat    | 새로운 기능 추가
docs	| 문서 수정
fix	    | 버그 수정
test    | 테스트 코드, 리팩토링 테스트 코드 추가
refactor| 코드 리팩토링
build   | 빌드 파일 수정
chore   | 빌드 업무 수정, 패키지 매니저 수정 (gitignore, ci/cd 관련 yaml파일 수정 등)
rename  | 파일 혹은 폴더명을 수정만 한 경우
remove  | 파일을 삭제만 한 경우

#### 예시
- {type}: 커멧메시지내용    
- 커밋 메시지 예시 - refactor: 로그인 기능 수정

-----------------------------------------------

### RAG

### 사용하는 이유
- 더 정확하고 관련성 높은 정보를 제공
  - 할루시네이션 효과 없음
  - 도메인에 특화된 정확한 답변을 제공할 수 있음

### 목표
 - 뉴스 데이터를 토대로 일일 동향 리포트 생성

0. 사전조건
  - DB에 종목 데이터가 저장되어 있음
  - 네이버 검색 API 키가 있음

1. 데이터 수집
  - 네이버 뉴스 검색 API를 통해 뉴스 기사 수집
  - 각 종목에 대해 뉴스 기사 10개를 수집(최대 100개)
  - 뉴스 기사 제목, 내용, 링크, 대표 이미지 저장
  - chroma vector store 저장
    1. 뉴스 데이터를 Document 형식으로 저장
    2. OpenAI의 text-embedding-3-large를 통해 벡터화
    3. chroma vector store에 저장
    - 문제점 : chroma에 저장된 데이터 개수가 많으면 에러 발생
    - 해결 : chroma db 샤딩 ex) collection을 chroma_db_1, chroma_db_2 ... 로 생성
  - MySQL DB에 저장

2. 검색
  - 쿼리 입력 시 뉴스 데이터 중 가장 유사도가 높은 Document 10개 검색
  - 검색된 데이터를 토대로 답변 생성
  - 답변을 생성하지 못하는 경우 :
    1. +5개의 문서를 추가로 검색
    2. 40개까지 검색
    3. 샤딩된 다른 vector store에서 검색
    4. 인터넷 검색을 통해 답변을 생성
    
3. 답변 생성
  - 검색된 데이터를 토대로 답변 생성
  - OpenAI의 gpt-4o-mini를 통해 답변 생성

### 개선 방안
  - langgraph를 활용하여 failover 구현
