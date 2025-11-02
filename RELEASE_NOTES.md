# Release Notes

## v1.1.0

### New Features
- **One-liner installation scripts**: Simplified installation process
  - Linux/macOS: `curl -sSL https://raw.githubusercontent.com/YOUR_USER/swapforqute/main/install.sh | bash`
  - Windows: `install.ps1` PowerShell script with automatic batch wrapper creation
  - Automatic creation of `sfq.bat` wrapper on Windows for qutebrowser compatibility

### Bug Fixes
- **Fixed schemeless URL handling**: URLs entered without a scheme (e.g., "reddit.com") are now properly processed
  - Previously, typing "reddit.com" without "https://" would fail because `urlparse()` couldn't detect the domain
  - Now automatically prepends "https://" to schemeless URLs before processing
  - Enables natural URL entry in qutebrowser without requiring the scheme prefix

### Tests
- Added comprehensive unit tests for schemeless URL scenarios:
  - `test_url_without_scheme`: Basic domain with path
  - `test_url_without_scheme_simple_domain`: Simple domain only (e.g., "reddit.com")
  - `test_url_without_scheme_with_path`: Domain with path and query parameters
- All 22 tests pass successfully
