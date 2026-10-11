# RabbitMQ 기반 IoT 모니터링 메시징 시스템

## 1. 프로젝트 소개

Python과 RabbitMQ를 활용하여 IoT 환경에서 발생하는 데이터를 메시지 형태로 전달하고 수신하는 과정을 구현한 프로젝트입니다.

RabbitMQ의 메시지 브로커 기능과 Exchange, Queue, Binding, Routing Key의 동작 원리를 이해하고, Docker Compose를 이용해 개발 환경을 구성하는 것을 목표로 합니다.

## 2. 개발 목표

- RabbitMQ를 활용한 메시지 발행(Publish) 및 수신(Consume) 구현
- Exchange 유형에 따른 메시지 라우팅 방식 이해
- Routing Key와 Binding을 이용한 메시지 전달 제어
- Docker Compose를 활용한 개발 환경 구성
- IoT 센서 데이터를 모사한 메시지 처리 구조 설계

## 3. 기술 스택

| 구분 | 기술 |
|---|---|
| Language | Python |
| Message Broker | RabbitMQ |
| Messaging Library | Pika |
| Database | MariaDB |
| Container | Docker, Docker Compose |
| Development Environment | Visual Studio Code |
| Version Control | Git, GitHub |

## 4. 시스템 구성

본 프로젝트는 Python 애플리케이션에서 생성한 메시지를 RabbitMQ에 전달하고, Consumer가 해당 메시지를 수신하는 구조로 구성됩니다.

```text
[Python Publisher]
        |
        | Publish Message
        v
    [Exchange]
        |
        | Binding & Routing Key
        v
      [Queue]
        |
        | Consume Message
        v
 [Python Consumer]

[Docker Compose]
    ├── RabbitMQ
    └── MariaDB
```

※ MariaDB는 현재 개발 환경에 구성되어 있으며, 메시지 데이터 저장 기능은 실제 구현 여부에 따라 별도로 기술합니다.

## 5. 주요 구현 기능

### 5.1 메시지 발행 및 수신

- Python의 `pika` 라이브러리를 이용한 RabbitMQ 연결
- Publisher를 통한 메시지 발행
- Consumer를 통한 메시지 수신
- 메시지 전송 및 수신 결과 확인

### 5.2 Exchange와 메시지 라우팅

RabbitMQ의 Exchange 유형에 따른 메시지 전달 방식을 실습했습니다.

- **Direct Exchange**: Routing Key가 일치하는 Binding을 통해 메시지 전달
- **Fanout Exchange**: 연결된 모든 Binding 대상으로 메시지 전달
- **Topic Exchange**: Routing Key의 패턴을 기반으로 메시지 전달

### 5.3 IoT 데이터 메시지 처리

IoT 센서 데이터를 모사한 메시지를 생성하고, 메시지의 Routing Key를 기준으로 데이터를 구분할 수 있도록 구성했습니다.

사용한 Routing Key의 예시는 다음과 같습니다.

- `data`
- `temperature`
- `humidity`
- `status`

이를 통해 센서 데이터 유형이나 상태 정보에 따라 메시지를 분류하고 전달하는 방식을 확인했습니다.

### 5.4 Docker 기반 개발 환경 구성

Docker Compose를 이용해 RabbitMQ와 MariaDB 컨테이너를 실행하고, 개발 환경을 구성했습니다.

이를 통해 개발 환경의 설치 및 실행 과정을 관리하고 각 서비스의 실행 상태를 확인했습니다.

## 6. 테스트 및 검증

현재까지 진행한 주요 검증 항목입니다.

- [x] Docker Compose를 통한 서비스 실행
- [x] RabbitMQ 연결 확인
- [x] Python Publisher의 메시지 발행 확인
- [x] Python Consumer의 메시지 수신 확인
- [x] Exchange 및 Binding을 통한 메시지 라우팅 확인
- [x] Topic Exchange의 패턴 기반 메시지 전달 확인
- [x] 여러 Consumer를 실행했을 때 메시지 분배 동작 확인

## 7. 실행 환경

### 사전 요구사항

- Python
- Docker Desktop
- Docker Compose
- RabbitMQ 및 MariaDB 실행에 필요한 설정 파일

### 실행 방법

1. 저장소를 로컬 환경에 복제합니다.
2. 프로젝트 디렉터리에서 Docker Compose를 실행합니다.
3. Python 가상환경을 활성화합니다.
4. 필요한 Python 패키지를 설치합니다.
5. Publisher와 Consumer를 실행하여 메시지 송수신을 확인합니다.

```powershell
docker compose up -d
docker compose ps
```

서비스 종료:

```powershell
docker compose down
```

Python 프로그램의 실행 명령어와 파일 경로는 실제 저장소 구조에 맞게 추가합니다.

## 8. 학습 내용 및 향후 개선 방향

이번 프로젝트를 통해 메시지 브로커의 역할과 메시지 라우팅 구조를 이해하고, Publisher와 Consumer 간의 비동기 메시지 전달 과정을 실습했습니다.

향후 다음 기능을 추가하여 IoT 모니터링 시스템으로 확장할 계획입니다.

- MariaDB를 활용한 센서 데이터 저장
- 센서 데이터의 임계치 초과 감지 및 알림
- Consumer 장애 및 메시지 처리 실패에 대한 예외 처리
- 메시지 영속성, ACK 및 재전송 처리
- 실시간 센서 데이터 모니터링 대시보드 구현

## 9. 참고 자료

- RabbitMQ. (n.d.). *RabbitMQ documentation*. https://www.rabbitmq.com/docs
- Pika Contributors. (n.d.). *Pika: Python RabbitMQ client library*. GitHub. https://github.com/pika/pika
- Docker, Inc. (n.d.). *Docker Compose documentation*. https://docs.docker.com/compose/
- MariaDB Foundation. (n.d.). *MariaDB documentation*. https://mariadb.com/docs/
