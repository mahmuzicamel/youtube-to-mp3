"""
Test fixtures and utilities for YouTube to MP3 tests
"""
import pytest
import tempfile
import os
from unittest.mock import Mock, MagicMock
from fastapi.testclient import TestClient
from io import BytesIO


@pytest.fixture
def temp_file():
    """Create a temporary file for testing"""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        yield tmp.name
    # Cleanup
    if os.path.exists(tmp.name):
        os.remove(tmp.name)


@pytest.fixture
def sample_mp3_data():
    """Sample MP3 data for testing"""
    # This is just fake data for testing
    return b'\xff\xfb\x90\x00' + b'fake mp3 data' * 100


@pytest.fixture
def sample_m4a_data():
    """Sample M4A data for testing"""
    # This is just fake data for testing
    return b'fake m4a data' * 100


@pytest.fixture
def mock_youtube_video():
    """Mock YouTube video object"""
    mock_video = Mock()
    mock_video.title = "Test Video Title"
    mock_video.length = 180  # 3 minutes
    mock_video.views = 1000000
    mock_video.author = "Test Author"
    return mock_video


@pytest.fixture
def mock_youtube_stream():
    """Mock YouTube stream object"""
    mock_stream = Mock()
    mock_stream.filesize = 5000000  # 5MB
    mock_stream.mime_type = "audio/mp4"
    mock_stream.abr = "128kbps"
    
    def mock_stream_to_buffer(buffer):
        # Simulate writing data to buffer
        buffer.write(b'fake audio data')
        buffer.flush()
    
    mock_stream.stream_to_buffer = mock_stream_to_buffer
    return mock_stream


@pytest.fixture
def mock_youtube_success(mock_youtube_video, mock_youtube_stream):
    """Mock successful YouTube object with video and stream"""
    mock_yt = Mock()
    mock_yt.title = mock_youtube_video.title
    mock_yt.length = mock_youtube_video.length
    mock_yt.views = mock_youtube_video.views
    mock_yt.author = mock_youtube_video.author
    
    mock_yt.streams.get_audio_only.return_value = mock_youtube_stream
    return mock_yt


@pytest.fixture
def mock_youtube_no_stream(mock_youtube_video):
    """Mock YouTube object with no available audio stream"""
    mock_yt = Mock()
    mock_yt.title = mock_youtube_video.title
    mock_yt.streams.get_audio_only.return_value = None
    return mock_yt


@pytest.fixture
def mock_audio_clip():
    """Mock MoviePy AudioFileClip"""
    mock_clip = Mock()
    mock_clip.duration = 180.5  # 3 minutes 30 seconds
    mock_clip.fps = 44100
    
    def mock_write_audiofile(filename, *args, **kwargs):
        # Create a fake MP3 file
        with open(filename, 'wb') as f:
            f.write(b'\xff\xfb\x90\x00' + b'fake mp3 data' * 100)
    
    mock_clip.write_audiofile = mock_write_audiofile
    mock_clip.close = Mock()
    return mock_clip


class MockNamedTemporaryFile:
    """Mock NamedTemporaryFile for testing"""
    
    def __init__(self, suffix="", delete=True):
        self.suffix = suffix
        self.delete = delete
        self.name = f"/tmp/test{suffix}"
        self.closed = False
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.delete:
            # Create the file so it exists for testing
            with open(self.name, 'wb') as f:
                f.write(b'test data')
    
    def write(self, data):
        pass
    
    def flush(self):
        pass


@pytest.fixture
def mock_temp_file():
    """Mock NamedTemporaryFile"""
    return MockNamedTemporaryFile


class TestDataFactory:
    """Factory for creating test data"""
    
    @staticmethod
    def create_youtube_url(video_id="dQw4w9WgXcQ"):
        """Create a YouTube URL for testing"""
        return f"https://www.youtube.com/watch?v={video_id}"
    
    @staticmethod
    def create_invalid_urls():
        """Create a list of invalid URLs for testing"""
        return [
            "",
            "not-a-url",
            "http://not-youtube.com",
            "https://youtube.com/invalid",
            "ftp://youtube.com/watch?v=test",
            "https://www.youtube.com/",  # No video ID
            "https://www.youtube.com/watch",  # No video ID
        ]
    
    @staticmethod
    def create_valid_urls():
        """Create a list of valid YouTube URLs for testing"""
        return [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
        ]


@pytest.fixture
def test_data_factory():
    """Test data factory fixture"""
    return TestDataFactory()


def create_test_client():
    """Create a test client for the FastAPI app"""
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from youtube_to_mp3 import app
        return TestClient(app)
    except ImportError:
        return None


@pytest.fixture
def api_client():
    """FastAPI test client fixture"""
    client = create_test_client()
    if client is None:
        pytest.skip("Could not import app for testing")
    return client


def assert_mp3_response(response):
    """Assert that response is a valid MP3 response"""
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert "Content-Disposition" in response.headers
    assert "attachment" in response.headers["Content-Disposition"]
    assert ".mp3" in response.headers["Content-Disposition"]


def assert_error_response(response, expected_status=500):
    """Assert that response is a valid error response"""
    assert response.status_code == expected_status
    assert response.headers["content-type"] == "application/json"
    
    error_data = response.json()
    assert "detail" in error_data
    assert isinstance(error_data["detail"], str)
    assert len(error_data["detail"]) > 0