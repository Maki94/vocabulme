import json
import requests
import codecs
from settings import DETECT_LANGUAGE_API


class DetectLanguageAPI:
    @staticmethod
    def is_english(text: str) -> bool:
        r = requests.post("http://ws.detectlanguage.com/0.2/detect",
                          data={'q': text, 'key': DETECT_LANGUAGE_API['key']})
        if r.status_code == 200:
            if isinstance(r.content, bytes):
                data = json.loads(codecs.decode(r.content, "utf-8"))
            else:
                data = json.loads(r.content)
            return data['data']['detections'][0]['language'] == 'en'


if __name__ == '__main__':
    print(DetectLanguageAPI.is_english("Buenos dias señor"), "\n")
    print(DetectLanguageAPI.is_english("Hello World!"), "\n")
