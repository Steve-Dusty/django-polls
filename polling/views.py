import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, ChoiceForm, VoteForm
from .models import Question, Choice


def home(request):
    questions = Question.objects.all()

    question_paginator = Paginator(questions, 5)

    page_num = request.GET.get('page')
    poll = question_paginator.get_page(page_num)

    context = {"questions": questions, "poll": poll}
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
            return redirect('/')

        else:
            messages.error(request, "You must select an choice!")
            return redirect('detail', question_id=question.id)


@login_required
def createpoll(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question(
                question_text=form.cleaned_data['question_text'])  # , do user mode here)
            question.save()
            return redirect('/')
    else:
        form = QuestionForm()
        return render(request, 'createpoll.html', {'form': form})


@login_required
def createchoice(request):
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = Choice(
                choice_text=form.cleaned_data['choice_text'],
                votes=0  # do question
            )
            choice.save()
            return redirect('createpoll')
    else:
        form = ChoiceForm()
        return redirect('createpoll')


def results(request, question_id):
    pass
