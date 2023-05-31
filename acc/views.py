from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, 'acc/index.html')

def login_user(request):
    if request.user.is_authenticated:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('acc:index')

    if request.method == "POST":
        un = request.POST.get("username")
        up = request.POST.get("password")
        user = authenticate(username = un, password = up)
        if user :
            login(request, user)
            messages.success(request, f"{user}님 환영합니다!")
            return redirect('acc:index')
        else :
            messages.info(request, "계정 정보가 일치하지 않습니다")
    return render(request, 'acc/login.html')

def logout_user(request):
    logout(request)
    messages.info(request, "로그아웃 되었습니다")
    return redirect('acc:index')

def signup(request):
    if request.user.is_authenticated:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('acc:index')

    if request.method == 'POST':
        un = request.POST.get("username")
        up = request.POST.get("upassword")
        ucp = request.POST.get("uchpassword")
        upc = request.FILES.get("upic")
        uc = request.POST.get("ucomment")
        
        try:
            if up == ucp :
                User.objects.create_user(username = un, password = up, comment = uc, pic = upc)
                messages.success(request, "회원가입이 성공적으로 이루어졌습니다")
                return redirect('acc:index')
            else:
                return redirect('acc:signup')
        except:
            messages.error(request, "비밀번호가 일치하지 않습니다")
    return render(request, 'acc/signup.html')

def profile(request):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect("acc:login")
    return render(request, 'acc/profile.html')

def update(request):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect("acc:login")

    if request.method == "POST":
        ue = request.POST.get("uemail")
        uc = request.POST.get("ucomment")
        up = request.FILES.get("upic")
        ua = request.POST.get("userage")
        user = request.user
        if up:
            user.pic.delete()
            user.pic = up
        user.email, user.comment, user.age = ue, uc, ua
        user.save()
        messages.success(request, "수정이 성공적으로 이루어졌습니다")
        return redirect('acc:profile')
    return render(request, 'acc/update.html')

def delete(request):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect("acc:login")

    user = request.user
    uep = request.POST.get("upassword")
    if check_password(uep, user.password):
        user.pic.delete()
        user.delete()
        messages.success(request, "계정이 성공적으로 삭제되었습니다")
        return redirect('acc:index')
    return redirect('acc:profile')

def chpass(request):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect("acc:login")

    user = request.user
    cp = request.POST.get("cpassword")
    if check_password(cp, user.password):
        np = request.POST.get("npassword")
        user.set_password(np)
        user.save()
        login(request, user)
        messages.success(request, "비밀번호 수정이 성공적으로 이루어졌습니다")
        return redirect('acc:profile')
    else:
        messages.error(request, "비밀번호가 일치하지 않습니다")
    return redirect('acc:update')