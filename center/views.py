from django.shortcuts import render, redirect
from .models import Center, Response
from acc.models import User
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
def index(request):
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")
    pg = request.GET.get("page", 1)

    if kw:
        if cate == "sub":
            b = Center.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Center.objects.filter(customer=u)
            except:
                b = Center.objects.none()
        elif cate == "con":
            b = Center.objects.filter(content__contains=kw)
    else:
            b = Center.objects.all()

    b = b.order_by("-pubdate")

    pag = Paginator(b, 3)
    obj = pag.get_page(pg)
    context = {
        "bset" : obj,
        "cate" : cate,
        "kw": kw
    }
    return render(request, 'center/index.html', context)

def detail(request, bpk):
    if request.user.is_anonymous:
        messages.error(request, "해당 게시글은 회원만 볼 수 있습니다")
        return redirect("acc:login")
        
    b = Center.objects.get(id=bpk)
    r = b.response_set.all()
    context = {
        "b" : b,
        "rset" : r
    }
    return render(request, "center/detail.html", context)

def create(request):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect("acc:login")

    if request.method == "POST":
        user = request.user
        bs = request.POST.get("bsubject")
        bc = request.POST.get("bcontent")
        Center(subject = bs, customer = user, content = bc).save()
        messages.success(request, "게시글이 성공적으로 작성되었습니다")
        return redirect('center:index')
    return render(request, "center/create.html")

def delete(request, bpk):
    b = Center.objects.get(id=bpk)
    if b.customer == request.user:
        b.delete()
        messages.success(request, "게시글이 성공적으로 삭제되었습니다")
    else:
        messages.error(request, "비정상적인 접근입니다")
    return redirect('center:index')

def update(request, bpk):
    b = Center.objects.get(id=bpk)

    if b.customer == request.user:
        if request.method == "POST":
            bs = request.POST.get("bsubject")
            bc = request.POST.get("bcontent")
            b.subject, b.content = bs, bc
            b.save()
            messages.success(request, "게시글이 성공적으로 수정되었습니다")
            return redirect('center:index')
        else:
            pass
    else:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('center:index')
    context = {
        "b" : b
    }
    return render(request, 'center/update.html', context)

def creply(request, bpk):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('center:index')

    b = Center.objects.get(id=bpk)
    c = request.POST.get("com")
    Response(center = b, counselor = request.user, comment = c).save()
    return redirect('center:detail', bpk)
    
def dreply(request, bpk, rpk):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('center:index')

    r = Response.objects.get(id=rpk)
    if not request.user == r.counselor:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('center:index')
    else:
        r.delete()
        return redirect('center:detail', bpk)