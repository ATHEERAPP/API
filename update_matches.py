import requests
import json
from datetime import datetime

def get_simple_data():
    # سنقوم بجلب بيانات تجريبية أولاً للتأكد من أن السيرفر يعمل
    # هذا الرابط سيعطينا بيانات مباريات حقيقية من مصدر مفتوح
    url = "https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            print("✅ الاتصال بالإنترنت ناجح")
            return response.json().get('rounds', [{}])[0].get('matches', [])
        else:
            print(f"❌ خطأ في الاتصال: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ حدث خطأ تقني: {e}")
        return []

if __name__ == "__main__":
    print("🚀 بدء تشغيل الروبوت...")
    matches = get_simple_data()
    
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches_count": len(matches),
        "matches": matches[:10] # نأخذ أول 10 مباريات فقط للتجربة
    }
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"✅ تم تحديث الملف بنجاح بـ {len(matches)} مباراة")
