from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.serializers import *
from api.models import Department, Question, Answer
from api.permissions import EditPermission, UserEditPermission


class UserCreate(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, UserEditPermission]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class QuestionListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.filter(is_active=True, users_flagged=None)
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, EditPermission]

    def get_queryset(self):
        """
        This view should return the question with given id
        if is_active field is set to True
        """
        q_id = self.kwargs['pk']
        return Question.objects.filter(id=q_id, is_active=True, users_flagged=None)
    serializer_class = QuestionSerializer

    def update(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        if question.answer_set.filter(is_active=True).count() > 0:
            return Response({"detail": "Answered questions cannot be updated"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, args, kwargs)

    def delete(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        question.is_active = False
        question.save()
        return Response({"detail": "Question deleted"}, status=status.HTTP_204_NO_CONTENT)


class QuestionFlagsCreate(generics.CreateAPIView):
    def get_queryset(self):
        """
        This view should return the question with given id
        if is_active field is set to True
        """
        q_id = self.kwargs['pk']
        return Question.objects.filter(id=q_id, is_active=True)
    serializer_class = QuestionFlagSerializer
    permission_classes = [IsAuthenticated]

    # maybe use restframework exception handler instead of overriding.
    def create(self, request, *args, **kwargs):
        try:
            return super(QuestionFlagsCreate, self).create(request, *args, **kwargs)
        except IntegrityError:
            return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnswerFlagsCreate(generics.CreateAPIView):
    def get_queryset(self):
        """
        This view should return the answer with given id
        if is_active field is set to True
        """
        a_id = self.kwargs['pk']
        return Answer.objects.filter(id=a_id, is_active=True)
    serializer_class = AnswerFlagSerializer
    permission_classes = [IsAuthenticated]

    # maybe use restframework exception handler instead of overriding.
    def create(self, request, *args, **kwargs):
        try:
            return super(AnswerFlagsCreate, self).create(request, *args, **kwargs)
        except IntegrityError:
            return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnswerListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        question = Question.objects.get(pk=self.kwargs['pk'])
        return question.answer_set.all().filter(is_active=True, users_flagged=None)
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        question=Question.objects.get(pk=self.kwargs['pk']))


class AnswerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, EditPermission]
    lookup_url_kwarg = 'val'

    def get_queryset(self):
        """
        This view should return the question with given id
        if is_active field is set to True
        """
        question = Question.objects.get(pk=self.kwargs['pk'])
        return Answer.objects.filter(pk=self.kwargs['val'], question=question, is_active=True, users_flagged=None)
    serializer_class = AnswerSerializer

    def delete(self, request, *args, **kwargs):
        answer = get_object_or_404(Answer, pk=kwargs['val'])
        answer.is_active = False
        answer.save()
        return Response({"detail": "Answer deleted"}, status=status.HTTP_204_NO_CONTENT)


def do_vote(request, model_text, model, kwargs):
    try:
        id = kwargs['pk']
        upvote = request.data['upvote'] == True
        if upvote:
            with transaction.atomic():
                question_or_answer = model.objects.get(
                    is_active=True, id=id)
                if request.user in question_or_answer.votes.all():
                    return Response({"detail": "Invalid %s vote" % (model_text)}, status=status.HTTP_400_BAD_REQUEST)
                question_or_answer.votes.add(request.user)
                question_or_answer.save()
                return Response({"votes": question_or_answer.votes.count()}, status=status.HTTP_200_OK)
        else:
            with transaction.atomic():
                question_or_answer = model.objects.get(
                    is_active=True, id=id)
                if request.user not in question_or_answer.votes.all():
                    return Response({"detail": "Invalid %s vote" % (model_text)}, status=status.HTTP_400_BAD_REQUEST)
                question_or_answer.votes.remove(request.user)
                question_or_answer.save()
                return Response({"votes": question_or_answer.votes.count()}, status=status.HTTP_200_OK)
    except (MultiValueDictKeyError, KeyError):
        return Response({"detail": "Missing required paramter"}, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        return Response({"detail": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except ObjectDoesNotExist:
        return Response({"detail": "%s does not exist" % (model_text)}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"detail": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def vote_question(request, **kwargs):
    return do_vote(request, "Question", Question, kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def vote_answer(request, **kwargs):
    return do_vote(request, "Answer", Answer, kwargs)
