import json
import random
from datetime import datetime

# 📝 هذا الروبوت يقوم بتحديث النتائج عشوائياً لتجربة الأنيميشن في تطبيقك
def simulate_live_update():
    try:
        # 1. قراءة الملف الحالي
        with open('matches.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 2. تحديث عشوائي للمباريات الموجودة
        for match in data['matches']:
            if match['status'] == 'live':
                # زيادة الدقيقة عشوائياً
                current_min = int(match.get('minute', '10'))
                match['minute'] = str(min(current_min + random.randint(1, 3), 90))
                
                # احتمالية تسجيل هدف (عشوائياً)
                if random.random() > 0.8:  # 20% احتمال حدوث هدف عند كل تحديث
                    score_parts = match['score'].split(' - ')
                    team_a_score = int(score_parts[0])
                    team_b_score = int(score_parts[1])
                    if random.choice([True, False]):
                        team_a_score += 1
                    else:
                        team_b_score += 1
                    match['score'] = f"{team_a_score} - {team_b_score}"

        # 3. حفظ التعديلات
        with open('matches.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print("✅ الروبوت قام بتحديث النتائج عشوائياً بنجاح!")
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    simulate_live_update()
