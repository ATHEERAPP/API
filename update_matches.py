import requests
import json
from datetime import datetime

# 🔑 إعدادات المصدر (API-Football)
# استبدل XXXXXX بمفتاحك الحقيقي الذي حصلت عليه من الموقع
API_KEY = "XXXXXX" 

# إعدادات الدوريات (مثال: الدوري السعودي 307، الإنجليزي 39، الإسباني 140)
LEAGUE_IDS = [307, 39, 140] 
TODAY = datetime.now().strftime('%Y-%m-%d')

def fetch_real_matches():
    all_fixtures = []
    headers = {
        'x-apisports-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    for league in LEAGUE_IDS:
        url = f"https://v3.football.api-sports.io/fixtures?league={league}&date={TODAY}"
        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            for item in data.get('response', []):
                status_short = item['fixture']['status']['short']
                
                # تحويل الحالة للغة التطبيق
                status_map = {
                    'NS': 'upcoming',
                    '1H': 'live',
                    'HT': 'live',
                    '2H': 'live',
                    'FT': 'finished'
                }
                
                match = {
                    "date": item['fixture']['date'].split('T')[0],
                    "league": item['league']['name'],
                    "league_logo": item['league']['logo'],
                    "teamA": item['teams']['home']['name'],
                    "logoA": item['teams']['home']['logo'],
                    "teamB": item['teams']['away']['name'],
                    "logoB": item['teams']['away']['logo'],
                    "status": status_map.get(status_short, 'upcoming'),
                    "score": f"{item['goals']['home']} - {item['goals']['away']}" if item['goals']['home'] is not None else "0 - 0",
                    "time": item['fixture']['date'].split('T')[1][0:5],
                    "minute": str(item['fixture']['status']['elapsed'] or ""),
                    "half": "مباشر" if status_short in ['1H', '2H', 'HT'] else "",
                    "broadcasts": [
                        {
                            "channel": "بث مباشر",
                            "commentator": "جاري التحديث",
                            "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8" # يمكنك وضع رابط افتراضي هنا
                        }
                    ]
                }
                all_fixtures.append(match)
        except Exception as e:
            print(f"Error fetching league {league}: {e}")

    return all_fixtures

# تحديث الملف النهائي
def update_json():
    matches = fetch_real_matches()
    
    # إذا لم يجد مباريات اليوم (مثلاً وقت الفجر)، يحافظ على الملف القديم أو يضع رسالة
    if not matches:
        print("⚠️ لم يتم العثور على مباريات حقيقية اليوم.")
        return

    data = {
        "custom_ad": {
            "is_active": True,
            "image_url": "https://raw.githubusercontent.com/ATHEERAPP/API/main/stadium_bg.jpg.png",
            "click_url": "https://google.com"
        },
        "matches": matches
    }

    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ تم تحديث {len(matches)} مباراة حقيقية!")

if __name__ == "__main__":
    update_json()
