import requests
import json
from datetime import datetime

def get_atheer_pro_data():
    API_KEY = "GYkTTE95YM1sCMsX"
    API_SECRET = "cdB4MZniIbltsK9n43gJdnHCsa0eAXs"
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    matches_list = []

    try:
        # 1️⃣ المحاولة الأولى: جلب المباريات المباشرة (Live Scores)
        live_url = f"https://live-score-api.com/api/client/scores/live.json?key={API_KEY}&secret={API_SECRET}"
        live_res = requests.get(live_url, timeout=15)
        
        if live_res.status_code == 200:
            live_data = live_res.json().get('data', {}).get('match', [])
            if live_data:
                for m in live_data:
                    matches_list.append({
                        "date": today_str,
                        "league": m.get('competition', {}).get('name'),
                        "teamA": m.get('home_name'),
                        "teamB": m.get('away_name'),
                        "logoA": f"https://live-score-api.com/api/client/teams/logo.json?id={m.get('home_id')}&key={API_KEY}&secret={API_SECRET}",
                        "logoB": f"https://live-score-api.com/api/client/teams/logo.json?id={m.get('away_id')}&key={API_KEY}&secret={API_SECRET}",
                        "score": m.get('score', 'vs'),
                        "time": m.get('time', '00:00'),
                        "status": "live",
                        "broadcasts": [{"channel": "beIN Sports", "commentator": "مباشر"}]
                    })

        # 2️⃣ المحاولة الثانية: إذا كانت القائمة فارغة، نجلب جدول اليوم (Fixtures)
        if not matches_list:
            fix_url = f"https://live-score-api.com/api/client/fixtures/matches.json?key={API_KEY}&secret={API_SECRET}"
            fix_res = requests.get(fix_url, timeout=15)
            if fix_res.status_code == 200:
                fix_data = fix_res.json().get('data', {}).get('fixtures', [])
                for f in fix_data:
                    matches_list.append({
                        "date": today_str,
                        "league": f.get('competition', {}).get('name'),
                        "teamA": f.get('home_name'),
                        "teamB": f.get('away_name'),
                        "logoA": f"https://live-score-api.com/api/client/teams/logo.json?id={f.get('home_id')}&key={API_KEY}&secret={API_SECRET}",
                        "logoB": f"https://live-score-api.com/api/client/teams/logo.json?id={f.get('away_id')}&key={API_KEY}&secret={API_SECRET}",
                        "score": "vs",
                        "time": f.get('time', '00:00')[:-3], # تنسيق HH:MM
                        "status": "timed",
                        "broadcasts": [{"channel": "beIN Sports", "commentator": "معلق المباراة"}]
                    })

        return matches_list
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    data = get_atheer_pro_data()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": data,
        "custom_ad": {"is_active": False}
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"🚀 تم التحديث! وجدنا {len(data)} مباراة.")
