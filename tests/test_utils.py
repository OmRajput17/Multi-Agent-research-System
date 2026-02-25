"""
Test script for src/utils/get_llm.py
Tests LLMConfig initialization and Groq LLM instantiation.
"""
from src.utils.get_llm import LLMConfig


def test_default_config():
    """Test LLMConfig with default parameters"""
    print("=" * 60)
    print("TEST 1: Default LLMConfig")
    print("=" * 60)
    config = LLMConfig()
    assert config.model_name == "llama-3.3-70b-versatile", f"Expected default model name, got {config.model_name}"
    assert config.temperature == 0.7, f"Expected default temp 0.7, got {config.temperature}"
    print(f"  Model: {config.model_name}")
    print(f"  Temperature: {config.temperature}")
    print("✅ Default Config PASSED\n")


def test_custom_config():
    """Test LLMConfig with custom parameters"""
    print("=" * 60)
    print("TEST 2: Custom LLMConfig")
    print("=" * 60)
    config = LLMConfig(model_name="llama-3.1-8b-instant", temperature=0.3)
    assert config.model_name == "llama-3.1-8b-instant"
    assert config.temperature == 0.3
    print(f"  Model: {config.model_name}")
    print(f"  Temperature: {config.temperature}")
    print("✅ Custom Config PASSED\n")


def test_get_llm():
    """Test that get_llm returns a valid ChatGroq instance"""
    print("=" * 60)
    print("TEST 3: get_llm() returns ChatGroq instance")
    print("=" * 60)
    config = LLMConfig()
    llm = config.get_llm()
    assert llm is not None, "LLM should not be None"
    print(f"  LLM Type: {type(llm).__name__}")
    print("✅ get_llm() PASSED\n")


def test_llm_invoke():
    """Test that the LLM can actually respond"""
    print("=" * 60)
    print("TEST 4: LLM invoke (live API call)")
    print("=" * 60)
    config = LLMConfig()
    llm = config.get_llm()
    response = llm.invoke("Say 'hello' in one word.")
    assert response is not None, "Response should not be None"
    assert hasattr(response, 'content'), "Response should have 'content' attribute"
    print(f"  Response: {response.content[:100]}")
    print("✅ LLM Invoke PASSED\n")


if __name__ == "__main__":
    test_default_config()
    test_custom_config()
    test_get_llm()
    test_llm_invoke()
    print("=" * 60)
    print("ALL UTILS TESTS PASSED ✅")
    print("=" * 60)
