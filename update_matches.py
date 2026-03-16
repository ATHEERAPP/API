import requests
import json
from datetime import datetime

def get_live_matches_pro():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': 'b43963bf5cfa411c8934edd9d5fafa69'}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            matches_list = []
            
            for m in data.get('matches', []):
                # قمت بتغيير الأسماء هنا لتناسب ما يطلبه تطبيقك عادة
                matches_list.append({
                    "league": m['competition']['name'],
                    "t1": m['homeTeam']['shortName'] or m['homeTeam']['name'], # تم التغيير لـ t1
                    "t2": m['awayTeam']['shortName'] or m['awayTeam']['name'], # تم التغيير لـ t2
                    "sc": f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}" if m['score']['fullTime']['home'] is not None else "vs", # تم التغيير لـ sc
                    "time": m['utcDate'][11:16],
                    "status": m['status']
                })
            return matches_list
        return []
    except:
        return []

if __name__ == "__main__":
    matches = get_live_matches_pro()
    
    # تأكد أن المفتاح الرئيسي هو "matches" كما في تطبيقك
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches_count": len(matches),
        "matches": matches
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print("✅ تم التحديث بالأسماء المتوافقة مع التطبيق!")
