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
                # تصحيح مسار النتيجة (fullTime بدلاً من full_time)
                score_data = m.get('score', {}).get('fullTime', {})
                home_score = score_data.get('home')
                away_score = score_data.get('away')
                
                # تنسيق النتيجة لـ Flutter
                display_score = f"{home_score} - {away_score}" if home_score is not None else "vs"
                
                matches_list.append({
                    "date": today_str, 
                    "league": m['competition']['name'],
                    "league_logo": m['competition']['emblem'],
                    "teamA": m['homeTeam']['shortName'] or m['homeTeam']['name'],
                    "teamB": m['awayTeam']['shortName'] or m['awayTeam']['name'],
                    "logoA": m['homeTeam']['crest'], 
                    "logoB": m['awayTeam']['crest'],
                    "score": display_score,
                    "time": m['utcDate'][11:16],
                    "status": "live" if m['status'] in ["IN_PLAY", "PAUSED"] else ("finished" if m['status'] == "FINISHED" else "timed"),
                    "broadcasts": [
                        {
                            "channel": "beIN Sports",
                            "commentator": "جاري التحديث...",
                            "stream_url": "" 
                        }
                    ]
                })
            return matches_list
        return []
    except Exception as e:
        print(f"Error: {e}")
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
    print(f"✅ تم بنجاح! تم العثور على {len(matches)} مباراة.")
