# 11-WeWantedExplorers Readme

## Introduction
- Wanted - 스타트업 채용 사이트 (wanted.co.kr) 클론
- 개발기간 : 2020.08.31 - 2020.09.11 (2주)
- 개발인원 : Front-end 4명, Back-end 2명

## Achievement
- 사이트 선정 후, 전체적인 설계부터 배포까지 구현
- 스크럼 적용, 2주간 매일 스탠드업 미팅과 2번의 스프린트
- git rebase를 사용해 branch 관리
- 더 빠른 응답속도를 위해 redis 사용
- 최종 배포는 Docker container로 AWS EC2

## Skill Stacks
- Python
- Django
- Bcrypt
- JWT
- MySQL
- Redis
- Scrapy
- AWS EC2, RDS, Elasticache

## Apps
- position : 포지션(e.g. 백엔드, 프론트엔드, 등) 공고
- company : 회사 정보
- resume : 이력서 관리
- user : 사용자 관리

## Description
  모든 models 및view에 대한 test를 진행됐습니다. 전체적인 플로우는 회원가입을 하고, 이력서를 작성하여서 회사와 관련된 채용 공고에 지원하는 플로우입니다.
