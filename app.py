from flask import Flask, render_template_string, request, redirect
import subprocess

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مركز تحكم موسيقى الـ Pi</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: white; text-align: center; padding: 30px 10px; margin: 0; }
        .container { max-width: 450px; margin: auto; background: #1e1e1e; padding: 25px; border-radius: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); }
        h1 { color: #1DB954; font-size: 24px; margin-bottom: 20px; }
        input[type="text"] { width: 90%; padding: 12px; border: 2px solid #333; border-radius: 8px; margin-bottom: 15px; font-size: 15px; text-align: center; background: #2a2a2a; color: white; }
        input[type="text"]:focus { border-color: #1DB954; outline: none; }
        .play-btn { background-color: #1DB954; color: white; border: none; padding: 14px; font-size: 16px; border-radius: 30px; cursor: pointer; width: 95%; font-weight: bold; margin-bottom: 25px; transition: 0.2s; }
        .play-btn:hover { background-color: #1ed760; }
        .controls-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 15px; }
        .control-btn { background-color: #333; color: white; border: none; padding: 12px; font-size: 15px; border-radius: 10px; cursor: pointer; transition: 0.2s; font-weight: 500; }
        .control-btn:hover { background-color: #444; }
        .stop-btn { background-color: #e91429; grid-column: span 2; }
        .stop-btn:hover { background-color: #ff2a3b; }
        .footer { margin-top: 25px; font-size: 11px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 مركز التحكم بالصوتيات</h1>
        
        <form method="POST" action="/play">
            <input type="text" name="url" placeholder="إلصق رابط يوتيوب هنا..." required>
            <button type="submit" class="play-btn">▶ تشغيل مقطع جديد</button>
        </form>
        
        <div class="controls-grid">
            <button class="control-btn" onclick="sendCmd('pause')">⏸ إيقاف مؤقت / استئناف</button>
            <button class="control-btn" onclick="sendCmd('mute')">🔇 كتم / إلغاء الكتم</button>
            <button class="control-btn" onclick="sendCmd('vol-up')">🔊 رفع الصوت (+)</button>
            <button class="control-btn" onclick="sendCmd('vol-down')">🔉 خفض الصوت (-)</button>
            <button class="control-btn control-btn stop-btn" onclick="sendCmd('stop')">⏹ إيقاف نهائي</button>
        </div>
        
        <div class="footer">التحكم الذكي مفعّل عبر شبكتك المحلية</div>
    </div>

    <script>
        function sendCmd(action) {
            fetch('/control/' + action, { method: 'POST' });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/play', methods=['POST'])
def play():
    url = request.form.get('url')
    if url:
        # إيقاف أي تشغيل قديم لتجنب تداخل الأصوات
        subprocess.run(["pkill", "mpv"])
        # تشغيل المقطع عبر أمرك السلس مع فتح مخرجات التحكم الداخلي
        subprocess.Popen(["mpv", "--no-video", "--input-ipc-server=/tmp/mpv-socket", url])
    return redirect('/')

@app.route('/control/<action>', methods=['POST'])
def control(action):
    # التحكم بالإيقاف والاستئناف
    if action == 'pause':
        subprocess.run(["echo 'cycle pause' | socat - /tmp/mpv-socket"], shell=True)
    # كتم الصوت
    elif action == 'mute':
        subprocess.run(["echo 'cycle mute' | socat - /tmp/mpv-socket"], shell=True)
    # رفع الصوت بمقدار 10 درجات مباشرة داخل المقطع
    elif action == 'vol-up':
        subprocess.run(["echo 'add volume 10' | socat - /tmp/mpv-socket"], shell=True)
    # خفض الصوت بمقدار 10 درجات مباشرة داخل المقطع
    elif action == 'vol-down':
        subprocess.run(["echo 'add volume -10' | socat - /tmp/mpv-socket"], shell=True)
    # الإنهاء الكامل للمشغل
    elif action == 'stop':
        subprocess.run(["pkill", "mpv"])
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
