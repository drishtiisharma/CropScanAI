"""
Automatic Translation Extraction Script
Extracts translatable strings from Flask templates and creates/updates .pot file
"""

import os
import subprocess
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent
BABEL_CFG = BASE_DIR / 'babel.cfg'
TRANSLATIONS_DIR = BASE_DIR / 'translations'
POT_FILE = TRANSLATIONS_DIR / 'messages.pot'
TEMPLATES_DIR = BASE_DIR / 'templates'

def create_babel_config():
    """Create babel.cfg if it doesn't exist"""
    config_content = """[python: **.py]

[jinja2: **/templates/**.html]
encoding = utf-8
"""
    
    with open(BABEL_CFG, 'w', encoding='utf-8') as f:
        f.write(config_content)
    print(f"✓ Created {BABEL_CFG}")

def extract_messages():
    """Extract messages from templates"""
    print("\n" + "="*60)
    print("EXTRACTING TRANSLATABLE STRINGS")
    print("="*60 + "\n")
    
    # Ensure translations directory exists
    TRANSLATIONS_DIR.mkdir(exist_ok=True)
    
    # Create babel config if needed
    if not BABEL_CFG.exists():
        create_babel_config()
    
    # Run pybabel extract
    cmd = [
        'pybabel', 'extract',
        '-F', str(BABEL_CFG),
        '-k', '_l',
        '-o', str(POT_FILE),
        '.'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        print(f"✓ Extracted messages to {POT_FILE}")
        
        # Count extracted strings
        with open(POT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            msgid_count = content.count('msgid "') - 1  # Subtract header
        
        print(f"✓ Found {msgid_count} translatable strings")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error extracting messages: {e}")
        print(e.stderr)
        return False
    
    return True

def init_language(lang_code):
    """Initialize a new language translation"""
    print(f"\nInitializing translation for: {lang_code}")
    
    cmd = [
        'pybabel', 'init',
        '-i', str(POT_FILE),
        '-d', str(TRANSLATIONS_DIR),
        '-l', lang_code
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        print(f"✓ Initialized {lang_code} translation")
        
        po_file = TRANSLATIONS_DIR / lang_code / 'LC_MESSAGES' / 'messages.po'
        print(f"✓ Created: {po_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error initializing language: {e}")
        print(e.stderr)

def update_language(lang_code):
    """Update existing language translation"""
    print(f"\nUpdating translation for: {lang_code}")
    
    cmd = [
        'pybabel', 'update',
        '-i', str(POT_FILE),
        '-d', str(TRANSLATIONS_DIR),
        '-l', lang_code
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        print(f"✓ Updated {lang_code} translation")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error updating language: {e}")
        print(e.stderr)

def compile_translations():
    """Compile all .po files to .mo files"""
    print("\n" + "="*60)
    print("COMPILING TRANSLATIONS")
    print("="*60 + "\n")
    
    cmd = [
        'pybabel', 'compile',
        '-d', str(TRANSLATIONS_DIR)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        print("✓ Compiled all translations")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error compiling translations: {e}")
        print(e.stderr)

def main():
    """Main workflow"""
    print("\n" + "="*60)
    print("FLASK TRANSLATION WORKFLOW")
    print("="*60)
    
    # Step 1: Extract messages
    if not extract_messages():
        print("\n✗ Extraction failed. Exiting.")
        return
    
    # Step 2: Check for existing translations
    lang_dirs = [d for d in TRANSLATIONS_DIR.iterdir() if d.is_dir() and d.name != '__pycache__']
    
    if lang_dirs:
        print("\n" + "-"*60)
        print("EXISTING TRANSLATIONS:")
        for lang_dir in lang_dirs:
            print(f"  • {lang_dir.name}")
        print("-"*60)
        
        # Update existing translations
        for lang_dir in lang_dirs:
            update_language(lang_dir.name)
    else:
        print("\n" + "-"*60)
        print("NO EXISTING TRANSLATIONS FOUND")
        print("-"*60)
        
        # Initialize Hindi translation as example
        choice = input("\nWould you like to initialize Hindi (hi) translation? (y/n): ")
        if choice.lower() == 'y':
            init_language('hi')
    
    # Step 3: Compile translations
    if lang_dirs or input("\nCompile translations now? (y/n): ").lower() == 'y':
        compile_translations()
    
    print("\n" + "="*60)
    print("WORKFLOW COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit the .po files in translations/<lang>/LC_MESSAGES/")
    print("2. Run this script again to compile translations")
    print("3. Restart your Flask app to see changes")

if __name__ == "__main__":
    main()
