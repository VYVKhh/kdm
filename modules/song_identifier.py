import requests
import time
import hmac
import hashlib
import base64

class SongIdentifier:
    def __init__(self):
        self.api_url = "https://identify-eu-west-1.acrcloud.com/v1/identify"  # عنوان API لـ ACRCloud
        self.access_key = "b0dea739056cbf6c326dc648ecb7fd27"  # مفتاح الوصول الذي قدمته
        self.access_secret = "YDxB87aFp6kJgNjDI0Xv3SNYPYkWjNbM7pRuqKRd"  # مفتاح السر الذي قدمته

    def identify_song(self, audio_file_path):
        # إعداد البيانات اللازمة للطلب
        data = {
            'access_key': self.access_key,
            'data_type': 'audio',
            'signature_version': '1',
            'timestamp': str(int(time.time())),
        }
        # حساب التوقيع الرقمي
        string_to_sign = f"{self.access_key}\n{data['data_type']}\n{data['signature_version']}\n{data['timestamp']}"
        signature = base64.b64encode(hmac.new(self.access_secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha1).digest()).decode('utf-8')
        data['signature'] = signature

        with open(audio_file_path, 'rb') as audio_file:
            files = {'sample': audio_file}
            response = requests.post(self.api_url, data=data, files=files)

        if response.status_code == 200:
            result = response.json()
            song_info = result.get('metadata', {}).get('music', [{}])[0].get('title', 'لم يتم العثور على معلومات الأغنية')
            return song_info
        else:
            return "حدث خطأ أثناء معرفة الأغنية. حاول مرة أخرى لاحقاً."