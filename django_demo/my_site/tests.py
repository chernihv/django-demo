import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question


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
        old_question= Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_normal_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        normal_question = Question(pub_date=time)
        self.assertEqual(normal_question.was_published_recently(), True)
