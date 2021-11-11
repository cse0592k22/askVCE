from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from api.models import Department, Question, Answer, QuestionFlag, AnswerFlag, Tag

user_data = ['1602-18-733-010@vce.ac.in', 'testuser', 'Test',
             'User', '2000-10-19', '2022', '1602-18-733-010',
             '1234567890', 'password56']


class UserAccountTests(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(*user_data)
        self.assertEqual(super_user.email, '1602-18-733-010@vce.ac.in')
        self.assertEqual(super_user.user_name, 'testuser')
        self.assertEqual(super_user.first_name, 'Test')
        self.assertEqual(super_user.last_name, 'User')
        self.assertEqual(super_user.htno, '1602-18-733-010')
        self.assertEqual(super_user.phone, '1234567890')
        self.assertEqual(super_user.grad_year, '2022')
        self.assertEqual(super_user.dob, '2000-10-19')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), '1602-18-733-010')

        with self.assertRaises(ValueError):
            user_data_invalid = user_data.copy()
            user_data_invalid[0] = 'foo@vce.ac.in'
            db.objects.create_user(*user_data_invalid)
            db.objects.create_superuser(*user_data, is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(*user_data, is_staff=False)

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(*user_data)
        self.assertEqual(user.email, '1602-18-733-010@vce.ac.in')
        self.assertEqual(user.user_name, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.htno, '1602-18-733-010')
        self.assertEqual(user.phone, '1234567890')
        self.assertEqual(user.grad_year, '2022')
        self.assertEqual(user.dob, '2000-10-19')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

        for i in range(len(user_data)):
            with self.assertRaises(ValueError):
                user_data_no_prop = user_data.copy()
                user_data_no_prop[i] = ''
                db.objects.create_user(*user_data_no_prop)

        with self.assertRaises(IntegrityError):
            db.objects.create_user(*user_data)


class DepartmentTests(TestCase):

    def test_string(self):
        department = Department.objects.create(
            code='CSE', name='Computer Science and Engineering')
        self.assertEqual(str(department), 'Computer Science and Engineering')


class TagTests(TestCase):

    def test_string(self):
        tag = Tag.objects.create(slug='new', description='blah blah..')
        self.assertEqual(str(tag), 'new')


class QuestionTests(TestCase):

    def test_object(self):
        db = get_user_model()
        user = db.objects.create_user(*user_data)
        question = Question.objects.create(
            user=user,
            title='q1?',
            body='now what?'
        )
        self.assertEqual(question.user, user)
        self.assertEqual(question.title, 'q1?')
        self.assertEqual(str(question), 'q1?')
        self.assertEqual(question.scope, 'college')
        self.assertEqual(question.body, 'now what?')
        self.assertTrue(question.is_active)


class QuestionFlagTests(TestCase):

    def test_object(self):
        db = get_user_model()
        user = db.objects.create_user(*user_data)
        question = Question.objects.create(
            user=user,
            title='q1?',
            body='now what?'
        )
        question_flag = QuestionFlag.objects.create(
            user=user,
            question=question,
            reason='hurt'
        )
        self.assertEqual(question_flag.user, user)
        self.assertEqual(question_flag.question, question)
        self.assertEqual(str(question_flag), 'hurt')
        self.assertEqual(question_flag.reason, 'hurt')


class AnswerTests(TestCase):

    def test_object(self):
        db = get_user_model()
        user = db.objects.create_user(*user_data)
        question = Question.objects.create(
            user=user,
            title='q1?',
            body='now what?'
        )
        answer = Answer.objects.create(
            question=question,
            user=user,
            body='nothing much'
        )
        self.assertEqual(answer.user, user)
        self.assertEqual(answer.question, question)
        self.assertEqual(str(answer), question.title)
        self.assertEqual(answer.body, 'nothing much')
        self.assertTrue(answer.is_active)


class AnswerFlagTests(TestCase):

    def test_object(self):
        db = get_user_model()
        user = db.objects.create_user(*user_data)
        question = Question.objects.create(
            user=user,
            title='q1?',
            body='now what?'
        )
        answer = Answer.objects.create(
            question=question,
            user=user,
            body='nothing much'
        )
        answer_flag = AnswerFlag.objects.create(
            user=user,
            answer=answer,
            reason='nsfw'
        )
        self.assertEqual(answer_flag.user, user)
        self.assertEqual(answer_flag.answer, answer)
        self.assertEqual(str(answer_flag), 'nsfw')
        self.assertEqual(answer_flag.reason, 'nsfw')
