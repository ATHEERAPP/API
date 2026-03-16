import requests
import json
from datetime import datetime

def get_atheer_pro_data():
    # مفاتيحك الشخصية من الصورة
    API_KEY = "GYkTTE95YM1sCMsX"
    API_SECRET = "cdB4MZniIbltsK9n43gJdnHCsa0eAXs"
    
    # 🎯 الرابط المعتمد في الـ Documentation الذي أرسلته
    url = f"https://livescore-api.com/api-client/scores/live.json?key={API_KEY}&secret={API_SECRET}"
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    matches_list = []

    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            
            # التأكد من نجاح الطلب (success: true)
            if res_json.get('success'):
                # الوصول للمباريات: data -> match
                matches_data = res_json.get('data', {}).get('match', [])
                
                # إذا كانت القائمة فارغة، نجرب جلب الجدول (Fixtures) بنفس التنسيق
                if not matches_data:
                    url_fix = f"https://livescore-api.com/api-client/fixtures/matches.json?key={API_KEY}&secret={API_SECRET}"
                    res_json = requests.get(url_fix, timeout=20).json()
                    matches_data = res_json.get('data', {}).get('fixtures', [])

                for m in matches_data:
                    # ممرات البيانات تختلف بين المباشر والجدول، سنعالجها بذكاء:
                    is_live = 'scores' in m
                    
                    matches_list.append({
                        "date": today_str,
                        "league": m.get('competition', {}).get('name') if is_live else m.get('competition_name'),
                        "teamA": m.get('home', {}).get('name') if is_live else m.get('home_name'),
                        "teamB": m.get('away', {}).get('name') if is_live else m.get('away_name'),
                        "logoA": m.get('home', {}).get('logo') if is_live else f"https://cdn.live-score-api.com/teams/{m.get('home_id')}.png",
                        "logoB": m.get('away', {}).get('logo') if is_live else f"https://cdn.live-score-api.com/teams/{m.get('away_id')}.png",
                        "score": m.get('scores', {}).get('score', 'vs') if is_live else "vs",
                        "time": m.get('time', '00:00'),
                        "status": "live" if is_live and m.get('status') == "IN PLAY" else "timed",
                        "broadcasts": [{"channel": "beIN Sports", "commentator": "جاري التحديث"}]
                    })
            
        return matches_list
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    final_data = get_atheer_pro_data()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": final_data,
        "custom_ad": {"is_active": False}
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ تم التحديث! وجدنا {len(final_data)} مباراة.")
