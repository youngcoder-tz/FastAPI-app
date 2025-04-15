import polib
import os
from pathlib import Path
from fastapi import HTTPException

class UITranslator:
    def __init__(self):
        self.translations = {}
        try:
            for lang in ['en', 'sw', 'fr']:
                po_path = Path(f"locales/{lang}/LC_MESSAGES/ui.po")
                if po_path.exists():
                    self.translations[lang] = polib.pofile(po_path)
                else:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Translation file missing for {lang}"
                    )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Translation system error: {str(e)}"
            )

    def get_translation(self, msgid: str, lang: str = 'en') -> str:
        if lang not in self.translations:
            return msgid
        entry = self.translations[lang].find(msgid)
        return entry.msgstr if entry else msgid