"""
BlueEdge Framework - Similarity Algorithms
==========================================

تطبيق خوارزميات حساب التشابه بين الأسماء العربية
استخدام Levenshtein Distance مع threshold = 0.25

Based on research paper: BlueEdge Framework
Author: Generated for Reproduction Package
"""

import re
from typing import Tuple, List, Dict, Union

class NameSimilarityCalculator:
    """
    حاسبة التشابه بين الأسماء العربية
    تطبق خوارزمية Levenshtein Distance مع تحسينات للأسماء العربية
    """
    
    def __init__(self, threshold: float = 0.25):
        """
        تهيئة الحاسبة
        
        Args:
            threshold (float): عتبة التشابه (default: 0.25 كما في البحث)
        """
        self.threshold = threshold
        self.honorifics = {
            'DR.', 'DR', 'DOCTOR', 'PROF.', 'PROF', 'PROFESSOR',
            'MR.', 'MR', 'MRS.', 'MRS', 'MISS', 'MS.', 'MS', 
            'SIR', 'MADAM'
        }
        self.nicknames = {
            'MOHAMMED': ['HAMADA', 'HAMMOUDA'],
            'IBRAHIM': ['BEBO'],
            'ABDULRAHMAN': ['ABDO'],
            'ABDULLAH': ['ABDU'],
            'SARA': ['SOSO'],
            'FATIMA': ['FIFI'],
            'AHMED': ['HAMADA'],
            'OMAR': ['OMARY'],
            'HASSAN': ['HASO']
        }
    
    def levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        حساب Levenshtein Distance بين نصين
        
        Args:
            s1, s2: النصوص المراد مقارنتها
            
        Returns:
            int: المسافة بين النصين
        """
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost of substitution (0.5 as mentioned in paper)
                cost = 0 if c1 == c2 else 0.5
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + cost
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def normalize_similarity(self, distance: float, max_length: int) -> float:
        """
        تطبيع نتيجة التشابه
        
        Args:
            distance: المسافة المحسوبة
            max_length: الطول الأقصى للنصين
            
        Returns:
            float: نسبة التشابه (0-1)
        """
        if max_length == 0:
            return 1.0
        
        similarity = 1 - (distance / max_length)
        return max(0.0, min(1.0, similarity))
    
    def preprocess_name(self, name: str) -> str:
        """
        تنظيف وتجهيز الاسم للمقارنة
        
        Args:
            name: الاسم الأصلي
            
        Returns:
            str: الاسم بعد التنظيف
        """
        if not name:
            return ""
        
        # تحويل لأحرف كبيرة
        name = name.upper().strip()
        
        # إزالة الألقاب الشرفية
        for honorific in self.honorifics:
            if name.startswith(honorific):
                name = name[len(honorific):].strip()
                break
        
        # إزالة الرموز الخاصة والأرقام
        name = re.sub(r'[^A-Z\s]', '', name)
        
        # إزالة المسافات الزائدة
        name = ' '.join(name.split())
        
        return name
    
    def expand_abbreviations(self, name: str) -> str:
        """
        توسيع الاختصارات
        
        Args:
            name: الاسم مع الاختصارات
            
        Returns:
            str: الاسم بعد توسيع الاختصارات
        """
        # التحقق من الاختصارات (مثل M. → MOHAMMED)
        if name.endswith('.') and len(name) <= 3:
            abbreviation_map = {
                'M.': 'MOHAMMED',
                'A.': 'AHMED',
                'S.': 'SARA',
                'F.': 'FATIMA',
                'O.': 'OMAR',
                'K.': 'KHALED',
                'N.': 'NOOR'
            }
            return abbreviation_map.get(name, name)
        
        return name
    
    def check_nicknames(self, name1: str, name2: str) -> bool:
        """
        فحص الأسماء المستعارة
        
        Args:
            name1, name2: الأسماء المراد مقارنتها
            
        Returns:
            bool: True إذا كانا نفس الشخص (اسم مستعار)
        """
        for original, nicks in self.nicknames.items():
            if (name1 == original and name2 in nicks) or \
               (name2 == original and name1 in nicks):
                return True
        return False
    
    def calculate_name_similarity(self, name1: str, name2: str) -> Dict[str, Union[float, bool]]:
        """
        حساب التشابه بين اسمين مع التفاصيل
        
        Args:
            name1, name2: الأسماء المراد مقارنتها
            
        Returns:
            dict: نتيجة مفصلة للمقارنة
        """
        # تنظيف الأسماء
        clean1 = self.preprocess_name(name1)
        clean2 = self.preprocess_name(name2)
        
        # توسيع الاختصارات
        expanded1 = self.expand_abbreviations(clean1)
        expanded2 = self.expand_abbreviations(clean2)
        
        # فحص الأسماء المستعارة
        is_nickname = self.check_nicknames(expanded1, expanded2)
        
        # حساب المسافة
        distance = self.levenshtein_distance(expanded1, expanded2)
        max_length = max(len(expanded1), len(expanded2))
        similarity = self.normalize_similarity(distance, max_length)
        
        # تحديد ما إذا كانا متطابقين
        is_duplicate = similarity >= (1 - self.threshold) or is_nickname
        
        return {
            'original_names': (name1, name2),
            'cleaned_names': (clean1, clean2),
            'expanded_names': (expanded1, expanded2),
            'levenshtein_distance': distance,
            'similarity_score': similarity,
            'is_nickname': is_nickname,
            'is_duplicate': is_duplicate,
            'threshold_used': self.threshold
        }
    
    def compare_full_names(self, record1: Dict, record2: Dict) -> Dict[str, Union[float, bool]]:
        """
        مقارنة الأسماء الكاملة بين سجلين
        
        Args:
            record1, record2: السجلات المراد مقارنتها
            
        Returns:
            dict: نتيجة المقارنة الشاملة
        """
        # استخراج أجزاء الأسماء
        first1 = record1.get('First Name', '')
        middle1 = record1.get('middle name', '')
        last1 = record1.get('last Name', '')
        
        first2 = record2.get('First Name', '')
        middle2 = record2.get('middle name', '')
        last2 = record2.get('last Name', '')
        
        # مقارنة كل جزء
        first_result = self.calculate_name_similarity(first1, first2)
        middle_result = self.calculate_name_similarity(middle1, middle2)
        last_result = self.calculate_name_similarity(last1, last2)
        
        # حساب التشابه الإجمالي
        similarities = [
            first_result['similarity_score'],
            middle_result['similarity_score'], 
            last_result['similarity_score']
        ]
        
        # التحقق من شرط BlueEdge: جميع المسافات <= threshold
        all_similar = all(sim >= (1 - self.threshold) for sim in similarities)
        
        # فحص الأسماء المستعارة
        has_nickname = any([
            first_result['is_nickname'],
            middle_result['is_nickname'],
            last_result['is_nickname']
        ])
        
        # النتيجة النهائية
        is_duplicate = all_similar or has_nickname
        
        return {
            'first_name_comparison': first_result,
            'middle_name_comparison': middle_result,
            'last_name_comparison': last_result,
            'overall_similarity': sum(similarities) / len(similarities),
            'all_parts_similar': all_similar,
            'has_nickname_match': has_nickname,
            'final_decision': is_duplicate,
            'confidence_score': min(similarities) if all_similar else max(similarities)
        }


# دوال مساعدة للاستخدام السريع
def quick_similarity(name1: str, name2: str, threshold: float = 0.25) -> float:
    """
    حساب سريع للتشابه بين اسمين
    
    Args:
        name1, name2: الأسماء
        threshold: العتبة
        
    Returns:
        float: نسبة التشابه
    """
    calculator = NameSimilarityCalculator(threshold)
    result = calculator.calculate_name_similarity(name1, name2)
    return result['similarity_score']


def is_duplicate_quick(record1: Dict, record2: Dict, threshold: float = 0.25) -> bool:
    """
    فحص سريع للتطابق بين سجلين
    
    Args:
        record1, record2: السجلات
        threshold: العتبة
        
    Returns:
        bool: True إذا كانا متطابقين
    """
    calculator = NameSimilarityCalculator(threshold)
    result = calculator.compare_full_names(record1, record2)
    return result['final_decision']


# اختبار سريع
if __name__ == "__main__":
    # اختبار الخوارزمية
    calculator = NameSimilarityCalculator()
    
    # اختبار 1: Different spelling
    result1 = calculator.calculate_name_similarity("MOHAMMED", "MOHAMMAD")
    print(f"MOHAMMED vs MOHAMMAD: {result1['similarity_score']:.3f} (Duplicate: {result1['is_duplicate']})")
    
    # اختبار 2: Nickname
    result2 = calculator.calculate_name_similarity("MOHAMMED", "HAMADA")
    print(f"MOHAMMED vs HAMADA: {result2['similarity_score']:.3f} (Nickname: {result2['is_nickname']})")
    
    # اختبار 3: Full name comparison
    record1 = {'First Name': 'MOHAMMED', 'middle name': 'AHMED', 'last Name': 'HASSAN'}
    record2 = {'First Name': 'MOHAMMAD', 'middle name': 'AHMAD', 'last Name': 'HASAN'}
    
    full_result = calculator.compare_full_names(record1, record2)
    print(f"Full name comparison: {full_result['final_decision']} (Confidence: {full_result['confidence_score']:.3f})") 
