import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Sum
from .forms import QuestionForm, ChoiceForm, VoteForm
from .models import Question, Choice


def home(request):
    questions = Question.objects.exclude(choice__isnull=True)

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
            return HttpResponseRedirect(reverse('results', args=(question.id,)))

        else:
            messages.error(request, "You must select an choice!")
            return redirect('detail', question_id=question.id)


@login_required
def createquestion(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('createchoice', question_id=question.id)
        else:
            return redirect('createquestion')
    else:
        form = QuestionForm()
        return render(request, 'createquestion.html', {'form': form})


@login_required
def createchoice(request, question_id):
    question = get_object_or_404(Question, pk=question_id, author=request.user)
    ChoiceFormset = inlineformset_factory(
        Question, Choice, fields=('choice_text',), extra=1)

    if request.method == 'POST':
        formset = ChoiceFormset(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            return redirect('createchoice', question_id=question.id)
        else:
            messages.error(
                request, 'Something went wrong with creating your choice. (Input 50 characters and above 0 characters)')
            return redirect('createchoice')

    formset = ChoiceFormset(instance=question)
    context = {'formset': formset, 'question': question}
    return render(request, 'createchoice.html', context)


def results(request, question_id):
    question = Question.objects.get(pk=question_id)
    choices = question.choice_set.all()
    total_votes = question.choice_set.aggregate(
        total_votes=Sum('votes')).get('total_votes')
    top_choice = choices[:2]
    sort_leaders = []
    for leaders in top_choice:
        sort_leaders.append(leaders.votes)
        largest = max(sort_leaders)
        occurances = sort_leaders.count(largest)
    if occurances == 1:
        top_choice = choices[:1]
        context = {'question': question,
                   'choices': choices, 'top_choice': top_choice, 'total_votes': total_votes}
    else:
        context = {'question': question,
                   'choices': choices, 'total_votes': total_votes}

    return render(request, 'results.html', context)
