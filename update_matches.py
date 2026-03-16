import requests
import json
from datetime import datetime
import re

def scrape_kooora_final_boss():
    # الرابط الأساسي مع بارامترات لضمان جلب كل الدوريات
    url = "https://www.kooora.com/?n=0&o=n"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
        "Referer": "https://www.kooora.com/",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        # محاولة جلب الصفحة
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        content = response.text

        # 1. استخراج الدوريات (Championships)
        leagues = {}
        # نمط البحث: championship(ID, Type, Name, ...)
        cp_pattern = r"championship\((\d+),.*?'(.*?)'"
        for cp_id, cp_name in re.findall(cp_pattern, content):
            leagues[cp_id] = cp_name

        # 2. استخراج المباريات (Matches) 
        # نمط البحث الشامل عن دالة match
        # الصيغة: match(ID, Date, TeamA, TeamB, Score, Time, LeagueID, ...)
        match_pattern = r"match\((\d+),'.*?','(.*?)','(.*?)','(.*?)','(.*?)',(\d+)"
        raw_matches = re.findall(match_pattern, content)
        
        matches_list = []
        for m in raw_matches:
            m_id, t1, t2, score, m_time, l_id = m
            
            # تنظيف البيانات من الرموز الزائدة
            t1 = t1.replace('\\', '').strip()
            t2 = t2.replace('\\', '').strip()
            score = score.replace('\\', '').strip() if score.strip() else "vs"
            
            matches_list.append({
                "league": leagues.get(l_id, "بطولة دولية"),
                "teamA": t1,
                "teamB": t2,
                "score": score,
                "time": m_time,
                "is_live": "مباشر" in content # فحص حالة البث العام
            })

        return matches_list

    except Exception as e:
        print(f"❌ خطأ: {e}")
        return []

if __name__ == "__main__":
    print("🧨 جاري تفجير حماية كورة واستخراج الدوريات...")
    data = scrape_kooora_final_boss()
    
    # فلترة النتائج لضمان عدم وجود تكرار
    unique_data = {f"{m['teamA']}{m['teamB']}": m for m in data}.values()
    final_list = list(unique_data)

    output = {
        "status": "success",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches_count": len(final_list),
        "matches": final_list
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"✅ مبروك! وجدنا {len(final_list)} مباراة من كل الدوريات.")
