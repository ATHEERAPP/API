import requests
import json
from datetime import datetime
import re

def scrape_kooora_bypass():
    # سنستخدم وسيطاً لتغيير الـ IP وتجاوز الحجب
    # الرابط الأصلي
    target_url = "https://www.kooora.com/?n=0&o=n"
    
    # استخدام خدمة AllOrigins أو ما يشابهها لتخطي الحجب (مجانية ومفتوحة)
    proxy_url = f"https://api.allorigins.win/get?url={requests.utils.quote(target_url)}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    try:
        print(f"📡 محاولة الاتصال عبر الوسيط لتجاوز الحظر...")
        response = requests.get(proxy_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # الوسيط يعيد البيانات داخل حقل 'contents'
            content = response.json().get('contents', '')
            
            # استخراج الدوريات
            leagues = {}
            cp_data = re.findall(r"championship\((\d+),.*?'(.*?)'", content)
            for cp_id, cp_name in cp_data:
                leagues[cp_id] = cp_name

            # استخراج المباريات
            match_data = re.findall(r"match\((\d+),'.*?','(.*?)','(.*?)','(.*?)','(.*?)',(\d+)", content)
            
            final_matches = []
            for m in match_data:
                m_id, t1, t2, score, m_time, l_id = m
                final_matches.append({
                    "league": leagues.get(l_id, "بطولة"),
                    "teamA": t1.replace('\\', '').strip(),
                    "teamB": t2.replace('\\', '').strip(),
                    "score": score.strip() if score.strip() else "vs",
                    "time": m_time.strip()
                })
            
            return final_matches
        return []
    except Exception as e:
        print(f"❌ خطأ في الوسيط: {e}")
        return []

if __name__ == "__main__":
    data = scrape_kooora_bypass()
    
    # إذا نجح الوسيط في جلب البيانات
    output = {
        "status": "success",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches_count": len(data),
        "matches": data
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    if len(data) > 0:
        print(f"🎉 نجحنا! تم صيد {len(data)} مباراة عبر الوسيط.")
    else:
        print("⚠️ لا تزال النتيجة صفر، الموقع يرفض حتى الوسيط العام.")
