import polib
from pathlib import Path

def validate_locales():
    errors = []
    required_keys = ["welcome_message", "complaint_instructions"]
    
    for lang in ['en', 'sw', 'fr']:
        po_path = Path(f"locales/{lang}/LC_MESSAGES/ui.po")
        if not po_path.exists():
            errors.append(f"Missing PO file for {lang}")
            continue
            
        try:
            po = polib.pofile(po_path)
            for key in required_keys:
                if not po.find(key):
                    errors.append(f"Missing translation key '{key}' in {lang}")
        except Exception as e:
            errors.append(f"Invalid PO file {lang}: {str(e)}")
    
    if errors:
        raise RuntimeError("Locale validation failed:\n" + "\n".join(errors))