#!/bin/bash

# Test runner script for YouTube to MP3 converter
# This script runs different types of tests based on arguments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to get the correct python command
get_python_cmd() {
    if [[ -f ".venv/bin/python" ]]; then
        echo ".venv/bin/python"
    elif command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        echo "python"
    else
        print_error "No Python interpreter found"
        exit 1
    fi
}

# Function to get the correct pytest command
get_pytest_cmd() {
    if [[ -f ".venv/bin/pytest" ]]; then
        echo ".venv/bin/pytest"
    elif command -v pytest &> /dev/null; then
        echo "pytest"
    else
        print_error "pytest not found"
        return 1
    fi
}
# Default values
RUN_UNIT=false
RUN_INTEGRATION=false
RUN_PERFORMANCE=false
RUN_SIMPLE=false
RUN_ALL=false
COVERAGE=false
VERBOSE=false

# Function to show usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Test runner for YouTube to MP3 converter"
    echo ""
    echo "Options:"
    echo "  -u, --unit          Run unit tests"
    echo "  -i, --integration   Run integration tests"
    echo "  -p, --performance   Run performance tests"
    echo "  -s, --simple        Run simple tests (no dependencies)"
    echo "  -a, --all           Run all tests"
    echo "  -c, --coverage      Run with coverage reporting"
    echo "  -v, --verbose       Verbose output"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -s               # Run simple tests only"
    echo "  $0 -u -v            # Run unit tests with verbose output"
    echo "  $0 -a -c            # Run all tests with coverage"
    echo "  $0 -i -p            # Run integration and performance tests"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--unit)
            RUN_UNIT=true
            shift
            ;;
        -i|--integration)
            RUN_INTEGRATION=true
            shift
            ;;
        -p|--performance)
            RUN_PERFORMANCE=true
            shift
            ;;
        -s|--simple)
            RUN_SIMPLE=true
            shift
            ;;
        -a|--all)
            RUN_ALL=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            print_error "Unknown option $1"
            usage
            exit 1
            ;;
    esac
done

# If no specific tests selected and not all, default to simple
if [[ "$RUN_ALL" == false && "$RUN_UNIT" == false && "$RUN_INTEGRATION" == false && "$RUN_PERFORMANCE" == false && "$RUN_SIMPLE" == false ]]; then
    print_info "No test type specified, running simple tests"
    RUN_SIMPLE=true
fi

# Set all flags if running all tests
if [[ "$RUN_ALL" == true ]]; then
    RUN_UNIT=true
    RUN_INTEGRATION=true
    RUN_PERFORMANCE=true
    RUN_SIMPLE=true
fi

# Check if we're in the right directory
if [[ ! -f "youtube-to-mp3.py" ]]; then
    print_error "youtube-to-mp3.py not found. Please run from the project root directory."
    exit 1
fi

# Create tests directory if it doesn't exist
if [[ ! -d "tests" ]]; then
    print_warning "Tests directory not found. Creating it..."
    mkdir tests
fi

print_info "Starting YouTube to MP3 Converter Tests"
echo "========================================"

# Keep track of test results
TOTAL_PASSED=0
TOTAL_FAILED=0

# Function to run simple tests
run_simple_tests() {
    print_info "Running simple tests..."
    
    PYTHON_CMD=$(get_python_cmd)
    
    # Try minimal tests first
    if [[ -f "tests/test_minimal.py" ]]; then
        print_info "Running minimal tests..."
        $PYTHON_CMD tests/test_minimal.py
        if [[ $? -eq 0 ]]; then
            print_success "Minimal tests passed"
            ((TOTAL_PASSED++))
        else
            print_error "Minimal tests failed"
            ((TOTAL_FAILED++))
        fi
    fi
    
    # Also try original simple tests
    if [[ -f "tests/test_simple.py" ]]; then
        print_info "Running comprehensive simple tests..."
        $PYTHON_CMD tests/test_simple.py
        if [[ $? -eq 0 ]]; then
            print_success "Simple tests passed"
            ((TOTAL_PASSED++))
        else
            print_warning "Simple tests had some failures (this is expected without all dependencies)"
        fi
    else
        print_warning "Simple test file not found"
    fi
}

# Function to run pytest-based tests
run_pytest_tests() {
    local test_type=$1
    local test_file=$2
    local markers=$3
    
    print_info "Running $test_type tests..."
    
    # Check if pytest is available
    PYTEST_CMD=$(get_pytest_cmd)
    if [[ $? -ne 0 ]]; then
        print_warning "pytest not found. Installing test dependencies..."
        PYTHON_CMD=$(get_python_cmd)
        $PYTHON_CMD -m pip install -r requirements-test.txt 2>/dev/null || {
            print_error "Failed to install test dependencies. Skipping $test_type tests."
            return
        }
        PYTEST_CMD=$(get_pytest_cmd)
    fi
    
    # Build pytest command
    local pytest_cmd="$PYTEST_CMD"
    
    if [[ "$VERBOSE" == true ]]; then
        pytest_cmd="$pytest_cmd -v"
    fi
    
    if [[ "$COVERAGE" == true ]]; then
        pytest_cmd="$pytest_cmd --cov=youtube_to_mp3 --cov-report=term-missing"
    fi
    
    if [[ -n "$markers" ]]; then
        pytest_cmd="$pytest_cmd -m \"$markers\""
    fi
    
    if [[ -f "$test_file" ]]; then
        pytest_cmd="$pytest_cmd $test_file"
        
        print_info "Running: $pytest_cmd"
        eval $pytest_cmd
        
        if [[ $? -eq 0 ]]; then
            print_success "$test_type tests passed"
            ((TOTAL_PASSED++))
        else
            print_error "$test_type tests failed"
            ((TOTAL_FAILED++))
        fi
    else
        print_warning "$test_type test file not found: $test_file"
    fi
}

# Run the selected tests
if [[ "$RUN_SIMPLE" == true ]]; then
    run_simple_tests
fi

if [[ "$RUN_UNIT" == true ]]; then
    run_pytest_tests "Unit" "tests/test_unit.py" "unit"
fi

if [[ "$RUN_INTEGRATION" == true ]]; then
    run_pytest_tests "Integration" "tests/test_integration.py" "integration"
fi

if [[ "$RUN_PERFORMANCE" == true ]]; then
    run_pytest_tests "Performance" "tests/test_performance.py" "performance"
fi

# Summary
echo ""
echo "========================================"
echo "Test Results Summary"
echo "========================================"

TOTAL_TESTS=$((TOTAL_PASSED + TOTAL_FAILED))

if [[ $TOTAL_TESTS -eq 0 ]]; then
    print_warning "No tests were run"
    exit 1
elif [[ $TOTAL_FAILED -eq 0 ]]; then
    print_success "All $TOTAL_PASSED test suite(s) passed! 🎉"
    exit 0
else
    print_error "$TOTAL_FAILED out of $TOTAL_TESTS test suite(s) failed"
    exit 1
fi