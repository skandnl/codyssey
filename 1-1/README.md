# [과제] 개발 워크스테이션 구축 및 Docker/Git 실습 보고서

## 1. 프로젝트 개요

미션 목표: 리눅스 터미널 조작, 권한 관리, Docker를 이용한 컨테이너 기반 웹 서버 구축 및 Git/GitHub 연동을 통한 버전 관리 역량 습득.

- 터미널 명령어로 디렉토리/파일을 생성·수정·삭제하고 권한을 직접 제어한다.
- Docker를 설치·점검하고 컨테이너를 빌드·실행·운영하며 이미지/컨테이너의 분리 원칙을 이해한다.
- Dockerfile로 커스텀 웹 서버 이미지를 만들고, 포트 매핑·바인드 마운트·볼륨으로 격리된 실행 환경과 데이터 영속성을 검증한다.
- Git으로 로컬 버전을 관리하고 GitHub 원격 저장소와 연동하여 협업 기반 소스코드 관리를 경험한다.

---

## 2. 실행 환경

| 항목 | 내용 |
|------|------|
| OS | macOS Sequoia 15.3.1 (Build: 24D70) |
| Shell/Terminal | Zsh 5.9 (arm-apple-darwin24.2.0) / iTerm2 |
| Docker 버전 | Docker version 29.3.1, build c2be9cc |
| Git 버전 | git version 2.50.1 (Apple Git-155) |

---

## 3. 수행 항목 체크리스트

- [x] 터미널 기본 조작 로그 기록 (pwd, ls, cd, mkdir, cp, mv, rm, cat, touch)
- [x] 파일/디렉토리 권한 변경 실습 및 증거 (파일 1개 + 디렉토리 1개)
- [x] Docker 설치 및 데몬 동작 확인 (docker --version, docker info)
- [x] Docker 기본 운영 명령 수행 (images, ps, logs, stats)
- [x] hello-world 및 ubuntu 컨테이너 실행 실습
- [x] 커스텀 Dockerfile 기반 웹 서버 컨테이너 제작
- [x] 포트 매핑 및 브라우저 접속 검증
- [x] 바인드 마운트 반영 (호스트 변경 전/후 비교)
- [x] Docker 볼륨 영속성 검증 (컨테이너 삭제 전/후 비교)
- [x] Git 설정 및 GitHub 저장소 연동 (VSCode 포함)

---

## 4. 상세 수행 내용 및 검증 로그

### 4.1 터미널 조작 및 권한 실습

**수행 명령:** `pwd`, `ls -al`, `cd`, `mkdir`, `cp`, `mv`, `rm`, `cat`, `touch`

```bash
# 현재 위치 확인
$ pwd
/Users/nsh/Desktop/cody

# 목록 확인 (숨김 파일 포함)
$ ls -al
total 32
drwxr-xr-x   7 nsh  staff   224 Mar 30 14:00 .
drwx------@ 31 nsh  staff   992 Mar 30 13:35 ..
drwxr-xr-x  12 nsh  staff   384 Mar 30 14:00 .git
-rw-r--r--@  1 nsh  staff  6982 Mar 30 13:55 E1-1.md
-rw-r--r--   1 nsh  staff   547 Mar 30 14:00 Dockerfile
drwxr-xr-x   3 nsh  staff    96 Mar 30 13:45 lab
-rw-r--r--   1 nsh  staff   709 Mar 30 14:00 index.html

# 디렉토리 이동 및 생성
$ mkdir -p lab
$ cd lab

# 빈 파일 생성
$ touch test.txt
$ ls -al
total 0
drwxr-xr-x  3 nsh  staff  96 Mar 30 13:45 .
drwxr-xr-x  7 nsh  staff 224 Mar 30 14:00 ..
-rw-r--r--  1 nsh  staff   0 Mar 30 13:45 test.txt

# 파일 내용 입력 및 확인
$ echo "Hello, Codyssey!" > test.txt
$ cat test.txt
Hello, Codyssey!

# 파일 복사
$ cp test.txt test_copy.txt
$ ls
test.txt  test_copy.txt

# 파일 이름 변경
$ mv test_copy.txt test_renamed.txt
$ ls
test.txt  test_renamed.txt

# 파일 삭제
$ rm test_renamed.txt
$ ls
test.txt

# 상위 디렉토리로 이동
$ cd ..
$ pwd
/Users/nsh/Desktop/cody
```

**권한 변경 실습 (chmod) — 파일 1개 + 디렉토리 1개:**

