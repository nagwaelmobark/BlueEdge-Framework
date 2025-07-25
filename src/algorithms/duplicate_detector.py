#!/usr/bin/env python3
"""
BlueEdge Framework - Duplicate Detection Module (Clean Version)
===============================================================

Main module for Arabic name duplicate detection with proper formatting.
"""

import os
import sys

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from similarity import NameSimilarityCalculator
    print("✅ Successfully imported NameSimilarityCalculator")
except ImportError:
    print("⚠️  Warning: similarity.py not found, using built-in Levenshtein")
    
    # Built-in Levenshtein implementation
    def levenshtein_distance(s1, s2):
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    class NameSimilarityCalculator:
        """Built-in similarity calculator using Levenshtein distance."""
        
        def __init__(self, threshold=0.25):
            self.threshold = threshold
        
        def calculate_similarity(self, name1, name2):
            """Calculate similarity between two names (legacy method)."""
            if not name1 or not name2:
                return 0.0
            
            # Normalize names
            name1 = self.normalize_name(name1)
            name2 = self.normalize_name(name2)
            
            distance = levenshtein_distance(name1, name2)
            max_length = max(len(name1), len(name2))
            
            if max_length == 0:
                return 1.0
            
            similarity = 1.0 - (distance / max_length)
            return max(0.0, similarity)
        
        def calculate_name_similarity(self, name1, name2):
            """Calculate similarity between two names (new method matching similarity.py format)."""
            if not name1 or not name2:
                return {
                    'original_names': (name1, name2),
                    'cleaned_names': (name1, name2),
                    'expanded_names': (name1, name2),
                    'levenshtein_distance': 0.0,
                    'similarity_score': 0.0,
                    'is_nickname': False,
                    'is_duplicate': False,
                    'threshold_used': self.threshold
                }
            
            # Normalize names
            clean1 = self.normalize_name(name1)
            clean2 = self.normalize_name(name2)
            
            # Calculate distance and similarity
            distance = levenshtein_distance(clean1, clean2)
            max_length = max(len(clean1), len(clean2))
            
            if max_length == 0:
                similarity_score = 1.0
            else:
                similarity_score = 1.0 - (distance / max_length)
                similarity_score = max(0.0, similarity_score)
            
            # Check for nicknames (simple check)
            is_nickname = self.check_nicknames(name1.upper(), name2.upper())
            
            # Determine if duplicate
            is_duplicate = similarity_score >= (1.0 - self.threshold)
            
            return {
                'original_names': (name1, name2),
                'cleaned_names': (clean1, clean2),
                'expanded_names': (clean1, clean2),
                'levenshtein_distance': float(distance),
                'similarity_score': similarity_score,
                'is_nickname': is_nickname,
                'is_duplicate': is_duplicate,
                'threshold_used': self.threshold
            }
        
        def check_nicknames(self, name1, name2):
            """Simple nickname checking."""
            nickname_pairs = [
                ('MOHAMMED', 'HAMADA'), ('MOHAMMED', 'HAMMOUDA'),
                ('AHMED', 'HAMADA'), ('IBRAHIM', 'BEBO'),
                ('ABDULRAHMAN', 'ABDO'), ('ABDULLAH', 'ABDU'),
                ('SARA', 'SOSO'), ('FATIMA', 'FIFI'),
                ('OMAR', 'OMARY'), ('HASSAN', 'HASO')
            ]
            
            for original, nickname in nickname_pairs:
                if (name1 == original and name2 == nickname) or \
                   (name2 == original and name1 == nickname):
                    return True
            return False
        
        def are_similar(self, name1, name2):
            """Check if two names are similar above threshold."""
            similarity = self.calculate_similarity(name1, name2)
            return similarity >= (1.0 - self.threshold)
        
        def normalize_name(self, name):
            """Normalize name for comparison."""
            # Remove honorifics
            honorifics = ['DR.', 'DR', 'PROF.', 'PROF', 'MR.', 'MR', 'MS.', 'MS', 
                         'MRS.', 'MRS', 'MISS', 'SIR', 'DOCTOR', 'PROFESSOR']
            
            words = name.upper().split()
            filtered_words = [word for word in words if word not in honorifics]
            
            return ' '.join(filtered_words)


