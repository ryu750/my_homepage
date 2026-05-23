from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "access_log.txt"

def write_log(action_type, details=""):
    """ログファイルに日時、IPアドレス、行動内容を書き込む関数"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    log_line = f"[{now}] [IP: {ip_address}] [{action_type}] {details}"
    print(log_line)  # ファイルに保存せず、VercelのLogs画面にそのまま出力させる

@app.route('/')
def home():
    write_log("PAGE_VIEW", "ホームページが読み込まれました")
    
    profile_data = {
        "name": "RM",
        "gear": "MacBook Air",
        "sns": [
            {"name": "X (Twitter)", "url": "https://x.com/uecboy"},
            {"name": "GitHub", "url": "https://github.com/ryu750"},
            {"name": "Pixiv", "url": "https://www.pixiv.net/users/101635004"}
        ],
        "hobbies": ["デジタルイラスト制作", "プログラミング", "武道"],
        
        "works": [
            {
                "category": "art",
                "tag": "Art",
                "title": "👩‍🎨 デジタルイラスト制作",
                "desc": "ibis Paint Xを使用したキャラクターイラストや厚塗り・アニメ塗り、構図の模索。",
                "urls": [] # 🔗 リンクがない場合は空の配列にする
            },
            {
                "category": "dev",
                "tag": "Development",
                "title": "💻 Pythonアプリ開発",
                "desc": "Flaskフレームワークを用いたWebツールの作成や、スクリプトによるデータ自動処理。",
                "urls": [
                    {"label": "🍽️ 調布グルメforUEC", "url": "https://chohu-dish.vercel.app"}
                ] # 🔗 2つ、3つと、ここへ辞書形式で並べるだけで無限に増やせます！
            },
            {
                "category": "other",
                "tag": "Martial Arts",
                "title": "🥋 武道",
                "desc": "心身の練成と技術向上に努めています。大学での広報活動も兼任。",
                "urls": [
                    {"label": "電通大合気道部🥋公式X", "url": "https://x.com/home"}
                ]
            }
        ],
        
        "history": [
            {"year": "2021年", "event": "私立明治学院高等学校入学"},
            {"year": "2025年", "event": "電気通信大学入学"},
            {"year": "2026年", "event": "合気道部広報担当になる"},
            {"year": "2026年", "event": "Webサイト『調布グルメ検索forUEC』を開発"}
        ]
    }
    return render_template('index.html', data=profile_data)

@app.route('/api/log', methods=['POST'])
def save_log():
    """フロントエンドからの行動ログを受け取って保存するAPIエンドポイント"""
    try:
        data = request.get_json()
        action = data.get('action')
        details = data.get('details', '')
        
        if action:
            write_log(action, details)
            return jsonify({"status": "success"}), 200
        return jsonify({"status": "bad_request"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
