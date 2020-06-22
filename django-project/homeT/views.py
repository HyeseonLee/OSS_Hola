from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from .models import Video

#[JY]About User 
from django.contrib.auth.models import User  
from django.contrib import auth  

#[HS]About post_like
from django.views.decorators.http import require_POST
from django.http import HttpResponse

class VideoLoad(ListView):
    model = Video

    def get(self,request):
        template_name = 'home_be.html'
        VideoList = Video.objects.all()
        return render(request, template_name, {'VideoList':VideoList})

@require_POST
def post_like(request):
    pk = request.POST.get('pk',None)
    video = get_object_or_404(Video, pk=pk)
    video_like, video_like_created = video.like_set.get_or_created(user=request.user)

    if not video_like_created:
        video_like.delete()
        message="좋아요 취소"
    else:
        message = "좋아요"
    context={'like_count':video.like_count,
    'message': message} # 'nickname':request.user.profile.닉네임 context로 추가 예정

    return HttpResponse(json.dumps(context), content_type='application/json') #context를 json타입으로 보낸다)


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            #auth.login(request, user)
            return redirect('correct')
        else:
            return redirect('uncorrect')
    return render(request, 'signup_be.html')

def correct(request):
    return render(request, 'signup_correct_be.html')

def uncorrect(request):
    return render(request, 'signup_uncorrect_be.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'unlog_be.html')
    else:
        return render(request, 'login_be.html')

def unlog(request):
    return render(request, 'unlog_be.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return render(request, 'home.html')












