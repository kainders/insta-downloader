from flask import Flask, render_template, request, send_file
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
    
    # 다운로드 파일 경로 설정
    download_path = 'downloads/'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
    }

    try:
        # yt-dlp로 영상 다운로드
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            filename = ydl.prepare_filename(info)
            filename_only = os.path.basename(filename)

        # 다운로드가 완료되면 그 파일을 클라이언트로 전송
        return send_file(os.path.join(download_path, filename_only), as_attachment=True)

    except Exception as e:
        return f"❌ 다운로드 중 오류 발생: {e}"

if __name__ == '__main__':
    app.run(debug=True)
