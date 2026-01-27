"""Tests for TemplateHooks."""

from strands_template import TemplateHooks


def test_template_hooks_init():
    """Test initialization."""
    hooks = TemplateHooks()
    assert hooks is not None