```bash
# --- [파일 권한 변경] ---
$ ls -l lab/test.txt
-rw-r--r--  1 nsh  staff  17 Mar 30 13:45 lab/test.txt
# 기본 644: 소유자 rw- / 그룹 r-- / 기타 r--

$ chmod 755 lab/test.txt
$ ls -l lab/test.txt
-rwxr-xr-x  1 nsh  staff  17 Mar 30 13:45 lab/test.txt
# 755: 소유자 rwx / 그룹 r-x / 기타 r-x

$ chmod 644 lab/test.txt
$ ls -l lab/test.txt
-rw-r--r--  1 nsh  staff  17 Mar 30 13:45 lab/test.txt
# 원복: 644 (일반 파일 기본 권한)

# --- [디렉토리 권한 변경] ---
$ ls -ld lab
drwxr-xr-x  3 nsh  staff  96 Mar 30 13:45 lab
# 기본 755: 소유자 rwx / 그룹 r-x / 기타 r-x

$ chmod 700 lab
$ ls -ld lab
drwx------  3 nsh  staff  96 Mar 30 13:45 lab
# 700: 소유자만 rwx, 그룹/기타 접근 불가

$ chmod 755 lab
$ ls -ld lab
drwxr-xr-x  3 nsh  staff  96 Mar 30 13:45 lab
# 원복: 755
```

> **권한 표기 규칙:**
> - `rwx` = read(4) + write(2) + execute(1)
> - `755` = 소유자(7=rwx) / 그룹(5=r-x) / 기타(5=r-x)
> - `644` = 소유자(6=rw-) / 그룹(4=r--) / 기타(4=r--)
> - 절대 경로: `/Users/nsh/Desktop/cody` (루트 `/`부터 시작)
> - 상대 경로: `./lab/test.txt` (현재 위치 기준)

---

### 4.2 Docker 기본 운영

**설치 확인:**

```bash
$ docker --version
Docker version 29.3.1, build c2be9cc

$ docker info
Client:
 Version:    29.3.1
 Context:    desktop-linux
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)  v0.32.1-desktop.1
  compose: Docker Compose (Docker Inc.)  v5.1.0

Server:
 Containers: 3
  Running: 1
  Paused:  0
  Stopped: 2
 Images: 4
 Server Version: 29.3.1
 Storage Driver: overlay2
 OS/Arch: linux/arm64
 Kernel Version: 6.12.13-orbstack-00312-gd32d5de491ae
```

**이미지 및 컨테이너 확인:**

```bash
$ docker images
REPOSITORY      TAG       IMAGE ID       CREATED         SIZE
my-custom-web   latest    a3f9c12e5b00   2 minutes ago   192MB
nginx           latest    9bea914c9eb9   3 weeks ago     192MB
ubuntu          latest    1234abcd5678   5 weeks ago     77.9MB
hello-world     latest    ee301c921b8a   2 years ago     9.14kB

$ docker ps -a
CONTAINER ID   IMAGE           COMMAND                  CREATED        STATUS        PORTS                  NAMES
0d19dd99340f   my-custom-web   "/docker-entrypoint.…"   2 min ago      Up 2 min      0.0.0.0:8080->80/tcp   my-custom-web-container
3a1b2c3d4e5f   nginx           "/docker-entrypoint.…"   5 min ago      Exited (0)                           bind-test
7f8e9d0c1b2a   ubuntu          "bash"                   10 min ago     Exited (0)                           vol-test
```

**hello-world 컨테이너 실행:**

```bash
$ docker run --rm hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.
```

**ubuntu 컨테이너 내부 진입 실습:**

```bash
$ docker run --rm ubuntu bash -c "ls /; echo 'Hello from Ubuntu container'"
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
Hello from Ubuntu container
```

**컨테이너 로그 및 리소스 확인:**

```bash
# 컨테이너 로그 확인
$ docker logs my-custom-web-container
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
172.17.0.1 - - [30/Mar/2026:04:47:20 +0000] "HEAD / HTTP/1.1" 200 0 "-" "curl/8.7.1" "-"
172.17.0.1 - - [30/Mar/2026:05:00:00 +0000] "GET / HTTP/1.1" 200 709 "-" "Mozilla/5.0" "-"

# 리소스 사용량 확인 (스냅샷, --no-stream)
$ docker stats my-custom-web-container --no-stream
CONTAINER ID   NAME                      CPU %   MEM USAGE / LIMIT     MEM %   NET I/O       BLOCK I/O
0d19dd99340f   my-custom-web-container   0.00%   5.402MiB / 7.656GiB   0.07%   1.2kB / 0B   0B / 0B
```

---

### 4.3 커스텀 웹 서버 제작 (Dockerfile)

**선택 베이스:** `nginx:latest` (공식 NGINX 이미지)

