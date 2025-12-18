import json
import os
from typing import Optional


class I18n:
    def __init__(self, locales_dir: str, default_language: str = "uz"):
        self.locales_dir = locales_dir
        self.default_language = default_language
        self.translations = {}
        self._load_translations()

    def _load_translations(self):
        """Load all translation files from locales directory."""
        if not os.path.exists(self.locales_dir):
            os.makedirs(self.locales_dir)
            return

        for filename in os.listdir(self.locales_dir):
            if filename.endswith(".json"):
                lang = filename.replace(".json", "")
                file_path = os.path.join(self.locales_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        self.translations[lang] = json.load(f)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def get(self, key: str, language: str = None, **kwargs) -> str:
        """Get translation for a key in the specified language."""
        if language is None:
            language = self.default_language

        # Fallback to default language if language not found
        if language not in self.translations:
            language = self.default_language

        # Get translation, fallback to key if not found
        translation = self.translations.get(language, {}).get(key, key)

        # Format with provided kwargs
        try:
            return translation.format(**kwargs)
        except KeyError:
            return translation

    def get_available_languages(self) -> list[str]:
        """Get list of available languages."""
        return list(self.translations.keys())


# Create global i18n instance
i18n = I18n(locales_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)), "locales"))
