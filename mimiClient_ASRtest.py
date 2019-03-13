import requests
import sys
import json


class mimiClientAPI:
    """mimiAPI"""

    def __init__(self, application_id, client_id, client_secret):
        self._client_id = application_id+':'+client_id
        self._client_secret = client_secret

    def get_accesstoken(self):
        """
        mimiアクセストークン取得
        """
        files = {
            'grant_type': (None, 'https://auth.mimi.fd.ai/grant_type/client_credentials'),
            'client_id': (None, self._client_id),
            'client_secret': (None, self._client_secret),
            'scope': (None, 'https://apis.mimi.fd.ai/auth/asr/websocket-api-service;https://apis.mimi.fd.ai/auth/asr/http-api-service;https://apis.mimi.fd.ai/auth/esr/websocket-api-service;https://apis.mimi.fd.ai/auth/esr/http-api-service;https://apis.mimi.fd.ai/auth/srs/speaker_groups.r;https://apis.mimi.fd.ai/auth/srs/speaker_groups.w;https://apis.mimi.fd.ai/auth/srs/speakers.r;https://apis.mimi.fd.ai/auth/srs/speakers.w;https://apis.mimi.fd.ai/auth/srs/speeches.r;https://apis.mimi.fd.ai/auth/srs/speeches.w;https://apis.mimi.fd.ai/auth/srs/trainers.r;https://apis.mimi.fd.ai/auth/srs/trainers.w;https://apis.mimi.fd.ai/auth/srs/websocket-api-service;https://apis.mimi.fd.ai/auth/srs/http-api-service;https://apis.mimi.fd.ai/auth/google-asr/websocket-api-service;https://apis.mimi.fd.ai/auth/google-asr/http-api-service;https://apis.mimi.fd.ai/auth/nict-asr/websocket-api-service;https://apis.mimi.fd.ai/auth/nict-asr/http-api-service'),
        }
        print("files : " , files)
        response = requests.post('https://auth.mimi.fd.ai/v2/token', files=files)
        accessToken = response.json()["accessToken"]
        return accessToken

    def voice_to_text(self, accessToken, input_file_path):
       """
       音声ー＞テキスト変換
       """
       #engine = "nict-asr"
       engine = "google-asr"
       #engine = "asr"
       headers = {
            'Content-Type': 'audio/x-pcm;bit=16;rate=48000;channels=1',
            'x-mimi-process': engine,
            'Authorization': 'Bearer '+accessToken,
       }
       data = open(input_file_path, 'rb').read()
       response = requests.post('https://service.mimi.fd.ai/', headers=headers, data=data)
       print(response)
       return response
       # return response.json()

    def output_file(self, text_list, file_path):
        with open(file_path, mode='w') as f:
            f.write('\n'.join(text_list))


if __name__=='__main__':
    """
    実行方法  (入力と出力のファイルは置いてあるパスまで指定）
    python text_evaluation.py input_excel/input_指向性_3_8.xlsx output_excel/output_指向性_3_8.xlsx
    """
    args = sys.argv
    # print(args[1], args[2], args[3], args[4], args[5])
    mimi_client_api = mimiClientAPI(args[1], args[2], args[3])
    accesstoken = mimi_client_api.get_accesstoken()
    print("accesstoken : ", accesstoken)
    response = mimi_client_api.voice_to_text(accesstoken, args[4])
    print("response : ", response)
    text_list = [i['result'] for i in response.json()['response']]
    mimi_client_api.output_file(text_list, args[5])
