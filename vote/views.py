from django.shortcuts import render, redirect
from .models import Topic, Choice
from django.contrib import messages

# Create your views here.
def index(request):
    t = Topic.objects.all()

    context = {
        "tset" : t
    }
    return render(request, "vote/index.html", context)

def detail(request, tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()
    context = {
        "t" : t,
        "cset" : c
    }
    return render(request, "vote/detail.html", context)

def vote(request, tpk):
    t = Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():
        t.voter.add(request.user)
        cpk = request.POST.get("cho")
        c = Choice.objects.get(id=cpk)
        c.choicer.add(request.user)
    messages.info(request, "투표가 이루어졌습니다")
    return redirect("vote:detail", tpk)

def cancel(request, tpk):
    u = request.user
    t = Topic.objects.get(id=tpk)
    t.voter.remove(u)
    u.choice_set.get(top=t).choicer.remove(u)
    messages.info(request, "투표를 무르셨습니다")
    return redirect("vote:detail", tpk)

def create(request):
    if request.user.is_anonymous:
        messages.error(request, "비정상적인 접근입니다")
        return redirect("acc:login")

    if request.method == "POST":
        s = request.POST.get("sub")
        user = request.user
        c = request.POST.get("con")
        ch = request.POST.getlist("cho")
        cm = request.POST.getlist("com")
        t = Topic(subject = s, maker = user, content = c)
        t.save()
        for name, com in zip(ch, cm):
            Choice(top=t, name=name, comment=com).save()
        messages.success(request, "해당 주제의 투표가 생성되었습니다")
        return redirect('vote:index')
    return render(request, "vote/create.html")

def update(request, tpk):
    t = Topic.objects.get(id=tpk)
    if not request.user == t.maker:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('vote:index')

    cset = Choice.objects.filter(top=t)
    cs = t.choice_set.all
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        ch = request.POST.getlist("cho")
        cm = request.POST.getlist("com")
        nch = request.POST.getlist("ncho")
        ncm = request.POST.getlist("ncom")
        t.subject, t.content = s, c
        t.save()

        for i, name, com in zip(cset, ch, cm):
            i.name, i.comment = name, com
            i.save()

        for na, co in zip(nch, ncm):
            Choice(top=t, name=na, comment=co).save()
            
        messages.success(request, "해당 주제의 투표가 수정되었습니다")
        return redirect('vote:index')

    context = {
        "t" : t,
        "cset" : cs
    }
    return render(request, "vote/update.html", context)

def delete(request, tpk):
    t = Topic.objects.get(id=tpk)
    if request.user == t.maker:
        t.delete()
        messages.info(request, "해당 주제의 투표가 삭제되었습니다")
    else:
        messages.error(request, "비정상적인 접근입니다")
    return redirect("vote:index")

def delete_choice(request, cpk, tpk):
    c = Choice.objects.get(id=cpk)
    if request.user == c.top.maker:
        c.delete()
        messages.info(request, "해당 보기가 삭제되었습니다")
    else:
        messages.error(request, "비정상적인 접근입니다")
    return redirect("vote:update", tpk)