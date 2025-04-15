from lingua import LanguageDetector
from transformers import MarianMTModel, MarianTokenizer

class LanguageProcessor:
    SUPPORTED_LANGUAGES = {
        'sw': 'Swahili',
        'en': 'English',
        'fr': 'French'
    }

    def __init__(self):
        self.detector = LanguageDetector.from_preset('accuracy')
        self.models = {
            'sw': {'tokenizer': MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-sw-en'),
                   'model': MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-sw-en')},
            'fr': {'tokenizer': MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-fr-en'),
                   'model': MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-fr-en')}
        }

    def detect_language(self, text: str) -> str:
        result = self.detector.detect_language_of(text)
        return self.SUPPORTED_LANGUAGES.get(result.iso_code_639_1.name.lower(), 'en')

    async def translate(self, text: str, target_lang: str = 'en') -> str:
        if target_lang == 'en':
            src_lang = self.detect_language(text)
            if src_lang != 'en':
                model = self.models[src_lang]
                inputs = model['tokenizer'](text, return_tensors="pt")
                outputs = model['model'].generate(**inputs)
                return model['tokenizer'].decode(outputs[0], skip_special_tokens=True)
        return text