import requests
import json
from datetime import datetime

def get_atheer_ultimate_data():
    # مفاتيحك من الصورة (تأكد أنها لم تتغير)
    API_KEY = "GYkTTE95YM1sCMsX"
    API_SECRET = "cdB4MZniIbltsK9n43gJdnHCsa0eAXs"
    
    # الحصول على تاريخ اليوم (yyyy-mm-dd)
    today = datetime.now().strftime("%Y-%m-%d")
    
    matches_list = []

    try:
        # 📡 سنطلب "كل" مباريات اليوم المتاحة في حسابك
        url = f"https://live-score-api.com/api/client/fixtures/matches.json?key={API_KEY}&secret={API_SECRET}&date={today}"
        
        print(f"📡 جاري الطلب من الرابط: {url}")
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            # فحص هيكلة البيانات
            fixtures = data.get('data', {}).get('fixtures', [])
            
            if not fixtures:
                print("⚠️ السيرفر أعاد قائمة فارغة، قد تحتاج لتفعيل الدوريات في لوحة تحكم الموقع.")
            
            for f in fixtures:
                matches_list.append({
                    "date": today,
                    "league": f.get('competition', {}).get('name', 'League'),
                    "teamA": f.get('home_name'),
                    "teamB": f.get('away_name'),
                    "logoA": f"https://live-score-api.com/api/client/teams/logo.json?id={f.get('home_id')}&key={API_KEY}&secret={API_SECRET}",
                    "logoB": f"https://live-score-api.com/api/client/teams/logo.json?id={f.get('away_id')}&key={API_KEY}&secret={API_SECRET}",
                    "score": "vs",
                    "time": f.get('time', '00:00')[:-3],
                    "status": "timed",
                    "broadcasts": [{"channel": "beIN Sports", "commentator": "جاري التحديث"}]
                })
        else:
            print(f"❌ خطأ من السيرفر: {response.status_code}")
            
        return matches_list

    except Exception as e:
        print(f"🚨 حدث خطأ برمي: {e}")
        return []

if __name__ == "__main__":
    results = get_atheer_ultimate_data()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": results,
        "custom_ad": {"is_active": False}
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
        
    print(f"🏁 تم الانتهاء. عدد المباريات المضافة: {len(results)}")
