#!/usr/bin/env python3
"""
Template Setup Script

Run this after cloning the template to customize it for your project.
This script will:
1. Ask for your project details
2. Rename files and directories
3. Replace placeholder values throughout the codebase
4. Delete itself when done

Usage:
    python setup_template.py
"""

import os
import re
import shutil
import sys


def to_snake_case(name: str) -> str:
    """Convert to snake_case (e.g., my_tool)."""
    s = re.sub(r'[-\s]+', '_', name)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s)
    s = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', s)
    return s.lower()


def to_pascal_case(name: str) -> str:
    """Convert to PascalCase (e.g., MyTool)."""
    words = re.split(r'[-_\s]+', name)
    return ''.join(word.capitalize() for word in words)


def to_kebab_case(name: str) -> str:
    """Convert to kebab-case (e.g., my-tool)."""
    s = to_snake_case(name)
    return s.replace('_', '-')


def get_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default."""
    if default:
        result = input(f"{prompt} [{default}]: ").strip()
        return result if result else default
    return input(f"{prompt}: ").strip()


def replace_in_file(filepath: str, replacements: dict[str, str]) -> None:
    """Replace all occurrences in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    print("\n🔧 Strands Template Setup\n")
    print("This will customize the template for your project.\n")
    
    # Gather information
    package_name = get_input("Package name (e.g., 'google', 'aws', 'slack')")
    if not package_name:
        print("❌ Package name is required")
        sys.exit(1)
    
    # Generate variations
    snake_name = to_snake_case(package_name)
    pascal_name = to_pascal_case(package_name)
    kebab_name = to_kebab_case(package_name)
    
    print(f"\n  PyPI package: strands-{kebab_name}")
    print(f"  Module:       strands_{snake_name}")
    print(f"  Classes:      {pascal_name}Model, {pascal_name}SessionManager, etc.")
    
    # Optional info
    print()
    author_name = get_input("Author name", "Your Name")
    author_email = get_input("Author email", "your.email@example.com")
    github_username = get_input("GitHub username", "yourusername")
    description = get_input("Package description", f"Strands Agents components for {package_name}")
    
    # Confirm
    print("\n" + "="*50)
    confirm = get_input("\nProceed with setup? (y/n)", "y")
    if confirm.lower() != 'y':
        print("Setup cancelled.")
        sys.exit(0)
    
    print("\n⏳ Setting up project...\n")
    
    # Define replacements
    replacements = {
        # Package/module names
        "strands-template": f"strands-{kebab_name}",
        "strands_template": f"strands_{snake_name}",
        # Class names
        "TemplateModel": f"{pascal_name}Model",
        "TemplateHookProvider": f"{pascal_name}HookProvider",
        "TemplateSessionManager": f"{pascal_name}SessionManager",
        "TemplateConversationManager": f"{pascal_name}ConversationManager",
        # Function names
        "template_tool": f"{snake_name}_tool",
        # Author info
        "Your Name": author_name,
        "your.email@example.com": author_email,
        "yourusername": github_username,
        "Your package description": description,
    }
    
    # Files to process
    files_to_process = [
        "pyproject.toml",
        "README.md",
        "src/strands_template/__init__.py",
        "src/strands_template/tool.py",
        "src/strands_template/model.py",
        "src/strands_template/session_manager.py",
        "src/strands_template/conversation_manager.py",
        "src/strands_template/hook_provider.py",
        "tests/test_tool.py",
        "tests/test_model.py",
        "tests/test_session_manager.py",
        "tests/test_conversation_manager.py",
        "tests/test_hook_provider.py",
    ]
    
    # Process files
    for filepath in files_to_process:
        if os.path.exists(filepath):
            replace_in_file(filepath, replacements)
            print(f"  ✓ Updated {filepath}")
    
    # Rename source directory
    old_src = "src/strands_template"
    new_src = f"src/strands_{snake_name}"
    if os.path.exists(old_src) and old_src != new_src:
        shutil.move(old_src, new_src)
        print(f"  ✓ Renamed {old_src} → {new_src}")
    
    # Clean up
    print("\n🧹 Cleaning up...")
    
    # Remove this setup script
    script_path = os.path.abspath(__file__)
    if os.path.exists(script_path):
        os.remove(script_path)
        print("  ✓ Removed setup_template.py")
    
    print("\n✅ Setup complete!\n")
    print("Next steps:")
    print("  1. Review the generated files")
    print("  2. Install dev dependencies: pip install -e '.[dev]'")
    print("  3. Run tests: pytest")
    print("  4. Start implementing your components")
    print()


if __name__ == "__main__":
    main()
