import polib

# Path to your PO file
po_file = 'C:/Users/HP/Desktop/FORCE PUSH/translations/hi/LC_MESSAGES/messages.po'
# Path for the output MO file
mo_file = 'C:/Users/HP/Desktop/FORCE PUSH/translations/hi/LC_MESSAGES/messages.mo'


# Load the PO file
po = polib.pofile(po_file)

# Save as MO file
po.save_as_mofile(mo_file)

print("MO file generated successfully!")
