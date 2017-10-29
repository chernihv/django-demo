from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from ..models.questions import Questions, Choice
from django.shortcuts import render, get_object_or_404


def all_question(request: HttpRequest):
    questions = Questions.objects.all()
    return render(request, 'blog/questions/all_questions.html', {'questions': questions})


def detail(request: HttpRequest, question_id: int):
    question = get_object_or_404(Questions, id=question_id)
    choices = question.choice_set.all()
    return render(request, 'blog/questions/question_detail.html', {'question': question, 'choices': choices})


def result(request: HttpRequest, question_id: int):
    return HttpResponse('Result questions: {q_id}'.format(q_id=question_id))


def vote(request: HttpRequest, question_id: int, choice_id: int):
    choice = Choice.objects.get(id=choice_id)
    choice.votes += 1
    choice.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
