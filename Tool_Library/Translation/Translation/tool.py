import random
import requests
import hashlib
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import os
BASE_MODEL = "facebook/nllb-200-distilled-600M"
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'


def get_translation_nllb(input_text: str or list, tgt_lang: str, src_lang: str, max_length: int,
                         access_token: str = "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") -> str or list:
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL, src_lang=src_lang, token=access_token, mirror='https://hf-mirror.com')
    model = AutoModelForSeq2SeqLM.from_pretrained(
        BASE_MODEL, mirror='https://hf-mirror.com')
    inputs = tokenizer(input_text, return_tensors="pt", padding=True)
    translated_tokens = model.generate(
        **inputs, forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang], max_length=max_length)
    if isinstance(input_text, str):
        translations = tokenizer.batch_decode(
            translated_tokens, skip_special_tokens=True)[0]
    elif isinstance(input_text, list):
        translations = tokenizer.batch_decode(
            translated_tokens, skip_special_tokens=True)
    return translations


endpoint = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
fromLang = 'auto'
salt = random.randint(32768, 65536)
header = {'Content-Type': 'application/x-www-form-urlencoded'}


def get_translation_baidu(text: str, tgt_lang: str,
                          appid: str = '',
                          secret_key: str = '') -> str:
    sign = appid + text + str(salt) + secret_key
    md = hashlib.md5()
    md.update(sign.encode(encoding='utf-8'))
    sign = md.hexdigest()
    data = {
        "appid": appid,
        "q": text,
        "from": fromLang,
        "to": tgt_lang,
        "salt": salt,
        "sign": sign
    }
    response = requests.post(endpoint, params=data, headers=header)
    text = response.json()
    try:
        results = text['trans_result'][0]['dst']
        return results
    except:
        return response.text


if __name__ == '__main__':
    print(get_translation_baidu('apple', 'zh'))
    print(get_translation_nllb('apple is red', 'zho_Hans', 'eng_Latn', 100))
