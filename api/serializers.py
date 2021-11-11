from django.urls.conf import path
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Answer, Department, Question, QuestionFlag, AnswerFlag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'user_name', 'first_name', 'last_name',
                  'dob', 'grad_year', 'htno', 'phone', 'department', 'password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'user_name': {'required': True},
            'htno': {'required': True, 'write_only': True},
            'dob': {'required': True, 'write_only': True},
            'grad_year': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
            'department': {'required': True},
            'password': {'required': True, 'write_only': True},
        }


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id', 'code', 'name', )


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    votes = serializers.SerializerMethodField()
    has_voted = serializers.SerializerMethodField()

    def get_votes(self, obj):
        return obj.votes.count()

    def get_has_voted(self, obj):
        user = self.context['request'].user
        if user in obj.votes.all():
            return True
        return False

    class Meta:
        model = Question
        fields = ('id', 'title', 'body', 'user', 'scope',
                  'tags', 'votes', 'has_voted', )


class QuestionFlagSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = QuestionFlag
        fields = ('id', 'user', 'question', 'reason')
        extra_kwargs = {
            'reason': {'required': True},
            'user': {'required': True},
            'question': {'required': True}
        }


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    question = serializers.ReadOnlyField(source='question.id')
    has_voted = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()

    def get_votes(self, obj):
        return obj.votes.count()

    def get_has_voted(self, obj):
        user = self.context['request'].user
        if user in obj.votes.all():
            return True
        return False

    class Meta:
        model = Answer
        fields = ('id', 'question', 'user', 'body', 'votes', 'has_voted',)
        extra_kwargs = {
            'body': {'required': True},
        }


class AnswerFlagSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = AnswerFlag
        fields = ('id', 'user', 'answer', 'reason')
        extra_kwargs = {
            'reason': {'required': True},
            'user': {'required': True},
            'question': {'required': True}
        }
