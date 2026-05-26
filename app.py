from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Vercelは読み取り専用システムのため、LOG_FILEへのファイル書き込み（open関数）を完全に廃止しました。

def write_log(action_type, details=""):
    """ログ内容をファイルではなく、VercelのLogs画面へ標準出力（print）する関数"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    log_line = f"[{now}] [IP: {ip_address}] [{action_type}] {details}"
    print(log_line)

@app.route('/')
def home():
    write_log("PAGE_VIEW", "ホームページが読み込まれました")

    today = datetime.now().date()
    current_year = today.year
    
    # 【生年月日設定】2006年3月4日生まれのRM様が次に迎える誕生日（21歳）の設定
    BIRTH_MONTH = 3
    BIRTH_DAY = 4
    TARGET_AGE = 21
    
    # 今年の誕生日を定義
    next_birthday = datetime(current_year, BIRTH_MONTH, BIRTH_DAY).date()
    
    # 2026年の誕生日はすでに過ぎているため、自動的にターゲットを「2027年3月4日」に補正
    if today > next_birthday:
        next_birthday = datetime(current_year + 1, BIRTH_MONTH, BIRTH_DAY).date()
    
    # 2027年3月4日までの残り日数を正確に自動計算
    days_left = (next_birthday - today).days
    
    profile_data = {
        "name": "RM",
        "gear": "MacBook Air",
        "target_age": TARGET_AGE,   # 🌟 確実に格納を修正：HTML側へ21歳を伝達
        "days_left": days_left,     # 🌟 確実に格納を修正：HTML側へ計算された残り日数を伝達
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
                "urls": []
            },
            {
                "category": "dev",
                "tag": "Development",
                "title": "💻 Pythonアプリ開発",
                "desc": "Flaskフレームワークを用いたWebツールの作成や、スクリプトによるデータ自動処理。",
                "urls": [
                    {"label": "🍽️ 調布グルメforUEC", "url": "https://chohu-dish.vercel.app"}
                ]
            },
            {
                "category": "other",
                "tag": "Martial Arts",
                "title": "🥋 武道",
                "desc": "心身の練成と技術向上に努めています。大学での広報活動も兼任。",
                "urls": [
                    {"label": "電通大合気道部🥋公式X", "url": "https://x.com/uec_aikido"}
                ]
            },
            {
                "category": "friends",
                "tag": "UEC Friends",
                "title": "🤝 電通大相互リンク",
                "desc": "同じ学内や個人開発で切磋琢磨している人達のホームページリンク集です。",
                "urls": [
                    {"label": "柴犬被り", "url": "https://memo.shibadogcap.com", "icon": "/static/shiba.jpeg"},
                    {"label": "しおり🔖", "url": "https://shiori-02-14.github.io/Homepage/index.html", "icon": "/static/shiori.jpeg"},
                    {"label": "トラマト", "url": "https://toramutton.me", "icon": "/static/toramato.jpeg"},
                    {"label": "ぽりとす", "url": "https://polythos.net", "icon": "/static/poritosu.jpeg"}
                ]
            }
        ],
        
        "history": [
            {"year": "2021年", "event": "明治学院高校入学"},
            {"year": "2024年", "event": "自宅入学(宅浪)"},
            {"year": "2025年", "event": "電気通信大学入学"},
            {"year": "2026年", "event": "合気道部広報担当になる"},
            {"year": "2026年", "event": "Webサイト『調布グルメ検索forUEC』を開発"}
        ],

        "skills": [
            {"name": "Python / Flask", "level": 30},
            {"name": "デジタルイラスト", "level": 50},
            {"name": "合気道", "level": 20}
        ],

        # 🌟 追加：ギャラリー用データ（※画像はstatic内に配置してください）
        "gallery_images": [
            {"title": "魔法少女ノ魔女裁判『桜羽エマ』", "url": "/static/art1.jpeg"},
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