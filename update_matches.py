import requests
import json
from datetime import datetime

def get_live_matches_pro():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': 'b43963bf5cfa411c8934edd9d5fafa69'}
    
    # الحصول على تاريخ اليوم بنفس التنسيق الذي يطلبه تطبيقك (yyyy-MM-dd)
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.statusCode == 200:
            data = response.json()
            matches_list = []
            
            for m in data.get('matches', []):
                matches_list.append({
                    "date": today_str, # 👈 هذا هو السطر السحري الذي سيجعلها تظهر في التطبيق
                    "league": m['competition']['name'],
                    "t1": m['homeTeam']['shortName'] or m['homeTeam']['name'],
                    "t2": m['awayTeam']['shortName'] or m['awayTeam']['name'],
                    "logoA": m['homeTeam']['crest'], # إضافة الشعارات لتظهر في البطاقات
                    "logoB": m['awayTeam']['crest'],
                    "sc": f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}" if m['score']['fullTime']['home'] is not None else "vs",
                    "time": m['utcDate'][11:16],
                    "status": "live" if m['status'] == "IN_PLAY" else ("finished" if m['status'] == "FINISHED" else "timed")
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
        "custom_ad": {"is_active": False} # إضافة حقل الإعلان لتجنب الأخطاء في التطبيق
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ تم تحديث {len(matches)} مباراة مع إضافة حقل التاريخ!")
