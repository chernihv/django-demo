from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from ..models.questions import Questions, Choice
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse


def all_question(request: HttpRequest):
    questions = Questions.objects.all()
    return render(request, 'blog/questions/all_questions.html', {'questions': questions})


def detail(request: HttpRequest, question_id: int):
    question = get_object_or_404(Questions, id=question_id)
    choices = question.choice_set.all()
    return render(request, 'blog/questions/question_detail.html', {'question': question, 'choices': choices})


def result(request: HttpRequest, question_id: int):
    question = get_object_or_404(Questions, id=question_id)
    return render(request, 'blog/questions/vote_results.html', {'question': question})


def vote(request: HttpRequest, question_id: int):
    question = get_object_or_404(Questions, id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'blog/questions/question_detail.html', {
            'question': question,
            'error_message': 'Вы не выбрали пункт',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('blog:vote_result', args=(question_id,)))
