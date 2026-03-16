import requests
import json
from datetime import datetime

def get_football_data():
    API_KEY = "b43963bf5cfa411c8934edd9d5fafa69"
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            matches_list = []
            today_str = datetime.now().strftime("%Y-%m-%d")

            matches = data.get('matches', [])
            for m in matches:
                competition = m.get('competition', {}).get('name', 'بطولة')
                home_team = m.get('homeTeam', {}).get('shortName', m.get('homeTeam', {}).get('name', 'فريق 1'))
                away_team = m.get('awayTeam', {}).get('shortName', m.get('awayTeam', {}).get('name', 'فريق 2'))
                home_crest = m.get('homeTeam', {}).get('crest', '')
                away_crest = m.get('awayTeam', {}).get('crest', '')
                
                status = m.get('status')
                score_home = m.get('score', {}).get('fullTime', {}).get('home')
                score_away = m.get('score', {}).get('fullTime', {}).get('away')
                
                score_home = score_home if score_home is not None else 0
                score_away = score_away if score_away is not None else 0

                if status in ['IN_PLAY', 'PAUSED']:
                    match_status = "live"
                    score = f"{score_home} - {score_away}"
                    time_str = "مباشر"
                elif status == 'FINISHED':
                    match_status = "finished"
                    score = f"{score_home} - {score_away}"
                    time_str = "انتهت"
                else:
                    match_status = "timed"
                    score = "vs"
                    # هنا التغيير الجذري! سنرسل التوقيت العالمي (UTC) كما هو 
                    # لكي يقوم تطبيق الهاتف بتحويله تلقائياً لدولة المستخدم
                    time_str = m.get('utcDate', '') # مثال: 2026-03-16T18:00:00Z

                matches_list.append({
                    "date": today_str,
                    "league": competition,
                    "teamA": home_team,
                    "teamB": away_team,
                    "logoA": home_crest,
                    "logoB": away_crest,
                    "score": score,
                    "time": time_str,
                    "status": match_status,
                    "broadcasts": [{"channel": "أثير الرياضي", "commentator": "تحديث تلقائي"}]
                })
                
            return matches_list
        else:
            return []
    except Exception as e:
        return []

if __name__ == "__main__":
    final_data = get_football_data()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": final_data,
        "custom_ad": {"is_active": False}
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
