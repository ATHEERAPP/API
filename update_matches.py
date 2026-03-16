import requests
import json
from datetime import datetime
import re

def scrape_kooora_today_final():
    # الرابط الذي أرسلته أنت (مباريات اليوم)
    url = "https://www.kooora.com/?n=0&o=n"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.kooora.com/",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8"
    }
    
    try:
        # طلب الصفحة مع تحديد ترميز اللغة العربية
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        html_content = response.text

        # 1. استخراج أسماء الدوريات (التي تظهر باللون الأصفر في الموقع)
        leagues = {}
        # النمط: championship(ID, Type, Name, ...)
        leagues_raw = re.findall(r"championship\((\d+),.*?'(.*?)'", html_content)
        for l_id, l_name in leagues_raw:
            leagues[l_id] = l_name

        # 2. استخراج المباريات (التي تظهر في الجدول)
        # النمط: match(ID, Date, TeamA, TeamB, Score, Time, LeagueID, ...)
        matches_raw = re.findall(r"match\((\d+),'.*?','(.*?)','(.*?)','(.*?)','(.*?)',(\d+)", html_content)
        
        matches_list = []
        for m in matches_raw:
            m_id, t1, t2, score, m_time, l_id = m
            
            # تنظيف النصوص من الرموز المشفره (مثل \u0627)
            t1_clean = t1.encode().decode('unicode-escape').replace('\\', '') if '\\' in t1 else t1
            t2_clean = t2.encode().decode('unicode-escape').replace('\\', '') if '\\' in t2 else t2
            
            matches_list.append({
                "league": leagues.get(l_id, "بطولة"),
                "teamA": t1_clean.strip(),
                "teamB": t2_clean.strip(),
                "score": score.strip() if score.strip() else "vs",
                "time": m_time.strip()
            })

        return matches_list
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return []

if __name__ == "__main__":
    print("🚀 جاري سحب المباريات من رابط 'مباريات اليوم'...")
    data = scrape_kooora_today_final()
    
    # حفظ النتائج
    output = {
        "status": "success",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches_count": len(data),
        "matches": data
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"✅ مبروك! وجدنا {len(data)} مباراة حقيقية.")
