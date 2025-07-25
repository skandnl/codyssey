아래에 두 가지 보너스 과제 내용을 각각 정리해 드릴게요. 보고서나 과제 제출용으로 적합하도록 깔끔하게 작성했습니다.

---

# 보너스 과제 1: Flask와 Gunicorn의 차이 및 배포 시 Gunicorn 사용 이유

## 1. Flask와 Gunicorn의 차이

* **Flask**

  * Python으로 작성된 경량 웹 프레임워크이다.
  * 개발자가 웹 애플리케이션을 쉽게 만들 수 있도록 도와주는 라이브러리 및 도구들의 집합이다.
  * 기본 내장 웹 서버(`flask run` 또는 `app.run()`)는 개발 및 테스트용으로 적합하며, 프로덕션 환경에 적합하지 않다.

* **Gunicorn (Green Unicorn)**

  * Python WSGI(Web Server Gateway Interface) HTTP 서버이다.
  * Flask 같은 WSGI 애플리케이션을 빠르고 안정적으로 실행하기 위한 프로덕션용 웹 서버이다.
  * 다중 워커 프로세스를 지원해 높은 동시 처리량과 안정성을 제공한다.

## 2. 배포 시 Gunicorn을 사용하는 이유

* Flask 기본 서버는 **단일 스레드**로 동작하며, 고성능이나 다중 요청 처리를 위한 기능이 부족하다.
* Gunicorn은 **멀티 프로세스, 멀티 스레드**를 지원해 여러 클라이언트 요청을 동시에 처리할 수 있다.
* 안정성과 성능 최적화가 되어 있어 \*\*실제 서비스 환경(프로덕션)\*\*에 적합하다.
* Gunicorn을 앞단에 두고 Nginx 같은 리버스 프록시 서버와 연동하면 확장성과 보안성을 더욱 높일 수 있다.

---

# 보너스 과제 2: .dockerignore 파일의 역할과 각 항목 추가 이유

## 1. `.dockerignore` 파일의 역할

* `.dockerignore` 파일은 도커 이미지 빌드 시 **빌드 컨텍스트에 포함하지 않을 파일이나 디렉토리 목록**을 지정하는 파일이다.
* 이를 통해 빌드 속도를 향상시키고, 이미지 크기를 줄이며, 불필요한 파일이 컨테이너에 복사되는 것을 방지한다.
* 예를 들어, Git 버전관리 파일이나 도커 관련 설정 파일, 캐시 파일 등을 제외할 수 있다.

## 2. 각 항목 추가 이유

* **`.git`**

  * Git 저장소 관련 모든 버전관리 파일과 폴더이다.
  * 소스 코드 버전 관리에만 필요하고, 컨테이너 실행에는 불필요하므로 제외한다.

* **`.gitignore`**

  * Git에서 추적하지 않을 파일을 지정하는 설정 파일이다.
  * 컨테이너 내에서는 필요 없으며, 빌드 컨텍스트에서 제외해 빌드 속도를 개선한다.

* **`.dockerignore`**

  * 자기 자신도 빌드 컨텍스트에 포함하지 않아 불필요한 중복 복사를 방지한다.

* **`Dockerfile`**

  * 도커 빌드 시 `Dockerfile`은 빌드 명령어로 사용되기 때문에, 이미지 내부에는 복사할 필요가 없다.
  * 이미지 크기를 줄이고, 불필요한 파일 복사를 막기 위해 제외한다.

---


