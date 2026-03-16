import requests
import json
from datetime import datetime

def get_live_matches_pro():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': 'b43963bf5cfa411c8934edd9d5fafa69'}
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # قاموس لتعريب أسماء الدوريات الكبرى يدوياً
    league_translation = {
        "Premier League": "الدوري الإنجليزي",
        "Serie A": "الدوري الإيطالي",
        "Primera Division": "الدوري الإسباني",
        "Bundesliga": "الدوري الألماني",
        "Ligue 1": "الدوري الفرنسي",
        "UEFA Champions League": "دوري أبطال أوروبا",
        "Championship": "دوري الدرجة الأولى الإنجليزي",
        "Campeonato Brasileiro Série A": "الدوري البرازيلي"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            matches_list = []
            
            for m in data.get('matches', []):
                league_name = m['competition']['name']
                # تعريب الاسم إذا كان موجوداً في القاموس، وإلا يبقى كما هو
                ar_league = league_translation.get(league_name, league_name)
                
                score_data = m.get('score', {}).get('fullTime', {})
                h_score = score_data.get('home')
                a_score = score_data.get('away')
                
                matches_list.append({
                    "date": today_str, 
                    "league": ar_league,
                    "league_logo": m['competition']['emblem'], # شعار الدوري
                    "teamA": m['homeTeam']['shortName'] or m['homeTeam']['name'],
                    "teamB": m['awayTeam']['shortName'] or m['awayTeam']['name'],
                    "logoA": m['homeTeam']['crest'], # شعار الفريق A
                    "logoB": m['awayTeam']['crest'], # شعار الفريق B
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
    print(f"✅ تم تحديث {len(matches)} مباراة مع الشعارات والأسماء!")
