import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.modules.core.platform_manager import PlatformURLManager


class TestPlatformURLManager(unittest.TestCase):
    def setUp(self):
        self.manager = PlatformURLManager()
    
    def test_get_profile_url(self):
        # Test with existing platform
        url = self.manager.get_profile_url("GitHub", "testuser")
        self.assertIsNotNone(url)
        
        # Test with non-existing platform with fallback
        url = self.manager.get_profile_url("NonExistentPlatform", "testuser", "https://example.com/testuser")
        self.assertEqual(url, "https://example.com/testuser")
        
        # Test with non-existing platform without fallback
        url = self.manager.get_profile_url("NonExistentPlatform", "testuser")
        self.assertEqual(url, "Unknown platform: NonExistentPlatform")
    
    def test_add_platform(self):
        # Add a new platform
        self.manager.add_platform("TestPlatform", "https://test.com/{}", ["testing"])
        
        # Verify it was added
        self.assertIn("TestPlatform", self.manager.platforms)
        self.assertEqual(self.manager.platforms["TestPlatform"], "https://test.com/{}")
        
        # Verify it was added to the category
        self.assertIn("TestPlatform", self.manager.categories["testing"])
    
    def test_remove_platform(self):
        # Add a platform to remove
        self.manager.add_platform("TestPlatform", "https://test.com/{}", ["testing"])
        
        # Remove it
        result = self.manager.remove_platform("TestPlatform")
        
        # Verify it was removed
        self.assertTrue(result)
        self.assertNotIn("TestPlatform", self.manager.platforms)
        self.assertNotIn("TestPlatform", self.manager.categories["testing"])
    
    def test_get_platforms_by_category(self):
        # Get platforms in a category
        social_platforms = self.manager.get_platforms_by_category("social")
        
        # Verify some expected platforms are in the social category
        self.assertIn("Facebook", social_platforms)
        self.assertIn("Twitter", social_platforms)
        self.assertIn("Instagram", social_platforms)


if __name__ == "__main__":
    unittest.main()
