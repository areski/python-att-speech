# -*- coding: utf-8 -*-

import json
import requests


class ATTSpeech:
    CLIENT_ID = "CLIENT_ID"
    CLIENT_SECRET = "CLIENT_SECRET"
    TOKEN = None

    def __init__(self, *args, **kwargs):
        self.get_token()

    def get_token(self):
        # Get Access Token via OAuth.
        # https://matrix.bf.sl.attcompute.com/apps/constellation-sandbox
        response = requests.post("https://api.att.com/oauth/token", {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type": "client_credentials",
            "scope": "SPEECH,STTC,TTS"
        })
        content = json.loads(response.content)
        self.TOKEN = content["access_token"]

    def text_from_file(self, path):

        with open(path, 'rb') as f:
            response = requests.post("https://api.att.com/speech/v3/speechToText",
                headers={
                    "Authorization": "Bearer %s" % self.TOKEN,
                    "Accept": "application/json",
                    "Content-Type": "audio/wav",
                    "X-SpeechContext": "Generic",
                }, data=f)
        content = json.loads(response.content)
        return content

    def text2speech(self, text):
        filename = "hello.wav"

        response = requests.post("https://api.att.com/speech/v3/textToSpeech",
            headers={
                "Authorization": "Bearer %s" % self.TOKEN,
                "Accept": "audio/amr-wb",
                "Content-length": str(len(text)),
                "Content-Type": "text/plain",
            }, data=text)
        # import ipdb; ipdb.set_trace()
        if response.status_code == 200:
            with open(filename, 'w') as f:
                f.write(response.content)
            return filename
        else:
            return False


# if __name__ == '__main__':

#     # from ATTEngine import ATTSpeech
#     attspeech = ATTSpeech()

#     content = attspeech.text_from_file('/home/areski/public_html/Audio/cepstral.wav')
#     print(content)

#     content = attspeech.text2speech("Hello world, this is amazing!")
#     print(content)
