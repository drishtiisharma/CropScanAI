import polib
import os

# File paths
po_file = r'C:\Users\HP\Desktop\TRANSLATION\CropScanAI\translations\hi\LC_MESSAGES\messages.po'
mo_file = r'C:\Users\HP\Desktop\TRANSLATION\CropScanAI\translations\hi\LC_MESSAGES\messages.mo'

print("Step 1: Reading PO file...")

# Read the PO file with proper encoding
try:
    # First, clean the PO file to remove BOM
    with open(po_file, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    # Write back without BOM
    temp_po = po_file.replace('.po', '_temp.po')
    with open(temp_po, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Cleaned PO file")
    
    # Load the cleaned PO file
    po = polib.pofile(temp_po, encoding='utf-8')
    print(f"✓ Loaded {len(po)} entries")
    
    # Ensure proper metadata
    po.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': 'you@example.com',
        'POT-Creation-Date': '2025-10-06 19:15+0530',
        'PO-Revision-Date': '2025-10-06 19:16+0530',
        'Last-Translator': 'Your Name <your@email.com>',
        'Language-Team': 'Hindi <hi@li.org>',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
        'Generated-By': 'Babel 2.17.0',
        'Language': 'hi',
    }
    
    print("✓ Set proper metadata")
    
    # Create directory if needed
    os.makedirs(os.path.dirname(mo_file), exist_ok=True)
    
    print("\nStep 2: Compiling to MO file...")
    
    # Save as MO file
    po.save_as_mofile(mo_file)
    
    print(f"✓ Successfully compiled!")
    print(f"\nFiles:")
    print(f"  PO: {po_file}")
    print(f"  MO: {mo_file}")
    print(f"\nEntries: {len(po)}")
    print(f"Translated: {len([e for e in po if e.msgstr])}")
    
    # Clean up temp file
    if os.path.exists(temp_po):
        os.remove(temp_po)
    
    # Verify the MO file can be read
    print("\nStep 3: Verifying MO file...")
    mo_test = polib.mofile(mo_file)
    print(f"✓ MO file is valid with {len(mo_test)} entries")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
