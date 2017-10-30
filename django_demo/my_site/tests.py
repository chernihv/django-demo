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
