"""
BlueEdge Framework - Duplicate Detection Engine (Simplified)
==========================================================
"""

import time
from similarity import NameSimilarityCalculator

class DetectionResult:
    """نتيجة كشف التطابق"""
    def __init__(self, is_duplicate, category, confidence, details, processing_time):
        self.is_duplicate = is_duplicate
        self.category = category
        self.confidence = confidence
        self.details = details
        self.processing_time = processing_time

class BlueEdgeDuplicateDetector:
    """كاشف التطابق المبسط"""
    
    def __init__(self, similarity_threshold=0.25):
        self.similarity_threshold = similarity_threshold
        self.similarity_calculator = NameSimilarityCalculator(similarity_threshold)
    
    def detect_spelling_pronunciation(self, name1, name2):
        """كشف اختلافات النطق والإملاء"""
        start_time = time.time()
        
        # استخدام similarity calculator
        result = self.similarity_calculator.calculate_name_similarity(name1, name2)
        
        processing_time = time.time() - start_time
        
        return DetectionResult(
            is_duplicate=result['is_duplicate'],
            category="DIFFERENT SPELLING AND PRONUNCIATION",
            confidence=result['similarity_score'],
            details=result,
            processing_time=processing_time
        )
    
    def comprehensive_detection(self, record1, record2):
        """كشف شامل مبسط"""
        results = []
        
        # استخراج الاسم الكامل
        full_name1 = record1.get('Full Name', '')
        full_name2 = record2.get('Full Name', '')
        
        if not full_name1 or not full_name2:
            return results
        
        # كشف الإملاء والنطق
        result = self.detect_spelling_pronunciation(full_name1, full_name2)
        results.append(result)
        
        return results
    
    def get_best_match(self, results):
        """اختيار أفضل نتيجة"""
        if not results:
            return DetectionResult(False, "NO_RESULTS", 0.0, {}, 0.0)
        
        # إرجاع أول نتيجة (مبسط)
        return results[0]

# دالة مساعدة
def detect_duplicates_quick(record1, record2):
    """كشف سريع للتطابق"""
    detector = BlueEdgeDuplicateDetector()
    results = detector.comprehensive_detection(record1, record2)
    best_result = detector.get_best_match(results)
    return best_result.is_duplicate

# اختبار
if __name__ == "__main__":
    print("🧪 بدء اختبار كاشف التطابق...")
    
    detector = BlueEdgeDuplicateDetector()
    
    # اختبار بسيط
    test_cases = [
        ("MOHAMMED AHMED HASSAN", "MOHAMMAD AHMAD HASAN"),
        ("AHMED MOHMMED ALI", "AHMED MOHAMMED ALI"),
        ("SARA HASSAN", "SOSO HASSAN"),
    ]
    
    for i, (name1, name2) in enumerate(test_cases, 1):
        print(f"\n--- اختبار {i} ---")
        print(f"الاسم 1: {name1}")
        print(f"الاسم 2: {name2}")
        
        try:
            results = detector.comprehensive_detection(
                {'Full Name': name1}, 
                {'Full Name': name2}
            )
            best = detector.get_best_match(results)
            
            print(f"النتيجة: {'متطابق' if best.is_duplicate else 'غير متطابق'}")
            print(f"الثقة: {best.confidence:.3f}")
            print(f"الفئة: {best.category}")
            
        except Exception as e:
            print(f"خطأ: {e}")
    
    print("\n✅ انتهى الاختبار!")