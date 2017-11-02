from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpRequest
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'my_site/questions.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return last five published questions"""
        return Question.objects.filter(
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'my_site/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'my_site/results.html'


def vote(request: HttpRequest, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'my_site/detail.html', {
            'question': question,
            'error_message': 'Вы не выбрали пункт',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('my_site:results', args=(question_id,)))
