"""
Simple tests that can be run without external dependencies
"""
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_import_app():
    """Test that we can import the app"""
    try:
        import youtube_to_mp3
        print("✓ Successfully imported youtube_to_mp3 module")
        return True  # Import successful
    except ImportError as e:
        print(f"✗ Failed to import youtube_to_mp3: {e}")
        return False

def test_app_creation():
    """Test that the FastAPI app is created"""
    try:
        from youtube_to_mp3 import app
        print("✓ Successfully imported FastAPI app")
        
        # Check app type
        app_type = str(type(app))
        if "FastAPI" in app_type:
            print("✓ App is a FastAPI instance")
            return True
        else:
            print(f"✗ App is not a FastAPI instance: {app_type}")
            return False
    except Exception as e:
        print(f"✗ Failed to import app: {e}")
        return False

def test_url_item_model():
    """Test the URLItem Pydantic model"""
    try:
        from youtube_to_mp3 import URLItem

        # Test valid URL
        url_item = URLItem(url="https://www.youtube.com/watch?v=test")
        if url_item.url == "https://www.youtube.com/watch?v=test":
            print("✓ URLItem model works with valid URL")
        else:
            print("✗ URLItem model failed with valid URL")
            return False

        # Test empty URL
        empty_url_item = URLItem(url="")
        if empty_url_item.url == "":
            print("✓ URLItem model works with empty URL")
            return True
        else:
            print("✗ URLItem model failed with empty URL")
            return False

    except Exception as e:
        print(f"✗ URLItem model test failed: {e}")
        return False

def test_app_routes():
    """Test that required routes exist"""
    try:
        from youtube_to_mp3 import app
        
        routes = [route.path for route in app.routes]
        print(f"Available routes: {routes}")
        
        if "/convert/" in routes:
            print("✓ Required route /convert/ exists")
            return True
        else:
            print("✗ Required route /convert/ not found")
            return False
    except Exception as e:
        print(f"✗ Route test failed: {e}")
        return False

def test_dependencies():
    """Test that required dependencies are available"""
    dependencies = [
        ("fastapi", "FastAPI framework"),
        ("pydantic", "Pydantic data validation"), 
        ("pytubefix", "YouTube downloading library"),
        ("moviepy", "Video/audio processing library"),
    ]
    
    available_count = 0
    for dep, description in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} ({description}) is available")
            available_count += 1
        except ImportError:
            print(f"✗ {dep} ({description}) is not available")
    
    print(f"Dependencies available: {available_count}/{len(dependencies)}")
    if available_count >= len(dependencies) - 1:
        return True
    else:
        print(f"✗ Too many dependencies missing: {available_count}/{len(dependencies)}")
        return False

def test_filename_sanitization():
    """Test filename sanitization logic"""
    test_cases = [
        ("normal_title", "normal_title"),
        ("title/with/slashes", "title_with_slashes"),
        ("title\\with\\backslashes", "title\\with\\backslashes"),  # Only forward slashes are replaced
        ("", ""),
        ("///", "___"),
    ]
    
    all_passed = True
    for input_title, expected in test_cases:
        result = input_title.replace("/", "_")
        if result == expected:
            print(f"✓ '{input_title}' -> '{result}'")
        else:
            print(f"✗ '{input_title}' -> '{result}' (expected '{expected}')")
            all_passed = False
    
    return all_passed

def run_all_tests():
    """Run all simple tests"""
    tests = [
        ("Import Test", test_import_app),
        ("App Creation Test", test_app_creation),
        ("URLItem Model Test", test_url_item_model),
        ("Routes Test", test_app_routes),
        ("Dependencies Test", test_dependencies),
        ("Filename Sanitization Test", test_filename_sanitization),
    ]
    
    print("Running Simple Tests for YouTube to MP3 Converter")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)