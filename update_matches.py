import requests
import json
from datetime import datetime

def get_pro_data():
    # مفاتيحك الشخصية من الصورة
    API_KEY = "GYkTTE95YM1sCMsX"
    API_SECRET = "cdB4MZniIbltsK9n43gJdnHCsa0eAXs"
    
    # 📡 هذا الرابط يجلب "كل" النتائج المتاحة حالياً في حسابك بدون فلترة تاريخ
    url = f"https://live-score-api.com/api/client/scores/live.json?key={API_KEY}&secret={API_SECRET}"
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    matches_list = []

    try:
        response = requests.get(url, timeout=20)
        print(f"Status Code: {response.status_code}") # سيظهر لك في GitHub Actions
        
        if response.status_code == 200:
            data = response.json()
            # فحص أين توجد البيانات بالضبط
            match_data = data.get('data', {}).get('match', [])
            
            # إذا كان الرابط الأول فارغاً، نجرب رابط الجدولة كخطة بديلة
            if not match_data:
                alt_url = f"https://live-score-api.com/api/client/fixtures/matches.json?key={API_KEY}&secret={API_SECRET}"
                alt_res = requests.get(alt_url, timeout=20)
                match_data = alt_res.json().get('data', {}).get('fixtures', [])

            for m in match_data:
                # استخراج البيانات بمرونة
                matches_list.append({
                    "date": today_str,
                    "league": m.get('competition', {}).get('name', 'League'),
                    "teamA": m.get('home_name', m.get('home_name')),
                    "teamB": m.get('away_name', m.get('away_name')),
                    "logoA": f"https://live-score-api.com/api/client/teams/logo.json?id={m.get('home_id')}&key={API_KEY}&secret={API_SECRET}",
                    "logoB": f"https://live-score-api.com/api/client/teams/logo.json?id={m.get('away_id')}&key={API_KEY}&secret={API_SECRET}",
                    "score": m.get('score', 'vs'),
                    "time": m.get('time', '00:00'),
                    "status": "live" if "score" in m else "timed",
                    "broadcasts": [{"channel": "beIN Sports", "commentator": "جاري التحديث"}]
                })
        return matches_list
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    matches = get_pro_data()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": matches,
        "custom_ad": {"is_active": False}
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ تم الانتهاء! عدد المباريات: {len(matches)}")
