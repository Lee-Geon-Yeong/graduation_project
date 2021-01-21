from django import forms
import json
import requests
class KaKaoTalkForm(forms.Form):
    text = forms.CharField(label='전송할 Talk', max_length=300)
    web_url = forms.CharField(label='Web URL', max_length=300, initial='http://192.168.43.60:8000/mjpeg?mode=stream')
    mobile_web_url = forms.CharField(label='Mobile URL', max_length=300, initial='http://192.168.43.60:8000/mjpeg?mode=stream')
    def send_talk(self):
        talk_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        with open("access_token.txt", "r") as f:
            token = f.read()
        header = {"Authorization": f"Bearer {token}"}
        text_template = {
            'object_type': 'text',
            'text': self.cleaned_data['text'],      # 여기서 보내고 싶은 내용 보내면 됨
            'link': {
                'web_url': self.cleaned_data['web_url'],
                'mobile_web_url': self.cleaned_data['mobile_web_url']
            },
            'button_title' : "카메라 보기"
        }
        print(text_template)
        payload = {'template_object': json.dumps(text_template)}
        res = requests.post(talk_url, data=payload, headers=header)
        return res, self.cleaned_data['text']    

# template_object={
#     "object_type": "feed",
#     "content": {
#         "title": "디저트 사진",
#         "description": "아메리카노, 빵, 케익",
#         "image_url": "http://mudkage.kakao.co.kr/dn/NTmhS/btqfEUdFAUf/FjKzkZsnoeE4o19klTOVI1/openlink_640x640s.jpg",
#         "image_width": 640,
#         "image_height": 640,
#         "link": {
#             "web_url": "http://www.daum.net",
#             "mobile_web_url": "http://m.daum.net",
#             "android_execution_params": "contentId=100",
#             "ios_execution_params": "contentId=100"
#         }
#     },
#     "social": {
#         "like_count": 100,
#         "comment_count": 200,
#         "shared_count": 300,
#         "view_count": 400,
#         "subscriber_count": 500
#     },        
#     "buttons": [
#         {
#             "title": "웹으로 이동",
#             "link": {
#                 "web_url": "http://www.daum.net",
#                 "mobile_web_url": "http://m.daum.net"
#             }
#         },
#         {
#             "title": "앱으로 이동",
#             "link": {
#                 "android_execution_params": "contentId=100",
#                 "ios_execution_params": "contentId=100"
#             }
#         }
#     ]
# }    