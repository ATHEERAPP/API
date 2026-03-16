import requests
import json
from datetime import datetime

def get_live_matches_pro():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': 'b43963bf5cfa411c8934edd9d5fafa69'}
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    league_translation = {
        "Premier League": "الدوري الإنجليزي",
        "Serie A": "الدوري الإيطالي",
        "Primera Division": "الدوري الإسباني",
        "Bundesliga": "الدوري الألماني",
        "Ligue 1": "الدوري الفرنسي",
        "UEFA Champions League": "دوري أبطال أوروبا"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            matches_list = []
            
            for m in data.get('matches', []):
                # استخراج معرف الفريق (ID) لجلب شعار PNG مضمون
                home_id = m['homeTeam']['id']
                away_id = m['awayTeam']['id']
                
                # تحويل الرابط إلى PNG لأن تطبيقك قد لا يدعم SVG مباشرة
                # سنستخدم مستودع شعارات موثوق يعتمد على الـ ID
                logo_a_url = f"https://crests.football-data.org/{home_id}.png"
                logo_b_url = f"https://crests.football-data.org/{away_id}.png"
                
                league_name = m['competition']['name']
                ar_league = league_translation.get(league_name, league_name)
                
                score_data = m.get('score', {}).get('fullTime', {})
                h_score = score_data.get('home')
                a_score = score_data.get('away')
                
                matches_list.append({
                    "date": today_str, 
                    "league": ar_league,
                    "league_logo": m['competition']['emblem'],
                    "teamA": m['homeTeam']['shortName'] or m['homeTeam']['name'],
                    "teamB": m['awayTeam']['shortName'] or m['awayTeam']['name'],
                    "logoA": logo_a_url, # روابط PNG مباشرة
                    "logoB": logo_b_url, # روابط PNG مباشرة
                    "score": f"{h_score} - {a_score}" if h_score is not None else "vs",
                    "time": m['utcDate'][11:16],
                    "status": "live" if m['status'] in ["IN_PLAY", "PAUSED"] else ("finished" if m['status'] == "FINISHED" else "timed"),
                    "broadcasts": [
                        {
                            "channel": "beIN Sports",
                            "commentator": "معلق عربي",
                            "stream_url": "" 
                        }
                    ]
                })
            return matches_list
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    matches = get_live_matches_pro()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": matches,
        "custom_ad": {"is_active": False, "image_url": "", "click_url": ""}
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print("✅ تم تحويل الشعارات إلى صيغة PNG لتعمل في التطبيق!")
