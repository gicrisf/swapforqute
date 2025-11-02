# Release Notes

## v1.0.0

### Breaking Changes
- **Script renamed**: `main.py` → `sfq.py`
  - Update your qutebrowser config.py to use the new script name
  - Old: `sfq_script_path = sfq_base_dir + "main.py"`
  - New: `sfq_script_path = sfq_base_dir + "sfq.py"`

### New Features
- **Hybrid configuration approach**: Built-in rules with optional JSON extension
  - Built-in RULES dictionary in sfq.py for quick setup
  - Optional `-c` flag to extend built-in rules with JSON config
  - JSON rules override built-in rules for duplicate domains
- **Comprehensive test suite**: Unit tests for all URL transformation logic
- **GitHub Actions**: Automated release workflow

### Improvements
- Simplified configuration flow - hardcoded rules in script as default
- Better README with clearer setup instructions
- Test coverage for all core functionality (force_https, domain replacement, query/fragment cleaning)

### Removed
- Example `config.json` file (now optional, user-created when needed)

### Migration Guide

If upgrading from a previous version:

1. **Update qutebrowser config.py**:
   - Change `main.py` to `sfq.py` in your script path

2. **Configuration**:
   - Built-in rules are now in the RULES dictionary (sfq.py:16-27)
   - If you had a config.json, you can still use it with the `-c` flag
   - Or migrate your rules to the built-in RULES dictionary for simpler setup

3. **Make executable**:
   ```bash
   chmod +x ~/.config/qutebrowser/userscripts/swapforqute/sfq.py
   ```

### Installation

For new users, see README.md for complete installation instructions.
