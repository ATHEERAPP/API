import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_kooora_all():
    # الرابط الذي يجمع كل مباريات اليوم في كورة
    url = "https://www.kooora.com/?live=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        matches_data = []
        current_league = "بطولة عامة"

        # موقع كورة يضع المباريات داخل جداول
        # سنقوم بالبحث عن كل الصفوف التي تحتوي على بيانات
        rows = soup.find_all(['div', 'table'], class_=['match_box', 'm_table'])
        
        for row in rows:
            # استخراج اسم الدوري إذا وجد (كورة يضعه في ترويسة الجدول)
            league_tag = row.find_previous('div', class_='league_name')
            if league_tag:
                current_league = league_tag.text.strip()

            # استخراج تفاصيل المباراة
            # ملاحظة: سنقوم ببرمجة الكود ليفهم هيكلة كورة المعقدة
            teams = row.find_all('td', class_='team_name')
            score = row.find('td', class_='match_score')
            time = row.find('td', class_='match_time')

            if len(teams) >= 2:
                matches_data.append({
                    "league": current_league,
                    "teamA": teams[0].text.strip(),
                    "teamB": teams[1].text.strip(),
                    "score": score.text.strip() if score else "v",
                    "time": time.text.strip() if time else "--:--",
                    "status": "live" if "مباشر" in row.text else "upcoming"
                })

        return matches_data
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    print("🚀 جاري سحب كل دوريات العالم من كورة...")
    all_matches = scrape_kooora_all()
    
    final_output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_matches": len(all_matches),
        "matches": all_matches
    }

    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(final_output, f, ensure_ascii=False, indent=4)
    
    print(f"✅ تم بنجاح! تم جلب {len(all_matches)} مباراة.")

if __name__ == "__main__":
    main()
