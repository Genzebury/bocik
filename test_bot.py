"""
Simple tests to verify bot functionality
"""
import json
import os
import sys

def test_config_example_valid():
    """Test that config.example.json is valid JSON"""
    with open('config.example.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    assert 'token' in config, "Config must have 'token' field"
    assert 'webhook_url' in config, "Config must have 'webhook_url' field"
    assert 'muted_role_name' in config, "Config must have 'muted_role_name' field"
    assert 'response_triggers' in config, "Config must have 'response_triggers' field"
    assert isinstance(config['response_triggers'], dict), "response_triggers must be a dictionary"
    
    print("✓ Config example is valid")

def test_bot_imports():
    """Test that bot.py can be imported (syntax check)"""
    # We can't fully import the bot without a valid config.json,
    # but we can check the syntax by compiling it
    import py_compile
    try:
        py_compile.compile('bot.py', doraise=True)
        print("✓ bot.py has valid Python syntax")
    except py_compile.PyCompileError as e:
        print(f"✗ bot.py has syntax errors: {e}")
        sys.exit(1)

def test_requirements_format():
    """Test that requirements.txt is properly formatted"""
    with open('requirements.txt', 'r') as f:
        lines = f.readlines()
    
    assert len(lines) > 0, "requirements.txt must not be empty"
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            assert '>=' in line or '==' in line, f"Invalid requirement format: {line}"
    
    print("✓ requirements.txt is properly formatted")

def test_gitignore_exists():
    """Test that .gitignore exists and contains important entries"""
    assert os.path.exists('.gitignore'), ".gitignore must exist"
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    assert 'config.json' in content, ".gitignore must include config.json"
    assert 'dm_logs.json' in content, ".gitignore must include dm_logs.json"
    assert '__pycache__' in content, ".gitignore must include __pycache__"
    
    print("✓ .gitignore is properly configured")

if __name__ == '__main__':
    print("Running bot tests...\n")
    
    try:
        test_config_example_valid()
        test_bot_imports()
        test_requirements_format()
        test_gitignore_exists()
        
        print("\n✅ All tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
