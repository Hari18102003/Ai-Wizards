from deep_translator import GoogleTranslator

# Function to translate text
def translate_text(text, target_language):
    """
    Translates a given text into the target language.

    :param text: The input text to be translated
    :param target_language: The language code (e.g., 'hi' for Hindi, 'ta' for Tamil)
    :return: Translated text
    """
    try:
        translator = GoogleTranslator(source="auto", target=target_language)
        return translator.translate(text)
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    input_text = "The doorman turned his attention to the Nert Red Eved Enernges from the Daarte, and we went on together to the Station The Children Client because of the cruelty of the world."
    language_code = "hi"  # Hindi
    
    translated_text = translate_text(input_text, language_code)
    
    if translated_text:
        print(f"Translated text in {language_code}: {translated_text}")
