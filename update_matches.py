import requests
import json
from datetime import datetime

def get_atheer_pro_data():
    # مفاتيحك من الصورة السابقة
    API_KEY = "GYkTTE95YM1sCMsX"
    API_SECRET = "cdB4MZniIbltsK9n43gJdnHCsa0eAXs"
    
    # رابط النتائج الحية (Live Scores) كما هو موضح في الدليل
    url = f"https://live-score-api.com/api-client/scores/live.json?key={API_KEY}&secret={API_SECRET}"
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    matches_list = []

    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            
            # حسب الدليل الذي أرسلته: البيانات تكون داخل success ثم data ثم match
            if res_json.get('success'):
                matches_data = res_json.get('data', {}).get('match', [])
                
                for m in matches_data:
                    matches_list.append({
                        "date": today_str,
                        "league": m.get('competition', {}).get('name', 'بطولة'),
                        "teamA": m.get('home', {}).get('name'), # الوصول للاسم داخل home
                        "teamB": m.get('away', {}).get('name'), # الوصول للاسم داخل away
                        "logoA": m.get('home', {}).get('logo'), # الرابط المباشر للشعار
                        "logoB": m.get('away', {}).get('logo'), # الرابط المباشر للشعار
                        "score": m.get('scores', {}).get('score', 'vs'), # النتيجة الحية
                        "time": m.get('time', '00'), # دقيقة المباراة
                        "status": "live" if m.get('status') == "IN PLAY" else "timed",
                        "broadcasts": [
                            {
                                "channel": "beIN Sports",
                                "commentator": "جاري التحديث..."
                            }
                        ]
                    })
            
            # إذا لم تكن هناك مباريات حية حالياً، ننتقل لجلب الجدول (Fixtures)
            if not matches_list:
                fix_url = f"https://live-score-api.com/api-client/fixtures/matches.json?key={API_KEY}&secret={API_SECRET}"
                fix_res = requests.get(fix_url, timeout=20)
                if fix_res.status_code == 200:
                    fix_json = fix_res.json()
                    fix_data = fix_json.get('data', {}).get('fixtures', [])
                    for f in fix_data:
                        matches_list.append({
                            "date": today_str,
                            "league": f.get('competition_name'),
                            "teamA": f.get('home_name'),
                            "teamB": f.get('away_name'),
                            "logoA": f"https://cdn.live-score-api.com/teams/{f.get('home_id')}.png", # تخمين رابط الشعار
                            "score": "vs",
                            "time": f.get('time', '00:00')[:-3],
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
    print(f"✅ تم التحديث بنجاح! وجدنا {len(data)} مباراة حية/مجدولة.")
