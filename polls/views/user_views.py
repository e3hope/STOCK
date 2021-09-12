from django.shortcuts import render, redirect
from django.http import response,HttpRequest,HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from ..models import User, UserCapital
from datetime import datetime
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
import json
import string
import random
import hashlib
import base64
import requests

# 로그인
@csrf_exempt
def login(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        data = {'error':1}
        try:
            queryset = User.objects.filter(id = request_data['id'])
            serialize = serializers.serialize('json', queryset)
            querydata = json.loads(serialize)[0]['fields']
            
            # 해쉬비번 검증 후 세션생성(로그인 성공)
            if check_password(request_data['pw'], querydata['password']) :
                request.session['id'] = querydata['id']
                data['error'] = 0
                data['data'] = {'id':querydata['id'],'name':querydata['name'],'email':querydata['email']}
        except:
            data['error'] = 1
        
        return JsonResponse(data,json_dumps_params={'ensure_ascii': False})

# 로그아웃
@csrf_exempt
def logout(request):
    data = {'error':1}
    try:
        request.session.clear()
        data['error'] = 0
    except:
        data['error'] = 1
    return JsonResponse(data,json_dumps_params={'ensure_ascii': False})

# 회원 가입
@csrf_exempt
def register(request):
   if request.method == 'POST':
        request_data = json.loads(request.body)
        user = User()
        user.id = request_data['id']
        user.password = make_password(request_data['pw'])
        user.name = request_data['name']
        user.email = request_data['email']
        user.date_insert = datetime.now()
        user.date_update = datetime.now()
        # 모의투자
        capital = UserCapital()
        capital.id = request_data['id']
        capital.capital = 10000000
        capital.date_check = datetime.today().strftime('%Y-%m-%d')
        capital.date_insert = datetime.now()
        capital.date_update = datetime.now()

        data = {'error':1}
        try:
            user.save()
            capital.save()
            data['error'] = 0
        except:
            data['error'] = 1
        return JsonResponse(data,json_dumps_params={'ensure_ascii': False})

# 정보 수정
@csrf_exempt
def edit(request):
    if request.method == 'POST':
        data = {'error':1}
        try:
            request_data = json.loads(request.body)
            user = User.objects.get(id=request.session['id'])
            
            # 정보 수정 데이터 확인 변수
            change_data = False
            
            # 정보 수정
            for k,v in request_data.items() :
                if v != request.session[k] :
                    setattr(user, k, v)
                    request.session[k] = v
                    change_data = True

            if change_data == True :
                user.save()
                data['error'] = 0

        except:
            data['error'] = 1

        return JsonResponse(data,json_dumps_params={'ensure_ascii': False})

# 패스워드 찾기
@csrf_exempt
def find_password(request):
    if request.method == 'POST':
        # email = EmailMessage(
        #     '[EasyStock]인증번호',      # 제목
        #     'Body goes here',           # 내용
        #     # 'e3hope21@gmail.com',       # 보내는 이메일 (settings에서 설정해서 작성안해도 됨)
        #     to=['e3hope@naver.com'],    # 받는 이메일 리스트
        # )
        # email.send()
        send_mail('[EasyStock]인증번호', 'contents', 'e3hope93@naver.com', ['e3hope@naver.com'], fail_silently=False)
        return HttpResponse('수정완료')