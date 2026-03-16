import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_kooora_final():
    # سنعود لنسخة الكمبيوتر مع تعزيز "هوية المتصفح"
    url = "https://www.kooora.com/?live=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
        "Referer": "https://www.kooora.com/"
    }
    
    matches_list = []
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # كورة يضع المباريات في صفوف تبدأ بـ 'm_'
        # سنبحث عن كل خلية تحتوي على اسم الفريق
        all_matches_rows = soup.find_all('tr', id=re.compile(r'^m_')) if 're' in globals() else soup.find_all('tr')
        
        for row in soup.select('tr'):
            # محاولة قنص الفرق والنتيجة من خلال الـ classes المشهورة في كورة
            team_a = row.select_one('td.team_name.team_a, td:nth-child(3)')
            team_b = row.select_one('td.team_name.team_b, td:nth-child(5)')
            score = row.select_one('td.match_score, td:nth-child(4)')
            
            if team_a and team_b and score:
                t1_text = team_a.get_text(strip=True)
                t2_text = team_b.get_text(strip=True)
                
                # التأكد أننا لم نسحب صفوف فارغة
                if t1_text and t2_text:
                    matches_list.append({
                        "t1": t1_text,
                        "t2": t2_text,
                        "sc": score.get_text(strip=True) if score else "vs",
                        "time": datetime.now().strftime("%H:%M")
                    })
        
        # إذا فشلت الطريقة الأولى، نجرب طريقة الـ "match_box" (للموبايل)
        if not matches_list:
            for box in soup.select('.match_box'):
                teams = box.select('.team_name')
                if len(teams) >= 2:
                    matches_list.append({
                        "t1": teams[0].get_text(strip=True),
                        "t2": teams[1].get_text(strip=True),
                        "sc": box.select_one('.match_score').get_text(strip=True) if box.select_one('.match_score') else "vs"
                    })

        return matches_list
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    data = scrape_kooora_final()
    # حذف التكرار إذا وجد
    unique_matches = [dict(t) for t in {tuple(d.items()) for d in data}]
    
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches_count": len(unique_matches),
        "matches": unique_matches
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ تم صيد {len(unique_matches)} مباراة!")
