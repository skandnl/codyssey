
from flask import Flask

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# 루트 URL('/')에 대한 라우트를 정의
@app.route("/")
def hello_world():
    """루트 URL 접속 시 "Hello, DevOps!" 문자열을 반환합니다."""
    return "Hello, DevOps!"

# 이 스크립트가 직접 실행될 때만 웹 서버를 구동
if __name__ == "__main__":
    # 모든 네트워크 인터페이스에서 접속 가능하도록 host를 '0.0.0.0'으로 설정하고l
    # 포트 번호를 8080으로 지정하여 서버 실행
    app.run(host="0.0.0.0", port=8080,debug=True)