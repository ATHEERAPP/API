import requests
import json
from datetime import datetime
import re

def scrape_kooora_your_link():
    # الرابط الذي حددته أنت يا مدير
    url = "https://www.kooora.com/كرة-القدم/مباريات-اليوم"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.kooora.com/",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8"
    }
    
    try:
        # طلب الصفحة مباشرة
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        html_content = response.text

        # استخراج الدوريات (Championships) من داخل الكود المصدري للرابط
        leagues = {}
        leagues_data = re.findall(r"championship\((\d+),.*?'(.*?)'", html_content)
        for l_id, l_name in leagues_data:
            leagues[l_id] = l_name

        # استخراج المباريات (Matches) من داخل الكود المصدري للرابط
        matches_data = re.findall(r"match\((\d+),'.*?','(.*?)','(.*?)','(.*?)','(.*?)',(\d+)", html_content)
        
        results = []
        for m in matches_data:
            m_id, t1, t2, score, m_time, l_id = m
            
            # تنظيف النصوص العربية المشفره
            t1_clean = t1.replace('\\', '').strip()
            t2_clean = t2.replace('\\', '').strip()
            
            results.append({
                "league": leagues.get(l_id, "بطولة"),
                "teamA": t1_clean,
                "teamB": t2_clean,
                "score": score.strip() if score.strip() else "vs",
                "time": m_time.strip()
            })

        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    print(f"🚀 جاري سحب البيانات من الرابط الذي حددته...")
    data = scrape_kooora_your_link()
    
    output = {
        "status": "success",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches_count": len(data),
        "matches": data
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"✅ تم سحب {len(data)} مباراة بنجاح من رابطك!")
