from django.utils.functional import new_method_proxy
from api.tests.test_setup import *
from api.models import Department, Question, Tag
from django.contrib.auth import get_user_model
from django.urls import reverse


# TODO find a better way to test with dummy data
# TODO avoid code repetition


class TestViews(TestSetUp):

    def create_user(self, user_data, dept):
        user_data['department'] = dept.pk
        res = self.client.post(reverse(self.user_C),
                               user_data)
        self.assertEqual(res.status_code, 201)

    def test_user_and_dept_endpoints(self):
        # user cannot register with no data
        res = self.client.post(reverse(self.user_C))
        self.assertEqual(res.status_code, 400)

        # department endpoint has data without logging in
        res = self.client.get(reverse(self.dept_L))
        self.assertEqual(res.status_code, 200)

        # user can create with valid data
        self.create_user(self.user_data_1, self.cse_dept)

        user = get_user_model().objects.get(htno=self.user_data_1['htno'])
        # user cannot update without login
        new_data = self.user_data_1
        new_data['grad_year'] = 2023
        res = self.client.post(
            reverse(self.user_RUD, args=[user.pk]), new_data)
        self.assertEqual(res.status_code, 403)

        # user cannot login before activation
        self.assertFalse(self.client.login(
            htno=self.user_data_1['htno'], password=self.user_data_1['password']))

        # user cannot list without login
        res = self.client.get(reverse(self.user_RUD, args=(user.pk, )))
        self.assertEqual(res.status_code, 403)

        # user can login after activation
        user.is_active = True
        user.save()
        with self.Auth(user) as client:
            res = client.put(
                reverse(self.user_RUD, args=[user.pk]), new_data)
            self.assertEqual(res.status_code, 200)

            # can list after login
            res = client.get(reverse(self.user_RUD, args=(user.pk,)))
            self.assertEqual(res.status_code, 200)

        # create second user and try to see first user details
        self.create_user(self.user_data_2, self.civ_dept)
        user2 = get_user_model().objects.get(htno=self.user_data_2['htno'])
        with self.Auth(user) as client:
            res = client.get(reverse(self.user_RUD, args=(user2.pk, )))
            self.assertEqual(res.status_code, 403)

    def test_question(self):
        self.create_user(self.user_data_1, self.cse_dept)
        user = get_user_model().objects.get(htno=self.user_data_1['htno'])
        # cannot view questions unless logged in.
        res = self.client.get(reverse(self.question_LC))
        self.assertEqual(res.status_code, 403)

        # can view once logged in.
        with self.Auth(user) as client:
            res = client.get(reverse(self.question_LC))
            self.assertEqual(res.status_code, 200)

        general_tag = Tag.objects.get(slug='general')
        question_data = self.question_data_1
        question_data['user'] = user.pk
        question_data['tags'] = [general_tag.slug]

        # cannot create unless logged in.
        res = self.client.post(reverse(self.question_LC), question_data)
        self.assertEqual(res.status_code, 403)

        # can create after login
        with self.Auth(user) as client:
            res = client.post(reverse(self.question_LC), question_data)
            self.assertEqual(res.status_code, 201)
            question_data['id'] = res.data['id']
        # cannot retrieve particular question before login
        res = self.client.get(
            reverse(self.question_RUD, args=(question_data['id'],)))
        self.assertEqual(res.status_code, 403)

        # cannot update before login
        new_question_data = question_data.copy()
        new_question_data['title'] = 'new title'
        res = self.client.put(
            reverse(self.question_RUD, args=(new_question_data['id'],)), new_question_data)
        self.assertEqual(res.status_code, 403)

        # cannot vote before login
        res = self.client.post(
            reverse(self.question_vote, args=(question_data['id'],)), kwargs={'upvote': True})
        self.assertEqual(res.status_code, 403)

        # cannot delete before login
        self.assertEqual(self.client.delete(
            reverse(self.question_RUD, args=(question_data['id'], ))).status_code, 403)

        with self.Auth(user) as client:
            # can retrieve after login
            res = client.get(
                reverse(self.question_RUD, args=(question_data['id'],)))
            self.assertDictContainsSubset(question_data, res.data)
            self.assertEqual(res.status_code, 200)

            # no question then 404
            res = client.put(
                reverse(self.question_RUD, args=(self.invalid_id,)), new_question_data)
            self.assertEqual(res.status_code, 404)

            # can update after login
            res = client.put(
                reverse(self.question_RUD, args=(new_question_data['id'],)), new_question_data)
            self.assertEqual(res.status_code, 200)

            # removing a vote should be a problem
            res = client.post(reverse(self.question_vote, args=(
                question_data['id'],)), {'upvote': False})
            self.assertEqual(res.status_code, 400)

            # can vote after login
            res = client.post(reverse(self.question_vote, args=(
                question_data['id'],)), {'upvote': True})
            self.assertEqual(res.status_code, 200)

            # now vote count should be 1
            res = client.get(
                reverse(self.question_RUD, args=(question_data['id'], )))
            self.assertEqual(res.data['votes'], 1)
            self.assertTrue(res.data['has_voted'])
            self.assertDictContainsSubset(new_question_data, res.data)

            # error if missing parameter
            res = client.post(reverse(self.question_vote, args=(
                question_data['id'],)), {})
            self.assertEqual(res.status_code, 400)

            # error if voting for nonexistent question
            res = client.post(reverse(self.question_vote, args=(
                self.invalid_id,)), {'upvote': True})
            self.assertEqual(res.status_code, 404)

            # voting again should be a problem
            res = client.post(reverse(self.question_vote, args=(
                question_data['id'],)), {'upvote': True})
            self.assertEqual(res.status_code, 400)

            # removing a vote should not be a problem
            self.assertEqual(client.post(reverse(self.question_vote, args=(
                question_data['id'],)), {'upvote': False}).status_code, 200)

            # removing again should be a problem
            self.assertEqual(client.post(reverse(self.question_vote, args=(
                question_data['id'],)), {'upvote': False}).status_code, 400)

            # delete a nonexistent question
            self.assertEqual(client.delete(
                reverse(self.question_RUD, args=(self.invalid_id, ))).status_code, 404)

            # delete a question
            self.assertEqual(client.delete(
                reverse(self.question_RUD, args=(question_data['id'], ))).status_code, 204)

            # make sure no questions are there
            res = client.get(reverse(self.question_LC))
            self.assertEqual(len(res.data), 0)

        # question should not be visible if a user flags it.

    def test_answer(self):
        self.create_user(self.user_data_1, self.cse_dept)
        user = get_user_model().objects.get(htno=self.user_data_1['htno'])
        general_tag = Tag.objects.get(slug='general')
        question_data = self.question_data_1
        question_data['user'] = user.pk
        question_data['tags'] = [general_tag.slug]
        with self.Auth(user) as client:
            res = client.post(reverse(self.question_LC), question_data)
            self.assertEqual(res.status_code, 201)
            question_data['id'] = res.data['id']

            # create an answer
            answer_data = self.answer_data_1
            answer_data['question'] = question_data['id']
            answer_data['user'] = user.pk
            res = client.post(reverse(self.answer_LC, args=(
                question_data['id'], )), answer_data)
            self.assertEqual(res.status_code, 201)

            # answered questions cannot be edited
            new_question_data = question_data.copy()
            new_question_data['title'] = 'new title'
            res = client.put(reverse(self.question_RUD, args=(
                question_data['id'], )), new_question_data)
            self.assertEqual(res.status_code, 400)
        # cannot create answer before login

        # cannot view answer before login

        # cannot edit answer before login

        # cannot delete answer before login

        # cannot upvote/downvote before login

        # can create/update/view/edit/delete/vote answer after login

        # only user who created can edit/delete

        # answer should not be visible if any user flags it.
        pass
