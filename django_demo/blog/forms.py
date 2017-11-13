from django.forms import Form
from .models import Feedback


class FeedbackForm(Form):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'question']
