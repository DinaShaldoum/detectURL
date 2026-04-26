from flask import Flask, render_template, request, jsonify
import requests
import re
import string
import random

app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# فحص الموقع
@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    url = data.get('url', '')
    if not url.startswith('http'):
        url = 'https://' + url
    
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        security_headers = ['Content-Security-Policy', 'X-Frame-Options', 'Strict-Transport-Security']
        found_headers = [f"✅ {h} موجود" if h in headers else f"❌ {h} مفقود" for h in security_headers]
        
        rating = "آمن" if response.url.startswith('https') and len([h for h in security_headers if h in headers]) >= 1 else "ضعيف"
        
        return jsonify({"url": url, "https": response.url.startswith('https'), "headers": found_headers, "rating": rating})
    except:
        return jsonify({"error": "تعذر الاتصال بالموقع"})

# فحص كلمة المرور
@app.route('/check-password', methods=['POST'])
def check_pass():
    password = request.json.get('password', '')
    score = 0
    if len(password) >= 8: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[@$!%*?&]", password): score += 1
    
    levels = ["سيئة جداً", "ضعيفة", "متوسطة", "قوية", "ممتازة", "قوية جداً"]
    return jsonify({"score": score, "level": levels[score]})

# توليد كلمة مرور
@app.route('/generate-password', methods=['GET'])
def gen_pass():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for i in range(16))
    return jsonify({"password": password})

if __name__ == '__main__':
    app.run(debug=True)