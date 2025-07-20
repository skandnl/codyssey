📄 도커 및 컨테이너 기술 개념 정리
### 1. 가상머신(VM)과 컨테이너의 차이
항목	가상머신 (Virtual Machine)	컨테이너 (Container)
아키텍처	하이퍼바이저 위에 OS 전체 설치	호스트 OS 위에 컨테이너 엔진 설치
시스템 자원	각 VM이 전체 OS를 포함 → 무겁고 느림	컨테이너는 호스트 커널 공유 → 가볍고 빠름
부팅 시간	수십 초 ~ 수 분	수 초 이내
이미지 크기	수 GB 이상	수 MB ~ 수백 MB
격리 수준	강력한 격리 (전체 OS 격리)	프로세스 수준의 격리
사용 사례	여러 OS 환경이 필요한 상황	마이크로서비스, DevOps, 빠른 배포

요약: VM은 무겁지만 보안과 격리에 유리하고, 컨테이너는 경량화된 환경에서 빠른 실행과 배포가 가능하다.

### 2. 컨테이너와 이미지의 차이
항목	컨테이너 (Container)	이미지 (Image)
정의	실행 중인 인스턴스	실행 가능한 파일 시스템 스냅샷
상태	동적 (mutable)	정적 (immutable)
목적	애플리케이션 실행	컨테이너 실행의 기반
생성 시점	이미지를 기반으로 생성	Dockerfile 등으로 사전 생성
존재 형태	프로세스로 동작	파일 형태로 저장됨 (.tar 등)

요약: 이미지는 실행 전 상태이며, 컨테이너는 그 이미지를 기반으로 실행된 애플리케이션 환경이다.

### 3. 컨테이너 런타임(Container Runtime)의 정의
컨테이너 런타임은 컨테이너의 생성, 실행, 중지, 삭제 등을 담당하는 소프트웨어입니다.
컨테이너 이미지를 기반으로 실제 컨테이너 프로세스를 실행하는 역할을 수행합니다.

컨테이너 런타임은 크게 두 단계로 나뉨:

High-level runtime: 예) Docker, containerd

Low-level runtime: 실제 리눅스 커널의 namespace/cgroups를 사용하여 컨테이너 생성 (예: runc)

### 4. CNCF Landscape 기준 컨테이너 런타임 종류 (3가지)
CNCF Cloud Native Landscape에 따르면 주요 컨테이너 런타임은 다음과 같습니다:

containerd

Docker에서 분리된 고성능 런타임

Kubernetes의 기본 런타임

CRI-O

Kubernetes만을 위해 개발된 경량 런타임

OpenShift 등에서 사용됨

gVisor

Google에서 개발

보안 격리에 중점을 둔 샌드박싱 런타임

### 5. 도커 이미지의 레이어 구조
Docker 이미지는 여러 개의 레이어로 구성된 스냅샷 구조입니다.

**레이어(Layer)**는 명령어(Dockerfile의 RUN, COPY, ADD 등)에 따라 생성됨.

각 레이어는 읽기 전용(read-only).

최상단 레이어만 읽기/쓰기 가능 (컨테이너 실행 시).

레이어는 캐싱되어 여러 이미지 간에 공유됨 → 빌드 속도 및 저장 공간 최적화.

예시 구조
Dockerfile
복사
편집
FROM ubuntu           # base layer
COPY . /app           # layer 1
RUN apt-get update    # layer 2
RUN pip install ...   # layer 3
ubuntu는 기반 이미지

각 명령어는 새로운 레이어로 추가됨

장점
효율적인 저장소 사용

빠른 빌드

변경된 부분만 다시 빌드 가능

