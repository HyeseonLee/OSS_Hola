from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
# [JY] User Model 작업때문에 잠시 주석처리합니다.
from .models import Video

#[JY]About User 
from django.contrib.auth.models import User  
from django.contrib import auth, messages #messages for video_like
from django.contrib.auth import get_user_model
User = get_user_model()

# [JY] User Model 작업때문에 잠시 주석처리합니다.-> 다시 살림
# [HS]About video_like
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import json

class VideoLoad(ListView):
    model = Video
    def get(self,request):
        template_name = 'home.html'
        VideoList = Video.objects.all()
        return render(request, template_name, {'VideoList':VideoList})

def detail(request, detail_id):
    detail_obj = get_object_or_404(Video, pk=detail_id)
    return render(request, 'detail_be.html', {'detailObj':detail_obj})


@require_POST
def video_like(request):
    pk = request.POST.get('pk',None)
    video = get_object_or_404(Video, pk=pk)
    video_like, video_like_created = video.like_set.get_or_create(user=request.user)
    # get_or_create는 (꺼내려는 모델의 인스턴스, boolean flag)를 튜플 형식으로 반환한다.
    
    if not video_like_created:
        # video_like_created가 FALSE일때, 기존 DB에 이미 인스턴스가 있는 상태니까 이미 눌러진 좋아요를 삭제한다.
        video_like.delete()
        message="좋아요 취소"
    else:
        # video_like_created가 TRUE일때, 좋아요 상태가 아니었고, 좋아요를 할거다.
        message = "좋아요"
    context={'like_count':video.like_count,
    'message': message} # 'nickname':request.user.profile.닉네임 context로 추가 예정

    return HttpResponse(json.dumps(context), content_type='application/json') #context를 json타입으로 보낸다)

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'], 
                nickname=request.POST['nickname'],
                age=request.POST['age'],
                workingout=request.POST['workout_data']
                )
            auth.login(request, user)
            return redirect('correct')
        else:
            return redirect('uncorrect')
    return render(request, 'signup.html')

def correct(request):
    return render(request, 'signup_correct.html')

def uncorrect(request):
    return render(request, 'signup_uncorrect.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('main')
        else:
            return render(request, 'unlog.html')
    else:
        return render(request, 'login.html')

def unlog(request):
    return render(request, 'unlog.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return render(request, 'home.html')










