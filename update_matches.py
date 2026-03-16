import requests
import json
from datetime import datetime
import re

def scrape_kooora_today():
    # الرابط الذي حددته أنت (مباريات اليوم)
    url = "https://www.kooora.com/?n=0&o=n"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.kooora.com/"
    }
    
    matches_list = []
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        content = response.text
        
        # البحث عن بيانات المباريات داخل دالة match() في كود الصفحة
        # الصيغة في كورة تكون غالباً: match(12345, '2026-03-16', 'فريق أ', 'فريق ب', '0 - 0', '19:00', ...)
        raw_matches = re.findall(r'match\((.*?)\);', content)
        
        # البحث عن أسماء الدوريات (تكون مخزنة في دالة championship)
        championships = re.findall(r'championship\((.*?)\);', content)
        leagues_dict = {}
        for cp in championships:
            cp_parts = cp.split(',')
            if len(cp_parts) > 2:
                cp_id = cp_parts[0].strip()
                cp_name = cp_parts[2].replace("'", "").strip()
                leagues_dict[cp_id] = cp_name

        for match in raw_matches:
            # تنظيف البيانات وتقسيمها
            parts = [p.strip().replace("'", "") for p in match.split(',')]
            
            # التقسيم المعتاد في كورة لصفحة مباريات اليوم:
            # [0] ID المباراة، [2] الفريق الأول، [3] الفريق الثاني، [4] النتيجة، [5] الوقت، [6] ID الدوري
            if len(parts) >= 7:
                t1 = parts[2]
                t2 = parts[3]
                score = parts[4] if parts[4] else "vs"
                match_time = parts[5]
                league_id = parts[6]
                
                league_name = leagues_dict.get(league_id, "بطولة أخرى")
                
                if t1 and t2:
                    matches_list.append({
                        "league": league_name,
                        "teamA": t1,
                        "teamB": t2,
                        "score": score,
                        "time": match_time
                    })

        return matches_list
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    print("🚀 جاري سحب مباريات اليوم من المصدر...")
    data = scrape_kooora_today()
    
    output = {
        "status": "success",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches_count": len(data),
        "matches": data
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"✅ مبروك! تم العثور على {len(data)} مباراة.")
