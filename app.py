from flask import Flask, request, send_file, redirect, url_for, render_template
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def srt_to_txt(srt_path, txt_path):
    with open(srt_path, 'r', encoding='utf-8') as srt_file:
        lines = srt_file.readlines()

    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        subtitle_text = []
        for line in lines:
            line = line.strip()
            if line and not (line[0].isdigit() or '-->' in line):  # Skip timestamp and index lines
                subtitle_text.append(line)
            elif subtitle_text:
                txt_file.write(' '.join(subtitle_text) + '\n')
                subtitle_text = []
        
        # Write the last subtitle block if there is any remaining
        if subtitle_text:
            txt_file.write(' '.join(subtitle_text) + '\n')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.srt'):
        srt_path = os.path.join(UPLOAD_FOLDER, file.filename)
        txt_path = os.path.join(PROCESSED_FOLDER, file.filename.replace('.srt', '.txt'))
        file.save(srt_path)
        srt_to_txt(srt_path, txt_path)
        return send_file(txt_path, as_attachment=True, attachment_filename=file.filename.replace('.srt', '.txt'))

    return redirect(request.url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
