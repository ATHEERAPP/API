import requests
import json
from datetime import datetime

def get_atheer_pro_data():
    # مفاتيحك من الصورة
    API_KEY = "GYkTTE95YM1sCMsX"
    API_SECRET = "cdB4MZniIbltsK9n43gJdnHCsa0eAXs"
    
    # 📡 سنستخدم رابط الـ SCORES لجلب الأهداف الحية والمباريات الجارية
    url = f"https://live-score-api.com/api/client/scores/live.json?key={API_KEY}&secret={API_SECRET}"
    
    today_str = datetime.now().strftime("%Y-%m-%d")

    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            data = response.json()
            matches_list = []
            
            # الموقع يضع المباريات الحية في ['data']['match']
            live_matches = data.get('data', {}).get('match', [])
            
            for m in live_matches:
                matches_list.append({
                    "date": today_str,
                    "league": m.get('competition', {}).get('name', 'بطولة'),
                    "league_logo": "", # الـ API يوفر روابط الصور في ملفات منفصلة، سنضعها يدوياً لو أردت
                    "teamA": m.get('home_name'),
                    "teamB": m.get('away_name'),
                    "logoA": f"https://live-score-api.com/api/client/teams/logo.json?id={m.get('home_id')}&key={API_KEY}&secret={API_SECRET}",
                    "logoB": f"https://live-score-api.com/api/client/teams/logo.json?id={m.get('away_id')}&key={API_KEY}&secret={API_SECRET}",
                    "score": m.get('score', 'vs'), # هنا تظهر النتيجة الحية (1-0)
                    "time": m.get('time', '00:00'), # هنا يظهر وقت المباراة الحالي
                    "status": "live" if m.get('status') == "IN_PLAY" else "timed",
                    "broadcasts": [
                        {
                            "channel": "beIN Sports",
                            "commentator": "جاري التحديث..."
                        }
                    ]
                })
            
            # 💡 إذا كانت القائمة فارغة (لا توجد مباريات حية)، نجلب الجدول (Fixtures)
            if not matches_list:
                fix_url = f"https://live-score-api.com/api/client/fixtures/matches.json?key={API_KEY}&secret={API_SECRET}"
                fix_res = requests.get(fix_url, timeout=20)
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
                            "time": f.get('time', '00:00')[:-3],
                            "status": "timed",
                            "broadcasts": [{"channel": "beIN Sports", "commentator": "معلق المباراة"}]
                        })
            
            return matches_list
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    final_matches = get_atheer_pro_data()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": final_matches,
        "custom_ad": {"is_active": False}
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ تم بنجاح! وجدنا {len(final_matches)} مباراة.")
