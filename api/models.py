from askvce.settings import EMAIL_FORMAT
from api.managers import UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from .managers import UserManager


class Department(models.Model):
    """
    Represents information about a department.
    """

    code = models.CharField(max_length=4, editable=False)
    name = models.CharField(max_length=150, editable=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx'),
        ]


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing the student
    """

    email = models.EmailField(_('email address'), unique=True, validators=[RegexValidator(
        regex=EMAIL_FORMAT, message="Enter valid organization email")])
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    dob = models.DateField(_('date of birth'))
    grad_year = models.IntegerField(validators=[
        RegexValidator(regex=('2\d{3}'), message="Enter valid grad_year: ")],)
    htno = models.CharField(max_length=15, validators=[
        RegexValidator(regex=('1602-\d{2}-7\d{2}-\d{3}'), message="Enter valid college htno: ")], unique=True)
    phone = models.CharField(max_length=10, validators=[
        RegexValidator(regex=('\d{10}'), message="Enter your phone no: ")], unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    usefullness_score = models.IntegerField(default=3)

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'htno'

    REQUIRED_FIELDS = ['email', 'user_name', 'first_name', 'last_name', 'dob',
                       'grad_year', 'phone']

    def __str__(self) -> str:
        return self.htno

    class Meta:
        indexes = [
            models.Index(fields=['htno'], name='htno_idx'),
            models.Index(fields=['phone'], name='phone_idx'),
        ]


class Tag(models.Model):
    """
    Tag represents a topic or category about a question
    """

    slug = models.CharField(max_length=50, unique=True, primary_key=True)
    description = models.TextField()

    def __str__(self):
        return self.slug

    class Meta:
        indexes = [
            models.Index(fields=['slug'], name='slug_idx'),
        ]


class Question(models.Model):
    """
    Question model representing a question asked
    """

    scope = (
        ('branch_grad_year', 'Same Brach Same Year'),
        ('grad_year', 'Same Year'),
        ('college', 'Entire College')
    )

    title = models.CharField(max_length=500)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    scope = models.CharField(max_length=50, choices=scope, default='college')
    tags = models.ManyToManyField(Tag)
    users_flagged = models.ManyToManyField(
        User, related_name='questions_flagged', through='QuestionFlag')
    votes = models.ManyToManyField(
        User, related_name='questions_upvoted', blank=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['user'], name='question_user_idx'),
        ]


class QuestionFlag(models.Model):
    """
    Related information about a question flagged.
    """

    reasons = (
        ('nsfw', 'Adult/Violent Content (Not Safe For Work)'),
        ('prom', 'Paid Promotion'),
        ('hurt', 'Hurting Sentiments'),
        ('less', 'Useless or not helpful')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=reasons)

    def __str__(self):
        return str(self.reason)

    class Meta:
        unique_together = ('user', 'question')
        indexes = [
            models.Index(fields=['user'], name='question_flag_user_idx'),
            models.Index(fields=['question'], name='question_flag_idx'),
        ]


class Answer(models.Model):
    """
    Answer model representing an answer for a question
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    body = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    users_flagged = models.ManyToManyField(
        User, related_name='answers_flagged', through='AnswerFlag')

    votes = models.ManyToManyField(
        User, related_name='answers_upvoted', blank=True)

    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['user'], name='answer_user_idx'),
            models.Index(fields=['question'], name='answer_question_idx'),
        ]


class AnswerFlag(models.Model):
    """
    Related information about a question flagged.
    """

    reasons = (
        ('nsfw', 'Adult/Violent Content (Not Safe For Work)'),
        ('prom', 'Paid Promotion'),
        ('hurt', 'Hurting Sentiments'),
        ('less', 'Useless or not helpful')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=reasons)

    def __str__(self):
        return str(self.reason)

    class Meta:
        unique_together = ('user', 'answer')
        indexes = [
            models.Index(fields=['user'], name='answer_flag_user_idx'),
            models.Index(fields=['answer'], name='answer_flag_idx'),
        ]
