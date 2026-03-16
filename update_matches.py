import requests
import json
from datetime import datetime

def get_matches_from_new_api():
    # الحصول على تاريخ اليوم بتنسيق YYYY-MM-DD
    today = datetime.now().strftime("%Y-%m-%d")
    
    # الرابط الذي استخرجته مع جعل التاريخ تلقائياً
    api_url = f"https://1tik.social/apimain/soccer/fixtures/date/{today}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://1tik.social/",
        "Accept": "application/json"
    }
    
    try:
        print(f"📡 جاري الاتصال بالمصدر: {api_url}")
        response = requests.get(api_url, headers=headers, timeout=30)
        
        if response.status_code in [200, 304]:
            data = response.json()
            
            # معالجة البيانات: سنفترض أن الـ API يعيد قائمة تحت اسم 'response' أو 'data'
            # سنقوم بحفظ البيانات بالكامل كما هي لتراها في ملف matches.json
            return data
        else:
            print(f"⚠️ فشل الطلب، كود الحالة: {response.status_code}")
            return {"error": "API failed", "code": response.status_code}
            
    except Exception as e:
        print(f"❌ خطأ تقني: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("🏟️ تحديث بيانات تطبيق أثير...")
    result = get_matches_from_new_api()
    
    output = {
        "status": "success",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": "1tik.social",
        "raw_data": result
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print("✅ تم التحديث! افتح ملف matches.json الآن.")
