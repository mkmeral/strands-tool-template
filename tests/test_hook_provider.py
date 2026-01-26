"""Tests for TemplateHookProvider."""

from strands_template import TemplateHookProvider


def test_template_hook_provider_init():
    """Test initialization."""
    hooks = TemplateHookProvider()
    assert hooks is not None
