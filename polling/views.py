from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuestionForm, ChoiceForm, VoteForm
from .models import Question, Choice


def home(request):
    questions = Question.objects.all()
    context = {"questions": questions}
    return render(request, 'home.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.all()
    context = {"question": question, "choices": choices}
    return render(request, 'detail.html', context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':

        form = VoteForm(request.POST, question=question)
        if form.is_valid():
            # form already got it and validated
            selected_choice = form.cleaned_data['choice']
            selected_choice.votes += 1
            selected_choice.save()
            # return HttpResponseRedirect('polling:results', question_id=question_id)
            return redirect('detail', question_id=question.id)

        else:
            return redirect('/')


def results(request, question_id):
    pass
