from rest_framework.test import APITestCase, APIClient
from api.models import Department, Tag


class TestSetUp(APITestCase):

    class Auth(object):
        """
        Returns an APIClient object after login.
        """

        def __init__(self, user) -> None:
            self.user = user
            self.client = APIClient()

        def __enter__(self):
            self.client.force_authenticate(user=self.user)
            return self.client

        def __exit__(self, exc_type, exc_value, tb):
            if exc_type is not None:
                return False
            self.client.logout()
            return True

    def setUp(self):
        self.user_data_1 = {
            'email': '1602-18-733-010@vce.ac.in',
            'dob': '2000-10-19',
            'grad_year': '2022',
            'user_name': 'foobar',
            'password': 'barfoo',
            'phone': '1234567890',
            'htno': '1602-18-733-956',
            'first_name': 'Foo',
            'last_name': 'Bar',
        }
        self.user_data_2 = {
            'email': '1602-18-733-011@vce.ac.in',
            'dob': '2000-10-19',
            'grad_year': '2022',
            'user_name': 'barfoo',
            'password': 'foobar',
            'phone': '1234567891',
            'htno': '1602-18-733-958',
            'first_name': 'Foo Two',
            'last_name': 'Bar',
        }
        self.question_data_1 = {
            'title': 'this is the title',
            'body': 'body of the question',
            'scope': 'college',
        }
        self.answer_data_1 = {
            'body': 'Hmm. sounds good'
        }
        self.general_tag = Tag.objects.get(slug='general')
        self.cse_tag = Tag.objects.get(slug='cse')
        self.cse_dept = Department.objects.get(code='CSE')
        self.civ_dept = Department.objects.get(code='CIV')

        self.dept_L = 'departments'
        self.user_C = 'users'
        self.user_RUD = 'user'
        self.question_LC = 'questions'
        self.question_RUD = 'question'
        self.answer_LC = 'question-answers'
        self.answer_RUD = 'question-answer'
        self.question_vote = 'question-vote'
        self.answer_vote = 'answer-vote'
        self.question_flag = 'question-flag'
        self.answer_flag = 'answer-flag'
        self.client = APIClient(enforce_csrf_checks=True)
        self.invalid_id = 999
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
