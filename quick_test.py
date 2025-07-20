"""
BlueEdge Framework - Quick Test
==============================
اختبار شامل لجميع مكونات النظام
"""

import sys
import os
import time

print("🚀 بدء الاختبار الشامل لإطار BlueEdge")
print("=" * 50)

# اختبار 1: استيراد المكتبات
print("\n📚 اختبار 1: استيراد المكتبات...")
try:
    sys.path.append('src')
    from similarity import NameSimilarityCalculator, quick_similarity
    from duplicate_detector import BlueEdgeDuplicateDetector, detect_duplicates_quick
    from data_anonymizer import BlueEdgeDataAnonymizer
    print("   ✅ تم استيراد جميع المكتبات بنجاح")
except Exception as e:
    print(f"   ❌ خطأ في الاستيراد: {e}")
    sys.exit(1)

# اختبار 2: خوارزميات التشابه
print("\n🧮 اختبار 2: خوارزميات التشابه...")
calculator = NameSimilarityCalculator()

test_cases = [
    ("MOHAMMED", "MOHAMMAD", "اختلاف إملاء"),
    ("AHMED", "AHMAD", "اختلاف إملاء"), 
    ("MOHAMMED", "HAMADA", "اسم مستعار"),
    ("SARA", "SOSO", "اسم مستعار"),
    ("MOHAMMED", "SARA", "أسماء مختلفة")
]

similarity_scores = []
for name1, name2, description in test_cases:
    result = calculator.calculate_name_similarity(name1, name2)
    score = result['similarity_score']
    is_duplicate = result['is_duplicate']
    
    status = "✅" if (is_duplicate and score > 0.5) or (not is_duplicate and score < 0.5) else "⚠️"
    print(f"   {status} {name1} ↔ {name2}: {score:.3f} ({description})")
    similarity_scores.append(score)

avg_si 
