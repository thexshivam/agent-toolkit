#!/usr/bin/env python3
"""
Validate Claude Skills for compliance.

Usage:
    python validate_skills.py              # Validate all skills
    python validate_skills.py videodb-search  # Validate specific skill
"""

import os
import sys
import re
import yaml
from pathlib import Path


def validate_skill(skill_path: Path) -> tuple[bool, list, list]:
    """
    Validate a single skill.
    
    Returns:
        (is_valid, errors, warnings)
    """
    errors = []
    warnings = []
    
    # Check SKILL.md exists
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        return False, ["SKILL.md not found"], []
    
    content = skill_file.read_text()
    
    # Check frontmatter
    if not content.startswith('---'):
        return False, ["SKILL.md must start with --- (YAML frontmatter)"], []
    
    try:
        end_idx = content.find('---', 3)
        if end_idx == -1:
            return False, ["YAML frontmatter not closed (missing ---)"], []
        
        frontmatter = yaml.safe_load(content[3:end_idx])
    except yaml.YAMLError as e:
        return False, [f"Invalid YAML: {e}"], []
    
    # Validate name
    name = frontmatter.get('name')
    if not name:
        errors.append("Missing 'name' in frontmatter")
    elif not isinstance(name, str):
        errors.append("'name' must be a string")
    else:
        if len(name) > 64:
            errors.append(f"Name too long ({len(name)} > 64 chars)")
        if not re.match(r'^[a-z0-9-]+$', name):
            errors.append("Name must be lowercase letters, numbers, hyphens only")
        if 'anthropic' in name.lower() or 'claude' in name.lower():
            errors.append("Name cannot contain 'anthropic' or 'claude'")
        if skill_path.name != name:
            warnings.append(f"Folder '{skill_path.name}' doesn't match name '{name}'")
    
    # Validate description
    desc = frontmatter.get('description')
    if not desc:
        errors.append("Missing 'description' in frontmatter")
    elif not isinstance(desc, str):
        errors.append("'description' must be a string")
    else:
        if len(desc) > 1024:
            errors.append(f"Description too long ({len(desc)} > 1024 chars)")
        if len(desc) < 20:
            warnings.append("Description is very short")
    
    # Check scripts
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        py_files = list(scripts_dir.glob("*.py"))
        for py_file in py_files:
            try:
                compile(py_file.read_text(), py_file, 'exec')
            except SyntaxError as e:
                errors.append(f"Syntax error in {py_file.name}: {e}")
    
    return len(errors) == 0, errors, warnings


def main():
    # Find skills directory
    skills_dir = Path("skills")
    if not skills_dir.exists():
        # Try from parent
        skills_dir = Path(".") 
        if not (skills_dir / "videodb-search").exists():
            print(" Cannot find skills directory")
            sys.exit(1)
    
    # Get skills to validate
    if len(sys.argv) > 1:
        paths = [skills_dir / sys.argv[1]]
    else:
        paths = [p for p in skills_dir.iterdir()
                 if p.is_dir() and not p.name.startswith('.') and p.name not in ['__pycache__', 'venv', 'env', 'scripts']]
    
    all_valid = True
    
    for path in paths:
        if not path.exists():
            print(f" Skill not found: {path}")
            all_valid = False
            continue
            
        is_valid, errors, warnings = validate_skill(path)
        
        print(f"\n{'='*50}")
        print(f"Skill: {path.name}")
        print('='*50)
        
        if errors:
            print(f"\n ERRORS ({len(errors)}):")
            for e in errors:
                print(f"   • {e}")
            all_valid = False
        
        if warnings:
            print(f"\n WARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"   • {w}")
        
        if is_valid:
            print("\n Valid" + (" (with warnings)" if warnings else ""))
    
    print(f"\n{'='*50}")
    print("All skills valid!" if all_valid else " Some skills have errors")
    print('='*50 + "\n")
    
    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()