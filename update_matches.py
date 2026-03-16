import requests
import json
from datetime import datetime

def get_atheer_genius_data():
    API_KEY = "GYkTTE95YM1sCMsX"
    API_SECRET = "cdB4MZniIbltsK9n43gJdnHCsa0eAXs"
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    matches_list = []

    # 📡 نطلب جدول مباريات اليوم
    url = f"https://livescore-api.com/api-client/fixtures/matches.json?key={API_KEY}&secret={API_SECRET}&date={today_str}"

    try:
        response = requests.get(url, timeout=20)
        res_json = response.json()
        
        # 1️⃣ هل الطلب نجح؟
        if res_json.get('success'):
            fixtures = res_json.get('data', {}).get('fixtures', [])
            
            # 2️⃣ ماذا لو نجح الطلب ولكن لا توجد مباريات اليوم؟ (صباح الإثنين مثلاً)
            if not fixtures:
                matches_list.append({
                    "date": today_str,
                    "league": "تنبيه من السيرفر",
                    "teamA": "لا توجد مباريات",
                    "teamB": "مجدولة لهذا اليوم",
                    "logoA": "https://cdn-icons-png.flaticon.com/512/1008/1008928.png", # أيقونة تنبيه
                    "logoB": "https://cdn-icons-png.flaticon.com/512/1008/1008928.png",
                    "score": "0 - 0",
                    "time": "00:00",
                    "status": "finished",
                    "broadcasts": [{"channel": "نظام أثير", "commentator": "الذكاء الاصطناعي"}]
                })
            
            # 3️⃣ جلب المباريات الحقيقية (إن وجدت)
            for f in fixtures:
                matches_list.append({
                    "date": today_str,
                    "league": f.get('competition', {}).get('name', 'بطولة'),
                    "teamA": f.get('home_name', 'فريق 1'),
                    "teamB": f.get('away_name', 'فريق 2'),
                    "logoA": f"https://livescore-api.com/api-client/teams/logo.json?id={f.get('home_id')}&key={API_KEY}&secret={API_SECRET}",
                    "logoB": f"https://livescore-api.com/api-client/teams/logo.json?id={f.get('away_id')}&key={API_KEY}&secret={API_SECRET}",
                    "score": "vs",
                    "time": str(f.get('time', '00:00'))[:5],
                    "status": "timed",
                    "broadcasts": [{"channel": "beIN Sports", "commentator": "تحديث ذكي"}]
                })
        
        # 4️⃣ هنا السحر: إذا رفض الموقع إعطاءنا بيانات، سنرسل الخطأ لهاتفك!
        else:
            error_message = res_json.get('error', 'خطأ غير معروف من السيرفر')
            matches_list.append({
                "date": today_str,
                "league": "❌ تم رفض الطلب",
                "teamA": "سبب المشكلة:",
                "teamB": str(error_message), # سيظهر لك الخطأ الانجليزي هنا
                "logoA": "https://cdn-icons-png.flaticon.com/512/1008/1008928.png",
                "logoB": "https://cdn-icons-png.flaticon.com/512/1008/1008928.png",
                "score": "Error",
                "time": "00:00",
                "status": "finished",
                "broadcasts": [{"channel": "نظام أثير", "commentator": "تحليل الخطأ"}]
            })

        return matches_list

    except Exception as e:
        # 5️⃣ إذا انهار الكود تماماً، سيبعث لك رسالة انهيار
        matches_list.append({
            "date": today_str,
            "league": "🚨 خطأ برمجي",
            "teamA": "حدث خطأ",
            "teamB": str(e)[:20],
            "logoA": "https://cdn-icons-png.flaticon.com/512/1008/1008928.png",
            "logoB": "https://cdn-icons-png.flaticon.com/512/1008/1008928.png",
            "score": "Err",
            "time": "00:00",
            "status": "finished",
            "broadcasts": [{"channel": "نظام أثير", "commentator": "إصلاح الطوارئ"}]
        })
        return matches_list

if __name__ == "__main__":
    final_data = get_atheer_genius_data()
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": final_data,
        "custom_ad": {"is_active": False}
    }
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print("✅ تم تنفيذ خطة كشف الأخطاء بنجاح!")
