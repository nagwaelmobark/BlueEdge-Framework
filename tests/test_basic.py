"""
Basic tests for BlueEdge framework
"""
import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestBlueEdgeBasic(unittest.TestCase):
    """Basic functionality tests"""
    
    def test_project_structure(self):
        """Test that project structure is correct"""
        required_files = [
            'README.md',
            'LICENSE', 
            'requirements.txt',
            'main.py',
            'CHANGELOG.md'
        ]
        
        for file in required_files:
            self.assertTrue(os.path.exists(file), f"Required file {file} exists")
    
    def test_src_structure(self):
        """Test that src directory structure is correct"""
        required_dirs = [
            'src/algorithms',
            'src/ui',
            'src/utils'
        ]
        
        for dir_path in required_dirs:
            self.assertTrue(os.path.exists(dir_path), f"Required directory {dir_path} exists")
    
    def test_core_files_exist(self):
        """Test that core files exist in correct locations"""
        core_files = [
            'src/algorithms/duplicate_detector.py',
            'src/ui/blueedge_mobile_app.py',
            'src/utils/firebase_config.py'
        ]
        
        for file_path in core_files:
            self.assertTrue(os.path.exists(file_path), f"Core file {file_path} exists")
    
    def test_import_modules(self):
        """Test that core modules can be imported"""
        try:
            # Test imports with new structure
            from src.algorithms import duplicate_detector
            from src.utils import firebase_config
            from src.utils import performance_monitor
            self.assertTrue(True, "Core modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import core modules: {e}")

class TestBlueEdgeAlgorithms(unittest.TestCase):
    """Test BlueEdge algorithms"""
    
    def test_similarity_calculation(self):
        """Test basic similarity calculation"""
        try:
            from src.algorithms.similarity import calculate_similarity
            
            # Test identical strings
            similarity = calculate_similarity("Mohammed", "Mohammed")
            self.assertEqual(similarity, 1.0, "Identical strings should have 100% similarity")
            
            # Test different strings
            similarity = calculate_similarity("Mohammed", "Ahmad")
            self.assertLess(similarity, 1.0, "Different strings should have less than 100% similarity")
            
        except ImportError:
            self.skipTest("Similarity module not available for testing")
        except Exception as e:
            self.fail(f"Similarity calculation failed: {e}")

def run_tests():
    """Run all tests"""
    print("🧪 Running BlueEdge Basic Tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestBlueEdgeBasic))
    suite.addTest(unittest.makeSuite(TestBlueEdgeAlgorithms))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests passed!")
        print(f"✅ Ran {result.testsRun} tests successfully")
    else:
        print("❌ Some tests failed:")
        print(f"   • Tests run: {result.testsRun}")
        print(f"   • Failures: {len(result.failures)}")
        print(f"   • Errors: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_tests() 
