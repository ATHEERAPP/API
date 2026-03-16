import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape():
    url = "https://www.kooora.com/?live=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        matches = []
        # محرك البحث عن المباريات
        for row in soup.select('table.m_table tr'):
            teams = row.select('td.team_name')
            if len(teams) >= 2:
                matches.append({
                    "t1": teams[0].text.strip(),
                    "t2": teams[1].text.strip(),
                    "sc": row.select_one('td.match_score').text.strip() if row.select_one('td.match_score') else "vs"
                })
        return matches
    except: return []

if __name__ == "__main__":
    data = {"last_update": datetime.now().strftime("%H:%M"), "matches": scrape()}
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("✅ Done")