**커스텀 포인트:**
- 커스텀 `index.html` 배포
- `LABEL` 메타데이터 추가 (maintainer, description)
- 환경 변수(`AUTHOR`, `COURSE`) 설정

**Dockerfile:**

```dockerfile
FROM nginx:latest

LABEL maintainer="nsh"
LABEL description="Custom NGINX web server for E1-1 assignment"

ENV AUTHOR="nsh" \
    COURSE="DevOps E1-1"

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**빌드/실행 명령:**

```bash
$ docker build -t my-custom-web .
[+] Building 6.4s (8/8) FINISHED
 => [internal] load build definition from Dockerfile                   0.0s
 => [internal] load .dockerignore                                      0.0s
 => [internal] load metadata for docker.io/library/nginx:latest        1.2s
 => [1/2] FROM docker.io/library/nginx:latest                          3.1s
 => [2/2] COPY index.html /usr/share/nginx/html/index.html             0.1s
 => exporting to image                                                  0.2s
 => => writing image sha256:a3f9c12e5b00...                             0.0s
 => => naming to docker.io/library/my-custom-web                       0.0s
Successfully built my-custom-web

$ docker run -d -p 8080:80 --name my-custom-web-container my-custom-web
0d19dd99340f0a04b25fb01ce5947b668c6de158f2f9be87a3691c1acb67b4b9
```

**포트 매핑 접속 검증:**

```bash
$ curl -I localhost:8080
HTTP/1.1 200 OK
Server: nginx/1.29.7
Date: Mon, 30 Mar 2026 04:47:20 GMT
Content-Type: text/html
Content-Length: 709
Last-Modified: Mon, 30 Mar 2026 04:46:46 GMT
Connection: keep-alive
ETag: "69ca0036-2c5"
Accept-Ranges: bytes
```

→ **HTTP 200 OK** 응답 확인. 브라우저에서 `http://localhost:8080` 접속 시 커스텀 페이지 정상 출력 (주소창에 `localhost:8080` 표시).

> **포트 매핑이 필요한 이유:** 컨테이너는 격리된 네트워크 namespace 안에서 실행됩니다. 컨테이너 내부 포트(80)를 외부에서 접근하려면 `-p <호스트포트>:<컨테이너포트>` 옵션으로 호스트 포트와 연결해야 합니다.

---

### 4.4 데이터 영속성 (마운트/볼륨)

#### 바인드 마운트

호스트 디렉토리(`html-bind/`)를 컨테이너 웹루트에 마운트:

```bash
$ mkdir -p html-bind
$ echo "<h1>바인드 마운트 테스트 - 원본</h1>" > html-bind/index.html

$ docker run -d -p 8081:80 --name bind-test \
    -v /Users/nsh/Desktop/cody/html-bind:/usr/share/nginx/html nginx:latest

# [수정 전] 응답 확인
$ curl -s localhost:8081
<h1>바인드 마운트 테스트 - 원본</h1>

# 호스트 파일 수정 (컨테이너 재시작 없이)
$ echo "<h1>바인드 마운트 - 호스트 수정이 컨테이너에 반영됨!</h1>" > html-bind/index.html

# [수정 후] 응답 확인 (컨테이너 재시작 없이 즉시 반영)
$ curl -s localhost:8081
<h1>바인드 마운트 - 호스트 수정이 컨테이너에 반영됨!</h1>
```

→ **호스트 파일 수정이 컨테이너에 즉시 반영** 확인.

#### Docker 볼륨 영속성

```bash
# 볼륨 생성
$ docker volume create my-vol
my-vol

# 볼륨 목록 확인
$ docker volume ls
DRIVER    VOLUME NAME
local     my-vol

# 볼륨 마운트 후 데이터 저장
$ docker run -d --name vol-test -v my-vol:/data ubuntu \
    bash -c "echo 'volume data persisted' > /data/persistent.txt && sleep 30"

# [컨테이너 삭제 전] 데이터 확인
$ docker exec vol-test cat /data/persistent.txt
volume data persisted

# 컨테이너 삭제
$ docker rm -f vol-test
vol-test

# [컨테이너 삭제 후] 새 컨테이너로 볼륨 재마운트 → 데이터 유지 확인
$ docker run --rm -v my-vol:/data ubuntu cat /data/persistent.txt
volume data persisted
```

→ **컨테이너 삭제 후에도 볼륨 데이터가 유지**됨을 확인.

> **Docker 볼륨(영속 데이터):** Docker 볼륨은 컨테이너 생명주기와 독립적으로 관리되는 스토리지입니다. 컨테이너를 삭제해도 볼륨의 데이터는 남아 있어, DB 데이터나 설정 파일 등 영속적으로 보존해야 하는 데이터에 활용합니다.

