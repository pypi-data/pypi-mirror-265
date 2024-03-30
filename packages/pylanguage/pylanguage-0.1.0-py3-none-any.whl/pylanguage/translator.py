import pathlib
import json
from typing import List

"""
    Handle translations. All translations must be in <lang_code>.json file.
"""

class Translator:
    """
        Class that handles translation.
    """
    def __init__(self, base_file: str, lang_code: str, lang_dir: str, fallback_base: bool = True) -> None:
        """
            Initialization code.

            Args:

                - base_file    : string: File name containing base translations.
                - lang_code    : string: Language code of the requested translation.
                - lang_dir     : string: Directory where the base file and translations are stored.
                - fallback_base: string: Use base file if translation not found. Default is True.
            
            Returns:

                - None
        """
        self.fallback_base = fallback_base # Enable fallback to base file
        self.lang_code = lang_code # Language code
        self.lang_dir = lang_dir # Location of translations
        self.lang_file = pathlib.Path().joinpath(self.lang_dir, self.lang_code + '.json') # Translation file
        self.base_file = pathlib.Path().joinpath(self.lang_dir, base_file) # Base file
        self.translations = {} # Translations
        self.base = {} # Base strings

        # Check if base file exist. If it does, get the base translation.
        if pathlib.Path(self.base_file).exists():
            f = open(self.base_file)
            try:
                self.base = json.load(f)
            except Exception:
                raise Exception(f"Error parsing {self.base_file.resolve()}. Check if file is valid JSON.")
        else:
            raise FileNotFoundError(f"The file {self.base_file.resolve()} does not exist.")
        
        # Check if translation file exist. If it does, get the translation.
        if pathlib.Path(self.lang_file).exists():
            f = open(self.lang_file)
            try:
                self.translations = json.load(f)
            except Exception:
                raise Exception(f"Error parsing {self.lang_file.resolve()}. Check if file is valid JSON.")
        else:
            if not self.fallback_base:
                raise FileNotFoundError(f"The file {self.lang_file.resolve()} does not exist.")
            else:
                self.translations = self.base
    
        # Validate the translations.
        for i in self.base.keys():
            if not i in self.translations.keys():
                raise Exception(f"Error parsing {self.translations.resolve()}. All keys in {self.base_file.resolve()} are not found in translations.")
        
        # Validate the base.
        for i in self.translations.keys():
            if not i in self.base.keys():
                raise Exception(f"Error parsing {self.base_file.resolve()}. All keys in {self.translations.resolve()} are not found in base file.")

    def get(self, string: str):
        """
            Get the translation of the string.

            Args:

                - string: string: String whose translation is to be returned.
            
            Returns:

                - translation: string: The translation corresponding to string.
        """
        return self.translations[string]

    def get_lang(self):
        """
            Get the language code.
            
            Args:
            
                - None
           
            Returns:
                
                - lang_code: string: Language code of the translation file in use.
        """
        return self.lang_code