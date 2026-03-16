import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_kooora_pro():
    url = "https://www.kooora.com/?live=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ar,en;q=0.9,en;q=0.8"
    }
    
    matches_list = []
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        
        # كورة يستخدم الـ ID الذي يبدأ بـ 'm_' لكل سطر مباراة
        all_rows = soup.find_all('tr', id=lambda x: x and x.startswith('m_'))
        
        for row in all_rows:
            try:
                # استخراج اسم الدوري (غالباً يكون في الترويسة السابقة للجدول)
                league = row.find_previous('div', class_='league_name')
                league_name = league.get_text(strip=True) if league else "بطولة"
                
                # استخراج الفرق
                teams = row.find_all('td', class_='team_name')
                # استخراج النتيجة
                score_cell = row.find('td', class_='match_score')
                # استخراج حالة المباراة أو الوقت
                status_cell = row.find('td', class_='match_time') or row.find('td', class_='match_status')

                if len(teams) >= 2:
                    matches_list.append({
                        "league": league_name,
                        "teamA": teams[0].get_text(strip=True),
                        "teamB": teams[1].get_text(strip=True),
                        "score": score_cell.get_text(strip=True) if score_cell else "vs",
                        "time": status_cell.get_text(strip=True) if status_cell else "--:--",
                        "live": "مباشر" in row.get_text()
                    })
            except: continue
            
        return matches_list
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    data = scrape_kooora_pro()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches_count": len(data),
        "matches": data
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ تم صيد {len(data)} مباراة بنجاح!")
