from flask import Flask, render_template, request
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']

    # URL이 비어 있으면 다운로드 시도하지 않기
    if not url.strip():
        return "❌ URL을 입력해주세요!"

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        filename = ydl.prepare_filename(info)
        filename_only = os.path.basename(filename)

    return render_template('result.html', filename=filename_only)

# ✅ 여기에 위치해야 해!!
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# ✅ 마지막에 이거!
if __name__ == '__main__':
    app.run(debug=True)
