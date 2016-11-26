from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from .models import Teacher, Vote, Student
from rest_framework import serializers, generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
import datetime
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teacher
        fields = ('url', 'id', 'name', 'photo_path', 'school', 'career', 'vote')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('teacher', 'user', 'create_time')


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.all().order_by('sort')
    serializer_class = TeacherSerializer


class VoteView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request, format=None):
        vote_set = Vote.objects.all()
        serializer = VoteSerializer(vote_set, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        pass


def is_during_active_time():
    time_begin = datetime.datetime(2016, 11, 16, 8, 0, 0)
    time_end = datetime.datetime(2016, 11, 27, 17, 0, 0)
    return datetime.datetime.now() > time_begin and datetime.datetime.now() < time_end


def is_whu_student(name, sid):
    user_set = Student.objects.filter(sid=sid, name=name)
    if user_set:
        return True
    else:
        return False


def is_out_three_times(user):
    vote_set = Vote.objects.filter(user=user)
    date_list = []
    for item in vote_set:
        if item.create_time.date() not in date_list:
            date_list.append(item.create_time.date())
        if len(date_list) >= 3:
            return True
    return False


def is_vote_today(user):
    vote_set = Vote.objects.filter(user=user).order_by('-id')
    if len(vote_set):
        if vote_set[0].create_time.date() == datetime.datetime.now().date():
            return True
    else:
        return False


def is_under_ten_checked(vote_list):
    if len(vote_list) <= 10:
        return True
    else:
        return False


@csrf_exempt
def get_token(request):
    sid = request.POST['sid']
    name = request.POST['name']

    if not is_during_active_time():
        return JsonResponse({'statu': 1, 'info': '尚未开放'})

    user_set = User.objects.filter(username=name)
    if user_set:
        user = user_set[0]
        if is_vote_today(user) or is_out_three_times(user):
            return JsonResponse({'statu': 1, 'info': '今日已投过票或投票已达三次'})
    elif is_whu_student(name, sid):
        user = User.objects.create_user(
            name,
            '',
            'tvote2016'
        )
    else:
        return JsonResponse({'statu': 1, 'info': '身份验证失败'})


    token_set = Token.objects.filter(user=user)
    if token_set:
        token = token_set[0].key
    else:
        token = create_token(user)
    return JsonResponse({'statu': 0, 'info': '验证成功', 'token': token})


def create_token(user):
    token = Token.objects.create(user=user)
    print(token.key)
    return token.key


@csrf_exempt
def vote(request):
    user = Token.objects.get(key=request.POST['token']).user
    vote_list = request.POST.getlist('list[]')
    if len(vote_list) > 10:
        return JsonResponse({'info': '不能选择超过10个老师', 'statu': 0})
    for item in vote_list:
        vote_item = Vote(teacher_id=item, user=user)
        vote_item.save()
    return JsonResponse({'info': '投票成功', 'statu': 1})


def cs(request):
    sid = request.GET['sid']
    name = request.GET['name']
    stu = Student(sid=sid, name=name)
    stu.save()
    return HttpResponse('success')


def py(request):
    py = Vote(teacher_id=10, user_id=1)
    py.save()
    return HttpResponse(Teacher.objects.get(pk=10).vote)











