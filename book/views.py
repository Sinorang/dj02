from django.shortcuts import render, redirect
from .models import Book
from django.contrib import messages
# Create your views here.
def index(request):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('acc:index')

    b = request.user.book_set.all()
    context = {
        "bset" : b
    }
    return render(request, "book/index.html", context)

def create(request):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('acc:index')

    if request.method == 'POST':
        im = bool(request.POST.get("impo"))
        sn = request.POST.get("sname")
        su = request.POST.get("surl")
        sc = request.POST.get("scon")
        Book(user=request.user, site_name=sn, site_url=su, site_con=sc, impo=im).save()
        messages.info(request, "북마크가 생성되었습니다")
        return redirect('book:index')
    return render(request, "book/create.html")

def delete(request, bpk):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('acc:index')

    b = Book.objects.get(id=bpk)
    if b.user == request.user:
        b.delete()
        messages.success(request, "북마크가 성공적으로 삭제되었습니다")
    else:
        messages.error(request, "비정상적인 접근입니다")
    return redirect('book:index')

def update(request, bpk):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('acc:index')

    b = Book.objects.get(id=bpk)
    if request.method == 'POST':
        im = bool(request.POST.get("impo"))
        sn = request.POST.get("sname")
        su = request.POST.get("surl")
        sc = request.POST.get("scon")
        b.impo, b.site_name, b.site_url, b.site_con = im, sn, su, sc
        b.save()
        messages.info(request, "북마크가 수정되었습니다")
        return redirect('book:index')

    context = {
        "b" : b
    }
    return render(request, "book/update.html", context)