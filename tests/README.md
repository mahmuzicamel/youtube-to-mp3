# Tests for YouTube to MP3 Converter

This directory contains comprehensive tests for the YouTube to MP3 converter application.

## Test Structure

```
tests/
├── conftest.py              # Test fixtures and utilities
├── test_simple.py           # Simple tests (no external dependencies)
├── test_unit.py             # Unit tests with mocking
├── test_integration.py      # Integration tests with real API calls
├── test_performance.py      # Performance and load tests
└── README.md               # This file
```

## Test Types

### 1. Simple Tests (`test_simple.py`)
- **Purpose**: Basic functionality tests without external dependencies
- **Dependencies**: None (uses only standard library)
- **What it tests**:
  - Module imports
  - App creation
  - Pydantic models
  - Route definitions
  - Basic logic (filename sanitization)

**Run with**:
```bash
python3 tests/test_simple.py
# or
./run_tests.sh -s
```

### 2. Unit Tests (`test_unit.py`)
- **Purpose**: Test individual functions with mocked dependencies
- **Dependencies**: pytest, pytest-mock, pytest-asyncio
- **What it tests**:
  - URLItem Pydantic model validation
  - download_audio_post function with mocked YouTube/MoviePy
  - Error handling scenarios
  - File cleanup
  - Response format

**Run with**:
```bash
pytest tests/test_unit.py -v
# or
./run_tests.sh -u
```

### 3. Integration Tests (`test_integration.py`)
- **Purpose**: Test the full API with real HTTP requests
- **Dependencies**: pytest, httpx, fastapi[all]
- **What it tests**:
  - API endpoint responses
  - Request/response format
  - Error handling
  - OpenAPI documentation endpoints
  - Content-Type headers

**Run with**:
```bash
pytest tests/test_integration.py -v
# or
./run_tests.sh -i
```

### 4. Performance Tests (`test_performance.py`)
- **Purpose**: Test response times, memory usage, and load handling
- **Dependencies**: pytest, psutil
- **What it tests**:
  - Response time for invalid requests
  - Memory usage patterns
  - Concurrent request handling
  - Load testing with multiple requests

**Run with**:
```bash
pytest tests/test_performance.py -v -m "performance"
# or
./run_tests.sh -p
```

## Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.performance` - Performance tests
- `@pytest.mark.load` - Load tests
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.network` - Tests requiring network access

## Installation

### Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### Install Application Dependencies

```bash
pip install -r requirements.txt
```

## Running Tests

### Quick Start (Simple Tests Only)
```bash
./run_tests.sh -s
```

### All Tests
```bash
./run_tests.sh -a
```

### Specific Test Types
```bash
./run_tests.sh -u          # Unit tests only
./run_tests.sh -i          # Integration tests only
./run_tests.sh -p          # Performance tests only
```

### With Coverage
```bash
./run_tests.sh -a -c       # All tests with coverage
```

### Using pytest directly

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_unit.py -v

# Run tests with markers
pytest -m "unit" -v                    # Unit tests only
pytest -m "not slow" -v                # Skip slow tests
pytest -m "performance or load" -v     # Performance tests only

# Run with coverage
pytest --cov=youtube_to_mp3 --cov-report=html

# Run specific test
pytest tests/test_unit.py::TestURLItem::test_url_item_valid -v
```

## Test Data

The tests use various types of test data:

### Valid YouTube URLs
- Standard YouTube URLs
- Short YouTube URLs (youtu.be)
- URLs with timestamps
- Mobile YouTube URLs

### Invalid URLs
- Empty strings
- Non-YouTube URLs
- Malformed URLs
- URLs without video IDs

### Mock Data
- Fake MP3 audio data
- Mock YouTube video metadata
- Mock audio streams
- Temporary file paths

## Writing New Tests

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test Function
```python
def test_something_specific():
    """Test that something specific works correctly"""
    # Arrange
    input_data = "test input"
    expected_output = "expected result"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

### Using Fixtures
```python
def test_with_fixture(mock_youtube_success, api_client):
    """Test using predefined fixtures"""
    # Fixtures are automatically provided
    response = api_client.post("/download_audio_post/", json={"url": "test"})
    assert response.status_code == 200
```

## Continuous Integration

These tests are designed to run in CI/CD environments:

### GitHub Actions Example
```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pip install -r requirements-test.txt
    ./run_tests.sh -a -c
```

### Docker Testing
```bash
# Build test image
docker build -t youtube-to-mp3-test -f Dockerfile.test .

# Run tests in container
docker run --rm youtube-to-mp3-test ./run_tests.sh -a
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure `youtube_to_mp3.py` exists (copy from `youtube-to-mp3.py`)
   - Install dependencies: `pip install -r requirements.txt`

2. **Network Test Failures**
   - Skip network tests: `pytest -m "not network"`
   - Check internet connection for integration tests

3. **Slow Tests**
   - Skip slow tests: `pytest -m "not slow"`
   - Run only fast tests for development

4. **Coverage Issues**
   - Install coverage: `pip install pytest-cov`
   - Ensure source code is in Python path

### Environment Variables

Set these for testing:
```bash
export PYTHONPATH="${PYTHONPATH}:."
export TEST_ENV=true
```

## Test Reports

### Coverage Report
```bash
pytest --cov=youtube_to_mp3 --cov-report=html
open htmlcov/index.html
```

### Test Results
```bash
pytest --junitxml=test-results.xml
```

## Performance Benchmarks

Expected performance characteristics:

- **Invalid URL Response**: < 5 seconds
- **Validation Error Response**: < 1 second
- **Concurrent Invalid Requests**: 95% success rate, 10+ requests/second
- **Memory Usage**: < 100MB increase for 50 requests

## Contributing

When adding new tests:

1. Follow the existing test structure
2. Add appropriate markers
3. Include both positive and negative test cases
4. Mock external dependencies in unit tests
5. Add performance considerations for slow operations
6. Update this README if adding new test categories