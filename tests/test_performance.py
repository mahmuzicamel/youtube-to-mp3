"""
Performance tests for YouTube to MP3 converter API
Tests response times, memory usage, and concurrent requests
"""
import pytest
import time
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from youtube_to_mp3 import app
except ImportError:
    app = None


@pytest.mark.skipif(app is None, reason="Could not import app")
@pytest.mark.performance
class TestPerformance:
    """Performance tests for the API"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_response_time_invalid_url(self, client):
        """Test response time for invalid URL (should be fast)"""
        start_time = time.time()
        
        response = client.post(
            "/convert/",
            json={"url": "invalid-url"}
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Should respond quickly for invalid URLs
        assert response_time < 5.0  # Less than 5 seconds
        assert response.status_code == 500
    
    def test_response_time_malformed_request(self, client):
        """Test response time for malformed requests"""
        start_time = time.time()
        
        response = client.post(
            "/convert/",
            json={}
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Validation should be very fast
        assert response_time < 1.0  # Less than 1 second
        assert response.status_code == 422
    
    def test_concurrent_invalid_requests(self, client):
        """Test handling multiple concurrent invalid requests"""
        def make_request():
            start_time = time.time()
            response = client.post(
                "/convert/",
                json={"url": "invalid-url"}
            )
            end_time = time.time()
            return {
                'status_code': response.status_code,
                'response_time': end_time - start_time
            }
        
        # Test with 10 concurrent requests
        num_requests = 10
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in as_completed(futures)]
        
        # All requests should complete
        assert len(results) == num_requests
        
        # All should return 500 (server error for invalid URL)
        for result in results:
            assert result['status_code'] == 500
        
        # Calculate average response time
        response_times = [result['response_time'] for result in results]
        avg_response_time = statistics.mean(response_times)
        max_response_time = max(response_times)
        
        print(f"Average response time: {avg_response_time:.2f}s")
        print(f"Max response time: {max_response_time:.2f}s")
        
        # Even under load, should respond reasonably quickly
        assert avg_response_time < 10.0  # Average less than 10 seconds
        assert max_response_time < 20.0  # No single request over 20 seconds
    
    def test_memory_usage_multiple_requests(self, client):
        """Test memory doesn't leak with multiple requests"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Make multiple requests
        for i in range(50):
            response = client.post(
                "/convert/",
                json={"url": "invalid-url"}
            )
            assert response.status_code == 500
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Initial memory: {initial_memory:.1f} MB")
        print(f"Final memory: {final_memory:.1f} MB")
        print(f"Memory increase: {memory_increase:.1f} MB")
        
        # Memory shouldn't increase dramatically (allow for some variance)
        assert memory_increase < 100  # Less than 100MB increase
    
    @pytest.mark.slow
    def test_timeout_handling(self, client):
        """Test that requests don't hang indefinitely"""
        # Test with an invalid URL that should fail quickly
        response = client.post(
            "/convert/",
            json={"url": "https://www.youtube.com/watch?v=invalid-video-id-12345"},
            timeout=10  # 10 second timeout should be sufficient for error response
        )
        # Should get an error response, not hang
        assert response.status_code in [400, 404, 422, 500]


@pytest.mark.skipif(app is None, reason="Could not import app")
@pytest.mark.load
class TestLoadTesting:
    """Load testing for the API"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_load_test_invalid_requests(self, client):
        """Simple load test with invalid requests"""
        def make_request(request_id):
            start_time = time.time()
            try:
                response = client.post(
                    "/convert/",
                    json={"url": f"invalid-url-{request_id}"}
                )
                success = response.status_code == 500
            except Exception as e:
                success = False
            
            end_time = time.time()
            return {
                'request_id': request_id,
                'success': success,
                'response_time': end_time - start_time
            }
        
        # Run 100 requests with 20 concurrent workers
        num_requests = 100
        max_workers = 20
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(make_request, i) 
                for i in range(num_requests)
            ]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Analyze results
        successful_requests = sum(1 for result in results if result['success'])
        response_times = [result['response_time'] for result in results if result['success']]
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            percentile_95 = sorted(response_times)[int(0.95 * len(response_times))]
        else:
            avg_response_time = float('inf')
            percentile_95 = float('inf')
        
        requests_per_second = successful_requests / total_time
        
        print(f"Total requests: {num_requests}")
        print(f"Successful requests: {successful_requests}")
        print(f"Total time: {total_time:.2f}s")
        print(f"Requests per second: {requests_per_second:.2f}")
        print(f"Average response time: {avg_response_time:.2f}s")
        print(f"95th percentile response time: {percentile_95:.2f}s")
        
        # Assertions for load test
        assert successful_requests >= num_requests * 0.95  # At least 95% success rate
        assert requests_per_second > 1  # At least 1 request per second
        assert avg_response_time < 30  # Average response time under 30 seconds


if __name__ == "__main__":
    # Run performance tests: python -m pytest tests/test_performance.py -v -m "performance"
    # Run load tests: python -m pytest tests/test_performance.py -v -m "load"
    # Run all: python -m pytest tests/test_performance.py -v
    pytest.main([__file__, "-v"])