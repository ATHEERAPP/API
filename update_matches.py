import requests
import json
from datetime import datetime

def get_live_matches_pro():
    # الرابط الرسمي لجلب مباريات اليوم من الدوريات الكبرى
    url = "https://api.football-data.org/v4/matches"
    
    # المفتاح الخاص بك الذي أرسلته
    headers = {
        'X-Auth-Token': 'b43963bf5cfa411c8934edd9d5fafa69'
    }
    
    try:
        print("📡 جاري الاتصال بـ Football-Data API...")
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            matches_list = []
            
            for m in data.get('matches', []):
                # استخراج البيانات المهمة لتطبيق "أثير"
                matches_list.append({
                    "league": m['competition']['name'],
                    "teamA": m['homeTeam']['shortName'] or m['homeTeam']['name'],
                    "teamB": m['awayTeam']['shortName'] or m['awayTeam']['name'],
                    "score": f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}" if m['score']['fullTime']['home'] is not None else "vs",
                    "time": m['utcDate'][11:16], # توقيت المباراة
                    "status": m['status'] # هل بدأت أم انتهت؟
                })
            
            return matches_list
        else:
            print(f"⚠️ فشل الطلب: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ خطأ تقني: {e}")
        return []

if __name__ == "__main__":
    matches = get_live_matches_pro()
    
    output = {
        "status": "success",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": "Football-Data.org (Official)",
        "matches_count": len(matches),
        "matches": matches
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"✅ تم بنجاح! وجدنا {len(matches)} مباراة حقيقية.")
