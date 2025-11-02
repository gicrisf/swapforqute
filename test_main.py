#!/usr/bin/env python3
"""
Unit tests for swapforqute main module.

Run with:
    python -m unittest test_main
    python -m unittest test_main.TestReplace.test_force_https
    python test_main.py
"""
import unittest
import os
import json
import tempfile
from main import replace, load_config, RULES

class TestReplace(unittest.TestCase):
    """Test URL replacement functionality."""

    def setUp(self):
        """Reset RULES to default state before each test."""
        RULES.clear()
        RULES.update({
            'example.com': {
                'force_https': True,
                'out': 'newexample.com',
                'clean_queries': True,
                'clean_fragments': True
            },
            'oldsite.org': {
                'force_https': True,
                'clean_queries': True
            }
        })

    def test_force_https(self):
        """Test forcing HTTPS scheme."""
        result = replace("http://example.com/page")
        self.assertTrue(result.startswith("https://"))
        self.assertIn("newexample.com", result)

    def test_domain_replacement(self):
        """Test replacing domain name."""
        result = replace("http://example.com/page")
        self.assertTrue("://newexample.com/" in result)

    def test_clean_queries(self):
        """Test removing query parameters."""
        result = replace("http://example.com/page?tracking=123&utm_source=spam")
        self.assertNotIn("tracking", result)
        self.assertNotIn("utm_source", result)
        self.assertNotIn("?", result)

    def test_clean_fragments(self):
        """Test removing URL fragments."""
        result = replace("http://example.com/page#section")
        self.assertNotIn("#", result)
        self.assertNotIn("section", result)

    def test_combined_transformations(self):
        """Test all transformations applied together."""
        url = "http://example.com/page?tracking=123#section"
        result = replace(url)

        self.assertEqual(result, "https://newexample.com/page")
        self.assertTrue(result.startswith("https://"))
        self.assertIn("newexample.com", result)
        self.assertNotIn("tracking", result)
        self.assertNotIn("section", result)

    def test_partial_transformations(self):
        """Test domain with only some transformations enabled."""
        url = "http://oldsite.org/page?param=value#anchor"
        result = replace(url)

        # Should force HTTPS and clean queries but NOT clean fragments or replace domain
        self.assertTrue(result.startswith("https://"))
        self.assertIn("oldsite.org", result)  # Domain NOT replaced
        self.assertNotIn("param", result)     # Queries cleaned
        self.assertIn("anchor", result)       # Fragments NOT cleaned

    def test_non_matching_domain(self):
        """Test URL with domain not in RULES."""
        url = "http://unknown.com/page?param=value#anchor"
        result = replace(url)

        # Should return unchanged
        self.assertEqual(result, url)

    def test_https_already_present(self):
        """Test that HTTPS URLs remain HTTPS."""
        url = "https://example.com/page"
        result = replace(url)

        self.assertTrue(result.startswith("https://"))

    def test_preserves_path(self):
        """Test that URL path is preserved."""
        url = "http://example.com/path/to/page"
        result = replace(url)

        self.assertIn("/path/to/page", result)

    def test_empty_path(self):
        """Test domain-only URL."""
        url = "http://example.com"
        result = replace(url)

        self.assertIn("newexample.com", result)


class TestConfigLoading(unittest.TestCase):
    """Test JSON configuration loading."""

    def setUp(self):
        """Reset RULES to default state before each test."""
        RULES.clear()
        RULES.update({
            'example.com': {
                'force_https': True,
                'out': 'newexample.com'
            }
        })

    def test_load_valid_json(self):
        """Test loading valid JSON configuration."""
        config_data = {
            "reddit.com": {
                "out": "old.reddit.com",
                "force_https": True,
                "clean_queries": True
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            load_config(temp_path)

            # Check that JSON rules were added
            self.assertIn('reddit.com', RULES)
            self.assertEqual(RULES['reddit.com']['out'], 'old.reddit.com')

            # Check that built-in rules still exist
            self.assertIn('example.com', RULES)
        finally:
            os.unlink(temp_path)

    def test_json_overrides_builtin(self):
        """Test that JSON rules override built-in rules for same domain."""
        config_data = {
            "example.com": {
                "out": "override.com",
                "force_https": False
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            load_config(temp_path)

            # JSON should override built-in
            self.assertEqual(RULES['example.com']['out'], 'override.com')
            self.assertEqual(RULES['example.com']['force_https'], False)
        finally:
            os.unlink(temp_path)

    def test_nonexistent_file(self):
        """Test loading non-existent config file."""
        # Should not raise exception
        load_config('/nonexistent/path.json')

        # Built-in rules should remain intact
        self.assertIn('example.com', RULES)

    def test_none_path(self):
        """Test passing None as config path."""
        # Should not raise exception
        load_config(None)

        # Built-in rules should remain intact
        self.assertIn('example.com', RULES)

    def test_empty_string_path(self):
        """Test passing empty string as config path."""
        # Should not raise exception
        load_config('')

        # Built-in rules should remain intact
        self.assertIn('example.com', RULES)


class TestIntegration(unittest.TestCase):
    """Integration tests combining config loading and URL replacement."""

    def setUp(self):
        """Reset RULES to default state before each test."""
        RULES.clear()
        RULES.update({
            'example.com': {
                'force_https': True,
                'out': 'newexample.com',
                'clean_queries': True
            }
        })

    def test_builtin_then_json_extension(self):
        """Test using built-in rules extended by JSON."""
        # Create JSON config with additional rule
        config_data = {
            "twitter.com": {
                "out": "nitter.net",
                "force_https": True,
                "clean_queries": True
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            load_config(temp_path)

            # Test built-in rule still works
            result1 = replace("http://example.com/page?tracking=123")
            self.assertEqual(result1, "https://newexample.com/page")

            # Test JSON rule works
            result2 = replace("http://twitter.com/user/status?ref=spam")
            self.assertEqual(result2, "https://nitter.net/user/status")
        finally:
            os.unlink(temp_path)

    def test_real_world_reddit_example(self):
        """Test real-world Reddit URL transformation."""
        config_data = {
            "www.reddit.com": {
                "out": "old.reddit.com",
                "force_https": True,
                "clean_queries": True
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            load_config(temp_path)

            url = "http://www.reddit.com/r/test?utm_source=share&utm_medium=web2x&context=3"
            result = replace(url)

            self.assertEqual(result, "https://old.reddit.com/r/test")
        finally:
            os.unlink(temp_path)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Reset RULES to minimal state."""
        RULES.clear()
        RULES.update({
            'test.com': {
                'force_https': True
            }
        })

    def test_url_without_scheme(self):
        """Test URL without http:// or https:// scheme."""
        # urlparse should handle this, but test to be sure
        url = "test.com/page"
        result = replace(url)
        # Should not match because netloc will be empty
        self.assertEqual(result, url)

    def test_rule_with_only_one_option(self):
        """Test rule with only one transformation enabled."""
        url = "http://test.com/page?query=value#fragment"
        result = replace(url)

        # Only force_https should apply
        self.assertTrue(result.startswith("https://"))
        self.assertIn("query=value", result)  # Queries preserved
        self.assertIn("#fragment", result)    # Fragments preserved

    def test_rule_with_no_options(self):
        """Test rule with empty options dict."""
        RULES.clear()
        RULES['empty.com'] = {}

        url = "http://empty.com/page"
        result = replace(url)

        # Should return unchanged (no transformations)
        self.assertEqual(result, url)

if __name__ == '__main__':
    unittest.main()
