
from flask import Flask, request, Response
import os
from io import BytesIO
from gtts import gTTS

DEFAULT_LANG = os.getenv('DEFAULT_LANG', 'ko')
app = Flask(__name__)

@app.route("/")
def home():
    text = "Hello, DevOps"
    lang = request.args.get('lang', DEFAULT_LANG)

    fp = BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(fp)
    fp.seek(0)  # 처음부터 읽을 수 있도록

    return Response(fp.getvalue(), mimetype='audio/mpeg')  # 바로 음성 스트리밍

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
