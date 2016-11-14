from django.shortcuts import render
from rest_framework.response import Response
from .models import Teacher, Vote
from rest_framework import serializers, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('url', 'name', 'photo_path', 'school', 'career')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('teacher', 'user', 'create_time')


class TeacherList(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class VoteView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request, format=None):
        vote_set = Vote.objects.all()
        serializer = VoteSerializer(vote_set, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        return


def is_during_active_time():
    pass


def is_whu_student():
    pass


def is_under_three():
    pass


def is_vote_today():
    pass


def is_under_ten_checked():
    pass


def get_token():
    pass





