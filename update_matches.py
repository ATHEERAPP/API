import requests
import json
from datetime import datetime
import re

def scrape_kooora_empire():
    # الرابط الأساسي الذي يحتوي على بيانات كل مباريات اليوم
    url = "https://www.kooora.com/?n=0&o=n"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.kooora.com/",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        content = response.text

        # 1. استخراج قاموس الدوريات (Championships)
        # مصفوفة كورة: championship(id, type, name, country_id, ...)
        leagues = {}
        cp_matches = re.findall(r"championship\((\d+),.*?'(.*?)'", content)
        for cp_id, cp_name in cp_matches:
            leagues[cp_id] = cp_name

        # 2. استخراج قاموس الدول (Countries) لتمييز الدوريات
        countries = {}
        ct_matches = re.findall(r"country\((\d+),.*?'(.*?)'", content)
        for ct_id, ct_name in ct_matches:
            countries[ct_id] = ct_name

        # 3. استخراج المباريات (Matches)
        # مصفوفة كورة: match(id, date, teamA, teamB, score, time, leagueID, ...)
        # نستخدم regex مرن جداً لصيد كل الأنماط
        match_data = re.findall(r"match\((\d+),'.*?','(.*?)','(.*?)','(.*?)','(.*?)',(\d+)", content)
        
        all_matches = []
        for m in match_data:
            m_id, t1, t2, score, m_time, l_id = m
            
            # تنظيف النتيجة
            clean_score = score.strip() if score.strip() else "vs"
            
            # تحديد اسم الدوري مع الدولة إذا أمكن
            league_name = leagues.get(l_id, "بطولة عالمية")
            
            all_matches.append({
                "league": league_name,
                "teamA": t1.strip(),
                "teamB": t2.strip(),
                "score": clean_score,
                "time": m_time.strip(),
                "status": "قادمة" if clean_score == "vs" else "جارية/انتهت"
            })

        return all_matches

    except Exception as e:
        print(f"❌ خطأ فني: {e}")
        return []

if __name__ == "__main__":
    print("🏟️ جاري جلب كل دوريات العالم لتطبيق أثير...")
    results = scrape_kooora_empire()
    
    # ترتيب المباريات حسب الدوري ليكون شكلها احترافياً في تطبيقك
    results.sort(key=lambda x: x['league'])

    output = {
        "status": "success",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_leagues": len(set(m['league'] for m in results)),
        "matches_count": len(results),
        "matches": results
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"✅ مبروك! تم تحديث {len(results)} مباراة من مختلف الدوريات.")
