import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def scrape_kooora():
    """
    وظيفة احترافية لسحب مباريات اليوم من موقع كورة
    تتضمن معالجة الأخطاء وتخطي الحماية
    """
    url = "https://www.kooora.com/?live=1"
    
    # متصفح وهمي متكامل لتجنب الحظر
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
        "Referer": "https://www.kooora.com/",
        "Cache-Control": "no-cache"
    }
    
    try:
        # إرسال الطلب للموقع
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8' # لضمان قراءة اللغة العربية بشكل صحيح
        
        if response.status_code != 200:
            print(f"❌ فشل الوصول للموقع: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'lxml')
        matches_list = []
        
        # موقع كورة ينظم المباريات في جداول بـ ID يبدأ بـ m_
        # سنقوم بالبحث عن كل الجداول التي تحتوي على بيانات مباريات
        tables = soup.find_all('table', class_='m_table')
        
        for table in tables:
            # محاولة استخراج اسم الدوري
            league_header = table.find_previous('div', class_='league_name')
            league_name = league_header.get_text(strip=True) if league_header else "بطولة متنوعة"
            
            rows = table.find_all('tr')
            for row in rows:
                # استخراج الفرق والنتائج
                teams = row.find_all('td', class_='team_name')
                score = row.find('td', class_='match_score')
                time_status = row.find('td', class_='match_time')
                
                if len(teams) >= 2:
                    match_data = {
                        "league": league_name,
                        "teamA": teams[0].get_text(strip=True),
                        "teamB": teams[1].get_text(strip=True),
                        "score": score.get_text(strip=True) if score else "vs",
                        "time": time_status.get_text(strip=True) if time_status else "--:--",
                        "is_live": "مباشر" in row.get_text()
                    }
                    matches_list.append(match_data)
        
        return matches_list

    except Exception as e:
        print(f"⚠️ حدث خطأ أثناء السحب: {e}")
        return []

if __name__ == "__main__":
    print("🚀 بدء محرك أثير لتحديث المباريات...")
    
    # تنفيذ عملية الصيد
    data = scrape_kooora()
    
    # تجهيز الملف النهائي
    final_json = {
        "status": "success",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_matches": len(data),
        "matches": data
    }
    
    # حفظ البيانات في ملف matches.json
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)
    
    print(f"✅ تم تحديث {len(data)} مباراة بنجاح في ملف matches.json")
