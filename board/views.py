from django.shortcuts import render, redirect
from .models import Board, Reply
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
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
    else:
            b = Board.objects.all()

    b = b.order_by("-pubdate")

    pag = Paginator(b, 3)
    obj = pag.get_page(pg)
    context = {
        "bset" : obj,
        "cate" : cate,
        "kw": kw
    }
    return render(request, 'board/index.html', context)

def detail(request, bpk):
    if request.user.is_anonymous:
        messages.error(request, "해당 게시글은 회원만 볼 수 있습니다")
        return redirect("acc:login")
        
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b" : b,
        "rset" : r
    }
    return render(request, "board/detail.html", context)

def create(request):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect("acc:login")

    if request.method == "POST":
        user = request.user
        bs = request.POST.get("bsubject")
        bc = request.POST.get("bcontent")
        Board(subject = bs, writer = user, content = bc).save()
        messages.success(request, "게시글이 성공적으로 작성되었습니다")
        return redirect('board:index')
    return render(request, "board/create.html")

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete()
        messages.success(request, "게시글이 성공적으로 삭제되었습니다")
    else:
        messages.error(request, "비정상적인 접근입니다")
    return redirect('board:index')

def update(request, bpk):
    b = Board.objects.get(id=bpk)

    if b.writer == request.user:
        if request.method == "POST":
            bs = request.POST.get("bsubject")
            bc = request.POST.get("bcontent")
            b.subject, b.content = bs, bc
            b.save()
            messages.success(request, "게시글이 성공적으로 수정되었습니다")
            return redirect('board:index')
        else:
            pass
    else:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('board:index')
    context = {
        "b" : b
    }
    return render(request, 'board/update.html', context)

def likey(request, bpk):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('board:index')

    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    messages.info(request, "좋아요를 누르셨습니다")
    return redirect("board:detail", bpk)

def unlikey(request, bpk):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('board:index')

    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    messages.info(request, "좋아요를 취소하셨습니다")
    return redirect("board:detail", bpk)

def creply(request, bpk):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('board:index')

    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    Reply(board = b, replyer = request.user, comment = c).save()
    return redirect('board:detail', bpk)
    
def dreply(request, bpk, rpk):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('board:index')

    r = Reply.objects.get(id=rpk)
    if not request.user == r.replyer:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('board:index')
    else:
        r.delete()
        return redirect('board:detail', bpk)