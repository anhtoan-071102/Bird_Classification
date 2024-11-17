from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from predict import predict

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tạo thư mục uploads nếu chưa có
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Trang chính cho phép tải lên hình ảnh
@app.route('/')
def home():
    return render_template('index.html')

# Xử lý hình ảnh tải lên và dự đoán
@app.route('/predict', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("No file part")
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        print("No selected file")
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(file_path)
        file.save(file_path)
        
        # Dự đoán loài chim từ hình ảnh
        result = predict(file_path)
        return render_template('result.html', filename=filename, result=result)

if __name__ == '__main__':
    app.run(debug=True)
