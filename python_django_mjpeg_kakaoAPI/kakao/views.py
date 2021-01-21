from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from kakao.forms import KaKaoTalkForm
import json
import requests
from django.contrib import messages
client_id = "a2d9314abe916b9a1c4836315083488d" #rest key

class KakaoLoginView(TemplateView):
    template_name = "kakao_login.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_id"] = client_id
        return context

class KakaoAuthView(TemplateView):
    template_name = "kakao_token.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = self.request.GET['code']
        token = self.getAccessToken(code)
        context["client_id"] = client_id
        context["token"] = token        
        self.save_access_token(token["access_token"])
        return context
    # 세션 코드값 code 를 이용해서 ACESS TOKEN과 REFRESH TOKEN을 발급 받음
    def getAccessToken(self, code):
        url = "https://kauth.kakao.com/oauth/token"
        payload = "grant_type=authorization_code"
        payload += "&client_id=" + client_id
        payload += "&redirect_url=http://192.168.43.60:8000/kakao/oauth&code=" + code #redirect url
    
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.post(url, data=payload, headers=headers)
        return response.json()
    
    def save_access_token(self, access_token):
        with open("access_token.txt", "w") as f:
            f.write(access_token)

class KakaoTalkView(FormView):
    form_class = KaKaoTalkForm
    template_name = "kakao_form.html"
    success_url = "/kakao/talk"
    def form_valid(self, form):
        res, text = form.send_talk()    # 실제 데이터 보내는 것이므로 중요함
        if res.json().get('result_code') == 0:
            messages.add_message(self.request, messages.SUCCESS, "메시지 전송 성공 : " + text)
        else:
            messages.add_message(self.request, messages.ERROR, "메시지 전송 실패 : " + str(res.json()))
        return super().form_valid(form)