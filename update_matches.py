import requests
import json
from datetime import datetime
import re

def scrape_kooora_today():
    # الرابط المباشر لصفحة مباريات اليوم
    url = "https://www.kooora.com/?n=0&o=n"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.kooora.com/",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        html_content = response.text

        # 1. استخراج أسماء الدوريات وتخزينها في قاموس
        # الصيغة: championship(ID, Type, Name, ...)
        leagues = {}
        cp_data = re.findall(r"championship\((\d+),.*?'(.*?)'", html_content)
        for cp_id, cp_name in cp_data:
            leagues[cp_id] = cp_name

        # 2. استخراج المباريات
        # الصيغة: match(ID, Date, TeamA, TeamB, Score, Time, LeagueID, ...)
        matches_raw = re.findall(r"match\((\d+),'.*?','(.*?)','(.*?)','(.*?)','(.*?)',(\d+)", html_content)
        
        final_matches = []
        for m in matches_raw:
            m_id, t1, t2, score, m_time, l_id = m
            
            # تنظيف النتيجة إذا كانت فارغة
            display_score = score.strip() if score.strip() else "vs"
            
            final_matches.append({
                "league": leagues.get(l_id, "بطولة غير محددة"),
                "teamA": t1.strip(),
                "teamB": t2.strip(),
                "score": display_score,
                "time": m_time.strip()
            })

        return final_matches

    except Exception as e:
        print(f"❌ خطأ أثناء السحب: {e}")
        return []

if __name__ == "__main__":
    print("🚀 جاري سحب مباريات اليوم من قلب كورة...")
    all_matches = scrape_kooora_today()
    
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches_count": len(all_matches),
        "matches": all_matches
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"✅ مبروك! تم العثور على {len(all_matches)} مباراة وتحديثها.")