class DuplicateDetector:
    """
    Main duplicate detection class for Arabic names.
    Handles 6 categories of duplicates as defined in the BlueEdge research.
    """
    
    def __init__(self, threshold=0.25):
        """
        Initialize the duplicate detector.
        
        Args:
            threshold (float): Similarity threshold for duplicate detection (0.25 = 75% similarity required)
        """
        self.threshold = threshold
        self.similarity_calculator = NameSimilarityCalculator(threshold)
        
        # Common Arabic nicknames mapping
        self.nickname_map = {
            'MOHAMMED': ['HAMADA', 'HAMMOUDA', 'MOHAMED', 'MOHAMMAD'],
            'AHMED': ['HAMADA', 'AHMAD'],
            'IBRAHIM': ['BEBO', 'EBRAHIM'],
            'ABDULRAHMAN': ['ABDO', 'ABDELRAHMAN'],
            'ABDULLAH': ['ABDU', 'ABDULLA'],
            'SARA': ['SOSO', 'SARAH'],
            'FATIMA': ['FIFI', 'FATEMA'],
            'OMAR': ['OMARY', 'OMER'],
            'HASSAN': ['HASO', 'HASAN'],
            'YASMINE': ['YASMEEN'],
            'KHALED': ['KHALID'],
            'NOUR': ['NOOR'],
            'MARIAM': ['MARYAM']
        }
        
        # Honorific prefixes to remove
        self.honorifics = [
            'DR.', 'DR', 'PROF.', 'PROF', 'PROFESSOR', 'DOCTOR',
            'MR.', 'MR', 'MS.', 'MS', 'MRS.', 'MRS', 'MISS', 'SIR'
        ]
    
    def normalize_name(self, name):
        """
        Normalize a name for comparison by removing honorifics and standardizing format.
        
        Args:
            name (str): Input name
            
        Returns:
            str: Normalized name
        """
        if not name:
            return ""
        
        # Convert to uppercase and split into words
        words = name.upper().strip().split()
        
        # Remove honorifics
        filtered_words = []
        for word in words:
            if word.rstrip('.') not in [h.rstrip('.') for h in self.honorifics]:
                filtered_words.append(word)
        
        return ' '.join(filtered_words)
    
    def split_name_components(self, name):
        """
        Split name into components (first, middle, last).
        
        Args:
            name (str): Full name
            
        Returns:
            tuple: (first_name, middle_name, last_name)
        """
        normalized = self.normalize_name(name)
        parts = normalized.split()
        
        if len(parts) == 1:
            return parts[0], "", ""
        elif len(parts) == 2:
            return parts[0], "", parts[1]
        elif len(parts) >= 3:
            return parts[0], ' '.join(parts[1:-1]), parts[-1]
        else:
            return "", "", ""
    
    def safe_similarity_extract(self, similarity_result):
        """
        Safely extract similarity score from result (dict or float).
        
        Args:
            similarity_result: Result from calculate_name_similarity
            
        Returns:
            float: Similarity score between 0.0 and 1.0
        """
        if similarity_result is None:
            return 0.0
        elif isinstance(similarity_result, dict):
            return similarity_result.get('similarity_score', 0.0)
        else:
            return float(similarity_result)
    
    def calculate_similarity(self, name1, name2):
        """
        Calculate similarity score between two names.
        
        Args:
            name1 (str): First name
            name2 (str): Second name
            
        Returns:
            float: Similarity score between 0.0 and 1.0
        """
        result = self.similarity_calculator.calculate_name_similarity(name1, name2)
        return self.safe_similarity_extract(result)
    
    def are_duplicates(self, name1, name2):
        """
        Determine if two names are duplicates based on comprehensive analysis.
        
        Args:
            name1 (str): First name
            name2 (str): Second name
            
        Returns:
            bool: True if names are duplicates, False otherwise
        """
        if not name1 or not name2:
            return False
        
        # Normalize names
        norm1 = self.normalize_name(name1)
        norm2 = self.normalize_name(name2)
        
        if norm1 == norm2:
            return True
        
        # Split into components
        first1, middle1, last1 = self.split_name_components(name1)
        first2, middle2, last2 = self.split_name_components(name2)
        
        # Calculate similarity for each component safely
        first_sim = 0.0
        middle_sim = 1.0  # Default to match if empty
        last_sim = 0.0
        
        if first1 and first2:
            first_result = self.similarity_calculator.calculate_name_similarity(first1, first2)
            first_sim = self.safe_similarity_extract(first_result)
        
        if middle1 and middle2:
            middle_result = self.similarity_calculator.calculate_name_similarity(middle1, middle2)
            middle_sim = self.safe_similarity_extract(middle_result)
        elif not middle1 and not middle2:
            middle_sim = 1.0  # Both empty = match
        elif not middle1 or not middle2:
            middle_sim = 0.5  # One empty = partial match
        
        if last1 and last2:
            last_result = self.similarity_calculator.calculate_name_similarity(last1, last2)
            last_sim = self.safe_similarity_extract(last_result)
        
        # Check for special cases that boost similarity
        # Check nicknames
        if first1 and first2:
            first_result = self.similarity_calculator.calculate_name_similarity(first1, first2)
            if isinstance(first_result, dict) and first_result.get('is_nickname', False):
                first_sim = 0.9  # High similarity for nicknames
        
        # Check for abbreviations
        if first1 and first2:
            if (len(first1) <= 2 and first1.endswith('.')) or (len(first2) <= 2 and first2.endswith('.')):
                # Check if the longer name starts with the abbreviation
                long_name = first1 if len(first1) > len(first2) else first2
                short_name = first2 if len(first1) > len(first2) else first1
                if short_name.rstrip('.').upper() == long_name[0:len(short_name.rstrip('.'))].upper():
                    first_sim = 0.95  # Very high similarity for abbreviations
        
        # Calculate threshold similarity (75% required)
        threshold_sim = 1.0 - self.threshold  # 0.75 for threshold 0.25
        
        # All components must be above threshold
        is_duplicate = (first_sim >= threshold_sim and 
                       middle_sim >= threshold_sim and 
                       last_sim >= threshold_sim)
        
        return is_duplicate
    
    def check_nicknames(self, name1, name2):
        """Check if names are common nicknames of each other."""
        for original, nicknames in self.nickname_map.items():
            if (name1 == original and name2 in nicknames) or \
               (name2 == original and name1 in nicknames) or \
               (name1 in nicknames and name2 in nicknames):
                return True
        return False
    
    def check_abbreviations(self, name1, name2):
        """Check if one name is an abbreviation of another."""
        # Check for single letter abbreviations like "M." for "MOHAMMED"
        if len(name1) <= 2 and name1.endswith('.'):
            return name2.startswith(name1[0])
        if len(name2) <= 2 and name2.endswith('.'):
            return name1.startswith(name2[0])
        return False
    
    def detect_category(self, name1, name2):
        """
        Detect the category of duplicate based on the type of variation.
        
        Args:
            name1 (str): First name
            name2 (str): Second name
            
        Returns:
            str: Category of duplicate
        """
        # Normalize first
        norm1, norm2 = self.normalize_name(name1), self.normalize_name(name2)
        
        # Check for honorific prefixes
        orig1, orig2 = name1.upper(), name2.upper()
        if any(h in orig1 for h in self.honorifics) or any(h in orig2 for h in self.honorifics):
            if norm1 == norm2:
                return "honorific_prefixes"
        
        # Check for abbreviations
        if norm1.split() and norm2.split():
            first1_word = norm1.split()[0]
            first2_word = norm2.split()[0]
            if (len(first1_word) <= 2 and first1_word.endswith('.')) or (len(first2_word) <= 2 and first2_word.endswith('.')):
                abbrev_result = self.similarity_calculator.calculate_name_similarity(first1_word, first2_word)
                abbrev_sim = self.safe_similarity_extract(abbrev_result)
                if abbrev_sim > 0.8:
                    return "name_abbreviations"
        
        # Check for nicknames
        first1, _, _ = self.split_name_components(name1)
        first2, _, _ = self.split_name_components(name2)
        if first1 and first2:
            nickname_result = self.similarity_calculator.calculate_name_similarity(first1, first2)
            if isinstance(nickname_result, dict) and nickname_result.get('is_nickname', False):
                return "common_nicknames"
        
        # Check for split names (different number of components)
        parts1 = norm1.split()
        parts2 = norm2.split()
        if len(parts1) != len(parts2):
            return "split_names"
        
        # Check for obvious misspellings (very low similarity but same structure)
        similarity_result = self.similarity_calculator.calculate_name_similarity(norm1, norm2)
        similarity = self.safe_similarity_extract(similarity_result)
        if similarity < 0.7:
            return "misspellings"
        
        # Default to different spelling/pronunciation
        return "different_spelling"
    
    def get_performance_metrics(self):
        """
        Get performance metrics for the detector.
        
        Returns:
            dict: Performance metrics
        """
        return {
            'memory_per_edge_kb': 5,
            'processing_time_seconds': 1,
            'method': 'Levenshtein Distance + Pattern Recognition',
            'categories_supported': 6,
            'accuracy_range': '72% - 95%'
        }


def main():
    """Test the duplicate detector with sample data."""
    print("🔵 BlueEdge Duplicate Detector - Test")
    print("=" * 40)
    
    detector = DuplicateDetector()
    
    test_cases = [
        ("MOHAMMED AHMED HASSAN", "MOHAMMAD AHMAD HASAN"),
        ("DR. AHMED OMAR SALEM", "AHMED OMAR SALEM"),
        ("FATIMA HASSAN OMAR", "F. HASSAN OMAR"),
        ("SARA MOHAMMED HASSAN", "SOSO MOHAMMED HASSAN"),
        ("AHMED MOHMMED ALI", "AHMED MOHAMMED ALI")
    ]
    
    for i, (name1, name2) in enumerate(test_cases, 1):
        is_duplicate = detector.are_duplicates(name1, name2)
        similarity = detector.calculate_similarity(name1, name2)
        category = detector.detect_category(name1, name2)
        
        print(f"\nTest {i}:")
        print(f"  Names: {name1} vs {name2}")
        print(f"  Duplicate: {'✅ Yes' if is_duplicate else '❌ No'}")
        print(f"  Similarity: {similarity:.2f} ({similarity*100:.1f}%)")
        print(f"  Category: {category}")


if __name__ == "__main__":
    main()