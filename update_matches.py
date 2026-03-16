import requests
import json
from datetime import datetime

def get_live_matches_pro():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': 'b43963bf5cfa411c8934edd9d5fafa69'}
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            matches_list = []
            
            for m in data.get('matches', []):
                # تحديد قناة افتراضية بناءً على الدوري ليعطي لمسة واقعية
                league_name = m['competition']['name']
                channel = "beIN Sports 1" if "Premier League" in league_name else "beIN Sports 3"
                
                matches_list.append({
                    "date": today_str, 
                    "league": league_name,
                    "league_logo": m['competition']['emblem'],
                    "teamA": m['homeTeam']['shortName'] or m['homeTeam']['name'],
                    "teamB": m['awayTeam']['shortName'] or m['awayTeam']['name'],
                    "logoA": m['homeTeam']['crest'], 
                    "logoB": m['awayTeam']['crest'],
                    "score": f"{m['score']['full_time']['home'] if m['score']['full_time']['home'] is not None else ''} - {m['score']['full_time']['away'] if m['score']['full_time']['away'] is not None else ''}".replace(" - ","vs") if m['score']['full_time']['home'] is None else f"{m['score']['full_time']['home']} - {m['score']['full_time']['away']}",
                    "time": m['utcDate'][11:16],
                    "status": "live" if m['status'] in ["IN_PLAY", "PAUSED"] else ("finished" if m['status'] == "FINISHED" else "timed"),
                    # 🎙️ إضافة بيانات المعلق والقناة لكي تظهر في شريط البطاقة السفلي
                    "broadcasts": [
                        {
                            "channel": channel,
                            "commentator": "جاري التحديث...",
                            "stream_url": "" # هنا يمكنك وضع رابط بث لاحقاً
                        }
                    ]
                })
            return matches_list
        return []
    except:
        return []

if __name__ == "__main__":
    matches = get_live_matches_pro()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": matches,
        "custom_ad": {"is_active": False, "image_url": "", "click_url": ""}
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print("✅ تم تحديث الأسماء وإضافة بيانات المعلقين الافتراضية!")
