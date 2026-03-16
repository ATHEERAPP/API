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
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        
        matches_list = []
        # البحث عن جداول المباريات في كورة
        tables = soup.find_all('table', class_='m_table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                teams = row.find_all('td', class_='team_name')
                score = row.find('td', class_='match_score')
                if len(teams) >= 2:
                    matches_list.append({
                        "league": "جميع البطولات",
                        "teamA": teams[0].get_text(strip=True),
                        "teamB": teams[1].get_text(strip=True),
                        "score": score.get_text(strip=True) if score else "vs",
                        "time": datetime.now().strftime("%H:%M")
                    })
        return matches_list
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    matches = scrape_kooora()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": matches
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ Success! Found {len(matches)} matches.")
