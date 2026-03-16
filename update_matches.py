import requests
import json
from datetime import datetime

def get_live_matches_pro():
    # الرابط الرسمي
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': 'b43963bf5cfa411c8934edd9d5fafa69'}
    
    # تاريخ اليوم ليقبله تطبيق فلاتر
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        
        # تصحيح الخطأ المطبعي من statusCode إلى status_code
        if response.status_code == 200:
            data = response.json()
            matches_list = []
            
            for m in data.get('matches', []):
                matches_list.append({
                    "date": today_str, 
                    "league": m['competition']['name'],
                    "t1": m['homeTeam']['shortName'] or m['homeTeam']['name'],
                    "t2": m['awayTeam']['shortName'] or m['awayTeam']['name'],
                    "logoA": m['homeTeam']['crest'], 
                    "logoB": m['awayTeam']['crest'],
                    "sc": f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}" if m['score']['fullTime']['home'] is not None else "vs",
                    "time": m['utcDate'][11:16],
                    # تحويل الحالة لتناسب تطبيقك
                    "status": "live" if m['status'] in ["IN_PLAY", "PAUSED"] else ("finished" if m['status'] == "FINISHED" else "timed")
                })
            return matches_list
        else:
            print(f"Error API: {response.status_code}")
            return []
    except Exception as e:
        print(f"Exception: {e}")
        return []

if __name__ == "__main__":
    matches = get_live_matches_pro()
    
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": matches,
        "custom_ad": {"is_active": False}
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
        
    print(f"✅ تم تحديث {len(matches)} مباراة بنجاح!")