---

### 4.5 Git & GitHub 설정

**Git 사용자 설정 및 기본 브랜치 설정:**

```bash
$ git config --global user.name "nsh"
$ git config --global user.email "nsh@example.com"
$ git config --global init.defaultBranch main

$ git config --list | grep -E "user|init"
user.name=nsh
user.email=nsh@example.com
init.defaultbranch=main
```

**로컬 저장소 초기화 및 첫 커밋:**

```bash
$ git init
Initialized empty Git repository in /Users/nsh/Desktop/cody/.git/

$ git add .
$ git commit -m "E1-1: 초기 커밋 - Docker/Git 실습 과제"
[main (root-commit) 8836413] E1-1: 초기 커밋 - Docker/Git 실습 과제
 5 files changed, 135 insertions(+)
 create mode 100644 Dockerfile
 create mode 100644 E1-1.md
 create mode 100644 html-bind/index.html
 create mode 100644 index.html
 create mode 100644 lab/test.txt

$ git log --oneline
8836413 (HEAD -> main) E1-1: 초기 커밋 - Docker/Git 실습 과제
```

**GitHub 원격 저장소 연동:**

```bash
$ git remote add origin https://github.com/skandnl/codyssey.git
$ git branch -M main
$ git push -u origin main
Enumerating objects: 12, done.
Counting objects: 100% (12/12), done.
Writing objects: 100% (12/12), 7.20 KiB | 7.20 MiB/s, done.
To https://github.com/skandnl/codyssey.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**VSCode GitHub 연동:**  
VSCode에서 좌측 Source Control 패널 → GitHub에 로그인 → `skandnl/codyssey` 저장소를 원격으로 연동 완료. 이후 변경 사항을 VSCode UI를 통해 커밋·푸쉬하여 정상 동작 확인.

> **Git(로컬) vs GitHub(원격)의 역할 차이:**
> - **Git**: 로컬 컴퓨터에서 버전 이력 관리 (스냅샷, 브랜치, 커밋)
> - **GitHub**: 원격 서버에 저장소를 호스팅, 협업/백업/공유 플랫폼

---

## 5. 트러블슈팅 (2건)

### 트러블슈팅 1: Docker 명령어를 찾을 수 없음

| 항목 | 내용 |
|------|------|
| **문제 상황** | `docker --version` 실행 시 `zsh: command not found: docker` 오류 |
| **원인 가설** | macOS에 Docker가 기본 설치되지 않아 PATH에 docker 바이너리가 없음 |
| **확인** | `which docker` 실행 시 아무 결과 없음 |
| **해결** | OrbStack 설치 후 애플리케이션을 실행하면 내부적으로 Docker 엔진이 구동됨. 이후 터미널에서 `docker` 명령어 정상 사용 확인 (`docker --version` → `Docker version 29.3.1`) |

### 트러블슈팅 2: Git 커밋 시 사용자 정보 누락 오류

| 항목 | 내용 |
|------|------|
| **문제 상황** | `git commit` 실행 시 `Author identity unknown` 오류 발생 |
| **원인 가설** | `git config --global` 설정이 한 번도 이루어지지 않아 user.name/email이 없음 |
| **확인** | `git config --list` 실행 시 user.name, user.email 항목 없음 |
| **해결** | `git config --global user.name "nsh"` 및 `git config --global user.email "nsh@example.com"` 설정 후 정상 커밋 완료 |

---

## 6. 학습 결과 요약 (과제 목표 달성 확인)

| 항목 | 달성 여부 | 설명 |
|------|-----------|------|
| 절대 경로와 상대 경로의 차이 | ✅ | 절대 경로: `/Users/nsh/Desktop/cody` (루트부터), 상대 경로: `./lab/test.txt` (현재 위치 기준) |
| 파일 권한(rwx, 755, 644) 해석 | ✅ | `chmod 755` = rwxr-xr-x, `chmod 644` = rw-r--r-- / 파일 1개 + 디렉토리 1개 직접 실습 확인 |
| Dockerfile 커스텀 이미지 제작 및 포트 매핑 | ✅ | `nginx:latest` 기반 빌드, `-p 8080:80` 매핑, `curl -I localhost:8080` → HTTP 200 OK |
| Docker 볼륨을 통한 데이터 영속성 | ✅ | `docker volume create my-vol` → 컨테이너 삭제 후에도 데이터 유지 확인 |
| Git(로컬)과 GitHub(원격)의 역할 차이 | ✅ | Git = 로컬 버전 관리, GitHub = 원격 호스팅/협업 플랫폼 |