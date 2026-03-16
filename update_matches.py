import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_matches():
    url = "https://www.kooora.com/?live=1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(url, headers=headers, timeout=20)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        results = []
        for row in soup.select('table.m_table tr'):
            teams = row.select('td.team_name')
            score = row.select_one('td.match_score')
            if len(teams) >= 2:
                results.append({
                    "league": "Kooora Live",
                    "t1": teams[0].get_text(strip=True),
                    "t2": teams[1].get_text(strip=True),
                    "sc": score.get_text(strip=True) if score else "vs"
                })
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    matches = get_matches()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": matches
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ Success: {len(matches)} matches.")
