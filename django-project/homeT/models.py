from django.conf import settings
from django.db import models
#[HS]About Tag extraction(using Regular expression)
import re

#[JY]About User Model
from django.contrib.auth.models import AbstractUser

class WorkOutCategory(models.Model) :
    categorys = models.CharField(max_length = 20, unique = True)

    def __str__(self):
        return self.categorys

class AgeCategory(models.Model) :
    categorys = models.CharField(max_length = 20, unique = True)

    def __str__(self):
        return self.categorys

class User(AbstractUser):
    nickname = models.TextField(blank=True, null=True)
    age = models.ForeignKey(AgeCategory, on_delete=models.CASCADE, null=True)
    workingout = models.ForeignKey(WorkOutCategory, on_delete=models.CASCADE, null=True)






# [JY] User Model 작업때문에 잠시 주석처리합니다.-> 다시 살림
class Video(models.Model):
    title = models.CharField(max_length=200)
    tagcontent = models.CharField(max_length=140, help_text="관련 태그를 최대 140자 입력 가능")
    v_id = models.CharField(max_length=140, help_text="youtube 영상 코드를 입력해주세요")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_user_set',through='Like') 
    tag_set = models.ManyToManyField('Tag', blank=True)

    @property
    def like_count(self):
        return self.like_user_set.count()

    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return self.title
    
    def tag_save(self):
        tags = re.findall(r'#(\w+)\b', self.tagcontent)
        #re.findall(정규표현식패턴, 텍스트) : 텍스트에서 정규표현식패터에 해당하는 값을 찾아서 리스트로 반환
        # #로 시작하고 
        # \w : 텍스트+숫자[a-zA-Z0-9] 
        # \b : 문자와 공백 사이의 문자
        # if not tags:
        #     return 
        for t in tags:
            tag, tag_created = Tag.objects.get_or_create(name=t)
            self.tag_set.add(tag) #ManyToMany에 인스턴스 추가
        

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.name