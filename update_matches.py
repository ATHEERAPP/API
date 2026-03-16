import requests
import json
from datetime import datetime, timedelta

def get_football_data():
    # 🔑 مفتاحك الشخصي من موقع football-data.org
    API_KEY = "b43963bf5cfa411c8934edd9d5fafa69"
    
    # 📡 رابط جلب مباريات اليوم
    url = "https://api.football-data.org/v4/matches"
    
    headers = {
        'X-Auth-Token': API_KEY
    }

    try:
        print("📡 جاري الاتصال بسيرفرات football-data.org...")
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            matches_list = []
            today_str = datetime.now().strftime("%Y-%m-%d")

            matches = data.get('matches', [])
            
            for m in matches:
                competition = m.get('competition', {}).get('name', 'بطولة')

                home_team = m.get('homeTeam', {}).get('shortName', m.get('homeTeam', {}).get('name', 'فريق 1'))
                away_team = m.get('awayTeam', {}).get('shortName', m.get('awayTeam', {}).get('name', 'فريق 2'))
                
                # جلب الشعارات بجودة عالية (Crests)
                home_crest = m.get('homeTeam', {}).get('crest', 'https://cdn-icons-png.flaticon.com/512/1864/1864470.png')
                away_crest = m.get('awayTeam', {}).get('crest', 'https://cdn-icons-png.flaticon.com/512/1864/1864470.png')

                status = m.get('status')
                score_home = m.get('score', {}).get('fullTime', {}).get('home')
                score_away = m.get('score', {}).get('fullTime', {}).get('away')
                
                score_home = score_home if score_home is not None else 0
                score_away = score_away if score_away is not None else 0

                # ⏱️ تحليل حالة المباراة
                if status in ['IN_PLAY', 'PAUSED']:
                    match_status = "live"
                    score = f"{score_home} - {score_away}"
                    time_str = "مباشر"
                elif status == 'FINISHED':
                    match_status = "finished"
                    score = f"{score_home} - {score_away}"
                    time_str = "انتهت"
                else:
                    match_status = "timed"
                    score = "vs"
                    # تحويل التوقيت إلى توقيت الجزائر (UTC+1)
                    utc_date_str = m.get('utcDate', '')
                    if utc_date_str:
                        utc_time = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
                        local_time = utc_time + timedelta(hours=1) 
                        time_str = local_time.strftime("%H:%M")
                    else:
                        time_str = "00:00"

                matches_list.append({
                    "date": today_str,
                    "league": competition,
                    "teamA": home_team,
                    "teamB": away_team,
                    "logoA": home_crest,
                    "logoB": away_crest,
                    "score": score,
                    "time": time_str,
                    "status": match_status,
                    "broadcasts": [{"channel": "أثير الرياضي", "commentator": "تحديث تلقائي"}]
                })
                
            return matches_list
        else:
            print(f"❌ خطأ من السيرفر. كود الخطأ: {response.status_code}")
            return []

    except Exception as e:
        print(f"🚨 خطأ برمجي: {e}")
        return []

if __name__ == "__main__":
    final_data = get_football_data()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": final_data,
        "custom_ad": {"is_active": False}
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ تم سحب البيانات بنجاح! عدد المباريات: {len(final_data)}")
