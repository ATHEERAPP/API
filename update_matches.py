import requests
import json
from datetime import datetime

def get_live_score_api_data():
    # المفاتيح من صورتك الشخصية
    API_KEY = "GYkTTE95YM1sCMsX"
    API_SECRET = "cdB4MZniIbltsK9n43gJdnHCsa0eAXs"
    
    # رابط جلب مباريات اليوم
    url = f"https://live-score-api.com/api/client/fixtures/matches.json?key={API_KEY}&secret={API_SECRET}"
    
    today_str = datetime.now().strftime("%Y-%m-%d")

    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            data = response.json()
            matches_list = []
            
            # استخراج البيانات من الهيكلية الخاصة بالموقع
            fixtures = data.get('data', {}).get('fixtures', [])
            
            for m in fixtures:
                # إنشاء روابط الشعارات باستخدام الـ IDs
                home_id = m.get('home_id')
                away_id = m.get('away_id')
                comp_id = m.get('competition', {}).get('id')
                
                matches_list.append({
                    "date": today_str,
                    "league": m.get('competition', {}).get('name', 'بطولة'),
                    "league_logo": f"https://live-score-api.com/api/client/competitions/logo.json?id={comp_id}&key={API_KEY}&secret={API_SECRET}",
                    "teamA": m.get('home_name'),
                    "teamB": m.get('away_name'),
                    "logoA": f"https://live-score-api.com/api/client/teams/logo.json?id={home_id}&key={API_KEY}&secret={API_SECRET}",
                    "logoB": f"https://live-score-api.com/api/client/teams/logo.json?id={away_id}&key={API_KEY}&secret={API_SECRET}",
                    "score": "vs", # الجدولة لا تحتوي على نتائج حية، سنستخدمها كبداية
                    "time": m.get('time', '00:00')[:-3], # تنسيق الوقت HH:MM
                    "status": "timed",
                    "broadcasts": [
                        {
                            "channel": "beIN Sports",
                            "commentator": "معلق المباراة"
                        }
                    ]
                })
            return matches_list
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    matches = get_live_score_api_data()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": matches,
        "custom_ad": {"is_active": False, "image_url": "", "click_url": ""}
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ تم التحديث بنجاح! وجدنا {len(matches)} مباراة.")
