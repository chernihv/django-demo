import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question
from django.core.urlresolvers import reverse


def create_question(question_text: str, days: int):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('my_site:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        q = create_question(question_text='Test question', days=-30)
        response = self.client.get(reverse('my_site:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: ({id}) Question text: {text}>'.format(id=q.id, text=q.question_text)],
        )

    def test_index_view_with_a_future_and_old_question(self):
        create_question('Future question', days=5)
        q = create_question('Old question', days=-5)
        response = self.client.get(reverse('my_site:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: ({id}) Question text: {text}>'.format(id=q.id, text=q.question_text)],
        )


class QuestionMethodTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        Testing method was_published_recently() in class Question
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_normal_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        normal_question = Question(pub_date=time)
        self.assertEqual(normal_question.was_published_recently(), True)
