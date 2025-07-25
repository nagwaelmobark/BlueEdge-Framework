#!/usr/bin/env python3
"""
BlueEdge Framework - Duplicate Detection Module (Fixed Version)
==============================================================

Main module for Arabic name duplicate detection with proper imports.
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
            """Calculate similarity between two names."""
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
    
    def calculate_similarity(self, name1, name2):
        """
        Calculate similarity score between two names.
        
        Args:
            name1 (str): First name
            name2 (str): Second name
            
        Returns:
            float: Similarity score between 0.0 and 1.0
        """
        return self.similarity_calculator.calculate_name_similarity(name1, name2)
    
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
        
        # Check each component
        first_sim = self.similarity_calculator.calculate_name_similarity(first1, first2) if first1 and first2 else 0
        middle_sim = self.similarity_calculator.calculate_name_similarity(middle1, middle2) if middle1 and middle2 else 1  # Assume match if empty
        last_sim = self.similarity_calculator.calculate_name_similarity(last1, last2) if last1 and last2 else 0
        
        # Check nicknames
        if self.check_nicknames(first1, first2):
            first_sim = 0.9  # High similarity for nicknames
        
        # Check abbreviations
        if self.check_abbreviations(first1, first2):
            first_sim = 0.95  # Very high similarity for abbreviations
        
        # All components must be above threshold
        threshold_sim = 1.0 - self.threshold  # Convert to similarity (0.75 for threshold 0.25)
        
        return (first_sim >= threshold_sim and 
                middle_sim >= threshold_sim and 
                last_sim >= threshold_sim)
    
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
        # Check for honorific prefixes
        orig1, orig2 = name1.upper(), name2.upper()
        if any(h in orig1 for h in self.honorifics) or any(h in orig2 for h in self.honorifics):
            if self.normalize_name(name1) == self.normalize_name(name2):
                return "honorific_prefixes"
        
        # Check for abbreviations
        norm1, norm2 = self.normalize_name(name1), self.normalize_name(name2)
        if self.check_abbreviations(norm1.split()[0] if norm1.split() else "", 
                                   norm2.split()[0] if norm2.split() else ""):
            return "name_abbreviations"
        
        # Check for nicknames
        first1, _, _ = self.split_name_components(name1)
        first2, _, _ = self.split_name_components(name2)
        if self.check_nicknames(first1, first2):
            return "common_nicknames"
        
        # Check for split names (different number of components)
        parts1 = norm1.split()
        parts2 = norm2.split()
        if len(parts1) != len(parts2):
            return "split_names"
        
        # Check for obvious misspellings (very low similarity but same structure)
        similarity = self.similarity_calculator.calculate_name_similarity(norm1, norm2)
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