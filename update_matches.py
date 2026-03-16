import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_kooora():
    url = "https://www.kooora.com/?live=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml') # استخدام lxml للسرعة
        
        matches_list = []
        # كورة ينظم المباريات في جداول بـ ID يبدأ بـ m_
        tables = soup.find_all('table', class_='m_table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                teams = row.find_all('td', class_='team_name')
                score = row.find('td', class_='match_score')
                status = row.find('td', class_='match_status')
                
                if len(teams) >= 2:
                    matches_list.append({
                        "league": "بطولات كورة", # يمكن تطويرها لاستخراج اسم الدوري
                        "teamA": teams[0].get_text(strip=True),
                        "teamB": teams[1].get_text(strip=True),
                        "score": score.get_text(strip=True) if score else "vs",
                        "status": status.get_text(strip=True) if status else "N/A"
                    })
        
        return matches_list
    except Exception as e:
        print(f"Error scraping: {e}")
        return []

if __name__ == "__main__":
    data = scrape_kooora()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": data
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ Done! Scraped {len(data)} matches.")
