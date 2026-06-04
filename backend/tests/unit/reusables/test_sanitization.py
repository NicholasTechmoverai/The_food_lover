import pytest

from reusables.main import clean_and_truncate, sanitizeContents, sanitize_name


class TestSanitizeContents:
    def test_strips_script_tags(self):
        dirty = '<p>Hello</p><script>alert("xss")</script>'
        result = sanitizeContents(dirty)
        assert "<script" not in result
        assert "Hello" in result

    def test_allows_safe_formatting_tags(self):
        html = "<p><strong>Bold</strong> and <em>italic</em></p>"
        result = sanitizeContents(html)
        assert "<strong>Bold</strong>" in result
        assert "<em>italic</em>" in result

    def test_strips_javascript_href(self):
        dirty = '<a href="javascript:alert(1)">Click</a>'
        result = sanitizeContents(dirty)
        assert "javascript:" not in result

    def test_linkifies_plain_urls(self):
        html = "Visit https://example.com for more"
        result = sanitizeContents(html)
        assert "https://example.com" in result


class TestSanitizeName:
    @pytest.mark.asyncio
    async def test_normalizes_spaces_and_special_chars(self):
        assert await sanitize_name("My Recipe Name!") == "my_recipe_name"

    @pytest.mark.asyncio
    async def test_preserves_allowed_chars(self):
        assert await sanitize_name("Pilau-Rice_01") == "pilau-rice_01"


class TestCleanAndTruncate:
    def test_returns_empty_for_none_or_empty(self):
        assert clean_and_truncate(None) == ""
        assert clean_and_truncate("") == ""

    def test_strips_html_tags(self):
        assert clean_and_truncate("<p>Hello <b>world</b></p>") == "Hello world"

    def test_decodes_html_entities(self):
        assert clean_and_truncate("Tom &amp; Jerry") == "Tom & Jerry"

    def test_truncates_long_text_with_ellipsis(self):
        result = clean_and_truncate("A" * 50, limit=20)
        assert result.endswith("...")
        assert len(result) == 20

    def test_does_not_truncate_short_text(self):
        text = "Short text"
        assert clean_and_truncate(text, limit=30) == text
