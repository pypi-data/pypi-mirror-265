'''File:get_translate.py
This file contains all functions to use Azure Translate service'''
import json
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
with open('config.json','r',encoding='utf-8') as f:
    config = json.load(f)
apikey = config.get('azure_translate_apikey')
endpoint = config.get('azure_translate_endpoint')
region = config.get("azure_translate_region")
def create_text_translation_client_with_credential():
    '''creates text translation variable using azure'''
    credential = TranslatorCredential(apikey, region)
    text_translator = TextTranslationClient(credential=credential,endpoint=endpoint)
    return text_translator
def get_language_code(language):
    '''azure language dictionary'''
    d = {"english":"en","french":"fr","german":"de","italian":"it"}
    try:
        result=d[language.lower()]
    except:
        result="en"
    return result
def to_target(query,target_language=None):
    '''converts the given query to english'''
    if target_language is None:
        target_language = ["en"]
    text_translator = create_text_translation_client_with_credential()
    input_text = [InputTextItem(text=f"{query}")]
    response = text_translator.translate(input_text,to=target_language)
    return response[0]["translations"][0]["text"]
def to_analysis(query,target_language=None):
    '''converts the given query to english'''
    if target_language is None:
        target_language = ["en"]
    text_translator = create_text_translation_client_with_credential()
    input_text = [InputTextItem(text=f"{query}")]
    response = text_translator.translate(input_text,to=target_language)
    return response
