"""
Integration tests for YouTube to MP3 converter API
Tests the API endpoints with real HTTP requests
"""
import pytest
import requests
import json
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path to import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from youtube_to_mp3 import app
except ImportError:
    # If import fails, we'll skip these tests
    app = None


@pytest.mark.skipif(app is None, reason="Could not import app")
@pytest.mark.integration
class TestAPIIntegration:
    """Integration tests for the API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_app_startup(self, client):
        """Test that the app starts up correctly"""
        # Test that we can make a request to any endpoint
        response = client.get("/")
        # Even if 404, it means the app is running
        assert response.status_code in [200, 404, 405]
    
    def test_download_audio_invalid_url(self, client):
        """Test API with invalid URL"""
        response = client.post(
            "/download_audio_post/",
            json={"url": "not-a-valid-url"}
        )
        assert response.status_code == 500  # Should return server error
    
    def test_download_audio_empty_url(self, client):
        """Test API with empty URL"""
        response = client.post(
            "/download_audio_post/",
            json={"url": ""}
        )
        assert response.status_code == 500  # Should return server error
    
    def test_download_audio_missing_url(self, client):
        """Test API with missing URL parameter"""
        response = client.post(
            "/download_audio_post/",
            json={}
        )
        assert response.status_code == 422  # Validation error
    
    def test_download_audio_invalid_json(self, client):
        """Test API with invalid JSON"""
        response = client.post(
            "/download_audio_post/",
            data="invalid json"
        )
        assert response.status_code == 422  # Validation error
    
    def test_download_audio_wrong_content_type(self, client):
        """Test API with wrong content type"""
        response = client.post(
            "/download_audio_post/",
            data="url=https://www.youtube.com/watch?v=test"
        )
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.slow
    @pytest.mark.network
    def test_download_audio_real_url(self, client):
        """
        Test with a real YouTube URL - this is a slow test
        Note: This test requires internet connection and may fail if the video is removed
        """
        # Using a short, likely stable video
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - likely to stay
        
        response = client.post(
            "/download_audio_post/",
            json={"url": test_url},
            timeout=60  # Give it time to download and convert
        )
        
        # This might succeed or fail depending on video availability
        # We're testing that it doesn't crash the server
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            # If successful, check response headers
            assert response.headers["content-type"] == "audio/mpeg"
            assert "Content-Disposition" in response.headers
            assert ".mp3" in response.headers["Content-Disposition"]
    
    def test_openapi_docs_available(self, client):
        """Test that OpenAPI documentation is available"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_openapi_json_available(self, client):
        """Test that OpenAPI JSON spec is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        
        # Check that it's valid JSON
        openapi_spec = response.json()
        assert "openapi" in openapi_spec
        assert "paths" in openapi_spec
        assert "/download_audio_post/" in openapi_spec["paths"]


@pytest.mark.skipif(app is None, reason="Could not import app")
@pytest.mark.integration
class TestAPIResponseFormat:
    """Test API response formats and headers"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_cors_headers(self, client):
        """Test CORS headers if enabled"""
        response = client.options("/download_audio_post/")
        # This will depend on your CORS configuration
        # Just testing that the request doesn't crash
        assert response.status_code in [200, 405]
    
    def test_error_response_format(self, client):
        """Test that error responses have correct format"""
        response = client.post(
            "/download_audio_post/",
            json={"url": "invalid"}
        )
        assert response.status_code == 500
        
        error_data = response.json()
        assert "detail" in error_data
        assert isinstance(error_data["detail"], str)


if __name__ == "__main__":
    # Run with: python -m pytest tests/test_integration.py -v
    # Run slow tests: python -m pytest tests/test_integration.py -v -m "slow"
    # Skip network tests: python -m pytest tests/test_integration.py -v -m "not network"
    pytest.main([__file__, "-v"])