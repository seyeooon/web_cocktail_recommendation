from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# 로그인 처리
def login_view(request):
    return render(request, 'login/login_page.html')  # 로그인 페이지 템플릿을 렌더링


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('main_page')  # 로그인 성공 시 메인 페이지로 리다이렉트
        else:
            messages.error(request, 'Invalid username or password')  # 로그인 실패 시 메시지 출력

    return render(request, 'login/login_page.html')

# 회원가입 처리
def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # 새로운 유저 저장
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # 회원가입 후 자동 로그인
                return redirect('main_page')  # 메인 페이지로 리다이렉트
        else:
            messages.error(request, 'Error during registration')  # 회원가입 실패 시 메시지

    else:
        form = UserCreationForm()

    return render(request, 'login/signup_page.html', {'form': form})
