# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-11-03

### Added
- **PoToken Anti-Bot Protection**: Comprehensive implementation to prevent YouTube 403 errors and bot detection
  - AUTO mode with WEB client for automatic token generation (requires Node.js)
  - MANUAL mode for browser-extracted tokens (PO_TOKEN + VISITOR_DATA)
  - Status endpoint (`/`) showing current PoToken configuration
  - Comprehensive documentation (`POTOKEN.md`) with token extraction guides
- **Security improvements**: Named constants for PoToken modes to resolve Bandit warnings
- **Kubernetes configuration**: Updated Helm charts with PoToken environment variables

### Changed
- **Docker optimization**: 63% size reduction from 1.94GB to 723MB using Alpine Linux
- **CI pipeline**: Switch to Alpine Docker images for production builds
- **Test framework**: Fixed test runner boolean return logic for compatibility
- **Code quality**: Replace string literals with named constants (`POTOKEN_MODE_AUTO`, `POTOKEN_MODE_MANUAL`)

### Fixed
- YouTube bot detection and 403 error prevention through PoToken implementation
- Bandit security warnings (B105 hardcoded password false positives)
- Test runner exit codes for proper CI/CD integration

### Security
- All Bandit security checks now pass (0 issues)
- Enhanced YouTube access reliability through proof-of-origin tokens

### Documentation
- Complete PoToken setup guide with browser extraction instructions
- Kubernetes deployment examples for both AUTO and MANUAL modes
- Troubleshooting guide for common YouTube access issues
- Docker configuration examples

### Testing
- All 32 tests passing (Simple, Unit, Integration, Performance)
- Updated unit tests for new PoToken implementation
- Verified compatibility with pytubefix official documentation

## [1.1.0] - Previous Release

### Added
- Kubernetes deployment with Helm charts
- GitHub Actions CI/CD pipeline
- Docker multi-stage builds

### Changed
- FastAPI application structure
- Test suite organization

### Fixed
- YouTube download reliability
- Container deployment issues

## [1.0.x] - Initial Releases

### Added
- Basic YouTube to MP3 conversion functionality
- FastAPI web service
- Docker containerization
- Basic test suite