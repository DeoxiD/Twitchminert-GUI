"""Basic tests for Twitchminert-GUI"""
import pytest


def test_import_models():
    """Test that models module can be imported"""
    import models
    assert models is not None


def test_import_config():
    """Test that config module can be imported"""
    import config
    assert config is not None


def test_basic_math():
    """Basic sanity test"""
    assert 1 + 1 == 2
